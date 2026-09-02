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
review_class: advisory
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
Charger la documentation d'architecture, les décisions structurantes et diagrammes pertinents ; en produire une synthèse sur l'issue.

## Gate / sortie
Synthèse du contexte existant (ou N/A consigné).
