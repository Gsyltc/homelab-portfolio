# Alignement de la mémoire de règles sur le contrat AI-DLC « Rules and the Learning Loop »

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : multica.gaston
accepté le : 2026-09-03
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — validation humaine explicite obtenue (multica.gaston, 2026-09-03). Le passage à Accepted supposait la validation humaine granulaire ; cette condition est satisfaite (invariant respecté : aucun ADR accepté sans validation humaine). Aucune règle n'est ajoutée / modifiée dans `core/rules/` par cet ADR : il **décide et trace la structure** de la mémoire de règles ; il ne passe pas par la boucle d'apprentissage (capture → confirmation → contrôle de conflit), réservée à l'**écriture de règles** (invariant SEC-5). Aucune posture de sécurité ni garde-fou de gouvernance n'est modifié.

## Contexte

La mémoire de règles multi-couches du workspace vit sous [`core/rules/`](../core/rules/), formalisée par l'[ADR-0004](0004-boucle-apprentissage-et-regles-persistantes.md) (*Accepted*) : quatre couches de précédence `workspace > project > phase > scope`, alimentées par une **boucle d'apprentissage** aux gates (journal d'observations → remontée des candidats → confirmation humaine granulaire → contrôle de conflit à l'admission → écriture), avec les clauses de sécurité **SEC-1 à SEC-5**.

Le Stage 4 de l'alignement AI-DLC 2.0 (issue ALI-197, parente ALI-193) porte cette mémoire sur le contrat **« Rules and the Learning Loop »** du *Harness Engineer Guide* (`awslabs/aidlc-workflows`). Le contrat amont fixe :

