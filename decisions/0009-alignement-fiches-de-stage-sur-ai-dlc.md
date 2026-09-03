# Alignement des fiches de stage sur le contrat AI-DLC « Anatomy of a Stage »

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : (en attente de validation humaine)
accepté le : (en attente)
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** tant que la validation humaine granulaire et le contrôle sécurité (Reviewer de sécurité) sur la nouvelle surface (vocabulaire de délégation, revue adversariale) ne sont pas obtenus. Passera à **Accepted** après validation humaine explicite (invariant : aucun ADR accepté sans validation humaine).

## Contexte

Les 20 fiches de stage (`core/common/stages/<phase>/<slug>.md`), portées par [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md), adoptaient déjà le triptyque conductor / stages / protocols et un front-matter machine-lisible. Trois écarts subsistaient vis-à-vis du contrat AI-DLC « Anatomy of a Stage » (Harness Engineer Guide, `harness-engineering/01-anatomy-of-a-stage`) :

1. **Corps non normé** — chaque fiche avait `## Objectif` / `## Steps` / `## Gate / sortie`, alors qu'AI-DLC impose un **corps en trois compartiments, dans l'ordre fixe** `## Steps` / `## Sensors` / `## Learn` (le parseur ne lit que le front-matter ; l'agent ne lit que le corps).
2. **Vocabulaire `mode` divergent** — la valeur maison `multi-agent` ne fait pas partie de l'ensemble AI-DLC `inline | subagent | pipeline | mob` (topologies de communication).
3. **`review_class` conflée** — les valeurs maison `advisory | granular | explicit | none` mélangeaient la **nature** de la revue et la **force** du gate ; AI-DLC sépare la nature (`review_class: adversarial | advisory | none` + `review_artifact`) de tout autre axe. Le champ `for_each` (itération une-fois-par-unité) était par ailleurs absent.

Ces écarts sont traités par l'issue ALI-195 (Stage 2 de l'alignement AI-DLC, parente ALI-193), sans importer le tooling non applicable (`bun`, compilation `stage-graph.json`) — cohérent avec [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md) et [ADR-0005](0005-verification-gates-et-sensors.md).

## Décision

**Aligner les 20 fiches sur le contrat « Anatomy of a Stage »** — corps en trois compartiments, vocabulaire `mode`/`review_class` AI-DLC, `for_each`, liaison de sensors — **en traçant les divergences maison assumées** plutôt qu'en important le tooling.

### 1. Corps en trois compartiments (ordre fixe)

Chaque fiche porte désormais, après le front-matter, `## Steps` → `## Sensors` → `## Learn` :

- **`## Steps`** — prose impérative (le travail métier), inchangée quant au fond.
- **`## Sensors`** — résumé local compact : `Outputs:` (où atterrissent les sorties + frontière de gate), `Imports:` **reflétant** le front-matter `sensors:` (`none` si vide), et `Upstream targets:` **reflétant** `consumes:` **uniquement quand** `upstream-coverage` est importé. Les exceptions propres au stage (ex. `Review artifact:`) y sont notées ; le comportement partagé reste dans [`stage-protocol.md`](../core/common/protocols/stage-protocol.md) (temps 4).
- **`## Learn`** — contrat de boucle d'apprentissage (voir divergence D-3 ci-dessous).

Le contrat est décrit dans [`stage-definition.md`](../core/common/protocols/stage-definition.md). Le corps est un **artefact de framework immuable en forme** ; la seule édition sanctionnée en cours de workflow est l'ajout d'un id de sensor à `sensors:`.

### 2. Vocabulaire `mode` (topologie de communication)

