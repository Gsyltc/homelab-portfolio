#!/usr/bin/env python3
"""Sensors de vérification du dossier sportif (stdlib uniquement).

Sous-commandes :
  suivi    <sport_dir>              format de sport/suivi-sportif.md
  archive  <sport_dir> [--modified] archivage de sport/programme-sportif.md
  all      <sport_dir> [--modified] les deux

Verdicts (même convention que les sensors du dépôt) :
  conforme | ecart | indisponible
Codes de sortie : 0 conforme, 1 ecart, 2 indisponible.
Sortie : JSON sur stdout. Le verdict n'est jamais réinterprété par l'appelant.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SUIVI = "suivi-sportif.md"
PROGRAMME = "programme-sportif.md"
ARCHIVE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})\.programme-sportif\.md$")
SESSION_RE = re.compile(
    r"^## (\d{4}-\d{2}-\d{2}) — Séance confirmée par (patient|humain)\s*$"
)
RPE_RE = re.compile(r"^- RPE séance : (\d{1,2})/10\s*$")
EVA_RE = re.compile(r"^- Douleur \(EVA\) : (\d{1,2})/10\s*$")
FATIGUE_RE = re.compile(r"^- Fatigue lendemain : (aucune|légère|marquée)\s*$")
OPTIONAL_RE = re.compile(r"^- (Symptômes|Retours) : \S.*$")
TABLE_HEADER = "| Exercice | Charge | Séries × répétitions |"
CHARGE_RE = re.compile(r"^(\d+(,\d+)? kg|poids du corps)$")


def _valid_date(text: str, fmt: str = "%Y-%m-%d") -> bool:
    try:
        datetime.strptime(text, fmt)
        return True
    except ValueError:
        return False


def _check_session(date: str, body: list[tuple[int, str]], errors: list[str]) -> None:
    seen = {"rpe": False, "eva": False, "table": False, "rows": 0}
    in_table = False
    for lineno, line in body:
        if not line.strip():
            in_table = False
            continue
        m = RPE_RE.match(line)
        if m:
            seen["rpe"] = True
            if int(m.group(1)) > 10:
                errors.append(f"L{lineno}: RPE hors 0-10")
            continue
        m = EVA_RE.match(line)
        if m:
            seen["eva"] = True
            if int(m.group(1)) > 10:
                errors.append(f"L{lineno}: EVA hors 0-10")
            continue
        if FATIGUE_RE.match(line) or OPTIONAL_RE.match(line):
            continue
        if line.strip() == TABLE_HEADER:
            seen["table"] = True
            in_table = True
            continue
        if in_table and re.match(r"^\|[-\s|]+\|$", line.strip()):
            continue
        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 3 or not cells[0] or not CHARGE_RE.match(cells[1]) or not cells[2]:
                errors.append(f"L{lineno}: ligne d'exercice invalide « {line.strip()} »")
            else:
                seen["rows"] += 1
            continue
        errors.append(f"L{lineno}: ligne non reconnue dans la séance {date} « {line.strip()} »")
    if not seen["rpe"]:
        errors.append(f"Séance {date}: ligne « - RPE séance : N/10 » manquante")
    if not seen["eva"]:
        errors.append(f"Séance {date}: ligne « - Douleur (EVA) : N/10 » manquante")
    if not seen["table"]:
        errors.append(f"Séance {date}: tableau « {TABLE_HEADER} » manquant")
    elif seen["rows"] == 0:
        errors.append(f"Séance {date}: aucun exercice dans le tableau")


def check_suivi(sport_dir: Path) -> dict:
    path = sport_dir / SUIVI
    if not sport_dir.is_dir():
        return {"sensor": "suivi-format", "verdict": "indisponible", "details": [f"{sport_dir} introuvable"]}
    if not path.is_file():
        return {"sensor": "suivi-format", "verdict": "ecart", "details": [f"{SUIVI} absent"]}
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# Suivi sportif"):
        errors.append("L1: titre « # Suivi sportif — <patient> » attendu")
    sessions: list[tuple[str, list[tuple[int, str]]]] = []
    for i, line in enumerate(lines[1:], start=2):
        if line.startswith("## "):
            m = SESSION_RE.match(line)
            if not m:
                errors.append(f"L{i}: en-tête de séance invalide « {line} » "
                              "(attendu « ## yyyy-MM-dd — Séance confirmée par patient|humain »)")
                sessions.append(("?", []))
                continue
            if not _valid_date(m.group(1)):
                errors.append(f"L{i}: date invalide {m.group(1)}")
            sessions.append((m.group(1), []))
        elif sessions:
            sessions[-1][1].append((i, line))
        elif line.strip():
            errors.append(f"L{i}: contenu avant la première séance")
    dates = [d for d, _ in sessions if d != "?"]
    if dates != sorted(dates):
        errors.append("Séances non classées par ordre chronologique croissant")
    if len(dates) != len(set(dates)):
        errors.append("Date de séance en double (regrouper dans une seule séance)")
    for date, body in sessions:
        if date != "?":
            _check_session(date, body, errors)
    return {"sensor": "suivi-format", "verdict": "ecart" if errors else "conforme", "details": errors}


def check_archive(sport_dir: Path, modified: bool) -> dict:
    sensor = "programme-archive"
    if not sport_dir.is_dir():
        return {"sensor": sensor, "verdict": "indisponible", "details": [f"{sport_dir} introuvable"]}
    prog = sport_dir / PROGRAMME
    if not prog.is_file():
        return {"sensor": sensor, "verdict": "ecart", "details": [f"{PROGRAMME} absent"]}
    errors: list[str] = []
    arch_dir = sport_dir / "archives"
    archives: list[Path] = []
    if arch_dir.is_dir():
        for f in sorted(arch_dir.iterdir()):
            m = ARCHIVE_RE.match(f.name)
            if not m or not _valid_date(m.group(1), "%Y-%m-%d_%H-%M"):
                errors.append(f"archives/{f.name}: nom invalide (attendu yyyy-MM-dd_hh-mm.programme-sportif.md)")
            else:
                archives.append(f)
    elif modified:
        errors.append("répertoire archives/ absent")
    if modified:
        if not archives:
            errors.append("modification déclarée mais aucune archive de l'ancienne version")
        else:
            latest = archives[-1]
            current = prog.read_text(encoding="utf-8")
            if latest.read_text(encoding="utf-8") == current:
                errors.append(f"archives/{latest.name} identique au programme actuel : "
                              "la nouvelle version n'a pas été écrite ou l'archive n'est pas celle de l'ancienne version")
            stamp = datetime.strptime(ARCHIVE_RE.match(latest.name).group(1), "%Y-%m-%d_%H-%M")
            if datetime.fromtimestamp(prog.stat().st_mtime) < stamp.replace(second=0):
                errors.append("programme antérieur à sa dernière archive : archive postérieure à la modification")
    pdf = sport_dir / "programme-sportif.pdf"
    if pdf.is_file() and pdf.stat().st_mtime + 1 < prog.stat().st_mtime:
        errors.append("programme-sportif.pdf antérieur au programme : PDF à régénérer")
    return {"sensor": sensor, "verdict": "ecart" if errors else "conforme", "details": errors}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["suivi", "archive", "all"])
    ap.add_argument("sport_dir", type=Path)
    ap.add_argument("--modified", action="store_true",
                    help="le programme vient d'être modifié : exiger l'archive de l'ancienne version")
    args = ap.parse_args(argv)
    results = []
    if args.command in ("suivi", "all"):
        results.append(check_suivi(args.sport_dir))
    if args.command in ("archive", "all"):
        results.append(check_archive(args.sport_dir, args.modified))
    print(json.dumps({"sensors_resultats": results}, ensure_ascii=False, indent=2))
    verdicts = {r["verdict"] for r in results}
    return 2 if "indisponible" in verdicts else 1 if "ecart" in verdicts else 0


if __name__ == "__main__":
    sys.exit(main())
