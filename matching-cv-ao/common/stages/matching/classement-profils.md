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
human_gate: light
produces: [classement-final]
consumes: [{artifact: matching-resultats, required: true}]
requires_stage: [croisement-profils]
sensors: []
scopes: [standard]
inputs: "Résultats de matching (scores)"
outputs: "Classement final avec recommandations"
---

# Classement des profils

## Objectif
Produire le classement final des profils et préparer la présentation pour validation humaine granulaire.

## Steps
### Step 1 — Agrégation et tri
Agrégérer les résultats de matching, trier par score décroissant, grouper par recommandation (recommandé / possible / déconseillé). **Les profils `exclu`** (non-conformité du niveau d'études sur AO gouvernemental) **sont sortis du classement principal** et regroupés dans une section dédiée « **Exclus — non-conformité études (gouvernemental)** » indiquant, pour chacun, le `motif_exclusion` (niveau requis vs niveau du collaborateur, équivalence MIFI, compensation appliquée le cas échéant).

### Step 2 — Préparation de la présentation
Pour chaque profil, préparer : nom, score total, détail par critère, recommandation, justification, et — pour un AO gouvernemental — le **statut de conformité des études** (`conformite_etudes.conforme`) et, si `conforme = "non"`, le **motif d'exclusion**. Format Markdown pour l'humain.

### Step 3 — Confirmation de résumé
Poster un résumé sur l'issue demandant confirmation avant de passer à la validation granulaire.

## Sensors
Outputs: `classement-final` → Phase Matching (gate: light).
Imports: none.

## Learn
Journaliser le classement sur l'issue.
