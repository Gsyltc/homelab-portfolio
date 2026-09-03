---
slug: detailed-deliverables
phase: construction
execution: ALWAYS
condition: "Always executes — rythme selon le mode d'exécution choisi"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Infrastructure Windows, OpenSpec Expert]
mode: mob
for_each: unit-of-work
summary_confirmation: required
reviewer: Reviewer de cohérence
review_class: advisory
review_artifact: livrable-<unite>.md
human_gate: granular
produces: [livrables_detailles]
consumes: [{artifact: walking_skeleton_valide, required: true}, {artifact: mode_execution_choisi, required: true}]
requires_stage: [walking-skeleton]
sensors: [required-sections, upstream-coverage, diagram-validity]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Walking skeleton validé + mode d'exécution"
outputs: "Livrables détaillés (documentation, diagrammes définitifs, coûts AWS, config infra, ou implémentation OpenSpec)"
---

# Production des livrables détaillés

## Objectif
Produire les livrables du lot cadré, au rythme fixé par le mode d'exécution — **une exécution par unité de travail** (`for_each: unit-of-work`).

## Steps
### Step 1 — Produire par livrable / agent (une fois par unité)
Le stage s'exécute **une fois par unité de travail** (`for_each: unit-of-work`). Chaque agent exécute son livrable (les `support_agents` travaillent en `mob` contre le brouillon du lead) ; en fin de travail, mentionne le coordinateur pour vérification. Documenter sur l'issue. L'agrégation des unités se déduit du graphe.

### Step 2 — Rythme de validation
- **Gated** *(défaut)* : chaque livrable validé granulairement avant de poursuivre.
- **Autonome** : livrables du même lot enchaînés ; validation granulaire **regroupée** en un point de synchronisation (l'humain valide en bloc, **toujours choix par choix**).

### Step 3 — Revue de cohérence (advisory)
À réception de chaque livrable, le coordinateur sollicite le **Reviewer de cohérence** (verdict consultatif : complétude, cohérence documentation ↔ décisions, conventions) avant le gate humain.

### Step 4 — Halt-and-ask systématique sur échec
S'arrêter et interroger l'humain sur : échec / impossibilité d'un livrable ; écart ou contrôle de sécurité requis ; gate / sensor en écart ou `⛔ indisponible` ; décision structurante nouvelle non cadrée ; action à impact / destructive (jamais autonome). L'autonomie ne court-circuite jamais le contrôle sécurité ni les actions à impact.

## Sensors
Outputs: livrables détaillés (une fois par unité).
Imports: `required-sections`, `upstream-coverage`, `diagram-validity`.
Upstream targets: `walking_skeleton_valide` (required), `mode_execution_choisi` (required) — couverture amont vérifiée à l'écriture de chaque livrable.
Review artifact: chaque `livrable-<unite>.md` porte la section `## Review` ajoutée par le Reviewer de cohérence.

## Learn
Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de production, corrections récurrentes par type de livrable) ; les remonter au **gate humain granulaire** (regroupé en mode autonome, jamais fusionné) ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit. Divergence tracée vs un journal `memory.md` externe (voir [ADR-0009](../../../../decisions/0009-alignement-fiches-de-stage-sur-ai-dlc.md)).
