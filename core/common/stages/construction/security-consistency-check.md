---
slug: security-consistency-check
phase: construction
execution: ALWAYS
condition: "Always executes"
lead_agent: Sylvain
support_agents: [Xavier]
mode: inline
summary_confirmation: required
reviewer: Xavier
review_class: granular
human_gate: none
produces: [controle_securite_coherence]
consumes: [{artifact: livrables_detailles, required: true}]
requires_stage: [detailed-deliverables]
sensors: [required-sections]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Livrables détaillés"
outputs: "Contrôle sécurité (Xavier) + cohérence documentation ↔ ADR, corrections demandées le cas échéant"
---

# Contrôle sécurité et cohérence

## Objectif
Vérifier la sécurité et la cohérence des livrables avant consolidation.

## Steps
### Step 1 — Solliciter Xavier
Pour tout livrable modifiant l'architecture (mêmes règles que `design-and-adr`). Plancher SG-3 : aucun gate / sensor advisory ne remplace ce contrôle.

### Step 2 — Vérifier structure, complétude, qualité, format et cohérence avec les ADR.

### Step 3 — Demander les corrections aux agents responsables le cas échéant.

## Gate / sortie
Contrôle sécurité + cohérence consignés. Sensor `required-sections` sur ADR / DAS.
