---
slug: deliverables-breakdown
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
produces: [decoupage_livrables, diagramme_workflow_retenu]
consumes: [{artifact: besoins_traces, required: true}]
requires_stage: [requirements-analysis]
sensors: [diagram-validity]
scopes: [standard, feature, infra, mvp, enterprise]
inputs: "Besoins tracés"
outputs: "Livrables découpés + agent responsable désigné par livrable + diagramme du workflow retenu"
---

# Planification et découpage en livrables

## Objectif
Découper le travail en livrables et désigner l'agent responsable de chacun.

## Steps
### Step 1 — Déterminer phases, étapes et profondeur.

### Step 2 — Découper et désigner l'agent responsable
- Documentation d'architecture / décisions structurantes / diagrammes → **Architecte de solution**.
- Choix AWS, diagrammes AWS, coûts → **Architecte AWS** (si AWS requis).
- Administration / infrastructure Windows → **Administrateur infrastructure Windows** (si concerné).
- Cycle spec-driven → **OpenSpec Expert** (uniquement si OpenSpec activé).

### Step 3 — Déclencher les agents
Créer les issues nécessaires ; déclencher chaque agent par mention (UUID résolu, jamais deviné) avec mission claire.

### Step 4 — Visualiser le workflow retenu (diagramme en code, syntaxe validée) sur l'issue.

## Sensors
Outputs: découpage + diagramme du workflow retenu.
Imports: `diagram-validity`.

## Learn
Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de découpage, affectation d'agents récurrente) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit. Divergence tracée vs le journal `memory.md` d'AI-DLC (voir [ADR-0009](../../../../decisions/0009-alignement-fiches-de-stage-sur-ai-dlc.md)).
