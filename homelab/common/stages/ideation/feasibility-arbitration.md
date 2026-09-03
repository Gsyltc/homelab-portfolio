---
slug: feasibility-arbitration
phase: ideation
execution: ALWAYS
condition: "Always executes — arbitrage Swarm/Proxmox amorcé (affiné en Cadrage)"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: optional
reviewer: null
review_class: none
human_gate: none
produces: [faisabilite_evaluee, arbitrage_swarm_proxmox_amorce]
consumes: [{artifact: intention_capturee, required: true}]
requires_stage: [intent-capture]
sensors: []
scopes: [stack-update, new-stack, security-patch, infra-terraform]
inputs: "Intention capturée"
outputs: "Faisabilité évaluée + arbitrage Docker Swarm / Proxmox amorcé"
---

# Faisabilité et arbitrage Swarm / Proxmox (amorce)

## Objectif

Vérifier que la stack est déployable dans le Homelab et amorcer l'arbitrage Swarm / Proxmox.

## Steps

### Step 1 — Faisabilité / contraintes

La stack est-elle déployable dans le Homelab (existence d'images Docker, alternative Proxmox sur `https://community-scripts.org/`) ?

### Step 2 — Arbitrage Docker Swarm vs Proxmox (amorce)

Arbitrage **amorcé** ici : si les deux existent, la question est **posée à l'humain** (affinée dans [`../cadrage/swarm-proxmox-arbitration.md`](../cadrage/swarm-proxmox-arbitration.md)). Ne jamais présumer le choix.

## Sensors

Outputs: faisabilité + arbitrage amorcé consignés. Aucun gate humain à ce stage.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de faisabilité, patterns Swarm/Proxmox récurrents) tracés, remontés au gate léger.
