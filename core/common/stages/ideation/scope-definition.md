---
slug: scope-definition
phase: ideation
execution: ALWAYS
condition: "Always executes — scope auto-détecté puis confirmé"
lead_agent: Architecture Solution & Intégration
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [scope_propose, axes_proposes]
consumes: [{artifact: intention_capturee, required: true}, {artifact: faisabilite_contraintes_evaluees, required: false}]
requires_stage: [intent-capture]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Intention capturée + contraintes"
outputs: "Scope auto-détecté proposé + axes (Depth / vérification) par défaut"
---

# Définition de périmètre (scope)

## Objectif
Auto-détecter le scope et proposer ses axes par défaut, sans démarrage silencieux.

## Steps
### Step 1 — Auto-détecter le scope
Détecter le scope depuis l'intention (mots-clés FR / EN, règle de désambiguïsation) — voir [`../../protocols/scopes-and-axes.md`](../../protocols/scopes-and-axes.md). Jamais de démarrage silencieux sur un scope déduit.

### Step 2 — Proposer scope + axes
Proposer le scope et ses **axes par défaut** (Depth / niveau de vérification) à la confirmation humaine (au stage `intent-scope-approval`).

## Gate / sortie
Scope + axes proposés. Le garde-fou sécurité s'applique : auto-détection = plancher, jamais plafond.
