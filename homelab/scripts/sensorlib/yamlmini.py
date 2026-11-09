"""Mini-analyseur YAML **statique** pour les sensors Homelab (bibliothèque standard seule).

Pas de PyYAML : un sous-ensemble suffisant des livrables docker-compose Homelab
(mappings imbriqués par indentation, séquences `- `, scalaires simples, blocs `|`/`>`,
commentaires `#`). But : **détecter des défauts de forme** (indentation incohérente,
clés dupliquées au même niveau, tabulation, documents multiples), jamais rendre ni
exécuter le contenu (SG-4). N'est pas un parseur conforme : les cas ambigus sont
signalés comme écarts, jamais lus comme conformes (SG-2).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


class YamlError(Exception):
    """Défaut de forme YAML : porte le numéro de ligne (1-based) et un message court."""

    def __init__(self, line: int, message: str) -> None:
        super().__init__(f"ligne {line} : {message}")
        self.line = line
        self.message = message


@dataclass
class Node:
    """Nœud de l'arbre : mapping (clés → Node) ou valeur scalaire/liste brute."""

    line: int
    kind: str  # "map" | "seq" | "scalar"
    mapping: dict[str, "Node"] = field(default_factory=dict)
    items: list["Node"] = field(default_factory=list)
    scalar: str | None = None
    # clés rencontrées dans l'ordre (diagnostic lisible)
    key_order: list[str] = field(default_factory=list)


_DOC_SEP = re.compile(r"^---\s*(?:#.*)?$")
_DOC_END = re.compile(r"^\.\.\.\s*(?:#.*)?$")
_KEY = re.compile(r"^(?P<key>(?:\"[^\"]*\"|'[^']*'|[^:#]+?))\s*:\s*(?P<val>.*?)\s*$")
_SEQ = re.compile(r"^-\s*(?P<val>.*?)\s*$")


def _strip_inline_comment(s: str) -> str:
    """Retire un commentaire `#` hors guillemets (approximation statique sûre)."""
    in_q = None
    out = []
    for ch in s:
        if in_q:
            out.append(ch)
            if ch == in_q:
                in_q = None
        elif ch in "\"'":
            in_q = ch
            out.append(ch)
        elif ch == "#":
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def split_documents(text: str) -> int:
    """Nombre de documents YAML (séparés par `---`). Un fichier sans `---` = 1 document."""
    count, seen_content = 0, False
    for raw in text.splitlines():
        line = raw.strip()
        if _DOC_SEP.match(line):
            count += 1
            seen_content = False
        elif line and not line.startswith("#"):
            if not seen_content and count == 0:
                count = 1
            seen_content = True
    return max(count, 1 if seen_content or count == 0 else count)


def _logical_lines(text: str) -> list[tuple[int, int, str]]:
    """(numéro 1-based, indentation, contenu) des lignes signifiantes du 1er document."""
    out: list[tuple[int, int, str]] = []
    started = False
    for i, raw in enumerate(text.splitlines(), 1):
        if "\t" in raw[: len(raw) - len(raw.lstrip(" \t"))]:
            raise YamlError(i, "tabulation dans l'indentation (interdite en YAML)")
        stripped = raw.strip()
        if _DOC_SEP.match(stripped):
            if started:  # 2e document : on s'arrête au 1er
                break
            continue
        if _DOC_END.match(stripped):
            break
        if not stripped or stripped.startswith("#"):
            continue
        content = _strip_inline_comment(raw)
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip(" "))
        out.append((i, indent, content.strip()))
        started = True
    return out


def parse(text: str) -> Node:
    """Analyse statique du 1er document. Lève `YamlError` sur défaut de forme."""
    lines = _logical_lines(text)
    root = Node(line=lines[0][0] if lines else 1, kind="map")
    if not lines:
        return root
    _parse_block(lines, 0, lines[0][1], root)
    return root


def _parse_block(lines: list[tuple[int, int, str]], start: int, indent: int, parent: Node) -> int:
    """Remplit `parent` à partir de `start` pour toutes les lignes à l'indentation `indent`."""
    i = start
    while i < len(lines):
        lineno, ind, content = lines[i]
        if ind < indent:
            return i
        if ind > indent:
            raise YamlError(lineno, "indentation inattendue (sur-indentation sans parent)")
        if content.startswith("- "):
            parent.kind = "seq"
            child = Node(line=lineno, kind="scalar", scalar=content[2:].strip())
            parent.items.append(child)
            i += 1
            continue
        if content == "-":
            parent.kind = "seq"
            child = Node(line=lineno, kind="map")
            parent.items.append(child)
            i = _parse_block(lines, i + 1, _next_indent(lines, i + 1, indent), child) if _has_deeper(lines, i + 1, indent) else i + 1
            continue
        m = _KEY.match(content)
        if not m:
            raise YamlError(lineno, f"ligne non reconnue « {content[:40]} » (clé/valeur attendue)")
        key = m.group("key").strip().strip("\"'")
        if not key:
            raise YamlError(lineno, "clé vide")
        if key in parent.mapping:
            raise YamlError(lineno, f"clé dupliquée « {key} » au même niveau")
        val = m.group("val")
        node = Node(line=lineno, kind="scalar", scalar=val or None)
        parent.mapping[key] = node
        parent.key_order.append(key)
        parent.kind = "map"
        if (not val or val in ("|", ">", "|-", ">-", "|+", ">+")) and _has_deeper(lines, i + 1, indent):
            node.kind = "map"
            i = _parse_block(lines, i + 1, _next_indent(lines, i + 1, indent), node)
        else:
            i += 1
    return i


def _has_deeper(lines, idx, indent) -> bool:
    return idx < len(lines) and lines[idx][1] > indent


def _next_indent(lines, idx, indent) -> int:
    return lines[idx][1] if idx < len(lines) else indent


def services(root: Node) -> dict[str, Node]:
    """Mapping `services:` d'un compose (vide si absent / mal formé)."""
    svc = root.mapping.get("services")
    if svc is None or svc.kind != "map":
        return {}
    return {k: v for k, v in svc.mapping.items()}
