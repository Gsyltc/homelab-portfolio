---
slug: brownfield-greenfield-detection
phase: initialization
execution: ALWAYS
condition: "Always executes — fait détecté, non validé"
lead_agent: null
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [contexte_brownfield_greenfield_consigne]
consumes: [{artifact: repertoire_projet_confirme, required: true}]
requires_stage: [directory-check]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Répertoire projet confirmé"
outputs: "Nature du travail (brownfield / greenfield) consignée sur l'issue"
---

# Détection brownfield / greenfield

## Objectif
Déterminer si le travail part d'un existant (brownfield) ou d'une page blanche (greenfield).

## Steps
### Step 1 — Détecter l'existant
- **Brownfield** : documentation d'architecture, ADR, diagrammes ou infrastructure préexistants → l'Inception activera `existing-context-loading` et le contrôle d'orphelins s'appuie sur l'existant.
- **Greenfield** : aucun existant pertinent → `existing-context-loading` marqué **N/A**, conception partant d'une page blanche.

### Step 2 — Consigner
Le résultat est **consigné sur l'issue** ; il n'appelle pas de validation humaine (fait détecté).

## Gate / sortie
Contexte brownfield / greenfield consigné. Aucun gate humain.
