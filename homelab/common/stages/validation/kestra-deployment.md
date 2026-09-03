---
slug: kestra-deployment
phase: validation
execution: CONDITIONAL
condition: "Uniquement sur « oui » explicite de l'humain pour lancer le déploiement Kestra"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [deploiement_kestra_si_demande]
consumes: [{artifact: depot_fichiers_confirme, required: true}]
requires_stage: [file-deposit]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Fichiers déposés et vérifiés"
outputs: "Flux Kestra configure_service lancé (sur validation explicite uniquement)"
---

# Déploiement Kestra (sur validation explicite uniquement)

## Objectif

Lancer le déploiement uniquement après un « oui » explicite de l'humain.

## Steps

### Step 1 — Demander et attendre le « oui » explicite

Le Tech Lead demande si l'humain souhaite lancer le déploiement via **Kestra**. **Uniquement après un « oui » explicite** : lancer le flux Kestra `configure_service`. Les fichiers doivent rester téléchargeables pour vérification.

### Step 2 — Garde-fou absolu

**Aucun lancement du flux `configure_service` sans validation humaine explicite de la configuration complète.** Action à impact → jamais autonome (invariant).

## Sensors

Outputs: déploiement lancé (conditionnel). Gate humain **explicite** (action à impact).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (patterns de déploiement Kestra) tracés, remontés au gate explicite.
