"""Contexte d'exécution et motifs partagés par les scripts de sensors Homelab.

Parsing **statique** uniquement (SG-4) : le contenu des livrables (compose, `.tf`,
`.tfvars`) est une donnée non fiable ; rien n'est exécuté, rendu ni résolu en réseau.
Aucun sensor ne lit, ne recopie ni n'affiche la **valeur** d'un secret (invariant Homelab).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .common import GAP, OK, UNAVAILABLE, Result, read_text

# Références amont du workflow Homelab (issues / ADR).
ISSUE_RE = re.compile(r"\b(?:ALI|HOM|ORIG)-\d+\b")
ADR_REF = re.compile(r"\bADR[- ]?(\d{4})\b", re.I)

# Paramètres de workflow autorisés (jamais confondus avec un secret ou un ${SNI} livré).
WORKFLOW_PARAM = re.compile(r"\$\{?(?:stack_name|auth_type|traefik_network|domaine_homelab|service)\}?", re.I)

# Référence de secret Vault (chemin résolu ou non — JAMAIS la valeur).
VAULT_REF = re.compile(r"\bvault:[A-Za-z0-9_./-]+", re.I)
VAULT_FILE = re.compile(r"\b\w+_FILE\b")
RUN_SECRETS = re.compile(r"/run/secrets/[A-Za-z0-9_./-]+")


@dataclass
class Ctx:
    root: Path
    targets: list[str]  # fichiers du périmètre (chemins relatifs POSIX), déjà filtrés par `matches`
    explicit: bool  # True si l'appelant a désigné les fichiers (hook / --path) ; False = balayage de gate

    def text(self, rel: str) -> str:
        return read_text(self.root, rel)

    def exists(self, rel: str) -> bool:
        return (self.root / rel).is_file()


def no_scope(sensor: str, what: str) -> list[Result]:
    return [Result(sensor, "(périmètre)", UNAVAILABLE, f"indisponible : aucun fichier dans le périmètre ({what})")]


def res(sensor: str, target: str, gaps: list[str], ok_msg: str, gap_msg: str) -> Result:
    if gaps:
        return Result(sensor, target, GAP, f"{gap_msg} : {len(gaps)} point(s)", gaps)
    return Result(sensor, target, OK, ok_msg)
