---
slug: stack-detection
phase: initialisation
execution: ALWAYS
condition: "Always executes — bootstrap déterministe"
lead_agent: null
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [detection_stack_existante_vs_nouvelle]
consumes: []
requires_stage: []
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Demande brute"
outputs: "Fait consigné : stack existante (modification) ou nouvelle (création)"
---

# Détection « stack existante vs nouvelle »

## Objectif

Déterminer de façon déterministe si la demande vise une stack existante ou une nouvelle stack.

## Steps

### Step 1 — Déterminer la nature

Analyser la demande : modification / correctif / mise à jour d'une stack **existante**, ou **création** d'une nouvelle stack.

### Step 2 — Consigner (sans valider)

Consigner le fait en commentaire (piste d'audit). Il **oriente** l'auto-détection du scope en Idéation (`stack-update` / `config-change` / `security-patch` vs `new-stack`) sans figer la décision. Ce n'est **pas** un gate.

## Sensors

Outputs: fait de détection consigné sur l'issue. Aucun gate humain (bootstrap déterministe).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : tenir le journal des candidats-règles sur l'issue. Stage d'Initialisation (bootstrap déterministe) → **saute** l'interaction liée au gate humain ; aucune règle n'est écrite hors du cycle capture → confirmation humaine → contrôle de conflit.
