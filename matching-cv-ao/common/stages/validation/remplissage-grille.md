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
scopes: [standard, complex, express]
inputs: "Profils validés + grille d'évaluation"
outputs: "Grille remplie avec les profils"
---

# Remplissage de la grille d'évaluation

## Objectif
Remplir la grille d'évaluation client fournie par l'humain avec les profils validés.

## Steps
### Step 1 — Grille (après matching)
Grille fournie → remplir. Grille absente → halt-and-ask, mention explicite de l'humain.

### Step 2 — Remplissage
Pour chaque critère de la grille, renseigner le(s) profil(s) correspondant(s) avec les données du matching validé (issues de l'artefact JSON `resultats-valides`). L'artefact produit `grille-remplie` est joint à l'issue (JSON / fichier de grille).

### Step 3 — Validation (gate humaine, action seule)
Présenter la grille remplie à l'humain pour validation via un **récap Markdown limité à l'action** (mention de l'humain + « valider la grille remplie — voir `grille-remplie` »). Les données restent dans l'artefact joint ; ne pas les reformuler en prose.

## Sensors
Outputs: `grille-remplie` → Phase Validation (gate: granular).
Imports: none.

## Learn
Documenter sur l'issue les choix de remplissage et les validations/rejets humains.
