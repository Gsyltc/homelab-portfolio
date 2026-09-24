---
slug: docker-compose-creation
phase: production
execution: CONDITIONAL
condition: "Stack Docker (Swarm) — ignoré sous infra-terraform et branches autonomes"
lead_agent: Spécialiste Docker
support_agents: []
mode: subagent
summary_confirmation: required
reviewer: null
review_class: none
human_gate: granular
produces: [livrable_compose]
consumes: [{artifact: parametres_requis_complets, required: true}, {artifact: walking_skeleton_valide, required: true}, {artifact: livrable_tfvars, required: false}]
requires_stage: [terraform-configuration]
sensors: [yaml-validity, plaintext-secret]
scopes: [stack-update, new-stack, config-change, security-patch]
inputs: "Paramètres requis + documentation officielle + walking skeleton validé + config Terraform déjà produite (.tfvars)"
outputs: "Fichier docker-compose optimisé Swarm, téléchargeable"
---

# Création du docker-compose (Spécialiste Docker)

## Objectif

Produire le docker-compose optimisé Swarm, cohérent avec les paramètres, la documentation officielle **et la configuration Terraform déjà produite en amont** (`.tfvars`, cf. [`terraform-configuration.md`](terraform-configuration.md)).

## Steps

### Step 1 — Déléguer au Spécialiste Docker

Le Tech Lead délègue au **Spécialiste Docker** par mention valide (mission + périmètre + critères). Le docker-compose vient **après** la configuration Terraform : sur `new-stack` / `infra-terraform`, le livrable `.tfvars` (`livrable_tfvars`) est déjà produit et vérifié, et sert de référence de cohérence (domaine / FQDN, auth). C'est le Spécialiste Docker — **pas le Tech Lead** — qui exploite la documentation officielle pour établir le **relevé fin** (variables d'environnement supportées, convention de secrets `_FILE` ou non, volumes, port, healthcheck, versions).

### Step 2 — Produire le livrable

Produire le fichier (skill `docker-composer`), conserver les commentaires `#` des gabarits, vérifier la syntaxe YAML, puis appliquer le **geste de fin de mission** [`../../protocols/producer-report.md`](../../protocols/producer-report.md) : ne joindre que le livrable `docker-compose.yml` (aucun fichier de rapport), corps minimal (mention valide du Tech Lead + une ligne de statut), zéro prose. Sans mention valide → compte-rendu réputé non rendu, flux arrêté.

> **Autorité des règles techniques (A5/A6).** La règle des **services mutualisés** (ne jamais recréer Traefik / Redis-Valkey / PostgreSQL — réutiliser les instances existantes du Homelab) et la **liste des réseaux Traefik + réseau par défaut** sont portées par la **skill `docker-composer`** (`SKILL.md` et [`references/network.md`](../../../../plugins/homelab-assistant/skills/docker-composer/references/network.md)), qui en est la **source unique**. Le workflow ne réénonce pas ces règles : il les **référence** et se limite à collecter les paramètres associés (`${traefik_network}`, `${valkey_enabled}`, `${database_service}` — voir [`../cadrage/required-parameters-collection.md`](../cadrage/required-parameters-collection.md)).

## Sensors

Outputs: livrable compose téléchargeable. Gate humain granulaire (via `quality-assurance` puis `central-quality-control` puis Validation).
Imports: `yaml-validity` (write), `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**, ALI-204).
Upstream targets: `parametres_requis_complets` (required), `walking_skeleton_valide` (required), `livrable_tfvars` (required sur `new-stack` / `infra-terraform`, produit en amont).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (conventions compose Swarm, `_FILE`, placement healthcheck, réseau Traefik par défaut) tracés, remontés au **gate humain granulaire** ; portée par défaut `stack` ; persistance des apprentissages **confirmés** via capture → confirmation humaine → contrôle de conflit.