- **Cinq couches** résolues au démarrage de chaque workflow : `org → team → project → phase → stage`.
  - Fichiers sous `core/memory/` : `org.md`, `team.md`, `project.md`, `phases/<phase>.md`. **Pas de champ `scope:` de front-matter** : la portée est **dérivée du nom de fichier**.
  - Les quatre fichiers de phase sont `phases/ideation.md`, `phases/inception.md`, `phases/construction.md`, `phases/operation.md` (l'`initialization` est bootstrap-only et **ne livre aucun fichier de règles**).
  - `org.md` est **livré par le cadre** (défauts hérités) ; l'auteur travaille surtout aux couches `team` et `project`.
  - La cinquième couche — **règles par stage** (`aidlc-stage-<slug>.md`) — est **réservée pour une future version** : on ne peut pas en écrire aujourd'hui.
- **Modèle strict-additif** : toutes les règles applicables apparaissent **simultanément** dans le contexte de l'agent ; **aucune couche n'en écrase silencieusement une autre** au runtime. Pas de bloc `overrides:`, pas de mot-clé `enforcement:`. On énonce une règle **positivement** à la portée où elle s'applique.
- **Contrôle de conflit avant écriture, pas au runtime** : puisque rien n'écrase au runtime, une règle qui **contredit** une couche plus large est un problème que le résolveur ne peut pas trancher. Le contrôle est donc fait **à l'admission** (comparaison LLM au niveau de la rubrique avant l'écriture déterministe) — **revise / skip / escalate** — et non résolu à l'exécution. C'est un **aide-audit**, pas une frontière d'enforcement runtime.
- **Boucle d'apprentissage** : journal (`memory.md`, quatre rubriques Interpretations / Deviations / Tradeoffs / Open questions) → gate qui présente les candidats verbatim → confirmation → écriture datée, **portée par défaut `project`** (la plus étroite), promotion « un clic » vers `team`, **pas de chemin vers `org`**. Une variante `SENSOR_PROPOSED` transforme un apprentissage récurrent en **liaison de sensor** (scaffold de manifeste + ajout de l'id au `sensors:` du stage). Les apprentissages s'appliquent au **prochain** workflow, jamais à celui en cours.

Contrainte de cadrage (ALI-193, ALI-197) : adapter au moteur A2A **Multica** sans importer le tooling amont non applicable (`bun`, hooks `.ts`, `dist/<harness>/`, `.claude/sensors/`) ; **préserver** la précédence et le contrôle de conflit à l'admission (une règle basse ne contredit jamais une règle haute sans arbitrage humain) ; toute divergence assumée est **tracée en décision structurante**.

Quatre questions étaient à trancher (ALI-197) : (1) chaîne de couches — ajouter `stage` ? modéliser `org`/`team` ? conserver `scope` ? ; (2) emplacement `core/rules/` vs `core/memory/` ; (3) cohérence de la boucle d'apprentissage après ajustement des couches ; (4) templates.

## Décision

### 1. Chaîne de couches — quatre couches conservées, `stage` différée, `org`/`team` fusionnés dans `workspace`, `scope` maison conservée

La chaîne **`workspace > project > phase > scope`** de l'[ADR-0004](0004-boucle-apprentissage-et-regles-persistantes.md) est **conservée**, avec les positions suivantes :

- **Couche `stage` — NON ajoutée maintenant (différée), en miroir de l'amont.** AI-DLC réserve la couche `stage` (`aidlc-stage-<slug>.md`) « pour une future version » et **interdit d'en écrire une aujourd'hui**. Ajouter une couche `stage` maison irait *au-delà* de l'amont, alors que le contrat lui-même ne l'ouvre pas. Décision : **rester aligné sur l'amont** en ne créant pas la couche `stage` ; la granularité fine reste couverte par la couche `scope` (par scope) et par les fiches de stage elles-mêmes (comportement, non règles apprises). Réévaluable si l'amont ouvre la couche `stage` ou si un besoin réel de règle par-stage émerge.
- **`org`/`team` — assumés comme fusion dans `workspace`.** Le workspace Multica **est** l'organisation **et** l'équipe : il n'existe pas de frontière org/équipe distincte à modéliser (une seule équipe, un seul espace de gouvernance). La couche `workspace` (toujours chargée, précédence maximale) **tient lieu des deux couches amont `org` + `team`**. Divergence de nommage assumée : `workspace` ≡ `org` ⊕ `team`. Conséquence sur la boucle : là où l'amont a une promotion `project → team` (avec `org` livré par le cadre, jamais écrit par la boucle), le workspace a une promotion `project → workspace` qui, **parce qu'elle touche la couche des invariants**, reste soumise au **contrôle sécurité systématique** (SEC-4) — garde-fou plus strict que le « un clic » amont, cohérent avec le fait que `workspace` fusionne aussi le rôle `org` (défauts non abaissables).
- **Couche `scope` — conservée (divergence maison assumée, déjà tracée ADR-0004).** AI-DLC n'a pas de couche `scope` de règles (le mot « scope » y désigne les *profils de workflow* — nos `scopes-and-axes`). Notre couche `scope` de règles est un **pont explicite** avec le mécanisme de scopes de l'[ADR-0003](0003-scopes-et-axes-depth-verification.md) ; elle est **conservée** comme couche de plus faible précédence. Elle dépend du Stage 3 (ALI-196) pour la liste canonique des scopes (source d'identité `core/scopes/*.md`, PR séparée) — sans impact sur la présente structure de règles.

**Correction de cohérence (5 phases) — ajout de `phases/ideation.md`.** L'[ADR-0006](0006-passage-5-phases-et-mode-autonomie-construction.md) (*Accepted*) a fait passer le workspace à **5 phases** (`Initialization → Ideation → Inception → Construction → Operation`), mais la couche `phase` des règles ne comptait que trois fichiers (`inception`, `construction`, `operation`). L'amont livre **quatre** fichiers de phase (`ideation`, `inception`, `construction`, `operation`) et **aucun** pour `initialization` (bootstrap-only). Décision : **ajouter `core/rules/phases/ideation.md`** (couche `phase`, chargement à la demande), et **ne pas** créer de fichier `initialization` — exactement le partitionnement amont. La couche `phase` passe donc de 3 à **4 fichiers**, cohérente à la fois avec l'amont et avec l'ADR-0006.

### 2. Emplacement — `core/rules/` conservé (divergence assumée, déjà tranchée ADR-0004)

L'amont place les règles sous `core/memory/` (fichiers `org.md` / `team.md` / `project.md` / `phases/`). Le workspace **conserve `core/rules/`**, décision déjà prise à l'[ADR-0004](0004-boucle-apprentissage-et-regles-persistantes.md) (arbitrage Q-A) et **confirmée ici** :

- `core/rules/` est **cohérent avec les autres surfaces déclaratives maison** (`core/sensors/`, `core/common/`, cf. [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md) Q1) et **agnostique de méthodologie**, contrairement à `core/memory/` (nommage lié au moteur amont).
- Le nom `rules` **dit ce que le répertoire contient** (règles persistantes versionnées), là où `memory` recouvre chez l'amont un espace plus large (space memory, learnings, practices-discovery) non répliqué ici.
- Aucun tooling amont (`aidlc-learnings.ts`, `/aidlc --doctor`, résolveur `core/memory`) n'est importé : renommer vers `core/memory/` n'apporterait **aucun bénéfice d'exécution** et casserait les nombreux pointeurs vivants (`AGENTS.md`, `README.md`, `conductor.md`, protocoles, fiches de stage, sensors) au prix d'une pure conformité de nommage.

**Divergence assumée et tracée** : emplacement `core/rules/` (et non `core/memory/`) ; sous-répertoires `projects/`, `phases/`, `scopes/` (et non fichiers `project.md` / `team.md` à plat). La **portée reste dérivable du chemin** (nom de fichier + répertoire), dans l'esprit du contrat amont « pas de champ `scope:`, la portée vient du fichier ».

### 3. Boucle d'apprentissage — cohérente, et plus conservatrice que l'amont

Après ajustement des couches, la boucle d'apprentissage existante ([ADR-0004](0004-boucle-apprentissage-et-regles-persistantes.md)) **reste cohérente** avec le contrat amont, avec **deux renforcements assumés** :

- **Précédence effective vs strict-additif.** L'amont est *strict-additif* (toutes les règles coexistent, rien n'écrase au runtime) et repousse tout arbitrage de conflit **à l'admission** (revise / skip / escalate). Le workspace **énonce une précédence de couches** (`workspace > project > phase > scope`) **ET** applique un **contrôle de conflit à l'admission** : une règle basse **ne peut pas contredire** une règle haute sans **arbitrage humain** (jamais tranché seul par un agent). Les deux modèles convergent sur l'essentiel — **le conflit se règle à l'écriture, jamais silencieusement au runtime** — et notre précédence explicite est un **sur-ensemble conservateur** du strict-additif (elle donne une clé de lecture déterministe *et* refuse la contradiction à l'admission). Divergence assumée : nous n'implémentons pas la concaténation strict-additive runtime du moteur amont (pas de moteur), mais nous en **préservons l'invariant de sûreté** par la précédence + le contrôle d'admission.
- **Portée par défaut `project`, promotion contrôlée.** Aligné sur l'amont (défaut = couche la plus étroite `project`). La promotion `project → workspace` (équivalent du `project → team`/`org` amont, fusionnés) reste une **décision structurante** soumise au **contrôle sécurité systématique** (SEC-4) — plus strict que le « un clic » amont, justifié par la fusion `org`+`team` dans `workspace` (défauts non abaissables). Pas d'écriture directe en `workspace` hors boucle + contrôle (SEC-5).
- **Application différée.** Identique à l'amont : une règle apprise s'applique au **prochain** workflow, jamais en cours de route (ADR-0004 IMP-003, clause SEC-3).
- **`SENSOR_PROPOSED` — parallèle assumé.** L'amont, quand l'apprentissage est un *check récurrent* plutôt qu'une règle, scaffolde un manifeste de sensor et ajoute son id au `sensors:` du stage d'origine. Le workspace dispose du même levier conceptuel via `core/sensors/` (pull-authoring par id — [ADR-0005](0005-verification-gates-et-sensors.md)) ; l'articulation fine « apprentissage → liaison de sensor » relève du **Stage 5 (ALI-198)** et n'est pas figée ici. Noté comme point de cohérence à confirmer au Stage 5.

Aucun invariant (validation humaine granulaire, ADR, piste d'audit, contrôle sécurité minimal, garde-fous des scopes) n'est affaibli ; les clauses **SEC-1 à SEC-5** restent intégralement en vigueur.

### 4. Templates — alignés sur la convention de rubriques topicales de l'amont, IDs et précédence préservés

L'amont organise chaque fichier de règles en **prose sous des rubriques topicales** (`## Way of Working`, `## Testing Posture`, `## Deployment`, `## Code Style`…), une règle = une puce sous la rubrique idoine. Décision : **adopter la convention de rubriques topicales** dans les templates, **tout en préservant** les identifiants stables `RULE-<COUCHE>-NNN`, la mention de précédence et l'origine + date (traçabilité, invariant SEC-5).

- `projects/_template.md` et `scopes/_template.md` : rubriques topicales indicatives ajoutées ; format de règle `RULE-*` conservé ; note de précédence conservée ; exemple par défaut conservé.
- **Pas de template `stage`** : la couche `stage` étant différée (§1), aucun `stages/_template.md` n'est créé — cohérent avec l'amont qui interdit d'écrire une règle de stage aujourd'hui.
- Ajout du fichier de phase manquant `phases/ideation.md` (§1), au même format que les trois autres fichiers de phase (règles apprises `RULE-PH-NNN`, note de précédence).

## Conséquences

### Positives

- **POS-001** : Chaîne de couches **décidée et tracée** ; alignement maximal sur l'amont (pas de couche `stage` tant que l'amont ne l'ouvre pas ; `org`/`team` fusionnés dans `workspace` ; 4 fichiers de phase comme l'amont).
- **POS-002** : Cohérence **5 phases** rétablie entre l'[ADR-0006](0006-passage-5-phases-et-mode-autonomie-construction.md) et la couche `phase` des règles (ajout `phases/ideation.md`).
- **POS-003** : Emplacement `core/rules/` **confirmé** et justifié (cohérence maison, agnostique de méthodologie, zéro pointeur cassé) ; divergence assumée et tracée.
- **POS-004** : L'invariant de sûreté de l'amont (conflit réglé à l'écriture, jamais au runtime) est **préservé et renforcé** par la précédence explicite + le contrôle de conflit à l'admission.
- **POS-005** : Templates alignés sur la convention de **rubriques topicales** amont, **sans perdre** les IDs `RULE-*`, la précédence ni la traçabilité (SEC-5).

### Négatives

- **NEG-001** : Divergence de **nommage** persistante avec l'amont (`core/rules/` vs `core/memory/`, `workspace` vs `org`/`team`) ; atténuée par la documentation explicite et par la dérivabilité de la portée depuis le chemin.
- **NEG-002** : L'absence de couche `stage` peut nécessiter, si un besoin réel émerge, un ADR ultérieur d'ouverture (réévaluation liée à l'amont).
- **NEG-003** : La convention de rubriques topicales ajoute une légère charge de rangement au moment de l'écriture d'une règle (choisir la rubrique) ; atténuée par le caractère indicatif des rubriques et par la remontée guidée par le coordinateur.

## Alternatives étudiées

### ALT-001 — Ajouter une couche `stage` maison dès maintenant

Créer `core/rules/stages/<slug>.md` + template `stage`.

**Raison du rejet** : l'amont **réserve** la couche `stage` et **interdit d'en écrire une** aujourd'hui ; l'ajouter irait *au-delà* du contrat sans base amont, pour une granularité déjà couverte par la couche `scope` et par les fiches de stage. Différé, réévaluable si l'amont l'ouvre.

### ALT-002 — Modéliser `org` et `team` en couches distinctes

Créer `core/rules/org.md` + `core/rules/team.md` en plus de `workspace.md`.

**Raison du rejet** : le workspace **est** l'organisation et l'équipe ; il n'existe pas de frontière distincte à modéliser. Deux couches supplémentaires seraient vides et introduiraient une précédence sans portée réelle. `workspace` fusionne les deux (déjà l'orientation de l'ADR-0004 ALT-002).

### ALT-003 — Renommer `core/rules/` en `core/memory/`

Aligner littéralement l'emplacement sur l'amont.

**Raison du rejet** : aucun bénéfice d'exécution (pas de tooling amont importé), casse de nombreux pointeurs vivants, et `memory` recouvre chez l'amont un périmètre plus large (space memory / learnings / practices) non répliqué. `core/rules/` est plus explicite et cohérent avec les autres surfaces maison (ADR-0004 Q-A, ADR-0007 Q1).

### ALT-004 — Adopter le strict-additif pur (supprimer la précédence explicite)

Remplacer la précédence `workspace > project > phase > scope` par une simple concaténation strict-additive.

**Raison du rejet** : sans moteur qui compile la vue additive au démarrage, une concaténation « à plat » perdrait la clé de lecture déterministe et le refus de contradiction à l'admission — un affaiblissement de l'invariant de sûreté. La précédence explicite + le contrôle d'admission **préservent** l'invariant amont (conflit réglé à l'écriture) et le renforcent ; c'est un sur-ensemble conservateur, pas une contradiction.

## Notes d'implémentation

- **IMP-001** : `core/rules/README.md` mis à jour — note d'alignement AI-DLC (contrat « Rules and the Learning Loop ») ; tableau des couches enrichi (différé `stage`, fusion `org`/`team` → `workspace`, divergence `scope`, divergence emplacement `core/rules/` vs `core/memory/`) ; ajout de la phase `ideation` (couche `phase` = 4 fichiers) ; note « précédence explicite ⊇ strict-additif, conflit réglé à l'admission ».
- **IMP-002** : Fichier `core/rules/phases/ideation.md` **créé** (couche `phase`, chargement à la demande, format `RULE-PH-NNN`), pour cohérence avec l'[ADR-0006](0006-passage-5-phases-et-mode-autonomie-construction.md). Aucun fichier `initialization` (bootstrap-only, aligné amont).
- **IMP-003** : Templates `projects/_template.md` et `scopes/_template.md` mis à jour — rubriques topicales indicatives ; IDs `RULE-*`, note de précédence et exemple conservés. **Pas** de `stages/_template.md` (couche `stage` différée).
- **IMP-004** : Pointeurs — `README.md`, `AGENTS.md`, `CONTRIBUTING.md` : plage `decisions/` mise à jour pour inclure le présent ADR. **Coordination de numérotation** : les Stages 2 à 5 ayant été rédigés en parallèle sur des branches séparées, deux collisions (`0009`, `0010`) ont été détectées au Stage 6 (ALI-199) puis résolues par renumérotation validée par l'humain : fiches de stage `0009`, scopes `0010`, **règles `0011` (présent ADR)**, sensors `0012`. La plage des pointeurs est `0001…0012`.
- **IMP-005** : Aucune règle écrite dans `core/rules/` par cet ADR (structure uniquement) ; la boucle d'apprentissage (capture → confirmation → contrôle de conflit) et les clauses SEC-1..5 restent inchangées. L'articulation `SENSOR_PROPOSED` → liaison de sensor est déférée au **Stage 5 (ALI-198)**.
- **IMP-006** : Aucune modification de la posture de sécurité ni d'un garde-fou de gouvernance. Le renforcement de la promotion `project → workspace` (contrôle sécurité systématique, SEC-4) était déjà en vigueur ; il est seulement **explicité** dans le contexte de la fusion `org`+`team`.

## Références

- **REF-001** : Issue ALI-197 (Stage 4 — Rules : chaîne de couches, emplacement, précédence) ; issue parente ALI-193 ; analyse ALI-184.
- **REF-002** : [ADR-0004 - Boucle d'apprentissage et règles persistantes multi-couches](0004-boucle-apprentissage-et-regles-persistantes.md)
- **REF-003** : [ADR-0003 - Scopes et axes Depth / vérification des livrables](0003-scopes-et-axes-depth-verification.md)
- **REF-004** : [ADR-0006 - Passage à 5 phases et mode d'autonomie en Construction](0006-passage-5-phases-et-mode-autonomie-construction.md)
- **REF-005** : [ADR-0007 - Adaptation au modèle conductor / stages / protocols](0007-adaptation-modele-conductor-stages-protocols.md)
- **REF-006** : [ADR-0005 - Verification gates et Sensors](0005-verification-gates-et-sensors.md)
- **REF-007** : [AI-DLC — Harness Engineer Guide, « Rules and the Learning Loop »](https://awslabs.github.io/aidlc-workflows/harness-engineering/05-rules-and-the-loop/)
- **REF-008** : [AI-DLC workflows (awslabs) — core/memory](https://github.com/awslabs/aidlc-workflows/tree/main/core/memory)
