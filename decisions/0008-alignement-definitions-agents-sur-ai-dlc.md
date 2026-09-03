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
2. **Reviewers** : décider si l'on modélise des personas « review-only » distincts (comme les 2 reviewers AI-DLC) ou si l'on conserve le champ `reviewer` sur les stages. → **Arbitrage humain** (ALI-194, « Créer des reviewers distinct ») : deux personas review-only distincts (voir § Décision 3).
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
| `consistency-reviewer-agent` | `balanced` | Persona **review-only** : juge un livrable contre des critères de cohérence explicites (entrée nouvelle, critères fixes). |
| `security-reviewer-agent` | `balanced` | Persona **review-only** : juge une surface de sécurité contre OWASP / STRIDE ; sortie sécurité-critique mais cadrée par des critères explicites de revue. |

Les deux personas **review-only** (Reviewer de cohérence, Reviewer de sécurité) sont classés `balanced` — profil « reviewer-shaped » du contrat AI-DLC (juger une entrée nouvelle contre des critères explicites). L'**Architecte cybersécurité** reste `judgment` : il conçoit et pilote la posture de sécurité (sortie sécurité-critique qui cascade), rôle distinct de la **revue** portée par le Reviewer de sécurité. `balanced` / `templated` projettent aujourd'hui à l'identique sur les harness où le tier ne change rien (Kiro/Cursor/Copilot héritent du modèle et de l'effort de session) ; le tier reste néanmoins **sémantiquement correct** et exploitable par un harness qui l'honore.

### 3. Reviewers — création de deux personas « review-only » distincts

Sur **directive humaine explicite** (« Créer des reviewers distinct », issue ALI-194), ce workspace **crée deux personas review-only distincts**, en miroir du modèle AI-DLC (2 reviewers), plutôt que de conserver la revue comme simple attribut porté par des fonctions productrices existantes :

