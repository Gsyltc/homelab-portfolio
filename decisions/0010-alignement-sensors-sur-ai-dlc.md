# Alignement des manifestes de sensors sur le contrat AI-DLC « Sensors »

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : (en attente de validation humaine)
accepté le : (en attente)
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** tant que la validation humaine granulaire et le contrôle sécurité (Architecte cybersécurité) sur la surface des manifestes ne sont pas obtenus. Passera à **Accepted** après validation humaine explicite (invariant : aucun ADR accepté sans validation humaine). Aucune posture de sécurité n'est modifiée ici : les clauses SG-1 à SG-6 ([ADR-0005](0005-verification-gates-et-sensors.md)) sont préservées à l'identique et le caractère advisory est reconduit.

## Contexte

Les sensors ont été introduits en [ADR-0005](0005-verification-gates-et-sensors.md) (Stage 4, ALI-188) avec un **schéma de manifeste maison** (`type`, `nature`, `priority`, `origine`, `triggers`, `checks`, `output`) et trois manifestes advisory (`required-sections`, `upstream-coverage`, `diagram-validity`).

Le Stage 5 de l'alignement AI-DLC (issue ALI-198, parente ALI-193) porte ces manifestes sur le contrat **« Sensors »** du *Harness Engineer Guide* (`awslabs/aidlc-workflows`, [chapitre Sensors](https://awslabs.github.io/aidlc-workflows/harness-engineering/06-sensors/)). Ce contrat pose un **descripteur de capacité pur** en front-matter — cinq champs obligatoires (`id`, `kind`, `command`, `default_severity`, `description`) et des champs optionnels (`category`, `fire_on`, `matches`) — le manifeste ne citant **jamais** de stage : la liaison stage ↔ sensor vit côté stage (`sensors:`), c'est le **pull-authoring** (déjà en place dans le dépôt, à maintenir).

Trois écarts vis-à-vis du contrat étaient à traiter, sans importer le tooling non applicable (dispatcher `.ts`, `bun`, hook `PostToolUse`, resolver `aidlc-graph.ts`) — cohérent avec le cadrage [ADR-0001](0001-alignement-core-workflow-sur-ai-dlc-2.0.md) et [ADR-0005](0005-verification-gates-et-sensors.md) :

