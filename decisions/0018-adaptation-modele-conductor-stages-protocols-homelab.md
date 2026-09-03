# Adaptation au modèle conductor / stages / protocols d'AI-DLC (Homelab)

---
auteurs: Mika (agent) — en attente de validation humaine granulaire (multica.gaston)
accepté par : (en attente)
accepté le : (en attente)
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** — en attente de la **validation humaine granulaire** et du **contrôle sécurité** (QA Docker / Architecte de sécurité Homelab) sur la nouvelle surface. Le passage à *Accepted* suppose ces deux conditions satisfaites (invariant : aucun ADR accepté sans validation humaine explicite). L'issue ALI-207 reste **non close** jusque-là.

## Contexte

Le workflow Homelab A2A était porté par un **document narratif unique**, `docs/homelab-workflow.md` (~66 ko), consolidé au terme des Stages 1 à 6 (ADR-0013..0017, tous *Accepted* ; Stage 6 ALI-206 validé). Ce document mêlait, dans un seul fichier, trois natures d'information distinctes :

1. le **savoir-faire d'exécution du coordinateur** (Tech Lead Homelab : « comment exécuter », gouvernance A2A, gates, chargement du contexte, concurrence par stack) ;
2. les **définitions d'étapes** (le « quoi » de chaque phase / stage) ;
3. les **mécanismes transverses** (scopes, learning loop, gates / sensors, collaboration A2A).

