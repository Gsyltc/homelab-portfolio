---
slug: deployment-under-validation
phase: operation
execution: CONDITIONAL
condition: "Exécuté si le travail comporte un déploiement / une administration ; sinon N/A"
lead_agent: Admin
support_agents: [Florian, Sylvain]
mode: subagent
summary_confirmation: required
reviewer: Xavier
review_class: explicit
human_gate: explicit
produces: [plan_ou_configuration_valide, rollback_si_action_destructive]
consumes: [{artifact: livrables_valides_mis_a_disposition, required: true}]
requires_stage: [consolidation-handoff]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, express, enterprise]
inputs: "Livrables validés"
outputs: "Plan / configuration validé explicitement par l'humain ; plan de rollback si action destructive"
---

# Déploiement / administration sous validation humaine

## Objectif
Déployer ou administrer uniquement sous validation humaine explicite, avec rollback si destructif.

## Steps
### Step 1 — Soumettre le plan complet à l'humain pour **validation explicite**.

### Step 2 — Plan de rollback (conditionnel)
Pour toute action destructive ou de migration (Admin Windows), publier un **plan de rollback détaillé** et le faire **valider par l'humain avant exécution**.

### Step 3 — Garde-fou
**Aucune action à impact (déploiement, migration, orchestration) sans validation humaine explicite.** Jamais autonome.

## Gate / sortie
Plan / configuration validé (+ rollback conditionnel). Frontière **Operation → Fin** : gate `artefacts-presents` (plan, rollback conditionnel).
