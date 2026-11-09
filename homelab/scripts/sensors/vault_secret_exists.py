#!/usr/bin/env python3
"""Sensor `vault-secret-exists` — applique `homelab/sensors/sensors/vault-secret-exists.md`.

Pour chaque **référence de secret Vault** présente dans le livrable, constate que la
référence est exploitable (chemin résoluble en forme). **Existence seule, JAMAIS la valeur** :
ce sensor ne lit, ne recopie ni n'affiche aucune valeur de secret (invariant non négociable).

La vérification réelle d'existence dans Vault relève de `homelab-vault-access` en lecture de
présence ; hors de cet environnement (parsing statique, SG-4), le sensor contrôle la **forme**
des références et signale celles qui ne portent pas de chemin exploitable. Le signal porte le
chemin de référence (jamais la valeur).

Exécution seule : `python3 homelab/scripts/sensors/vault_secret_exists.py --root <projet> [--path <fichier>...]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import OK, Result  # noqa: E402
from sensorlib.context import Ctx, VAULT_REF, no_scope, res  # noqa: E402

ID = "vault-secret-exists"

# Chemin Vault exploitable : vault:kv/<stack>/<clé> — au moins deux segments après `vault:`.
_WELL_FORMED = re.compile(r"^vault:[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+$", re.I)


def run(ctx: Ctx) -> list[Result]:
    sid, results = ID, []
    seen_any = False
    for rel in ctx.targets:
        refs = VAULT_REF.findall(ctx.text(rel))
        if not refs:
            continue
        seen_any = True
        gaps: list[str] = []
        for ref in refs:
            # on ne restitue QUE le chemin de référence, jamais la valeur (invariant Homelab)
            if not _WELL_FORMED.match(ref):
                gaps.append(f"{rel} — référence Vault mal formée « {ref} » (chemin non exploitable)")
        results.append(res(sid, rel, gaps,
                           f"{len(refs)} référence(s) Vault bien formée(s) — existence à confirmer par homelab-vault-access (présence seule)",
                           "référence(s) Vault non exploitable(s)"))
    if not seen_any:
        return no_scope(sid, "aucune référence de secret Vault (vault:…) dans le périmètre")
    return results


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
