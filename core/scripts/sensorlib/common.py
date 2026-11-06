"""Briques communes des sensors `core` : manifestes, globs, parsing Markdown, verdicts.

Python standard uniquement (aucune dépendance). Parsing **statique** : le contenu
des artefacts est une donnée non fiable, rien n'est exécuté ni résolu en réseau (SG-4).
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

OK, GAP, UNAVAILABLE = "ok", "gap", "unavailable"
ICONS = {OK: "✅", GAP: "⚠️", UNAVAILABLE: "⛔"}
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".aidlc-sensors"}


@dataclass
class Result:
    """Verdict d'un sensor sur une cible (SG-2 : `unavailable` n'est jamais un vert)."""

    sensor: str
    target: str
    verdict: str
    summary: str
    findings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "sensor": self.sensor,
            "target": self.target,
            "verdict": self.verdict,
            "icon": ICONS[self.verdict],
            "summary": self.summary,
            "findings": self.findings,
        }


def worst(results: list[Result]) -> str:
    """Pire verdict d'une liste (indisponible > écart > conforme). Liste vide = indisponible."""
    if not results:
        return UNAVAILABLE
    verdicts = {r.verdict for r in results}
    for v in (UNAVAILABLE, GAP):
        if v in verdicts:
            return v
    return OK


# --------------------------------------------------------------------------- #
# Manifestes
# --------------------------------------------------------------------------- #

REQUIRED_MANIFEST_KEYS = ("id", "kind", "command", "default_severity", "description", "origine")


@dataclass
class Manifest:
    id: str
    fire_on: str
    matches: str | None
    severity: str
    description: str
    path: Path
    meta: dict[str, str]
    missing: list[str]

    @property
    def valid(self) -> bool:
        return not self.missing and self.meta.get("kind") == "deterministic"


