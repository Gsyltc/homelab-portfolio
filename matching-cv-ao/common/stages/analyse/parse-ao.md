---
slug: parse-ao
phase: analyse
execution: ALWAYS
condition: "Always executes"
lead_agent: Analyste RFP
support_agents: []
mode: subagent
summary_confirmation: optional
reviewer: null
review_class: advisory
review_artifact: ""
human_gate: light
produces: [ao-exigences, ao-profils-recherches]
consumes: [{artifact: ao-pdf-received, required: true}]
requires_stage: [chargement-cv]
sensors: []
scopes: [standard]
inputs: "PDF d'AO + chemin du répertoire"
outputs: "Résumé AO (JSON) + exigences + profils recherchés"
---

# Analyse de l'AO

## Objectif
Parser le PDF d'appel d'offres, en extraire les exigences fonctionnelles et techniques, et identifier les profils recherchés.

## Steps
### Step 1 — Délégation à l'Analyste RFP
Mentionner l'Analyste RFP avec mission claire : parser le PDF d'AO, extraire exigences et profils recherchés, produire le JSON structuré, sauvegarder dans `${ROOT_DIRECTORY}/ao/<client>/<titre-ao>`. **En fin de tâche, l'Analyste rend son résultat en mentionnant en retour le Coordinateur** `[@Coordinateur Matching](mention://agent/<UUID-COORDINATEUR>)` (mention agent valide, pas une simple réponse), puis vérifie les `trigger_outcomes`. Ne jamais deviner ni coder en dur l'UUID : le résoudre à chaque fois via `multica agent list --output json` et l'injecter dans la mention.

### Step 2 — Contrôle du livrable
Vérifier que le JSON retourné contient bien les champs : `ao` (metadata), `exigences` (liste), `profils_recherches` (liste). Signaler les écarts.

### Step 3 — Validation humaine légère
Présenter à l'humain : résumé de l'AO, nombre d'exigences extraites, profils identifiés. Demander validation (Keep/Modify/Redo).

## Sensors
Outputs: `ao-exigences`, `ao-profils-recherches` → Phase Analyse (gate: light).
Imports: none.

## Learn
Documenter sur l'issue les choix d'extraction et les validations/rejets humains.
