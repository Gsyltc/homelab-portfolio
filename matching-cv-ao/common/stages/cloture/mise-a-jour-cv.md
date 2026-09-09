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
consumes: [{artifact: livraison-finale, required: false}, {artifact: cv-profils, required: false}]
requires_stage: [livraison]
sensors: []
scopes: [standard, format-cv]
inputs: "Demande de mise à jour CV + livraison effectuée (scope standard) ou CV extraits/validés (scope format-cv)"
outputs: "CV mis à jour"
---

# Mise à jour des CV

## Objectif
Mettre à jour les CV des collaborateurs si l'humain le demande (ajout de compétences, mise à jour d'expérience issue du matching).

## Prérequis selon le scope
- **Scope `standard`** (et `complex` / `express`) : le stage dépend de la **livraison finale** du matching (`livraison-finale`, produit par `livraison`) — comportement inchangé.
- **Scope `format-cv`** : `livraison` est **hors périmètre**. Le prérequis `livraison-finale` est donc **neutralisé** ; la mise à jour s'appuie sur les **CV extraits/validés** (`cv-profils`, produit par `extraction-cv`). Le champ `requires_stage: [livraison]` ne s'applique **pas** sous ce scope.

C'est pourquoi `consumes` déclare les deux artefacts en `required: false` : sous `standard` c'est `livraison-finale` qui alimente l'étape, sous `format-cv` c'est `cv-profils`.

## Steps
### Step 1 — Demande de mise à jour
Si l'humain a demandé une mise à jour de CV, déléguer au Gestionnaire CV.

### Step 2 — Délégation au Gestionnaire CV
Mentionner le Gestionnaire CV avec mission claire : mettre à jour les CV concernés avec les informations validées lors du matching, en respectant l'**organisation stricte du répertoire `cv/`** : CV sources dans `cv/originaux/`, fiche d'analyse Markdown **du jour** à la racine de `cv/` (anciennes fiches déplacées dans `cv/archives/`), JSON d'analyse **versionné** à la racine (`<nom>-<prenom>-<AAAA-MM-JJ>.json`, sans écraser l'historique), et **date de dernière modification = date du jour**. **En fin de tâche, le Gestionnaire CV rend son résultat en mentionnant en retour le Coordinateur** `[@Coordinateur Matching](mention://agent/<UUID-COORDINATEUR>)` (mention agent valide, pas une simple réponse), puis vérifie les `trigger_outcomes`. Ne jamais deviner ni coder en dur l'UUID : le résoudre à chaque fois via `multica agent list --output json` et l'injecter dans la mention.

### Step 3 — Validation explicite
Présenter les modifications effectuées à l'humain pour validation explicite avant finalisation.

## Sensors
Outputs: `cv-mis-a-jour` → Phase Clôture (gate: explicit).
Imports: none.

## Learn
Documenter sur l'issue les mises à jour effectuées et les validations humaines.
