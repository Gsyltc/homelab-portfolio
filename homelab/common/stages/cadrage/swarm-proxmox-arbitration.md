---
slug: swarm-proxmox-arbitration
phase: cadrage
execution: CONDITIONAL
condition: "Création / modification de stack où Docker Swarm ET Proxmox sont possibles"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [arbitrage_swarm_proxmox]
consumes: [{artifact: cadrage_confirme, required: true}, {artifact: arbitrage_swarm_proxmox_amorce, required: false}]
requires_stage: [intake-framing]
sensors: []
scopes: [stack-update, new-stack, security-patch, infra-terraform]
inputs: "Cadrage confirmé + arbitrage amorcé en Idéation"
outputs: "Choix Docker Swarm / Proxmox arbitré par l'humain (si les deux existent)"
---

# Vérifications préalables et arbitrage Swarm / Proxmox

## Objectif

Trancher entre Docker Swarm et Proxmox lorsque les deux sont possibles.

## Steps

### Step 1 — Vérifier les images et alternatives

Confirmer que les images Docker nécessaires existent **et** chercher une alternative Proxmox sur `https://community-scripts.org/`.

### Step 2 — Arbitrer avec l'humain

Si les **deux** existent → demander à l'humain de choisir **Docker Swarm** ou **Proxmox** et **attendre** sa réponse avant toute suite. Ne jamais présumer le choix.

## Sensors

Outputs: choix Swarm / Proxmox consigné. Frontière **Cadrage → Production** : artefact `arbitrage_swarm_proxmox` (conditionnel) contrôlé par le gate — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (préférences Swarm / Proxmox par type de stack) tracés, remontés au gate granulaire.
