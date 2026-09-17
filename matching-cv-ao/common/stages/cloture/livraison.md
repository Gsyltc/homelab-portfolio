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
- **Section obligatoire « Collaborateurs non retenus » (filtre d'éligibilité Gestionnaire CV)** : lister **chaque collaborateur écarté en amont du matching** (issu de `cv-eligibilite`) en distinguant les deux sous-états `exclu` / `a_verifier`, chacun avec ses **raisons par axe** (`{axe, detail}`). Catégories, sous-états et axes définis une seule fois dans le protocole `governance-security` (§ Catégories décisionnelles — non-retenus & exclus). Cette section est **obligatoire** dans le rapport final, même si aucun collaborateur n'est concerné (indiquer alors « aucun »).
- **Pour un AO gouvernemental : section « Exclus — non-conformité études »** listant les collaborateurs **exclus pour non-conformité du niveau d'études** (`recommandation = "exclu"`), avec le **motif d'exclusion**. Mention **obligatoire** et **distincte** de la section « Collaborateurs non retenus » ci-dessus (voir `governance-security`, même section).
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
