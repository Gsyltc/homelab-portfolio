#!/usr/bin/env python3
"""Sensor `diagram-validity` — applique le bloc `checks` de `core/sensors/sensors/diagram-validity.md`.

Exécution seule : `python3 core/scripts/sensors/diagram_validity.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import Result, unterminated_fence  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402
from sensorlib.diagrams import blocks  # noqa: E402

ID = "diagram-validity"


MERMAID_TYPES = ("graph", "flowchart", "sequencediagram", "classdiagram", "statediagram", "erdiagram", "journey",
                 "gantt", "pie", "quadrantchart", "requirementdiagram", "gitgraph", "mindmap", "timeline", "sankey",
                 "xychart", "block", "packet", "kanban", "architecture", "c4context", "c4container", "c4component",
                 "c4dynamic", "c4deployment", "zenuml")
_PUML_START = re.compile(r"^\s*@start(\w+)", re.I)
_PUML_END = re.compile(r"^\s*@end(\w+)", re.I)
_BRACKET = {"(": ")", "[": "]", "{": "}"}


def _balanced(text: str) -> str | None:
    """Premier défaut de parenthésage/guillemets d'une ligne, sinon None."""
    stack, in_q = [], None
    for ch in text:
        if in_q:
            if ch == in_q:
                in_q = None
        elif ch == '"':
            in_q = ch
        elif ch in _BRACKET:
            stack.append(ch)
        elif ch in _BRACKET.values():
            if not stack or _BRACKET[stack.pop()] != ch:
                return f"« {ch} » inattendu"
    if in_q:
        return "guillemet non fermé"
    if stack:
        return f"« {stack[-1]} » non fermé"
    return None


def _check_mermaid(block: list[str], start: int) -> list[str]:
    gaps = []
    body = [(i, l) for i, l in enumerate(block, start) if l.strip() and not l.strip().startswith("%%")]
    if not body:
        return [f"ligne {start} : bloc mermaid vide"]
    first = body[0][1].strip()
    if first.startswith("---"):  # front-matter mermaid
        end = next((k for k, (_, l) in enumerate(body[1:], 1) if l.strip() == "---"), None)
        body = body[end + 1:] if end else body
        first = body[0][1].strip() if body else ""
    word = re.split(r"[\s;{]", first, maxsplit=1)[0].lower().replace("-", "")
    if not any(word == t or word.startswith(t) for t in MERMAID_TYPES):
        gaps.append(f"ligne {body[0][0]} : type de diagramme mermaid inconnu « {first.split()[0] if first else ''} »")
    depth = 0
    for i, line in body[1:]:
        s = line.strip()
        if re.match(r"^(subgraph|loop|alt|opt|par|critical|break|rect)\b", s):
            depth += 1
        elif s == "end":
            depth -= 1
            if depth < 0:
                gaps.append(f"ligne {i} : « end » sans ouverture")
                depth = 0
        if (err := _balanced(s)) and not word.startswith(("sequencediagram", "pie", "gantt", "journey")):
            gaps.append(f"ligne {i} : {err}")
    if depth > 0:
        gaps.append(f"{depth} bloc(s) subgraph/loop/alt non refermé(s) par « end »")
    return gaps


def _check_plantuml(block: list[str], start: int) -> list[str]:
    gaps, opened = [], []
    for i, line in enumerate(block, start):
        if m := _PUML_START.match(line):
            opened.append((m.group(1).lower(), i))
        elif m := _PUML_END.match(line):
            if not opened or opened[-1][0] != m.group(1).lower():
                gaps.append(f"ligne {i} : @end{m.group(1)} sans @start correspondant")
            else:
                opened.pop()
        if re.match(r"^\s*!(include|includeurl|import)\w*\s+https?://", line, re.I):
            gaps.append(f"ligne {i} : inclusion distante non évaluée (SG-4)")
    gaps += [f"ligne {i} : @start{t} sans @end{t}" for t, i in opened]
    if not any(_PUML_START.match(l) for l in block):
        gaps.append(f"ligne {start} : balise @startuml (ou @start…) absente")
    depth = 0
    for i, line in enumerate(block, start):
        code = re.sub(r"'.*$", "", line)
        depth += code.count("{") - code.count("}")
    if depth != 0:
        gaps.append(f"accolades déséquilibrées ({'+' if depth > 0 else ''}{depth})")
    return gaps


def _check_structurizr(block: list[str], start: int, full_document: bool = False) -> list[str]:
    """Un extrait Markdown peut être un fragment : `workspace` n'est exigé que d'un fichier .dsl complet."""
    gaps = []
    code = [(i, re.sub(r"(?<!:)//.*$|#.*$", "", l)) for i, l in enumerate(block, start)]
    if full_document and not any(re.match(r"^\s*workspace\b", l) for _, l in code):
        gaps.append(f"ligne {start} : mot-clé « workspace » racine absent")
    depth = 0
    for i, l in code:
        if l.count('"') % 2:
            gaps.append(f"ligne {i} : guillemet non fermé")
        depth += l.count("{") - l.count("}")
        if depth < 0:
            gaps.append(f"ligne {i} : « }} » sans « {{ » correspondant")
            depth = 0
        if re.match(r"^\s*!(include|script|plugin|docs|adrs)\b.*(https?://)", l):
            gaps.append(f"ligne {i} : directive distante non évaluée (SG-4)")
    if depth:
        gaps.append(f"{depth} accolade(s) « {{ » non fermée(s)")
    return gaps

def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    for rel in ctx.targets:
        text, gaps, count = ctx.text(rel), [], 0
        if rel.endswith((".puml", ".dsl")):
            lines = text.splitlines()
            count, gaps = 1, (_check_plantuml if rel.endswith(".puml") else lambda b, s: _check_structurizr(b, s, True))(lines, 1)
        else:
            if (n := unterminated_fence(text.splitlines())):
                gaps.append(f"ligne {n} : bloc de code non refermé")
            for lang, start, block in blocks(text):
                count += 1
                fn = {"mermaid": _check_mermaid, "plantuml": _check_plantuml, "puml": _check_plantuml}.get(lang, _check_structurizr)
                gaps += [f"[{lang}] {g}" for g in fn(block, start)]
        if count == 0 and not gaps:
            continue  # aucun diagramme dans ce fichier : rien à vérifier
        results.append(res(sid, rel, gaps, f"syntaxe valide ({count} diagramme(s), contrôle structurel)", "erreur de parsing"))
    return results or no_scope(sid, "aucun diagramme mermaid/plantuml/structurizr trouvé")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
