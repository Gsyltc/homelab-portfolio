---
slug: labels-audit-init
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
produces: [labels_poses, piste_audit_initialisee, demande_brute_consignee, regles_global_chargees]
consumes: []
requires_stage: [deployment-prereqs-precheck]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Demande brute"
outputs: "Labels Homelab (+ Docker Swarm), piste d'audit initialisée, règles global chargées"
---

# Labels et initialisation de la piste d'audit

## Objectif

Poser les labels, initialiser la piste d'audit et charger les règles toujours actives.

## Steps

### Step 1 — Poser les labels

Poser systématiquement le label **`Homelab`**.

### Step 2 — Initialiser la piste d'audit

Initialiser la piste d'audit : consigner sur l'issue l'entrée **brute** de la demande, non résumée (`demande_brute_consignee`). C'est la **seule** consignation de l'entrée brute du workflow : les stages suivants s'y réfèrent sans la recopier.

### Step 3 — Charger les règles toujours actives (chargement paresseux)

Charger **paresseusement** la couche `global` de la mémoire de règles (voir [`homelab/rules/`](../../../rules/README.md)). Aucune instruction complète de spécialiste ni secret n'est chargé à ce stade (chargement optimisé pour le contexte).

## Sensors

Outputs: labels + piste d'audit initialisée + règles `global` chargées. Aucun gate humain. Frontière **Demande → Phase 0** : gate `artefacts-presents` (demande brute consignée, label `Homelab` posé) — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : la couche `global` chargée ici est le point d'entrée de la mémoire de règles. Stage d'Initialisation → tient le journal des candidats-règles mais **saute** l'interaction liée au gate humain.
