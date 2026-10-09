---
slug: deployment-under-validation
phase: operation
execution: CONDITIONAL
condition: "Exécuté si le travail comporte un déploiement / une administration ; sinon N/A"
lead_agent: Infrastructure Windows
support_agents: [Architecte AWS, Architecture Solution & Intégration, OpenSpec Expert]
mode: subagent
summary_confirmation: required
reviewer: Reviewer de sécurité
review_class: adversarial
review_artifact: plan-deploiement.md
human_gate: explicit
produces: [plan_ou_configuration_valide, rollback_si_action_destructive, archivage_openspec_si_active]
consumes: [{artifact: livrables_valides_mis_a_disposition, required: true}]
requires_stage: [delivery-handoff]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, express, enterprise]
inputs: "Livrables validés"
outputs: "Plan / configuration validé explicitement par l'humain ; plan de rollback si action destructive ; archivage OpenSpec effectué après déploiement si le projet applique OpenSpec"
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

### Step 5 — Archivage OpenSpec post-déploiement (conditionnel)

> **Exécuté uniquement si le projet applique OpenSpec** (`OpenSpec : Oui`) **et** après que le changement a été **réellement implémenté ET déployé** (déploiement validé par l'humain, Steps 1-4). C'est le découplage approbation ≠ archivage : l'approbation de la spec (achevée en Construction, [`../construction/consolidation-handoff.md`](../construction/consolidation-handoff.md), Step 2) **n'a rien archivé** ; l'archivage n'a lieu qu'ici.

Une fois le déploiement effectif et validé, le coordinateur sollicite l'**OpenSpec Expert** (délégué en `subagent`). Celui-ci **vérifie les préconditions** (implémentation et déploiement effectifs), puis **archive le changement** : fusion des deltas dans les specs vivantes (`openspec/specs/<capability>/spec.md`) et déplacement du change vers `openspec/changes/archive/AAAA-MM-JJ-<nom>/` ([`../../../agents/openspec-agent.md`](../../../agents/openspec-agent.md), « Archivage post-déploiement »). Il remonte le résultat sur l'issue. Si le projet n'applique pas OpenSpec, ce step est N/A.

## Sensors

Outputs: plan / configuration validé (+ rollback conditionnel ; archivage OpenSpec post-déploiement si le projet applique OpenSpec). Frontière **Operation → Fin** : gate `artefacts-presents` (plan, rollback conditionnel).
Imports: none.
Review artifact: `plan-deploiement.md` porte la section `## Review` ajoutée par le Reviewer de sécurité.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de déploiement, patterns de rollback récurrents) ; les remonter au **gate humain explicite** d'Operation ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
