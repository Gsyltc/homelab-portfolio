---
name: project-defaults
description: Paramètres par défaut des projets d'architecture. Définit la structure de répertoire standard, les conventions de nommage, l'emplacement racine (${ROOT_DIRECTORY}), la table de correspondance des agents du workflow core (nom, fonction) et la procédure de création d'un nouveau projet. Utiliser pour initialiser ou vérifier la structure d'un projet, recréer la liste des agents ou créer un nouveau projet.
---

# Paramètres par défaut des projets d'architecture

Cette skill définit les **paramètres par défaut** que tout architecte doit appliquer lors de la création ou de la vérification d'un projet d'architecture. **Ces paramètres font autorité** et priment sur toute instruction contraire trouvée dans les agents ou autres skills.

Elle est également la **source unique de vérité** pour :

- la **table de correspondance des agents** du workflow `core` (nom, fonction) — voir [Table de correspondance des agents](#table-de-correspondance-des-agents) ;
- la **procédure de création d'un nouveau projet** — voir [Création d'un nouveau projet](#création-dun-nouveau-projet).

## Structure de répertoire par défaut

Chaque projet d'architecture doit respecter la structure suivante :

```
${ROOT_DIRECTORY}/<nom-client>/<nom-projet>/
├── decisions/              # ADR (Architecture Decision Records)
├── documentation/          # Documentation d'architecture de solution
│   ├── architecture-logicielle/    # Architecture détaillée logicielle
│   ├── architecture-donnees/        # Architecture détaillée des données
│   ├── architecture-infra/         # Architecture détaillée infrastructure
│   └── architecture-securite/      # Architecture détaillée sécurité
├── models/                 # Modèles de diagrammes (C4, PlantUML, etc.)
├── views/                  # Vues de diagrammes (C4 views, etc.)
└── presentations/          # Présentations archivées (horodatées)
```

## Description des répertoires

### `decisions/`

**Contient** : Toutes les Architecture Decision Records (ADR) du projet.

**Conventions** :
- Chaque ADR suit le format défini par la skill `create-architectural-decision-record`
- Nommage : `ADR-NNN-titre-en-kebab-case.md` (ex. `ADR-001-choix-base-de-donnees.md`)
- Numérotation séquentielle et croissante
- Un ADR approuvé ne doit pas être modifié ; un nouvel ADR le remplace si nécessaire

### `documentation/`

**Contient** : La documentation d'architecture de solution (DAS) complète.

**Sous-répertoires** :

| Sous-répertoire | Contenu |
|------------------|---------|
| `architecture-logicielle/` | Architecture détaillée de chaque système logiciel (composants, séquences, données) |
| `architecture-donnee/` | Architecture détaillée des données (modèles, flux, gouvernance des données, cycle de vie) |
| `architecture-infra/` | Architecture détaillée de l'infrastructure (réseau, calcul, stockage, déploiement) |
| `architecture-securite/` | Architecture détaillée de la sécurité (STRIDE, contrôles, conformité) |

**Conventions** :
- Utiliser les gabarits de la skill `architecture-solution-gabarits` pour la structure des documents
- Chaque document d'architecture détaillée est dans un sous-répertoire dédié par système logiciel
- La DAS principale (fichiers `001` à `15`) se trouve à la racine de `documentation/`

#### Répartition `!docs` / `!adrs` en DSL (Structurizr) : documentation globale ↔ détaillée

Dans les fichiers DSL Structurizr, répartir les directives `!docs` / `!adrs` selon le **niveau** de la documentation, sans doublon :

| Directive | Niveau | Attachement |
|-----------|--------|-------------|
| `!docs documentation` (racine de `documentation/`) | Documentation d'architecture de solution **globale** | **workspace** (`workspace.dsl`) |
| `!adrs decisions` | Décisions d'architecture **globales** | **workspace** (`workspace.dsl`) |
| `!docs documentation/<sous-répertoire>` (ex. `architecture-securite/`) | Documentation **détaillée** | **`softwareSystem` concerné** (ex. `origin`), jamais le workspace |

Rappels Structurizr : `!docs <dir>` importe le Markdown du répertoire indiqué **uniquement** (non récursif pour le Markdown) — racine et sous-répertoire ne se recouvrent donc pas (pas de doublon) ; `!docs` / `!adrs` s'attachent au **contexte parent** (workspace, software system ou container). **Zéro doublon** : une directive à un seul endroit.

### `models/`

**Contient** : Les modèles de diagrammes (fichiers source).

**Conventions** :
- Formats supportés : PlantUML (`.puml`), Mermaid (`.mmd`), Structurizr DSL (`.dsl`), CALM, Archimate
- Nommage : `<type>-<description>.<extension>` (ex. `c4-context-systeme-principal.dsl`)
- **Lorsque C4 est le format retenu** (voir la règle de sélection ci-dessous), les modèles C4 sont dans un **fichier unique** respectant le DSL de Structurizr
- Les diagrammes **réutilisent le thème du projet** (répertoire `theme/`, p. ex. `theme/0000-default-styles.dsl`) **lorsqu'il est disponible** (Structurizr, PlantUML, etc.) ; ne pas réinventer ni approximer un style quand le thème existe
- **Format de modélisation par défaut (règle de sélection)** : la norme **par défaut** d'un projet est **C4** (modélisé en Structurizr DSL). Si un **autre format est explicitement précisé** pour le projet — **ArchiMate** ou **CALM** — dans la **description du projet** (workspace Multica) **ou** le **`README.md` du projet**, alors **C4 n'est pas utilisé** : on utilise **le format défini**. Ordre de résolution :
  1. Format explicitement nommé dans la **description du projet** ou le **`README.md`** (`ArchiMate` ou `CALM`) → ce format fait foi, **C4 est écarté**.
  2. **Sinon → C4 par défaut** (Structurizr DSL).

  Mode opératoire du format retenu : [`references/structurizr.md`](references/structurizr.md) (C4), [`references/archimate.md`](references/archimate.md) (ArchiMate), [`references/calm.md`](references/calm.md) (CALM). Ne pas mélanger les formats pour un même projet ; en cas d'ambiguïté (plusieurs formats cités, mention contradictoire), demander l'arbitrage humain avant de générer.

### `views/`

**Contient** : Les vues de diagrammes (représentations visuelles), définies en **Structurizr DSL** (`views/000X-*.dsl`) et incluses (`!include`) depuis `workspace.dsl`.

**Conventions** :
- Les vues C4 suivent la hiérarchie : Contexte → Conteneurs → Composants → Code.
- Chaque vue référence le modèle correspondant dans `models/`.
- Nommage : `<ordre>-<description>.dsl` (préfixe numérique à 4 chiffres, ex. `0001-contexte.dsl`, `0008-lignage-donnees.dsl`) ; une **table de correspondance** à jour dans `views/README.md`.
- Le **modèle reste la source de vérité** : toute évolution d'une vue passe par les fichiers `views/000X-*.dsl` ; les définitions de modèle (acteurs, systèmes, conteneurs, liens) vivent sous `models/`.

#### Diagrammes : fichiers de référence à charger au besoin

L'intégration des diagrammes dans la DAS suit la convention **« vue `image` Structurizr rendue par kroki + `embed:` »**. Les instructions détaillées sont **déportées** dans des fichiers de référence **chargés uniquement au besoin** (production, intégration ou révision d'un diagramme) :

