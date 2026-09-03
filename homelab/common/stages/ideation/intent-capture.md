---
slug: intent-capture
phase: ideation
execution: ALWAYS
condition: "Always executes (branches n8n / home-assistant court-circuitées vers leur flux dédié)"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: optional
reviewer: null
review_class: none
human_gate: none
produces: [intention_capturee]
consumes: [{artifact: detection_stack_existante_vs_nouvelle, required: false}]
requires_stage: [labels-audit-init]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Demande brute (humain / agent)"
outputs: "Intention déclarée consignée + clarté évaluée"
---

# Capture d'intention

## Objectif

Consigner l'intention déclarée et sa clarté avant toute conception.

## Steps

### Step 1 — Consigner l'intention brute

Consigner l'**intention déclarée** (entrée brute humain / agent) sur l'issue.

### Step 2 — Évaluer la clarté

Aucune supposition : une intention ambiguë est **clarifiée avec l'humain** avant d'avancer.

## Sensors

Outputs: intention capturée consignée. Aucun gate humain à ce stage (le gate léger est porté par `intent-scope-approval`).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : ouvrir le journal des candidats-règles d'Idéation ; remontée au gate léger (`intent-scope-approval`), jamais dans le run courant.
