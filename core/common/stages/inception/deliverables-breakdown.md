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
produces: [decoupage_livrables]
consumes: [{artifact: besoins_traces, required: true}, {artifact: verdict_impact_structurant, required: true}]
requires_stage: [requirements-analysis]
sensors: []
scopes: [standard, feature, infra, mvp, enterprise]
inputs: "Besoins tracés + verdict d'impact structurant"
outputs: "Impact structurant Oui ⇒ issue ADR parente créée en premier (déléguée à l'Architecte de solution), issue d'origine passée en blocked ; ses sous-issues de livrable (une par spécialiste/architecte, hors revues, agent assigné, backlog) ne sont créées qu'après acceptation humaine de l'ADR, puis l'ADR passe en blocked. ADR refusée ⇒ ADR et issue d'origine annulées (cancelled) en cascade. Toutes les sous-issues done ⇒ ADR done puis issue d'origine done (dérivé). Impact structurant Non ⇒ issues de livrable créées directement en backlog ; si enfants de l'issue d'origine, celle-ci est blocked jusqu'à leur achèvement."
---

# Planification et découpage en livrables

## Objectif

Découper le travail en livrables et désigner l'agent responsable de chacun.

## Steps

### Step 1 — Déterminer phases, étapes et profondeur

### Step 2 — Découper et désigner l'agent responsable

