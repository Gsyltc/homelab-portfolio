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
scopes: [standard]
inputs: "Profils validés"
outputs: "Livrable final (résumé Markdown)"
---

# Livraison

## Objectif
Produire et livrer le résumé final du matching à l'humain.

## Steps
### Step 1 — Production du livrable final
Produire un document Markdown récapitulatif contenant :
- Résumé de l'AO analysée
- Liste des profils retenus avec scores et justification
- **Section obligatoire « Collaborateurs non retenus » (filtre d'éligibilité Gestionnaire CV)** : lister **chaque collaborateur écarté par le Gestionnaire CV en amont du matching** (issu de `cv-eligibilite`), avec la/les **raison(s)** (axe `etudes | mifi | experiences | coherence | fraicheur_cv` + détail), en **distinguant explicitement** deux catégories :
  - **`exclu`** — écarté définitivement vis-à-vis de l'AO ;
  - **`a_verifier`** — en attente d'un arbitrage humain (ex. MIFI non tranché ; ne rien inventer).
  Cette section est **obligatoire** dans le rapport final, même si aucun collaborateur n'est concerné (indiquer alors « aucun »).
- **Pour un AO gouvernemental : section « Exclus — non-conformité études »** listant explicitement les collaborateurs **exclus pour non-conformité du niveau d'études** (`recommandation = "exclu"`), avec le **motif d'exclusion** (niveau requis vs niveau du collaborateur, équivalence MIFI, compensation appliquée). Cette mention est **obligatoire** dans le rapport final et **distincte** de la section « Collaborateurs non retenus » (filtre d'éligibilité amont) ci-dessus.
- Grille remplie (si disponible)
- Recommandations

### Step 2 — Validation explicite humaine
Demander à l'humain de valider explicitement la livraison. Sur approbation, marquer la livraison comme terminée.

### Step 3 — Notification
Si demandé, envoyer une notification ntfy à l'humain.

## Sensors
Outputs: `livraison-finale` → Phase Clôture (gate: explicit).
Imports: none.

## Learn
Documenter sur l'issue la livraison finale et les validations.
