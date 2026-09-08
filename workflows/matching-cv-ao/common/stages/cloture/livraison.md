---
slug: livraison
phase: cloture
execution: ALWAYS
condition: "Always executes"
lead_agent: Coordinateur Matching
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
review_artifact: ""
human_gate: explicit
produces: [livraison-finale]
consumes: [{artifact: resultats-valides, required: true}]
requires_stage: [presentation-resultats]
sensors: []
scopes: [standard]
inputs: "Profils validés"
outputs: "Livrable final (résumé Markdown)"
---

# Livraison

## Objectif
Produire et livrer le résumé final du matching à l'humain.

## Steps
### Step 1 — Production du livrable final
Produire un document Markdown récapitulatif contenant :
- Résumé de l'AO analysée
- Liste des profils retenus avec scores et justification
- Grille remplie (si disponible)
- Recommandations

### Step 2 — Validation explicite humaine
Demander à l'humain de valider explicitement la livraison. Sur approbation, marquer la livraison comme terminée.

### Step 3 — Notification
Si demandé, envoyer une notification ntfy à l'humain.

## Sensors
Outputs: `livraison-finale` → Phase Clôture (gate: explicit).
Imports: none.

## Learn
Documenter sur l'issue la livraison finale et les validations.
