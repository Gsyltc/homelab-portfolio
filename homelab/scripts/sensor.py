#!/usr/bin/env python3
"""Exécuteur déterministe des sensors et verification gates du workflow Homelab.

Sous-commandes (Python ≥ 3.9, bibliothèque standard uniquement) :

  list                                          sensors disponibles (manifestes valides)
  describe <id>                                 champs du manifeste
  fire <id> [--path P ...] [--scope S]          exécute un sensor (balayage de gate sans --path)
  gate <frontière> [--scope S] [--attest a,b]   rapport de vérification d'une frontière de phase
  hook [--sensors a,b] [--scope S]              hook d'écriture (stdin JSON harnais) : sensors `fire_on: write`

`--scope` (ou SENSORS_SCOPE) résout la **sévérité conditionnelle** : `severity_overrides`
d'un manifeste et `blocking_on_scope` / `conditional_on_scope` d'une frontière de `gates.md`
(décision humaine ALI-204 + contrôle sécurité Analyste QA, SG-1).

Contrat (README.md) : **advisory**, code retour 0 même en écart (⚠️) ou ⛔, sauf erreur
d'usage (2). `--strict` renvoie 1 s'il y a un écart ou un ⛔ (usage CI uniquement).
Indisponible ≠ conforme (SG-2) ; source = manifeste @ commit (SG-5) ; parsing statique (SG-4).
Aucun sensor n'expose jamais la **valeur** d'un secret (invariant Homelab).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sensorlib.context import Ctx  # noqa: E402
from sensorlib.common import (  # noqa: E402
    GAP, ICONS, OK, UNAVAILABLE, Manifest, Result, glob_match, list_files,
    parse_manifest, source_commit, worst,
)

SENSORS_DIR = Path(__file__).resolve().parents[1] / "sensors" / "sensors"
GATES_FILE = Path(__file__).resolve().parents[1] / "sensors" / "gates.md"
REPO_ANCHOR = Path(__file__).resolve().parents[2]  # racine du dépôt portant les manifestes
SENSOR_REL = "homelab/sensors/sensors"
GATES_REL = "homelab/sensors/gates.md"
SCRIPTS_DIR = Path(__file__).resolve().parent / "sensors"  # un script par sensor : sensors/<id avec _>.py
WRITE_SKIP = (".aidlc-sensors/",)


# --------------------------------------------------------------------------- #
# Manifestes & sévérité conditionnelle (severity_overrides, SG-1)
# --------------------------------------------------------------------------- #


def load_manifests() -> dict[str, Manifest]:
    return {m.id: m for m in (parse_manifest(p) for p in sorted(SENSORS_DIR.glob("*.md")))}


def severity_overrides(manifest: Manifest) -> list[tuple[list[str], str]]:
    """Lit le bloc multi-ligne `severity_overrides:` (liste `- scopes: [...]` / `severity: ...`).

    `parse_manifest` ne lit que le front-matter plat ; ce bloc YAML liste est relu ici
    depuis le texte du manifeste. Retourne [(scopes, severity), ...] (vide si absent).
    """
    text = manifest.path.read_text(encoding="utf-8")
    fm = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.S)
    if not fm:
        return []
    block = fm.group(1)
    m = re.search(r"^severity_overrides:\s*\n(?P<body>(?:[ \t].*\n?|\s*#.*\n?)+)", block, re.M)
    if not m:
        return []
    out: list[tuple[list[str], str]] = []
    scopes: list[str] | None = None
    for line in m.group("body").splitlines():
        if sm := re.search(r"scopes:\s*\[(.*?)\]", line):
            scopes = [s.strip() for s in sm.group(1).split(",") if s.strip()]
        elif vm := re.search(r"severity:\s*(\S+)", line):
            if scopes is not None:
                out.append((scopes, vm.group(1).strip()))
                scopes = None
    return out


def resolve_severity(manifest: Manifest, scope: str | None) -> str:
    """Sévérité effective d'un sensor pour `scope` : override si le scope correspond, sinon défaut."""
    if scope:
        for scopes, sev in severity_overrides(manifest):
            if scope in scopes:
                return sev
    return manifest.severity


