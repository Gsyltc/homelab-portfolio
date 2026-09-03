---
slug: security-consistency-check
phase: construction
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecture Solution & Intégration
support_agents: [Architecte cybersécurité]
mode: inline
summary_confirmation: required
reviewer: Reviewer de sécurité
review_class: granular
human_gate: none
produces: [controle_securite_coherence]
consumes: [{artifact: livrables_detailles, required: true}]
requires_stage: [detailed-deliverables]
sensors: [required-sections]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Livrables détaillés"
outputs: "Contrôle sécurité + cohérence documentation ↔ décisions structurantes, corrections demandées le cas échéant"
---

# Contrôle sécurité et cohérence

## Objectif
Vérifier la sécurité et la cohérence des livrables avant consolidation.

## Steps
### Step 1 — Solliciter l'Architecte cybersécurité
Pour tout livrable modifiant l'architecture (mêmes règles que `design-and-decisions`). Plancher SG-3 : aucun gate / sensor advisory ne remplace ce contrôle.

### Step 2 — Vérifier structure, complétude, qualité, format et cohérence avec les décisions structurantes.

### Step 3 — Demander les corrections aux agents responsables le cas échéant.

## Gate / sortie
Contrôle sécurité + cohérence consignés. Sensor `required-sections` sur les documents de décision / DAS.
