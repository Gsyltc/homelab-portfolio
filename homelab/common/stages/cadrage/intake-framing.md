---
slug: intake-framing
phase: cadrage
execution: ALWAYS
condition: "Always executes (branches n8n / home-assistant court-circuitées)"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [cadrage_confirme]
consumes: [{artifact: intention_perimetre_approuves, required: true}]
requires_stage: [n8n-absolute-rule]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Intention + périmètre approuvés, scope confirmé"
outputs: "Cadrage confirmé + domaine identifié"
---

# Réception et cadrage

## Objectif

Cadrer la demande et identifier le domaine avant toute génération. La documentation officielle est déjà consignée (étape 3 de l'amorçage du [`conductor`](../../conductor.md)) : ne pas la relire.

## Steps

### Step 1 — Identifier le domaine

Stack Docker (Spécialiste Docker / Analyste QA), Home Assistant (Expert Home Assistant), Terraform (Spécialiste Terraform), ou domaine sans agent (Ansible, logs, Flux Kestra → Tech Lead réalise lui-même la vérification et le signale à l'humain).

## Sensors

Outputs: cadrage confirmé + domaine identifié. Aucun gate propre à ce stage.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (domaines et délégations par type de demande) tracés, remontés au gate granulaire de fin de Production / Validation.
