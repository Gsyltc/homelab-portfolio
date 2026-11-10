"""Utilitaires communs aux sensors Python du plugin `medical-assistant`.

Python ≥ 3.9, bibliothèque standard uniquement. Conventions de verdict :

- `✅` conforme ;
- `⚠️` écart (le contrôle a tourné, la donnée ne respecte pas le contrat) ;
- `⛔` indisponible (contrôle impossible : donnée ou environnement absent) — **jamais lu comme un vert**.

Aucun secret n'est affiché : ni l'URL ni le jeton Home Assistant ne sortent des scripts.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

OK, GAP, UNAVAILABLE = "✅", "⚠️", "⛔"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TABLE_HEADER = ["Date", "Repas", "Appareil", "Emplacement de la recette"]

FICHIERS = {
    "retenus": "repas-retenus.md",
    "exclus": "repas-exclus.md",
    "refuses": "ingredients-refuses.md",
}


@dataclass
class Resultat:
    """Verdict d'un sensor sur une cible, avec ses écarts détaillés."""

    sensor: str
    cible: str
    verdict: str
    message: str
    details: list[str] = field(default_factory=list)


def norm(value: str) -> str:
    """Libellé comparable : minuscules, sans accents ni ponctuation."""
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(c for c in value if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def parse_jour(value) -> date | None:
    """Date ISO `AAAA-MM-JJ` → `date`, sinon `None`."""
    if not isinstance(value, str) or not DATE_RE.match(value.strip()):
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


def lire_front_matter(texte: str) -> tuple[dict[str, str], str]:
    """Front matter plat `clé: valeur` → (métadonnées, corps). Absent ou mal formé → ({}, texte)."""
    if not texte.startswith("---\n"):
        return {}, texte
    fin = texte.find("\n---\n", 4)
    if fin == -1:
        return {}, texte
    meta: dict[str, str] = {}
    for ligne in texte[4:fin].splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#"):
            continue
        if ":" not in ligne:
            return {}, texte
        cle, _, valeur = ligne.partition(":")
        meta[cle.strip()] = valeur.strip().strip('"').strip("'")
    return meta, texte[fin + 5 :]


def lire_tableau(corps: str) -> tuple[list[dict[str, str]], list[str]]:
    """Lit le tableau des repas retenus ; retourne (lignes, écarts de forme)."""
    lignes = corps.splitlines()
    entete = None
    for i, ligne in enumerate(lignes):
        if ligne.strip().startswith("|") and "Repas" in ligne and "Date" in ligne:
            entete = i
            break
    if entete is None:
        return [], ["tableau des repas introuvable (en-tête « Date | Repas | Appareil | Emplacement de la recette »)"]

    ecarts: list[str] = []
    colonnes = [c.strip() for c in lignes[entete].strip().strip("|").split("|")]
    if colonnes != TABLE_HEADER:
        ecarts.append("en-tête de tableau non conforme : " + " | ".join(colonnes))

    rangees: list[dict[str, str]] = []
    for ligne in lignes[entete + 1 :]:
        s = ligne.strip()
        if not s.startswith("|"):
            if rangees:
                break
            continue
        cellules = [c.strip() for c in s.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cellules):
            continue  # ligne séparatrice
        if len(cellules) != len(TABLE_HEADER):
            ecarts.append(f"ligne à {len(cellules)} colonnes (attendu {len(TABLE_HEADER)}) : {s[:100]}")
            continue
        rangees.append(dict(zip(TABLE_HEADER, cellules)))
    return rangees, ecarts


def lire_liste(corps: str, libelle: str) -> tuple[list[str], list[str]]:
    """Lit une liste à puces `- élément` ; retourne (éléments, écarts de forme)."""
    elements: list[str] = []
    ecarts: list[str] = []
    for ligne in corps.splitlines():
        s = ligne.strip()
        if not s or s.startswith("#") or s.startswith(">"):
            continue
        if s.startswith("- "):
            contenu = s[2:].strip()
            if not contenu:
                ecarts.append(f"{libelle} : puce vide")
            else:
                elements.append(contenu)
        elif s.startswith("|"):
            ecarts.append(f"{libelle} : tableau inattendu (liste à puces attendue) : {s[:80]}")
        else:
            ecarts.append(f"{libelle} : ligne hors format (attendu « - élément ») : {s[:80]}")
    return elements, ecarts


def afficher(sensor: str, resultats: list[Resultat], fmt: str = "text") -> None:
    if fmt == "json":
        print(json.dumps([r.__dict__ for r in resultats], ensure_ascii=False, indent=2))
        return
    for r in resultats:
        print(f"Sensor {r.sensor} — {r.cible}")
        print(f"- verdict : {r.verdict} {r.message}")
        for detail in r.details:
            print(f"  - {detail}")


def code_sortie(resultats: list[Resultat], strict: bool, bloquant: bool) -> int:
    """Code retour : 1 seulement si `--strict` (CI) ou sensor bloquant, et qu'un écart existe."""
    ecart = any(r.verdict in (GAP, UNAVAILABLE) for r in resultats)
    return 1 if ecart and (strict or bloquant) else 0


def chemin_donnees(data_dir: str) -> Path:
    return Path(data_dir).expanduser()
