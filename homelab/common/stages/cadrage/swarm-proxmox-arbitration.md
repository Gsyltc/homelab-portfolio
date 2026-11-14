---
slug: swarm-proxmox-arbitration
phase: cadrage
execution: CONDITIONAL
condition: "Création / modification de stack"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [arbitrage_swarm_proxmox]
consumes: [{artifact: cadrage_confirme, required: true}, {artifact: recherche_helper_scripts, required: true}]
requires_stage: [intake-framing]
sensors: []
scopes: [stack-update, new-stack, security-patch, infra-terraform]
inputs: "Cadrage confirmé + recherche Helper-Scripts (Idéation)"
outputs: "Choix Docker Swarm / Proxmox arbitré par l'humain (si les deux existent)"
---

# Vérifications préalables et arbitrage Swarm / Proxmox

## Objectif

Trancher entre Docker Swarm et Proxmox lorsque les deux sont possibles.

## Steps

### Step 1 — Lire la recherche

Vérifier que les images Docker existent et lire `recherche_helper_scripts` (produit en Idéation par [`feasibility-arbitration`](../ideation/feasibility-arbitration.md)). **Ne pas la refaire.** Si elle est absente : s'arrêter et exécuter d'abord `feasibility-arbitration`.

### Step 2 — Arbitrer (seul stage qui pose la question)

- Aucun script trouvé → consigner « Docker Swarm retenu, aucune alternative Proxmox ».
- Script trouvé → demander à l'humain **Docker Swarm** ou **Proxmox**, **attendre** sa réponse. Ne jamais présumer.

## Sensors

Outputs: choix Swarm / Proxmox consigné. Frontière **Cadrage → Production** : artefact `arbitrage_swarm_proxmox` (**bloquant** sur `new-stack` / `infra-terraform`) contrôlé par le gate — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (préférences Swarm / Proxmox par type de stack) tracés, remontés au gate granulaire.
