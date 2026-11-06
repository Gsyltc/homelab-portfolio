"""Extraction des blocs de diagramme en code d'un document Markdown (partagé)."""

from __future__ import annotations

import re


def blocks(text: str) -> list[tuple[str, int, list[str]]]:
    """Blocs de code clôturés `mermaid|plantuml|puml|structurizr|dsl` : (langage, 1re ligne, contenu)."""
    lines, out, i = text.splitlines(), [], 0
    while i < len(lines):
        m = re.match(r"^\s*(```|~~~)\s*([\w-]+)", lines[i])
        if m:
            fence, lang, j = m.group(1), m.group(2).lower(), i + 1
            while j < len(lines) and not lines[j].strip().startswith(fence):
                j += 1
            if lang in ("mermaid", "plantuml", "puml", "structurizr", "dsl"):
                out.append((lang, i + 2, lines[i + 1:j]))
            i = j
        i += 1
    return out
