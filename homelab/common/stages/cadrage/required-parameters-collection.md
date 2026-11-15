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
produces: [parametres_requis_complets, auth_type_fige, mode_execution_choisi]
consumes: [{artifact: cadrage_confirme, required: true}, {artifact: fqdn_valide, required: false}, {artifact: auth_type_valide, required: false}, {artifact: database_service_valide, required: false}, {artifact: traefik_network_valide, required: false}]
requires_stage: [intake-framing]
sensors: [required-parameters]
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Cadrage confirmé + FQDN et auth validés au gate léger"
outputs: "parametres.json (paramètres requis complets et valides) + ${auth_type} figé (ou arbitré par l'humain)"
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
| Type d'authentification `${auth_type}` | Optionnel | `none`, `local`, `forwardauth`, `oidc` — validé au gate léger, repris sans redemander. |
| FQDN d'exposition `${fqdn}` | Déductible | Nom de domaine complet. Voir « Détail : FQDN » ci-dessous. |
| Paramètres OIDC `${oidc_params}` | Déductible (si `${auth_type}` = `oidc`) | IdP, nom du client, redirect URI, scopes — voir Step 3. Sans objet pour les autres types. |
| Stockage `${storage}` | Déductible | NFS du Homelab : serveur `truenas`, chemin `/mnt/datas/${ENVIRONMENT}/<services\|databases>/<stack_name>`. **Source unique** : [`template.yml`](../../../../plugins/homelab-assistant/skills/docker-composer/references/template.yml) (section `VOLUMES`) de la skill `docker-composer`. Ne jamais demander le serveur ni le chemin. |
| Secrets et variables Vault `${vault}` | Déductible | **Noms uniquement, jamais de valeur.** Voir « Détail : Vault » ci-dessous. |
| Réseau Traefik `${traefik_network}` | Déductible | **Source unique** : liste et réseau par défaut définis dans la skill `docker-composer` ([`references/network.md`](../../../../plugins/homelab-assistant/skills/docker-composer/references/network.md)). Validé au gate léger ([`network-preselection`](../initialisation/network-preselection.md)), repris sans redemander. |
| Activer Valkey `${valkey_enabled}` | Déductible | `true`, `false` — le Homelab possède **déjà** un Valkey/Redis mutualisé : ne jamais recréer ce service, s'y connecter (règle portée par la skill `docker-composer`). |
| Service base de données `${database_service}` | Optionnel | `postgres`, `mysql`, `mariadb`, `mongodb`, `none` — validé au gate léger ([`database-preselection`](../initialisation/database-preselection.md)), repris sans redemander. |

**Un seul message de confirmation**, au format [`output-format`](../../protocols/output-format.md) (une décision par bloc, valeur déduite comme **proposition par défaut**, toute valeur manquante connue incluse dès ce message) : le Tech Lead propose en bloc les valeurs par défaut déduites restantes (`${storage}`, `${valkey_enabled}`, `${vault}` et, si `oidc`, `${oidc_params}`) ainsi que le **mode d'exécution** de la Production (options et défaut : [`autonomy-mode`](../production/autonomy-mode.md)), et attend la confirmation ou correction de l'humain.

### Détail : FQDN `${fqdn}`

- **Défaut** : `<stack_name>.<domaine du homelab>`.
  - Domaine : source unique [`domaine-homelab.md`](../../../../plugins/homelab-assistant/skills/configuration-applications/references/domaine-homelab.md).
  - Préfixe déduit des FQDN des stacks existantes si une convention diffère.
- Valeur complète déjà présentée et validée au gate léger ([`intent-scope-approval`](../ideation/intent-scope-approval.md)) : la reprendre sans redemander.
- Si l'humain n'a modifié que le sous-domaine : recomposer `<sous-domaine>.<domaine du homelab>`.
- Écrit **en clair** dans le Terraform, jamais `${SNI}`.

### Détail : Vault `${vault}`

- **Deux listes**, `secrets` et `variables`, construites de la même façon selon les besoins de la stack.
  - Noms attendus par l'application : sa documentation fait foi, aucun nom imposé par le workflow.
  - Sources : éléments exigés par la documentation officielle, plus ceux induits par les paramètres retenus.
  - Exemples : secrets (client secret si `oidc`, mot de passe si base dédiée, compte admin initial) ; variables (URL publique `${fqdn}`, hôte / nom de la base, issuer OIDC).
