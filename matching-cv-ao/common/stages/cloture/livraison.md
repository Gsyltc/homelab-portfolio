---
slug: livraison
phase: cloture
execution: ALWAYS
condition: "Always executes"
lead_agent: Coordinateur Matching
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
review_artifact: ""
human_gate: explicit
produces: [livraison-finale]
consumes: [{artifact: resultats-valides, required: true}, {artifact: cv-eligibilite, required: true}]
requires_stage: [presentation-resultats]
sensors: []
scopes: [standard, complex, express]
inputs: "Profils validés"
outputs: "Livrable final (artefact JSON joint `livraison-finale`) + récap Markdown limité à l'action de validation"
---

# Livraison

## Objectif
Produire et livrer le résumé final du matching à l'humain. **Gate `explicit`** : le livrable est un **artefact JSON joint** `livraison-finale` ; le récap Markdown est **conservé mais limité à l'action** (« valider la livraison »), l'humain n'en lit jamais le JSON brut.

## Steps
### Step 1 — Production du livrable final (JSON joint)
Produire l'artefact **JSON joint** `livraison-finale` (via `multica attachment`) contenant :
- Résumé de l'AO analysée
- Liste des profils retenus avec scores et justification
- **Section obligatoire « collaborateurs non retenus » (filtre d'éligibilité Gestionnaire CV)** : **chaque collaborateur écarté en amont du matching** (issu de `cv-eligibilite`) en distinguant les deux sous-états `exclu` / `a_verifier`, chacun avec ses **raisons par axe** (`{axe, detail}`). Catégories, sous-états et axes définis une seule fois dans le protocole `governance-security` (§ Catégories décisionnelles — non-retenus & exclus). **Obligatoire**, même si aucun collaborateur n'est concerné (indiquer alors « aucun »).
- **Pour un AO gouvernemental : bloc « exclus — non-conformité études »** listant les collaborateurs **exclus pour non-conformité du niveau d'études** (`recommandation = "exclu"`), avec le **motif d'exclusion**. **Obligatoire** et **distinct** de la section « collaborateurs non retenus » ci-dessus (voir `governance-security`, même section).
- Grille remplie (si disponible)
- Recommandations

### Step 2 — Validation explicite humaine (récap limité à l'action)
Demander à l'humain de valider explicitement la livraison via un **récap Markdown limité à l'action** (mention de l'humain + « valider la livraison — voir `livraison-finale` ») pointant l'artefact JSON joint, sans reformuler son contenu en prose. Sur approbation, marquer la livraison comme terminée.

### Step 3 — Notification
Si demandé, envoyer une notification ntfy à l'humain.

## Sensors
Outputs: `livraison-finale` → Phase Clôture (gate: explicit).
Imports: none.

## Learn
Documenter sur l'issue la livraison finale et les validations.
