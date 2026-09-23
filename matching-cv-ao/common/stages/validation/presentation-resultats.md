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
Présenter chaque profil à l'humain pour validation granulaire (Keep/Modify/Redo par profil). **Gate humaine granulaire** : la présentation Markdown reste **DÉTAILLÉE, profil par profil** — l'humain lit le détail complet de chaque profil pour décider, pas un simple pointeur vers le JSON. Le JSON joint `classement-final` reste la source/piste d'audit.

> **Présentation détaillée (exigence humaine).** La réduction de prose vaut pour les échanges A2A (JSON joint), **pas** pour la présentation à l'humain aux gates. Le détail par critère, la recommandation et la justification sont **repris en clair** pour chaque profil.

## Steps
### Step 1 — Présentation profil par profil (DÉTAILLÉE)
Pour chaque profil (dans l'ordre du classement `classement-final`), présenter en Markdown, **en clair**, le détail utile à la décision : **nom**, **score total**, **détail par critère** (compétences, expérience, études, disponibilité), **recommandation**, **justification**, et — pour un AO gouvernemental — le **statut de conformité des études** (et le motif si `exclu`). Terminer chaque profil par la **décision demandée** : ✅ Keep / 💬 Modify / ❌ Redo. Le JSON joint `classement-final` reste la source ; la présentation à l'humain le **reprend en clair**, elle ne se limite pas à le pointer.

### Step 2 — Traitement des Modify/Redo
Sur Modify : ajuster et re-présenter **cet élément uniquement** (avec le même niveau de détail).
Sur Redo : proposer une alternative et relancer **cet élément uniquement** (présentation détaillée).
Ne jamais avancer sur un profil non validé.

### Step 3 — Synthèse des validations (piste d'audit)
Consigner sur l'issue l'artefact **JSON joint** `resultats-valides` (profils validés / rejetés / modifiés) et poster un commentaire **minimal** le référençant.

## Sensors
Outputs: `resultats-valides` → Phase Validation (gate: granular).
Imports: none.

## Learn
Documenter sur l'issue chaque validation/rejet par profil. Consigner les candidats-règles.
