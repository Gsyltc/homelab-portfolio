---
slug: classement-profils
phase: matching
execution: ALWAYS
condition: "Always executes"
lead_agent: Coordinateur Matching
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
review_artifact: ""
human_gate: none
produces: [classement-final]
consumes: [{artifact: matching-resultats, required: true}, {artifact: cv-eligibilite, required: true}]
requires_stage: [croisement-profils]
sensors: []
scopes: [standard, complex, express]
inputs: "Résultats de matching (scores)"
outputs: "Classement final avec recommandations"
---

# Classement des profils

## Objectif
Produire le classement final des profils et préparer la présentation pour validation humaine granulaire.

## Steps
### Step 1 — Agrégation et tri
Agrégérer les résultats de matching, trier par score décroissant, grouper par recommandation (recommandé / possible / déconseillé). Produire **deux sections d'écartement distinctes**, définies une seule fois dans le protocole `governance-security` (§ Catégories décisionnelles — non-retenus & exclus) :

- **« Exclus — non-conformité études (Matcher) »** — profils `exclu` pour non-conformité du niveau d'études (AO gouvernemental) **sortis du classement principal**, avec pour chacun le `motif_exclusion` (niveau requis vs niveau du collaborateur, équivalence MIFI, compensation appliquée le cas échéant).
- **« Non retenus (Gestionnaire CV) »** — non-retenus du filtre d'éligibilité amont (`cv-eligibilite`, **jamais scorés**), en deux sous-listes `exclu` / `a_verifier`, chacune avec ses **raisons par axe** (`{axe, detail}`) ; ne rien inventer.

### Step 2 — Préparation de la présentation
Pour chaque profil, structurer dans l'artefact **JSON joint** `classement-final` : nom, score total, détail par critère, recommandation, justification, et — pour un AO gouvernemental — le **statut de conformité des études** (`conformite_etudes.conforme`) et, si `conforme = "non"`, le **motif d'exclusion**. **Pas de Markdown ici** : le classement est un artefact A2A ; sa **restitution lisible et détaillée à l'humain** intervient à la gate du stage `presentation-resultats` (présentation profil par profil détaillée).

### Step 3 — Confirmation de résumé (piste d'audit)
Joindre l'artefact `classement-final` (JSON) à l'issue via `multica attachment` et poster un commentaire **minimal** le référençant. Ce stage est `inline` (pas de délégation, pas de mention A2A) ; la confirmation avant validation granulaire est portée par la gate humaine du stage suivant, **sans récap Markdown ici**.

## Sensors
Outputs: `classement-final` → transmis directement à la Phase 3 (`presentation-resultats`), sans gate humaine à cette frontière.
Imports: none.

## Learn
Journaliser le classement sur l'issue.
