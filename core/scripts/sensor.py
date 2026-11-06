#!/usr/bin/env python3
"""Exécuteur déterministe des sensors et verification gates du workflow `core`.

Sous-commandes (Python ≥ 3.9, bibliothèque standard uniquement) :

  list                                  sensors disponibles (manifestes valides)
  describe <id>                         champs du manifeste
  fire <id> [--path P ...]              exécute un sensor (balayage de gate sans --path)
  gate <frontière> [--attest a,b]       rapport de vérification d'une frontière de phase
  hook [--sensors a,b]                  hook d'écriture (stdin JSON harnais) : sensors `fire_on: write`

Contrat (README.md) : **advisory**, code retour 0 même en écart (⚠️) ou ⛔, sauf erreur
d'usage (2). `--strict` renvoie 1 s'il y a un écart ou un ⛔ (usage CI uniquement).
Indisponible ≠ conforme (SG-2) ; source = manifeste @ commit (SG-5) ; parsing statique (SG-4).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sensorlib.context import Ctx  # noqa: E402
from sensorlib.diagrams import blocks as diagram_blocks  # noqa: E402
from sensorlib.common import (  # noqa: E402
    GAP, ICONS, OK, UNAVAILABLE, Manifest, Result, glob_match, list_files,
    parse_manifest, source_commit, worst,
)

SENSORS_DIR = Path(__file__).resolve().parents[1] / "sensors" / "sensors"
GATES_FILE = Path(__file__).resolve().parents[1] / "sensors" / "gates.md"
REPO_ANCHOR = Path(__file__).resolve().parents[2]  # racine du dépôt portant les manifestes
SENSOR_REL = "core/sensors/sensors"
SCRIPTS_DIR = Path(__file__).resolve().parent / "sensors"  # un script par sensor : sensors/<id avec _>.py
WRITE_SKIP = (".aidlc-sensors/",)


# --------------------------------------------------------------------------- #
# Manifestes & exécution
# --------------------------------------------------------------------------- #


def load_manifests() -> dict[str, Manifest]:
    return {m.id: m for m in (parse_manifest(p) for p in sorted(SENSORS_DIR.glob("*.md")))}


def script_path(sid: str) -> Path:
    return SCRIPTS_DIR / (sid.replace("-", "_") + ".py")


def load_check(sid: str):
    """Charge le script du sensor `sid` ; None si absent ou sans `run` / `ID` conforme (=> ⛔, SG-2)."""
    path = script_path(sid)
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(f"core_sensor_{path.stem}", path)
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
                       f"indisponible : script absent ou invalide ({script_path(sid).relative_to(SCRIPTS_DIR.parent.parent.parent).as_posix()})")]
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


def emit(results: list[Result], commit: str | None, fmt: str) -> str:
    if fmt == "json":
        return json.dumps({"source_commit": commit, "verdict": worst(results),
                           "results": [r.to_dict() for r in results]}, ensure_ascii=False, indent=2)
    return render(results, commit)


# --------------------------------------------------------------------------- #
# Verification gates
# --------------------------------------------------------------------------- #


def parse_boundaries() -> dict[str, dict]:
    """Extrait les frontières du bloc YAML de gates.md (format plat maîtrisé, sans dépendance YAML)."""
    text = GATES_FILE.read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    cur: dict | None = None
    in_list = False
    for line in text.splitlines():
        if m := re.match(r"^\s*-\s+id:\s*(\S+)", line):
            cur = {"id": m.group(1), "artefacts": [], "sensors": [], "checks": []}
            out[cur["id"]] = cur
            in_list = False
        elif cur is None:
            continue
        elif m := re.match(r"^\s*frontiere:\s*\"?(.*?)\"?\s*$", line):
            cur["frontiere"] = m.group(1)
        elif re.match(r"^\s*artefacts_requis:", line):
            in_list = True
        elif in_list and (m := re.match(r"^\s*-\s+(\w+)", line)):
            cur["artefacts"].append(m.group(1))
        elif m := re.match(r"^\s*(checks|sensors):\s*\[(.*?)\]", line):
            in_list = False
            cur[m.group(1)] = [x.strip() for x in m.group(2).split(",") if x.strip()]
    return out


def _has_diagram(root: Path) -> bool:
    for rel in list_files(root, "{documentation/**/*.md,**/*.puml,**/*.dsl}"):
        if rel.endswith((".puml", ".dsl")) or diagram_blocks((root / rel).read_text(encoding="utf-8", errors="replace")):
            return True
    return False


def artefact_status(name: str, root: Path, attested: set[str]) -> tuple[str, str]:
    probes = {
        "adr_conception": lambda: bool(list_files(root, "decisions/[0-9][0-9][0-9][0-9]-*.md")),
        "adr_a_jour": lambda: bool(list_files(root, "decisions/[0-9][0-9][0-9][0-9]-*.md")),
        "livrables_detailles": lambda: bool(list_files(root, "documentation/*.md")),
        "diagramme_principal": lambda: _has_diagram(root),
    }
    if name in probes:
        return (OK, "présent") if probes[name]() else (GAP, "absent du projet")
    if name in attested:
        return OK, "attesté par le coordinateur (non vérifiable par fichier)"
    return UNAVAILABLE, "non vérifiable par fichier — à attester par le coordinateur (--attest)"


def run_gate(bid: str, root: Path, attested: set[str], commit: str | None) -> tuple[str, str]:
    boundaries = parse_boundaries()
    b = boundaries.get(bid)
    if b is None:
        raise SystemExit(f"frontière inconnue « {bid} » (disponibles : {', '.join(boundaries)})")
    manifests = load_manifests()
    needed = list(dict.fromkeys(b["sensors"] + [s for s in ("traceability", "upstream-coverage")
                                               if "liaison-tracabilite" in b["checks"] or "absence-orphelin" in b["checks"]]))
    by_sensor = {s: run_sensor(s, root, None, manifests, commit) for s in needed}
    lines = [f"Rapport de vérification — {bid}   (source : core/sensors/gates.md @ {commit or 'indéterminé'})",
             f"Frontière : {b.get('frontiere', bid)}"]
    verdicts: dict[str, str] = {}
    if "artefacts-presents" in b["checks"]:
        art = {a: artefact_status(a, root, attested) for a in b["artefacts"]}
        verdicts["artefacts-presents"] = worst([Result("g", a, v, d) for a, (v, d) in art.items()])
        lines.append(f"- artefacts-presents : {ICONS[verdicts['artefacts-presents']]}")
        lines += [f"    - {a} : {ICONS[v]} {d}" for a, (v, d) in art.items()]
    for check, sensor in (("liaison-tracabilite", "traceability"), ("absence-orphelin", "upstream-coverage")):
        if check in b["checks"]:
            verdicts[check] = worst(by_sensor[sensor])
            lines.append(f"- {check} : {ICONS[verdicts[check]]} (via sensor {sensor})")
    if b["sensors"]:
        lines.append("Sensors de gate :")
        for s in b["sensors"]:
            rs = by_sensor[s]
            counts = {v: sum(r.verdict == v for r in rs) for v in (OK, GAP, UNAVAILABLE)}
            detail = ", ".join(f"{ICONS[v]} {n}" for v, n in counts.items() if n)
            lines.append(f"- {s} : {ICONS[worst(rs)]} {len(rs)} cible(s) ({detail})")
            shown = [(r.target, f) for r in rs for f in (r.findings or ([r.summary] if r.verdict == UNAVAILABLE else []))]
            lines += [f"    - {t} : {f}" for t, f in shown[:15]]
            if len(shown) > 15:
                lines.append(f"    - … {len(shown) - 15} autre(s) point(s) — voir `fire {s}`")
    overall = worst([Result("g", "-", v, "") for v in verdicts.values()] + [r for rs in by_sensor.values() for r in rs]) \
        if verdicts or by_sensor else OK
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
        root = Path(args.root or payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
        raw = hook_file_path(payload)
        rel = _relativize(raw, root) if raw else None
        if rel is None or any(s in rel + "/" for s in WRITE_SKIP):
            return 0  # pas d'écriture de fichier du projet : rien à faire
        manifests, commit = load_manifests(), resolve_commit()
        wanted = {s.strip() for s in args.sensors.split(",")} if args.sensors else None
        results: list[Result] = []
        for sid, m in manifests.items():
            if m.fire_on != "write" or (wanted is not None and sid not in wanted):
                continue
            if m.matches and not glob_match(m.matches, rel):
                continue
            results += run_sensor(sid, root, [rel], manifests, commit)
        # une cible sans diagramme (aucun contenu à vérifier) renvoie ⛔ « périmètre » : bruit à l'écriture
        results = [r for r in results if not (r.verdict == UNAVAILABLE and "aucun diagramme" in r.summary)]
        if not results:
            return 0
        text = emit(results, commit, "text")
        _append_audit(args.audit_file, text)
        if args.format == "claude":
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                     "additionalContext": "Sensors advisory (core)\n" + text}},
                             ensure_ascii=False))
        else:
            print(text)
    except Exception as exc:  # noqa: BLE001 — un hook ne bloque jamais, mais il ne se tait pas (SG-2)
        print(f"Sensor hook — ⛔ indisponible : {type(exc).__name__}: {exc}", file=sys.stderr)
    return 0


def _append_audit(path: str | None, text: str) -> None:
    """Hors Multica : piste d'audit append-only dans un fichier (ADR 0038, capacité AUDIT dégradée)."""
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(f"\n<!-- {datetime.now(timezone.utc).isoformat(timespec='seconds')} -->\n{text}\n")


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
    f.add_argument("--format", choices=["text", "json"], default="text")
    g = sub.add_parser("gate")
    g.add_argument("boundary", nargs="?")
    g.add_argument("--attest", default="", help="artefacts abstraits attestés par le coordinateur (a,b)")
    h = sub.add_parser("hook")
    h.add_argument("--root", default=argparse.SUPPRESS, help="racine du projet (aussi accepté avant la sous-commande)")
    h.add_argument("--sensors", help="restreint aux ids déclarés par le stage actif (a,b)")
    h.add_argument("--format", choices=["text", "claude"], default="text")
    h.add_argument("--audit-file", help="ajoute le rapport à ce fichier (audit append-only hors Multica)")
    args = ap.parse_args(argv)
    root = Path(args.root or os.getcwd())

    if args.cmd == "hook":
        return cmd_hook(args)
    manifests, commit = load_manifests(), resolve_commit()
    if args.cmd == "list":
        for m in manifests.values():
            script = script_path(m.id)
            impl = f"core/scripts/sensors/{script.name}" if load_check(m.id) and m.valid else "⛔ script absent/invalide"
            print(f"{m.id:20} fire_on={m.fire_on:5} {impl:50} {m.description[:60]}")
        return 0
    if args.cmd == "describe":
        m = manifests.get(args.id)
        if not m:
            print(f"sensor inconnu : {args.id}", file=sys.stderr)
            return 2
        print(json.dumps(m.meta, ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "fire":
        results = run_sensor(args.id, root, args.path, manifests, commit)
        print(emit(results, commit, args.format))
        return 1 if args.strict and worst(results) != OK else 0
    if args.cmd == "gate":
        if not args.boundary:
            print("frontières : " + ", ".join(parse_boundaries()))
            return 0
        verdict, report = run_gate(args.boundary, root, {a for a in args.attest.split(",") if a}, commit)
        print(report)
        return 1 if args.strict and verdict != OK else 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