- ➡️ **[`references/kroki-diagrammes.md`](references/kroki-diagrammes.md)** — intégration des diagrammes à la DAS : règle `image`+kroki+`embed:`, proscription du `![](….svg)`, renderers par type de source, câblage `theme/0002-external-tools.dsl`, regroupement par famille et numérotation fixe (`0001`–`0006`+), validation DSL, traçabilité.
- ➡️ **[`references/structurizr.md`](references/structurizr.md)** — modèle C4 et vues : arborescence `workspace.dsl` / `models/` / `views/` / `theme/`, modèle = source de vérité, hiérarchie C4, validation (`structurizr.sh validate`), export / Structurizr Lite.
- ➡️ **[`references/archify.md`](references/archify.md)** — diagrammes HTML/SVG **pour les présentations client** (skill `archify`, agent « Présentation client ») : 5 types, flux `finalize`, garde d'authenticité ; **distinct** de l'intégration DAS.
- ➡️ **[`references/archimate.md`](references/archimate.md)** — modélisation **d'entreprise** ArchiMate (The Open Group / TOGAF) : couches Motivation/Stratégie/Métier/Application/Technologie, production en code (Archi `.archimate` ou PlantUML-Archimate), intégration DAS via `kroki plantuml`.
- ➡️ **[`references/calm.md`](references/calm.md)** — **CALM** (Common Architecture Language Model, FINOS, architecture-as-code JSON) : nodes/relationships/interfaces/controls/flows, validation CLI, toolchain (CALM Hub / CalmStudio / VS Code).

