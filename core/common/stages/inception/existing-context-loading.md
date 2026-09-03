---
slug: existing-context-loading
phase: inception
execution: CONDITIONAL
condition: "Brownfield détecté en Initialization ET contexte insuffisant"
lead_agent: Architecture Solution & Intégration
support_agents: [Architecte de solution]
mode: inline
summary_confirmation: optional
reviewer: null
review_class: none
human_gate: none
produces: [synthese_contexte_existant]
consumes: [{artifact: contexte_brownfield_greenfield_consigne, required: true}, {artifact: cadrage_confirme, required: true}]
requires_stage: [intake-framing]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Contexte brownfield détecté"
outputs: "Synthèse de la documentation d'architecture, décisions structurantes et diagrammes existants (ou N/A si greenfield)"
---

# Chargement du contexte existant (conditionnel)

## Objectif
Charger et synthétiser l'existant pertinent en contexte brownfield.

## Steps
### Step 1 — Condition d'exécution
Exécuter **SI** brownfield détecté et contexte insuffisant. **Ignorer (N/A) SI** greenfield ou contexte déjà suffisant.

### Step 2 — Charger et synthétiser
Charger la documentation d'architecture, les décisions structurantes et diagrammes pertinents ; en produire une synthèse sur l'issue. L'Architecte de solution est une **voix adoptée** en `inline`, pas une revue indépendante.

## Sensors
Outputs: synthèse du contexte existant (ou N/A consigné).
Imports: none.

## Learn
Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de contexte existant récurrents) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit. Divergence tracée vs un journal `memory.md` externe (voir [ADR-0009](../../../../decisions/0009-alignement-fiches-de-stage-sur-ai-dlc.md)).
