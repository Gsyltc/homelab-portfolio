---
slug: closure
phase: validation
execution: ALWAYS
condition: "Always executes — clôture après validation humaine"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [issue_close]
consumes: [{artifact: validation_humaine_explicite, required: true}, {artifact: depot_fichiers_confirme, required: false}, {artifact: deploiement_kestra_si_demande, required: false}]
requires_stage: [file-deposit]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Validation humaine + dépôt / déploiement"
outputs: "Issue passée à Done, récapitulatif des livrables et emplacements"
---

# Clôture

## Objectif

Clore l'issue uniquement après la validation humaine, avec récapitulatif.

## Steps

### Step 1 — Passer à Done après validation humaine

Passer l'issue à **Done** **uniquement** après la validation humaine, avec le récapitulatif des livrables et leur emplacement. `Done` reste une décision humaine.

## Sensors

Outputs: issue close + récapitulatif. Frontière **Validation → Clôture** : gate `artefacts-presents` (validation explicite, dépôt confirmé, déploiement si demandé) + sensor `vault-secret-exists` — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : bilan des candidats-règles du workflow ; persistance des apprentissages **confirmés** dans `homelab/rules/` (application au prochain workflow, jamais au run courant).