Règle minimale à retenir : tout diagramme (PlantUML, Mermaid, BPMN, …) est intégré à la DAS **exclusivement** via une vue `image` kroki référencée par `![…](embed:<clé>)` ; jamais de SVG inclus directement. Archify ne sert que la restitution (présentations), pas l'intégration DAS.

### `presentations/`

**Contient** : Les présentations archivées du projet (supports de revue, comités, présentations client, etc.).

**Conventions** :
- Chaque présentation est **horodatée** et archivée dans le répertoire `presentations/` du projet : `${ROOT_DIRECTORY}/<nom-client>/<nom-projet>/presentations/`
- Nommage : `<YYYY-MM-DD>-<nom-de-la-présentation>` (date ISO 8601 en préfixe), ex. `2026-10-02-revue-architecture-cible.pdf`
- La date correspond à la date de la présentation ; conserver chaque version archivée (ne pas écraser une présentation antérieure)

## Répertoire racine du projet

Le répertoire racine d'un projet suit la convention :

```
${ROOT_DIRECTORY}/<nom-client-en-minuscules>/<nom-projet-en-minuscules>
```

- `${ROOT_DIRECTORY}` est une **variable d'environnement définie dans les agents**. Ne jamais coder en dur un chemin absolu ; toujours résoudre le chemin racine à partir de cette variable.
- **Exemple** : Pour le client « monclient » et le projet « Migration », avec `${ROOT_DIRECTORY}` valant `/data/projets` → `/data/projets/monclient/migration`.

