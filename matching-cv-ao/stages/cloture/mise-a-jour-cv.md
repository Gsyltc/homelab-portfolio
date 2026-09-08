---
slug: mise-a-jour-cv
phase: cloture
execution: CONDITIONAL
condition: "Mise à jour de CV demandée par l'humain"
lead_agent: Gestionnaire CV
support_agents: []
mode: subagent
summary_confirmation: optional
reviewer: null
review_class: none
review_artifact: ""
human_gate: explicit
produces: [cv-mis-a-jour]
consumes: [{artifact: livraison-finale, required: true}]
requires_stage: [livraison]
sensors: []
scopes: [standard]
inputs: "Demande de mise à jour CV + livraison effectuée"
outputs: "CV mis à jour"
---

# Mise à jour des CV

## Objectif
Mettre à jour les CV des collaborateurs si l'humain le demande (ajout de compétences, mise à jour d'expérience issue du matching).

## Steps
### Step 1 — Demande de mise à jour
Si l'humain a demandé une mise à jour de CV, déléguer au Gestionnaire CV.

### Step 2 — Délégation au Gestionnaire CV
Mentionner le Gestionnaire CV avec mission claire : mettre à jour les CV concernés avec les informations validées lors du matching.

### Step 3 — Validation explicite
Présenter les modifications effectuées à l'humain pour validation explicite avant finalisation.

## Sensors
Outputs: `cv-mis-a-jour` → Phase Clôture (gate: explicit).
Imports: none.

## Learn
Documenter sur l'issue les mises à jour effectuées et les validations humaines.