Adoption de l'ensemble AI-DLC `inline | subagent | pipeline | mob`. **Mapping maison** : `multi-agent → mob`. Les trois stages concernés — `design-and-decisions`, `walking-skeleton`, `detailed-deliverables` — font travailler plusieurs architectes **en parallèle contre le brouillon du lead** en une ronde d'objection bornée, ce que `mob` (maillage) décrit exactement, mieux que `pipeline` (chaîne ordonnée). Les trois ont `support_agents` non vide (contrainte AI-DLC : `pipeline`/`mob` exigent des supports). `requirements-analysis` reste `subagent` (délégation hub-and-spoke). `pipeline` reste inutilisé (aucun stage n'a de chaînage ordonné strict). `stage-protocol.md` §2 est mis à jour en conséquence.

### 3. `review_class` + `review_artifact`

Adoption du vocabulaire AI-DLC `adversarial | advisory | none`. **Mapping** :

- Stages à **Reviewer de sécurité** → `review_class: adversarial` (revue indépendante non substituable, plancher SG-3) : `design-and-decisions`, `security-consistency-check`, `walking-skeleton`, `deployment-under-validation`.
- Stages à **Reviewer de cohérence** → `review_class: advisory` (revue consultative) : `requirements-analysis`, `detailed-deliverables`, `mockups`.
- Sans reviewer → `review_class: none`.

`review_artifact` est ajouté partout où `reviewer != null`, nommant le livrable Markdown qui porte la section `## Review` (jamais déduit de l'ordre de `produces`). Deux corrections de cohérence :

- `feasibility-constraints` et `existing-context-loading` portaient `review_class: advisory` **sans** reviewer (support_agents = voix adoptées `inline`, pas une revue indépendante) → passés à `none`.
- `consolidation-handoff` portait `review_class: granular` avec `reviewer: null` → passé à `none` ; la **force du gate** reste sur `human_gate: granular` (voir D-2).

### 4. `for_each`

`for_each: unit-of-work` ajouté à `detailed-deliverables`, seul stage s'exécutant **une fois par unité de travail** (les livrables détaillés sont produits par unité). Les autres stages omettent le champ (exécution unique). L'agrégation se déduit du graphe.

### 5. Liaison de sensors

Les `sensors:` existants sont conservés et ne référencent que les trois manifestes présents (`required-sections`, `upstream-coverage`, `diagram-validity`). L'évaluation d'ajouts (traçabilité, sources) est **différée au Stage 5** (ALI-198, schéma des manifestes) : la liaison finale sera reprise une fois les manifestes conformes. Le compartiment `## Sensors` reflète fidèlement l'état courant (pull-authoring, aucun id orphelin).

## Divergences maison assumées (tracées)

- **D-1 — Pas de compilation `stage-graph.json`.** Multica n'exécute pas le moteur AI-DLC. Le graphe reste **conceptuel**, dérivé de `consumes` / `produces` / `requires_stage`. Conforme à [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md).
- **D-2 — Axe `human_gate` conservé.** AI-DLC porte la nature de revue sur `review_class` sans axe de force de gate déclaratif. Le workspace conserve `human_gate` (`none | light | granular | explicit`) comme **axe distinct** matérialisant la validation humaine granulaire (invariant de gouvernance A2A). `review_class` ne porte plus que la **nature** de la revue ; les anciennes valeurs `granular` / `explicit` de `review_class`, qui conflaient les deux axes, sont retirées.
- **D-3 — `## Learn` pointe vers la boucle maison, pas vers `memory.md`.** AI-DLC prescrit un journal `memory.md` à quatre rubriques tenu par le stage. Le workspace utilise la **boucle d'apprentissage maison** ([ADR-0004](0004-boucle-apprentissage-et-regles-persistantes.md)) : journal de candidats-règles **sur l'issue** pendant le travail, puis remontée / persistance des apprentissages **confirmés** au gate humain dans [`core/rules/`](../core/rules/README.md) (cycle capture → confirmation humaine → contrôle de conflit). Les stages d'Initialization tiennent le journal mais **sautent** l'interaction liée au gate (bootstrap déterministe). Cohérent avec le choix « conventions Markdown, moteur A2A Multica ».
- **D-4 — `pipeline` inutilisé.** Aucun stage n'a de chaînage ordonné strict de supports ; la valeur reste dans le vocabulaire pour un usage futur.

## Conséquences

### Positives

- **POS-001** : Les 20 fiches respectent le contrat « Anatomy of a Stage » (corps en 3 compartiments, ordre fixe) — directement lisibles par un lecteur AI-DLC.
- **POS-002** : `mode` et `review_class` alignés sur le vocabulaire AI-DLC ; contraintes de cohérence explicites (`pipeline`/`mob` ⇒ supports ; `reviewer != null` ⇒ `review_class != none` + `review_artifact`).
- **POS-003** : Séparation nette **nature de revue** (`review_class`) vs **force de gate** (`human_gate`) — plus de conflation.
- **POS-004** : `for_each` rend explicite l'itération une-fois-par-unité de la Construction.
- **POS-005** : Divergences assumées **tracées**, pas corrigées aveuglément (respect du cadrage ALI-193).

### Négatives

- **NEG-001** : Coexistence d'un vocabulaire AI-DLC (`review_class`) et d'un axe maison (`human_gate`) ; atténué par la documentation explicite dans `stage-definition.md` et la présente décision.
- **NEG-002** : La liaison fine de sensors reste partielle tant que le Stage 5 (ALI-198) n'a pas figé le schéma des manifestes ; atténué par le pull-authoring (aucun id orphelin) et le report explicite.
- **NEG-003** : Surface d'instructions de délégation enrichie (`mob`, revue adversariale) ⇒ à soumettre au contrôle sécurité avant *Accepted* (voir IMP-005).

## Alternatives étudiées

### ALT-001 — Mapper `multi-agent → pipeline`

**Raison du rejet** : `pipeline` est une **chaîne ordonnée** (chaque support voit l'amont) ; les stages concernés font contribuer les architectes **en parallèle** contre un brouillon commun — c'est un **maillage** (`mob`), pas une chaîne.

### ALT-002 — Conserver `review_class: granular | explicit`

**Raison du rejet** : conflait nature de revue et force de gate. La force de gate est déjà portée par `human_gate` ; garder les deux axes sur `review_class` dupliquerait l'information et divergerait du vocabulaire AI-DLC sans bénéfice.

### ALT-003 — Importer le journal `memory.md` d'AI-DLC pour `## Learn`

**Raison du rejet** : dupliquerait la boucle d'apprentissage maison déjà outillée et versionnée dans `core/rules/` ([ADR-0004](0004-boucle-apprentissage-et-regles-persistantes.md)), avec un canal d'écriture concurrent — risque de divergence et affaiblissement du contrôle de conflit à l'admission (SEC-5). La divergence D-3 est préférée.

## Notes d'implémentation

- **IMP-001** : 20 fiches réécrites (corps en 3 compartiments) ; front-matter mis à jour (`mode`, `review_class`, `review_artifact`, `for_each`).
- **IMP-002** : `stage-definition.md` — schéma étendu (topologies `mode`, `for_each`, `review_class` AI-DLC + `review_artifact`, contrat de corps en 3 compartiments, règles de cohérence) ; divergences D-2 et D-3 tracées inline.
- **IMP-003** : `stage-protocol.md` §2 — en-tête de délégation aligné (`subagent | pipeline | mob`, topologie par mode, note `for_each`).
- **IMP-004** : Corrections de cohérence `review_class`/`reviewer` sur `feasibility-constraints`, `existing-context-loading`, `consolidation-handoff` (voir Décision §3).
- **IMP-005** : Contrôle sécurité (Reviewer de sécurité) sollicité sur la nouvelle surface (vocabulaire de délégation `mob`, revue adversariale, `review_artifact` portant `## Review`) **avant** validation humaine et passage à *Accepted*.
- **IMP-006** : Liaison fine de sensors **différée** au Stage 5 (ALI-198) ; l'état courant (3 manifestes) est reflété fidèlement dans `## Sensors`.

## Références

- **REF-001** : [ADR-0004 - Boucle d'apprentissage et règles persistantes](0004-boucle-apprentissage-et-regles-persistantes.md)
- **REF-002** : [ADR-0005 - Verification gates et Sensors](0005-verification-gates-et-sensors.md)
- **REF-003** : [ADR-0007 - Adaptation au modèle conductor / stages / protocols](0007-adaptation-modele-conductor-stages-protocols.md)
- **REF-004** : [ADR-0008 - Alignement des définitions d'agents sur AI-DLC](0008-alignement-definitions-agents-sur-ai-dlc.md)
- **REF-005** : Issue ALI-195 (Stage 2 — Stages) ; issue parente ALI-193 ; analyse ALI-184.
- **REF-006** : [AI-DLC — Anatomy of a Stage](https://awslabs.github.io/aidlc-workflows/harness-engineering/01-anatomy-of-a-stage/) ; [AI-DLC workflows (awslabs)](https://github.com/awslabs/aidlc-workflows)
