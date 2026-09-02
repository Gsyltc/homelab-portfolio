---
slug: consolidation-handoff
phase: construction
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecture Solution & Intégration
support_agents: [Experte d'archivage, OpenSpec Expert]
mode: inline
summary_confirmation: required
reviewer: null
review_class: granular
human_gate: granular
produces: [livrables_valides_mis_a_disposition]
consumes: [{artifact: controle_securite_coherence, required: true}]
requires_stage: [security-consistency-check]
sensors: [required-sections]
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Livrables contrôlés"
outputs: "Livrables validés granulairement + mis à disposition (Experte d'archivage) ; archivage OpenSpec si activé"
---

# Consolidation, validation humaine et mise à disposition

## Objectif
Valider les livrables restants et les mettre à disposition.

## Steps
### Step 1 — Validation granulaire humaine
De chaque livrable / choix restant à approuver (boucle Keep / Modify / Redo).

### Step 2 — Mise à disposition
Confier à l'**Experte d'archivage** le téléversement, la visualisation, le téléchargement et l'archivage des documents validés dans le répertoire du projet ; fournir à l'humain un récapitulatif accessible.

### Step 3 — Archivage OpenSpec (si activé)
L'OpenSpec Expert archive le changement (fusion des deltas dans les specs vivantes) et passe l'issue à Done après approbation.

## Gate / sortie
Livrables validés et mis à disposition. Frontière **Construction → Operation** : gate `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin` + sensor `required-sections`.
