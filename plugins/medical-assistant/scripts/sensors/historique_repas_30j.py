#!/usr/bin/env python3
"""Sensor `historique-repas-30j` — l'historique des repas tient dans 30 jours glissants.

Contrôle **bloquant** (décision humaine, AUQU-153) : `repas-retenus.md` ne doit contenir aucune
entrée dont la date est antérieure à *date de référence − 30 jours*. Un repas plus ancien laissé
dans l'historique = **échec** (il redevient proposable et brouille le décompte des 30 jours).

Le script purge-t-il ? **Non** : il ne modifie jamais la donnée. C'est l'agent qui purge
(étape « Purge de l'historique glissant »), puis relance le sensor.

Exécution : `python3 plugins/medical-assistant/scripts/sensors/historique_repas_30j.py \
    --data-dir /nfs/workspace/datas/repas [--date AAAA-MM-JJ] [--format json]`
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _communs import (  # noqa: E402
    FICHIERS, GAP, OK, UNAVAILABLE, Resultat, afficher, code_sortie, chemin_donnees,
    lire_front_matter, lire_tableau, parse_jour,
)

ID = "historique-repas-30j"
BLOQUANT = True
FENETRE_JOURS = 30


def controler(data_dir: Path, reference: date) -> list[Resultat]:
    chemin = data_dir / FICHIERS["retenus"]
    if not chemin.is_file():
        return [Resultat(ID, FICHIERS["retenus"], UNAVAILABLE, f"indisponible : fichier absent ({chemin})")]

    _, corps = lire_front_matter(chemin.read_text(encoding="utf-8"))
    rangees, ecarts_forme = lire_tableau(corps)
    if ecarts_forme:
        return [Resultat(ID, FICHIERS["retenus"], UNAVAILABLE,
                         "indisponible : tableau illisible, contrôle impossible", ecarts_forme)]

    limite = reference - timedelta(days=FENETRE_JOURS)
    trop_anciens: list[str] = []
    dates_invalides: list[str] = []
    for rangee in rangees:
        jour = parse_jour(rangee.get("Date", ""))
        if jour is None:
            dates_invalides.append(f"date illisible : {rangee.get('Date', '')!r} ({rangee.get('Repas', '')})")
        elif jour < limite:
            trop_anciens.append(f"{jour} — {rangee.get('Repas', '')} (plus de {FENETRE_JOURS} jours)")

    details = dates_invalides + trop_anciens
    if details:
        return [Resultat(ID, FICHIERS["retenus"], GAP,
                         f"FAILED : {len(trop_anciens)} repas au-delà de {FENETRE_JOURS} jours"
                         + (f", {len(dates_invalides)} date(s) illisible(s)" if dates_invalides else ""),
                         details)]
    return [Resultat(ID, FICHIERS["retenus"], OK,
                     f"historique conforme : {len(rangees)} entrée(s), aucune plus ancienne que {limite} (30 jours)")]


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description="Sensor historique-repas-30j (bloquant).")
    parseur.add_argument("--data-dir", default="/nfs/workspace/datas/repas")
    parseur.add_argument("--date", help="date de référence AAAA-MM-JJ (défaut : aujourd'hui)")
    parseur.add_argument("--format", choices=["text", "json"], default="text")
    parseur.add_argument("--strict", action="store_true", help="(déjà bloquant : conservé pour uniformité)")
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
