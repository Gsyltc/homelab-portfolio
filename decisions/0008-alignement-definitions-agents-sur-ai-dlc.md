# Alignement des définitions d'agents sur le contrat AI-DLC « Adding an Agent »

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : (en attente de validation humaine)
accepté le : (en attente)
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** tant que la validation humaine granulaire n'est pas obtenue. Passera à **Accepted** après validation humaine explicite (invariant : aucun ADR accepté sans validation humaine). Aucune modification de la posture de sécurité ni de la surface d'exécution des agents n'est actée ici (voir § Contrôle sécurité).

## Contexte

Les définitions d'agents du workflow d'architecture vivent sous [`core/agents/`](../core/agents/) (9 fichiers `.md` : coordinateur, 4 architectes, cybersécurité, OpenSpec, archivage, notifications, vente). Le Stage 1 de l'alignement AI-DLC 2.0 (issue ALI-194, parente ALI-193) porte ces fichiers sur le contrat **« Adding an Agent »** du *Harness Engineer Guide* (`awslabs/aidlc-workflows`).

Le contrat amont fixe un front-matter d'agent minimal :

- `name` — **doit égaler le stem du fichier** (déjà conforme ici) ;
- `display_name` — libellé humain (déjà présent) ;
- `description` — résumé du rôle (déjà présent) ;
- `disallowedTools` — **doit inclure `Task`** ; interdiction non optionnelle de l'auto-délégation (un agent ne peut pas engendrer ses propres sous-agents, ce qui cascaderait des chaînes de délégation que le cadre est conçu pour empêcher) ;
- `tier` — `judgment` / `balanced` / `templated` ; nomme la **nature du travail**, projeté ensuite en clés `model` / `effort` par harness (jamais de `model:` brut en source).

Point clé du contrat : **`allowedTools` ne fait pas partie du schéma AI-DLC**. Un agent hérite par défaut de tout le *toolset* de session ; pour le **restreindre**, on utilise une *allowlist* optionnelle `tools:` (et non `allowedTools`). Nos 9 fichiers portaient un champ `allowedTools: Multica` — non conforme et sans effet dans le contrat amont.

Trois écarts étaient à traiter (issue ALI-194) :

1. **Front-matter** : remplacer `allowedTools: Multica` par `disallowedTools: Task` (obligatoire) + `tier` par agent.
2. **Reviewers** : décider si l'on modélise des personas « review-only » distincts (comme les 2 reviewers AI-DLC) ou si l'on conserve le champ `reviewer` sur les stages.
3. **Connaissances par agent** : overlay de connaissances par persona (`knowledge/<agent>/`) ou documentation de la raison pour laquelle les skills Multica en tiennent lieu.

Contrainte de cadrage (ALI-193) : adapter au moteur A2A **Multica**, sans importer le tooling amont non applicable (`bun`, hooks `.ts`, `dist/<harness>/`) ; toute divergence assumée est tracée ; aucune régression sur l'exécution A2A.

## Décision

### 1. Front-matter — adoption du contrat, `allowedTools` retiré

Pour les 9 fichiers `core/agents/*.md` :

- **Retrait** de `allowedTools: Multica` (hors contrat, sans effet).
- **Ajout** de `disallowedTools: Task` sur **chaque** agent — matérialise dans la source la frontière « pas d'auto-délégation », déjà imposée côté runtime Multica (un agent traite l'issue qui lui est assignée et délègue uniquement par **mention A2A** résolue par le coordinateur, jamais par un outil `Task`).
- **Ajout** d'un champ `tier` par agent (voir § tiers).
- `name` = stem et `display_name` : **déjà conformes**, laissés intacts.

**Divergence assumée (tracée)** : le champ `disallowedTools` est un front-matter **Claude-only** dans l'amont ; les projections Kiro le retirent et imposent la même frontière via la config native de l'agent. Sur **Multica**, il n'existe pas d'outil `Task` : la valeur est donc **documentaire / déclarative** (intention explicite « aucune sous-délégation »), sans effet d'exécution mais cohérente avec le contrat et avec la gouvernance A2A du workspace ([`core/common/protocols/governance-security.md`](../core/common/protocols/governance-security.md)). Aucun champ `tools:` d'*allowlist* n'est ajouté : les agents Multica reçoivent leurs capacités via l'assignation de **skills** (voir § 3), pas via une *allowlist* d'outils de session.

### 2. Tiers retenus

