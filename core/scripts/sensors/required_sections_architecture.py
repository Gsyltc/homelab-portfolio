#!/usr/bin/env python3
"""Sensor `required-sections-architecture` — applique le bloc `checks` de `core/sensors/sensors/required-sections-architecture.md`.

Couvre la DAS (fichiers mandatory de `documentation/`) et l'architecture détaillée (chapitre `architecture-securite/`).
Exécution seule : `python3 core/scripts/sensors/required_sections_architecture.py --root <projet> [--path <fichier>...] [--format json]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import GAP, Result, has_content, strip_comments  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402
from sensorlib.sections import section_gaps  # noqa: E402

ID = "required-sections-architecture"

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


def _is_securite_file(rel: str, name: str) -> bool:
    return rel.startswith("documentation/") and rel.endswith(f"architecture-securite/{name}")


def _expected(rel: str) -> list[str] | None:
    """Sections attendues du fichier `rel` (DAS ou architecture détaillée) ; None = hors périmètre."""
    if rel.startswith("documentation/") and rel.count("/") == 1 and rel.rsplit("/", 1)[-1] in DAS_FILES:
        return DAS_FILES[rel.rsplit("/", 1)[-1]]
    return next((SECURITE_FILES[n] for n in SECURITE_FILES if _is_securite_file(rel, n)), None)


def run(ctx: Ctx) -> list[Result]:
    results = []
    for rel in ctx.targets:
        expected = _expected(rel)
        if expected is None:
            continue  # fichier recommandé, hors périmètre mandatory (non signalé)
        text = ctx.text(rel)
        gaps = [] if has_content(strip_comments(text).splitlines()) else ["fichier vide ou limité au gabarit"]
        gaps += section_gaps(text, expected)
        results.append(res(ID, rel, gaps, "conforme", "rubriques manquantes/vides"))
    if not ctx.explicit and any(t.startswith("documentation/") for t in ctx.targets):  # gate : fichier mandatory absent = écart (SG-2)
        missing = [f"documentation/{f}" for f in DAS_FILES
                   if f"documentation/{f}" not in ctx.targets and not ctx.exists(f"documentation/{f}")]
        missing += [f"…/architecture-securite/{f}" for f in SECURITE_FILES
                    if not any(_is_securite_file(t, f) for t in ctx.targets)]
        if missing:
            results.append(Result(ID, "documentation/", GAP, f"fichiers mandatory manquants : {len(missing)}", missing))
    return results or no_scope(ID, "DAS ou chapitre architecture-securite")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
