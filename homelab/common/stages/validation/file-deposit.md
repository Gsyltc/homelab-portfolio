---
slug: file-deposit
phase: validation
execution: CONDITIONAL
condition: "Après validation humaine explicite, sur confirmation des chemins — N/A pour branches n8n / HA"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [depot_fichiers_confirme]
consumes: [{artifact: validation_humaine_explicite, required: true}, {artifact: prerequis_deploiement_verifies, required: true}]
requires_stage: [human-granular-validation]
sensors: [vault-secret-exists]
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Configuration validée + prérequis §répertoire vérifiés"
outputs: "Fichiers déposés dans les répertoires de travail, vérifiés"
---

# Dépôt des fichiers dans les répertoires de travail (sur confirmation)

## Objectif

Déposer les livrables validés aux emplacements conventionnels, sur confirmation explicite.

## Steps

### Step 1 — Proposer les chemins et attendre confirmation

> Prérequis : la variable `[répertoire de travail]` a été vérifiée ([`deployment-prereqs-check.md`](deployment-prereqs-check.md)).

Le Tech Lead **propose** les chemins de dépôt en les affichant, et **attend la confirmation explicite** de l'humain avant tout dépôt :

- docker-compose : `/[répertoire de travail]/docker/stacks/[domaine]/[nom-stack].yml` (domaine = valeur `domain` du `config.tfvars` ; convention `<stack>.yml`).
- Terraform : `[répertoire de travail]/terraform/[type]/[nom-de-la-stack]/config.tfvars` (type = `swarm` si Docker Swarm, `service` si Proxmox ; créer le répertoire s'il n'existe pas).

### Step 2 — Vérifier après dépôt

Après dépôt, vérifier les fichiers copiés (contenu conforme, parse YAML pour le compose).

## Sensors

Outputs: dépôt confirmé + fichiers vérifiés. Action à impact → validation humaine explicite requise (invariant).
Imports: `vault-secret-exists` (gate — existence seule, **jamais** la valeur).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (conventions de chemins de dépôt) tracés, remontés au gate explicite.
