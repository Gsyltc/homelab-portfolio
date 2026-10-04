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
consumes: [{artifact: parametres_requis_complets, required: true}, {artifact: walking_skeleton_valide, required: true}]
requires_stage: [autonomy-mode]
sensors: [yaml-validity, plaintext-secret]
scopes: [stack-update, new-stack, config-change, security-patch]
inputs: "Paramètres requis (collectés en Cadrage §2.4 — domaine / FQDN, auth) + documentation officielle + walking skeleton validé"
outputs: "Fichier docker-compose optimisé Swarm, téléchargeable"
---

# Création du docker-compose (Spécialiste Docker)

## Objectif

Produire le docker-compose optimisé Swarm, cohérent avec les **paramètres collectés en Cadrage (§2.4)** (domaine / FQDN, auth) et la documentation officielle. Ce stage s'exécute **en parallèle** de la configuration Terraform ([`terraform-configuration.md`](terraform-configuration.md)) : il ne dépend pas du `.tfvars`, et la cohérence `.tfvars` ↔ compose est réconciliée par l'Analyste QA en aval.

## Steps

### Step 1 — Déléguer au Spécialiste Docker (en parallèle du Terraform)

Le Tech Lead délègue au **Spécialiste Docker** par mention valide (mission + périmètre + critères), **en parallèle** de la délégation au Spécialiste Terraform (deux sous-issues `--stage 1` ; verrou de concurrence par artefact, cf. [`governance-security.md`](../../protocols/governance-security.md) § concurrence). **La sous-issue Docker passe en `in_progress`** dès que son travail démarre (cycle de statut des sous-issues : [`stage-protocol.md` § Cycle de statut des sous-issues & barrière de stage](../../protocols/stage-protocol.md#cycle-de-statut-des-sous-issues--barrière-de-stage)). Le compose s'appuie sur les **paramètres collectés en Cadrage (§2.4)**, pas sur un `.tfvars` en amont. C'est le Spécialiste Docker — **pas le Tech Lead** — qui exploite la documentation officielle pour établir le **relevé fin** (variables d'environnement supportées, convention de secrets `_FILE` ou non, volumes, port, healthcheck, versions).

### Step 2 — Produire le livrable

Produire le fichier (skill `docker-composer`), conserver les commentaires `#` des gabarits, vérifier la syntaxe YAML, puis appliquer le **geste de fin de mission** [`producer-report.md`](../../protocols/producer-report.md) : ne joindre que le livrable `docker-compose.yml` (aucun fichier de rapport), corps minimal (mention valide du Tech Lead + une ligne de statut), zéro prose. Sans mention valide → compte-rendu réputé non rendu, flux arrêté. **Une fois le livrable produit et le compte-rendu rendu, la sous-issue Docker passe en `in_review`** (livrable produit, en attente de vérification QA ; cf. [`stage-protocol.md` § Cycle de statut des sous-issues & barrière de stage](../../protocols/stage-protocol.md#cycle-de-statut-des-sous-issues--barrière-de-stage)).

> **Autorité des règles techniques (A5/A6).** La règle des **services mutualisés** (ne jamais recréer Traefik / Redis-Valkey / PostgreSQL — réutiliser les instances existantes du Homelab) et la **liste des réseaux Traefik + réseau par défaut** sont portées par la **skill `docker-composer`** (`SKILL.md` et [`references/network.md`](../../../../plugins/homelab-assistant/skills/docker-composer/references/network.md)), qui en est la **source unique**. Le workflow ne réénonce pas ces règles : il les **référence** et se limite à collecter les paramètres associés (`${traefik_network}`, `${valkey_enabled}`, `${database_service}` — voir [`required-parameters-collection.md`](../cadrage/required-parameters-collection.md)).

## Sensors

Outputs: livrable compose téléchargeable. Gate humain granulaire (via `quality-assurance` puis `central-quality-control` puis Validation).
Imports: `yaml-validity` (write), `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**).
Upstream targets: `parametres_requis_complets` (required), `walking_skeleton_valide` (required). Plus de dépendance `livrable_tfvars` : le compose est produit en parallèle du `.tfvars`.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (conventions compose Swarm, `_FILE`, placement healthcheck, réseau Traefik par défaut) tracés, remontés au **gate humain granulaire** ; portée par défaut `stack` ; persistance des apprentissages **confirmés** via capture → confirmation humaine → contrôle de conflit.