def _unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def parse_manifest(path: Path) -> Manifest:
    """Lit le front-matter plat d'un manifeste (clé: valeur). Provenance `origine` requise (SG-1)."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.S)
    meta: dict[str, str] = {}
    if m:
        for line in m.group(1).splitlines():
            km = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
            if km:
                meta[km.group(1)] = _unquote(km.group(2))
    missing = [k for k in REQUIRED_MANIFEST_KEYS if not meta.get(k)]
    return Manifest(
        id=meta.get("id", path.stem),
        fire_on=meta.get("fire_on", "write"),
        matches=meta.get("matches"),
        severity=meta.get("default_severity", "advisory"),
        description=meta.get("description", ""),
        path=path,
        meta=meta,
        missing=missing,
    )


# --------------------------------------------------------------------------- #
# Globs (accolades, `**`, `*`, `?`) — chemins POSIX relatifs à la racine du projet
# --------------------------------------------------------------------------- #


def expand_braces(pattern: str) -> list[str]:
    m = re.search(r"\{([^{}]*)\}", pattern)
    if not m:
        return [pattern]
    out: list[str] = []
    for alt in m.group(1).split(","):
        out.extend(expand_braces(pattern[: m.start()] + alt + pattern[m.end():]))
    return out


def _glob_to_regex(glob: str) -> re.Pattern[str]:
    i, n, rx = 0, len(glob), ""
    while i < n:
        c = glob[i]
        if glob.startswith("**/", i):
            rx += "(?:.*/)?"
            i += 3
        elif glob.startswith("**", i):
            rx += ".*"
            i += 2
        elif c == "*":
            rx += "[^/]*"
            i += 1
        elif c == "?":
            rx += "[^/]"
            i += 1
        elif c == "[" and (j := glob.find("]", i + 2)) != -1:
            rx += glob[i:j + 1]
            i = j + 1
        else:
            rx += re.escape(c)
            i += 1
    return re.compile(rx + r"\Z")


def glob_match(pattern: str, rel_path: str) -> bool:
    rel_path = rel_path.replace("\\", "/")
    if rel_path.startswith("./"):
        rel_path = rel_path[2:]
    return any(_glob_to_regex(g).match(rel_path) for g in expand_braces(pattern))


def list_files(root: Path, pattern: str | None) -> list[str]:
    """Fichiers de `root` (chemins relatifs POSIX) qui satisfont `pattern` (None = tous)."""
    found: list[str] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        rel = p.relative_to(root).as_posix()
        if pattern is None or glob_match(pattern, rel):
            found.append(rel)
    return found


# --------------------------------------------------------------------------- #
# Markdown
# --------------------------------------------------------------------------- #

_COMMENT = re.compile(r"<!--.*?-->", re.S)
_FENCE = re.compile(r"^\s*(```|~~~)")
_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def read_text(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="replace")


def strip_comments(text: str) -> str:
    """Retire les commentaires HTML en conservant les retours à la ligne (numéros de ligne stables)."""
    return _COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def strip_front_matter(text: str) -> str:
    m = re.match(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", text, re.S)
    return ("\n" * m.group(0).count("\n") + text[m.end():]) if m else text


def code_mask(lines: list[str]) -> list[bool]:
    """True pour chaque ligne située dans un bloc de code clôturé (délimiteurs inclus)."""
    mask, fence = [], None
    for line in lines:
        m = _FENCE.match(line)
        if fence is None and m:
            fence = m.group(1)
            mask.append(True)
        elif fence is not None:
            mask.append(True)
            if m and m.group(1) == fence:
                fence = None
        else:
            mask.append(False)
    return mask


def unterminated_fence(lines: list[str]) -> int | None:
    """Numéro (1-based) de la ligne ouvrant un bloc de code jamais refermé, sinon None."""
    fence, start = None, 0
    for i, line in enumerate(lines, 1):
        m = _FENCE.match(line)
        if m and fence is None:
            fence, start = m.group(1), i
        elif m and m.group(1) == fence:
            fence = None
    return start if fence else None


def norm(s: str) -> str:
    """Normalise un titre : sans emphase/backticks/numérotation, espaces réduits, casse ignorée."""
    s = re.sub(r"[*_`]", "", s)
    s = re.sub(r"^\s*\d+(?:\.\d+)*[.)]?\s+", "", s)
    s = s.replace("’", "'")
    return re.sub(r"\s+", " ", s).strip().casefold()


@dataclass
class Section:
    level: int
    title: str
    line: int  # 1-based
    body: list[str]  # lignes jusqu'au prochain titre de niveau <= (sous-sections incluses)


def sections(text: str) -> list[Section]:
    """Sections Markdown (hors blocs de code, commentaires et front-matter ignorés)."""
    lines = strip_comments(strip_front_matter(text)).splitlines()
    mask = code_mask(lines)
    heads: list[tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        if not mask[i]:
            m = _HEADING.match(line)
            if m:
                heads.append((i, len(m.group(1)), m.group(2)))
    out: list[Section] = []
    for idx, (i, level, title) in enumerate(heads):
        end = len(lines)
        for j, lv, _ in heads[idx + 1:]:
            if lv <= level:
                end = j
                break
        out.append(Section(level, title, i + 1, lines[i + 1:end]))
    return out


def find_section(secs: list[Section], expected: str) -> Section | None:
    want = norm(expected)
    for s in secs:
        t = norm(s.title)
        if t == want or t.startswith(want + " ") or t.startswith(want + "("):
            return s
    return None


_PLACEHOLDER = re.compile(
    r"^(?:<[^>]*>|\[[^\]]*\]|\{[^}]*\}|\.{2,}|…|x{2,}|tbd|todo|à compléter|a completer|n/a|-+|:?-{2,}:?)$",
    re.I,
)


def has_content(lines: list[str]) -> bool:
    """Vrai si les lignes portent un contenu propre (hors titres, séparateurs, en-têtes de tableau, gabarit vide)."""
    for idx, raw in enumerate(lines):
        line = raw.strip()
        if not line or _HEADING.match(line) or re.fullmatch(r"[-*_=\s|:]+", line):
            continue
        nxt = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
        if "|" in line and re.fullmatch(r"[|\s:-]+", nxt) and "-" in nxt:
            continue  # ligne d'en-tête d'un tableau
        line = re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", line)
        cells = [c.strip() for c in line.strip("|").split("|")] if "|" in line else [line]
        if any(c and not _PLACEHOLDER.match(c) for c in cells):
            return True
    return False


def body_without_headings_has_content(sec: Section) -> bool:
    return has_content(sec.body)


# --------------------------------------------------------------------------- #
# Provenance (SG-5)
# --------------------------------------------------------------------------- #


def source_commit(anchor: Path) -> str | None:
    """`<sha court>[-dirty]` du dépôt qui porte les manifestes, ou None si non traçable."""
    try:
        run = lambda *a: subprocess.run(  # noqa: E731
            ["git", "-C", str(anchor), *a], capture_output=True, text=True, timeout=15, check=True
        ).stdout.strip()
        sha = run("rev-parse", "--short", "HEAD")
        dirty = run("status", "--porcelain", "--", "core/sensors", "core/scripts")
        return sha + ("-dirty" if dirty else "")
    except (OSError, subprocess.SubprocessError):
        return None
