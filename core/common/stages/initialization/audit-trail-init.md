---
slug: audit-trail-init
phase: initialization
execution: ALWAYS
condition: "Always executes"
lead_agent: null
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [piste_audit_ouverte, regles_toujours_actives_chargees]
consumes: [{artifact: contexte_brownfield_greenfield_consigne, required: true}]
requires_stage: [brownfield-greenfield-detection]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Contexte détecté (répertoire, brownfield / greenfield)"
outputs: "Piste d'audit initialisée sur l'issue, règles toujours actives + index chargés (chargement paresseux)"
---

# Initialisation de l'état et de la piste d'audit

## Objectif
Ouvrir la piste d'audit et charger le contexte léger, de façon déterministe.

## Steps
### Step 1 — Ouvrir la piste d'audit sur l'issue
Consigner le contexte détecté (répertoire, brownfield / greenfield). Aucun secret consigné.

### Step 2 — Charger les règles toujours actives
`core/rules/workspace.md` + `project` courant, et l'**index** (titres) des autres couches (chargement paresseux).

### Step 3 — Chargement optimisé pour le contexte
Métadonnées légères uniquement (descriptions d'agents / skills, index du registre de décisions, sommaire de la doc). Voir [`conductor.md`](../../conductor.md).

## Sensors
Outputs: piste d'audit ouverte, règles actives chargées. Aucun gate humain (Initialization reste sous les invariants : piste d'audit, aucun secret).
Imports: none.

## Learn
Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : ce stage **ouvre** le journal des candidats-règles sur l'issue et charge les règles persistantes (chargement paresseux). Stage d'Initialization (bootstrap déterministe) → **saute** l'interaction liée au gate humain ; l'écriture de règles reste réservée au cycle capture → confirmation humaine → contrôle de conflit. Divergence tracée vs le journal `memory.md` d'AI-DLC (voir [ADR-0009](../../../../decisions/0009-alignement-fiches-de-stage-sur-ai-dlc.md)).
