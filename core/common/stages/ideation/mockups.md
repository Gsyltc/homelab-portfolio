---
slug: mockups
phase: ideation
execution: CONDITIONAL
condition: "UI uniquement — N/A pour les travaux d'architecture / infrastructure sans UI (cas majoritaire)"
lead_agent: Architecte de solution
support_agents: []
mode: subagent
summary_confirmation: optional
reviewer: Reviewer de cohérence
review_class: advisory
review_artifact: maquettes.md
human_gate: none
produces: [maquettes]
consumes: [{artifact: intention_capturee, required: true}]
requires_stage: [intent-capture]
sensors: []
scopes: [standard, feature, mvp, enterprise]
inputs: "Intention comportant une interface utilisateur"
outputs: "Maquettes / wireframes légers (ou N/A)"
---

# Maquettes / wireframes (conditionnel — UI uniquement)

## Objectif
Produire ou référencer des maquettes légères si le travail comporte une UI.

## Steps
### Step 1 — Déterminer l'applicabilité
Si le travail comporte une interface utilisateur → produire ou référencer des maquettes légères (déléguées à l'Architecte de solution en `subagent`). Sinon → **marquer N/A** (cas majoritaire du workspace, orienté architecture / infrastructure).

### Step 2 — Revue de cohérence (advisory)
Une fois les maquettes produites, le coordinateur sollicite le **Reviewer de cohérence** (mention A2A, UUID résolu) ; son verdict est **consultatif** (cohérence intention ↔ maquettes, conventions) et n'engage pas de gate. Revue **sautée** si N/A.

## Sensors
Outputs: maquettes légères (ou N/A consigné). Aucune production détaillée ni décision structurante à ce stade.
Review artifact: `maquettes.md` porte la section `## Review` ajoutée par le Reviewer de cohérence.
Imports: none.

## Learn
Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (conventions de maquettage récurrentes) ; les remonter au **gate humain** léger d'Ideation ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit. Divergence tracée vs un journal `memory.md` externe (voir [ADR-0009](../../../../decisions/0009-alignement-fiches-de-stage-sur-ai-dlc.md)).
