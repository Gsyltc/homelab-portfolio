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
consumes: [{artifact: controle_qualite_central_go, required: true}, {artifact: controle_securite_posture, required: false}]
requires_stage: [central-quality-control, security-delegation]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Livrables contrôlés (QA, contrôle central) + revue sécurité close"
outputs: "Prérequis de dépôt vérifiés (bloquant si manquant)"
---

# Vérification des prérequis de dépôt (bloquant, avant toute action de Validation)

## Objectif

Garantir que le dépôt des fichiers est possible avant toute action à impact. L'accès Kestra est vérifié au déploiement ([`kestra-deployment`](kestra-deployment.md) Step 2), pas ici.

## Steps

### Step 1 — Variable de dépôt (bloquant)

Confirmer que la variable `[répertoire de travail]` du Tech Lead est **définie et non vide**. Si absente → **ne pas** tenter le dépôt, passer l'issue en `blocked` et signaler à l'humain : « Variable d'environnement du répertoire de travail non définie : impossible de calculer les chemins de dépôt. Merci de la renseigner avant déploiement. »

## Sensors

Outputs: prérequis vérifiés. Ce contrôle est le **contrôle bloquant de référence** ; il est anticipé en advisory au gate `phase3-phase4` de [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (prérequis d'environnement récurrents) tracés, remontés au gate explicite d'Operation.
