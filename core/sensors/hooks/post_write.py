#!/usr/bin/env python3
"""Hook d'écriture advisory : exécute les sensors `fire_on: write` sur le fichier écrit.

Point d'entrée **unique et agnostique du harnais** (ADR 0038) : lit le JSON de hook sur stdin
(Claude Code `PostToolUse`, Kiro CLI `postToolUse`, ou tout harnais fournissant
`tool_input.file_path`), délègue à `core/scripts/sensor.py hook`, et sort **toujours 0**.

Exemples d'enregistrement : `core/sensors/README.md` (§ Hooks).
"""
import subprocess
import sys
from pathlib import Path

SENSOR = Path(__file__).resolve().parents[2] / "scripts" / "sensor.py"

if __name__ == "__main__":
    try:
        subprocess.run([sys.executable, str(SENSOR), "hook", *sys.argv[1:]], stdin=sys.stdin)
        sys.exit(0)  # advisory : jamais bloquant
    except Exception as exc:  # noqa: BLE001 — un hook ne bloque jamais, mais ne se tait pas (SG-2)
        print(f"Sensor hook — ⛔ indisponible : {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(0)
