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

> **Source du CV pour le matching** : si un CV PDF/DOCX a été fourni dans l'issue pour un collaborateur, le stage `extraction-cv` en a d'abord produit une nouvelle version JSON — c'est elle qui est croisée. Si aucun CV n'a été fourni, le matching utilise directement la **dernière version JSON déjà extraite** (flux A2A). Voir la règle de sélection de la source CV dans [`../../../agents/gestionnaire-cv-agent.md`](../../../agents/gestionnaire-cv-agent.md).

## Steps
### Step 1 — Délégation au Matcher Profils
Mentionner le Matcher Profils avec mission claire : croiser **la dernière version JSON** de chaque profil CV (`cv-profils`) avec les exigences AO, calculer le score pondéré (compétences 50%, expérience 35%, études 10%, disponibilité 5%), classer par score décroissant. **En fin de tâche, le Matcher rend son résultat en mentionnant en retour le Coordinateur** `[@Coordinateur Matching](mention://agent/<UUID-COORDINATEUR>)` (mention agent valide, pas une simple réponse), puis vérifie les `trigger_outcomes`. Ne jamais deviner ni coder en dur l'UUID : le résoudre à chaque fois via `multica agent list --output json` et l'injecter dans la mention.

> **Fraîcheur des compétences** : le Matcher doit **exclure du calcul de compatibilité toute compétence non utilisée depuis plus de 10 ans** (champ `derniere_utilisation`). Une exigence couverte uniquement par une compétence périmée est considérée comme **non couverte**.

> **Conformité du niveau d'études (AO gouvernemental)** : lorsque `ao.client_gouvernemental = true`, le Matcher doit **croiser le niveau d'études requis + l'équivalence MIFI (`mifi`) + la politique de compensation de l'AO** pour statuer la conformité de chaque collaborateur (bloc `conformite_etudes`). Un collaborateur **non conforme** (`conforme = "non"`) est **exclu** du classement (`recommandation = "exclu"`, `motif_exclusion` renseigné, `score_total` écarté). Un collaborateur en `conforme = "a_verifier"` (MIFI non tranché) est **signalé à l'humain**, sans exclusion automatique. Cette règle **n'altère pas** les poids du scoring immuable (voir [`../../../agents/matcher-profils-agent.md`](../../../agents/matcher-profils-agent.md)).

### Step 2 — Contrôle du livrable
Vérifier que le JSON contient la liste `resultats` avec les champs : `collaborateur`, `score_total`, détail par critère (dont `score_competences.competences_ignorees_peremption`), `conformite_etudes` (dont `conforme` et `motif_exclusion` si `conforme = "non"`, renseigné pour un AO gouvernemental), `recommandation` (valeur `exclu` possible), `justification`.

### Step 3 — Gate advisory
Présenter à l'humain : top 5 des profils avec scores, recommandations. **Faire ressortir explicitement les profils exclus** (`recommandation = "exclu"` — non-conformité du niveau d'études sur AO gouvernemental, avec motif) **et ceux à vérifier** (`conformite_etudes.conforme = "a_verifier"`, MIFI non tranché). L'humain peut ajuster les poids ou demander un recalcul.

## Sensors
Outputs: `matching-resultats` → Phase Matching (gate: advisory).
Imports: none.

## Learn
Documenter sur l'issue les ajustements de scoring et les validations/rejets humains.