| Agent (stem) | `tier` | Justification |
| --- | --- | --- |
| `architecture-solution-integration-agent` | `judgment` | Coordinateur : arbitrage multi-contraintes, routage, cohérence — raisonnement dense qui cascade en aval. |
| `solution-architect-agent` | `judgment` | Conception d'architecture sous contexte dense (NFR, compromis, décisions structurantes). |
| `aws-architect-agent` | `judgment` | Choix de services, arbitrages coût / Well-Architected, contre-indications. |
| `cybersecurity-architect-agent` | `judgment` | Analyse de risques (OWASP / STRIDE), surface sécurité critique — ne doit **jamais** sous-raisonner (garde-fou : « en cas de doute, `judgment` »). |
| `windows-infrastructure-admin-agent` | `judgment` | Décisions de migration, plans de rollback, contraintes d'identité / licences / sauvegardes. |
| `openspec-agent` | `judgment` | Spec-Driven Development : conception de propositions et deltas, raisonnement méthodologique. |
| `archiving-agent` | `templated` | Procédure déterministe (import / export / archive) encodée dans la skill ; sortie majoritairement suivant un patron. |
| `notification-agent` | `templated` | Envoi ntfy paramétré (skill `ntfy-notifications`) ; sortie suivant un patron. |
| `sales-proposals-agent` | `templated` | Synthèse de livrables **déjà validés** en supports commerciaux ; méthodologie encodée dans la skill `sales-deck-generation` ; ne réinvente pas le contenu technique. |

