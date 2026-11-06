#!/usr/bin/env python3
"""Sensor `upstream-coverage` — applique le bloc `checks` de `core/sensors/sensors/upstream-coverage.md`.

Exécution seule : `python3 core/scripts/sensors/upstream_coverage.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from sensorlib.common import GAP, OK, Result, find_section, has_content, sections  # noqa: E402
from sensorlib.context import Ctx, ISSUE_RE, ADR_PATH, no_scope, res  # noqa: E402


ID = "upstream-coverage"


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    ensemble: list[str] = []
    for rel in ctx.targets:
        text = ctx.text(rel)
        if ADR_PATH.match(rel):
            gaps = []
            refs = find_section(sections(text), "Références")
            if not (refs and has_content(refs.body)):
                gaps.append("section « Références » absente ou vide")
            if not ISSUE_RE.search(text):
                gaps.append("aucune référence à l'issue d'origine (ALI-/HOM-/ORIG-<n>)")
            results.append(res(sid, rel, gaps, "référence amont présente", "référence amont manquante"))
        else:
            ensemble.append(rel)
    if ensemble:  # documentation/ et livrables/ : évalués en ensemble
        cited = [r for r in ensemble if ISSUE_RE.search(ctx.text(r))]
        if cited:
            results.append(Result(sid, f"ensemble ({len(ensemble)} fichier(s))", OK,
                                  f"référence amont présente ({len(cited)}/{len(ensemble)} fichier(s) citent l'issue)"))
        else:
            results.append(Result(sid, f"ensemble ({len(ensemble)} fichier(s))", GAP,
                                  "aucune référence amont détectée", [f"sans référence : {r}" for r in ensemble]))
    return results or no_scope(sid, "décisions, documentation ou livrables")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
