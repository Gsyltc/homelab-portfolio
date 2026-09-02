---
slug: intent-scope-approval
phase: ideation
execution: ALWAYS
condition: "Always executes — gate humain léger"
lead_agent: Architecture Solution & Intégration
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: light
produces: [intention_perimetre_approuves]
consumes: [{artifact: intention_capturee, required: true}, {artifact: scope_propose, required: true}, {artifact: axes_proposes, required: true}]
requires_stage: [scope-definition]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Intention reformulée, scope + axes proposés"
outputs: "Intention + périmètre approuvés par l'humain (gate léger)"
---

# Approbation de l'intention et du périmètre (gate humain léger)

## Objectif
Valider *qu'on part dans la bonne direction*, avant d'engager la conception détaillée.

## Steps
### Step 1 — Présenter à l'humain
Présenter : l'**intention** reformulée, le **scope** proposé, ses **axes** (Depth / vérification).

### Step 2 — Gate léger (Keep / Modify / Redo)
L'humain approuve ou ajuste. C'est un gate **léger** : il ne valide pas encore les décisions d'architecture (celles-ci sont validées granulairement en Inception). Rien n'engage l'Inception tant que l'intention et le périmètre ne sont pas approuvés.

## Gate / sortie
Intention + périmètre approuvés. Frontière **Ideation → Inception** : verification gate `artefacts-presents` (intention, scope) + approbation périmètre tracée.
