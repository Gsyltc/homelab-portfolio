#!/usr/bin/env python3
"""Sensor `checklist-progress` — applique le bloc `checks` de `core/sensors/sensors/checklist-progress.md`.

Il **constate** l'avancement porté par le fichier d'état de la checklist d'architecture
(`documentation/00-checklist-architecture.md`) et le **restitue** : % global de la solution,
% du cadrage, % des besoins (MoSCoW), % des livrables. Il ne **décide** ni n'**écrit** rien
(advisory ; aucun auto-accept). La mécanique du calcul (barème 80/10/10, agrégation) reste la
source unique du protocole `core/common/protocols/architecture-checklist.md` : ce sensor lit les
% déjà portés dans le fichier d'état, il ne les recalcule pas.

Fichier absent / illisible / sans avancement lisible ⇒ `⛔ indisponible` (SG-2, jamais lu comme
conforme).

Exécution seule : `python3 core/scripts/sensors/checklist_progress.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import OK, UNAVAILABLE, Result, sections  # noqa: E402
from sensorlib.context import Ctx  # noqa: E402

ID = "checklist-progress"

STATE_FILE = "documentation/00-checklist-architecture.md"

# % global — porté hors section : « **% global :** 42 % »
_GLOBAL_RE = re.compile(r"%\s*global[^\d%]*(\d{1,3})\s*%", re.I)
# % d'une section — porté dans son titre : « ## Cadrage — 42 % »
_SECTION_PCT_RE = re.compile(r"(\d{1,3})\s*%\s*$")

# Titre de section ↔ libellé restitué. On cible par début de titre normalisé
# (le gabarit porte « ## Besoins (MoSCoW) — N % »).
SECTIONS = [
    ("cadrage", "cadrage"),
    ("besoins", "besoins"),
    ("livrables", "livrables"),
]


def _section_pct(title: str) -> int | None:
    m = _SECTION_PCT_RE.search(title)
    if not m:
        return None
    val = int(m.group(1))
    return val if 0 <= val <= 100 else None


def run(ctx: Ctx) -> list[Result]:
    sid = ID
    if not ctx.exists(STATE_FILE):
        return [Result(sid, STATE_FILE, UNAVAILABLE,
                       "indisponible : fichier d'état de la checklist absent",
                       [f"{STATE_FILE} introuvable dans le projet (checklist non initialisée)"])]
    try:
        text = ctx.text(STATE_FILE)
    except OSError as exc:
        return [Result(sid, STATE_FILE, UNAVAILABLE,
                       "indisponible : fichier d'état illisible", [str(exc)])]

    gm = _GLOBAL_RE.search(text)
    glob = int(gm.group(1)) if gm and 0 <= int(gm.group(1)) <= 100 else None

    found: dict[str, int] = {}
    for sec in sections(text):
        norm_title = sec.title.strip().casefold()
        for key, prefix in SECTIONS:
            if key in found:
                continue
            if norm_title.startswith(prefix):
                pct = _section_pct(sec.title)
                if pct is not None:
                    found[key] = pct

    # Rien de lisible du tout (ni global, ni aucune section) ⇒ fichier non exploitable (SG-2).
    if glob is None and not found:
        return [Result(sid, STATE_FILE, UNAVAILABLE,
                       "indisponible : aucun avancement lisible dans le fichier d'état",
                       ["ni % global ni % de section (Cadrage / Besoins / Livrables) détecté"])]

    def pct(key: str) -> str:
        return f"{found[key]} %" if key in found else "n/d"

    glob_txt = f"{glob} %" if glob is not None else "n/d"
    summary = (
        f"avancement restitué — solution {glob_txt} | "
        f"cadrage {pct('cadrage')} | besoins {pct('besoins')} | livrables {pct('livrables')}"
    )
    findings = [
        f"avancement global de la solution : {glob_txt}",
        f"avancement du cadrage : {pct('cadrage')}",
        f"avancement des besoins (MoSCoW) : {pct('besoins')}",
        f"avancement des livrables : {pct('livrables')}",
    ]
    # Avancement partiellement illisible : constat tracé, sans dégrader le verdict (advisory).
    not_read = ([] if glob is not None else ["global"]) + [k for k, _ in SECTIONS if k not in found]
    if not_read:
        findings.append(f"avancement(s) non lu(s) dans le fichier d'état : {', '.join(not_read)}")
    return [Result(sid, STATE_FILE, OK, summary, findings)]


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
