---
slug: feasibility-constraints
phase: ideation
execution: ALWAYS
condition: "Always executes — évaluation légère"
lead_agent: Sylvain
support_agents: [Manuel, Florian, Xavier]
mode: inline
summary_confirmation: required
reviewer: null
review_class: advisory
human_gate: none
produces: [faisabilite_contraintes_evaluees]
consumes: [{artifact: intention_capturee, required: true}]
requires_stage: [intent-capture]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Intention capturée"
outputs: "Faisabilité et contraintes fortes (techniques, sécurité, coût, délais) évaluées légèrement"
---

# Faisabilité et contraintes

## Objectif
Éviter d'engager l'Inception sur une base non viable, sans produire d'étude détaillée.

## Steps
### Step 1 — Évaluation légère
Évaluer la faisabilité et les contraintes fortes (techniques, sécurité, coût, délais) susceptibles de rendre le travail non pertinent ou de le réorienter.

### Step 2 — Réorientation éventuelle
Si une contrainte forte remet en cause l'intention, la signaler à l'humain avant d'avancer. L'étude détaillée relève de l'Inception, pas de ce stage.

## Gate / sortie
Faisabilité / contraintes consignées sur l'issue. Allégé (➖) sur `poc` / `express`.
