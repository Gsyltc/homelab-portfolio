---
slug: requirements-analysis
phase: inception
execution: ALWAYS
condition: "Always executes — profondeur adaptative"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Architecte cybersécurité]
mode: subagent
summary_confirmation: required
reviewer: Architecture Solution & Intégration
review_class: granular
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

## Gate / sortie
Besoins retenus documentés sur l'issue. Sensor `upstream-coverage` à l'écriture.