Aucun agent n'est classé `balanced` : la seule fonction « review-shaped » du workspace (revue de sécurité) est portée par l'Architecte cybersécurité, classé `judgment` car sa sortie est sécurité-critique et cascade sur la validation humaine (voir § 3 des reviewers). `balanced` / `templated` projettent aujourd'hui à l'identique sur les harness où le tier ne change rien (Kiro/Cursor/Copilot héritent du modèle et de l'effort de session) ; le tier reste néanmoins **sémantiquement correct** et exploitable par un harness qui l'honore.

### 3. Reviewers — conservation du champ `reviewer` sur les stages (pas de persona review-only)

L'amont AI-DLC livre **2 personas « review-only »** distincts. Ce workspace **ne crée pas** de tels personas et **conserve** la modélisation déjà actée en [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md) : la revue est un **attribut du stage** (`reviewer:` + `review_class:` dans le front-matter de stage, [`stage-definition.md`](../core/common/protocols/stage-definition.md)), et le protocole [`reviewer.md`](../core/common/protocols/reviewer.md) définit **deux natures de revue non substituables** portées par des fonctions **existantes** :

- **revue de cohérence** → **coordinateur** (Architecture Solution & Intégration) ;
- **revue de sécurité** (obligatoire, plancher SG-3) → **Architecte cybersécurité**.

**Raison** : dans le moteur A2A Multica, un « reviewer » est une **fonction sollicitée par mention** à un temps du stage, pas un exécutable chargé dans un stage. Créer deux agents review-only dupliquerait des rôles déjà tenus, sans gain d'exécution, et brouillerait le routage (deux entrées de plus dans `multica agent list`). La séparation cohérence / sécurité est déjà garantie par le protocole et le plancher SG-3.

### 4. Connaissances par agent — les skills Multica tiennent lieu d'overlay

L'amont pose deux niveaux de connaissances : `core/knowledge/aidlc-<agent>/` (méthodologie cadre) et un overlay d'équipe au niveau espace `aidlc/knowledge/<agent>/`. Ce workspace **ne crée pas** d'arborescence `core/knowledge/<agent>/` et documente la raison :

- La connaissance par persona est portée par les **skills Multica**, déclarées dans le champ `skills:` de chaque agent et **effectivement chargées** après **import** (`multica skill import`) puis **assignation** (`multica agent skills add|set`) — mécanisme déjà documenté dans [`README.md`](../README.md) et [`CONTRIBUTING.md`](../CONTRIBUTING.md).
- Les skills sources vivent à l'emplacement canonique **Agent Plugins v1.0.0** `plugins/<nom>/skills/<skill>/SKILL.md` (front-matter `name` + `description`), pas sous `core/knowledge/`.
- Un répertoire `core/knowledge/<agent>/` parallèle créerait une **seconde source** de connaissance non chargée par le runtime Multica (un `.md` déposé dans le dépôt n'est pas découvert automatiquement), donc un risque de divergence sans bénéfice d'exécution.

L'overlay d'équipe (standards maison par persona) reste possible ultérieurement **via une skill dédiée importée et assignée**, cohérent avec le modèle skills-portées-par-plugins ; il n'est pas ouvert dans ce stage.

## Conséquences

### Positives

- **POS-001** : Front-matter d'agent conforme au contrat AI-DLC (`name`=stem, `display_name`, `description`, `disallowedTools: Task`, `tier`) ; alignement structurel sans importer le tooling amont.
- **POS-002** : Frontière « pas d'auto-délégation » **explicite dans la source**, cohérente avec la gouvernance A2A par mention.
- **POS-003** : `tier` rend lisible la nature du travail par agent et ouvre la voie à une projection modèle/effort par un harness qui l'honore, sans redécision.
- **POS-004** : Pas de duplication de rôles (reviewers) ni de sources de connaissance concurrentes (knowledge) — cohérence avec ADR-0007 et le modèle skills-Multica.

### Négatives

- **NEG-001** : `disallowedTools: Task` est **inerte à l'exécution sur Multica** (pas d'outil `Task`) : valeur documentaire ; atténué par le fait qu'il matérialise une intention et satisfait le contrat pour tout futur portage de harness.
- **NEG-002** : La classification `tier` n'a **aucun effet** sur les harness qui héritent du modèle/effort de session (Kiro/Cursor/Copilot) ; elle reste néanmoins sémantiquement utile et sans coût.
- **NEG-003** : L'absence d'overlay `core/knowledge/<agent>/` impose de passer par l'import/assignation de skills pour enrichir un persona ; c'est le mécanisme Multica attendu, mais il diffère de l'amont (documenté ici).

## Alternatives étudiées

### ALT-001 — Conserver `allowedTools: Multica`

**Raison du rejet** : hors contrat AI-DLC (le schéma ne connaît pas `allowedTools` ; la restriction se fait par `tools:`), et sans effet — un champ trompeur. Le contrat impose au contraire `disallowedTools`.

### ALT-002 — Ajouter une *allowlist* `tools:` restrictive par agent

**Raison du rejet** : sur Multica les capacités sont conférées par **assignation de skills**, pas par une *allowlist* d'outils de session. Une `tools:` restrictive n'aurait pas de correspondance runtime et risquerait de sur-contraindre à tort. Laisser hériter le toolset de session (recommandation amont : « most personas are best left to inherit everything »).

### ALT-003 — Créer deux personas « review-only » (miroir de l'amont)

**Raison du rejet** : dans le moteur A2A, la revue est une fonction sollicitée par mention, déjà tenue par le coordinateur (cohérence) et l'Architecte cybersécurité (sécurité) — voir [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md) et [`reviewer.md`](../core/common/protocols/reviewer.md). Deux agents supplémentaires dupliqueraient des rôles existants.

### ALT-004 — Créer une arborescence `core/knowledge/<agent>/`

**Raison du rejet** : créerait une source de connaissance non chargée par le runtime Multica (découverte non automatique), concurrente des skills importées/assignées — divergence sans bénéfice d'exécution.

## Notes d'implémentation

- **IMP-001** : 9 fichiers `core/agents/*.md` modifiés — `allowedTools: Multica` retiré ; `disallowedTools: Task` + `tier` ajoutés. Validité YAML du front-matter vérifiée sur les 9 (name=stem, `display_name` présent, `disallowedTools: Task`, `tier` ∈ {judgment, templated}).
- **IMP-002** : Reviewers — **aucun fichier agent créé** ; la modélisation `reviewer:` sur stages + [`reviewer.md`](../core/common/protocols/reviewer.md) est conservée (ADR-0007).
- **IMP-003** : Connaissances — **aucune arborescence `core/knowledge/`** créée ; les skills Multica (import + assignation) tiennent lieu d'overlay, conformément à [`README.md`](../README.md) / [`CONTRIBUTING.md`](../CONTRIBUTING.md).
- **IMP-004** : Pointeurs — `README.md` et `AGENTS.md` mentionnent `decisions/ (0001…0007)` ; mis à jour vers `0001…0008`.
- **IMP-005** : Contrôle sécurité — les modifications sont **déclaratives** (front-matter) et **ne modifient pas** la surface d'exécution ni la posture de sécurité (aucune instruction exécutable, aucune frontière de délégation nouvelle : `disallowedTools: Task` **renforce** la frontière existante). La sollicitation systématique de l'Architecte cybersécurité reste requise dès qu'un stage ultérieur touche une surface de sécurité ([`reviewer.md`](../core/common/protocols/reviewer.md), plancher SG-3).

## Références

- **REF-001** : Issue ALI-194 (Stage 1 — Agents : front-matter AI-DLC, reviewers, connaissances) ; issue parente ALI-193 ; analyse ALI-184.
- **REF-002** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-003** : [ADR-0007 - Adaptation au modèle conductor / stages / protocols](0007-adaptation-modele-conductor-stages-protocols.md)
- **REF-004** : [`core/common/protocols/reviewer.md`](../core/common/protocols/reviewer.md) — deux natures de revue (cohérence / sécurité).
- **REF-005** : [`core/common/protocols/stage-definition.md`](../core/common/protocols/stage-definition.md) — champs `reviewer` / `review_class` du front-matter de stage.
- **REF-006** : [AI-DLC — Harness Engineer Guide, « Adding an Agent »](https://awslabs.github.io/aidlc-workflows/harness-engineering/03-adding-an-agent/)
- **REF-007** : [AI-DLC workflows (awslabs) — core/agents](https://github.com/awslabs/aidlc-workflows)
