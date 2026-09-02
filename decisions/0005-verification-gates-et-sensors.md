# Verification gates et Sensors déterministes advisory

---
auteurs: Sylvain G.
accepté par : ""
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

## Contexte

Le workflow `docs/core-workflow.md` disposait de la **validation humaine granulaire** et du **contrôle sécurité systématique** (Architecte cybersécurité), mais **d'aucun contrôle automatique de traçabilité** aux frontières de phases ni de **check déterministe** à l'écriture d'un artefact. L'analyse comparative avec AI-DLC 2.0 (issue parente ALI-184, cadrage ALI-185, [ADR-0001](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)) a identifié deux écarts, comblés au Stage 4 (ALI-188) :

- **E — Verification gates** : AI-DLC ajoute, aux gates, un contrôle automatique de traçabilité (présence des artefacts, liaison exigence ↔ décision ↔ livrable, absence d'orphelin), distinct de la décision humaine.
- **F — Sensors** : AI-DLC ajoute des checks déterministes advisory à l'écriture d'un artefact (sections requises, couverture amont, linter, traçabilité), là où nos contrôles reposaient sur le jugement d'un agent.

Le niveau de vérification `renforcé` du Stage 2 ([ADR-0003](0003-scopes-et-axes-depth-verification.md)) en posait déjà le cadre advisory ; ce stade le **matérialise**. Le mécanisme s'appuie sur la piste d'audit sur l'issue formalisée au Stage 3 ([ADR-0004](0004-boucle-apprentissage-et-regles-persistantes.md)). Le workspace produit **majoritairement de la documentation d'architecture** (DAS, ADR, diagrammes générés en code), ce qui oriente le choix des sensors.

Les arbitrages (sensors prioritaires, advisory vs bloquant, rubriques de référence, outillage) sont soumis à l'humain sur l'issue ALI-188.

## Décision

**Introduire deux mécanismes de fiabilisation déterministe, tous deux advisory**, dans le respect des invariants de gouvernance A2A.

**Verification gates** — à chaque **frontière de phase**, en amont du gate humain, un contrôle automatique de traçabilité en trois points : (1) présence des artefacts requis, (2) liaison exigence ↔ ADR ↔ livrable, (3) absence d'artefact orphelin. Frontières adossées à la structure Inception / Construction / Operation actuelle (la matrice suivra l'ossature à 5 phases au Stage 5). **En cas d'écart** : signalement dans un « Rapport de vérification » sur l'issue et proposition de revenir corriger, **sans blocage**.

**Sensors** — checks déterministes déclenchés à l'écriture d'un artefact. **Trois sensors**, dont **deux prioritaires** :

