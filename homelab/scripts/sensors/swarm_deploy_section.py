#!/usr/bin/env python3
"""Sensor `swarm-deploy-section` — applique `homelab/sensors/sensors/swarm-deploy-section.md`.

Vérifie que chaque service du docker-compose livré porte une section `deploy` compatible
Docker Swarm, et signale les directives non honorées en Swarm (`restart`, `depends_on`).
Parsing **statique** (SG-4) ; si le fichier ne parse pas, ⛔ indisponible (SG-2).

Exécution seule : `python3 homelab/scripts/sensors/swarm_deploy_section.py --root <projet> [--path <fichier>...]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import UNAVAILABLE, Result  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402
from sensorlib import yamlmini  # noqa: E402

ID = "swarm-deploy-section"
NON_SWARM = ("restart", "depends_on")


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    for rel in ctx.targets:
        try:
            root = yamlmini.parse(ctx.text(rel))
        except yamlmini.YamlError as exc:
            results.append(Result(sid, rel, UNAVAILABLE, f"indisponible : YAML non analysable ({exc})"))
            continue
        services = yamlmini.services(root)
        if not services:
            results.append(Result(sid, rel, UNAVAILABLE,
                                  "indisponible : aucune section `services:` exploitable (pas un compose ?)"))
            continue
        gaps: list[str] = []
        for name, node in services.items():
            keys = node.mapping if node.kind == "map" else {}
            if "deploy" not in keys:
                gaps.append(f"service « {name} » : section `deploy` absente (requise en Swarm)")
            else:
                dep = keys["deploy"].mapping if keys["deploy"].kind == "map" else {}
                placement = dep.get("placement")
                if not (placement and placement.kind == "map" and "constraints" in placement.mapping):
                    gaps.append(f"service « {name} » : `deploy.placement.constraints` absent (recommandé, advisory)")
            for d in NON_SWARM:
                if d in keys:
                    gaps.append(f"service « {name} » : directive non-Swarm `{d}` (ignorée/remplacée en Swarm)")
        results.append(res(sid, rel, gaps,
                           f"section `deploy` présente sur {len(services)} service(s)",
                           "service(s) sans deploy / directive non-Swarm"))
    return results or no_scope(sid, "aucun fichier .yml/.yaml dans le périmètre")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
