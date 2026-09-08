---
slug: presentation-resultats
phase: validation
execution: ALWAYS
condition: "Always executes"
lead_agent: Coordinateur Matching
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
review_artifact: ""
human_gate: granular
produces: [resultats-valides]
consumes: [{artifact: classement-final, required: true}]
requires_stage: [classement-profils]
sensors: []
scopes: [standard]
inputs: "Classement final"
outputs: "Profils validés par l'humain"
---

# Présentation des résultats

## Objectif
Présenter chaque profil à l'humain pour validation granulaire (Keep/Modify/Redo par profil).

## Steps
### Step 1 — Présentation profil par profil
Pour chaque profil (dans l'ordre du classement), présenter :
- Nom et score total
- Détail par critère (compétences, expérience, études, disponibilité)
- Recommandation et justification

Demander par profil : ✅ Keep / 💬 Modify / ❌ Redo.

### Step 2 — Traitement des Modify/Redo
Sur Modify : ajuster la présentation et re-présenter **cet élément uniquement**.
Sur Redo : proposer une alternative et relancer **cet élément uniquement**.
Ne jamais avancer sur un profil non validé.

### Step 3 — Synthèse des validations
Poster sur l'issue la synthèse : profils validés, profils rejetés, profils modifiés.

## Sensors
Outputs: `resultats-valides` → Phase Validation (gate: granular).
Imports: none.

## Learn
Documenter sur l'issue chaque validation/rejet par profil. Consigner les candidats-règles.
