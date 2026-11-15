#!/usr/bin/env python3
"""Sensor `version-livrables` — applique `homelab/sensors/sensors/version-livrables.md`.

Compare le `sha256` de chaque livrable (compose, `.tfvars`) du répertoire de relecture à la version
enregistrée dans `versions.json`, et vérifie que chaque verdict de sensor requis existe pour ce `sha256`.
Lecture seule, parsing statique (SG-4) : seules des empreintes sont calculées.

Exécution seule : `python3 homelab/scripts/sensors/version_livrables.py --root <projet> [--path <versions.json>...]`
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import UNAVAILABLE, Result  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402

ID = "version-livrables"

REQUIRED = {
    "compose": ("yaml-validity", "plaintext-secret", "swarm-deploy-section", "traefik-coherence"),
    "tfvars": ("terraform-no-sni", "plaintext-secret"),
}
VERDICTS = {"conforme", "ecart", "indisponible"}
NOT_DELIVERABLE = {"versions.json", "parametres.json", "preselection.json"}


def kind(name: str) -> str | None:
    if name.endswith(".tfvars"):
        return "tfvars"
    if name.endswith((".yml", ".yaml")):
        return "compose"
    return None


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check(data: dict, folder: Path) -> list[str]:
    gaps: list[str] = []
    livrables = data.get("livrables")
    if not isinstance(livrables, dict) or not livrables:
        return ["livrables : objet non vide attendu"]
    for name, entry in livrables.items():
        k = kind(name)
        if k is None:
            gaps.append(f"{name} : type de livrable inconnu (compose .yml/.yaml ou .tfvars)")
            continue
        if not isinstance(entry, dict) or not isinstance(entry.get("sha256"), str):
            gaps.append(f"{name} : sha256 manquant dans versions.json")
            continue
        path = folder / name
        if not path.is_file():
            gaps.append(f"{name} : fichier absent du répertoire")
            continue
        actual = sha256(path)
        if actual != entry["sha256"]:
            gaps.append(f"{name} : sha256 différent de la version validée (fichier modifié depuis)")
            continue
        verdicts = entry.get("verdicts") if isinstance(entry.get("verdicts"), dict) else {}
        for sid in REQUIRED[k]:
            v = verdicts.get(sid)
            if not isinstance(v, dict) or v.get("verdict") not in VERDICTS:
                gaps.append(f"{name} : verdict `{sid}` absent")
            elif v.get("sha256") != actual:
                gaps.append(f"{name} : verdict `{sid}` périmé (autre sha256)")
    registered = set(livrables)
    for f in sorted(folder.iterdir()):
        if f.is_file() and f.name not in NOT_DELIVERABLE and kind(f.name) and f.name not in registered:
            gaps.append(f"{f.name} : livrable non enregistré dans versions.json")
    return gaps


def run(ctx: Ctx) -> list[Result]:
    results: list[Result] = []
    for rel in ctx.targets:
        try:
            data = json.loads(ctx.text(rel))
        except json.JSONDecodeError as exc:
            results.append(Result(ID, rel, UNAVAILABLE, f"indisponible : JSON invalide (ligne {exc.lineno})"))
            continue
        if not isinstance(data, dict):
            results.append(Result(ID, rel, UNAVAILABLE, "indisponible : objet JSON attendu"))
            continue
        gaps = check(data, (ctx.root / rel).parent)
        results.append(res(ID, rel, gaps, "livrables identiques à la version validée",
                           "livrables ou verdicts non conformes à la version validée"))
    return results or no_scope(ID, "aucun versions.json sous .a-valider/<id-tâche>/<stack>/")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
