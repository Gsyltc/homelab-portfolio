---
slug: required-parameters-collection
phase: cadrage
execution: ALWAYS
condition: "Always executes pour une stack — via homelab-stack-workflow"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: granular
produces: [parametres_requis_complets, auth_type_fige]
consumes: [{artifact: cadrage_confirme, required: true}, {artifact: auth_type_preselectionne, required: false}]
requires_stage: [intake-framing]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Cadrage confirmé + auth pré-sélectionné"
outputs: "Tous les paramètres requis renseignés + ${auth_type} figé (ou arbitré par l'humain)"
---

# Collecte des paramètres requis

## Objectif

Réunir tous les paramètres requis avant de générer quoi que ce soit.

## Steps

### Step 1 — Vérifier les paramètres requis

Le Tech Lead vérifie que tous les paramètres sont renseignés ; **il ne génère rien tant qu'un paramètre requis est manquant** :

| Paramètre | Requis | Valeurs |
| --- | --- | --- |
| Nom de la stack `${stack_name}` | Oui | Texte alphanumérique |
| Type d'authentification `${auth_type}` | Optionnel | `none`, `local`, `forwardauth`, `ldap`, `saml`, `oidc` |
| Réseau Traefik `${traefik_network}` | Déductible | Sinon `network.md` ; défaut `traefik_frontend` **à confirmer par l'humain** |
| Activer Valkey `${valkey_enabled}` | Déductible | `true`, `false` |
| Service base de données `${database_service}` | Optionnel | `postgres`, `mysql`, `mariadb`, `mongodb`, `none` |

Demander aussi si la stack nécessite une création / modification de secrets ou variables dans **HashiCorp Vault** (le signaler à l'humain ; agent Vault dédié à créer plus tard).

### Step 2 — Sélection automatique du type d'authentification

`${auth_type}` est **optionnel** (non bloquant). Lorsque la documentation officielle précise les types possibles, le Tech Lead **choisit automatiquement** — **le premier disponible ET gratuit l'emporte** :

1. **`oidc`** — OIDC / OAuth disponible et gratuit ;
2. **`saml`** — SAML disponible et gratuit ;
3. **`ldap`** — LDAP disponible et gratuit ;
4. **`forwardauth`** — auth locale désactivable, ou aucune auth ;
5. **`local`** — auth locale non désactivable.

**En cas de doute → demander à l'humain** et attendre. Le doute ne bascule **jamais** vers un choix implicite.

## Sensors

Outputs: paramètres requis complets + `${auth_type}` figé. Frontière **Cadrage → Production** : gate `artefacts-presents` + `liaison-tracabilite` (tous les paramètres §requis reliés à la demande) — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (paramètres par défaut par stack, réseau Traefik conventionnel) tracés, remontés au gate granulaire. La règle d'auto-sélection d'authentification est un **invariant** (non abaissable — SEC-1).
