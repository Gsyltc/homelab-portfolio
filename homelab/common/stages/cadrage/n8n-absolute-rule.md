---
slug: n8n-absolute-rule
phase: cadrage
execution: ALWAYS
condition: "Always executes en premier — déclenche la branche n8n si un déclencheur n8n est présent"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [routage_n8n_decide]
consumes: [{artifact: intention_perimetre_approuves, required: true}]
requires_stage: [intent-scope-approval]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Demande, titre d'issue, références de flux"
outputs: "Décision de routage : délégation immédiate à l'Expert n8n, ou poursuite du flux stack"
---

# Règle absolue n8n (TOUJOURS EN PREMIER)

## Objectif

Router immédiatement toute demande n8n vers l'Expert n8n, sans aucune exception.

## Steps

### Step 1 — Détecter n8n

Si la demande concerne n8n (mot « n8n » dans la demande, un titre d'issue ou une référence de flux).

### Step 2 — Déléguer immédiatement et arrêter le flux stack

→ **déléguer IMMÉDIATEMENT à l'Expert n8n** (voir [`../production/n8n-branch.md`](../production/n8n-branch.md)) par mention valide `[@Label](mention://agent/<uuid>)`, avec mission claire, et **arrêter** ce flux. **Aucune exception, pas même l'analyse.** C'est un invariant non contournable (voir [`../../protocols/governance-security.md`](../../protocols/governance-security.md)).

## Sensors

Outputs: décision de routage consignée. Aucun gate humain (règle déterministe).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : la règle absolue n8n est un **invariant** — aucune règle apprise ne peut la lever (SEC-1).
