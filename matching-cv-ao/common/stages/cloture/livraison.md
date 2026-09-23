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
outputs: "Livrable final (artefact JSON joint `livraison-finale`) + présentation finale Markdown DÉTAILLÉE à l'humain"
---

# Livraison

## Objectif
Produire et livrer le résumé final du matching à l'humain. **Gate `explicit`** : le livrable structuré est un **artefact JSON joint** `livraison-finale` (source machine / piste d'audit), mais la **présentation finale à l'humain reste TRÈS DÉTAILLÉE en Markdown** — l'humain lit un rapport complet et lisible, jamais du JSON brut ni un simple pointeur vers le fichier.

> **Présentation finale = détaillée (exigence humaine, non négociable).** La réduction de prose du workflow vaut pour les **échanges A2A** (agent↔agent, portés par JSON joint) ; elle **ne s'applique pas** à la présentation finale à l'humain. Le récap de livraison doit **reprendre en clair** l'ensemble du contenu du livrable (résumé AO, profils retenus avec scores et justification détaillée, non-retenus et exclusions avec motifs, grille, recommandations), pas seulement l'action « valider ».

## Steps
### Step 1 — Production du livrable final (JSON joint)
Produire l'artefact **JSON joint** `livraison-finale` (via `multica attachment`) contenant :
- Résumé de l'AO analysée
- Liste des profils retenus avec scores et justification
- **Section obligatoire « collaborateurs non retenus » (filtre d'éligibilité Gestionnaire CV)** : **chaque collaborateur écarté en amont du matching** (issu de `cv-eligibilite`) en distinguant les deux sous-états `exclu` / `a_verifier`, chacun avec ses **raisons par axe** (`{axe, detail}`). Catégories, sous-états et axes définis une seule fois dans le protocole `governance-security` (§ Catégories décisionnelles — non-retenus & exclus). **Obligatoire**, même si aucun collaborateur n'est concerné (indiquer alors « aucun »).
- **Pour un AO gouvernemental : bloc « exclus — non-conformité études »** listant les collaborateurs **exclus pour non-conformité du niveau d'études** (`recommandation = "exclu"`), avec le **motif d'exclusion**. **Obligatoire** et **distinct** de la section « collaborateurs non retenus » ci-dessus (voir `governance-security`, même section).
- Grille remplie (si disponible)
- Recommandations

### Step 2 — Présentation finale DÉTAILLÉE + validation explicite
Présenter à l'humain une **présentation finale Markdown détaillée et lisible** reprenant l'intégralité du contenu du livrable (le JSON joint `livraison-finale` reste la source/piste d'audit) :
- **Résumé de l'AO analysée** (client, objet, exigences clés, profils recherchés).
- **Profils retenus** — pour **chaque** profil : nom, **score total**, **détail par critère** (compétences 50 %, expérience 35 %, études 10 %, disponibilité 5 %), **recommandation** et **justification**.
- **Collaborateurs non retenus** (filtre d'éligibilité Gestionnaire CV) — sous-états `exclu` / `a_verifier` avec **raisons par axe** (`{axe, detail}`).
- **Pour un AO gouvernemental** : bloc **« exclus — non-conformité études »** avec le **motif d'exclusion** par collaborateur.
- **Grille remplie** (si disponible) et **recommandations**.

Terminer par la **demande de validation explicite** (mention de l'humain + « valider la livraison »). Le détail ci-dessus est présenté **en clair dans le commentaire**, pas seulement pointé. Sur approbation, marquer la livraison comme terminée.

### Step 3 — Notification
Si demandé, envoyer une notification ntfy à l'humain.

## Sensors
Outputs: `livraison-finale` → Phase Clôture (gate: explicit).
Imports: none.

## Learn
Documenter sur l'issue la livraison finale et les validations.
