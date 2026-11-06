"""Contexte d'exécution et motifs partagés par les scripts de sensors."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .common import GAP, OK, UNAVAILABLE, Result, read_text

ISSUE_RE = re.compile(r"\b(?:ALI|HOM|ORIG)-\d+\b")
BA_RE = re.compile(r"\bBA-\d+\b")
REQ_RE = re.compile(r"\b(?:N?FR)-\d+\b")
ADR_PATH = re.compile(r"^decisions/\d{4}-[^/]+\.md$")
MOSCOW = re.compile(r"\b(?:must|should|could|won'?t)\b", re.I)


@dataclass
class Ctx:
    root: Path
    targets: list[str]  # fichiers du périmètre (chemins relatifs POSIX), déjà filtrés par `matches`
    explicit: bool  # True si l'appelant a désigné les fichiers (hook / --path) ; False = balayage de gate

    def text(self, rel: str) -> str:
        return read_text(self.root, rel)

    def exists(self, rel: str) -> bool:
        return (self.root / rel).is_file()


def no_scope(sensor: str, what: str) -> list[Result]:
    return [Result(sensor, "(périmètre)", UNAVAILABLE, f"indisponible : aucun fichier dans le périmètre ({what})")]


def res(sensor: str, target: str, gaps: list[str], ok_msg: str, gap_msg: str) -> Result:
    if gaps:
        return Result(sensor, target, GAP, f"{gap_msg} : {len(gaps)} point(s)", gaps)
    return Result(sensor, target, OK, ok_msg)
