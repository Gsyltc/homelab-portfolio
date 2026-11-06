"""Implémentation exécutable des sensors `core` (un `run_<id>(ctx)` par manifeste).

Chaque fonction applique le « contrat de vérification » (`checks`) du manifeste
`core/sensors/sensors/<id>.md` et renvoie des `Result`. Aucun verdict vert sans
vérification effective : périmètre vide ou source absente => ⛔ indisponible (SG-2).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .common import (
    GAP, OK, UNAVAILABLE, Result, code_mask, find_section, has_content, norm,
    read_text, sections, strip_comments, strip_front_matter, unterminated_fence,
)

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


def _no_scope(sensor: str, what: str) -> list[Result]:
    return [Result(sensor, "(périmètre)", UNAVAILABLE, f"indisponible : aucun fichier dans le périmètre ({what})")]


def _res(sensor: str, target: str, gaps: list[str], ok_msg: str, gap_msg: str) -> Result:
    if gaps:
        return Result(sensor, target, GAP, f"{gap_msg} : {len(gaps)} point(s)", gaps)
    return Result(sensor, target, OK, ok_msg)


# --------------------------------------------------------------------------- #
# required-sections
# --------------------------------------------------------------------------- #

ADR_META = ["auteurs", "accepté par", "accepté le", "supersedes", "superseded_by"]
ADR_SECTIONS = ["Status", "Date de création", "Contexte", "Décision", "Conséquences",
                "Alternatives étudiées", "Notes d'implémentation", "Références"]
DAS_FILES = {
    "001-document-architecture-solution.md": ["Métadonnées du document", "Historique du document", "Arrimages", "Structure de la documentation"],
    "01-introduction.md": ["Contexte", "Périmètre", "Parties prenantes"],
    "02-objectifs.md": ["Objectifs de la solution", "Exigences non-fonctionnelles (NFRs)", "Matrice de suivi"],
    "06-architecture-solutions.md": ["Description de l'architecture de solution", "Liste des diagrammes d'architecture"],
    "08-contraintes.md": ["Lois et règlementations", "Conformités"],
    "10-cycle_vie_donnees.md": ["Gouvernance de données", "Classification des données"],
    "11-securite.md": ["Sécurité applicative", "Frontières de confiance", "Sécurité Infrastructure", "Gestion des identités et des accès (GIA)"],
}
SECURITE_FILES = {
    "01-surfaces-et-actifs.md": ["Surfaces d'attaque"],
    "02-menaces-stride.md": ["Matrice de synthèse STRIDE par surface"],
    "03-risques-owasp.md": ["Table de couverture OWASP Top 10"],
}


def _section_gaps(text: str, expected: list[str]) -> list[str]:
    secs = sections(text)
    gaps = []
    for name in expected:
        s = find_section(secs, name)
        if s is None:
            gaps.append(f"rubrique manquante : « {name} »")
        elif not has_content(s.body):
            gaps.append(f"rubrique vide : « {name} » (ligne {s.line})")
    return gaps


def _adr_gaps(text: str) -> list[str]:
    gaps = []
    m = re.search(r"^---\s*\n(.*?)\n---\s*$", text, re.S | re.M)
    meta = m.group(1) if m else ""
    for key in ADR_META:
        if not re.search(rf"^{re.escape(key)}\s*:", meta, re.M | re.I):
            gaps.append(f"en-tête : clé « {key} » absente")
    secs = sections(text)
    status = find_section(secs, "Status")
    date_in_status = bool(status and re.search(r"date de création", "\n".join(status.body), re.I))
    gaps += _section_gaps(text, [x for x in ADR_SECTIONS if not (x == "Date de création" and date_in_status)])
    cons = find_section(secs, "Conséquences")
    if cons:
        subs = {norm(s.title) for s in secs if s.level > cons.level and cons.line < s.line <= cons.line + len(cons.body)}
        for sub in ("positives", "négatives"):
            if not any(t.startswith(sub) for t in subs):
                gaps.append(f"« Conséquences » : sous-rubrique « {sub.capitalize()} » absente")
    date = find_section(secs, "Date de création")
    zone = "\n".join(date.body) if date else "\n".join(status.body if status else [])
    if (date or date_in_status) and not re.search(r"\b\d{4}-\d{2}-\d{2}\b", zone):
        gaps.append("« Date de création » : date YYYY-MM-DD absente")
    return gaps


def _is_securite_file(rel: str, name: str) -> bool:
    return rel.startswith("documentation/") and rel.endswith(f"architecture-securite/{name}")


def run_required_sections(ctx: Ctx) -> list[Result]:
    sid, results = "required-sections", []
    if not ctx.targets and not ctx.explicit:
        pass  # le balayage de gate signale quand même les fichiers mandatory manquants
    for rel in ctx.targets:
        text = ctx.text(rel)
        base = rel.rsplit("/", 1)[-1]
        if ADR_PATH.match(rel):
            gaps = _adr_gaps(text)
        elif rel.startswith("documentation/") and rel.count("/") == 1 and base in DAS_FILES:
            gaps = [] if has_content(strip_comments(text).splitlines()) else ["fichier vide ou limité au gabarit"]
            gaps += _section_gaps(text, DAS_FILES[base])
        elif any(_is_securite_file(rel, n) for n in SECURITE_FILES):
            name = rel.rsplit("architecture-securite/", 1)[1]
            gaps = [] if has_content(strip_comments(text).splitlines()) else ["fichier vide ou limité au gabarit"]
            gaps += _section_gaps(text, SECURITE_FILES[name])
        else:
            continue  # fichier recommandé, hors périmètre mandatory (non signalé)
        results.append(_res(sid, rel, gaps, "conforme", "rubriques manquantes/vides"))
    if not ctx.explicit:  # gate : fichiers mandatory absents = écart (SG-2)
        docs = [t for t in ctx.targets if t.startswith("documentation/")]
        if docs:
            missing = [f"documentation/{f}" for f in DAS_FILES if f"documentation/{f}" not in ctx.targets and not ctx.exists(f"documentation/{f}")]
            missing += [f"…/architecture-securite/{f}" for f in SECURITE_FILES if not any(_is_securite_file(t, f) for t in ctx.targets)]
            if missing:
                results.append(Result(sid, "documentation/", GAP, f"fichiers mandatory manquants : {len(missing)}", missing))
    return results or _no_scope(sid, "ADR, DAS ou chapitre architecture-securite")


# --------------------------------------------------------------------------- #
# upstream-coverage
# --------------------------------------------------------------------------- #


def run_upstream_coverage(ctx: Ctx) -> list[Result]:
    sid, results = "upstream-coverage", []
    ensemble: list[str] = []
    for rel in ctx.targets:
        text = ctx.text(rel)
        if ADR_PATH.match(rel):
            gaps = []
            refs = find_section(sections(text), "Références")
            if not (refs and has_content(refs.body)):
                gaps.append("section « Références » absente ou vide")
            if not ISSUE_RE.search(text):
                gaps.append("aucune référence à l'issue d'origine (ALI-/HOM-/ORIG-<n>)")
            results.append(_res(sid, rel, gaps, "référence amont présente", "référence amont manquante"))
        else:
            ensemble.append(rel)
    if ensemble:  # documentation/ et livrables/ : évalués en ensemble
        cited = [r for r in ensemble if ISSUE_RE.search(ctx.text(r))]
        if cited:
            results.append(Result(sid, f"ensemble ({len(ensemble)} fichier(s))", OK,
                                  f"référence amont présente ({len(cited)}/{len(ensemble)} fichier(s) citent l'issue)"))
        else:
            results.append(Result(sid, f"ensemble ({len(ensemble)} fichier(s))", GAP,
                                  "aucune référence amont détectée", [f"sans référence : {r}" for r in ensemble]))
    return results or _no_scope(sid, "décisions, documentation ou livrables")


# --------------------------------------------------------------------------- #
# diagram-validity (parsing statique : structure, pas de rendu — SG-4)
# --------------------------------------------------------------------------- #

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


def _blocks(text: str) -> list[tuple[str, int, list[str]]]:
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


def run_diagram_validity(ctx: Ctx) -> list[Result]:
    sid, results = "diagram-validity", []
    for rel in ctx.targets:
        text, gaps, count = ctx.text(rel), [], 0
        if rel.endswith((".puml", ".dsl")):
            lines = text.splitlines()
            count, gaps = 1, (_check_plantuml if rel.endswith(".puml") else lambda b, s: _check_structurizr(b, s, True))(lines, 1)
        else:
            if (n := unterminated_fence(text.splitlines())):
                gaps.append(f"ligne {n} : bloc de code non refermé")
            for lang, start, block in _blocks(text):
                count += 1
                fn = {"mermaid": _check_mermaid, "plantuml": _check_plantuml, "puml": _check_plantuml}.get(lang, _check_structurizr)
                gaps += [f"[{lang}] {g}" for g in fn(block, start)]
        if count == 0 and not gaps:
            continue  # aucun diagramme dans ce fichier : rien à vérifier
        results.append(_res(sid, rel, gaps, f"syntaxe valide ({count} diagramme(s), contrôle structurel)", "erreur de parsing"))
    return results or _no_scope(sid, "aucun diagramme mermaid/plantuml/structurizr trouvé")


# --------------------------------------------------------------------------- #
# detailed-arch-refs
# --------------------------------------------------------------------------- #

_BAD_LINK = re.compile(r"\]\([^)\s]*(?:architecture-detaillee|architecture-securite)/[^)\s]*\.md[^)]*\)")
_SYS_SUFFIX = re.compile(r"\s\((?:SYS|SYSTEM|SYSTÈME)-?\d+[^)]*\)\s*$", re.I)


def run_detailed_arch_refs(ctx: Ctx) -> list[Result]:
    sid, results = "detailed-arch-refs", []
    for rel in ctx.targets:
        lines = strip_comments(ctx.text(rel)).splitlines()
        mask, gaps = code_mask(lines), []
        for i, line in enumerate(lines, 1):
            if mask[i - 1]:
                continue
            for m in _BAD_LINK.finditer(line):
                gaps.append(f"ligne {i} : renvoi par chemin de fichier {m.group(0)[2:-1]!r} (attendu : documentation/<SS>#<ancre>)")
            if re.match(r"^#{1,6}\s", line) and _SYS_SUFFIX.search(line):
                gaps.append(f"ligne {i} : titre avec suffixe de système « {line.strip()} »")
        results.append(_res(sid, rel, gaps, "conforme", "renvoi/titre non conforme"))
    return results or _no_scope(sid, "documentation/**/*.md")


# --------------------------------------------------------------------------- #
# data-lifecycle
# --------------------------------------------------------------------------- #

DL_FILE = "documentation/10-cycle_vie_donnees.md"
DL_SECTIONS = ["Cycle de vie des données", "Gouvernance de données", "Classification des données"]
_LIFECYCLE = re.compile(r"collecte|stockage|utilisation|archivage|suppression|conservation|r[ée]tention|destruction|purge", re.I)
_LEVEL = re.compile(r"public|interne|confidentiel|restreint|sensible|secret|personnel|pii|rp|nominatif|classifi", re.I)


def run_data_lifecycle(ctx: Ctx) -> list[Result]:
    sid = "data-lifecycle"
    if not ctx.exists(DL_FILE):
        return [Result(sid, DL_FILE, GAP, "fichier absent", [f"{DL_FILE} introuvable dans le projet"])]
    secs = sections(ctx.text(DL_FILE))
    gaps = _section_gaps(ctx.text(DL_FILE), DL_SECTIONS)
    cycle, klass = find_section(secs, DL_SECTIONS[0]), find_section(secs, DL_SECTIONS[2])
    if cycle and has_content(cycle.body) and not _LIFECYCLE.search("\n".join(cycle.body)):
        gaps.append("aucune donnée rattachée à une étape du cycle de vie (collecte/stockage/utilisation/archivage/suppression)")
    if klass and has_content(klass.body) and not _LEVEL.search("\n".join(klass.body)):
        gaps.append("aucune donnée du projet classifiée (niveau de sensibilité absent)")
    return [_res(sid, DL_FILE, gaps, "présent et renseigné (données projet classifiées + rattachées au cycle)", "document incomplet")]


# --------------------------------------------------------------------------- #
# claim-sources
# --------------------------------------------------------------------------- #

_MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_ADR_REF = re.compile(r"\bADR[- ]?(\d{4})\b", re.I)
_HYPOTHESIS = re.compile(r"hypoth[eè]se", re.I)
_CONFIRMED = re.compile(r"confirm(?:ée?|ation)\s+(?:humaine|par)|valid[ée]e?\s+par|confirm[ée]\s+le|✅", re.I)


def _with_continuation(lines: list[str], i: int) -> str:
    """Ligne `i` (1-based) + la suivante, si celle-ci ne porte pas une autre hypothèse."""
    nxt = lines[i] if i < len(lines) and not _HYPOTHESIS.search(lines[i]) else ""
    return f"{lines[i - 1]} {nxt}"


def run_claim_sources(ctx: Ctx) -> list[Result]:
    sid, results = "claim-sources", []
    for rel in ctx.targets:
        lines = strip_comments(ctx.text(rel)).splitlines()
        mask, gaps = code_mask(lines), []
        base = (ctx.root / rel).parent
        for i, line in enumerate(lines, 1):
            if mask[i - 1]:
                continue
            for m in _MD_LINK.finditer(line):
                target = m.group(1).split("#")[0]
                if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue  # ancre locale, URL ou mailto : non résolu hors ligne (SG-4)
                if not (base / target).resolve().exists():
                    gaps.append(f"ligne {i} : source non résoluble « {target} »")
            for m in _ADR_REF.finditer(line):
                if not list((ctx.root / "decisions").glob(f"{m.group(1)}-*.md")):
                    gaps.append(f"ligne {i} : ADR-{m.group(1)} cité mais introuvable dans decisions/")
            if _HYPOTHESIS.search(line) and not _CONFIRMED.search(_with_continuation(lines, i)):
                gaps.append(f"ligne {i} : hypothèse sans confirmation humaine explicite tracée")
        if ADR_PATH.match(rel):
            refs = find_section(sections(ctx.text(rel)), "Références")
            if not (refs and has_content(refs.body)):
                gaps.append("ADR sans source : section « Références » absente ou vide")
        results.append(_res(sid, rel, gaps, "affirmations sourcées", "source manquante / hypothèse non confirmée"))
    return results or _no_scope(sid, "documentation/*.md, decisions/NNNN-*.md")


# --------------------------------------------------------------------------- #
# traceability
# --------------------------------------------------------------------------- #

_SCENARIO = re.compile(r"^#{2,6}\s+(?:Scenario|Scénario)\b", re.I)


def run_traceability(ctx: Ctx) -> list[Result]:
    sid = "traceability"
    texts = {r: strip_comments(strip_front_matter(ctx.text(r))) for r in ctx.targets}
    gaps: list[str] = []
    ba_defs: dict[str, tuple[str, int, str]] = {}  # BA -> (fichier, ligne, texte)
    req_ids: dict[str, str] = {}  # exigence -> 1er fichier où elle apparaît
    pairs: set[tuple[str, str]] = set()
    for rel, text in texts.items():
        lines = text.splitlines()
        mask = code_mask(lines)
        for i, line in enumerate(lines, 1):
            if mask[i - 1] or re.search(r"\b(?:BA|N?FR)-(?:xxx|…|\.\.\.)", line, re.I):
                continue
            bas, reqs = set(BA_RE.findall(line)), set(REQ_RE.findall(line))
            for b in bas:
                if b not in ba_defs or (MOSCOW.search(line) and not MOSCOW.search(ba_defs[b][2])):
                    ba_defs[b] = (rel, i, line)
                pairs.update((b, r) for r in reqs)
            for r in reqs:
                req_ids.setdefault(r, rel)
    if not ba_defs and not req_ids:
        return [Result(sid, "(périmètre)", UNAVAILABLE,
                       "indisponible : aucun identifiant amont BA-…/FR-…/NFR-… trouvé (fail closed)")]
    linked_ba = {b for b, _ in pairs}
    for b, (rel, i, line) in sorted(ba_defs.items()):
        if not MOSCOW.search(line):
            gaps.append(f"{b} ({rel}:{i}) : priorité MoSCoW absente")
        if b not in linked_ba:
            gaps.append(f"{b} ({rel}:{i}) : aucune exigence liée (FR-/NFR- sur la même ligne)")
    downstream = [r for r in ctx.targets if r.startswith(("decisions/", "livrables/"))]
    for r, src in sorted(req_ids.items()):
        if not any(re.search(rf"\b{re.escape(r)}\b", texts[d]) for d in downstream):
            gaps.append(f"{r} ({src}) : exigence sans ADR ni livrable aval")
    all_ids = set(ba_defs) | set(req_ids)
    for rel in (d for d in downstream if ADR_PATH.match(d)):
        if not (set(BA_RE.findall(texts[rel])) | set(REQ_RE.findall(texts[rel]))) & all_ids:
            gaps.append(f"{rel} : décision sans exigence ni besoin amont (orphelin dérivé)")
    for rel, text in texts.items():  # scénarios de spec : « Tracé vers » avec BA-… et exigence
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if _SCENARIO.match(line):
                nxt = "\n".join(lines[idx + 1: idx + 15])
                trace = re.search(r"Tracé vers\s*:(.*)", nxt)
                if not trace or not BA_RE.search(trace.group(1)):
                    gaps.append(f"{rel}:{idx + 1} : scénario sans « Tracé vers » vers un besoin BA-…")
    return [_res(sid, f"ensemble ({len(ctx.targets)} fichier(s))", gaps, "chaîne tracée", "maillon manquant / orphelin")]


CHECKS: dict[str, Callable[[Ctx], list[Result]]] = {
    "required-sections": run_required_sections,
    "upstream-coverage": run_upstream_coverage,
    "diagram-validity": run_diagram_validity,
    "detailed-arch-refs": run_detailed_arch_refs,
    "data-lifecycle": run_data_lifecycle,
    "claim-sources": run_claim_sources,
    "traceability": run_traceability,
}
