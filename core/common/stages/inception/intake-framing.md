---
slug: intake-framing
phase: inception
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecture Solution & Intégration
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [cadrage_confirme]
consumes: [{artifact: intention_perimetre_approuves, required: true}]
requires_stage: [intent-scope-approval]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Intention et périmètre approuvés, contexte projet initialisé"
outputs: "Demande cadrée, répertoire confirmé, activation OpenSpec éventuelle confirmée"
---

# Réception et cadrage

## Objectif
Reprendre la demande approuvée et clarifier le besoin d'affaires sans deviner.

## Steps
### Step 1 — Passer l'issue en `in_progress`.

### Step 2 — Reprendre l'entrée brute et l'intention approuvée
Confirmer le répertoire du projet (détecté en Initialization) et l'activation éventuelle d'OpenSpec.

### Step 3 — Clarifier le besoin d'affaires
Objectifs, exigences fonctionnelles et non fonctionnelles, contraintes. **Ne poser que les questions qui changent réellement la conception.** Ne jamais deviner une information manquante.

## Sensors
Outputs: cadrage confirmé sur l'issue.
Imports: none.

## Learn
Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (questions de cadrage récurrentes, motifs d'activation OpenSpec) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit. Divergence tracée vs le journal `memory.md` d'AI-DLC (voir [ADR-0009](../../../../decisions/0009-alignement-fiches-de-stage-sur-ai-dlc.md)).
