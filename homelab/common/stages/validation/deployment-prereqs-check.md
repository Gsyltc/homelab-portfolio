---
slug: deployment-prereqs-check
phase: validation
execution: ALWAYS
condition: "Always executes en premier en Validation — contrôle bloquant de référence"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [prerequis_deploiement_verifies]
consumes: [{artifact: controle_qualite_central_go, required: true}]
requires_stage: [central-quality-control]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Livrables contrôlés"
outputs: "Prérequis de dépôt / déploiement vérifiés (bloquant si manquant)"
---

# Vérification des prérequis de déploiement (bloquant, avant toute action de Validation)

## Objectif

Garantir que le dépôt et le déploiement sont possibles avant toute action à impact.

## Steps

### Step 1 — Variable de dépôt (bloquant)

Confirmer que la variable `[répertoire de travail]` du Tech Lead est **définie et non vide**. Si absente → **ne pas** tenter le dépôt, passer l'issue en `blocked` et signaler à l'humain : « Variable d'environnement du répertoire de travail non définie : impossible de calculer les chemins de dépôt. Merci de la renseigner avant déploiement. »

### Step 2 — Accessibilité du flux Kestra

Confirmer que le flux Kestra `configure_service` est **accessible** avant d'envisager le déploiement ([`kestra-deployment.md`](kestra-deployment.md)). S'il est injoignable → le signaler explicitement à l'humain, ne pas promettre de déploiement automatique, proposer le dépôt manuel comme repli.

## Sensors

Outputs: prérequis vérifiés. Ce contrôle est le **contrôle bloquant de référence** ; il est anticipé en advisory dès la Phase 0 ([`../initialisation/deployment-prereqs-precheck.md`](../initialisation/deployment-prereqs-precheck.md)) et au gate `phase3-phase4` de [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (prérequis d'environnement récurrents) tracés, remontés au gate explicite d'Operation.