- `required-sections` *(prioritaire)* — rubriques obligatoires présentes et non vides sur ADR / DAS (rubriques dérivées des ADR existants 0001–0004).
- `upstream-coverage` *(prioritaire)* — le livrable référence explicitement sa demande amont (issue d'origine + ADR parent le cas échéant).
- `diagram-validity` *(complémentaire)* — syntaxe des diagrammes générés en code (Mermaid / PlantUML / Structurizr) valide.

**Caractère advisory (décision de gouvernance)** — gates et sensors **ne bloquent jamais** la validation humaine granulaire, **ne la remplacent pas**, et **ne remplacent pas** le contrôle sécurité systématique. Un signal au vert ne vaut pas validation ; un signal en échec n'autorise aucun raccourci. Rendre un sensor **bloquant** est une décision structurante explicite (ADR + contrôle sécurité) — par défaut, tout reste advisory.

**Intégration à la piste d'audit** — les signaux vivent **sur l'issue** (pas de fichier `audit.md`) : « Rapport de vérification » à chaque frontière (avant la validation humaine) et signal de sensor à l'écriture d'un artefact. Faits vérifiables uniquement ; le jugement reste humain. Un écart advisory récurrent peut alimenter un candidat-règle de la boucle d'apprentissage, sans court-circuiter la validation.

**Outillage** — les checks sont des **conventions documentées** dans le workflow, **accompagnées de manifestes déclaratifs** versionnés dans `core/sensors/` (un fichier par sensor + un manifeste de gates). Ces manifestes **ne sont pas exécutables** à ce stade : ils fixent le contrat pour un outillage (script / CI) ultérieur, sans redécider le fond.

## Conséquences

### Positives

- **POS-001** : Traçabilité contrôlée automatiquement aux frontières de phases ; l'humain valide le contenu, pas la plomberie.
- **POS-002** : Checks déterministes reproductibles (sections, couverture amont, syntaxe), à la place du seul jugement d'agent.
- **POS-003** : Caractère advisory = aucun risque de blocage de la gouvernance ni de contournement du contrôle sécurité ou de la validation humaine.
- **POS-004** : Matérialise le niveau `renforcé` de l'ADR-0003 et s'appuie sur la piste d'audit de l'ADR-0004 (cohérence de la refonte).
- **POS-005** : Manifestes déclaratifs versionnés = base outillable ultérieurement (CI) sans redécider la sémantique.

### Négatives

- **NEG-001** : `core/sensors/` est un nouvel artefact à maintenir cohérent avec le workflow et les gabarits d'ADR / DAS.
- **NEG-002** : Tant que non outillés, les checks reposent sur l'application disciplinée du coordinateur (advisory, non automatisé).
- **NEG-003** : Un signal advisory peut être perçu comme du bruit s'il n'est pas relié à une action ; d'où la trace factuelle et le lien avec la boucle d'apprentissage.

## Alternatives étudiées

### ALT-001 - Sensors bloquants par défaut

Rendre les checks contraignants (bloquer l'avancée sur échec).

**Raison du rejet** : un check déterministe bloquant peut arrêter le workflow sur un faux positif et empiéter sur la décision humaine ; il déplace le pouvoir de décision vers un automate. Retenu : advisory par défaut, passage à bloquant réservé à une décision ADR + contrôle sécurité.

### ALT-002 - Scripts exécutables (CI) dès l'introduction

Produire directement des scripts / hooks CI exécutables.

**Raison du rejet** : figer une implémentation avant d'avoir stabilisé la sémantique (rubriques, périmètres, frontières) et l'ossature de phases (Stage 5 à venir) créerait de la reprise. Retenu : conventions + manifestes déclaratifs, outillage ultérieur sans redécision du fond.

### ALT-003 - Reprise de l'axe « test strategy » / linter de code d'AI-DLC tel quel

Centrer les sensors sur le linting de code et le volume de tests.

**Raison du rejet** : le workspace produit majoritairement de la documentation ; les sensors utiles portent sur les sections d'ADR / DAS, la couverture amont et la syntaxe des diagrammes. Le cas code / IaC reste couvert par le repli « stratégie de tests » de l'axe de vérification (ADR-0003).

## Notes d'implémentation

- **IMP-001** : Mécanisme documenté dans la section « Verification gates & Sensors » de [`docs/core-workflow.md`](../docs/core-workflow.md).
- **IMP-002** : Manifestes déclaratifs scaffoldés dans `core/sensors/` — [`README.md`](../core/sensors/README.md), [`gates.md`](../core/sensors/gates.md), `sensors/{required-sections,upstream-coverage,diagram-validity}.md`.
- **IMP-003** : Frontières adossées à Inception / Construction / Operation ; la matrice suivra l'ossature à 5 phases au Stage 5 (voir [ADR-0003](0003-scopes-et-axes-depth-verification.md), IMP-003).
- **IMP-004** : Advisory par défaut ; le passage à bloquant d'un sensor est une décision ADR + contrôle sécurité (Architecte cybersécurité).
- **IMP-005** : Contrôle sécurité (Architecte cybersécurité) sollicité sur le mécanisme ; les clauses retenues sont intégrées avant validation humaine finale.

## Références

- **REF-001** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [ADR-0003 - Scopes et axes Depth / vérification des livrables](0003-scopes-et-axes-depth-verification.md)
- **REF-003** : [ADR-0004 - Boucle d'apprentissage et règles persistantes multi-couches](0004-boucle-apprentissage-et-regles-persistantes.md)
- **REF-004** : [AI-DLC workflows (awslabs) — core](https://github.com/awslabs/aidlc-workflows/tree/main/core)
- **REF-005** : Issue ALI-188 — Stage 4, Verification gates + Sensors (piste d'audit et arbitrages).
