---
slug: croisement-profils
phase: matching
execution: ALWAYS
condition: "Always executes"
lead_agent: Matcher Profils
support_agents: []
mode: subagent
summary_confirmation: optional
reviewer: null
review_class: advisory
review_artifact: ""
human_gate: light
produces: [matching-resultats]
consumes: [{artifact: ao-profils-recherches, required: true}, {artifact: cv-profils, required: true}]
requires_stage: [parse-ao, extraction-cv]
sensors: []
scopes: [standard]
inputs: "Exigences AO + profils CV (dernière version JSON, `cv-profils`)"
outputs: "Scores et classement des profils (JSON)"
---

# Croisement profils ↔ exigences

## Objectif
Croiser les exigences de l'AO avec les profils des collaborateurs et calculer un score pondéré pour chaque profil. Dans les scopes `standard`, `complex` et `express`, l'artefact CV croisé est la **dernière version JSON** de chaque collaborateur (`<nom>-<prenom>-<AAAA-MM-JJ>.json`, `cv-profils`) — flux entre agents ; les versions JSON antérieures et les fichiers sources (supprimés après extraction) ne sont jamais utilisés.

## Steps
### Step 1 — Délégation au Matcher Profils
Mentionner le Matcher Profils avec mission claire : croiser **la dernière version JSON** de chaque profil CV (`cv-profils`) avec les exigences AO, calculer le score pondéré (compétences 50%, expérience 35%, études 10%, disponibilité 5%), classer par score décroissant. **En fin de tâche, le Matcher rend son résultat en mentionnant en retour le Coordinateur** `[@Coordinateur Matching](mention://agent/<UUID-COORDINATEUR>)` (mention agent valide, pas une simple réponse), puis vérifie les `trigger_outcomes`. Ne jamais deviner ni coder en dur l'UUID : le résoudre à chaque fois via `multica agent list --output json` et l'injecter dans la mention.

> **Fraîcheur des compétences** : le Matcher doit **exclure du calcul de compatibilité toute compétence non utilisée depuis plus de 10 ans** (champ `derniere_utilisation`). Une exigence couverte uniquement par une compétence périmée est considérée comme **non couverte**.

### Step 2 — Contrôle du livrable
Vérifier que le JSON contient la liste `resultats` avec les champs : `collaborateur`, `score_total`, détail par critère (dont `score_competences.competences_ignorees_peremption`), `recommandation`, `justification`.

### Step 3 — Gate advisory
Présenter à l'humain : top 5 des profils avec scores, recommandations. L'humain peut ajuster les poids ou demander un recalcul.

## Sensors
Outputs: `matching-resultats` → Phase Matching (gate: advisory).
Imports: none.

## Learn
Documenter sur l'issue les ajustements de scoring et les validations/rejets humains.
