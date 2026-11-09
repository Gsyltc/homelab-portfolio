#!/usr/bin/env python3
"""Sensor `traefik-coherence` — applique `homelab/sensors/sensors/traefik-coherence.md`.

Contrôle de **surface** de la cohérence Traefik du compose livré : présence des labels de
routage (`traefik.enable`, router rule, entrypoint) et appartenance au réseau Traefik.
**Ne réimplémente pas** l'analyse Traefik : l'autorité reste le check `traefik-manager-read`
(skill de l'Analyste QA). Parsing **statique / lecture seule** (SG-4), jamais d'écriture.

Exécution seule : `python3 homelab/scripts/sensors/traefik_coherence.py --root <projet> [--path <fichier>...]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import UNAVAILABLE, Result  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402
from sensorlib import yamlmini  # noqa: E402

ID = "traefik-coherence"

_ENABLE = re.compile(r"traefik\.enable\s*[:=]\s*[\"']?true", re.I)
_ROUTER_RULE = re.compile(r"traefik\.http\.routers\..+\.rule", re.I)
_ENTRYPOINT = re.compile(r"traefik\.http\.routers\..+\.entrypoints", re.I)
_TRAEFIK_NET = re.compile(r"traefik", re.I)


def _service_text(node: yamlmini.Node) -> str:
    """Reconstitue un texte plat des scalaires d'un service (labels/networks en liste ou map)."""
    out: list[str] = []

    def walk(n: yamlmini.Node) -> None:
        if n.scalar:
            out.append(n.scalar)
        for k in n.key_order:
            out.append(k)
            walk(n.mapping[k])
        for it in n.items:
            walk(it)

    walk(node)
    return "\n".join(out)


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
        exposed = 0
        for name, node in services.items():
            text = _service_text(node)
            if not _ENABLE.search(text) and "traefik.enable" not in text:
                continue  # service non exposé via Traefik : hors périmètre de cohérence
            exposed += 1
            if not _ROUTER_RULE.search(text):
                gaps.append(f"service « {name} » : aucune `traefik.http.routers.<r>.rule` (règle de routage)")
            if not _ENTRYPOINT.search(text):
                gaps.append(f"service « {name} » : aucun `entrypoints` déclaré (advisory)")
            if not _TRAEFIK_NET.search(text):
                gaps.append(f"service « {name} » : aucune appartenance visible au réseau Traefik")
        if exposed == 0:
            results.append(Result(sid, rel, UNAVAILABLE,
                                  "indisponible : aucun service exposé via Traefik détecté (rien à corréler)"))
            continue
        results.append(res(sid, rel, gaps,
                           f"cohérence de surface Traefik OK ({exposed} service(s) exposé(s)) — autorité : traefik-manager-read",
                           "incohérence Traefik de surface"))
    return results or no_scope(sid, "aucun fichier .yml/.yaml dans le périmètre")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
