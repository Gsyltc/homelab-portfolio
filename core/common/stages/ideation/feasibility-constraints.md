---
slug: feasibility-constraints
phase: ideation
execution: ALWAYS
condition: "Always executes — évaluation légère"
lead_agent: Architecture Solution & Intégration
support_agents: [Architecte de solution, Architecte AWS, Architecte Cybersécurité]
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
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

Évaluer la faisabilité et les contraintes fortes (techniques, sécurité, coût, délais) susceptibles de rendre le travail non pertinent ou de le réorienter. Les `support_agents` (Architecte de solution, Architecte AWS, Architecte cybersécurité) sont des **voix adoptées** en `inline`, pas une revue indépendante.

### Step 2 — Réorientation éventuelle

Si une contrainte forte remet en cause l'intention, la signaler à l'humain avant d'avancer. L'étude détaillée relève de l'Inception, pas de ce stage.

## Sensors

Outputs: faisabilité / contraintes consignées sur l'issue. Allégé (➖) sur `poc` / `express`.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (contraintes récurrentes, motifs de réorientation) ; les remonter au **gate humain** léger d'Ideation ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
