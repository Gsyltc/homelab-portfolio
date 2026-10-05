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
produces: [cadrage_confirme, verdict_impact_structurant]
consumes: [{artifact: intention_perimetre_approuves, required: true}]
requires_stage: [intent-scope-approval]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Intention et périmètre approuvés, contexte projet initialisé"
outputs: "Demande cadrée, répertoire confirmé, activation OpenSpec éventuelle confirmée, verdict d'impact structurant (déclencheur ADR obligatoire)"
---

# Réception et cadrage

## Objectif

Reprendre la demande approuvée et clarifier le besoin d'affaires sans deviner.

## Steps

### Step 1 — Passer l'issue en `in_progress`

### Step 2 — Reprendre l'entrée brute et l'intention approuvée

Confirmer le répertoire du projet (détecté en Initialization) et l'activation éventuelle d'OpenSpec.

### Step 3 — Clarifier le besoin d'affaires

Objectifs, exigences fonctionnelles et non fonctionnelles, contraintes. **Ne poser que les questions qui changent réellement la conception.** Ne jamais deviner une information manquante.

### Step 4 — Évaluer l'impact structurant (déclencheur ADR obligatoire)

Dès qu'une issue est ajoutée par l'humain, le coordinateur **statue explicitement** sur son **impact structurant** : la demande modifie-t-elle une décision d'architecture (choix technologique, frontière de système, modèle de données, intégration, sécurité, infrastructure, pattern transverse) ou en introduit-elle une nouvelle ? Le verdict (`impact structurant : Oui / Non`, avec justification) est **tracé sur l'issue** (piste d'audit).

- **Impact structurant = Oui** ⇒ le **flux ADR est obligatoire (ADR d'abord)** : le découpage ([`deliverables-breakdown`](deliverables-breakdown.md), Step 3) crée l'**issue ADR en premier**, comme **issue parente** (déléguée à l'Architecte de solution), **avant tout livrable** ; le stage [`design-and-decisions`](design-and-decisions.md) la conduit jusqu'au bout de son cycle (production mob → revue de cohérence → revue de sécurité → **ADR Proposée** → décision humaine granulaire). Les livrables ne sont créés qu'**après acceptation**, en **sous-issues** de l'ADR. Cette obligation est un **garde-fou non contournable** (voir [`../../conductor.md`](../../conductor.md), « Garde-fous ») : aucun scope, aucune règle apprise, aucun gate advisory ne peut la lever. Un impact structurant **ne peut jamais être traité sans ADR**.
- **Impact structurant = Non** ⇒ pas d'ADR imposée ; le flux `design-and-decisions` reste disponible si une décision structurante émerge en cours de conception.
- **Doute** ⇒ ne jamais deviner : demander l'arbitrage de l'humain (halt-and-ask) et, par défaut prudent, traiter comme un impact structurant (plancher, jamais plafond).

## Sensors

Outputs: cadrage confirmé + verdict d'impact structurant tracés sur l'issue.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (questions de cadrage récurrentes, motifs d'activation OpenSpec) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
