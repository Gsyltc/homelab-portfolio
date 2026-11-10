#!/usr/bin/env python3
"""Sensor `fichiers-repas-conformes` — les trois fichiers de données sont à jour et conformes.

Contrôle, pour `repas-retenus.md`, `repas-exclus.md` et `ingredients-refuses.md` :

- présence du fichier et d'un front matter plat `clé: valeur` ;
- `type` attendu, `updated` = date ISO valide et non future ;
- `count` entier cohérent avec le nombre réel d'entrées du corps ;
- `repas-retenus.md` : `rolling_window_days: 30`, en-tête de tableau conforme, 4 colonnes par
  ligne, dates ISO valides, `oldest` / `newest` égaux aux bornes réelles ;
- `repas-exclus.md` / `ingredients-refuses.md` : liste à puces `- élément`, sans doublon.

Advisory par défaut (code 0) ; `--strict` renvoie 1 en cas d'écart ou d'indisponibilité.

Exécution : `python3 plugins/medical-assistant/scripts/sensors/fichiers_repas_conformes.py \
    --data-dir /nfs/workspace/datas/repas [--date AAAA-MM-JJ] [--format json]`
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _communs import (  # noqa: E402
    FICHIERS, GAP, OK, UNAVAILABLE, Resultat, afficher, code_sortie, chemin_donnees,
    lire_front_matter, lire_liste, lire_tableau, norm, parse_jour,
)

ID = "fichiers-repas-conformes"
BLOQUANT = False
FENETRE_JOURS = 30


def _entier(meta: dict[str, str], cle: str, ecarts: list[str]) -> int | None:
    valeur = meta.get(cle)
    if valeur is None or valeur.strip() == "":
        ecarts.append(f"front matter : clé « {cle} » absente")
        return None
    try:
        return int(valeur)
    except ValueError:
        ecarts.append(f"front matter : « {cle} » n'est pas un entier ({valeur!r})")
        return None


def _date_front(meta: dict[str, str], cle: str, ecarts: list[str]) -> date | None:
    valeur = meta.get(cle, "")
    if not valeur:
        ecarts.append(f"front matter : clé « {cle} » absente")
        return None
    jour = parse_jour(valeur)
    if jour is None:
        ecarts.append(f"front matter : « {cle} » n'est pas une date ISO ({valeur!r})")
    return jour


def _controler_retenus(chemin: Path) -> list[str]:
    ecarts: list[str] = []
    meta, corps = lire_front_matter(chemin.read_text(encoding="utf-8"))
    if not meta:
        return ["front matter absent ou mal formé"]

    if meta.get("type") != "repas-retenus":
        ecarts.append(f"front matter : type « {meta.get('type', '')} » (attendu « repas-retenus »)")
    _date_front(meta, "updated", ecarts)
    fenetre = _entier(meta, "rolling_window_days", ecarts)
    if fenetre is not None and fenetre != FENETRE_JOURS:
        ecarts.append(f"front matter : rolling_window_days = {fenetre} (attendu {FENETRE_JOURS})")
    declare = _entier(meta, "count", ecarts)

    rangees, ecarts_forme = lire_tableau(corps)
    ecarts += ecarts_forme
    if declare is not None and declare != len(rangees):
        ecarts.append(f"front matter : count = {declare} mais {len(rangees)} ligne(s) dans le tableau")

    dates: list[date] = []
    for rangee in rangees:
        jour = parse_jour(rangee.get("Date", ""))
        if jour is None:
            ecarts.append(f"tableau : date ISO invalide {rangee.get('Date', '')!r} ({rangee.get('Repas', '')})")
            continue
        dates.append(jour)
        for colonne in ("Repas", "Appareil"):
            if not rangee.get(colonne, "").strip():
                ecarts.append(f"tableau : colonne « {colonne} » vide pour {jour}")

    if dates:
        for cle, attendu in (("oldest", min(dates).isoformat()), ("newest", max(dates).isoformat())):
            valeur = meta.get(cle, "")
            if valeur != attendu:
                ecarts.append(f"front matter : {cle} = {valeur!r} (attendu {attendu})")
    else:
        for cle in ("oldest", "newest"):
            if meta.get(cle, "").strip():
                ecarts.append(f"front matter : {cle} renseigné ({meta[cle]!r}) alors que le tableau est vide")
    return ecarts


def _controler_liste(chemin: Path, type_attendu: str, libelle: str) -> list[str]:
    ecarts: list[str] = []
    meta, corps = lire_front_matter(chemin.read_text(encoding="utf-8"))
    if not meta:
        return ["front matter absent ou mal formé"]

    if meta.get("type") != type_attendu:
        ecarts.append(f"front matter : type « {meta.get('type', '')} » (attendu « {type_attendu} »)")
    _date_front(meta, "updated", ecarts)
    declare = _entier(meta, "count", ecarts)

    elements, ecarts_forme = lire_liste(corps, libelle)
    ecarts += ecarts_forme
    if declare is not None and declare != len(elements):
        ecarts.append(f"front matter : count = {declare} mais {len(elements)} élément(s) dans la liste")

    vus: set[str] = set()
    for element in elements:
        cle = norm(element)
        if cle in vus:
            ecarts.append(f"{libelle} : doublon « {element} »")
        vus.add(cle)
    return ecarts


def controler(data_dir: Path, reference: date) -> list[Resultat]:
    resultats: list[Resultat] = []
    controleurs = (
        ("retenus", _controler_retenus),
        ("exclus", lambda chemin: _controler_liste(chemin, "repas-exclus", "repas exclus")),
        ("refuses", lambda chemin: _controler_liste(chemin, "ingredients-refuses", "ingrédients refusés")),
    )

    for cle, controle in controleurs:
        nom = FICHIERS[cle]
        chemin = data_dir / nom
        if not chemin.is_file():
            resultats.append(Resultat(ID, nom, UNAVAILABLE, f"indisponible : fichier absent ({chemin})"))
            continue
        try:
            ecarts = controle(chemin)
        except OSError as exc:
            resultats.append(Resultat(ID, nom, UNAVAILABLE, f"indisponible : lecture impossible ({type(exc).__name__})"))
            continue

        meta, _ = lire_front_matter(chemin.read_text(encoding="utf-8"))
        jour_maj = parse_jour(meta.get("updated", ""))
        if jour_maj and jour_maj > reference:
            ecarts.append(f"front matter : updated ({jour_maj}) postérieur à la date de référence ({reference})")

        if ecarts:
            resultats.append(Resultat(ID, nom, GAP, f"{len(ecarts)} écart(s) de format", ecarts))
        else:
            resultats.append(Resultat(ID, nom, OK, "front matter et corps conformes"))
    return resultats


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description="Sensor fichiers-repas-conformes (advisory).")
    parseur.add_argument("--data-dir", default="/nfs/workspace/datas/repas")
    parseur.add_argument("--date", help="date de référence AAAA-MM-JJ (défaut : aujourd'hui)")
    parseur.add_argument("--format", choices=["text", "json"], default="text")
    parseur.add_argument("--strict", action="store_true", help="code 1 en cas d'écart (CI)")
    args = parseur.parse_args(argv)
    reference = parse_jour(args.date) if args.date else date.today()
    if reference is None:
        resultats = [Resultat(ID, args.date, UNAVAILABLE, "date de référence invalide (attendu AAAA-MM-JJ)")]
    else:
        resultats = controler(chemin_donnees(args.data_dir), reference)
    afficher(ID, resultats, args.format)
    return code_sortie(resultats, args.strict, BLOQUANT)


if __name__ == "__main__":
    sys.exit(main())
