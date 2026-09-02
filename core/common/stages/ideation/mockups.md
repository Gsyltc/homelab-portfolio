---
slug: mockups
phase: ideation
execution: CONDITIONAL
condition: "UI uniquement — N/A pour les travaux d'architecture / infrastructure sans UI (cas majoritaire)"
lead_agent: Manuel
support_agents: []
mode: subagent
summary_confirmation: optional
reviewer: Sylvain
review_class: advisory
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
Si le travail comporte une interface utilisateur → produire ou référencer des maquettes légères (déléguées à Manuel). Sinon → **marquer N/A** (cas majoritaire du workspace, orienté architecture / infrastructure).

## Gate / sortie
Maquettes légères (ou N/A consigné). Aucune production détaillée ni ADR à ce stade.
