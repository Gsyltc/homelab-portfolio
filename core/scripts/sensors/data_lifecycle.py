#!/usr/bin/env python3
"""Sensor `data-lifecycle` — applique le bloc `checks` de `core/sensors/sensors/data-lifecycle.md`.

Exécution seule : `python3 core/scripts/sensors/data_lifecycle.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import GAP, Result, find_section, has_content, sections  # noqa: E402
from sensorlib.context import Ctx, res  # noqa: E402
from sensorlib.sections import section_gaps  # noqa: E402

ID = "data-lifecycle"


DL_FILE = "documentation/10-cycle_vie_donnees.md"
DL_SECTIONS = ["Cycle de vie des données", "Gouvernance de données", "Classification des données"]
_LIFECYCLE = re.compile(r"collecte|stockage|utilisation|archivage|suppression|conservation|r[ée]tention|destruction|purge", re.I)
_LEVEL = re.compile(r"public|interne|confidentiel|restreint|sensible|secret|personnel|pii|rp|nominatif|classifi", re.I)


def run(ctx: Ctx) -> list[Result]:
    sid = ID
    if not ctx.exists(DL_FILE):
        return [Result(sid, DL_FILE, GAP, "fichier absent", [f"{DL_FILE} introuvable dans le projet"])]
    secs = sections(ctx.text(DL_FILE))
    gaps = section_gaps(ctx.text(DL_FILE), DL_SECTIONS)
    cycle, klass = find_section(secs, DL_SECTIONS[0]), find_section(secs, DL_SECTIONS[2])
    if cycle and has_content(cycle.body) and not _LIFECYCLE.search("\n".join(cycle.body)):
        gaps.append("aucune donnée rattachée à une étape du cycle de vie (collecte/stockage/utilisation/archivage/suppression)")
    if klass and has_content(klass.body) and not _LEVEL.search("\n".join(klass.body)):
        gaps.append("aucune donnée du projet classifiée (niveau de sensibilité absent)")
    return [res(sid, DL_FILE, gaps, "présent et renseigné (données projet classifiées + rattachées au cycle)", "document incomplet")]


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
