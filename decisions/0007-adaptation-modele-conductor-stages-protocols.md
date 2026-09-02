# Adaptation au modèle conductor / stages / protocols d'AI-DLC

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : (en attente de validation humaine)
accepté le : (en attente)
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** tant que la validation humaine granulaire et le contrôle sécurité (Xavier) sur la nouvelle surface ne sont pas obtenus. Passera à **Accepted** après validation humaine explicite (invariant : aucun ADR accepté sans validation humaine).

## Contexte

Le workflow d'architecture A2A du workspace était porté par un **document narratif unique**, `docs/core-workflow.md` (~74 ko), consolidé au terme des Stages 1 à 6 (ADR-0001..0006, tous *Accepted* sur `main` ; PR #40 mergée). Ce document mêlait, dans un seul fichier, trois natures d'information distinctes :

1. le **savoir-faire d'exécution du coordinateur** (« comment exécuter un stage », gouvernance, gates, chargement du contexte) ;
2. les **définitions d'étapes** (le « quoi » de chaque phase / stage) ;
3. les **mécanismes transverses** (scopes, learning loop, gates / sensors, collaboration A2A).

Le modèle de référence **AI-DLC 2.0** (`awslabs/aidlc-workflows`, dossier `core/aidlc-common/`) éclate au contraire ces trois natures en un **triptyque** : `conductor.md` (coordinateur) / `stages/<phase>/<stage>.md` (fiches d'étape à front-matter YAML) / `protocols/*.md` (protocoles partagés). Cette structuration rend le workflow **directement exploitable par un coordinateur** et par un outillage ultérieur, sans re-narration.

Le Stage 7 (issue ALI-192) porte cette structuration dans `homelab-portfolio`, **sans casser la dynamique du workflow ni les acquis des Stages 1 à 6**. Cinq inputs ont été soumis à l'humain avant écriture et tranchés sur l'issue :

- **Q1 — Emplacement** : `core/common/` (validé), et non `core/aidlc-common/` de l'amont — cohérent avec `core/rules/` et `core/sensors/`, et agnostique de méthodologie.
- **Q2 — Sort de `docs/core-workflow.md`** : **source unique** (validé) — le triptyque devient canonique ; `docs/core-workflow.md` devient un **stub de redirection**.
- **Q3 — Granularité des stages** : liste validée (20 stages sur 5 phases).
- **Q4 — Front-matter** : schéma validé (champs amont conservés + adaptation A2A + champ `human_gate` ajouté ; champs de tooling `bun` supprimés).
- **Q5 — Tooling** : conventions Markdown pures (validé), cohérent avec le choix « manifestes déclaratifs non exécutables » d'[ADR-0005](0005-verification-gates-et-sensors.md).

## Décision

**Adopter le modèle conductor / stages / protocols** d'AI-DLC 2.0 comme **source unique** du workflow d'architecture, sous `core/common/`, dans le strict respect des invariants de gouvernance A2A.

### 1. Emplacement et structure

```
core/common/
├── conductor.md                     # instructions du coordinateur (point d'entrée)
├── protocols/
│   ├── stage-definition.md          # schéma du front-matter d'une fiche de stage
│   ├── stage-protocol.md            # cycle générique d'exécution d'un stage
│   ├── governance-security.md       # gouvernance A2A, contrôle sécurité, invariants, garde-fous
│   ├── reviewer.md                  # protocole de revue (cohérence ADR + revue sécurité)
│   └── scopes-and-axes.md           # scopes, axes Depth / vérification, matrice stage × scope
└── stages/
    ├── initialization/  (directory-check, brownfield-greenfield-detection, audit-trail-init)
    ├── ideation/        (intent-capture, feasibility-constraints, scope-definition, mockups, intent-scope-approval)
    ├── inception/       (intake-framing, existing-context-loading, requirements-analysis, deliverables-breakdown, design-and-adr)
    ├── construction/    (walking-skeleton, detailed-deliverables, security-consistency-check, consolidation-handoff)
    └── operation/       (deployment-under-validation, completion-notification, maintenance-support)
```

### 2. Front-matter des fiches de stage

Chaque fiche porte un front-matter YAML dont le contrat est défini dans `protocols/stage-definition.md` : champs amont conservés (`slug`, `phase`, `execution`, `condition`, `mode`, `summary_confirmation`, `produces`, `consumes`, `requires_stage`, `sensors`, `scopes`, `inputs`, `outputs`, `review_class`) ; **adaptation A2A** (`lead_agent` / `support_agents` / `reviewer` = labels d'agents du workspace, pas les personas amont) ; **champ ajouté** `human_gate` (`none` / `light` / `granular` / `explicit`) matérialisant les gates du workspace ; **champs de tooling `bun` / `aidlc-*.ts` supprimés**.

### 3. Source unique + compatibilité ascendante

`docs/core-workflow.md` devient un **stub de redirection** portant une table de correspondance ancien contenu → nouvel emplacement. Aucune référence n'est cassée :

- les **liens de prose historique** des ADR 0001..0006 (immuables) continuent de résoudre vers le stub ;
- les **pointeurs vivants** (`AGENTS.md`, `core/rules/README.md`, `core/sensors/README.md`, `core/sensors/gates.md`) sont mis à jour vers la nouvelle source canonique.

### 4. Aucune dynamique perdue

Le triptyque reprend **intégralement** la dynamique du workflow consolidé : gouvernance A2A, boucle Keep / Modify / Redo aux gates, résolution des questions / contradictions intra-stage, journal d'observations (candidats-règles), verification gates aux frontières de phases, invariants et garde-fous (plancher sécurité des scopes, SEC-1..5, SG-1..6), mode d'autonomie en Construction (walking skeleton + halt-and-ask). Les mécanismes déjà outillés (`core/rules/`, `core/sensors/`) restent canoniques et sont référencés, non dupliqués.

### 5. Agnostique du tooling amont

Le tooling `bun` / `aidlc-*.ts` de l'amont n'est **pas** importé : protocoles et fiches restent des **conventions Markdown** adaptées au moteur A2A Multica (mentions UUID, statut d'issue, piste d'audit sur l'issue), cohérent avec [ADR-0005](0005-verification-gates-et-sensors.md).

## Conséquences

### Positives

- **POS-001** : Workflow directement exploitable par un coordinateur — séparation nette entre savoir-faire (conductor), étapes (stages) et mécanismes (protocols).
- **POS-002** : Front-matter machine-lisible ⇒ ouvre la voie à un outillage (routage, verification gates) sans re-narration ni redécision de fond.
- **POS-003** : Source unique — plus de risque de divergence entre un document narratif et une structure ; le stub garantit la compatibilité ascendante ([ADR-0002](0002-strategie-compatibilite-et-terminologie.md)).
- **POS-004** : Alignement structurel sur AI-DLC 2.0 (`core/aidlc-common`) tout en restant agnostique de méthodologie et de tooling.

### Négatives

- **NEG-001** : Fragmentation en 26 fichiers — la vue d'ensemble narrative disparaît au profit d'une navigation par liens ; atténué par la table de stages du conductor et le stub de correspondance.
- **NEG-002** : Surface d'instructions exécutables plus étalée ⇒ surface d'injection potentielle ; atténué par la clause « UNTRUSTED DATA » de `protocols/governance-security.md` et soumis au contrôle sécurité (Xavier).
- **NEG-003** : L'agent Sylvain porte, dans sa définition, un pointeur `docs/core-workflow.md` ; le stub le maintient valide, mais la définition d'agent (hors repo) devra être mise à jour vers `core/common/conductor.md`.

## Alternatives étudiées

### ALT-001 — Conserver `docs/core-workflow.md` en parallèle (vue narrative + triptyque)

**Raison du rejet** : arbitrage humain Q2 = **source unique**. Deux sources co-existantes créent un risque de divergence et de double maintenance.

### ALT-002 — Aligner sur `core/aidlc-common/` (préfixe amont)

**Raison du rejet** : arbitrage humain Q1 = `core/common/`. Le préfixe `aidlc-` lierait la structure à une méthodologie, contraire au principe d'agnosticité.

### ALT-003 — Importer le tooling `bun` / `aidlc-*.ts` de l'amont

**Raison du rejet** : arbitrage humain Q5 + cohérence [ADR-0005](0005-verification-gates-et-sensors.md) (manifestes déclaratifs non exécutables) ; le passage à l'exécutable reste une évolution ultérieure, hors périmètre.

## Notes d'implémentation

- **IMP-001** : 26 fichiers créés sous `core/common/` (conductor + 5 protocols + 20 stages).
- **IMP-002** : `docs/core-workflow.md` converti en stub de redirection avec table de correspondance ; contenu normatif retiré (déplacé dans le triptyque).
- **IMP-003** : Pointeurs vivants mis à jour (`AGENTS.md`, `core/rules/README.md`, `core/sensors/README.md`, `core/sensors/gates.md`) ; prose historique des ADR 0001..0006 **laissée intacte** (enregistrements immuables ; le stub maintient leurs liens).
- **IMP-004** : Diagrammes Mermaid du conductor (flowchart des 5 phases + sequence A2A + flowchart du stage-protocol / reviewer) — **syntaxe à valider** (Mermaid v11) avant acceptation.
- **IMP-005** : Contrôle sécurité (Xavier) sollicité sur la nouvelle surface (instructions exécutables du coordinateur, frontières de délégation, protection contre l'injection via entrées non fiables) **avant** validation humaine et passage à *Accepted*.
- **IMP-006** : Revue sécurité Xavier (OWASP Top 10 + STRIDE) — verdict **✅ approuvé, aucun risque élevé / moyen**, 2 durcissements mineurs **non bloquants** intégrés : **M-1** (bannière « PRIORITÉ » de `conductor.md` : clause explicitant qu'elle ne vaut que pour les instructions de premier rang du triptyque, jamais pour une donnée non fiable — renforce UNTRUSTED DATA) ; **M-2** (matrice stage × scope de `scopes-and-axes.md` : note `[^poc-sec]` sur la cellule `poc` du contrôle sécurité — plancher OWASP / STRIDE jamais nul, seule la profondeur varie).

## Références

- **REF-001** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [ADR-0002 - Stratégie de compatibilité et terminologie](0002-strategie-compatibilite-et-terminologie.md)
- **REF-003** : [ADR-0003 - Scopes et axes Depth / vérification](0003-scopes-et-axes-depth-verification.md)
- **REF-004** : [ADR-0004 - Boucle d'apprentissage et règles persistantes](0004-boucle-apprentissage-et-regles-persistantes.md)
- **REF-005** : [ADR-0005 - Verification gates et Sensors](0005-verification-gates-et-sensors.md)
- **REF-006** : [ADR-0006 - Passage à 5 phases et mode d'autonomie en Construction](0006-passage-5-phases-et-mode-autonomie-construction.md)
- **REF-007** : Issue ALI-192 (Stage 7 — Adaptation au modèle conductor / stages / protocols) ; issue parente ALI-184 ; cadrage ALI-185.
- **REF-008** : [AI-DLC workflows (awslabs) — core/aidlc-common](https://github.com/awslabs/aidlc-workflows)
