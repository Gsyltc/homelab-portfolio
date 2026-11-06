#!/usr/bin/env python3
"""Sensor `claim-sources` — applique le bloc `checks` de `core/sensors/sensors/claim-sources.md`.

Exécution seule : `python3 core/scripts/sensors/claim_sources.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import Result, code_mask, find_section, has_content, sections, strip_comments  # noqa: E402
from sensorlib.context import Ctx, ADR_PATH, no_scope, res  # noqa: E402


ID = "claim-sources"


_MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_ADR_REF = re.compile(r"\bADR[- ]?(\d{4})\b", re.I)
_HYPOTHESIS = re.compile(r"hypoth[eè]se", re.I)
_CONFIRMED = re.compile(r"confirm(?:ée?|ation)\s+(?:humaine|par)|valid[ée]e?\s+par|confirm[ée]\s+le|✅", re.I)


def _with_continuation(lines: list[str], i: int) -> str:
    """Ligne `i` (1-based) + la suivante, si celle-ci ne porte pas une autre hypothèse."""
    nxt = lines[i] if i < len(lines) and not _HYPOTHESIS.search(lines[i]) else ""
    return f"{lines[i - 1]} {nxt}"


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    for rel in ctx.targets:
        lines = strip_comments(ctx.text(rel)).splitlines()
        mask, gaps = code_mask(lines), []
        base = (ctx.root / rel).parent
        for i, line in enumerate(lines, 1):
            if mask[i - 1]:
                continue
            for m in _MD_LINK.finditer(line):
                target = m.group(1).split("#")[0]
                if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue  # ancre locale, URL ou mailto : non résolu hors ligne (SG-4)
                if not (base / target).resolve().exists():
                    gaps.append(f"ligne {i} : source non résoluble « {target} »")
            for m in _ADR_REF.finditer(line):
                if not list((ctx.root / "decisions").glob(f"{m.group(1)}-*.md")):
                    gaps.append(f"ligne {i} : ADR-{m.group(1)} cité mais introuvable dans decisions/")
            if _HYPOTHESIS.search(line) and not _CONFIRMED.search(_with_continuation(lines, i)):
                gaps.append(f"ligne {i} : hypothèse sans confirmation humaine explicite tracée")
        if ADR_PATH.match(rel):
            refs = find_section(sections(ctx.text(rel)), "Références")
            if not (refs and has_content(refs.body)):
                gaps.append("ADR sans source : section « Références » absente ou vide")
        results.append(res(sid, rel, gaps, "affirmations sourcées", "source manquante / hypothèse non confirmée"))
    return results or no_scope(sid, "documentation/*.md, decisions/NNNN-*.md")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
