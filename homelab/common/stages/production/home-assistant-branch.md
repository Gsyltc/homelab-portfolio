---
slug: home-assistant-branch
phase: production
execution: CONDITIONAL
condition: "Demande Home Assistant — branche autonome"
lead_agent: Expert Home Assistant
support_agents: []
mode: subagent
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [modification_home_assistant_proposee_ou_appliquee]
consumes: [{artifact: intention_perimetre_approuves, required: true}]
requires_stage: [intake-framing]
sensors: []
scopes: [home-assistant]
inputs: "Demande Home Assistant"
outputs: "Modification Home Assistant proposée puis appliquée après validation humaine explicite"
---

# Branche Home Assistant (Expert Home Assistant)

## Objectif

Traiter toute demande Home Assistant via MCP officiel, sous séquence de validation stricte.

## Steps

### Step 1 — Séquence obligatoire (jamais dans un autre ordre)

**Propositions** (mode modification limité à l'élément visé, ou mode création) → **vérification par le Tech Lead** (mention valide) → **validation humaine explicite** → seulement ensuite **modification réelle** via le MCP officiel.

### Step 2 — Confirmer l'effet réel et rendre compte

Relire l'état des entités pour confirmer l'effet réel, puis **mentionner le Tech Lead** (mention valide) avec le récapitulatif.

## Sensors

Outputs: proposition / modification appliquée. Gate humain **explicite** avant toute modification réelle (action à impact).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (patterns d'entités / scènes / automatisations récurrents) tracés, remontés à la validation humaine.