def script_path(sid: str) -> Path:
    return SCRIPTS_DIR / (sid.replace("-", "_") + ".py")


def load_check(sid: str):
    """Charge le script du sensor `sid` ; None si absent ou sans `run` / `ID` conforme (=> ⛔, SG-2)."""
    path = script_path(sid)
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(f"homelab_sensor_{path.stem}", path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:  # noqa: BLE001 — un script illisible n'est jamais un vert
        return None
    return mod.run if getattr(mod, "ID", None) == sid and callable(getattr(mod, "run", None)) else None


def resolve_commit() -> str | None:
    return os.environ.get("SENSORS_SOURCE_COMMIT") or source_commit(REPO_ANCHOR)


def run_sensor(sid: str, root: Path, paths: list[str] | None, manifests: dict[str, Manifest],
               commit: str | None) -> list[Result]:
    """Exécute un sensor. Manifeste/implémentation/provenance défaillants => ⛔ (SG-1, SG-2, SG-5)."""
    m = manifests.get(sid)
    if m is None:
        return [Result(sid, "-", UNAVAILABLE, f"indisponible : sensor inconnu « {sid} »")]
    if not m.valid:
        why = f"champs manquants {m.missing}" if m.missing else "kind != deterministic"
        return [Result(sid, "-", UNAVAILABLE, f"indisponible : manifeste invalide ({why}) — provenance non traçable (SG-1)")]
    check = load_check(sid)
    if check is None:
        return [Result(sid, "-", UNAVAILABLE,
                       f"indisponible : script absent ou invalide ({script_path(sid).name})")]
    results: list[Result] = []
    if paths is None:
        targets, explicit = list_files(root, m.matches), False
    else:
        targets, explicit = [], True
        for p in paths:
            rel = _relativize(p, root)
            if rel is None or not (root / rel).is_file():
                results.append(Result(sid, p, UNAVAILABLE, "indisponible : fichier introuvable ou hors du projet"))
            elif m.matches and not glob_match(m.matches, rel):
                results.append(Result(sid, rel, UNAVAILABLE, f"indisponible : hors périmètre (matches: {m.matches})"))
            else:
                targets.append(rel)
        if not targets:
            return results
    try:
        results += check(Ctx(root, targets, explicit))
    except Exception as exc:  # noqa: BLE001 — un sensor en erreur n'est jamais un vert (SG-2)
        results.append(Result(sid, "-", UNAVAILABLE, f"indisponible : erreur d'exécution ({type(exc).__name__}: {exc})"))
    if commit is None:  # SG-5 : provenance non traçable => ⛔
        results = [Result(r.sensor, r.target, UNAVAILABLE, "indisponible : commit des manifestes non traçable (SG-5)", r.findings)
                   for r in results]
    return results


def _relativize(path: str, root: Path) -> str | None:
    p = Path(path)
    p = p if p.is_absolute() else (root / p)
    try:
        return p.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# Rendu
# --------------------------------------------------------------------------- #


def render(results: list[Result], commit: str | None) -> str:
    out = []
    for r in results:
        out.append(f"Sensor {r.sensor} — {r.target}   (source : {SENSOR_REL}/{r.sensor}.md @ {commit or 'indéterminé'})")
        out.append(f"- verdict : {ICONS[r.verdict]} {r.summary}")
        out += [f"  - {f}" for f in r.findings]
    return "\n".join(out)


def emit(results: list[Result], commit: str | None, fmt: str, severities: dict[str, str] | None = None) -> str:
    if fmt == "json":
        payload = {"source_commit": commit, "verdict": worst(results),
                   "results": [r.to_dict() for r in results]}
        if severities:
            payload["severities"] = severities
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return render(results, commit)


# --------------------------------------------------------------------------- #
# Verification gates (format Homelab enrichi : blocking_on_scope / conditional_on_scope / prerequis_40)
# --------------------------------------------------------------------------- #


def parse_boundaries() -> dict[str, dict]:
    """Extrait les frontières du bloc YAML de gates.md (format Homelab enrichi, sans dépendance YAML)."""
    text = GATES_FILE.read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    cur: dict | None = None
    section: str | None = None  # liste en cours : artefacts / prerequis_40 / blocking / conditional
    pending: dict | None = None  # entrée en cours de blocking_on_scope / conditional_on_scope
    for raw in text.splitlines():
        line = raw.rstrip()
        if m := re.match(r"^\s*-\s+id:\s*(\S+)", line):
            cur = {"id": m.group(1), "artefacts": [], "sensors": [], "checks": [],
                   "prerequis_40": [], "blocking_on_scope": [], "conditional_on_scope": []}
            out[cur["id"]] = cur
            section = pending = None
        elif cur is None:
            continue
        elif m := re.match(r"^\s*frontiere:\s*\"?(.*?)\"?\s*$", line):
            cur["frontiere"] = m.group(1)
        elif re.match(r"^\s*artefacts_requis:", line):
            section = "artefacts"
        elif re.match(r"^\s*prerequis_40:", line):
            section = "prerequis_40"
        elif re.match(r"^\s*blocking_on_scope:", line):
            section = "blocking"
        elif re.match(r"^\s*conditional_on_scope:", line):
            section = "conditional"
        elif m := re.match(r"^\s*(checks|sensors):\s*\[(.*?)\]", line):
            section = None
            cur[m.group(1)] = [x.strip() for x in m.group(2).split(",") if x.strip()]
        elif section in ("artefacts", "prerequis_40") and (m := re.match(r"^\s*-\s+(\w+)", line)):
            cur[section].append(m.group(1))
        elif section in ("blocking", "conditional"):
            key = "blocking_on_scope" if section == "blocking" else "conditional_on_scope"
            if m := re.match(r"^\s*-\s+artifact:\s*(\S+)", line):
                pending = {"artifact": m.group(1), "scopes": []}
                cur[key].append(pending)
            elif pending is not None and (m := re.search(r"scopes:\s*\[(.*?)\]", line)):
                pending["scopes"] = [x.strip() for x in m.group(1).split(",") if x.strip()]
            elif pending is not None and (m := re.match(r"^\s*source_stage:\s*(\S+)", line)):
                pending["source_stage"] = m.group(1)
    return out


# Probes d'artefacts spécifiques au Homelab (présence de fichier uniquement, SG-4).
def artefact_status(name: str, root: Path, attested: set[str]) -> tuple[str, str]:
    probes = {
        "livrable_compose_present": lambda: bool(list_files(root, "{**/*compose*.yml,**/*compose*.yaml,**/docker-compose.y*ml}")),
        "livrable_tfvars_present": lambda: bool(list_files(root, "{**/*.tfvars,**/*.tf}")),
    }
    if name in probes:
        return (OK, "présent") if probes[name]() else (GAP, "absent du projet")
    if name in attested:
        return OK, "attesté par le coordinateur (non vérifiable par fichier)"
    return UNAVAILABLE, "non vérifiable par fichier — à attester par le coordinateur (--attest)"


def _is_blocking_artifact(boundary: dict, artifact: str, scope: str | None) -> bool:
    if not scope:
        return False
    for e in boundary["blocking_on_scope"]:
        if e["artifact"] == artifact and scope in e["scopes"]:
            return True
    return False


def _is_conditional_artifact(boundary: dict, artifact: str, scope: str | None) -> bool:
    for e in boundary["conditional_on_scope"]:
        if e["artifact"] == artifact:
            return scope is None or scope in e["scopes"]
    return False


def run_gate(bid: str, root: Path, scope: str | None, attested: set[str], commit: str | None) -> tuple[str, str]:
    boundaries = parse_boundaries()
    b = boundaries.get(bid)
    if b is None:
        raise SystemExit(f"frontière inconnue « {bid} » (disponibles : {', '.join(boundaries)})")
    manifests = load_manifests()
    lines = [f"Rapport de vérification — {bid}   (source : {GATES_REL} @ {commit or 'indéterminé'})",
             f"Frontière : {b.get('frontiere', bid)}" + (f"   (scope : {scope})" if scope else "")]
    verdicts: list[str] = []
    if "artefacts-presents" in b["checks"]:
        lines.append("- artefacts-presents :")
        for a in b["artefacts"]:
            v, d = artefact_status(a, root, attested)
            blocking = _is_blocking_artifact(b, a, scope)
            conditional = _is_conditional_artifact(b, a, scope)
            tag = ""
            if blocking and v != OK:
                tag, v = " (écart BLOQUANT)", GAP
            elif conditional and v != OK:
                tag = " (conditionnel sur ce scope)" if (scope and any(scope in e["scopes"] for e in b["conditional_on_scope"] if e["artifact"] == a)) else " (sans objet hors scope)"
                if not (scope and any(scope in e["scopes"] for e in b["conditional_on_scope"] if e["artifact"] == a)):
                    v = OK  # artefact conditionnel hors scope : sans objet
            verdicts.append(v)
            lines.append(f"    - {a} : {ICONS[v]} {d}{tag}")
    # prérequis §4.0 (présence de fichier non vérifiable : attestation coordinateur)
    if b["prerequis_40"]:
        lines.append("- prérequis §4.0 :")
        for p in b["prerequis_40"]:
            v, d = artefact_status(p, root, attested)
            verdicts.append(v)
            lines.append(f"    - {p} : {ICONS[v]} {d}")
    # sensors de gate — chaque id du champ sensors:, aucune omission (SG-2)
    severities: dict[str, str] = {}
    if b["sensors"]:
        lines.append("Sensors de gate :")
        for s in b["sensors"]:
            rs = run_sensor(s, root, None, manifests, commit)
            m = manifests.get(s)
            sev = resolve_severity(m, scope) if m else "advisory"
            severities[s] = sev
            counts = {v: sum(r.verdict == v for r in rs) for v in (OK, GAP, UNAVAILABLE)}
            detail = ", ".join(f"{ICONS[v]} {n}" for v, n in counts.items() if n)
            sev_tag = " [BLOQUANT]" if sev == "blocking" else ""
            lines.append(f"- {s}{sev_tag} : {ICONS[worst(rs)]} {len(rs)} cible(s) ({detail})")
            shown = [(r.target, f) for r in rs for f in (r.findings or ([r.summary] if r.verdict == UNAVAILABLE else []))]
            lines += [f"    - {t} : {f}" for t, f in shown[:15]]
            if len(shown) > 15:
                lines.append(f"    - … {len(shown) - 15} autre(s) point(s) — voir `fire {s}`")
            verdicts.append(worst(rs))
    overall = worst([Result("g", "-", v, "") for v in verdicts]) if verdicts else OK
    return overall, "\n".join(lines)


# --------------------------------------------------------------------------- #
# Hook d'écriture (PostToolUse Write|Edit) — toujours code 0
# --------------------------------------------------------------------------- #


def hook_file_path(payload: dict) -> str:
    ti = payload.get("tool_input") or payload.get("toolInput") or {}
    for src in (ti, payload):
        for key in ("file_path", "path", "filePath", "target_file"):
            if isinstance(src, dict) and isinstance(src.get(key), str):
                return src[key]
    return ""


def cmd_hook(args: argparse.Namespace) -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        root = Path(getattr(args, "root", None) or payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
        raw = hook_file_path(payload)
        rel = _relativize(raw, root) if raw else None
        if rel is None or any(s in rel + "/" for s in WRITE_SKIP):
            return 0  # pas d'écriture de fichier du projet : rien à faire
        manifests, commit = load_manifests(), resolve_commit()
        scope = args.scope or os.environ.get("SENSORS_SCOPE")
        wanted = {s.strip() for s in args.sensors.split(",")} if args.sensors else None
        results: list[Result] = []
        severities: dict[str, str] = {}
        for sid, m in manifests.items():
            if m.fire_on != "write" or (wanted is not None and sid not in wanted):
                continue
            if m.matches and not glob_match(m.matches, rel):
                continue
            results += run_sensor(sid, root, [rel], manifests, commit)
            severities[sid] = resolve_severity(m, scope)
        if not results:
            return 0
        text = emit(results, commit, "text")
        if args.format == "claude":
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                     "additionalContext": "Sensors advisory (homelab)\n" + text}},
                             ensure_ascii=False))
        else:
            print(text)
    except Exception as exc:  # noqa: BLE001 — un hook ne bloque jamais, mais il ne se tait pas (SG-2)
        print(f"Sensor hook — ⛔ indisponible : {type(exc).__name__}: {exc}", file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="racine du projet à vérifier (défaut : répertoire courant)")
    ap.add_argument("--strict", action="store_true", help="code 1 si écart ou ⛔ (CI uniquement ; le défaut est advisory)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    d = sub.add_parser("describe")
    d.add_argument("id")
    f = sub.add_parser("fire")
    f.add_argument("id")
    f.add_argument("--path", nargs="+", help="fichier(s) à vérifier ; absent = balayage de gate")
    f.add_argument("--scope", help="scope actif (résout la sévérité conditionnelle)")
    f.add_argument("--format", choices=["text", "json"], default="text")
    g = sub.add_parser("gate")
    g.add_argument("boundary", nargs="?")
    g.add_argument("--scope", help="scope actif (résout blocking_on_scope / conditional_on_scope)")
    g.add_argument("--attest", default="", help="artefacts abstraits attestés par le coordinateur (a,b)")
    h = sub.add_parser("hook")
    h.add_argument("--root", default=argparse.SUPPRESS, help="racine du projet (aussi accepté avant la sous-commande)")
    h.add_argument("--sensors", help="restreint aux ids déclarés par le stage actif (a,b)")
    h.add_argument("--scope", help="scope actif (résout la sévérité conditionnelle)")
    h.add_argument("--format", choices=["text", "claude"], default="text")
    args = ap.parse_args(argv)
    root = Path(args.root or os.getcwd())

    if args.cmd == "hook":
        if not hasattr(args, "scope"):
            args.scope = None
        return cmd_hook(args)
    manifests, commit = load_manifests(), resolve_commit()
    if args.cmd == "list":
        for m in manifests.values():
            script = script_path(m.id)
            impl = f"homelab/scripts/sensors/{script.name}" if load_check(m.id) and m.valid else "⛔ script absent/invalide"
            ov = severity_overrides(m)
            sev = m.severity + (f" (override: {','.join(s for sc, _ in ov for s in sc)})" if ov else "")
            print(f"{m.id:22} fire_on={m.fire_on:5} sev={sev:28} {impl:42} {m.description[:50]}")
        return 0
    if args.cmd == "describe":
        m = manifests.get(args.id)
        if not m:
            print(f"sensor inconnu : {args.id}", file=sys.stderr)
            return 2
        meta = dict(m.meta)
        ov = severity_overrides(m)
        if ov:
            meta["severity_overrides"] = [{"scopes": sc, "severity": sv} for sc, sv in ov]
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "fire":
        results = run_sensor(args.id, root, args.path, manifests, commit)
        m = manifests.get(args.id)
        sev = resolve_severity(m, args.scope) if m else "advisory"
        print(emit(results, commit, args.format, {args.id: sev} if args.format == "json" else None))
        if args.format != "json" and sev == "blocking" and worst(results) == GAP:
            print(f"\n⚠️ sévérité BLOQUANTE sur scope « {args.scope} » : écart à corriger ou lever explicitement (SG-1).")
        return 1 if args.strict and worst(results) != OK else 0
    if args.cmd == "gate":
        if not args.boundary:
            print("frontières : " + ", ".join(parse_boundaries()))
            return 0
        verdict, report = run_gate(args.boundary, root, args.scope, {a for a in args.attest.split(",") if a}, commit)
        print(report)
        return 1 if args.strict and verdict != OK else 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
