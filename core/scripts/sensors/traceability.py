#!/usr/bin/env python3
"""Sensor `traceability` — applique le bloc `checks` de `core/sensors/sensors/traceability.md`.

Exécution seule : `python3 core/scripts/sensors/traceability.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import UNAVAILABLE, Result, code_mask, strip_comments, strip_front_matter  # noqa: E402
from sensorlib.context import Ctx, BA_RE, REQ_RE, ADR_PATH, MOSCOW, res  # noqa: E402


ID = "traceability"


_SCENARIO = re.compile(r"^#{2,6}\s+(?:Scenario|Scénario)\b", re.I)


def run(ctx: Ctx) -> list[Result]:
    sid = ID
    texts = {r: strip_comments(strip_front_matter(ctx.text(r))) for r in ctx.targets}
    gaps: list[str] = []
    ba_defs: dict[str, tuple[str, int, str]] = {}  # BA -> (fichier, ligne, texte)
    req_ids: dict[str, str] = {}  # exigence -> 1er fichier où elle apparaît
    pairs: set[tuple[str, str]] = set()
    for rel, text in texts.items():
        lines = text.splitlines()
        mask = code_mask(lines)
        for i, line in enumerate(lines, 1):
            if mask[i - 1] or re.search(r"\b(?:BA|N?FR)-(?:xxx|…|\.\.\.)", line, re.I):
                continue
            bas, reqs = set(BA_RE.findall(line)), set(REQ_RE.findall(line))
            for b in bas:
                if b not in ba_defs or (MOSCOW.search(line) and not MOSCOW.search(ba_defs[b][2])):
                    ba_defs[b] = (rel, i, line)
                pairs.update((b, r) for r in reqs)
            for r in reqs:
                req_ids.setdefault(r, rel)
    if not ba_defs and not req_ids:
        return [Result(sid, "(périmètre)", UNAVAILABLE,
                       "indisponible : aucun identifiant amont BA-…/FR-…/NFR-… trouvé (fail closed)")]
    linked_ba = {b for b, _ in pairs}
    for b, (rel, i, line) in sorted(ba_defs.items()):
        if not MOSCOW.search(line):
            gaps.append(f"{b} ({rel}:{i}) : priorité MoSCoW absente")
        if b not in linked_ba:
            gaps.append(f"{b} ({rel}:{i}) : aucune exigence liée (FR-/NFR- sur la même ligne)")
    downstream = [r for r in ctx.targets if r.startswith(("decisions/", "livrables/"))]
    for r, src in sorted(req_ids.items()):
        if not any(re.search(rf"\b{re.escape(r)}\b", texts[d]) for d in downstream):
            gaps.append(f"{r} ({src}) : exigence sans ADR ni livrable aval")
    all_ids = set(ba_defs) | set(req_ids)
    for rel in (d for d in downstream if ADR_PATH.match(d)):
        if not (set(BA_RE.findall(texts[rel])) | set(REQ_RE.findall(texts[rel]))) & all_ids:
            gaps.append(f"{rel} : décision sans exigence ni besoin amont (orphelin dérivé)")
    for rel, text in texts.items():  # scénarios de spec : « Tracé vers » avec BA-… et exigence
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if _SCENARIO.match(line):
                nxt = "\n".join(lines[idx + 1: idx + 15])
                trace = re.search(r"Tracé vers\s*:(.*)", nxt)
                if not trace or not BA_RE.search(trace.group(1)):
                    gaps.append(f"{rel}:{idx + 1} : scénario sans « Tracé vers » vers un besoin BA-…")
    return [res(sid, f"ensemble ({len(ctx.targets)} fichier(s))", gaps, "chaîne tracée", "maillon manquant / orphelin")]


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
