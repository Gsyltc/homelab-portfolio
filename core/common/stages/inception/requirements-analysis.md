---
slug: requirements-analysis
phase: inception
execution: ALWAYS
condition: "Always executes — profondeur adaptative"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Architecte Cybersécurité]
mode: subagent
summary_confirmation: required
reviewer: Reviewer de cohérence
review_class: advisory
review_artifact: besoins.md
human_gate: none
produces: [besoins_traces]
consumes: [{artifact: cadrage_confirme, required: true}, {artifact: synthese_contexte_existant, required: false}]
requires_stage: [intake-framing]
sensors: [upstream-coverage]
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Cadrage confirmé + contexte existant éventuel"
outputs: "Besoins fonctionnels et non fonctionnels tracés (profondeur selon Depth)"
---

# Analyse des besoins (profondeur adaptative)

## Objectif
Recueillir les besoins au niveau de détail dicté par l'axe Depth.

## Steps
### Step 1 — Profondeur adaptative
- **Minimale** : demande simple et claire — documenter l'analyse d'intention.
- **Standard** : besoins fonctionnels et non fonctionnels (performance, sécurité, scalabilité, portabilité, maintenabilité).
- **Complète** : haut risque — besoins détaillés avec traçabilité.

### Step 2 — Renforcement sécurité conditionnel
`security-patch` → couvrir a minima l'**analyse d'impact du correctif** (surface, effets de bord, non-régression). `enterprise` → **classification des données** + point de contrôle « applicabilité des normes ». Voir [`../../protocols/governance-security.md`](../../protocols/governance-security.md).

### Step 3 — Revue de cohérence (advisory)
Le coordinateur sollicite le **Reviewer de cohérence** (mention A2A, UUID résolu) à réception des besoins tracés ; verdict **consultatif** (complétude, cohérence avec le cadrage, conventions), demande de correction éventuelle avant le gate humain.

## Sensors
Outputs: besoins retenus documentés sur l'issue.
Imports: `upstream-coverage`.
Upstream targets: `cadrage_confirme` (required), `synthese_contexte_existant` (optionnel) — couverture amont vérifiée à l'écriture des besoins.
Review artifact: `besoins.md` porte la section `## Review` ajoutée par le Reviewer de cohérence.

## Learn
Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de besoins, seuils de profondeur, renforcements sécurité récurrents) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit. Divergence tracée vs un journal `memory.md` externe (voir [ADR-0009](../../../../decisions/0009-alignement-fiches-de-stage-sur-ai-dlc.md)).
