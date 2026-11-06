#!/usr/bin/env python3
"""Sensor `style-concision` — applique le bloc `checks` de `core/sensors/sensors/style-concision.md`.

Exécution seule : `python3 core/scripts/sensors/style_concision.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).

Forme uniquement (`RULE-WS-007`, `common/protocols/document-style.md`), jamais le fond.
Exclusions : blocs de code, front-matter, commentaires HTML, tableaux de gabarit (précédés de
`<!-- gabarit -->`) et sections de gabarit non encore renseignées.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import Result, code_mask, strip_front_matter  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402

ID = "style-concision"

PARAGRAPHE_LIGNES_MAX = 5
PHRASE_MOTS_MAX = 35
PUCES_NIVEAUX_MAX = 3
TABLEAU_COLONNES_MAX = 5
CELLULE_MOTS_MAX = 25

_LIST = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+(.*)$")
_TABLE = re.compile(r"^\s*\|.*\|\s*$")
_SEP = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
_GABARIT = re.compile(r"<!--\s*gabarit\s*-->", re.I)
_SENTENCE_END = re.compile(r"(?<=[.!?…])\s+(?=[A-ZÀ-ÖØ-Ý«\"'(\[])")


def _plain(text: str) -> str:
    """Texte lisible : sans cibles de liens, code en ligne ni emphase."""
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"`[^`]*`", "x", text)
    return re.sub(r"[*_]", "", text)


def _words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def _sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_END.split(_plain(text)) if s.strip()]


def _check(text: str) -> list[str]:
    raw = strip_front_matter(text).splitlines()
    mask = code_mask(raw)
    lines, in_comment = [], False
    for i, line in enumerate(raw):  # commentaires HTML masqués, sauf le marqueur de gabarit
        if in_comment:
            in_comment = "-->" not in line
            lines.append("")
        elif line.strip().startswith("<!--") and not _GABARIT.search(line):
            in_comment = "-->" not in line
            lines.append("")
        else:
            lines.append(line)
    gaps: list[str] = []
    para: list[tuple[int, str]] = []

    def flush() -> None:
        if not para:
            return
        if len(para) > PARAGRAPHE_LIGNES_MAX:
            gaps.append(f"ligne {para[0][0]} : paragraphe de {len(para)} lignes (max {PARAGRAPHE_LIGNES_MAX})")
        for s in _sentences(" ".join(t for _, t in para)):
            if _words(s) > PHRASE_MOTS_MAX:
                gaps.append(f"ligne {para[0][0]} : phrase de {_words(s)} mots (max {PHRASE_MOTS_MAX})")
        para.clear()

    i = 0
    while i < len(lines):
        line, n = lines[i], i + 1
        if mask[i] or not line.strip() or line.lstrip().startswith(("#", ">", "<!--")):
            flush()
            i += 1
            continue
        if _GABARIT.search(line):  # le tableau qui suit est imposé par un gabarit : ignoré
            flush()
            i += 1
            while i < len(lines) and _TABLE.match(lines[i]):
                i += 1
            continue
        if _TABLE.match(line):
            flush()
            j = i
            while j < len(lines) and _TABLE.match(lines[j]) and not mask[j]:
                j += 1
            for k in range(i, j):
                if _SEP.match(lines[k]) and "-" in lines[k]:
                    continue
                cells = [c.strip() for c in lines[k].strip().strip("|").split("|")]
                if k == i and len(cells) > TABLEAU_COLONNES_MAX:
                    gaps.append(f"ligne {k + 1} : tableau de {len(cells)} colonnes (max {TABLEAU_COLONNES_MAX})")
                for c in cells:
                    if _words(_plain(c)) > CELLULE_MOTS_MAX:
                        gaps.append(f"ligne {k + 1} : cellule de {_words(_plain(c))} mots (max {CELLULE_MOTS_MAX})")
            i = j
            continue
        m = _LIST.match(line)
        if m:
            flush()
            depth = len(m.group(1).replace("\t", "    ")) // 2 + 1
            if depth > PUCES_NIVEAUX_MAX:
                gaps.append(f"ligne {n} : puce de niveau {depth} (max {PUCES_NIVEAUX_MAX})")
            for s in _sentences(m.group(2)):
                if _words(s) > PHRASE_MOTS_MAX:
                    gaps.append(f"ligne {n} : phrase de {_words(s)} mots (max {PHRASE_MOTS_MAX})")
            i += 1
            continue
        para.append((n, line.strip()))
        i += 1
    flush()
    return gaps


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    for rel in ctx.targets:
        results.append(res(sid, rel, _check(ctx.text(rel)), "style conforme", "écart(s) de style"))
    return results or no_scope(sid, "documentation/*.md, decisions/NNNN-*.md")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
