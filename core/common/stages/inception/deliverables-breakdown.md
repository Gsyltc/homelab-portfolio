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

### Step 1 — Déterminer phases, étapes et profondeur

### Step 2 — Découper et désigner l'agent responsable

- Documentation d'architecture / décisions structurantes / diagrammes → **Architecte de solution**.
- Analyse et cycle de vie des données (modélisation, gouvernance, classification, `10-cycle_vie_donnees.md`) → **Architecte de données** (délégué par l'Architecte de solution, qui valide le livrable — critère : sensor `data-lifecycle`).
- Choix AWS, diagrammes AWS, coûts → **Architecte AWS** (si AWS requis).
- Administration / infrastructure Windows → **Infrastructure Windows** (si concerné).
- Cycle spec-driven → **OpenSpec Expert** (uniquement si OpenSpec activé).

### Step 3 — Déclencher les agents

Créer les issues nécessaires ; déclencher chaque agent par mention (UUID résolu, jamais deviné) avec mission claire.

Chaque mission déléguée inclut **obligatoirement** :

- Le **nom de l'agent de retour en texte clair** (le coordinateur), **sans lien de mention actif vers lui-même** : la pose du lien de retour actif et le passage en `in_review` reviennent à l'agent délégataire en fin de tâche. L'obligation de retour A2A a **une seule source non contournable** — la « Checklist de sortie de stage » de [`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md) — et n'est pas redéfinie ici (voir aussi [`../../protocols/governance-security.md`](../../protocols/governance-security.md), « Règle A2A »).
- Le **tag de méthodologie** sur l'issue déléguée (**contexte Multica uniquement**) : toute issue confiée à l'**OpenSpec Expert** (cycle spec-driven, OpenSpec activé) est taguée **`OpenSpec`** — `multica issue label add <issue-id> <label-id>`, l'id du label résolu via `multica label list --output json` (créer le label `OpenSpec` via `multica label create` s'il n'existe pas). Ce tag rend visible, dès le découpage, quelles issues relèvent de la méthode OpenSpec. Les labels d'issue étant **propres à Multica**, l'étape est sautée hors Multica. L'**OpenSpec Expert pose aussi ce tag en première action** s'il traite une issue Multica (voir [`../../../agents/openspec-agent.md`](../../../agents/openspec-agent.md)) : le premier des deux qui agit suffit, l'autre est idempotent.

### Step 4 — Visualiser le workflow retenu (diagramme en code, syntaxe validée) sur l'issue

## Sensors

Outputs: découpage + diagramme du workflow retenu.
Imports: `diagram-validity`.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de découpage, affectation d'agents récurrente) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
