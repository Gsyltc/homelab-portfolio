#!/usr/bin/env python3
"""Sensor `repas-calendrier-agenda` — les repas retenus sont dans le calendrier Home Assistant.

Pour chaque repas retenu à venir (date ≥ date de référence, ou la date passée en `--jour`) :

1. un évènement « repas » existe le jour du repas, **19h–20h**, dont le `summary` porte le nom
   du plat et dont la `description` liste les **ingrédients en puces** (`- ingrédient`) ;
2. l'évènement du lendemain existe, **12h–13h**, même `summary`, **sans description**.

Advisory par défaut (code 0) ; `--strict` renvoie 1 en cas d'écart ou d'indisponibilité.
Aucun secret n'est affiché : l'URL et le jeton Home Assistant ne sortent jamais du script.

Exécution : `python3 plugins/medical-assistant/scripts/sensors/repas_calendrier_agenda.py \
    --data-dir /nfs/workspace/datas/repas [--date AAAA-MM-JJ] [--jour AAAA-MM-JJ] [--format json]`
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _communs import (  # noqa: E402
    FICHIERS, GAP, OK, UNAVAILABLE, Resultat, afficher, code_sortie, lire_front_matter,
    lire_tableau, norm, parse_jour, chemin_donnees,
)

ID = "repas-calendrier-agenda"
BLOQUANT = False

URL_ENV = "HOMEASSISTANT_URL"
TOKEN_ENV = "HOMEASSISTANT_TOKEN"
ENTITY_ENV = "HOMEASSISTANT_CALENDAR_ENTITY"
DEFAULT_ENTITY = "calendar.repas"

HEURE_REPAS_DEBUT, HEURE_REPAS_FIN = 19, 20
HEURE_LENDEMAIN_DEBUT, HEURE_LENDEMAIN_FIN = 12, 13


# --------------------------------------------------------------------------- #
# Données de repas
# --------------------------------------------------------------------------- #


def charger_repas(data_dir: Path, reference: date, jour: date | None = None) -> list[dict]:
    """Repas retenus à contrôler : date ≥ référence (ou date == `jour`), triés par date."""
    chemin = data_dir / FICHIERS["retenus"]
    if not chemin.is_file():
        raise FileNotFoundError(str(chemin))
    meta, corps = lire_front_matter(chemin.read_text(encoding="utf-8"))
    rangees, _ = lire_tableau(corps)
    repas = []
    for rangee in rangees:
        jour_repas = parse_jour(rangee.get("Date", ""))
        if jour_repas is None:
            continue
        if jour is not None and jour_repas != jour:
            continue
        if jour is None and jour_repas < reference:
            continue
        repas.append({"date": jour_repas, "repas": rangee.get("Repas", "")})
    return sorted(repas, key=lambda r: r["date"])


# --------------------------------------------------------------------------- #
# Accès Home Assistant (lecture seule)
# --------------------------------------------------------------------------- #


def _dt(valeur) -> datetime | None:
    """Date/heure ISO d'un évènement HA (dateTime ou date) → datetime, sinon None."""
    brut = valeur.get("dateTime") or valeur.get("date") if isinstance(valeur, dict) else valeur
    if not brut:
        return None
    brut = str(brut)
    try:
        dt = datetime.fromisoformat(brut.replace("Z", "+00:00"))
    except ValueError:
        return None
    if "T" not in brut:
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt


def normaliser_evenements(bruts: list[dict]) -> list[dict]:
    evenements = []
    for ev in bruts or []:
        debut, fin = _dt(ev.get("start")), _dt(ev.get("end"))
        if debut is None:
            continue
        evenements.append({
            "summary": str(ev.get("summary") or ""),
            "description": str(ev.get("description") or ""),
            "debut": debut,
            "fin": fin or debut,
        })
    return evenements


def _creneau(ev: dict, jour: date, debut: int, fin: int) -> bool:
    d, f = ev["debut"], ev["fin"]
    return (
        d.date() == jour
        and d.hour == debut and d.minute == 0
        and f.hour == fin and f.minute == 0
    )


def _correspond(ev: dict, plat: str) -> bool:
    evenement, cible = norm(ev["summary"]), norm(plat)
    return bool(cible) and (cible in evenement or evenement in cible)