- **`consistency-reviewer-agent`** — display_name **« Reviewer de cohérence »** ; porte la **revue de cohérence** (documentation ↔ décisions, absence de conflit / d'artefact orphelin, complétude, conventions).
- **`security-reviewer-agent`** — display_name **« Reviewer de sécurité »** ; porte la **revue de sécurité** (OWASP / STRIDE toujours actifs ; NIST / COBIT si docs risques ; normes réglementaires sur demande explicite), **obligatoire et non substituable** (plancher SG-3).

Les deux sont **review-only** : `disallowedTools: Task`, tier `balanced` (personas de revue qui jugent une entrée nouvelle contre des critères explicites), **ne produisent aucun livrable** et ne prennent aucune décision structurante.

**Rewiring** — le champ `reviewer:` des fiches de stage pointe désormais vers ces personas (fonctions) :

| Nature | Ancien `reviewer:` | Nouveau `reviewer:` | Stages |
| --- | --- | --- | --- |
| cohérence | Architecture Solution & Intégration | **Reviewer de cohérence** | `requirements-analysis`, `detailed-deliverables`, `mockups` |
| sécurité | Architecte cybersécurité | **Reviewer de sécurité** | `design-and-decisions`, `security-consistency-check`, `walking-skeleton`, `deployment-under-validation` |

**Séparation des rôles préservée** : le **coordinateur** *sollicite* désormais les reviewers (il ne porte plus lui-même la revue de cohérence). L'**Architecte cybersécurité** reste la fonction **d'analyse / production** de posture de sécurité (conception, durcissement, pilotage du scope `security-patch`), **distincte** du Reviewer de sécurité qui rend le **verdict de revue**. Les protocoles [`reviewer.md`](../core/common/protocols/reviewer.md), [`governance-security.md`](../core/common/protocols/governance-security.md), [`stage-definition.md`](../core/common/protocols/stage-definition.md), [`stage-protocol.md`](../core/common/protocols/stage-protocol.md) et [`scopes-and-axes.md`](../core/common/protocols/scopes-and-axes.md) sont mis à jour en conséquence. Les **invariants** (validation humaine granulaire, plancher SG-3 : la revue de sécurité ne peut être ni portée, ni remplacée, ni conditionnée par la revue de cohérence ou un gate advisory) restent intacts.

> **Supersession** : cette décision **révise** l'orientation initialement proposée (conservation du champ `reviewer:` sans persona dédié) à la suite de l'arbitrage humain. Elle reste cohérente avec [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md) (la revue demeure un attribut de stage `reviewer:` + `review_class:`) : seule la **fonction** cible du champ change, vers des personas dédiés.

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
- **POS-004** : Deux personas **review-only** distincts (cohérence / sécurité) alignés sur le modèle AI-DLC (2 reviewers) et sur la directive humaine ; séparation nette entre *sollicitation* (coordinateur), *analyse / production* (Architecte cybersécurité) et *verdict de revue* (Reviewers). Pas de source de connaissance concurrente (knowledge) — cohérence avec le modèle skills-Multica.
- **POS-005** : `reviewer:` des stages résout désormais vers une fonction dédiée et lisible dans `multica agent list` ; le routage A2A de la revue devient explicite.

### Négatives

- **NEG-001** : `disallowedTools: Task` est **inerte à l'exécution sur Multica** (pas d'outil `Task`) : valeur documentaire ; atténué par le fait qu'il matérialise une intention et satisfait le contrat pour tout futur portage de harness.
- **NEG-002** : La classification `tier` n'a **aucun effet** sur les harness qui héritent du modèle/effort de session (Kiro/Cursor/Copilot) ; elle reste néanmoins sémantiquement utile et sans coût.
- **NEG-003** : L'absence d'overlay `core/knowledge/<agent>/` impose de passer par l'import/assignation de skills pour enrichir un persona ; c'est le mécanisme Multica attendu, mais il diffère de l'amont (documenté ici).
- **NEG-004** : Deux fonctions de plus à provisionner sur Multica (import + assignation des agents « Reviewer de cohérence » / « Reviewer de sécurité », résolution d'UUID au moment de la mention) ; atténué par l'alignement au modèle AI-DLC et par la clarté du routage. **Changement de surface de sécurité** : la fonction qui rend le verdict de revue de sécurité passe de l'Architecte cybersécurité à un Reviewer de sécurité dédié — à soumettre au contrôle sécurité avant *Accepted* (voir IMP-005).

## Alternatives étudiées

### ALT-001 — Conserver `allowedTools: Multica`

**Raison du rejet** : hors contrat AI-DLC (le schéma ne connaît pas `allowedTools` ; la restriction se fait par `tools:`), et sans effet — un champ trompeur. Le contrat impose au contraire `disallowedTools`.

### ALT-002 — Ajouter une *allowlist* `tools:` restrictive par agent

**Raison du rejet** : sur Multica les capacités sont conférées par **assignation de skills**, pas par une *allowlist* d'outils de session. Une `tools:` restrictive n'aurait pas de correspondance runtime et risquerait de sur-contraindre à tort. Laisser hériter le toolset de session (recommandation amont : « most personas are best left to inherit everything »).

### ALT-003 — Conserver le champ `reviewer:` sans persona dédié (revue portée par le coordinateur + Architecte cybersécurité)

**Raison du rejet** : d'abord proposée (la revue comme fonction sollicitée par mention, tenue par des fonctions existantes), cette option a été **écartée sur arbitrage humain explicite** (« Créer des reviewers distinct », ALI-194) au profit de deux personas review-only, en miroir du modèle AI-DLC (2 reviewers). L'arbitrage humain prime.

### ALT-004 — Créer une arborescence `core/knowledge/<agent>/`

**Raison du rejet** : créerait une source de connaissance non chargée par le runtime Multica (découverte non automatique), concurrente des skills importées/assignées — divergence sans bénéfice d'exécution.

## Notes d'implémentation

- **IMP-001** : 9 fichiers `core/agents/*.md` existants modifiés — `allowedTools: Multica` retiré ; `disallowedTools: Task` + `tier` ajoutés. **2 fichiers créés** (`consistency-reviewer-agent.md`, `security-reviewer-agent.md`), portant le total à **11 agents**. Validité YAML du front-matter vérifiée sur les 11 (name=stem, `display_name` présent, `disallowedTools: Task`, `tier` ∈ {judgment, balanced, templated}).
- **IMP-002** : Reviewers — **2 personas review-only créés** (tier `balanced`) ; le champ `reviewer:` de 7 fiches de stage rewiré (3 cohérence, 4 sécurité) ; protocoles mis à jour ([`reviewer.md`](../core/common/protocols/reviewer.md) §1/§2 + mermaid, [`governance-security.md`](../core/common/protocols/governance-security.md) table des acteurs + section contrôle sécurité, [`stage-definition.md`](../core/common/protocols/stage-definition.md) schéma + liste des fonctions + règle SG-3, [`stage-protocol.md`](../core/common/protocols/stage-protocol.md), [`scopes-and-axes.md`](../core/common/protocols/scopes-and-axes.md) ligne matrice, `stages/inception/design-and-decisions.md`).
- **IMP-003** : Connaissances — **aucune arborescence `core/knowledge/`** créée ; les skills Multica (import + assignation) tiennent lieu d'overlay, conformément à [`README.md`](../README.md) / [`CONTRIBUTING.md`](../CONTRIBUTING.md).
- **IMP-004** : Pointeurs — `README.md` et `AGENTS.md` mentionnent `decisions/ (0001…0007)` ; mis à jour vers `0001…0008`.
- **IMP-005** : Contrôle sécurité — le front-matter est **déclaratif**, mais la **création d'un Reviewer de sécurité dédié** et le rewiring du `reviewer:` de sécurité **modifient une surface de gouvernance** (la fonction qui rend le verdict de revue de sécurité). Les **invariants sont préservés** : plancher SG-3 intact (la revue de sécurité reste obligatoire, non substituable, précède la validation humaine ; l'Architecte cybersécurité reste l'analyste/pilote). Cette modification de surface est **soumise au contrôle sécurité** (mention du Reviewer de sécurité / Architecte cybersécurité par le coordinateur) **avant** validation humaine et passage à *Accepted*, conformément à [`reviewer.md`](../core/common/protocols/reviewer.md) et [`governance-security.md`](../core/common/protocols/governance-security.md).

## Références

- **REF-001** : Issue ALI-194 (Stage 1 — Agents : front-matter AI-DLC, reviewers, connaissances) ; issue parente ALI-193 ; analyse ALI-184.
- **REF-002** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-003** : [ADR-0007 - Adaptation au modèle conductor / stages / protocols](0007-adaptation-modele-conductor-stages-protocols.md)
- **REF-004** : [`core/common/protocols/reviewer.md`](../core/common/protocols/reviewer.md) — deux natures de revue (cohérence / sécurité).
- **REF-005** : [`core/common/protocols/stage-definition.md`](../core/common/protocols/stage-definition.md) — champs `reviewer` / `review_class` du front-matter de stage.
- **REF-006** : [AI-DLC — Harness Engineer Guide, « Adding an Agent »](https://awslabs.github.io/aidlc-workflows/harness-engineering/03-adding-an-agent/)
- **REF-007** : [AI-DLC workflows (awslabs) — core/agents](https://github.com/awslabs/aidlc-workflows)
