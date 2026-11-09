#!/usr/bin/env python3
"""Sensor `terraform-no-sni` — applique `homelab/sensors/sensors/terraform-no-sni.md`.

Vérifie l'**absence de `${SNI}` / `$SNI`** dans les fichiers Terraform livrés (`.tf` / `.tfvars`) :
le workflow impose d'y écrire les domaines/URLs en clair, pas `${SNI}`. Les paramètres de
workflow (`${stack_name}`, `${auth_type}`, …) restent autorisés et ne sont pas visés.
Parsing **statique** par motif (SG-4).

Exécution seule : `python3 homelab/scripts/sensors/terraform_no_sni.py --root <projet> [--path <fichier>...]`
(advisory par défaut ; bloquant sur `security-patch` / `new-stack` — résolu par le dispatcher).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import Result  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402

ID = "terraform-no-sni"
_SNI = re.compile(r"\$\{?SNI\}?")


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    for rel in ctx.targets:
        gaps: list[str] = []
        for i, line in enumerate(ctx.text(rel).splitlines(), 1):
            if _SNI.search(line):
                gaps.append(f"{rel}:{i} — `${{SNI}}` présent (domaine/URL en clair attendu)")
        results.append(res(sid, rel, gaps, "aucun ${SNI}", "${SNI} présent"))
    return results or no_scope(sid, "aucun fichier .tf/.tfvars dans le périmètre")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
