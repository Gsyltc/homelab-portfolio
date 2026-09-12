---
slug: domain-triage
phase: cadrage
execution: CONDITIONAL
condition: "Demande ambiguë (mot « automatisation », ou nommage pouvant viser aussi bien un flux n8n qu'une automatisation Home Assistant) ET ne concernant PAS une stack Docker/Swarm ou Proxmox ET domaine non explicite (n8n pas nommé explicitement)"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [routage_domaine_decide]
consumes: [{artifact: intention_perimetre_approuves, required: true}]
requires_stage: [n8n-absolute-rule]
sensors: []
scopes: [n8n, home-assistant]
inputs: "Demande ambiguë hors stack, intention + périmètre approuvés"
outputs: "Décision d'aiguillage : délégation à l'Expert n8n, à l'Expert Home Assistant, ou remontée humaine explicite (ambiguïté persistante / élément inexistant)"
---

# Triage de domaine (n8n vs Home Assistant)

## Objectif

Pour une demande **ambiguë hors stack**, déterminer par **recherche de correspondance** via les deux MCP à quel domaine (n8n ou Home Assistant) elle appartient, puis aiguiller — **sans aucune analyse**.

## Steps

### Step 1 — Confirmer le déclenchement du triage

N'exécuter ce stage que si la demande est **ambiguë** (mot « automatisation », ou un nommage pouvant viser aussi bien un **flux n8n** qu'une **automatisation Home Assistant**) **ET** ne concerne **pas** une stack Docker/Swarm ou Proxmox. Les demandes dont le domaine est **déjà explicite** (« n8n » nommé explicitement → règle absolue n8n, voir [`n8n-absolute-rule.md`](n8n-absolute-rule.md) ; « Home Assistant » nommé explicitement → branche Home Assistant) **ne passent pas** par ce triage. Les demandes de stack (Docker/Swarm, Proxmox) suivent leur routage habituel ([`swarm-proxmox-arbitration.md`](swarm-proxmox-arbitration.md)).

### Step 2 — Recherche de correspondance (existence seulement, AUCUNE analyse)

Rechercher **uniquement l'existence** d'une correspondance de nom, sans lire la logique interne, sans diagnostiquer, sans modifier :

- **MCP n8n** — rechercher si un **workflow** portant ce nom existe.
- **MCP Home Assistant** — rechercher **uniquement parmi les automatisations** si une correspondance de ce nom existe.

Le diagnostic, la lecture de logique et la modification restent la responsabilité du spécialiste (Expert n8n / Expert Home Assistant), **jamais** du Tech Lead. À cette étape, les MCP servent UNIQUEMENT à déterminer le domaine et à router.

### Step 3 — Décider l'aiguillage (quatre cas)

- **Trouvé côté n8n uniquement** → déléguer à l'**Expert n8n** (voir [`../production/n8n-branch.md`](../production/n8n-branch.md)) par mention valide `[@Label](mention://agent/<uuid>)` (rôle → agent résolu via [`homelab/agents/`](../../../agents/README.md) au moment de déléguer), avec mission claire, et **arrêter** le flux stack.
- **Trouvé côté Home Assistant uniquement** → déléguer à l'**Expert Home Assistant** (voir [`../production/home-assistant-branch.md`](../production/home-assistant-branch.md)) par mention valide, avec mission claire.
- **Trouvé des deux côtés** → **NE PAS trancher seul** : demander au **propriétaire du workspace** par une **mention explicite**, indiquer les **deux** correspondances trouvées, et **attendre** sa décision avant toute délégation.
- **Trouvé nulle part** :
  - Si l'issue demande de **créer** un flux ou une automatisation → passer en **mode création** et router vers le spécialiste correspondant au **type demandé** (Expert n8n pour un flux, Expert Home Assistant pour une automatisation).
  - Si l'issue demande de **vérifier, contrôler ou modifier** un flux / une automatisation **existant(e)** → informer le **propriétaire du workspace** par une **mention explicite** que le flux ou l'automatisation **n'existe pas**, et **attendre**.

Consigner la recherche, les correspondances trouvées et la décision d'aiguillage en commentaire (piste d'audit).

## Sensors

Outputs: décision de routage de domaine consignée sur l'issue ; aiguillage vers la branche n8n / Home Assistant, ou remontée humaine explicite (ambiguïté persistante / élément inexistant sur une demande de vérification/modification). Aucun gate humain propre au triage (aiguillage déterministe) ; la remontée humaine des cas « deux côtés » et « inexistant sur vérification/modification » est un **arrêt bloquant** (jamais de décision à la place de l'humain).
Imports: none.
Upstream targets: intention_perimetre_approuves (`intent-scope-approval`).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de désambiguïsation n8n vs Home Assistant, nommages récurrents) tracés, remontés à la validation humaine. Le triage ne fait **aucune analyse** ni modification — recherche d'existence et aiguillage uniquement ; la règle absolue n8n (déclencheur explicite) reste un **invariant** non levé par ce stage.
