#!/usr/bin/env python3
"""Sensor `yaml-validity` — applique le bloc `checks` de `homelab/sensors/sensors/yaml-validity.md`.

Vérifie qu'un livrable compose parse en YAML valide (syntaxe seule, sans rendu ni réseau) :
document unique, aucune clé dupliquée au même niveau. Parsing **statique** (SG-4).

Exécution seule : `python3 homelab/scripts/sensors/yaml_validity.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import Result  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402
from sensorlib import yamlmini  # noqa: E402

ID = "yaml-validity"


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    for rel in ctx.targets:
        text = ctx.text(rel)
        gaps: list[str] = []
        try:
            yamlmini.parse(text)
        except yamlmini.YamlError as exc:
            gaps.append(str(exc))
        ndoc = yamlmini.split_documents(text)
        if ndoc > 1:
            gaps.append(f"document_unique : {ndoc} documents YAML (séparateurs `---`) — un seul attendu par stack")
        results.append(res(sid, rel, gaps, "YAML valide (syntaxe, document unique, pas de clé dupliquée)",
                           "erreur de parsing"))
    return results or no_scope(sid, "aucun fichier .yml/.yaml dans le périmètre")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
