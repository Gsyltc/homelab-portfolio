#!/usr/bin/env python3
"""Sensor `required-parameters` — applique `homelab/sensors/sensors/required-parameters.md`.

Vérifie que le fichier `parametres.json` produit par le stage `required-parameters-collection`
contient tous les paramètres requis et que chaque valeur est valide. Les valeurs de référence
(domaine du Homelab, serveur NFS, réseaux Traefik) sont lues dans leurs sources uniques du dépôt.

Parsing **statique** (SG-4). Aucune valeur de secret n'est lue ni affichée : une clé ressemblant
à un secret est signalée par son nom seul.

Exécution seule : `python3 homelab/scripts/sensors/required_parameters.py --root <projet> [--path <fichier>...]`
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

ID = "required-parameters"

REPO = Path(__file__).resolve().parents[3]
SKILLS = REPO / "plugins" / "homelab-assistant" / "skills"
DOMAIN_SRC = SKILLS / "configuration-applications" / "references" / "domaine-homelab.md"
NETWORK_SRC = SKILLS / "docker-composer" / "references" / "network.md"
NFS_SRC = SKILLS / "docker-composer" / "references" / "template.yml"

KEYS = {"stack_name", "cible", "auth_type", "fqdn", "oidc", "storage", "traefik_network",
        "valkey_enabled", "database_service", "vault_secrets_required"}
OIDC_KEYS = {"idp", "client_name", "redirect_uri", "scopes"}
STORAGE_KEYS = {"server", "paths"}
CIBLES = {"swarm", "proxmox"}
AUTH_TYPES = {"none", "local", "forwardauth", "oidc"}
DATABASES = {"postgres", "mysql", "mariadb", "mongodb", "none"}

KNOWN_KEYS = KEYS | OIDC_KEYS | STORAGE_KEYS

STACK_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HOST_RE = re.compile(r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$")
SECRET_KEY_RE = re.compile(r"(?:password|passwd|secret|token|api[_-]?key|private[_-]?key)", re.I)
PLACEHOLDER_RE = re.compile(r"<[^>]*>|\$\{(?!ENVIRONMENT\})[^}]*\}|\bTODO\b|\bxxx+\b|\bTBD\b", re.I)


# --------------------------------------------------------------------------- #
# Sources uniques (None = source illisible => ⛔, jamais un vert)
# --------------------------------------------------------------------------- #


def homelab_domain() -> str | None:
    try:
        m = re.search(r"\|\s*`homelab_domain`\s*\|\s*`([^`]+)`", DOMAIN_SRC.read_text(encoding="utf-8"))
    except OSError:
        return None
    return m.group(1).strip().lower() if m else None


def traefik_networks() -> set[str] | None:
    try:
        text = NETWORK_SRC.read_text(encoding="utf-8")
    except OSError:
        return None
    nets = set(re.findall(r"^-\s+([a-z0-9_]+)\s*:", text, re.M))
    return nets or None


def nfs_server() -> str | None:
    try:
        m = re.search(r"addr=([A-Za-z0-9_.-]+)", NFS_SRC.read_text(encoding="utf-8"))
    except OSError:
        return None
    return m.group(1) if m else None


# --------------------------------------------------------------------------- #
# Contrôles
# --------------------------------------------------------------------------- #


def _walk(node, path: str, gaps: list[str]) -> None:
    """Clés de secret (nom seul, jamais la valeur) et valeurs non résolues."""
    if isinstance(node, dict):
        for k, v in node.items():
            sub = f"{path}.{k}" if path else k
            if k not in KNOWN_KEYS and SECRET_KEY_RE.search(k):
                gaps.append(f"{sub} : clé de secret interdite (les secrets relèvent de Vault ; valeur non affichée)")
                continue
            _walk(v, sub, gaps)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk(v, f"{path}[{i}]", gaps)
    elif isinstance(node, str) and PLACEHOLDER_RE.search(node):
        gaps.append(f"{path} : valeur non résolue (gabarit ou espace réservé)")


def _unknown(obj: dict, allowed: set[str], where: str, gaps: list[str]) -> None:
    for k in sorted(set(obj) - allowed):
        gaps.append(f"{where}{k} : clé inconnue (attendues : {', '.join(sorted(allowed))})")


def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def check(params: dict) -> tuple[list[str], list[str]]:
    """Retourne (écarts, sources indisponibles)."""
    gaps: list[str] = []
    missing_src: list[str] = []
    _unknown(params, KEYS, "", gaps)
    _walk(params, "", gaps)

    stack = params.get("stack_name")
    if not _nonempty_str(stack):
        gaps.append("stack_name : requis")
    elif not STACK_RE.match(stack):
        gaps.append("stack_name : minuscules, chiffres et tirets uniquement")

    cible = params.get("cible")
    if cible not in CIBLES:
        gaps.append(f"cible : requis, valeurs {sorted(CIBLES)} (issu de swarm-proxmox-arbitration)")

    auth = params.get("auth_type")
    if auth is not None and auth not in AUTH_TYPES:
        gaps.append(f"auth_type : valeurs {sorted(AUTH_TYPES)}")

    fqdn = params.get("fqdn")
    if not _nonempty_str(fqdn):
        gaps.append("fqdn : requis (déduit : <stack_name>.<domaine du homelab>)")
    elif not HOST_RE.match(fqdn):
        gaps.append("fqdn : nom de domaine complet invalide")
    else:
        domain = homelab_domain()
        if domain is None:
            missing_src.append(f"domaine du homelab illisible ({DOMAIN_SRC.name})")
        elif not fqdn.endswith("." + domain):
            gaps.append(f"fqdn : hors du domaine du homelab ({domain})")

    oidc = params.get("oidc")
    if auth == "oidc":
        if not isinstance(oidc, dict):
            gaps.append("oidc : requis si auth_type = oidc")
        else:
            _unknown(oidc, OIDC_KEYS, "oidc.", gaps)
            if oidc.get("idp") != "authentik":
                gaps.append("oidc.idp : doit valoir « authentik » (seul IdP OIDC du Homelab)")
            if not _nonempty_str(oidc.get("client_name")):
                gaps.append("oidc.client_name : requis")
            uri = oidc.get("redirect_uri")
            if not _nonempty_str(uri):
                gaps.append("oidc.redirect_uri : requis (chemin de callback de la documentation officielle)")
            elif _nonempty_str(fqdn) and not uri.startswith(f"https://{fqdn}/"):
                gaps.append("oidc.redirect_uri : doit commencer par https://<fqdn>/")
            scopes = oidc.get("scopes")
            if not (isinstance(scopes, list) and scopes and all(_nonempty_str(s) for s in scopes)):
                gaps.append("oidc.scopes : liste non vide requise")
            elif "openid" not in scopes:
                gaps.append("oidc.scopes : « openid » requis")
    elif oidc is not None:
        gaps.append("oidc : sans objet si auth_type ≠ oidc")

    if cible == "swarm":
        _check_swarm(params, stack, gaps, missing_src)

    db = params.get("database_service")
    if db is not None and db not in DATABASES:
        gaps.append(f"database_service : valeurs {sorted(DATABASES)}")

    if not isinstance(params.get("vault_secrets_required"), bool):
        gaps.append("vault_secrets_required : booléen requis (réponse à la question Vault du Step 1)")
    return gaps, missing_src


def _check_swarm(params: dict, stack, gaps: list[str], missing_src: list[str]) -> None:
    storage = params.get("storage")
    if not isinstance(storage, dict):
        gaps.append("storage : requis sur Docker Swarm (NFS du Homelab)")
    else:
        _unknown(storage, STORAGE_KEYS, "storage.", gaps)
        server = nfs_server()
        if server is None:
            missing_src.append(f"serveur NFS illisible ({NFS_SRC.name})")
        elif storage.get("server") != server:
            gaps.append(f"storage.server : doit valoir « {server} » (NFS du Homelab)")
        paths = storage.get("paths")
        if not (isinstance(paths, list) and paths):
            gaps.append("storage.paths : liste non vide requise")
        else:
            name = re.escape(stack) if _nonempty_str(stack) else r"[^/]+"
            path_re = re.compile(rf"^/mnt/datas/(?:\$\{{ENVIRONMENT\}}|[a-z]+)/(?:services|databases)/{name}$")
            for i, p in enumerate(paths):
                if not (isinstance(p, str) and path_re.match(p)):
                    gaps.append(f"storage.paths[{i}] : attendu /mnt/datas/${{ENVIRONMENT}}/<services|databases>/<stack_name>")

    net = params.get("traefik_network")
    nets = traefik_networks()
    if not _nonempty_str(net):
        gaps.append("traefik_network : requis sur Docker Swarm")
    elif nets is None:
        missing_src.append(f"liste des réseaux Traefik illisible ({NETWORK_SRC.name})")
    elif net not in nets:
        gaps.append(f"traefik_network : réseau inconnu (attendus : {', '.join(sorted(nets))})")

    if not isinstance(params.get("valkey_enabled"), bool):
        gaps.append("valkey_enabled : booléen requis sur Docker Swarm")


def run(ctx: Ctx) -> list[Result]:
    results: list[Result] = []
    for rel in ctx.targets:
        try:
            params = json.loads(ctx.text(rel))
        except json.JSONDecodeError as exc:
            results.append(Result(ID, rel, UNAVAILABLE, f"indisponible : JSON invalide (ligne {exc.lineno})"))
            continue
        if not isinstance(params, dict):
            results.append(Result(ID, rel, UNAVAILABLE, "indisponible : objet JSON attendu"))
            continue
        gaps, missing_src = check(params)
        if missing_src:
            results.append(Result(ID, rel, UNAVAILABLE, "indisponible : source de référence illisible",
                                  missing_src + gaps))
            continue
        results.append(res(ID, rel, gaps, "paramètres requis complets et valides", "paramètres manquants ou invalides"))
    return results or no_scope(ID, "aucun parametres.json sous .a-valider/<id-tâche>/<stack>/")


if __name__ == "__main__":
    from sensorlib.standalone import main

    sys.exit(main(ID))
