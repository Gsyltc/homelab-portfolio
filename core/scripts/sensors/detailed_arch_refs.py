#!/usr/bin/env python3
"""Sensor `detailed-arch-refs` — applique le bloc `checks` de `core/sensors/sensors/detailed-arch-refs.md`.

Exécution seule : `python3 core/scripts/sensors/detailed_arch_refs.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import Result, code_mask, strip_comments  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402


ID = "detailed-arch-refs"


_BAD_LINK = re.compile(r"\]\([^)\s]*(?:architecture-detaillee|architecture-securite)/[^)\s]*\.md[^)]*\)")
_SYS_SUFFIX = re.compile(r"\s\((?:SYS|SYSTEM|SYSTÈME)-?\d+[^)]*\)\s*$", re.I)


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    for rel in ctx.targets:
        lines = strip_comments(ctx.text(rel)).splitlines()
        mask, gaps = code_mask(lines), []
        for i, line in enumerate(lines, 1):
            if mask[i - 1]:
                continue
            for m in _BAD_LINK.finditer(line):
                gaps.append(f"ligne {i} : renvoi par chemin de fichier {m.group(0)[2:-1]!r} (attendu : documentation/<SS>#<ancre>)")
            if re.match(r"^#{1,6}\s", line) and _SYS_SUFFIX.search(line):
                gaps.append(f"ligne {i} : titre avec suffixe de système « {line.strip()} »")
        results.append(res(sid, rel, gaps, "conforme", "renvoi/titre non conforme"))
    return results or no_scope(sid, "documentation/**/*.md")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
