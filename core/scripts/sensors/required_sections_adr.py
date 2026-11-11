#!/usr/bin/env python3
"""Sensor `required-sections-adr` — applique le bloc `checks` de `core/sensors/sensors/required-sections-adr.md`.

Exécution seule : `python3 core/scripts/sensors/required_sections_adr.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import find_section, norm, sections  # noqa: E402
from sensorlib.context import Ctx, ADR_PATH, no_scope, res  # noqa: E402
from sensorlib.sections import section_gaps  # noqa: E402

ID = "required-sections-adr"

ADR_META = ["auteurs", "parties_prenantes", "accepte_par", "accepte_le", "supersedes", "superseded_by"]
ADR_STATUS = {"proposed", "accepted", "rejected", "superseded", "deprecated"}
ADR_CRITERES_DEPUIS = "2026-11-11"  # « Critères de décision » exigés pour les ADR créés à partir de cette date
ADR_SECTIONS = ["Status", "Date de création", "Contexte", "Décision", "Conséquences",
                "Alternatives étudiées", "Notes d'implémentation", "Références"]


def _adr_gaps(text: str, ctx: Ctx | None = None) -> list[str]:
    gaps = []
    m = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.S)
    if not m:
        gaps.append("en-tête : front matter absent en tête de fichier (avant le titre H1)")
    meta = m.group(1) if m else ""
    for key in ADR_META:
        if not re.search(rf"^{re.escape(key)}\s*:", meta, re.M):
            gaps.append(f"en-tête : clé « {key} » absente")
    secs = sections(text)
    status = find_section(secs, "Status")
    date_in_status = bool(status and re.search(r"date de création", "\n".join(status.body), re.I))
    gaps += section_gaps(text, [x for x in ADR_SECTIONS if not (x == "Date de création" and date_in_status)])
    if status:
        values = [norm(line) for line in status.body if line.strip() and not line.lstrip().startswith(("<!--", "#"))]
        first = re.split(r"[\s:,;(]", values[0])[0] if values else ""
        if values and first not in ADR_STATUS:  # « Superseded par [ADR-NNNN](…) » accepté : le mot-clé en tête fait foi
            gaps.append(f"« Status » : valeur « {values[0]} » hors {sorted(ADR_STATUS)}")
        if sum(1 for v in values if v in ADR_STATUS) > 1:
            gaps.append("« Status » : statut unique attendu")
    cons = find_section(secs, "Conséquences")
    if cons:
        subs = {norm(s.title) for s in secs if s.level > cons.level and cons.line < s.line <= cons.line + len(cons.body)}
        for sub in ("positives", "négatives"):
            if not any(t.startswith(sub) for t in subs):
                gaps.append(f"« Conséquences » : sous-rubrique « {sub.capitalize()} » absente")
        for code, label in (("POS", "Positives"), ("NEG", "Négatives")):
            if not re.search(rf"\b{code}-\d{{3}}\b", "\n".join(cons.body)):
                gaps.append(f"« Conséquences » : aucune puce codée {code}-NNN ({label})")
    alt = find_section(secs, "Alternatives étudiées")
    if alt and not re.search(r"\bALT-\d{3}\b", "\n".join(alt.body) + "\n".join(s.title for s in secs if alt.line < s.line <= alt.line + len(alt.body))):
        gaps.append("« Alternatives étudiées » : aucune alternative codée ALT-NNN")
    date = find_section(secs, "Date de création")
    zone = "\n".join(date.body) if date else "\n".join(status.body if status else [])
    dm = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", zone)
    if (date or date_in_status) and not dm:
        gaps.append("« Date de création » : date YYYY-MM-DD absente")
    if dm and dm.group(1) >= ADR_CRITERES_DEPUIS:
        gaps += section_gaps(text, ["Critères de décision"])
    if ctx is not None:
        for key in ("supersedes", "superseded_by"):
            km = re.search(rf"^{key}\s*:\s*\"?(\d{{4}})", meta, re.M)
            if km and not list((ctx.root / "decisions").glob(f"{km.group(1)}-*.md")):
                gaps.append(f"en-tête : « {key} » référence l'ADR {km.group(1)} introuvable dans decisions/")
    return gaps


def run(ctx: Ctx) -> list:
    results = [res(ID, rel, _adr_gaps(ctx.text(rel), ctx), "conforme", "rubriques manquantes/vides")
               for rel in ctx.targets if ADR_PATH.match(rel)]
    return results or no_scope(ID, "ADR")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
