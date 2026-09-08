---
slug: extraction-cv
phase: analyse
execution: ALWAYS
condition: "Always executes"
lead_agent: Gestionnaire CV
support_agents: []
mode: subagent
summary_confirmation: optional
reviewer: null
review_class: advisory
review_artifact: ""
human_gate: light
produces: [cv-profils]
consumes: [{artifact: cv-available, required: true}]
requires_stage: [chargement-cv]
sensors: []
scopes: [standard]
inputs: "Inventaire des CV disponibles"
outputs: "Profils CV structurés (JSON)"
---

# Extraction des CV

## Objectif
Lire les CV des collaborateurs et en extraire les informations structurées (compétences, expérience, études, disponibilité).

## Steps
### Step 1 — Délégation au Gestionnaire CV
Mentionner le Gestionnaire CV avec mission claire : lire les CV de tous les collaborateurs, extraire les informations structurées, produire le JSON.

### Step 2 — Contrôle du livrable
Vérifier que le JSON contient bien la liste `collaborateurs` avec les champs : `nom`, `competences`, `experience`, `etudes`, `disponibilite`. Signaler les écarts.

### Step 3 — Validation humaine légère
Présenter à l'humain : nombre de collaborateurs analysés, synthèse des profils extraits. Demander validation.

## Sensors
Outputs: `cv-profils` → Phase Analyse (gate: light).
Imports: none.

## Learn
Documenter sur l'issue les choix d'extraction et les validations/rejets humains.
