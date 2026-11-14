---
slug: feasibility-arbitration
phase: ideation
execution: ALWAYS
condition: "Always executes — faisabilité + recherche Helper-Scripts"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: optional
reviewer: null
review_class: none
human_gate: none
produces: [faisabilite_evaluee, recherche_helper_scripts]
consumes: [{artifact: intention_capturee, required: true}, {artifact: scope_propose, required: true}]
requires_stage: [scope-detection]
sensors: []
scopes: [stack-update, new-stack, security-patch, infra-terraform]
inputs: "Intention capturée + scope proposé"
outputs: "Faisabilité évaluée + recherche Helper-Scripts consignée"
---

# Faisabilité et recherche Helper-Scripts

## Objectif

Vérifier que la stack est déployable dans le Homelab et consigner la recherche Helper-Scripts.

## Steps

### Step 1 — Faisabilité

Existence d'images Docker, alternative Proxmox.

### Step 2 — Recherche Helper-Scripts (obligatoire, source unique)

Si le scope proposé (`scope-detection`) est `new-stack` / `infra-terraform`, **avant le gate `intent-scope-approval` et tout le Cadrage** : chercher sur `https://community-scripts.org/`, puis par recherche web. Consigner sur l'issue le lien, ou « aucun script trouvé » (`recherche_helper_scripts`). Si le gate léger relève ensuite le scope vers l'un d'eux, la recherche est faite avant de passer en Cadrage. Le choix Swarm / Proxmox n'est **pas** fait ici : voir [`swarm-proxmox-arbitration`](../cadrage/swarm-proxmox-arbitration.md).

## Sensors

Outputs: faisabilité + recherche consignées. Frontière Idéation → Cadrage : `recherche_helper_scripts` bloquant (voir [`gates.md`](../../../sensors/gates.md)). Aucun gate humain à ce stage.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de faisabilité, patterns Swarm/Proxmox récurrents) tracés, remontés au gate léger.
