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
consumes: [{artifact: ao-profils-recherches, required: true}, {artifact: cv-profils, required: true}, {artifact: cv-eligibilite, required: true}]
requires_stage: [parse-ao, extraction-cv]
sensors: []
scopes: [standard]
inputs: "Exigences AO + verdict d'éligibilité (`cv-eligibilite`, retenus uniquement) + profils CV (dernière version JSON, `cv-profils`) des seuls retenus"
outputs: "Scores et classement des profils (JSON)"
---

# Croisement profils ↔ exigences

## Objectif
Croiser les exigences de l'AO avec les profils des collaborateurs et calculer un score pondéré pour chaque profil. **Le Matcher ne score que les collaborateurs retenus par le Gestionnaire CV** (`eligibilite.collaborateurs_possibles` de `cv-eligibilite`) : les collaborateurs `exclu` et `a_verifier` du filtre d'éligibilité amont **ne sont pas scorés**, mais sont transmis tels quels au classement/livraison. Dans les scopes `standard`, `complex` et `express`, l'artefact CV croisé est la **dernière version JSON** de chaque retenu (`<nom>-<prenom>-<AAAA-MM-JJ>.json`, `cv-profils`, référencée par `analyse_json` dans `cv-eligibilite`) — flux entre agents ; les versions JSON antérieures et les fichiers sources (supprimés après extraction) ne sont jamais utilisés.

> **Filtre d'éligibilité amont (Gestionnaire CV)** : le Gestionnaire CV a déjà appliqué, en amont, une **sélection d'éligibilité vis-à-vis de l'AO** (axes Études / MIFI si nécessaire / Expériences / **Localisation si présence sur site requise**) produisant trois états — `possible`, `a_verifier`, `exclu`. Le Matcher **reçoit du coordinateur uniquement la liste des retenus** (`possible`) et **ne lit / ne score que ceux-là**. Les `exclu` et `a_verifier` sont des **non-retenus d'éligibilité**, distincts des exclus « conformité études » internes au Matcher ci-dessous, et sont propagés au classement et à la livraison avec leurs raisons (dont l'axe `localisation` : ex. « AO Montréal, candidat à Québec — > 70 km », ou ville manquante en `a_verifier`).

> **Source du CV pour le matching** : le Matcher lit lui-même la **dernière version JSON** des seuls retenus (`analyse_json` de `eligibilite.collaborateurs_possibles`) — les CV ne lui sont pas transmis par le Gestionnaire CV. Si un CV PDF/DOCX a été fourni dans l'issue pour un retenu, le stage `extraction-cv` en a d'abord produit une nouvelle version JSON — c'est elle qui est croisée. Si aucun CV n'a été fourni, le matching utilise directement la **dernière version JSON déjà extraite** (flux A2A). Voir la règle de sélection de la source CV dans [`../../../agents/gestionnaire-cv-agent.md`](../../../agents/gestionnaire-cv-agent.md).

## Steps
### Step 1 — Délégation au Matcher Profils
Mentionner le Matcher Profils avec mission claire : croiser **la dernière version JSON** des **seuls profils retenus par le Gestionnaire CV** (`eligibilite.collaborateurs_possibles`, référencés par leur `analyse_json` dans `cv-eligibilite`) avec les exigences AO, calculer le score pondéré (compétences 50%, expérience 35%, études 10%, disponibilité 5%), classer par score décroissant. **Ne pas scorer** les collaborateurs `exclu` ni `a_verifier` du filtre d'éligibilité amont — les propager tels quels (avec leurs raisons) au classement. **En fin de tâche, le Matcher rend son résultat en mentionnant en retour le Coordinateur** `[@Coordinateur Matching](mention://agent/<UUID-COORDINATEUR>)` (mention agent valide, pas une simple réponse), puis vérifie les `trigger_outcomes`. Ne jamais deviner ni coder en dur l'UUID : le résoudre à chaque fois via `multica agent list --output json` et l'injecter dans la mention.

> **Fraîcheur des compétences** : le Matcher doit **exclure du calcul de compatibilité toute compétence non utilisée depuis plus de 10 ans** (champ `derniere_utilisation`). Une exigence couverte uniquement par une compétence périmée est considérée comme **non couverte**.

> **Conformité du niveau d'études (AO gouvernemental) — double check aval du filtre amont** : le filtre d'éligibilité du Gestionnaire CV ne supprime pas ce contrôle. Lorsque `ao.client_gouvernemental = true`, le Matcher doit **croiser le niveau d'études requis + l'équivalence MIFI (`mifi`) + la politique de compensation de l'AO** pour statuer la conformité de chaque **retenu** (bloc `conformite_etudes`) — il s'agit d'un **double contrôle en aval** du filtre d'éligibilité amont. Un retenu **non conforme** (`conforme = "non"`) est **exclu** du classement (`recommandation = "exclu"`, `motif_exclusion` renseigné, `score_total` écarté). Un retenu en `conforme = "a_verifier"` (MIFI non tranché) est **signalé à l'humain**, sans exclusion automatique. Cette règle **n'altère pas** les poids du scoring immuable (voir [`../../../agents/matcher-profils-agent.md`](../../../agents/matcher-profils-agent.md)).

### Step 2 — Contrôle du livrable
Vérifier que le JSON contient la liste `resultats` avec les champs : `collaborateur`, `score_total`, détail par critère (dont `score_competences.competences_ignorees_peremption`), `conformite_etudes` (dont `conforme` et `motif_exclusion` si `conforme = "non"`, renseigné pour un AO gouvernemental), `recommandation` (valeur `exclu` possible), `justification`. Vérifier également que **seuls les retenus d'éligibilité** (`possible`) figurent dans `resultats`, et que les **non-retenus d'éligibilité** (`exclu` / `a_verifier` du Gestionnaire CV, avec leurs raisons) sont **propagés tels quels** vers le classement/livraison (distincts des exclus « conformité études » du Matcher).

### Step 3 — Gate advisory
Présenter à l'humain : top 5 des profils retenus avec scores, recommandations. **Faire ressortir explicitement les profils exclus** (`recommandation = "exclu"` — non-conformité du niveau d'études sur AO gouvernemental, avec motif) **et ceux à vérifier** (`conformite_etudes.conforme = "a_verifier"`, MIFI non tranché). **Rappeler les non-retenus d'éligibilité amont** (Gestionnaire CV) — `exclu` et `a_verifier` avec leurs raisons par axe (dont l'axe `localisation` : hors rayon de proximité > 70 km, ou ville manquante) — qui n'ont pas été scorés. L'humain peut ajuster les poids ou demander un recalcul.

## Sensors
Outputs: `matching-resultats` → Phase Matching (gate: advisory).
Imports: none.

## Learn
Documenter sur l'issue les ajustements de scoring et les validations/rejets humains.