- Documentation d'architecture / décisions structurantes / Patrons d'architecture / diagrammes → **Architecte de solution**.
- Analyse et cycle de vie des données (modélisation, gouvernance, classification, `10-cycle_vie_donnees.md`) → **Architecte de données** (délégué par l'Architecte de solution, qui valide le livrable — critère : sensor `data-lifecycle`).
- Choix AWS, diagrammes AWS, coûts → **Architecte AWS** (si AWS requis).
- Administration / infrastructure Windows → **Infrastructure Windows** (si concerné).
- Cycle spec-driven → **OpenSpec Expert** (uniquement si OpenSpec activé).

> **Pré-requis — verdict de méthodologie.** Toute condition « **si OpenSpec activé** » de ce stage (Steps 3.3 et 4, délégation à l'OpenSpec Expert) s'appuie sur le **verdict de méthodologie** analysé et tracé au cadrage ([`intake-framing`](intake-framing.md), Step 3 ; règle « Activation conditionnelle d'une méthodologie » de [`conductor.md`](../../conductor.md)). Le coordinateur **lit ce verdict** avant de découper ; s'il est **absent ou ambigu**, il ne devine pas et ne traite pas OpenSpec comme inactif par défaut : **halt-and-ask** (faire statuer l'humain, puis l'inscrire dans la description du projet). Le même principe vaut pour toute autre méthodologie déclarée.

### Step 3 — Flux impact structurant (ADR d'abord, livrables en sous-issues)

Dès que le **verdict d'impact structurant** établi au cadrage ([`intake-framing`](intake-framing.md), Step 5) vaut **`Oui`**, l'ordre est **inversé par rapport au reste du stage** : **rien n'est créé avant l'ADR**. L'**issue ADR est créée en premier** et devient l'**issue parente** de la décision ; les livrables n'existent qu'**après acceptation humaine**, en **sous-issues (enfants)** de cette ADR. S'il y a plusieurs décisions structurantes, appliquer ce flux **une fois par ADR**. En cas de doute sur le verdict, halt-and-ask.

```mermaid
flowchart TD
    Start([Impact structurant = Oui]) --> A1
    A1["1 · Création de l'issue ADR<br/>par l'Architecte de solution — issue parente<br/>issue d'origine → blocked"] --> A2
    A2["2 · Revue de cohérence"] --> A3
    A3["3 · Revue de sécurité"] --> Prop["ADR Proposée"]
    Prop --> Gate{"4 · Gate humaine"}
    Gate -->|Refusée| KO["ADR → cancelled<br/>issue d'origine → cancelled (cascade)<br/>flux clôturé — aucun livrable"]
    Gate -->|Acceptée| Issues["Création des sous-issues de livrables<br/>enfants de l'ADR · 1 spécialiste / architecte par issue<br/>backlog · agent assigné · puis lancées<br/>ADR (parente) → blocked"]
    Issues --> Run["Sous-issues : todo → in_progress → done"]
    Run --> Check{"Toutes les sous-issues done ?"}
    Check -->|Non| Run
    Check -->|Oui| Done["ADR → done, puis issue d'origine → done (dérivé)"]
```

#### Step 3.1 — Créer l'issue ADR (parente), déléguée à l'Architecte de solution

Le coordinateur crée l'**issue ADR**, déléguée à l'**Architecte de solution**, qui conduit son cycle au stage [`design-and-decisions`](design-and-decisions.md) : production mob → revue de cohérence → revue de sécurité → **ADR Proposée** → décision humaine granulaire. C'est un **garde-fou non contournable** (voir [`conductor.md`](../../conductor.md), « Garde-fous ») : un impact structurant ne peut jamais être traité sans son issue ADR.

> **L'issue d'origine est bloquée dès la création de l'issue ADR.** L'issue ADR étant une **sous-issue de l'issue d'origine** (celle que l'humain a ajoutée et qui a déclenché le flux), le coordinateur passe l'**issue d'origine en `blocked`** (`multica issue status <id-origine> blocked`) dès qu'il crée et lance l'issue ADR. L'issue d'origine **ne reprend jamais** tant que le flux ADR n'est pas terminé : son déblocage est **dérivé** (voir Step 3.2 pour le refus et Step 3.4 pour la clôture). C'est le garde-fou « Issue parente bloquée tant que ses sous-issues ne sont pas terminées » ([`conductor.md`](../../conductor.md), « Garde-fous »).

> **Tout le cycle de revue se déroule sur l'issue ADR.** Les deux revues de l'ADR (cohérence puis sécurité) sont **sollicitées et postées sur cette issue ADR**, jamais sur l'issue d'origine qui a déclenché le flux : la piste d'audit de la décision reste entière sur l'issue qui la porte (voir l'encadré d'ouverture de [`../../protocols/reviewer.md`](../../protocols/reviewer.md) et [`design-and-decisions`](design-and-decisions.md), Steps 2–3).

#### Step 3.2 — Gate humaine : accepter ou refuser

- **ADR acceptée (Keep)** ⇒ le coordinateur crée les **sous-issues de livrable** (Step 3.3), puis les lance.
- **ADR refusée** ⇒ l'issue ADR passe à **`cancelled`** ; aucun livrable n'est créé, le flux se clôt. **L'issue d'origine qui a déclenché le flux est annulée en cascade** : le coordinateur la passe également à **`cancelled`** (`multica issue status <id-origine> cancelled`) — un refus d'ADR ne laisse jamais l'issue d'origine ouverte ou bloquée en suspens. Si l'humain reformule la décision, c'est une **nouvelle** issue d'origine (et une nouvelle issue ADR) qui est relancée.

#### Step 3.3 — Sous-issues de livrable, créées **seulement après acceptation** (enfants de l'ADR)

Pour chaque délégation, le coordinateur crée une **sous-issue** rattachée à l'ADR (`--parent <id-ADR>`), en **`backlog`** avec son **agent délégataire assigné** (`--assignee-id`, UUID résolu, jamais deviné), puis la lance (`multica issue status <id> todo`, qui démarre l'agent) avec mention A2A. **Une fois toutes les sous-issues de livrable créées et lancées, le coordinateur passe l'issue ADR (parente) en `blocked`** (`multica issue status <id-ADR> blocked`) : elle le reste tant que ses sous-issues ne sont pas toutes terminées (garde-fou « Issue parente bloquée », voir Step 3.4 pour le déblocage dérivé).

> **Directives complètes, dérivées de l'ADR acceptée.** L'agent délégataire démarre « à froid » : il **ne voit pas** le fil de l'ADR ni le contexte du coordinateur. Chaque sous-issue doit donc être **autosuffisante** et **reporter explicitement les décisions de l'ADR acceptée** qui conditionnent le livrable — sans quoi l'agent ne peut pas exécuter correctement. Le coordinateur **puise ces directives dans l'ADR tranchée** (`decisions/<NNNN>-<titre>.md`) et les inscrit dans la description de la sous-issue : voir [« Mission déléguée — contenu obligatoire »](#mission-déléguée--contenu-obligatoire) ci-dessous. En cas d'information manquante dans l'ADR pour cadrer un livrable, halt-and-ask plutôt que deviner.

Voir aussi la [règle « une sous-issue par agent »](#une-issue-par-spécialiste--architecte-hors-revues--règle-de-délégation) ci-dessous.

**Uniquement si OpenSpec activé** : ajouter de même une sous-issue dédiée au cycle spec-driven OpenSpec (création / modification / suppression de spécifications), déléguée à l'OpenSpec Expert.

#### Step 3.4 — Clôture de l'ADR quand tous les livrables sont terminés

L'issue ADR reste **`blocked` comme parente** tant que ses sous-issues tournent. Dès que **toutes** ses sous-issues sont `done`, le coordinateur passe l'**issue ADR à `done`** (`multica issue status <id-ADR> done`) : clôture **dérivée** de l'état des enfants, **sans acte humain supplémentaire**. L'issue ADR étant elle-même une sous-issue de l'**issue d'origine** (restée `blocked` depuis Step 3.1), sa clôture **débloque l'issue d'origine en cascade** : le coordinateur passe l'**issue d'origine à `done`** (`multica issue status <id-origine> done`) — le flux ne se poursuit sur l'issue d'origine qu'**après** la fin complète du flux ADR et de ses livrables, jamais avant.

### Step 4 — Sans décision structurante (`verdict Non`) : livrables directs en backlog

Pas d'ADR : le coordinateur crée directement les **issues de livrable** (une par spécialiste / architecte), en **`backlog`** avec agent assigné (`--assignee-id`, UUID résolu), **sans parent ADR**, puis les promeut selon le séquencement du stage. **Uniquement si OpenSpec activé**, ajouter de même l'issue du cycle spec-driven OpenSpec.

> **Issue d'origine bloquée tant que ses livrables tournent.** Lorsque ces issues de livrable sont créées comme **sous-issues de l'issue d'origine** (`--parent <id-origine>`), le coordinateur passe l'**issue d'origine en `blocked`** une fois les livrables lancés et ne la débloque (`done`) que lorsque **tous** sont `done` — même garde-fou que sur le flux ADR (« Issue parente bloquée tant que ses sous-issues ne sont pas terminées », [`conductor.md`](../../conductor.md), « Garde-fous »). Déblocage **dérivé** de l'état des enfants, sans acte humain supplémentaire.

#### <a id="une-issue-par-spécialiste--architecte-hors-revues--règle-de-délégation"></a>Une issue par spécialiste / architecte (hors revues) — règle de délégation

Chaque **délégation de livrable** donne lieu à **une issue dédiée par agent** (Architecte de solution, Architecte de données, Architecte AWS, Infrastructure Windows, OpenSpec Expert) — **jamais** une issue fourre-tout partagée. Chaque issue porte un périmètre, des critères d'acceptation et l'agent de retour (le coordinateur, en texte clair) propres à l'agent délégataire.

**Les revues ne sont pas des issues.** Les **revues** (Reviewer de cohérence, Reviewer de sécurité) sont des fonctions *review-only* **sollicitées en place par le coordinateur** sur l'issue qui porte l'artefact revu — l'**issue ADR dédiée** sur impact structurant (jamais l'issue d'origine), l'issue du livrable sinon (voir [`protocols/reviewer.md`](../../protocols/reviewer.md)) ; elles postent leurs conclusions dans cette issue, **sans issue dédiée**. La règle « une issue par agent » ne vaut donc **que** pour les délégations de production de livrable.

#### <a id="mission-déléguée--contenu-obligatoire"></a>Mission déléguée — contenu obligatoire

Chaque mission déléguée inclut **obligatoirement** :

- Le **contexte de décision issu de l'ADR** (sur impact structurant) : la mission **reporte explicitement**, depuis l'ADR acceptée (`decisions/<NNNN>-<titre>.md`), les éléments qui cadrent le livrable — **option retenue et sa justification**, **contraintes et exigences** imposées (technologie, frontières de système, modèle de données, intégration, sécurité, infrastructure, patterns transverses), **périmètre précis** confié à cet agent et **ce qui en est explicitement exclu**, **critères d'acceptation**, **dépendances** vers d'autres livrables, et **référence à l'ADR parente** (lien / numéro). Objectif : l'agent délégataire, qui démarre sans le contexte du coordinateur, dispose de **toutes** les directives pour exécuter sans redemander ni deviner. (Hors impact structurant — Step 4 —, la mission reporte de même les décisions de cadrage pertinentes.)
- Le **nom de l'agent de retour en texte clair** (le coordinateur), **sans lien de mention actif vers lui-même** : la pose du lien de retour actif et le passage en `in_review` reviennent à l'agent délégataire en fin de tâche. L'obligation de retour A2A a **une seule source non contournable** — la « Checklist de sortie de stage » de [`stage-protocol.md`](../../protocols/stage-protocol.md) — et n'est pas redéfinie ici (voir aussi [`governance-security.md`](../../protocols/governance-security.md), « Règle A2A »).
- Le **tag de méthodologie** sur l'issue déléguée (**contexte Multica uniquement**) : toute issue confiée à l'**OpenSpec Expert** (cycle spec-driven, OpenSpec activé) est taguée **`OpenSpec`** — `multica issue label add <issue-id> <label-id>`, l'id du label résolu via `multica label list --output json` (créer le label `OpenSpec` via `multica label create` s'il n'existe pas). Ce tag rend visible, dès le découpage, quelles issues relèvent de la méthode OpenSpec. Les labels d'issue étant **propres à Multica**, l'étape est sautée hors Multica. L'**OpenSpec Expert pose aussi ce tag en première action** s'il traite une issue Multica (voir [`openspec-agent.md`](../../../agents/openspec-agent.md)) : le premier des deux qui agit suffit, l'autre est idempotent.

## Sensors

Outputs: impact structurant Oui ⇒ issue ADR parente d'abord (issue d'origine → `blocked`), ses sous-issues de livrable (backlog, agents assignés) créées et lancées après acceptation humaine puis l'ADR → `blocked` ; ADR refusée ⇒ ADR et issue d'origine → `cancelled` (cascade) ; ADR `done` quand toutes ses sous-issues sont `done`, puis issue d'origine → `done` (dérivé) ; impact structurant Non ⇒ issues de livrable directes en backlog (issue d'origine → `blocked` si elles en sont les enfants, jusqu'à leur achèvement).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de découpage, affectation d'agents récurrente) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
