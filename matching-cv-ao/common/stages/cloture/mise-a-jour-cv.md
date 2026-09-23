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
scopes: [standard, complex, express, format-cv]
inputs: "Demande de mise à jour CV + livraison effectuée (scope standard) ou CV extraits/validés (scope format-cv)"
outputs: "CV mis à jour"
---

# Mise à jour des CV

## Objectif
Mettre à jour les CV des collaborateurs si l'humain le demande (ajout de compétences, mise à jour d'expérience issue du matching) et **produire le CV livrable au format DOCX (par défaut) à partir des gabarits fournis** (CV long / CV court / format client spécifique) — **le format Markdown reste possible uniquement sur demande explicite de l'humain**.

> **Fiche d'analyse ≠ CV livrable** : la fiche d'analyse Markdown + le JSON restent la **mémoire interne** (données) ; le **CV livrable est un DOCX par défaut** rempli depuis un **gabarit fourni** (jamais inventé), situé dans `${ROOT_DIRECTORY}/gabarits/cv/`. Le **format Markdown reste possible uniquement sur demande explicite de l'humain**. Voir la compétence `cv-generation` du plugin `rh-assistant`.

> **Enracinement des chemins** : tous les chemins relatifs sont enracinés sur `${ROOT_DIRECTORY}` (répertoire de travail du workspace) — analyses et livrables dans `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`, gabarits dans `${ROOT_DIRECTORY}/gabarits/cv/`.

## Prérequis selon le scope
- **Scope `standard`** (et `complex` / `express`) : le stage dépend de la **livraison finale** du matching (`livraison-finale`, produit par `livraison`) — comportement inchangé.
- **Scope `format-cv`** : `livraison` est **hors périmètre**. Le prérequis `livraison-finale` est donc **neutralisé** ; la mise à jour s'appuie sur les **CV extraits/validés** (`cv-profils`, produit par `extraction-cv`). Le champ `requires_stage: [livraison]` ne s'applique **pas** sous ce scope.

C'est pourquoi `consumes` déclare les deux artefacts en `required: false` : sous `standard` c'est `livraison-finale` qui alimente l'étape, sous `format-cv` c'est `cv-profils`.

## Steps
### Step 1 — Demande de mise à jour
Si l'humain a demandé une mise à jour de CV, déléguer au Gestionnaire CV.

### Step 2 — Délégation au Gestionnaire CV
Déléguer au Gestionnaire CV selon la **procédure de délégation A2A définie une seule fois dans `stage-protocol` (temps 2)** : JSON de mission joint (type `delegation` du message A2A) + commentaire **minimal** = mention active `[@Gestionnaire CV](mention://agent/<uuid>)` + nom du fichier JSON joint. La mission vit **dans le JSON joint**, pas en prose dans le fil : mettre à jour les CV concernés avec les informations validées lors du matching **et produire le CV livrable au format DOCX (par défaut) à partir du gabarit fourni** (CV long / CV court / format client spécifique, dans `${ROOT_DIRECTORY}/gabarits/cv/` — **gabarit jamais inventé** ; si absent ⇒ halt-and-ask, **pas de repli Markdown automatique**), ou **au format Markdown si l'humain l'a explicitement demandé**, en appliquant la compétence `cv-generation` du plugin `rh-assistant` (procédure de production/mise à jour après validation humaine) et en respectant l'**organisation stricte du répertoire `cv/`** enracinée sur `${ROOT_DIRECTORY}` : CV sources **fournis en pièces jointes de l'issue** et **supprimés après extraction** (originaux non conservés, non stockés dans `cv/`), fiche d'analyse Markdown **du jour** à la racine de `cv/` (mémoire ; anciennes fiches déplacées dans `cv/archives/`), JSON d'analyse **versionné** à la racine (`<nom>-<prenom>-<AAAA-MM-JJ>.json`, sans écraser l'historique), **CV livrable versionné** (`<nom>-<prenom>-<type-gabarit>-<AAAA-MM-JJ>.docx` en DOCX, ou `<nom>-<prenom>-cv-<AAAA-MM-JJ>.md` en Markdown sur demande) à la racine de `cv/`, et **date de dernière modification = date du jour**. **Retour de délégation obligatoire au Coordinateur** en fin de tâche : **JSON de retour joint** (type `retour` du message A2A) + commentaire minimal clos par la mention active + nom du fichier JSON, vérification `trigger_outcomes` — procédure définie une seule fois dans le protocole `stage-protocol` (temps 3).

### Step 3 — Validation explicite (présentation détaillée)
Présenter à l'humain **en détail** les mises à jour effectuées et le **CV livrable produit** (format : DOCX par défaut avec le type de gabarit — CV long / CV court / format client ; ou Markdown si explicitement demandé) pour validation explicite avant finalisation. L'artefact JSON reste la source/piste d'audit ; la présentation à l'humain **reprend en clair** ce qui a changé, elle ne se limite pas à l'action « valider ».

## Sensors
Outputs: `cv-mis-a-jour` → Phase Clôture (gate: explicit).
Imports: none.

## Learn
Documenter sur l'issue les mises à jour effectuées et les validations humaines.
