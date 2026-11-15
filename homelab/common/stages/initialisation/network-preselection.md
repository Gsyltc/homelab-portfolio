---
slug: network-preselection
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
produces: [traefik_network_preselectionne]
consumes: [{artifact: detection_stack_existante_vs_nouvelle, required: true}, {artifact: lien_documentation_officielle, required: true}]
requires_stage: [database-preselection]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Stack détectée + documentation officielle (lue à l'étape 3 de l'amorçage)"
outputs: "Réseau Traefik recommandé + justification"
---

# Pré-sélection du réseau Traefik

## Objectif

Recommander le réseau Traefik, pour que l'humain le valide au gate léger.

## Steps

### Step 1 — Stack existante

Si `stack-detection` a trouvé la stack, consigner le réseau actuel, lu dans son compose (`traefik.swarm.network`). Fin du stage.

### Step 2 — Nouvelle stack

Choisir dans la liste de la skill `docker-composer` ([`network.md`](../../../../plugins/homelab-assistant/skills/docker-composer/references/network.md), source unique) le réseau correspondant à la nature de l'application : sécurité / authentification, administration, télémétrie, sinon le réseau par défaut (`traefik_frontend`). Consigner la valeur et sa justification. Sans objet si la cible n'est pas Docker Swarm.

## Sensors

Outputs: `traefik_network_preselectionne` consigné sur l'issue et dans la section `reseau` de `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/preselection.json` (format : sensor [`initial-proposal`](../../../sensors/sensors/initial-proposal.md)). Présenté au point 7 de [`intent-scope-approval`](../ideation/intent-scope-approval.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (réseau par famille d'applications) tracés, remontés au gate léger.
