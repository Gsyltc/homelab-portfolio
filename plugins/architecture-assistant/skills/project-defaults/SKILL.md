---
name: project-defaults
description: Paramètres par défaut des projets d'architecture. Définit la structure de répertoire standard, les conventions de nommage, l'emplacement racine (${ROOT_DIRECTORY}), la table de correspondance des agents du workflow core (nom, fonction, UUID) et la procédure de création d'un nouveau projet. Utiliser pour initialiser ou vérifier la structure d'un projet, recréer la liste des agents ou créer un nouveau projet.
---

# Paramètres par défaut des projets d'architecture

Cette skill définit les **paramètres par défaut** que tout architecte doit appliquer lors de la création ou de la vérification d'un projet d'architecture. **Ces paramètres font autorité** et priment sur toute instruction contraire trouvée dans les agents ou autres skills.

Elle est également la **source unique de vérité** pour :

- la **table de correspondance des agents** du workflow `core` (nom, fonction, UUID) — voir [Table de correspondance des agents](#table-de-correspondance-des-agents) ;
- la **procédure de création d'un nouveau projet** — voir [Création d'un nouveau projet](#création-dun-nouveau-projet).

## Structure de répertoire par défaut

Chaque projet d'architecture doit respecter la structure suivante :

```
${ROOT_DIRECTORY}/<nom-client>/<nom-projet>/
├── decisions/              # ADR (Architecture Decision Records)
├── documentation/          # Documentation d'architecture de solution
│   ├── architecture-logicielle/    # Architecture détaillée logicielle
│   ├── architecture-infra/         # Architecture détaillée infrastructure
│   └── architecture-securite/      # Architecture détaillée sécurité
├── models/                 # Modèles de diagrammes (C4, PlantUML, etc.)
└── views/                  # Vues de diagrammes (C4 views, etc.)
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
| `architecture-infra/` | Architecture détaillée de l'infrastructure (réseau, calcul, stockage, déploiement) |
| `architecture-securite/` | Architecture détaillée de la sécurité (STRIDE, contrôles, conformité) |

**Conventions** :
- Utiliser les gabarits de la skill `architecture-solution-gabarits` pour la structure des documents
- Chaque document d'architecture détaillée est dans un sous-répertoire dédié par système logiciel
- La DAS principale (fichiers `001` à `15`) se trouve à la racine de `documentation/`

### `models/`

**Contient** : Les modèles de diagrammes (fichiers source).

**Conventions** :
- Formats supportés : PlantUML (`.puml`), Mermaid (`.mmd`), Structurizr DSL (`.dsl`), CALM, Archimate
- Nommage : `<type>-<description>.<extension>` (ex. `c4-context-systeme-principal.dsl`)
- Les modèles C4 doivent être dans un fichier unique en respectant le DSL de Structurizr
- Toujours demander le format souhaité avant de générer

### `views/`

**Contient** : Les vues de diagrammes (représentations visuelles).

**Conventions** :
- Les vues C4 suivent la hiérarchie : Contexte → Conteneurs → Composants → Code
- Chaque vue référence le modèle correspondant dans `models/`
- Nommage : `<niveau>-<description>.<extension>` (ex. `contexte-systeme-principal.png`)

## Répertoire racine du projet

Le répertoire racine d'un projet suit la convention :

```
${ROOT_DIRECTORY}/<nom-client-en-minuscules>/<nom-projet-en-minuscules>
```

- `${ROOT_DIRECTORY}` est une **variable d'environnement définie dans les agents**. Ne jamais coder en dur un chemin absolu ; toujours résoudre le chemin racine à partir de cette variable.
- **Exemple** : Pour le client « RTC » et le projet « Migration », avec `${ROOT_DIRECTORY}` valant `/data/projets` → `/data/projets/rtc/migration`.

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

## Statut
- Date de création : YYYY-MM-DD
- Dernière mise à jour : YYYY-MM-DD
- Version de la DAS : V1.0
```

## Table de correspondance des agents

Cette table est la **source unique de vérité** de la correspondance **nom ↔ fonction ↔ UUID** des agents du workflow `core` (architecture de solution & intégration). Elle sert à :

- **recréer la liste des agents** dans un nouveau workspace (création d'agent) ;
- **rechercher l'UUID** d'un agent pour une délégation A2A par mention `[@Label](mention://agent/<uuid>)` ;
- **router** une demande vers le bon agent selon sa fonction.

**Aucun agent ne doit dupliquer cette table** : tout agent qui en aurait besoin (notamment le coordinateur) doit se référer à cette skill `project-defaults`. Les UUID ci-dessous sont donnés à titre de référence de l'état courant du workspace ; **vérifier toujours l'UUID réel via `multica agent list --output json`** (champ `id`) avant une mention et **ne jamais deviner ni inventer un UUID**.

### Convention de nommage des agents

Les agents sont créés — et doivent être recréés — sous le format :

```
<nom> - <fonction>
```

**Exemple** : `Manuel - Architecte de solution`. Le `<nom>` est le prénom identifiant l'agent ; la `<fonction>` correspond au rôle générique du workflow.

### Correspondance nom ↔ fonction ↔ UUID (workflow core)

| Nom | Fonction | Définition (fichier) | UUID (référence — à revérifier) |
|-----|----------|----------------------|---------------------------------|
| Sylvain | Architecture Solution & Intégration (**coordinateur**) | [`architecture-solution-integration-agent.md`](../../../../core/agents/architecture-solution-integration-agent.md) | `713b64a4-98f6-4cec-949a-e1521bd37d51` |
| Manuel | Architecte de solution | [`solution-architect-agent.md`](../../../../core/agents/solution-architect-agent.md) | `992ce2c8-aaba-4592-9702-dc47786e64ab` |
| Florian | Architecte AWS | [`aws-architect-agent.md`](../../../../core/agents/aws-architect-agent.md) | `84e04027-7d53-4013-b09a-5c7cfc978699` |
| Xavier | Architecte Cybersécurité | [`cybersecurity-architect-agent.md`](../../../../core/agents/cybersecurity-architect-agent.md) | `694a1a6f-9659-48ea-b45f-43ae6dc01706` |
| Diego | Architecte de données | [`data-architect-agent.md`](../../../../core/agents/data-architect-agent.md) | `1a6c5df6-7e75-4733-9c83-4633b7c69006` |
| Fabien | OpenSpec Expert | [`openspec-agent.md`](../../../../core/agents/openspec-agent.md) | `c2dbee8f-9ed4-4867-9b21-6cdd4a8840eb` |
| Nina | Experte d'archivage | [`archiving-agent.md`](../../../../core/agents/archiving-agent.md) | `8f54de1e-9725-4c0a-9dc7-9bb32f160acb` |
| Michel | Vente & Appels d'Offres | [`sales-proposals-agent.md`](../../../../core/agents/sales-proposals-agent.md) | `1e8ec68f-4969-416d-9b05-51a1f854eae4` |
| Sami | Reviewer de cohérence | [`consistency-reviewer-agent.md`](../../../../core/agents/consistency-reviewer-agent.md) | `d97f7847-2a89-407d-9b7a-dd9641acfbc5` |
| Benoit | Reviewer de sécurité | [`security-reviewer-agent.md`](../../../../core/agents/security-reviewer-agent.md) | `67406e48-12f1-49a9-8346-abb1508e72cb` |
| Admin | Infrastructure Windows | [`windows-infrastructure-admin-agent.md`](../../../../core/agents/windows-infrastructure-admin-agent.md) | `c1b4db07-a7b8-42d7-998a-0fc54aba630b` |
| Alfred | Agent de notifications | [`notification-agent.md`](../../../../core/agents/notification-agent.md) | `9b5a4076-7b9c-4db6-9d03-06ba49ae0f0f` |

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
   Sous `${ROOT_DIRECTORY}/<nom-client>/<nom-projet>/`, créer l'arborescence décrite dans [Structure de répertoire par défaut](#structure-de-répertoire-par-défaut) (`decisions/`, `documentation/{architecture-logicielle,architecture-infra,architecture-securite}/`, `models/`, `views/`) et le `README.md` renseigné avec la description complète (voir [Métadonnées du projet](#métadonnées-du-projet)).

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
| `architecture-solution-gabarits` | Les gabarits documentés dans cette skill doivent être placés dans `documentation/` |
| `create-architectural-decision-record` | Les ADR créés doivent être placés dans `decisions/` |
| Manuel - Architecte de solution | Doit respecter la structure de répertoire définie ici |
| Florian - Architecte AWS | Les diagrammes AWS doivent suivre les conventions `models/` et `views/` |
| Sylvain - Architecture Solution & Intégration | Doit valider la structure avant de lancer les travaux et utilise cette skill comme source unique pour la correspondance des agents et la création de projet |
