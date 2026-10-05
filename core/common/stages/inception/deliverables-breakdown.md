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
outputs: "Tâches de livrable créées en backlog (une par spécialiste/architecte délégataire, hors revues, agent assigné) + sous-tâche ADR bloquante créée ensuite si impact structurant (parent des tâches, qui démarrent à l'ADR done) + diagramme du workflow retenu"
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

### Step 3 — Créer les tâches (backlog), puis l'ADR, puis lancer au feu vert

Le découpage suit un **ordre strict** : d'abord **créer** toutes les tâches de livrable (en `backlog`, agent assigné, non démarrées), **ensuite** — si décision structurante — créer l'ADR comme **dépendance bloquante**, et **enfin** lancer les tâches liées une fois l'ADR `done`.

#### Step 3.1 — Créer les tâches des spécialistes / architectes en `backlog` (agents assignés, non démarrées)

Créer **toutes** les tâches de livrable **d'abord**, chacune en statut **`backlog`** avec son **agent délégataire assigné** (`--assignee` / `--assignee-id`, UUID résolu, jamais deviné) — `multica issue create ... --status backlog --assignee-id <uuid>`. Le statut `backlog` **parque** la tâche sans la démarrer : aucune production ne commence tant qu'elle n'est pas promue (Step 3.3). On crée donc le découpage complet **avant** toute décision structurante et **avant** tout lancement.

> **Une tâche par spécialiste / architecte (hors revues) — règle de délégation.** Chaque **délégation de livrable** à un spécialiste / architecte donne lieu à **une tâche (issue) dédiée par agent** : une tâche pour l'Architecte de solution, une pour l'Architecte de données, une pour l'Architecte AWS, une pour l'Infrastructure Windows, une pour l'OpenSpec Expert — **jamais** une tâche fourre-tout partagée entre plusieurs spécialistes. Chaque tâche porte un périmètre, des critères d'acceptation et l'agent de retour (le coordinateur, en texte clair) propres à l'agent délégataire.
>
> **Exclusion explicite — les revues ne sont pas des tâches.** Les **revues** (Reviewer de cohérence, Reviewer de sécurité) **ne font pas l'objet d'une tâche dédiée** : ce sont des fonctions *review-only* **sollicitées en place par le coordinateur** sur l'issue qui porte le livrable / l'ADR (voir [`../../protocols/reviewer.md`](../../protocols/reviewer.md)). Elles postent leurs conclusions directement dans cette issue, sans issue dédiée. La règle « une tâche par agent » ne s'applique donc **qu'aux délégations de production de livrable**, jamais aux revues.

#### Step 3.2 — Si décision structurante : créer l'ADR, posée en dépendance bloquante des tâches

> **Sous-tâche ADR obligatoire et bloquante sur impact structurant.** Lorsque le **verdict d'impact structurant** établi au cadrage ([`intake-framing`](intake-framing.md), Step 4) vaut **`Oui`**, le coordinateur crée — **après** la création des tâches de livrable (Step 3.1) — une **sous-tâche dédiée portant l'ADR**, déléguée à l'**Architecte de solution** (qui conduit le flux ADR au stage [`design-and-decisions`](design-and-decisions.md) : production mob → revue de cohérence → revue de sécurité → **ADR Proposée** → décision humaine granulaire). Cette sous-tâche est **distincte** des tâches de livrable et respecte la règle « une tâche par agent ». Lorsque plusieurs décisions structurantes sont identifiées, créer **une sous-tâche ADR par ADR**. C'est un **garde-fou non contournable** (voir [`../../conductor.md`](../../conductor.md), « Garde-fous ») : un impact structurant ne peut jamais être traité sans que sa sous-tâche ADR soit créée. En cas de doute sur le verdict, halt-and-ask.
>
> **Rattachement des tâches `backlog` à l'ADR.** Une fois l'ADR créée, le coordinateur **rattache** les tâches de livrable déjà créées en `backlog` (Step 3.1) à l'ADR comme **dépendance bloquante** : `multica issue update <id-tâche-spécialiste> --parent <id-sous-tâche-ADR>`. Les tâches restent en `backlog` (non démarrées) tant que l'ADR n'est pas tranchée.
>
> **Pas de décision structurante (`verdict Non`)** ⇒ pas d'ADR : le coordinateur promeut directement les tâches `backlog` selon le reste du séquencement du stage (pas de gate ADR à franchir).

#### Step 3.3 — Lancer les tâches liées une fois l'ADR tranchée (gate bloquant)

> **L'ADR est la condition de démarrage des tâches des spécialistes / architectes (gate bloquant).** Les tâches, créées en `backlog` (Step 3.1) et rattachées à l'ADR (Step 3.2), **ne démarrent pas** tant que l'ADR n'est pas tranchée. Transitions de ce gate :
>
> - **ADR → `done` (Keep humain)** = **feu vert** : le coordinateur **promeut et lance alors en parallèle** toutes les tâches des spécialistes / architectes dépendantes — promotion du `backlog` vers le démarrage (`multica issue status <id> todo`, qui démarre l'agent assigné) et mentions A2A (UUID résolus). C'est le seul point de départ autorisé pour ces tâches.
> - **ADR → `cancelled` (rejet humain)** = **propagation du rejet** : toutes les tâches des spécialistes / architectes dépendantes de cette ADR passent **aussi à `cancelled`** (`multica issue status <id> cancelled`), car leur condition indispensable n'est pas satisfaite. Le coordinateur trace la propagation sur l'issue et, le cas échéant, relance une nouvelle ADR si l'humain reformule la décision.
> - **ADR encore en cours** (`in_progress` / `in_review` / `ADR Proposée`) ⇒ les tâches dépendantes **restent en `backlog`** (aucune production avant le feu vert).

#### Mission déléguée — contenu obligatoire

Chaque mission déléguée inclut **obligatoirement** :

- Le **nom de l'agent de retour en texte clair** (le coordinateur), **sans lien de mention actif vers lui-même** : la pose du lien de retour actif et le passage en `in_review` reviennent à l'agent délégataire en fin de tâche. L'obligation de retour A2A a **une seule source non contournable** — la « Checklist de sortie de stage » de [`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md) — et n'est pas redéfinie ici (voir aussi [`../../protocols/governance-security.md`](../../protocols/governance-security.md), « Règle A2A »).
- Le **tag de méthodologie** sur l'issue déléguée (**contexte Multica uniquement**) : toute issue confiée à l'**OpenSpec Expert** (cycle spec-driven, OpenSpec activé) est taguée **`OpenSpec`** — `multica issue label add <issue-id> <label-id>`, l'id du label résolu via `multica label list --output json` (créer le label `OpenSpec` via `multica label create` s'il n'existe pas). Ce tag rend visible, dès le découpage, quelles issues relèvent de la méthode OpenSpec. Les labels d'issue étant **propres à Multica**, l'étape est sautée hors Multica. L'**OpenSpec Expert pose aussi ce tag en première action** s'il traite une issue Multica (voir [`../../../agents/openspec-agent.md`](../../../agents/openspec-agent.md)) : le premier des deux qui agit suffit, l'autre est idempotent.

### Step 4 — Visualiser le workflow retenu (diagramme en code, syntaxe validée) sur l'issue

## Sensors

Outputs: tâches de livrable en backlog (agents assignés) + sous-tâche ADR bloquante créée ensuite (si impact structurant), tâches lancées à l'ADR `done` + diagramme du workflow retenu.
Imports: `diagram-validity`.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de découpage, affectation d'agents récurrente) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
