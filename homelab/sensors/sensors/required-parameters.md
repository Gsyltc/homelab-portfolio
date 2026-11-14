---
id: required-parameters
kind: deterministic
command: "python3 homelab/scripts/sensor.py fire required-parameters"
default_severity: advisory
severity_overrides:
  - scopes: [new-stack, infra-terraform]
    severity: blocking
description: "Vérifie que parametres.json (stage required-parameters-collection) contient tous les paramètres requis, avec des valeurs valides."
category: governance
fire_on: gate
matches: "**/.a-valider/*/*/parametres.json"
origine: HOM-313
---

# Sensor `required-parameters` — paramètres requis complets et valides

Check déterministe exécuté **au gate `phase2-phase3`** (Cadrage → Production) sur le fichier `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/parametres.json`, écrit par le Tech Lead au stage [`required-parameters-collection`](../../common/stages/cadrage/required-parameters-collection.md). **Bloquant** sur `new-stack` / `infra-terraform`, advisory ailleurs.

## Format du fichier

```json
{
  "stack_name": "sync-in",
  "cible": "swarm",
  "auth_type": "oidc",
  "fqdn": "sync.jeedom-gaston.ovh",
  "oidc": {
    "idp": "authentik",
    "client_name": "sync-in",
    "redirect_uri": "https://sync.jeedom-gaston.ovh/<callback de la doc officielle>",
    "scopes": ["openid", "profile", "email"]
  },
  "storage": {
    "server": "truenas",
    "paths": ["/mnt/datas/${ENVIRONMENT}/services/sync-in"]
  },
  "traefik_network": "traefik_frontend",
  "valkey_enabled": false,
  "database_service": "mariadb",
  "vault": {
    "secrets": [
      {"nom": "<nom attendu par l'application>", "besoin": "clé de chiffrement exigée par la doc (section …)"},
      {"nom": "<nom attendu par l'application>", "besoin": "client secret OIDC (auth_type = oidc)"}
    ],
    "variables": [
      {"nom": "<nom attendu par l'application>", "besoin": "URL publique (fqdn) exigée par la doc"},
      {"nom": "<nom attendu par l'application>", "besoin": "hôte de la base (database_service = mariadb)"}
    ]
  },
  "mode_execution": "gated"
}
```

## Contrat de vérification (`checks`)

| Clé | Règle |
| --- | --- |
| `stack_name` | Requis. Minuscules, chiffres, tirets. |
| `cible` | Requis : `swarm` ou `proxmox` (cible choisie au gate léger `intent-scope-approval`). |
| `auth_type` | Optionnel : `none`, `local`, `forwardauth`, `oidc`. |
| `fqdn` | Requis. Nom de domaine complet, sous le domaine de [`domaine-homelab.md`](../../../plugins/homelab-assistant/skills/configuration-applications/references/domaine-homelab.md). |
| `oidc` | Requis si `auth_type` = `oidc`, absent sinon. `idp` = `authentik` ; `client_name` non vide ; `redirect_uri` commence par `https://<fqdn>/` ; `scopes` contient `openid`. |
| `storage` | Requis si `cible` = `swarm`. `server` = serveur NFS de [`template.yml`](../../../plugins/homelab-assistant/skills/docker-composer/references/template.yml) ; chaque chemin = `/mnt/datas/${ENVIRONMENT}/<services\|databases>/<stack_name>`. |
| `traefik_network` | Requis si `cible` = `swarm`. Réseau listé dans [`network.md`](../../../plugins/homelab-assistant/skills/docker-composer/references/network.md). |
| `valkey_enabled` | Booléen, requis si `cible` = `swarm`. |
| `database_service` | Optionnel : `postgres`, `mysql`, `mariadb`, `mongodb`, `none`. |
| `vault` | Requis : `secrets` et `variables`, listes (éventuellement vides) d'objets `{nom, besoin}`. `nom` : libre, celui attendu par l'application (lettre ou `_` en tête, puis lettres, chiffres, `_`, `.`, `-`, 128 car. max), unique dans sa liste. `besoin` : non vide. Une valeur n'y figure jamais. |
| `mode_execution` | Requis : `gated` (défaut) ou `autonome` (voir [`autonomy-mode`](../../common/stages/production/autonomy-mode.md)). |

Contrôles transverses :
- Clé inconnue → écart (faute de frappe, paramètre hors contrat).
- Valeur non résolue (`<…>`, `${…}` autre que `${ENVIRONMENT}`, `TODO`, `TBD`, `xxx`) → écart.
- Clé ressemblant à un secret (`password`, `secret`, `token`, `api_key`, `private_key`) → écart, signalée par son nom seul. **La valeur n'est jamais lue ni affichée.**

Les valeurs de référence sont lues dans leurs sources uniques. Une source illisible donne `⛔`, jamais `✅` (SG-2).

## Sortie (piste d'audit)

```
Sensor required-parameters — <fichier>   (source : homelab/sensors/sensors/required-parameters.md @ <commit>)
- verdict : ✅ paramètres requis complets et valides | ⚠️ <clé> : <règle non respectée> | ⛔ indisponible : <motif>
```

## Garde-fou

Le sensor contrôle la forme et la complétude, pas la pertinence des choix. Il ne remplace pas la validation humaine granulaire ni le contrôle QA (SG-3). Parsing statique uniquement (SG-4).
