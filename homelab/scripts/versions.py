#!/usr/bin/env python3
"""Génère `versions.json` (sensor `version-livrables`) à partir des YAML de retour et de rapport.

`python3 homelab/scripts/versions.py record --dir <.a-valider/<id-tâche>/<stack>> <retour.yaml>...`

Le Tech Lead télécharge les YAML joints (`multica attachment download`) puis lance cette commande. Le script
calcule le `sha256` de chaque livrable (compose, `.tfvars`) du répertoire, lit les verdicts de sensors des YAML
(`sensors_resultats[]` d'un message A2A, `sensors[]` / `report.sensors[]` d'un rapport reviewer) et rattache chaque
verdict au livrable dont le `sha256` correspond. Un verdict sans `sha256`, ou d'une autre version, est **ignoré** et
signalé, jamais deviné. Si plusieurs verdicts existent pour un même couple (livrable, sensor), le plus défavorable
l'emporte (indisponible > ecart > conforme). Rien n'est lu dans les livrables au-delà de leur empreinte.

Requiert PyYAML (YAML joints en notation flow). Sans PyYAML ou sur YAML illisible : code 2, aucun fichier écrit.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "sensors"))

from version_livrables import NOT_DELIVERABLE, REQUIRED, kind, sha256  # noqa: E402

RANK = {"conforme": 0, "ecart": 1, "indisponible": 2}


def load_yaml(path: Path):
    try:
        import yaml
    except ImportError:
        raise SystemExit("PyYAML requis pour lire les YAML joints (pip install pyyaml) : aucun fichier écrit")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise SystemExit(f"{path} : YAML illisible ({exc.__class__.__name__}) : aucun fichier écrit")


def entries(doc) -> list[dict]:
    """Verdicts de sensors d'un document : A2A (`sensors_resultats`) ou rapport reviewer (`sensors`)."""
    if not isinstance(doc, dict):
        return []
    root = doc.get("report") if isinstance(doc.get("report"), dict) else doc
    out: list[dict] = []
    for key, idkey in (("sensors_resultats", "sensor"), ("sensors", "id")):
        for e in root.get(key) or []:
            if isinstance(e, dict) and e.get(idkey):
                out.append({"sensor": str(e[idkey]), "verdict": e.get("verdict"), "sha256": e.get("sha256")})
    return out


def record(folder: Path, retours: list[Path]) -> tuple[dict, list[str]]:
    livrables = {}
    for f in sorted(folder.iterdir()):
        if f.is_file() and f.name not in NOT_DELIVERABLE and kind(f.name):
            livrables[f.name] = {"sha256": sha256(f), "verdicts": {}}
    by_sha = {v["sha256"]: name for name, v in livrables.items()}
    notes: list[str] = []
    for r in retours:
        for e in entries(load_yaml(r)):
            sha, verdict = e["sha256"], e["verdict"]
            name = by_sha.get(sha.lower()) if isinstance(sha, str) else None
            if verdict not in RANK:
                notes.append(f"{r.name} : verdict `{e['sensor']}` ignoré (valeur « {verdict} » inconnue)")
            elif name is None:
                notes.append(f"{r.name} : verdict `{e['sensor']}` ignoré (sha256 absent ou autre version)")
            else:
                cur = livrables[name]["verdicts"].get(e["sensor"])
                if cur is None or RANK[verdict] > RANK[cur["verdict"]]:
                    livrables[name]["verdicts"][e["sensor"]] = {"verdict": verdict, "sha256": sha.lower()}
    for name, v in livrables.items():
        for sid in REQUIRED[kind(name)]:
            if sid not in v["verdicts"]:
                notes.append(f"{name} : verdict `{sid}` manquant pour ce sha256")
    return {"livrables": livrables}, notes


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Génère versions.json pour le sensor version-livrables.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record", help="écrit <dir>/versions.json")
    r.add_argument("--dir", required=True, help="répertoire de relecture .a-valider/<id-tâche>/<stack>")
    r.add_argument("retours", nargs="+", help="YAML retour / rapport (téléchargés depuis l'issue)")
    args = ap.parse_args(argv)
    folder = Path(args.dir)
    if not folder.is_dir():
        print(f"{folder} : répertoire introuvable", file=sys.stderr)
        return 2
    data, notes = record(folder, [Path(p) for p in args.retours])
    if not data["livrables"]:
        print(f"{folder} : aucun livrable (compose ou .tfvars)", file=sys.stderr)
        return 2
    (folder / "versions.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"versions.json écrit : {', '.join(data['livrables'])}")
    for n in notes:
        print(f"- {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
