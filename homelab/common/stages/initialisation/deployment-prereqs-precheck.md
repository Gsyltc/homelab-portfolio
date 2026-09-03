---
slug: deployment-prereqs-precheck
phase: initialisation
execution: ALWAYS
condition: "Always executes — rappel advisory anticipé (le contrôle bloquant reste en Validation §4.0)"
lead_agent: null
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [prerequis_deploiement_anticipes]
consumes: []
requires_stage: [concurrency-lock-read]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Contexte de la stack et de l'environnement du Tech Lead"
outputs: "Rappel advisory anticipé : [répertoire de travail] défini ? flux Kestra accessible ?"
---

# Vérification anticipée des prérequis de déploiement

## Objectif

Signaler tôt un prérequis de déploiement manquant, sans en faire ici le contrôle bloquant.

## Steps

### Step 1 — Rappel advisory anticipé

Rappel **advisory anticipé** des prérequis de la Validation (`deployment-prereqs-check`) : présence de la variable `[répertoire de travail]` du Tech Lead et accessibilité du flux Kestra `configure_service`.

### Step 2 — Signaler tôt, ne pas bloquer

Un prérequis manquant est **signalé tôt** (pour ne pas engager un cadrage qui échouera au dépôt), mais **n'est pas** ici le contrôle bloquant : le stage `deployment-prereqs-check` (entrée de Validation) reste le contrôle bloquant de référence.

## Sensors

Outputs: rappel advisory consigné. Aucun gate humain (bootstrap déterministe). C'est le pendant anticipé du gate `phase3-phase4` de [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : tenir le journal des candidats-règles sur l'issue. Stage d'Initialisation → **saute** l'interaction liée au gate humain.
