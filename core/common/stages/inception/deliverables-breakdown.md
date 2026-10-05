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
consumes: [{artifact: besoins_traces, required: true}, {artifact: verdict_impact_structurant, required: true}]
requires_stage: [requirements-analysis]
sensors: [diagram-validity]
scopes: [standard, feature, infra, mvp, enterprise]
inputs: "Besoins tracés + verdict d'impact structurant"
outputs: "Livrables découpés + une tâche dédiée par spécialiste/architecte délégataire (hors revues) + sous-tâche ADR bloquante créée si impact structurant (parent des tâches spécialistes) + diagramme du workflow retenu"
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
- **Révision des patrons d'architecture** (ajout / suppression / modification des patterns de référence) → **Architecte de solution**, **lorsqu'une décision structurante l'impose** (contrôle inconditionnel évalué au stage [`design-and-decisions`](design-and-decisions.md), Step 6 ; si les patrons restent inchangés, aucune tâche — consigner « patrons inchangés »).
- Cycle spec-driven **et mise à jour des spécifications sur décision structurante** → **OpenSpec Expert** (**uniquement si OpenSpec activé** ; hors projet OpenSpec, aucune tâche OpenSpec — N/A).

### Step 3 — Déclencher les agents

Créer les issues nécessaires ; déclencher chaque agent par mention (UUID résolu, jamais deviné) avec mission claire.

> **Une tâche par spécialiste / architecte (hors revues) — règle de délégation.** Chaque **délégation de livrable** à un spécialiste / architecte donne lieu à **une tâche (issue) dédiée par agent** : une tâche pour l'Architecte de solution, une pour l'Architecte de données, une pour l'Architecte AWS, une pour l'Infrastructure Windows, une pour l'OpenSpec Expert — **jamais** une tâche fourre-tout partagée entre plusieurs spécialistes. Chaque tâche porte un périmètre, des critères d'acceptation et l'agent de retour (le coordinateur, en texte clair) propres à l'agent délégataire.
>
> **Exclusion explicite — les revues ne sont pas des tâches.** Les **revues** (Reviewer de cohérence, Reviewer de sécurité) **ne font pas l'objet d'une tâche dédiée** : ce sont des fonctions *review-only* **sollicitées en place par le coordinateur** sur l'issue qui porte le livrable / l'ADR (voir [`protocols/reviewer.md`](../../protocols/reviewer.md)). Elles postent leurs conclusions directement dans cette issue, sans issue dédiée. La règle « une tâche par agent » ne s'applique donc **qu'aux délégations de production de livrable**, jamais aux revues.
>
> **Sous-tâche ADR obligatoire et bloquante sur impact structurant.** Lorsque le **verdict d'impact structurant** établi au cadrage ([`intake-framing`](intake-framing.md), Step 4) vaut **`Oui`**, le découpage **crée obligatoirement une sous-tâche dédiée portant l'ADR**, déléguée à l'**Architecte de solution** (qui conduit le flux ADR au stage [`design-and-decisions`](design-and-decisions.md) : production mob → revue de cohérence → revue de sécurité → **ADR Proposée** → décision humaine granulaire). Cette sous-tâche est **distincte** des autres tâches de livrable et respecte la règle « une tâche par agent ». Lorsque plusieurs décisions structurantes sont identifiées, créer **une sous-tâche ADR par ADR**. C'est un **garde-fou non contournable** (voir [`conductor.md`](../../conductor.md), « Garde-fous ») : un impact structurant ne peut jamais être traité sans que sa sous-tâche ADR soit créée au découpage. En cas de doute sur le verdict, halt-and-ask.
>
> **L'ADR est la condition de démarrage des tâches des spécialistes / architectes (gate bloquant).** Les tâches des spécialistes / architectes **dépendent de la sous-tâche ADR** : elles sont créées au découpage mais **ne démarrent pas** tant que l'ADR n'est pas tranchée. La sous-tâche ADR est posée comme **tâche parente / dépendance bloquante** des tâches de livrable (sous Multica : `multica issue update <id-tâche-spécialiste> --parent <id-sous-tâche-ADR>`, ou `--no-start` à la création pour empêcher le démarrage prématuré). Transitions de ce gate :
>
> - **ADR → `done` (Keep humain)** = **feu vert** : le coordinateur **lance alors en parallèle** toutes les tâches des spécialistes / architectes dépendantes (mentions A2A, UUID résolus) — c'est le seul point de départ autorisé pour ces tâches.
> - **ADR → `cancelled` (rejet humain)** = **propagation du rejet** : toutes les tâches des spécialistes / architectes dépendantes de cette ADR passent **aussi à `cancelled`** (`multica issue status <id> cancelled`), car leur condition indispensable n'est pas satisfaite. Le coordinateur trace la propagation sur l'issue et, le cas échéant, relance une nouvelle ADR si l'humain reformule la décision.
> - **ADR encore en cours** (`in_progress` / `in_review` / `ADR Proposée`) ⇒ les tâches dépendantes **restent non démarrées** (aucune production avant le feu vert).

Chaque mission déléguée inclut **obligatoirement** :

- Le **nom de l'agent de retour en texte clair** (le coordinateur), **sans lien de mention actif vers lui-même** : la pose du lien de retour actif et le passage en `in_review` reviennent à l'agent délégataire en fin de tâche. L'obligation de retour A2A a **une seule source non contournable** — la « Checklist de sortie de stage » de [`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md) — et n'est pas redéfinie ici (voir aussi [`../../protocols/governance-security.md`](../../protocols/governance-security.md), « Règle A2A »).
- Le **tag de méthodologie** sur l'issue déléguée (**contexte Multica uniquement**) : toute issue confiée à l'**OpenSpec Expert** (cycle spec-driven, OpenSpec activé) est taguée **`OpenSpec`** — `multica issue label add <issue-id> <label-id>`, l'id du label résolu via `multica label list --output json` (créer le label `OpenSpec` via `multica label create` s'il n'existe pas). Ce tag rend visible, dès le découpage, quelles issues relèvent de la méthode OpenSpec. Les labels d'issue étant **propres à Multica**, l'étape est sautée hors Multica. L'**OpenSpec Expert pose aussi ce tag en première action** s'il traite une issue Multica (voir [`../../../agents/openspec-agent.md`](../../../agents/openspec-agent.md)) : le premier des deux qui agit suffit, l'autre est idempotent.

### Step 4 — Visualiser le workflow retenu (diagramme en code, syntaxe validée) sur l'issue

## Sensors

Outputs: découpage + sous-tâche ADR bloquante (si impact structurant) + diagramme du workflow retenu.
Imports: `diagram-validity`.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de découpage, affectation d'agents récurrente) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
