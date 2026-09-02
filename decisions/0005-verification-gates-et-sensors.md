# Verification gates et Sensors déterministes advisory

---
auteurs: Sylvain G.
accepté par : Sylvain G. (validation humaine — multica.gaston)
accepté le : 2026-09-02
supersedes: ""
superseded_by: ""

---

## Status

Accepted

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

**Renforcements issus du contrôle sécurité (Architecte cybersécurité, contrôle réalisé sur commit `81140e3`)** — verdict « posture solide, aucun blocage à l'introduction » ; 6 clauses contraignantes **SG-1 à SG-6** intégrées (workflow § Verification gates & Sensors, `core/sensors/README.md` et manifestes) :

- **SG-1 — intégrité du canal des manifestes** (analogue SEC-5) : `core/sensors/` modifié uniquement en PR revue, versionné, avec `origine` + date ; provenance non traçable ⇒ invalide. Affaiblir un check (retrait de règle, exception, réduction du périmètre) = modification de la surface de gouvernance soumise au contrôle sécurité systématique.
- **SG-2 — indisponible ≠ conforme** : verdict explicite `⛔ indisponible` (sensor / gate non exécuté, en erreur, hors périmètre) tracé comme un écart, jamais comme un vert ; l'absence d'un signal attendu est elle-même un écart.
- **SG-3 — plancher sécurité** (symétrique de R1→R8) : un gate / sensor ne peut jamais porter, remplacer, conditionner ni court-circuiter le contrôle sécurité systématique ni le plancher sécurité des scopes ; le contrôle sécurité reste hors du périmètre automatisable.
- **SG-4 — pré-requis de l'exécution différée** (ancrés dans cet ADR, à respecter avant tout passage en CI) : parsing statique uniquement (ni rendu, ni réseau, ni exécution de code / directive embarquée) ; contenu d'artefact = donnée non fiable ; environnement sans secret ni privilège ; `triggers` glob bornés au repo ; échec ⇒ `⛔ indisponible`.
- **SG-5 — signal = donnée factuelle à source tracée** : rapport / signal portant sa source (manifeste + version / commit) ; provenance non traçable ⇒ `⛔ indisponible` ; le jugement reste humain.
- **SG-6 — anti-érosion sémantique des manifestes** (analogue SEC-1) : restreindre le périmètre, ajouter une exception ou conditionner un check est un affaiblissement soumis au contrôle sécurité, même sans contradiction littérale.

## Conséquences

### Positives

- **POS-001** : Traçabilité contrôlée automatiquement aux frontières de phases ; l'humain valide le contenu, pas la plomberie.
- **POS-002** : Checks déterministes reproductibles (sections, couverture amont, syntaxe), à la place du seul jugement d'agent.
- **POS-003** : Caractère advisory = aucun risque de blocage de la gouvernance ni de contournement du contrôle sécurité ou de la validation humaine.
- **POS-004** : Matérialise le niveau `renforcé` de l'ADR-0003 et s'appuie sur la piste d'audit de l'ADR-0004 (cohérence de la refonte).
- **POS-005** : Manifestes déclaratifs versionnés = base outillable ultérieurement (CI) sans redécider la sémantique.
- **POS-006** : Les clauses SG-1 à SG-6 (contrôle sécurité) ferment les vecteurs résiduels : édition silencieuse des manifestes (Tampering — SG-1 / SG-6), fausse assurance sur signal manquant (Spoofing de conformité — SG-2), automatisation d'un contrôle de sécurité (Elevation of Privilege — SG-3), surface d'attaque de l'exécution différée (SG-4), rapport non répudiable (Repudiation — SG-5). `core/sensors/` atteint le niveau d'exigence de `core/rules/`.

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
- **IMP-005** : Contrôle sécurité (Architecte cybersécurité) réalisé sur le mécanisme (commit `81140e3`, périmètre OWASP / STRIDE ; aucune norme spécifique — mécanisme de gouvernance documentaire sans donnée personnelle ni de paiement) — verdict **« posture solide, aucun blocage à l'introduction »**, 6 clauses **SG-1 à SG-6 intégrées** (workflow § Verification gates & Sensors, `core/sensors/README.md` et manifestes) avant validation humaine.

## Références

- **REF-001** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [ADR-0003 - Scopes et axes Depth / vérification des livrables](0003-scopes-et-axes-depth-verification.md)
- **REF-003** : [ADR-0004 - Boucle d'apprentissage et règles persistantes multi-couches](0004-boucle-apprentissage-et-regles-persistantes.md)
- **REF-004** : [AI-DLC workflows (awslabs) — core](https://github.com/awslabs/aidlc-workflows/tree/main/core)
- **REF-005** : Issue ALI-188 — Stage 4, Verification gates + Sensors (piste d'audit et arbitrages).
