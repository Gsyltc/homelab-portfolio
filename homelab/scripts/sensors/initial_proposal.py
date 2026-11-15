#!/usr/bin/env python3
"""Sensor `initial-proposal` — applique `homelab/sensors/sensors/initial-proposal.md`.

Vérifie que `preselection.json`, alimenté par les stages de pré-sélection d'Initialisation
(`deployment-target-preselection`, `auth-preselection`, `database-preselection`,
`network-preselection`), est complet avant la proposition initiale (`intent-scope-approval`).
Une section absente ou remplie par « non vérifié » / « à trancher » sans options est un écart.

Parsing **statique** (SG-4). Aucune valeur de secret n'est lue ni affichée.

Exécution seule : `python3 homelab/scripts/sensors/initial_proposal.py --root <projet> [--path <fichier>...]`
(advisory : code retour 0 ; `--strict` renvoie 1 en cas d'écart ou de ⛔, usage CI).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensorlib.common import UNAVAILABLE, Result  # noqa: E402
from sensorlib.context import Ctx, no_scope, res  # noqa: E402

ID = "initial-proposal"

NETWORK_SRC = (Path(__file__).resolve().parents[3] / "plugins" / "homelab-assistant" / "skills"
               / "docker-composer" / "references" / "network.md")


def traefik_networks() -> set[str] | None:
    """Réseaux Traefik de la skill docker-composer (source unique) ; None si illisible."""
    try:
        text = NETWORK_SRC.read_text(encoding="utf-8")
    except OSError:
        return None
    nets = set(re.findall(r"^-\s+([a-z0-9_]+)\s*:", text, re.M))
    return nets or None

SECTIONS = {"cibles", "auth", "database", "reseau"}
AUTH_TYPES = {"none", "local", "forwardauth", "oidc"}
DATABASES = {"postgres", "mysql", "mariadb", "mongodb", "none"}
TARGETS = {"docker-swarm", "proxmox"}

URL_RE = re.compile(r"^https?://\S+$")
PROXMOX_RE = re.compile(
    r"^https://(?:raw\.githubusercontent\.com/community-scripts/ProxmoxVE/main/ct/[a-z0-9._-]+\.sh"
    r"|community-scripts\.org/scripts/[a-z0-9._-]+)$")
UNRESOLVED_RE = re.compile(
    r"non\s+(?:v[ée]rifi[ée]|recherch[ée]|consult[ée])|[àa]\s+v[ée]rifier|inconnu|<[^>]*>|\bTODO\b|\bTBD\b", re.I)


def _str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _unknown(obj: dict, allowed: set[str], where: str, gaps: list[str]) -> None:
    for k in sorted(set(obj) - allowed):
        gaps.append(f"{where}{k} : clé inconnue (attendues : {', '.join(sorted(allowed))})")


def _walk(node, path: str, gaps: list[str]) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            _walk(v, f"{path}.{k}" if path else k, gaps)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk(v, f"{path}[{i}]", gaps)
    elif isinstance(node, str) and UNRESOLVED_RE.search(node):
        gaps.append(f"{path} : valeur non résolue (« non vérifié », gabarit ou TODO) — exécuter le stage")


def _check_cibles(c, gaps: list[str]) -> None:
    if not isinstance(c, dict):
        gaps.append("cibles : requis (deployment-target-preselection)")
        return
    if "actuelle" in c:  # stack existante
        _unknown(c, {"actuelle"}, "cibles.", gaps)
        if c["actuelle"] not in TARGETS:
            gaps.append(f"cibles.actuelle : valeurs {sorted(TARGETS)}")
        return
    _unknown(c, {"docker", "proxmox", "variantes_testees"}, "cibles.", gaps)
    for k in ("docker", "proxmox"):
        if k not in c:
            gaps.append(f"cibles.{k} : requis (objet si disponible, null sinon)")
    docker, proxmox = c.get("docker"), c.get("proxmox")
    if docker is not None:
        if not (isinstance(docker, dict) and _str(docker.get("image"))):
            gaps.append("cibles.docker.image : requis si Docker disponible")
        else:
            _unknown(docker, {"image"}, "cibles.docker.", gaps)
    if proxmox is not None:
        if not isinstance(proxmox, dict):
            gaps.append("cibles.proxmox : objet {script, source} attendu")
        else:
            _unknown(proxmox, {"script", "source"}, "cibles.proxmox.", gaps)
            if not (_str(proxmox.get("script")) and PROXMOX_RE.match(proxmox["script"])):
                gaps.append("cibles.proxmox.script : URL ct/<slug>.sh du dépôt community-scripts/ProxmoxVE attendue")
            if not (_str(proxmox.get("source")) and URL_RE.match(proxmox["source"])):
                gaps.append("cibles.proxmox.source : URL de la ligne `# Source:` du script requise (écarte les homonymes)")
    variantes = c.get("variantes_testees")
    if not (isinstance(variantes, list) and variantes and all(_str(v) for v in variantes)):
        gaps.append("cibles.variantes_testees : liste non vide requise (méthode de recherche Helper-Scripts)")
    if "docker" in c and "proxmox" in c and docker is None and proxmox is None:
        gaps.append("cibles : aucune cible disponible — le signaler à l'humain, ne pas poster une proposition vide")


def _check_choice(name: str, sec, allowed: set[str], stage: str, gaps: list[str]) -> None:
    if not isinstance(sec, dict):
        gaps.append(f"{name} : requis ({stage})")
        return
    if "sans_objet" in sec:
        _unknown(sec, {"sans_objet"}, f"{name}.", gaps)
        if not _str(sec["sans_objet"]):
            gaps.append(f"{name}.sans_objet : raison requise")
        return
    _unknown(sec, {"recommande", "options", "justification", "source"}, f"{name}.", gaps)
    has_rec, has_opt = "recommande" in sec, "options" in sec
    if has_rec == has_opt:
        gaps.append(f"{name} : `recommande` OU `options` requis (un seul)")
    elif has_rec and sec["recommande"] not in allowed:
        gaps.append(f"{name}.recommande : valeurs {sorted(allowed)}")
    elif has_opt:
        opts = sec["options"]
        if not (isinstance(opts, list) and len(opts) >= 2 and all(o in allowed for o in opts)):
            gaps.append(f"{name}.options : au moins 2 valeurs parmi {sorted(allowed)}")
    if not _str(sec.get("justification")):
        gaps.append(f"{name}.justification : requise")
    if not _str(sec.get("source")):
        gaps.append(f"{name}.source : requise (lien vers la doc, ou configuration actuelle)")


def check(p: dict) -> list[str]:
    gaps: list[str] = []
    _unknown(p, SECTIONS, "", gaps)
    _walk(p, "", gaps)
    _check_cibles(p.get("cibles"), gaps)
    _check_choice("auth", p.get("auth"), AUTH_TYPES, "auth-preselection", gaps)
    _check_choice("database", p.get("database"), DATABASES, "database-preselection", gaps)
    nets = traefik_networks()
    if nets is None:
        gaps.append(f"reseau : liste des réseaux Traefik illisible ({NETWORK_SRC.name})")
    else:
        _check_choice("reseau", p.get("reseau"), nets, "network-preselection", gaps)
    return gaps


def run(ctx: Ctx) -> list[Result]:
    results: list[Result] = []
    for rel in ctx.targets:
        try:
            p = json.loads(ctx.text(rel))
        except json.JSONDecodeError as exc:
            results.append(Result(ID, rel, UNAVAILABLE, f"indisponible : JSON invalide (ligne {exc.lineno})"))
            continue
        if not isinstance(p, dict):
            results.append(Result(ID, rel, UNAVAILABLE, "indisponible : objet JSON attendu"))
            continue
        results.append(res(ID, rel, check(p), "pré-sélections complètes", "pré-sélections manquantes ou non résolues"))
    return results or no_scope(ID, "aucun preselection.json sous .a-valider/<id-tâche>/<stack>/")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
