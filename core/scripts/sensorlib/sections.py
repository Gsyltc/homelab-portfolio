"""Contrôle de présence et de contenu des rubriques Markdown (partagé)."""

from __future__ import annotations

from .common import find_section, has_content, sections


def section_gaps(text: str, expected: list[str]) -> list[str]:
    secs = sections(text)
    gaps = []
    for name in expected:
        s = find_section(secs, name)
        if s is None:
            gaps.append(f"rubrique manquante : « {name} »")
        elif not has_content(s.body):
            gaps.append(f"rubrique vide : « {name} » (ligne {s.line})")
    return gaps
