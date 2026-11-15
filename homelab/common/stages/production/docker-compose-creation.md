---
slug: docker-compose-creation
phase: production
execution: CONDITIONAL
condition: "Stack Docker (Swarm) — ignoré sous infra-terraform et branches autonomes. Produit en parallèle de terraform-configuration."
lead_agent: Spécialiste Docker
support_agents: []
mode: subagent
summary_confirmation: required
reviewer: null
review_class: none
human_gate: granular
produces: [livrable_compose]
consumes: [{artifact: parametres_requis_complets, required: true}, {artifact: mode_execution_applique, required: true}]
requires_stage: [autonomy-mode]
sensors: [yaml-validity, plaintext-secret]
scopes: [stack-update, new-stack, config-change, security-patch]
inputs: "Paramètres requis (collectés en Cadrage §2.4 — domaine / FQDN, auth) + documentation officielle + mode d'exécution appliqué"
outputs: "Fichier docker-compose optimisé Swarm, déposé dans `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/`"
---

# Création du docker-compose (Spécialiste Docker)

## Objectif

Produire le docker-compose optimisé Swarm, cohérent avec les **paramètres collectés en Cadrage (§2.4)** (domaine / FQDN, auth) et la documentation officielle. Ce stage s'exécute **en parallèle** de la configuration Terraform ([`terraform-configuration.md`](terraform-configuration.md)) : il ne dépend pas du `.tfvars`, et la cohérence `.tfvars` ↔ compose est réconciliée par l'Analyste QA en aval.

## Steps

### Step 1 — Déléguer au Spécialiste Docker (en parallèle du Terraform)

Le Tech Lead délègue au **Spécialiste Docker** par mention valide (mission + périmètre + critères).

- La délégation se fait **en parallèle** de celle au Spécialiste Terraform (deux sous-issues `--stage 1`). Verrou de concurrence par artefact : [`governance-security.md`](../../protocols/governance-security.md) § concurrence.
- La sous-issue Docker passe en `in_progress` dès que son travail démarre. Cycle : [`stage-protocol.md` § Cycle de statut des sous-issues & barrière de stage](../../protocols/stage-protocol.md#cycle-de-statut-des-sous-issues--barrière-de-stage).
- Le compose s'appuie sur les **paramètres collectés en Cadrage (§2.4)**, pas sur un `.tfvars` en amont.
- Le **relevé fin** (variables d'environnement supportées, convention de secrets `_FILE` ou non, volumes, port, healthcheck, versions) est établi par le Spécialiste Docker, **pas le Tech Lead**, à partir de la documentation officielle.

### Step 2 — Produire le livrable

Produire le fichier (skill `docker-composer`) :

1. Conserver les commentaires `#` des gabarits.
2. Vérifier la syntaxe YAML.
3. Déposer les fichiers dans le **répertoire de relecture** (voir ci-dessous).
4. Appliquer le **geste de fin de mission** [`producer-report.md`](../../protocols/producer-report.md) : joindre `docker-compose.yml` **et** le message A2A `retour` (`retour-docker-<stack>.yaml`).
5. Livrable produit et compte-rendu rendu : la sous-issue Docker passe en `in_review` (en attente de vérification QA). Cycle : [`stage-protocol.md` § Cycle de statut des sous-issues & barrière de stage](../../protocols/stage-protocol.md#cycle-de-statut-des-sous-issues--barrière-de-stage).

> **Autorité des règles techniques (A5/A6).** La skill `docker-composer` est la **source unique** de :
>
> - la règle des **services mutualisés** (ne jamais recréer Traefik / Redis-Valkey / PostgreSQL, réutiliser les instances existantes) ;
> - la **liste des réseaux Traefik** et le réseau par défaut, dans `SKILL.md` et [`references/network.md`](../../../../plugins/homelab-assistant/skills/docker-composer/references/network.md).
>
> Le workflow ne réénonce pas ces règles : il les référence et collecte les paramètres associés (`${traefik_network}`, `${valkey_enabled}`, `${database_service}`, voir [`required-parameters-collection.md`](../cadrage/required-parameters-collection.md)).

> **Répertoire de relecture.** Fichiers générés déposés uniquement dans `.a-valider/<id-tâche>/<stack>/` : [`review-directory.md`](../../protocols/review-directory.md).

## Sensors

Outputs: livrable compose lisible dans `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/` (et joint à l'issue). Gate humain granulaire **selon le mode d'exécution** ([`autonomy-mode`](autonomy-mode.md)) : gated → validation à ce stage ; autonome → regroupée au point de synchronisation.
Imports: `yaml-validity` (write), `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**). L'auteur en est **propriétaire** : ses verdicts, avec le `sha256` du compose, voyagent dans le YAML `retour` et sont repris par la QA ([`governance-security.md`](../../protocols/governance-security.md) § « Un contrôle, un propriétaire »).
Upstream targets: `parametres_requis_complets` (required), `mode_execution_applique` (required). Plus de dépendance `livrable_tfvars` : le compose est produit en parallèle du `.tfvars`.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (conventions compose Swarm, `_FILE`, placement healthcheck, réseau Traefik par défaut) tracés, remontés **en fin de workflow**, dans un message séparé ([`closure`](../validation/closure.md)); portée par défaut `stack` ; persistance des apprentissages **confirmés** via capture → confirmation humaine → contrôle de conflit.