- **Chaque entrée porte** :
  - son `besoin` (pourquoi elle existe) ;
  - sa `categorie` : `generable` (secret aléatoire créable par le Tech Lead), `variable` (non secrète, avec sa `valeur` validée) ou `humain` (valeur que seul l'humain détient ; défaut en cas de doute).
- La catégorie est montrée à l'humain et conditionne l'option d'écriture des clés Vault du gate final.
- **Emplacements** (layout : skill `homelab-vault-access`) : secrets → `services/<stack_name>` ; variables → `env_variables/<stack_name>`.
- Stack existante : lister les clés présentes (noms seuls). Liste vide si aucun besoin.

### Dépendances entre paramètres

Avant de poser le message, le Tech Lead identifie les paramètres qui **dépendent d'une valeur que seul l'humain détient** (nom d'un groupe ou d'un mapping Authentik, rôle admin, valeur de `main_group`…).

- Chacun est présenté **dans la même décision** que la valeur dont il dépend, avec la valeur demandée en toutes lettres (« à fournir : nom exact du mapping »).
- Il **n'est pas validé sans elle** (règle : [`conductor.md`](../../conductor.md), « Élément dépendant d'une valeur manquante »).
- Valeur non fournie : l'élément et ses dérivés (scope, variable Vault, action humaine) sont retirés ensemble plutôt que livrés incomplets.

La création des clés Vault proposées reste une action humaine (agent Vault dédié à créer plus tard) : le message le signale.

### Step 2 — Sélection automatique du type d'authentification

`${auth_type}` est **optionnel** (non bloquant). Lorsque la documentation officielle précise les types possibles, le Tech Lead **choisit automatiquement** — **le premier disponible ET gratuit l'emporte** :

1. **`oidc`** — OIDC / OAuth disponible et gratuit ;
2. **`forwardauth`** — auth locale désactivable, ou aucune auth ;
3. **`local`** — auth locale non désactivable.

**En cas de doute** → l'option est présentée à l'humain au gate léger (point 5 de [`intent-scope-approval`](../ideation/intent-scope-approval.md)). Le doute ne bascule **jamais** vers un choix implicite.

> **SAML / LDAP non supportés.** Ces deux types ne sont implémentés ni côté middlewares Traefik ni côté template Terraform, et sont exclus de la règle de sélection. Si une stack requiert SAML ou LDAP : **demander à l'humain**.

### Step 3 — Paramètres OIDC (si `${auth_type}` = `oidc`)

Le Tech Lead **déduit** les paramètres OIDC au lieu de les demander, puis les présente pour **une validation globale unique** (Keep / Modify / Redo) :

| Paramètre | Valeur déduite par défaut |
| --- | --- |
| IdP | **Authentik**, seul IdP OIDC du Homelab. Ne jamais demander l'IdP ni son URL d'émetteur : le client est créé par le Terraform (`oauth[]`). |
| Nom du client | `${stack_name}` |
| Redirect URI | Chemin de callback issu de la **documentation officielle** de l'application (ex. `/oauth2/callback`, `/authorization-code/callback`), préfixé par `https://${fqdn}` — dépend donc de `${fqdn}` (déduit au Step 1) |
| Scopes | Ceux requis par la documentation officielle ; à défaut `openid profile email` |

Règles :

- Si la documentation officielle ne permet pas de déterminer le chemin de callback ou les scopes → **demander à l'humain** pour cette valeur uniquement ; jamais d'invention.
- **Aucun secret** ([`governance-security.md`](../../protocols/governance-security.md) § « Aucun secret ») ; il relève de Vault (proposé dans `${vault}`, voir Step 1).
- La règle d'auto-sélection du Step 2 (`oidc → forwardauth → local`) est **inchangée** (SEC-1) : ce Step ne fait que renseigner les paramètres une fois `oidc` retenu.
- Mapping vers le Terraform : `oauth[]` et `allowed_redirect_uris[][]` (voir la skill `configuration-applications`, [`authentification.md`](../../../../plugins/homelab-assistant/skills/configuration-applications/references/authentification.md)).

### Step 4 — Écrire `parametres.json`

Après la confirmation de l'humain, écrire les valeurs retenues dans `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/parametres.json`. Format et règles : sensor [`required-parameters`](../../../sensors/sensors/required-parameters.md).

## Sensors

Outputs: `parametres.json` dans `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/` (artefact `parametres_requis_complets`) + `${auth_type}` figé. Frontière **Cadrage → Production** : voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: `required-parameters` (gate — **bloquant sur `new-stack` / `infra-terraform`**).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (paramètres par défaut par stack, réseau Traefik conventionnel) tracés, remontés **en fin de workflow**, dans un message séparé ([`closure`](../validation/closure.md)). La règle d'auto-sélection d'authentification est un **invariant** (non abaissable — SEC-1).
