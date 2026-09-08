---
slug: remplissage-grille
phase: validation
execution: CONDITIONAL
condition: "Grille d'évaluation fournie par l'humain"
lead_agent: Coordinateur Matching
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
review_artifact: ""
human_gate: granular
produces: [grille-remplie]
consumes: [{artifact: resultats-valides, required: true}, {artifact: grille-evaluation, required: true}]
requires_stage: [presentation-resultats]
sensors: []
scopes: [standard]
inputs: "Profils validés + grille d'évaluation"
outputs: "Grille remplie avec les profils"
---

# Remplissage de la grille d'évaluation

## Objectif
Remplir la grille d'évaluation client fournie par l'humain avec les profils validés.

## Steps
### Step 1 — Vérification de la grille
Vérifier que l'humain a fourni une grille d'évaluation. Si absente, la demander. **Ne jamais inventer de grille.**

### Step 2 — Remplissage
Pour chaque critère de la grille, renseigner le(s) profil(s) correspondant(s) avec les données du matching validé.

### Step 3 — Validation
Présenter la grille remplie à l'humain pour validation.

## Sensors
Outputs: `grille-remplie` → Phase Validation (gate: granular).
Imports: none.

## Learn
Documenter sur l'issue les choix de remplissage et les validations/rejets humains.
