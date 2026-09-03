---
slug: deployment-under-validation
phase: operation
execution: CONDITIONAL
condition: "Exécuté si le travail comporte un déploiement / une administration ; sinon N/A"
lead_agent: Administrateur infrastructure Windows
support_agents: [Architecte AWS, Architecture Solution & Intégration]
mode: subagent
summary_confirmation: required
reviewer: Reviewer de sécurité
review_class: adversarial
review_artifact: plan-deploiement.md
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

### Step 1 — Soumettre le plan complet à l'humain pour **validation explicite**

### Step 2 — Contrôle sécurité adversarial

Le coordinateur sollicite le **Reviewer de sécurité** sur le plan de déploiement / administration (surface à impact) ; revue **adversariale, non substituable** (plancher SG-3), intégrée **avant** la validation humaine explicite.

### Step 3 — Plan de rollback (conditionnel)

Pour toute action destructive ou de migration (Administrateur infrastructure Windows), publier un **plan de rollback détaillé** et le faire **valider par l'humain avant exécution**.

### Step 4 — Garde-fou

**Aucune action à impact (déploiement, migration, orchestration) sans validation humaine explicite.** Jamais autonome.

## Sensors

Outputs: plan / configuration validé (+ rollback conditionnel). Frontière **Operation → Fin** : gate `artefacts-presents` (plan, rollback conditionnel).
Imports: none.
Review artifact: `plan-deploiement.md` porte la section `## Review` ajoutée par le Reviewer de sécurité.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de déploiement, patterns de rollback récurrents) ; les remonter au **gate humain explicite** d'Operation ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
