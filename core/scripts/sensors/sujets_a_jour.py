#!/usr/bin/env python3
"""Sensor `sujets-a-jour` — applique le contrat de `core/sensors/sensors/sujets-a-jour.md`.

Vérifie que le champ `sujets` du front-matter d'un document d'architecture reflète ses titres `##` / `###`
(dans l'ordre). Un document sans front-matter ou sans champ `sujets` est hors périmètre (non signalé).
Exécution seule : `python3 core/scripts/sensors/sujets_a_jour.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import Result, norm, sections  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402

ID = "sujets-a-jour"

_FRONT = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)
_PROGRESS = re.compile(r"\s+[—-]\s+\d+(?:[.,]\d+)?\s*%\s*$")  # suffixe d'avancement dynamique (ex. checklist « Cadrage — 40 % »)
_KEY = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$")


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _split_inline(s: str) -> list[str]:
    """Éclate le contenu d'une liste inline `[a, "b, c"]` en respectant les guillemets."""
    items, cur, quote = [], "", ""
    for ch in s:
        if quote:
            cur += ch
            quote = "" if ch == quote else quote
        elif ch in "\"'":
            cur += ch
            quote = ch
        elif ch == ",":
            items.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        items.append(cur)
    return [_unquote(i) for i in items if i.strip()]


def read_sujets(text: str) -> list[str] | None:
    """Valeurs du champ `sujets` du front-matter ; None si front-matter ou champ absent."""
    m = _FRONT.match(text)
    if not m:
        return None
    lines = m.group(1).splitlines()
    for i, line in enumerate(lines):
        k = _KEY.match(line)
        if not k or k.group(1) != "sujets":
            continue
        val = k.group(2).split(" #")[0].strip() if not k.group(2).lstrip().startswith(("\"", "'")) else k.group(2).strip()
        if val.startswith("["):
            return _split_inline(val.rstrip().removesuffix("]").lstrip("["))
        if val in ("", "|", ">"):
            out = []
            for nxt in lines[i + 1:]:
                s = nxt.strip()
                if s.startswith("- "):
                    out.append(_unquote(s[2:].split(" #")[0] if not s[2:].lstrip().startswith(("\"", "'")) else s[2:]))
                elif s and not nxt.startswith((" ", "\t")):
                    break
            return out
        return [_unquote(val)]
    return None


def run(ctx: Ctx) -> list[Result]:
    results = []
    for rel in ctx.targets:
        text = ctx.text(rel)
        declared = read_sujets(text)
        if declared is None:
            continue  # pas de champ `sujets` : rien à tenir à jour
        actual = [_PROGRESS.sub("", s.title) for s in sections(text) if s.level in (2, 3)]
        d, a = [norm(x) for x in declared], [norm(x) for x in actual]
        gaps = [f"titre absent de `sujets` : « {t} »" for t, n in zip(actual, a) if n not in d]
        gaps += [f"`sujets` sans titre correspondant : « {t} »" for t, n in zip(declared, d) if n not in a]
        if not gaps and d != a:
            gaps.append("`sujets` contient les bons titres mais pas dans l'ordre du document")
        results.append(res(ID, rel, gaps, "conforme", "`sujets` désynchronisé des titres ##/###"))
    return results or no_scope(ID, "documentation/**/*.md portant un champ `sujets`")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
