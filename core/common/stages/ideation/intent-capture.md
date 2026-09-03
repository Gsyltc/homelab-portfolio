---
slug: intent-capture
phase: ideation
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecture Solution & Intégration
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [intention_capturee]
consumes: [{artifact: piste_audit_ouverte, required: true}]
requires_stage: [audit-trail-init]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Demande brute (entrée non résumée)"
outputs: "Demande brute consignée + intention reformulée en une phrase vérifiable"
---

# Capture d'intention

## Objectif

Consigner l'entrée brute et reformuler l'intention en une phrase vérifiable.

## Steps

### Step 1 — Consigner la demande brute

Consigner l'**entrée non résumée** sur l'issue (piste d'audit).

### Step 2 — Reformuler

Reformuler l'intention en une phrase vérifiable (« ce travail vise à… ») et la confirmer.

## Sensors

Outputs: intention capturée sur l'issue. Le gate humain léger a lieu plus tard (`intent-scope-approval`).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles issus des corrections / reformulations humaines pendant le travail ; les remonter formulés en règles courtes au **gate humain** (ici, l'approbation d'Ideation en `intent-scope-approval`) ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
