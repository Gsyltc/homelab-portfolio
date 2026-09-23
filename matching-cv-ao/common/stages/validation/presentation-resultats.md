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
scopes: [standard, complex, express]
inputs: "Classement final"
outputs: "Profils validés par l'humain"
---

# Présentation des résultats

## Objectif
Présenter chaque profil à l'humain pour validation granulaire (Keep/Modify/Redo par profil). **Gate humaine** : le récap Markdown est **conservé mais limité à l'action** (Keep/Modify/Redo par profil) ; les données détaillées vivent dans le JSON joint `classement-final` (l'humain n'en lit jamais le brut).

## Steps
### Step 1 — Présentation profil par profil (récap limité à l'action)
Pour chaque profil (dans l'ordre du classement `classement-final`), présenter un **récap Markdown minimal** pointant le JSON : nom, score total, et la **décision demandée** — ✅ Keep / 💬 Modify / ❌ Redo. Le détail par critère (compétences, expérience, études, disponibilité), la recommandation et la justification restent dans le JSON joint ; ne pas les recopier en prose au-delà de ce qui éclaire la décision.

### Step 2 — Traitement des Modify/Redo
Sur Modify : ajuster et re-présenter **cet élément uniquement** (récap limité à l'action).
Sur Redo : proposer une alternative et relancer **cet élément uniquement**.
Ne jamais avancer sur un profil non validé.

### Step 3 — Synthèse des validations (piste d'audit)
Consigner sur l'issue l'artefact **JSON joint** `resultats-valides` (profils validés / rejetés / modifiés) et poster un commentaire **minimal** le référençant.

## Sensors
Outputs: `resultats-valides` → Phase Validation (gate: granular).
Imports: none.

## Learn
Documenter sur l'issue chaque validation/rejet par profil. Consigner les candidats-règles.
