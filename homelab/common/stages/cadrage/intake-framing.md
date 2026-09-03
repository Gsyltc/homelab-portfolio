---
slug: intake-framing
phase: cadrage
execution: ALWAYS
condition: "Always executes (branches n8n / home-assistant court-circuitées)"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [cadrage_confirme, lien_documentation_officielle]
consumes: [{artifact: intention_perimetre_approuves, required: true}]
requires_stage: [n8n-absolute-rule]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Intention + périmètre approuvés, scope confirmé"
outputs: "Cadrage confirmé + lien de documentation officielle consigné + domaine identifié"
---

# Réception et cadrage

## Objectif

Cadrer la demande et consigner la documentation officielle avant toute génération.

## Steps

### Step 1 — Confirmer l'état de l'issue

Confirmer que l'issue est en `in_progress` et que le label `Homelab` est posé (posé en Phase 0).

### Step 2 — Consigner la demande brute

Consigner la demande initiale (entrée brute) en commentaire si ce n'est pas déjà fait en amont.

### Step 3 — Règle préalable de documentation officielle (niveau cadrage)

Appliquer la **règle préalable de documentation officielle** (voir [`../../conductor.md`](../../conductor.md)) au **niveau cadrage uniquement** (lien officiel + déployabilité + paramètres de cadrage), **sans** relevé fin des variables / conventions, et documenter le résultat.

### Step 4 — Identifier le domaine

Stack Docker (Spécialiste Docker / QA Docker), Home Assistant (Expert Home Assistant), Terraform (Spécialiste Terraform), ou domaine sans agent (Ansible, logs, Kestra → Tech Lead réalise lui-même la vérification et le signale à l'humain).

## Sensors

Outputs: cadrage + lien de documentation officielle consignés. Frontière **Cadrage → Production** : gate `artefacts-presents` + `liaison-tracabilite` sur le lien de documentation officielle (artefact requis PROPRE au Homelab) — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (sources de documentation officielle par stack) tracés, remontés au gate granulaire de fin de Production / Validation.
