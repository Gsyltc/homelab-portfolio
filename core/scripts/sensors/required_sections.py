#!/usr/bin/env python3
"""Sensor `required-sections` — applique le bloc `checks` de `core/sensors/sensors/required-sections.md`.

Exécution seule : `python3 core/scripts/sensors/required_sections.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import GAP, Result, find_section, has_content, norm, sections, strip_comments  # noqa: E402
from sensorlib.context import Ctx, ADR_PATH, no_scope, res  # noqa: E402
from sensorlib.sections import section_gaps  # noqa: E402

ID = "required-sections"


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
    gaps += section_gaps(text, [x for x in ADR_SECTIONS if not (x == "Date de création" and date_in_status)])
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


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    if not ctx.targets and not ctx.explicit:
        pass  # le balayage de gate signale quand même les fichiers mandatory manquants
    for rel in ctx.targets:
        text = ctx.text(rel)
        base = rel.rsplit("/", 1)[-1]
        if ADR_PATH.match(rel):
            gaps = _adr_gaps(text)
        elif rel.startswith("documentation/") and rel.count("/") == 1 and base in DAS_FILES:
            gaps = [] if has_content(strip_comments(text).splitlines()) else ["fichier vide ou limité au gabarit"]
            gaps += section_gaps(text, DAS_FILES[base])
        elif any(_is_securite_file(rel, n) for n in SECURITE_FILES):
            name = rel.rsplit("architecture-securite/", 1)[1]
            gaps = [] if has_content(strip_comments(text).splitlines()) else ["fichier vide ou limité au gabarit"]
            gaps += section_gaps(text, SECURITE_FILES[name])
        else:
            continue  # fichier recommandé, hors périmètre mandatory (non signalé)
        results.append(res(sid, rel, gaps, "conforme", "rubriques manquantes/vides"))
    if not ctx.explicit:  # gate : fichiers mandatory absents = écart (SG-2)
        docs = [t for t in ctx.targets if t.startswith("documentation/")]
        if docs:
            missing = [f"documentation/{f}" for f in DAS_FILES if f"documentation/{f}" not in ctx.targets and not ctx.exists(f"documentation/{f}")]
            missing += [f"…/architecture-securite/{f}" for f in SECURITE_FILES if not any(_is_securite_file(t, f) for t in ctx.targets)]
            if missing:
                results.append(Result(sid, "documentation/", GAP, f"fichiers mandatory manquants : {len(missing)}", missing))
    return results or no_scope(sid, "ADR, DAS ou chapitre architecture-securite")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