Le modèle de référence **AI-DLC 2.0** (`awslabs/aidlc-workflows`, dossier `core/aidlc-common/`) éclate ces trois natures en un **triptyque** : `conductor.md` (coordinateur) / `stages/<phase>/<stage>.md` (fiches d'étape à front-matter YAML) / `protocols/*.md` (protocoles partagés). Le workspace a déjà adopté ce triptyque pour le workflow d'architecture (`core/common/`, [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md), issue ALI-192).

Le Stage 7 (issue **ALI-207**) porte cette structuration pour le **Homelab**, **sans casser la dynamique du workflow ni les acquis des Stages 1 à 6**. Six inputs étaient à trancher ; ils sont résolus par **alignement sur ALI-192** (Q6) et par les **pointeurs déjà en place** dans le dépôt :

- **Q1 — Emplacement** : `homelab/common/` — cohérent avec `homelab/rules/`, `homelab/scopes/`, `homelab/sensors/` et le miroir `core/common/` ; **déjà référencé** comme source canonique par [`homelab/agents/tech-lead-homelab-agent.md`](../homelab/agents/tech-lead-homelab-agent.md) et les READMEs `homelab/agents/`, `homelab/sensors/`. Pas de préfixe `aidlc-` (agnosticité de méthodologie).
- **Q2 — Sort de `docs/homelab-workflow.md`** : **source unique** = le triptyque ; `docs/homelab-workflow.md` devient un **stub de redirection** (compatibilité ascendante).
- **Q3 — Granularité des stages** : **26 stages** sur 5 phases (voir ci-dessous), branches `n8n` / `home-assistant` `CONDITIONAL` (autonomes), arbitrage Swarm/Proxmox `CONDITIONAL`.
- **Q4 — Front-matter** : schéma amont conservé + adaptation A2A Multica (`lead_agent` / `support_agents` / `reviewer` = fonctions de l'équipe Homelab) + champ `human_gate` ; champs de tooling `bun` / `aidlc-*.ts` supprimés.
- **Q5 — Tooling** : conventions Markdown pures, cohérent avec [ADR-0016](0016-verification-gates-et-sensors-homelab.md) (manifestes déclaratifs non exécutables).
- **Q6 — Cohérence** : structure alignée sur `core/common/` (ALI-192) autant que possible.

## Décision

**Adopter le modèle conductor / stages / protocols** d'AI-DLC 2.0 comme **source unique** du workflow Homelab, sous `homelab/common/`, dans le strict respect des garde-fous absolus du Homelab.

### 1. Emplacement et structure

```
homelab/common/
├── conductor.md                     # instructions du coordinateur Tech Lead Homelab (point d'entrée)
├── protocols/
│   ├── stage-definition.md          # schéma du front-matter d'une fiche de stage
│   ├── stage-protocol.md            # cycle générique d'exécution d'un stage
│   ├── governance-security.md       # gouvernance A2A, contrôle sécurité, concurrence par stack, invariants, garde-fous
│   ├── reviewer.md                  # protocole de revue (contrôle qualité central + contrôle sécurité QA Docker)
│   └── scopes-and-axes.md           # 7 scopes, axes Depth / vérification, matrice stage × scope
└── stages/
    ├── initialisation/  (stack-detection, concurrency-lock-read, deployment-prereqs-precheck, labels-audit-init)
    ├── ideation/        (intent-capture, feasibility-arbitration, scope-detection, auth-preselection, intent-scope-approval)
    ├── cadrage/         (n8n-absolute-rule, intake-framing, swarm-proxmox-arbitration, required-parameters-collection)
    ├── production/      (autonomy-mode, docker-compose-creation, docker-compose-qa, terraform-configuration, n8n-branch, home-assistant-branch, central-quality-control)
    └── validation/      (deployment-prereqs-check, review-and-notification, human-granular-validation, file-deposit, kestra-deployment, closure)
```

Les répertoires de phase portent la **nomenclature métier Homelab** (`initialisation`, `ideation`, `cadrage`, `production`, `validation`), correspondant aux 5 phases AI-DLC (`Initialization → Ideation → Inception → Construction → Operation`) figées au Stage 5 ([ADR-0017](0017-passage-5-phases-et-mode-autonomie-homelab.md)).

### 2. Front-matter des fiches de stage

Contrat défini dans `protocols/stage-definition.md` : champs amont conservés (`slug`, `phase`, `execution`, `condition`, `mode`, `summary_confirmation`, `produces`, `consumes`, `requires_stage`, `sensors`, `scopes`, `inputs`, `outputs`, `review_class`) ; **adaptation A2A** (`lead_agent` / `support_agents` / `reviewer` = fonctions de l'équipe Homelab : Tech Lead Homelab, Spécialiste Docker, QA Docker, Spécialiste Terraform, Expert n8n, Expert Home Assistant, Architecte de sécurité Homelab, Agent de notifications) ; **champ** `human_gate` (`none` / `light` / `granular` / `explicit`) ; **champs de tooling `bun` supprimés**. Le **QA Docker** porte la revue `adversarial` (sécurité technique, plancher SG-3), faute d'Architecte cybersécurité dédié dans l'équipe Homelab (même choix qu'[ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md) / [ADR-0016](0016-verification-gates-et-sensors-homelab.md)).

### 3. Source unique + compatibilité ascendante

`docs/homelab-workflow.md` devient un **stub de redirection** portant une table de correspondance ancien contenu → nouvel emplacement. Aucune référence n'est cassée :

- la **prose historique** des ADR 0013..0017 (immuables) continue de résoudre vers le stub ;
- les **pointeurs vivants** (`AGENTS.md` routage Homelab, `homelab/agents/README.md`, `homelab/sensors/README.md`, `homelab/sensors/gates.md`, `homelab/scopes/README.md`, les 7 fichiers de scope, `homelab/agents/security-architect-homelab-agent.md`) sont mis à jour vers la source canonique `homelab/common/`.

### 4. Aucune dynamique perdue

Le triptyque reprend **intégralement** la dynamique du workflow consolidé : gouvernance A2A (Tech Lead coordonne, spécialistes produisent), **règle absolue n8n**, **règle préalable de documentation officielle**, **verrou de concurrence par stack** (`active_step`), **sélection automatique du type d'authentification**, boucle Keep / Modify / Redo aux gates, journal d'observations (candidats-règles), verification gates aux frontières de phases, invariants et garde-fous (plancher sécurité des scopes, SEC-1..5, SG-1..6, sensors sécurité bloquants sur `security-patch` / `new-stack`), mode d'autonomie en Production (walking skeleton + halt-and-ask), prérequis §4.0 (`[répertoire de travail]`, Kestra). Les mécanismes déjà outillés (`homelab/rules/`, `homelab/sensors/`, `homelab/scopes/`) restent canoniques et sont **référencés, non dupliqués**.

### 5. Agnostique du tooling amont

Le tooling `bun` / `aidlc-*.ts` de l'amont n'est **pas** importé : protocoles et fiches restent des **conventions Markdown** adaptées au moteur A2A Multica (mentions UUID, `trigger_outcomes`, statut d'issue, verrou metadata, piste d'audit sur l'issue).

## Conséquences

### Positives

- **POS-001** : Workflow Homelab directement exploitable par le Tech Lead — séparation nette savoir-faire (conductor) / étapes (stages) / mécanismes (protocols).
- **POS-002** : Front-matter machine-lisible ⇒ ouvre la voie à un outillage (routage, gates) sans re-narration.
- **POS-003** : Source unique — plus de divergence entre narration et structure ; le stub garantit la compatibilité ascendante.
- **POS-004** : Alignement structurel sur `core/common/` (ALI-192) tout en restant agnostique de méthodologie et de tooling ; deux workflows indépendants mais de forme identique.

### Négatives

- **NEG-001** : Fragmentation en 32 fichiers (conductor + 5 protocols + 26 stages) — la vue narrative disparaît au profit d'une navigation par liens ; atténué par la table de stages du conductor et le stub de correspondance.
- **NEG-002** : Surface d'instructions exécutables plus étalée ⇒ surface d'injection potentielle ; atténué par la clause « UNTRUSTED DATA » de `protocols/governance-security.md`, soumis au contrôle sécurité.
- **NEG-003** : Une **copie parallèle** subsiste sous `core/workflows/homelab/homelab-workflow.md` (~35 ko, version antérieure), référencée par `README.md`, `CONTRIBUTING.md` et l'agent `core/agents/architecture-solution-integration-agent.md`. **Hors périmètre de ce stage** (qui vise `docs/homelab-workflow.md`) ; divergence signalée à l'humain pour arbitrage (aligner sur le stub / le triptyque, ou retirer la copie).

## Alternatives étudiées

### ALT-001 — Conserver `docs/homelab-workflow.md` en parallèle (vue narrative + triptyque)

**Raison du rejet** : arbitrage Q2 = source unique (aligné sur ALI-192). Deux sources co-existantes créent un risque de divergence et de double maintenance.

### ALT-002 — Emplacement `homelab/` racine ou `homelab/aidlc-common/`

**Raison du rejet** : `homelab/common/` est déjà référencé par les artefacts en place (tech-lead agent, READMEs) et cohérent avec `core/common/` ; le préfixe `aidlc-` lierait la structure à une méthodologie.

### ALT-003 — Importer le tooling `bun` / `aidlc-*.ts`

**Raison du rejet** : arbitrage Q5 + cohérence [ADR-0016](0016-verification-gates-et-sensors-homelab.md) (manifestes déclaratifs). Le passage à l'exécutable reste une évolution ultérieure, hors périmètre.

## Notes d'implémentation

- **IMP-001** : 32 fichiers créés sous `homelab/common/` (conductor + 5 protocols + 26 stages).
- **IMP-002** : `docs/homelab-workflow.md` converti en stub de redirection avec table de correspondance et table des phases ; bannière « PRIORITÉ » conservée.
- **IMP-003** : Pointeurs vivants mis à jour (`AGENTS.md`, `homelab/agents/README.md`, `homelab/agents/security-architect-homelab-agent.md`, `homelab/sensors/README.md`, `homelab/sensors/gates.md`, `homelab/scopes/README.md` + 7 fichiers de scope) ; prose historique des ADR 0013..0017 **laissée intacte** (le stub maintient leurs liens).
- **IMP-004** : `homelab/sensors/gates.md` réaligné sur les **5 phases** (frontières `entree-phase0`, `phase0-phase1`, `phase1-phase2`, `phase2-phase3`, `phase3-phase4`, `phase4-cloture` ; §1.4 → §2.4, §3.0 → §4.0, `prerequis_30` → `prerequis_40`).
- **IMP-005** : Diagrammes Mermaid du conductor (flowchart 5 phases + sequence A2A) et des protocoles (stage-protocol, reviewer) — **syntaxe à valider** (Mermaid v11) avant acceptation.
- **IMP-006** : Contrôle sécurité (QA Docker / Architecte de sécurité Homelab) à solliciter sur la nouvelle surface (instructions exécutables du coordinateur, frontières de délégation, protection contre l'injection) **avant** validation humaine et passage à *Accepted*.

## Références

- **REF-001** : [ADR-0007 — Adaptation au modèle conductor / stages / protocols (core, ALI-192)](0007-adaptation-modele-conductor-stages-protocols.md)
- **REF-002** : [ADR-0013 — Cadrage de la refonte homelab-workflow.md sur AI-DLC](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)
- **REF-003** : [ADR-0014 — Scopes Homelab et axes Depth / vérification](0014-scopes-homelab-et-axes-depth-verification.md)
- **REF-004** : [ADR-0015 — Learning loop et règles persistantes Homelab](0015-learning-loop-et-regles-persistantes-homelab.md)
- **REF-005** : [ADR-0016 — Verification gates et Sensors Homelab](0016-verification-gates-et-sensors-homelab.md)
- **REF-006** : [ADR-0017 — Passage à 5 phases et mode d'autonomie Homelab](0017-passage-5-phases-et-mode-autonomie-homelab.md)
- **REF-007** : Issue ALI-207 (Stage 7 — Homelab) ; issue parente ALI-200.
- **REF-008** : [AI-DLC workflows (awslabs) — core/aidlc-common](https://github.com/awslabs/aidlc-workflows)
