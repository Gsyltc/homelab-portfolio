---
id: initial-proposal
kind: deterministic
command: "python3 homelab/scripts/sensor.py fire initial-proposal"
default_severity: advisory
severity_overrides:
  - scopes: [new-stack, infra-terraform]
    severity: blocking
description: "Vérifie que preselection.json (stages de pré-sélection d'Initialisation) est complet avant la proposition initiale."
category: governance
fire_on: gate
matches: "**/.a-valider/*/*/preselection.json"
origine: HOM-313
---

# Sensor `initial-proposal` — pré-sélections complètes avant la proposition initiale

Check déterministe exécuté **avant de poster la proposition initiale** ([`intent-scope-approval`](../../common/stages/ideation/intent-scope-approval.md)) et au gate `phase0-phase1`, sur `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/preselection.json`. Chaque stage de pré-sélection écrit sa section. **Bloquant** sur `new-stack` / `infra-terraform`, advisory ailleurs.

## Format du fichier

```json
{
  "cibles": {
    "docker": {"image": "syncin/server"},
    "proxmox": {"script": "https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/sync-in.sh",
                "source": "https://github.com/Sync-in/server"},
    "variantes_testees": ["sync-in", "syncin"]
  },
  "auth": {"recommande": "oidc", "justification": "SSO OIDC supporté", "source": "<lien doc>"},
  "database": {"recommande": "mariadb", "justification": "moteur exigé par la doc", "source": "<lien doc>"},
  "kestra": {"statut": "accessible"}
}
```

## Contrat de vérification (`checks`)

| Section | Écrite par | Règle |
| --- | --- | --- |
| `cibles` | `deployment-target-preselection` | Stack existante : `{actuelle: docker-swarm\|proxmox}`. Sinon : `docker` (`{image}` ou `null`), `proxmox` (`{script, source}` ou `null`, `script` = URL `ct/<slug>.sh` du dépôt `community-scripts/ProxmoxVE`), `variantes_testees` non vide. Au moins une cible disponible. |
| `auth` | `auth-preselection` | `recommande` (un type) **ou** `options` (≥ 2 types), + `justification` et `source`. Ou `{sans_objet: raison}`. |
| `database` | `database-preselection` | Même forme, valeurs `postgres`, `mysql`, `mariadb`, `mongodb`, `none`. Ou `{sans_objet: raison}`. |
| `kestra` | `deployment-prereqs-precheck` | `statut` : `accessible` ou `injoignable`. |

Contrôles transverses :
- Clé inconnue → écart.
- Valeur non résolue (« non vérifié », « non recherché », « à vérifier », « inconnu », `<…>`, `TODO`, `TBD`) → écart : le stage doit être exécuté, pas contourné.

## Sortie (piste d'audit)

```
Sensor initial-proposal — <fichier>   (source : homelab/sensors/sensors/initial-proposal.md @ <commit>)
- verdict : ✅ pré-sélections complètes | ⚠️ <section> : <règle non respectée> | ⛔ indisponible : <motif>
```

## Garde-fou

Le sensor contrôle la complétude et la forme, pas la pertinence des recommandations. Il ne remplace pas le gate léger ni la validation humaine (SG-3). Parsing statique uniquement (SG-4).
