---
slug: required-parameters-collection
phase: cadrage
execution: ALWAYS
condition: "Always executes pour une stack — via le workflow Homelab (triptyque homelab/common/)"
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
| Type d'authentification `${auth_type}` | Optionnel | `none`, `local`, `forwardauth`, `oidc` |
| FQDN d'exposition `${fqdn}` | Déductible | Texte (nom de domaine complet). **Défaut** : `<stack_name>.<domaine du homelab>` — domaine : **source unique** [`domaine-homelab.md`](../../../../plugins/homelab-assistant/skills/configuration-applications/references/domaine-homelab.md) ; préfixe déduit des FQDN des stacks existantes si une convention diffère. Le défaut est **proposé et confirmé en un seul message** (jamais une question ouverte), avec les autres défauts déductibles. Écrit **en clair** dans le Terraform, jamais `${SNI}`. |
| Paramètres OIDC `${oidc_params}` | Déductible (si `${auth_type}` = `oidc`) | IdP, nom du client, redirect URI, scopes — voir Step 3. Sans objet pour les autres types. |
| Réseau Traefik `${traefik_network}` | Déductible | **Source unique** : liste et réseau par défaut définis dans la skill `docker-composer` ([`references/network.md`](../../../../plugins/homelab-assistant/skills/docker-composer/references/network.md)) ; défaut **à confirmer par l'humain**. |
| Activer Valkey `${valkey_enabled}` | Déductible | `true`, `false` — le Homelab possède **déjà** un Valkey/Redis mutualisé : ne jamais recréer ce service, s'y connecter (règle portée par la skill `docker-composer`). |
| Service base de données `${database_service}` | Optionnel | `postgres`, `mysql`, `mariadb`, `mongodb`, `none` — PostgreSQL mutualisé **déjà** présent : ne jamais recréer `postgres`, s'y connecter (règle portée par la skill `docker-composer`). |

**Un seul message de confirmation** : le Tech Lead propose en bloc les valeurs par défaut déduites (`${fqdn}`, `${traefik_network}`, `${valkey_enabled}`) et attend la confirmation ou correction de l'humain.

Demander aussi si la stack nécessite une création / modification de secrets ou variables dans **HashiCorp Vault** (le signaler à l'humain ; agent Vault dédié à créer plus tard).

### Step 2 — Sélection automatique du type d'authentification

`${auth_type}` est **optionnel** (non bloquant). Lorsque la documentation officielle précise les types possibles, le Tech Lead **choisit automatiquement** — **le premier disponible ET gratuit l'emporte** :

1. **`oidc`** — OIDC / OAuth disponible et gratuit ;
2. **`forwardauth`** — auth locale désactivable, ou aucune auth ;
3. **`local`** — auth locale non désactivable.

**En cas de doute → demander à l'humain** et attendre. Le doute ne bascule **jamais** vers un choix implicite.

> **SAML / LDAP non encore supportés.** Ces deux types étaient historiquement listés dans l'ordre de sélection mais ne sont pas implémentés côté middlewares Traefik ni côté template Terraform. Ils ont été **retirés** de la règle de sélection (voir [ADR-0024](../../../../decisions/0024-retrait-temporaire-saml-ldap-authentification.md)). Si une stack requiert SAML ou LDAP → **demander à l'humain** ; leur ré-intégration fera l'objet des actions tracées dans l'ADR-0024.

### Step 3 — Paramètres OIDC (si `${auth_type}` = `oidc`)

Le Tech Lead **déduit** les paramètres OIDC au lieu de les demander, puis les présente pour **une validation globale unique** (Keep / Modify / Redo) :

| Paramètre | Valeur déduite par défaut |
| --- | --- |
| IdP | **Authentik** (IdP du Homelab) |
| Nom du client | `${stack_name}` |
| Redirect URI | Chemin de callback issu de la **documentation officielle** de l'application (ex. `/oauth2/callback`, `/authorization-code/callback`), préfixé par `https://${fqdn}` — dépend donc de `${fqdn}` (déduit au Step 1) |
| Scopes | Ceux requis par la documentation officielle ; à défaut `openid profile email` |

Règles :

- Si la documentation officielle ne permet pas de déterminer le chemin de callback ou les scopes → **demander à l'humain** pour cette valeur uniquement ; jamais d'invention.
- **Aucun secret** (client secret, jetons) dans les livrables ni les commentaires ; le secret relève de Vault (signalé à l'humain, voir Step 1).
- La règle d'auto-sélection du Step 2 (`oidc → forwardauth → local`) est **inchangée** (SEC-1) : ce Step ne fait que renseigner les paramètres une fois `oidc` retenu.
- Mapping vers le Terraform : `oauth[]` et `allowed_redirect_uris[][]` (voir la skill `configuration-applications`, [`authentification.md`](../../../../plugins/homelab-assistant/skills/configuration-applications/references/authentification.md)).

## Sensors

Outputs: paramètres requis complets (dont `${fqdn}` et, si `oidc`, `${oidc_params}`) + `${auth_type}` figé. Frontière **Cadrage → Production** : gate `artefacts-presents` + `liaison-tracabilite` (tous les paramètres §requis reliés à la demande) — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (paramètres par défaut par stack, réseau Traefik conventionnel) tracés, remontés au gate granulaire. La règle d'auto-sélection d'authentification est un **invariant** (non abaissable — SEC-1).
