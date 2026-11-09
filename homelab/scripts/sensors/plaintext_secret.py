#!/usr/bin/env python3
"""Sensor `plaintext-secret` — applique `homelab/sensors/sensors/plaintext-secret.md`.

Détecte des **motifs de secret en clair** (mot de passe / token / clé API / clé privée)
dans un livrable compose ou Terraform. **Ne lit, ne recopie ni n'affiche JAMAIS la valeur** :
le signal porte l'emplacement (fichier:ligne + clé) et le type de motif, jamais le contenu.

Exceptions tolérées : convention `*_FILE`, référence `${...}`, `vault:*`, `/run/secrets/*`.
Parsing **statique** par motif (SG-4), jamais de résolution de secret.

Exécution seule : `python3 homelab/scripts/sensors/plaintext_secret.py --root <projet> [--path <fichier>...]`
(advisory par défaut ; bloquant sur `security-patch` / `new-stack` — résolu par le dispatcher).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import Result, code_mask  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402

ID = "plaintext-secret"

# Motifs de secret en clair : capturent la CLÉ, jamais la valeur (le groupe de valeur n'est pas restitué).
# Le préfixe optionnel `\w*[_.-]?` capte les clés composées (DB_PASSWORD, MYSQL_TOKEN, …).
_PATTERNS = [
    re.compile(r"(?i)(?:^|[^\w])(\w*(?:password|passwd|pwd))\s*[:=]\s*['\"]?[^\s'\"$]{6,}"),
    re.compile(r"(?i)(?:^|[^\w])(\w*(?:token|api[_-]?key|secret|access[_-]?key))\s*[:=]\s*['\"]?[A-Za-z0-9/_+.-]{12,}"),
    re.compile(r"(-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
]
# Exceptions : la ligne porte une référence indirecte (jamais une valeur en clair).
_EXCEPT = re.compile(r"(_FILE\b|\$\{[^}]+\}|\bvault:|/run/secrets/)")
_KEY = re.compile(r"(?i)(\w*(?:password|passwd|pwd|token|api[_-]?key|secret|access[_-]?key))\b")


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    for rel in ctx.targets:
        lines = ctx.text(rel).splitlines()
        mask = code_mask(lines) if rel.endswith(".md") else [False] * len(lines)
        gaps: list[str] = []
        for i, line in enumerate(lines, 1):
            if i - 1 < len(mask) and mask[i - 1]:
                continue
            if _EXCEPT.search(line):
                continue  # référence indirecte tolérée (fichier / Vault / env / secret Docker)
            for pat in _PATTERNS:
                if pat.search(line):
                    key_m = _KEY.search(line)
                    key = key_m.group(1) if key_m else "clé privée PEM"
                    # emplacement + type de motif UNIQUEMENT — jamais la valeur (invariant Homelab)
                    gaps.append(f"{rel}:{i} clé « {key} » — motif de secret en clair (valeur masquée)")
                    break
        results.append(res(sid, rel, gaps, "aucun secret en clair détecté", "motif(s) suspect(s)"))
    return results or no_scope(sid, "aucun fichier compose/.tf/.tfvars dans le périmètre")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
