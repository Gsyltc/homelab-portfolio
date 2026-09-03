---
slug: concurrency-lock-read
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
produces: [etat_verrou_concurrence]
consumes: [{artifact: detection_stack_existante_vs_nouvelle, required: false}]
requires_stage: [stack-detection]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Stack visée"
outputs: "État du verrou active_step lu (libre / occupé)"
---

# Lecture du verrou de concurrence par stack

## Objectif

Garantir de façon déterministe qu'un seul traitement est actif par stack avant tout cadrage.

## Steps

### Step 1 — Lire le verrou

Lire la clé de metadata `active_step` de la stack visée (règle « un seul traitement par stack »).

### Step 2 — Sérialiser si occupé

Si un traitement est **déjà actif** sur cette stack : ne pas démarrer un second flux ; mettre la demande en file (commentaire « en attente : traitement `<X>` en cours ») et reprendre à la libération du verrou. Cette lecture est déterministe et **précède** tout cadrage.

## Sensors

Outputs: état du verrou consigné. Aucun gate humain (bootstrap déterministe).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : tenir le journal des candidats-règles sur l'issue. Stage d'Initialisation → **saute** l'interaction liée au gate humain.