1. **Schéma de front-matter** — le schéma maison ne portait ni `kind`, ni `command`, ni `default_severity` (l'axe sévérité était le champ `nature`), ni `fire_on` / `matches` (le déclenchement était le champ `triggers`).
2. **Sort de `command`** — champ obligatoire chez AI-DLC (préfixe d'invocation exécuté par le dispatcher), sans objet sur un dépôt doc-first sans exécutable.
3. **Couverture** — 3 sensors présents ; AI-DLC en livre six (dont `claim-sources`, `traceability`, `linter`, `type-check`) : évaluer les ajouts pertinents doc-first.

## Décision

**Aligner les manifestes sur le contrat « Sensors »** — front-matter conforme, `fire_on` / `matches`, sensors additionnels doc-first — **en traçant les divergences maison assumées** plutôt qu'en important le tooling.

### 1. Schéma de front-matter conforme

Chaque manifeste porte désormais le descripteur de capacité AI-DLC :

```yaml
id: <kebab-case, = stem du fichier>   # obligatoire
kind: deterministic                    # obligatoire (seule valeur acceptée)
command: <préfixe d'invocation>        # obligatoire — voir DIV-command
default_severity: advisory             # obligatoire (advisory | blocking)
description: <une ligne>               # obligatoire
category: <label libre>                # optionnel (document-shape | provenance | traceability)
fire_on: <write | gate>                # optionnel — défaut write
matches: <glob>                        # optionnel — filtre de chemin
origine: ALI-<n>                        # champ maison conservé (provenance SG-1)
```

Le champ maison `nature` est remplacé par `default_severity` ; `priority` passe du front-matter au titre / corps (mention *prioritaire* / *complémentaire*) ; `triggers` est remplacé par `matches` (+ `fire_on`) ; `checks` et `output`, qui décrivaient la sémantique de vérification, passent dans le **corps** du manifeste (comme les manifestes AI-DLC qui portent la logique en prose de corps). L'invariant `id` = stem du fichier est respecté.

### 2. `fire_on` / `matches`

- `required-sections` → `fire_on: gate` (check de forme documentaire évalué une fois par livrable au gate) ; `matches` = ADR + DAS.
- `upstream-coverage` → `fire_on: gate` (évalué en ensemble sur les livrables de l'étape) ; `matches` = ADR + DAS + livrables.
- `diagram-validity` → `fire_on: write` (feedback incrémental rapide à l'écriture d'un diagramme) ; `matches` = `**/*.md` (blocs intégrés) + `.puml` + `.dsl`.
- `claim-sources` → `fire_on: gate` ; `matches` = DAS + ADR.
- `traceability` → `fire_on: gate` ; `matches` = DAS + ADR + livrables.

`fire_on: gate` est retenu pour les checks transverses ou « ensemble de livrables » ; `write` pour le seul check à feedback incrémental utile (syntaxe de diagramme). Conforme à la règle AI-DLC : `write` pour du feedback incrémental, `gate` pour du contrôle whole-deliverable / cross-file.

### 3. Sensors additionnels (couverture doc-first)

Deux ajouts pertinents pour un dépôt majoritairement documentaire, adaptés des sensors AI-DLC homonymes :

- **`claim-sources`** *(category: provenance, gate)* — adaptation de `aidlc-claim-sources` : chaque affirmation retenue (intention capturée, DAS, ADR) porte une **source résoluble** ; les hypothèses conservées correspondent à une **confirmation humaine explicite** tracée sur l'issue.
- **`traceability`** *(category: traceability, gate)* — adaptation de `aidlc-traceability` : cohérence de la **chaîne exigence → ADR → livrable**, identifiants amont stables, **absence d'orphelin dérivé**. Complémentaire de `upstream-coverage` (qui vérifie la *citation* d'amont) et recoupe `liaison-tracabilite` / `absence-orphelin` du verification gate.

**`linter` et `type-check` restent N/A** tant que le dépôt ne produit ni code ni IaC (repli « stratégie de tests » de l'axe de vérification, [ADR-0003](0003-scopes-et-axes-depth-verification.md)) ; ils seront ajoutés le jour où un livrable exécutable apparaît.

### 4. Sévérité : advisory par défaut (reconduit)

Les cinq sensors sont `default_severity: advisory`. Chez AI-DLC, `blocking` est **enforcé au gate** (`fire_on: gate`). Ici, le caractère advisory est une **décision de gouvernance A2A** ([ADR-0005](0005-verification-gates-et-sensors.md)) : gates et sensors ne bloquent jamais la validation humaine granulaire, ne la remplacent pas, et ne remplacent pas le contrôle sécurité systématique. Le passage d'un sensor à `blocking` reste une décision structurante explicite (ADR + contrôle sécurité).

## Divergences maison assumées (tracées)

- **DIV-command — `command` non exécutable.** Le dépôt est **doc-first** et n'embarque pas le dispatcher AI-DLC (`.ts`, `bun`, hook `PostToolUse` / `gate-start`). Le champ obligatoire `command` porte un **placeholder tracé** (`non-exécutable (advisory documentaire) — voir ADR-0010`) : les sensors restent des **conventions documentées** advisory ; le corps du manifeste fixe la sémantique (`checks`, `output`, garde-fous) pour qu'un outillage (script / CI) puisse être ajouté ultérieurement **sans redécider** le fond. Cohérent avec la « nature déclarative non exécutable » de [ADR-0005](0005-verification-gates-et-sensors.md).
- **DIV-prefix — pas de préfixe `aidlc-`.** AI-DLC exige `core/sensors/aidlc-<id>.md` : le resolver `loadSensors` (`SENSOR_FILE_REGEX = /^aidlc-([a-z][a-z0-9-]*)\.md$/`) **ignore silencieusement** tout fichier sans préfixe. Multica n'exécute pas ce resolver ; les manifestes restent sous `core/sensors/sensors/<id>.md` **sans préfixe**, en conservant l'invariant `id` = stem du fichier. Un dispatcher futur devra soit renommer avec le préfixe, soit adapter le regex.
- **DIV-advisory — advisory par défaut.** Voir Décision §4 : `blocking` non employé (décision de gouvernance), là où AI-DLC l'autorise au gate.
- **DIV-champs — `input_schema` / `output_schema` / `timeout_seconds` omis.** Champs du dispatcher exécutable (schéma d'entrée / sortie, délai), non applicables tant que les sensors ne sont pas outillés. Le champ maison `origine` est conservé (exigence de provenance SG-1, [ADR-0005](0005-verification-gates-et-sensors.md)).
- **DIV-graph — pas de compilation de graphe de sensors.** Aucune résolution compile-time des imports `sensors:` (pas de `stage-graph.json`) : la cohérence « aucun id orphelin » est vérifiée par convention / revue (recoupe le Stage 6, ALI-199). Cohérent avec [ADR-0009 (stages)](0009-alignement-fiches-de-stage-sur-ai-dlc.md), divergence D-1.

## Conséquences

### Positives

- **POS-001** : Les cinq manifestes portent le descripteur de capacité AI-DLC (`id` / `kind` / `command` / `default_severity` / `description` + `category` / `fire_on` / `matches`) — directement lisibles par un lecteur AI-DLC.
- **POS-002** : `fire_on` / `matches` remplacent `triggers` : distinction explicite write vs gate et filtre de chemin borné (recoupe SG-4, globs bornés au repo).
- **POS-003** : Couverture doc-first renforcée (`claim-sources`, `traceability`) sur les axes provenance et traçabilité, complémentaires des gates et de `upstream-coverage`.
- **POS-004** : Pull-authoring conservé (les stages importent par id nu) ; aucun champ de ciblage de stage introduit côté manifeste.
- **POS-005** : Divergences assumées **tracées**, pas corrigées aveuglément (respect du cadrage ALI-193) ; posture de sécurité (SG-1 à SG-6) et caractère advisory inchangés.

### Négatives

- **NEG-001** : Coexistence d'un front-matter AI-DLC et d'un champ maison `origine` ; atténué par la documentation explicite (README § Format) et la présente décision.
- **NEG-002** : `command` en placeholder tant que non outillé : un lecteur AI-DLC doit lire DIV-command pour comprendre qu'aucune commande n'est réellement exécutée.
- **NEG-003** : Absence de préfixe `aidlc-` : un import du dispatcher AI-DLC tel quel ne découvrirait pas les manifestes (DIV-prefix) — assumé tant que l'exécution passe par Multica.
- **NEG-004** : Deux nouveaux sensors à maintenir cohérents avec les gabarits d'ADR / DAS et les gates.

## Alternatives étudiées

### ALT-001 — Fournir une `command` réelle exécutable dès maintenant

Écrire des scripts / hooks exécutables et référencer une vraie commande.

**Raison du rejet** : figer une implémentation avant d'avoir stabilisé la sémantique et sans moteur d'exécution Multica pour les hooks créerait de la reprise ; contraire à la « nature déclarative non exécutable » de [ADR-0005](0005-verification-gates-et-sensors.md). Retenu : placeholder tracé (DIV-command), outillage ultérieur sans redécision.

### ALT-002 — Adopter le préfixe `aidlc-` sur les fichiers

Renommer en `core/sensors/aidlc-<id>.md` pour matcher le resolver AI-DLC.

**Raison du rejet** : le resolver AI-DLC n'est pas importé (exécution Multica) ; le préfixe n'apporterait aucune découverte réelle et alourdirait les chemins, tout en imposant de dé-préfixer les `id` importés côté stage. Retenu : sans préfixe, `id` = stem (DIV-prefix), à réévaluer si un dispatcher est un jour importé.

### ALT-003 — Rendre `claim-sources` / `traceability` bloquants au gate

Enforcer ces deux checks comme AI-DLC l'autorise.

**Raison du rejet** : contredirait la décision de gouvernance advisory ([ADR-0005](0005-verification-gates-et-sensors.md)) et déplacerait le pouvoir de décision vers un automate non outillé. Retenu : advisory par défaut ; passage à `blocking` = décision ADR + contrôle sécurité.

## Notes d'implémentation

- **IMP-001** : 3 manifestes réécrits (`required-sections`, `upstream-coverage`, `diagram-validity`) au schéma conforme ; `checks` / `output` déplacés dans le corps.
- **IMP-002** : 2 manifestes créés (`claim-sources`, `traceability`) sous `core/sensors/sensors/`, `origine: ALI-198`.
- **IMP-003** : [`core/sensors/README.md`](../core/sensors/README.md) — table « Sensors définis » (5 sensors, colonnes `category` / `fire_on` / `default_severity`), section « Format d'un manifeste (contrat AI-DLC) » réécrite, section « Divergences assumées » ajoutée (DIV-command / DIV-prefix / DIV-advisory / DIV-champs).
- **IMP-004** : `gates.md` inchangé — il référence les sensors par id stable (`diagram-validity`, `required-sections`) toujours valides ; son propre schéma (`type: verification-gates`) est hors périmètre de cette décision (sensors).
- **IMP-005** : Liaison fine des `sensors:` des stages **différée / confirmée au Stage 6** (ALI-199, vérification globale) : les ids importés (`required-sections`, `upstream-coverage`, `diagram-validity`) restent inchangés donc aucun import n'est orphelin ; l'ajout éventuel de `claim-sources` / `traceability` à des stages relève de la vérification d'ensemble et de la boucle d'apprentissage.
- **IMP-006** : Contrôle sécurité (Architecte cybersécurité) sur la surface des manifestes **avant** validation humaine et passage à *Accepted* ; clauses SG-1 à SG-6 reconduites sans changement.

## Références

- **REF-001** : [ADR-0001 — Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [ADR-0003 — Scopes et axes Depth / vérification des livrables](0003-scopes-et-axes-depth-verification.md)
- **REF-003** : [ADR-0005 — Verification gates et Sensors](0005-verification-gates-et-sensors.md)
- **REF-004** : [ADR-0009 — Alignement des fiches de stage sur AI-DLC](0009-alignement-fiches-de-stage-sur-ai-dlc.md)
- **REF-005** : [AI-DLC Harness Engineer Guide — Sensors](https://awslabs.github.io/aidlc-workflows/harness-engineering/06-sensors/)
- **REF-006** : [`core/sensors/README.md`](../core/sensors/README.md) ; manifestes `core/sensors/sensors/*.md`
- **REF-007** : Issue ALI-198 (Stage 5 — Sensors) ; issue parente ALI-193 ; analyse ALI-184.
