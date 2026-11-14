---
slug: database-preselection
phase: initialisation
execution: ALWAYS
condition: "Always executes pour une demande de stack"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [database_service_preselectionne]
consumes: [{artifact: detection_stack_existante_vs_nouvelle, required: true}, {artifact: lien_documentation_officielle, required: true}]
requires_stage: [auth-preselection]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Stack détectée + documentation officielle (lue à l'étape 3 de l'amorçage)"
outputs: "Base de données recommandée + justification"
---

# Pré-sélection de la base de données

## Objectif

Recommander le service de base de données, pour que l'humain le valide au gate léger.

## Steps

### Step 1 — Stack existante

Si `stack-detection` a trouvé la stack, consigner la base actuelle, lue dans sa configuration. Fin du stage.

### Step 2 — Nouvelle stack

Lire dans la documentation officielle les moteurs supportés (`postgres`, `mysql`, `mariadb`, `mongodb`, ou aucun). Recommander :

1. `postgres` si supporté : PostgreSQL mutualisé du Homelab, jamais recréé (règle de la skill `docker-composer`) ;
2. sinon le moteur exigé par la documentation ;
3. `none` si l'application n'utilise pas de base.

Consigner la valeur recommandée et sa justification (lien vers la section de la doc). En cas de doute, lister les options : l'humain tranche au gate léger.

## Sensors

Outputs: `database_service_preselectionne` consigné sur l'issue et dans la section `database` de `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/preselection.json` (format : sensor [`initial-proposal`](../../../sensors/sensors/initial-proposal.md)). Sans objet (ex. `infra-terraform`) : `sans_objet` + raison. Présenté au point 6 de [`intent-scope-approval`](../ideation/intent-scope-approval.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (moteurs de base par famille d'applications) tracés, remontés au gate léger.
