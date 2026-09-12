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
Mentionner l'Analyste RFP avec mission claire : parser le PDF d'AO, extraire exigences et profils recherchés, produire le JSON structuré, sauvegarder dans `${ROOT_DIRECTORY}/ao/<client>/<titre-ao>`. **Détecter le caractère gouvernemental du client** (`client_gouvernemental`) et, le cas échéant, la **politique d'équivalence des diplômes** acceptée par l'AO (`equivalence_diplomes` : mécanisme, compensation en années d'xp par année d'études manquante, `reference_ao`) — exemple : « Niveau requis Baccalauréat — Équivalence DEC + 3 années d'xp par année d'études manquante ». **Détecter le mode de travail** (`localisation_travail.mode` ∈ {`teletravail`, `sur_site`, `hybride`, `non_precise`}) et, pour un travail `sur_site`/`hybride`, **extraire l'adresse du site** (`ville_site` au minimum, `adresse_site` si disponible) avec le `rayon_km` de proximité (défaut `70`) — ex. « présence sur site à Montréal ». **Ne jamais inventer** : si l'AO ne précise pas, `acceptee: "non_precise"` / `mode: "non_precise"` et champs à `null`. Renseigner `etudes_requises` de chaque profil recherché avec le niveau requis. **En fin de tâche, l'Analyste rend son résultat en mentionnant en retour le Coordinateur** `[@Coordinateur Matching](mention://agent/<UUID-COORDINATEUR>)` (mention agent valide, pas une simple réponse), puis vérifie les `trigger_outcomes`. Ne jamais deviner ni coder en dur l'UUID : le résoudre à chaque fois via `multica agent list --output json` et l'injecter dans la mention.

### Step 2 — Contrôle du livrable
Vérifier que le JSON retourné contient bien les champs : `ao` (metadata, dont `client_gouvernemental`, `equivalence_diplomes` avec `acceptee` ∈ {`oui`, `non`, `non_precise`}, et `localisation_travail` avec `mode` ∈ {`teletravail`, `sur_site`, `hybride`, `non_precise`} et `ville_site` non nul si `mode` ∈ {`sur_site`, `hybride`}), `exigences` (liste), `profils_recherches` (liste, dont `etudes_requises` renseigné). Signaler les écarts.

### Step 3 — Validation humaine légère
Présenter à l'humain : résumé de l'AO, nombre d'exigences extraites, profils identifiés. **Pour un AO gouvernemental, présenter explicitement la politique d'équivalence des diplômes détectée** (`equivalence_diplomes` : mécanisme + compensation + référence AO) **ou son absence** (`non_precise` — ne rien inventer, mention humaine possible), afin que l'humain en ait connaissance avant le matching. **Présenter le mode de travail détecté** (`localisation_travail.mode`) et, pour un travail `sur_site`/`hybride`, la **ville/adresse du site** et le **rayon de proximité** (70 km par défaut) qui servira à écarter les collaborateurs trop éloignés — ou signaler `non_precise` (mention humaine possible). Demander validation (Keep/Modify/Redo).

## Sensors
Outputs: `ao-exigences`, `ao-profils-recherches` → Phase Analyse (gate: light).
Imports: none.

## Learn
Documenter sur l'issue les choix d'extraction et les validations/rejets humains.
