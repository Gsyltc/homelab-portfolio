---
slug: detailed-deliverables
phase: construction
execution: ALWAYS
condition: "Always executes — rythme selon le mode d'exécution choisi"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Administrateur infrastructure Windows, OpenSpec Expert]
mode: multi-agent
summary_confirmation: required
reviewer: Architecture Solution & Intégration
review_class: granular
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
Produire les livrables du lot cadré, au rythme fixé par le mode d'exécution.

## Steps
### Step 1 — Produire par livrable / agent
Chaque agent exécute son livrable ; en fin de travail, mentionne le coordinateur pour vérification. Documenter sur l'issue.

### Step 2 — Rythme de validation
- **Gated** *(défaut)* : chaque livrable validé granulairement avant de poursuivre.
- **Autonome** : livrables du même lot enchaînés ; validation granulaire **regroupée** en un point de synchronisation (l'humain valide en bloc, **toujours choix par choix**).

### Step 3 — Halt-and-ask systématique sur échec
S'arrêter et interroger l'humain sur : échec / impossibilité d'un livrable ; écart ou contrôle de sécurité requis ; gate / sensor en écart ou `⛔ indisponible` ; décision structurante nouvelle non cadrée ; action à impact / destructive (jamais autonome). L'autonomie ne court-circuite jamais le contrôle sécurité ni les actions à impact.

## Gate / sortie
Livrables détaillés. Sensors `required-sections` / `upstream-coverage` / `diagram-validity` à l'écriture.
