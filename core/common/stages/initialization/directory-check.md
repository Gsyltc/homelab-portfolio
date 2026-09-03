---
slug: directory-check
phase: initialization
execution: CONDITIONAL
condition: "Sollicite l'humain uniquement si le répertoire projet est introuvable ou ambigu"
lead_agent: null
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [repertoire_projet_confirme]
consumes: []
requires_stage: []
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Demande brute, contexte du workspace"
outputs: "Répertoire officiel du projet confirmé (ou demande de confirmation à l'humain)"
---

# Vérification du répertoire projet

## Objectif
Garantir de façon déterministe l'existence du répertoire officiel du projet avant tout travail.

## Steps
### Step 1 — Vérifier l'existence
Vérifier le répertoire officiel du projet et les emplacements conventionnels (`decisions/`, documentation d'architecture, `core/rules/`, `core/sensors/`).

### Step 2 — Garde déterministe (seul cas de sollicitation humaine à cette phase)
Répertoire introuvable ou ambigu → demander confirmation à l'humain et **ne pas lancer les travaux** sans elle. Ce n'est **pas** un gate de validation : c'est une garde déterministe.

## Sensors
Outputs: répertoire confirmé consigné sur l'issue. Aucun gate humain (bootstrap déterministe).
Imports: none.

## Learn
Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tenir le journal des candidats-règles sur l'issue. Stage d'Initialization (bootstrap déterministe) → **saute** l'interaction liée au gate humain ; aucune règle n'est écrite hors du cycle capture → confirmation humaine → contrôle de conflit. Divergence tracée vs le journal `memory.md` d'AI-DLC (voir [ADR-0009](../../../../decisions/0009-alignement-fiches-de-stage-sur-ai-dlc.md)).
