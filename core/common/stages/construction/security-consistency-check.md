---
slug: security-consistency-check
phase: construction
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecture Solution & Intégration
support_agents: [Architecte Cybersécurité]
mode: inline
summary_confirmation: required
reviewer: Reviewer de sécurité
review_class: adversarial
review_artifact: controle-securite-coherence.md
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

> **Séquencement — la sécurité intervient en dernier (garde-fou).** Ce contrôle sécurité ne démarre **qu'après que toutes les tâches des spécialistes / architectes dépendantes ont été produites et revues** (revue de cohérence passée, livrables remontés `in_review` par leurs agents délégataires). Il porte sur l'**ensemble consolidé des livrables**, et non tâche par tâche au fil de l'eau. Tant qu'une tâche de livrable reste en production ou non revue, le coordinateur **ne sollicite pas** encore le Reviewer de sécurité pour cette phase. Ce séquencement est un garde-fou (voir [`conductor.md`](../../conductor.md), « Contrôle sécurité minimal »). *(Il ne concerne pas la revue de sécurité adversariale propre à l'ADR, qui a lieu plus tôt, au stage [`design-and-decisions.md`](../inception/design-and-decisions.md), pour conditionner la décision humaine sur l'ADR.)*

## Steps

### Step 1 — Solliciter le Reviewer de sécurité (revue adversariale)

Pour tout livrable modifiant l'architecture (mêmes règles que `design-and-decisions`), le coordinateur sollicite le **Reviewer de sécurité** ; l'Architecte cybersécurité (voix adoptée `inline`) pilote l'analyse de posture. Plancher SG-3 : aucun gate / sensor advisory, aucune revue de cohérence ne remplace ce contrôle adversarial.

### Step 2 — Vérifier structure, complétude, qualité, format et cohérence avec les décisions structurantes

### Step 3 — Demander les corrections aux agents responsables le cas échéant

## Sensors

Outputs: contrôle sécurité + cohérence consignés.
Imports: `required-sections` (documents de décision / DAS).
Review artifact: `controle-securite-coherence.md` porte la section `## Review` ajoutée par le Reviewer de sécurité.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de non-conformité sécurité / cohérence récurrents) ; les remonter au **gate humain** de Construction ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit (toute règle touchant la sécurité repasse au contrôle sécurité).
