---
slug: n8n-absolute-rule
phase: cadrage
execution: ALWAYS
condition: "Always executes en premier — déclenche la branche n8n si un déclencheur n8n EXPLICITE est présent"
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
outputs: "Décision de routage : délégation immédiate à l'Expert n8n (n8n explicite), passage au triage de domaine (demande ambiguë hors stack), ou poursuite du flux stack"
---

# Règle absolue n8n (TOUJOURS EN PREMIER)

## Objectif

Router immédiatement toute demande **explicitement n8n** vers l'Expert n8n, sans aucune exception ; laisser les demandes **ambiguës hors stack** au triage de domaine.

## Steps

### Step 1 — Détecter n8n de façon EXPLICITE

Si la demande concerne n8n **de façon explicite** : mot « n8n » nommé dans la demande, un titre d'issue ou une référence de flux n8n. Le mot « automatisation » (ou tout nommage pouvant viser aussi bien un **flux n8n** qu'une **automatisation Home Assistant**) n'est **pas** un déclencheur explicite : il est **ambigu**.

### Step 2 — Déléguer immédiatement et arrêter le flux stack (n8n explicite)

Déclencheur n8n **explicite** présent → **déléguer IMMÉDIATEMENT à l'Expert n8n** (voir [`../production/n8n-branch.md`](../production/n8n-branch.md)) par mention valide `[@Label](mention://agent/<uuid>)`, avec mission claire, et **arrêter** ce flux. **Aucune exception, pas même l'analyse.** C'est un invariant non contournable (voir [`../../protocols/governance-security.md`](../../protocols/governance-security.md)).

### Step 3 — Aiguiller une demande ambiguë hors stack vers le triage de domaine

Si la demande est **ambiguë** (mot « automatisation », ou nommage pouvant viser un flux n8n **ou** une automatisation Home Assistant) **ET** ne concerne **pas** une stack Docker/Swarm ou Proxmox → **ne pas** appliquer la règle absolue n8n ; passer d'abord par le **triage de domaine** ([`domain-triage.md`](domain-triage.md)), qui détermine le domaine par recherche de correspondance MCP (existence seulement, aucune analyse) et aiguille. Une demande de **stack** (Docker/Swarm, Proxmox), même si elle emploie le mot « automatisation », suit son routage habituel et **ne** déclenche pas le triage.

## Sensors

Outputs: décision de routage consignée. Aucun gate humain (règle déterministe). Le triage de domaine ne s'ouvre que pour les demandes ambiguës hors stack ; il ne peut jamais lever la règle absolue n8n lorsque n8n est explicite.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : la règle absolue n8n (déclencheur **explicite**) est un **invariant** — aucune règle apprise ne peut la lever (SEC-1). Les candidats-règles de désambiguïsation (n8n vs Home Assistant) sont tracés côté triage de domaine ([`domain-triage.md`](domain-triage.md)).