**Règles** :
- Le nom du client est toujours en **minuscules**
- Le nom du projet est toujours en **minuscules**
- Vérifier l'existence du répertoire avant tout travail
- Si le répertoire n'existe pas, demander confirmation à l'humain (hors procédure de création d'un nouveau projet, qui crée cette structure)

## Métadonnées du projet

Chaque projet doit contenir un fichier `README.md` à sa racine avec les métadonnées minimales :

```markdown
# <Nom du Projet>

## Description
<Description complète du projet — identique à la description du projet dans le workspace>

## Équipe
- Architecte de solution : <Nom>
- Architecte cloud : <Nom>
- Tech Lead : <Nom>

## Répertoires
- `decisions/` : ADR du projet
- `documentation/` : Documentation d'architecture de solution
- `models/` : Modèles de diagrammes
- `views/` : Vues de diagrammes
- `presentations/` : Présentations archivées (horodatées, `<YYYY-MM-DD>-<nom>`)

## Statut
- Date de création : YYYY-MM-DD
- Dernière mise à jour : YYYY-MM-DD
- Version de la DAS : V1.0
```

## Détermination de l'auteur par défaut d'un ADR

Cette règle **fait autorité** et s'applique à **tout** ADR du workflow : l'auteur par défaut d'un ADR est **toujours l'architecte de solution (humain) du projet**, et il doit être **déduit automatiquement**, dans l'ordre suivant, **sans solliciter l'humain tant qu'une source répond** :

1. **README du projet** — section `## Équipe`, ligne « Architecte de solution : <nom> » (voir [Métadonnées du projet](#métadonnées-du-projet)) ;
2. **sinon** l'arrimage du document `001-document-architecture-solution.md` — matrice RACI, rôle « Architecte de solution », colonne « Nom ».

**Ne demander le ou les noms des auteurs à l'humain que si l'information est absente des deux sources.** Ne jamais inscrire le nom d'un agent comme auteur. Un auteur supplémentaire explicitement fourni par l'humain complète ou remplace ce défaut.

> La skill `create-architecture-decision-record` applique cette règle ; elle ne la duplique pas comme source : cette section de `project-defaults` est la **source unique de vérité**.

## Table de correspondance des agents

Cette table est la **source unique de vérité** de la correspondance **nom ↔ fonction** des agents du workflow `core` (architecture de solution & intégration). Elle sert à :

- **recréer la liste des agents** dans un nouveau workspace (création d'agent) ;
- **rechercher l'UUID** d'un agent pour une délégation A2A par mention `[@Label](mention://agent/<uuid>)` ;
- **router** une demande vers le bon agent selon sa fonction.

**Aucun agent ne doit dupliquer cette table** : tout agent qui en aurait besoin (notamment le coordinateur) doit se référer à cette skill `project-defaults`. Cette table ne fige **aucun UUID** : chaque workspace a ses propres UUID. **Résoudre l'UUID d'un agent via `multica agent list --output json`** (champ `id`) avant chaque mention, en s'appuyant sur son nom/sa fonction ci-dessous, et **ne jamais deviner ni inventer un UUID**.

### Convention de nommage des agents

Les agents sont créés — et doivent être recréés — sous le format :

```
<nom> - <fonction>
```

**Exemple** : `Manuel - Architecte de solution`. Le `<nom>` est le prénom identifiant l'agent ; la `<fonction>` correspond au rôle générique du workflow.

### Correspondance nom ↔ fonction (workflow core)

| Nom | Fonction | Définition (fichier) |
|-----|----------|----------------------|
| Sylvain | Architecture Solution & Intégration (**coordinateur**) | [`architecture-solution-integration-agent.md`](../../../../core/agents/architecture-solution-integration-agent.md) |
| Manuel | Architecte de solution | [`solution-architect-agent.md`](../../../../core/agents/solution-architect-agent.md) |
| Florian | Architecte AWS | [`aws-architect-agent.md`](../../../../core/agents/aws-architect-agent.md) |
| Xavier | Architecte Cybersécurité | [`cybersecurity-architect-agent.md`](../../../../core/agents/cybersecurity-architect-agent.md) |
| Diego | Architecte de données | [`data-architect-agent.md`](../../../../core/agents/data-architect-agent.md) |
| Fabien | OpenSpec Expert | [`openspec-agent.md`](../../../../core/agents/openspec-agent.md) |
| Nina | Experte d'archivage | [`archiving-agent.md`](../../../../core/agents/archiving-agent.md) |
| Michel | Vente & Appels d'Offres | [`sales-proposals-agent.md`](../../../../core/agents/sales-proposals-agent.md) |
| Camille | Présentation client | [`client-presentation-agent.md`](../../../../core/agents/client-presentation-agent.md) |
| Sami | Reviewer de cohérence | [`consistency-reviewer-agent.md`](../../../../core/agents/consistency-reviewer-agent.md) |
| Benoit | Reviewer de sécurité | [`security-reviewer-agent.md`](../../../../core/agents/security-reviewer-agent.md) |
| Admin | Infrastructure Windows | [`windows-infrastructure-admin-agent.md`](../../../../core/agents/windows-infrastructure-admin-agent.md) |
| Alfred | Agent de notifications | [`notification-agent.md`](../../../../core/agents/notification-agent.md) |

> La définition conforme (front-matter + corps) de chaque agent vit dans [`agents/`](../../../../core/agents/). Pour (re)créer un agent, utiliser le `display_name` du fichier comme `<fonction>` et l'associer à son `<nom>` selon la table ci-dessus, au format `<nom> - <fonction>`.

## Création d'un nouveau projet

À la **demande de création d'un nouveau projet**, appliquer la procédure suivante dans l'ordre. Chaque étape à impact (création de projet, dépôt de fichiers, création d'agents/skills) reste soumise à la **validation humaine granulaire** définie dans la gouvernance du workflow.

1. **Créer le projet dans le workspace.**
   `multica project create --name "<nom-projet>" ...` (résoudre les options via `multica project create --help`). Le projet porte le nom du projet.

2. **Ajouter le repository dans les ressources du projet.**
   Lier le dépôt Git du projet aux ressources du projet dans le workspace, afin que chaque run démarre informé.

3. **Demander une description complète du projet.**
   Solliciter l'humain pour une description complète. Cette description sert **à deux endroits** :
   - la **description du projet** dans le workspace (champ description du projet Multica) ;
   - le fichier **`README.md`** à la racine du projet (section `## Description`).
   Ne pas inventer la description : si elle n'est pas fournie, la demander avant de continuer.

4. **Créer la structure du projet sur le disque.**
   Sous `${ROOT_DIRECTORY}/<nom-client>/<nom-projet>/`, créer l'arborescence décrite dans [Structure de répertoire par défaut](#structure-de-répertoire-par-défaut) (`decisions/`, `documentation/{architecture-logicielle,architecture-infra,architecture-securite,architecture-donnees}/`, `models/`, `views/`, `presentations/`) et le `README.md` renseigné avec la description complète (voir [Métadonnées du projet](#métadonnées-du-projet)).

5. **Créer les agents du workflow `core` s'ils n'existent pas.**
   Vérifier via `multica agent list --output json` la présence des agents de la [Table de correspondance des agents](#table-de-correspondance-des-agents). Pour chaque agent absent, le créer au format `<nom> - <fonction>` à partir de sa définition dans [`agents/`](../../../../core/agents/) (front-matter + corps).

6. **Créer les skills du workflow `core` s'ils n'existent pas.**
   Vérifier via `multica skill list --output json` la présence des skills du workflow `core` (portées par le plugin [`architecture-assistant`](../../)) et, pour chacune absente, l'importer (`multica skill import`) puis l'assigner aux agents concernés (`multica agent skills add|set`). Un `SKILL.md` présent dans le dépôt n'est **pas** découvert automatiquement à l'exécution : il faut l'importer dans le workspace.

## Règles d'application

1. **Par défaut** : Ces paramètres s'appliquent à tout nouveau projet d'architecture
2. **Priorité** : Ces paramètres priment sur toute instruction contraire dans les agents ou skills existants
3. **Héritage** : Les agents (Manuel, Florian, Sylvain, …) et les skills (`architecture-solution-gabarits`, `create-architectural-decision-record`) doivent respecter cette structure
4. **Table de correspondance** : Aucun agent ne duplique la table de correspondance des agents ; tout agent s'y référant utilise cette skill comme source unique
5. **Exception** : Seule une instruction explicite de l'humain peut déroger à ces paramètres
6. **Vérification** : Avant de commencer tout travail, vérifier que la structure du projet respecte ces conventions

## Cohérence avec les skills et agents existants

| Skill / Agent | Relation avec cette skill |
|---------------|---------------------------|
| `architecture-solution-gabarits` | Les gabarits documentés dans cette skill doivent être placés dans `documentation/` ; les **diagrammes générés en code** (règle d'or 9) sont intégrés à la DAS selon la convention « vues `image` kroki + `embed:` » de la section [`views/`](#views) ci-dessus |
| `create-architectural-decision-record` | Les ADR créés doivent être placés dans `decisions/` |
| Manuel - Architecte de solution | Doit respecter la structure de répertoire définie ici |
| Florian - Architecte AWS | Les diagrammes AWS doivent suivre les conventions `models/` et `views/` |
| Sylvain - Architecture Solution & Intégration | Doit valider la structure avant de lancer les travaux et utilise cette skill comme source unique pour la correspondance des agents et la création de projet |
