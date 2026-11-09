"""Point d'entrée commun des scripts de sensors exécutés seuls (`python3 sensors/<id>.py`)."""

from __future__ import annotations

import argparse
import os


def main(sensor_id: str) -> int:
    ap = argparse.ArgumentParser(description=f"Exécute le sensor {sensor_id} (advisory : code 0 par défaut).")
    ap.add_argument("--root", default=os.getcwd(), help="racine du projet à vérifier (défaut : répertoire courant)")
    ap.add_argument("--path", nargs="+", help="fichier(s) à vérifier ; absent = balayage de gate")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--strict", action="store_true", help="code 1 si écart ou ⛔ (CI uniquement)")
    args = ap.parse_args()
    import sensor  # dispatcher : même logique de manifeste, de provenance et de verdict (SG-1/2/5)

    argv = ["--root", args.root] + (["--strict"] if args.strict else []) + ["fire", sensor_id, "--format", args.format]
    if args.path:
        argv += ["--path", *args.path]
    return sensor.main(argv)