def correler(repas: list[dict], evenements: list[dict]) -> list[str]:
    """Écarts entre les repas attendus et les évènements du calendrier (fonction pure, testable)."""
    ecarts: list[str] = []
    for entree in repas:
        jour_repas, plat = entree["date"], entree["repas"]
        ev_repas = [e for e in evenements if _creneau(e, jour_repas, HEURE_REPAS_DEBUT, HEURE_REPAS_FIN) and _correspond(e, plat)]
        if not ev_repas:
            ecarts.append(f"{jour_repas} « {plat} » : aucun évènement repas {HEURE_REPAS_DEBUT}h–{HEURE_REPAS_FIN}h au calendrier")
        else:
            description = (ev_repas[0]["description"] or "").strip()
            puces = [l for l in description.splitlines() if l.strip().startswith("- ")]
            if not puces:
                ecarts.append(f"{jour_repas} « {plat} » : ingrédients non consignés (description sans puce « - »)")
            elif any(l.strip() and not l.strip().startswith("- ") for l in description.splitlines()):
                ecarts.append(f"{jour_repas} « {plat} » : description non conforme (chaque ligne d'ingrédient doit commencer par « - »)")

        lendemain = jour_repas + timedelta(days=1)
        ev_lendemain = [e for e in evenements if _creneau(e, lendemain, HEURE_LENDEMAIN_DEBUT, HEURE_LENDEMAIN_FIN) and _correspond(e, plat)]
        if not ev_lendemain:
            ecarts.append(f"{jour_repas} « {plat} » : aucun créneau du lendemain {lendemain} {HEURE_LENDEMAIN_DEBUT}h–{HEURE_LENDEMAIN_FIN}h")
        elif (ev_lendemain[0]["description"] or "").strip():
            ecarts.append(f"{jour_repas} « {plat} » : le créneau du lendemain ne doit pas porter de description")
    return ecarts


def lire_calendrier(base: str, token: str, entite: str, debut: date, fin: date) -> list[dict]:
    """Évènements `[debut, fin]` du calendrier HA (lecture seule, stdlib)."""
    url = (
        f"{base.rstrip('/')}/api/calendars/{quote(entite, safe='.')}"
        f"?start={quote(debut.isoformat() + 'T00:00:00')}"
        f"&end={quote(fin.isoformat() + 'T23:59:59')}"
    )
    requete = Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    with urlopen(requete, timeout=20) as reponse:  # noqa: S310 — URL fournie par l'environnement de l'agent
        return json.loads(reponse.read().decode("utf-8"))


# --------------------------------------------------------------------------- #
# Exécution
# --------------------------------------------------------------------------- #


def run(args) -> list[Resultat]:
    reference = parse_jour(args.date) if args.date else date.today()
    if reference is None:
        return [Resultat(ID, args.date, UNAVAILABLE, "date de référence invalide (attendu AAAA-MM-JJ)")]
    jour = parse_jour(args.jour) if args.jour else None
    if args.jour and jour is None:
        return [Resultat(ID, args.jour, UNAVAILABLE, "--jour invalide (attendu AAAA-MM-JJ)")]

    try:
        repas = charger_repas(chemin_donnees(args.data_dir), reference, jour)
    except FileNotFoundError as exc:
        return [Resultat(ID, FICHIERS["retenus"], UNAVAILABLE, f"indisponible : fichier absent ({exc})")]

    if not repas:
        cible = jour.isoformat() if jour else f"≥ {reference.isoformat()}"
        return [Resultat(ID, cible, OK, "aucun repas à venir à contrôler")]

    base, token = os.environ.get(URL_ENV, "").strip(), os.environ.get(TOKEN_ENV, "").strip()
    manquants = [nom for nom, valeur in ((URL_ENV, base), (TOKEN_ENV, token)) if not valeur]
    if manquants:
        return [Resultat(ID, "calendrier HA", UNAVAILABLE, f"indisponible : variable(s) d'environnement absente(s) : {', '.join(manquants)}")]

    entite = os.environ.get(ENTITY_ENV, "").strip() or DEFAULT_ENTITY
    debut = min(r["date"] for r in repas)
    fin = max(r["date"] for r in repas) + timedelta(days=1)
    try:
        bruts = lire_calendrier(base, token, entite, debut, fin)
    except HTTPError as exc:  # message sans URL ni jeton
        return [Resultat(ID, entite, UNAVAILABLE, f"indisponible : Home Assistant a répondu HTTP {exc.code}")]
    except (URLError, TimeoutError, ValueError) as exc:
        return [Resultat(ID, entite, UNAVAILABLE, f"indisponible : calendrier injoignable ({type(exc).__name__})")]

    ecarts = correler(repas, normaliser_evenements(bruts))
    if ecarts:
        return [Resultat(ID, f"{len(repas)} repas à venir", GAP, f"{len(ecarts)} écart(s) calendrier", ecarts)]
    return [Resultat(ID, f"{len(repas)} repas à venir", OK, "repas et ingrédients présents au calendrier (repas 19h–20h + créneau 12h–13h)")]


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description="Sensor repas-calendrier-agenda (advisory).")
    parseur.add_argument("--data-dir", default="/nfs/workspace/datas/repas")
    parseur.add_argument("--date", help="date de référence AAAA-MM-JJ (défaut : aujourd'hui)")
    parseur.add_argument("--jour", help="ne contrôler que ce jour AAAA-MM-JJ")
    parseur.add_argument("--format", choices=["text", "json"], default="text")
    parseur.add_argument("--strict", action="store_true", help="code 1 en cas d'écart (CI)")
    args = parseur.parse_args(argv)
    resultats = run(args)
    afficher(ID, resultats, args.format)
    return code_sortie(resultats, args.strict, BLOQUANT)


if __name__ == "__main__":
    sys.exit(main())
