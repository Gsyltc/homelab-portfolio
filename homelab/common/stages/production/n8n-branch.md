---
slug: n8n-branch
phase: production
execution: CONDITIONAL
condition: "Demande n8n — branche autonome (déclenchée par n8n-absolute-rule)"
lead_agent: Expert n8n
support_agents: []
mode: subagent
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [flux_n8n_propose_ou_applique]
consumes: [{artifact: routage_n8n_decide, required: true}]
requires_stage: [n8n-absolute-rule]
sensors: []
scopes: [n8n]
inputs: "Demande n8n"
outputs: "Flux n8n proposé puis appliqué après validation humaine explicite"
---

# Branche n8n (Expert n8n)

## Objectif

Traiter entièrement toute demande n8n via l'Expert n8n, sous double validation.

## Steps

### Step 1 — Traitement exclusif par l'Expert n8n

La demande est **entièrement** traitée par l'Expert n8n (aucune tâche n8n exécutée par le Tech Lead — règle absolue n8n, [`../cadrage/n8n-absolute-rule.md`](../cadrage/n8n-absolute-rule.md)). L'Expert n8n détermine le mode (flux existant → analyse limitée à ce flux ; sinon → création) via le serveur MCP n8n.

### Step 2 — Proposition → feu vert Tech Lead → validation humaine

L'Expert n8n **propose** la conception ou les changements, les fait **valider par le Tech Lead** (mention valide), **n'applique rien** via le MCP avant ce feu vert, applique **après validation humaine explicite**, vérifie l'état du flux, puis **mentionne le Tech Lead** avec le récapitulatif. Publication d'un flux : confirmation humaine explicite obligatoire.

## Sensors

Outputs: proposition / flux appliqué. Gate humain **explicite** avant toute application réelle (action à impact).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (patterns de flux n8n récurrents) tracés, remontés à la validation humaine ; la règle absolue n8n est un **invariant**.
