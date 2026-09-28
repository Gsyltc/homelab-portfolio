# Centralisation dans `project-defaults` : chemin racine `${ROOT_DIRECTORY}`, table de correspondance des agents et procédure de création de projet

---
auteurs: Mika (agent)
accepté par :
accepté le :
supersedes: ""
superseded_by: ""

---

## Status

Proposed

## Contexte

La skill `project-defaults` (workflow `core` d'architecture de solution & intégration) fait autorité sur la structure de répertoire, les conventions de nommage et les emplacements par défaut d'un projet d'architecture. Trois écarts limitaient sa portée :

1. **Chemin racine codé en dur.** La skill imposait un répertoire racine littéral `/nfs/workspace/alithya/<client>/<projet>`, spécifique à un hôte. Ce couplage empêche la réutilisation de la skill dans un autre environnement et contredit le reste du dépôt, où l'emplacement de travail est déjà résolu via la variable d'environnement `${ROOT_DIRECTORY}` (déjà utilisée, par exemple, par les fiches de stage du workflow `matching-cv-ao`).

2. **Absence de source unique pour la correspondance des agents.** Le workflow `core` désigne ses acteurs par rôle générique (fonction). La correspondance concrète **nom ↔ fonction ↔ UUID** — nécessaire pour recréer la liste des agents dans un nouveau workspace, rechercher un UUID et router une délégation A2A — n'était centralisée nulle part pour le workflow `core`. Le seul modèle existant, la « Table de correspondance » du **Tech Lead Homelab** ([`homelab/agents/tech-lead-homelab-agent.md`](../homelab/agents/tech-lead-homelab-agent.md)), appartient au **workflow Homelab** (autre équipe) et ne couvre pas les agents d'architecture.

3. **Aucune procédure outillée de création de projet.** La création d'un nouveau projet (projet workspace, liaison du dépôt, description, structure disque, agents et skills `core`) reposait sur des étapes implicites, non tracées dans une source unique.

Le format d'agent du workspace est `<nom> - <fonction>` (ex. `Manuel - Architecte de solution`) ; cette convention doit être explicitée pour permettre de recréer les agents à l'identique.

## Décision

**Faire de la skill `project-defaults` la source unique de vérité** pour ces trois points, et **l'exporter dans le dépôt** sous le plugin `architecture-assistant`.

Contenu de la décision :

- **DEC-001 — `${ROOT_DIRECTORY}`.** Remplacer toute référence au chemin littéral `/nfs/workspace/alithya` par la variable d'environnement `${ROOT_DIRECTORY}` (définie dans les agents). La convention de racine devient `${ROOT_DIRECTORY}/<nom-client-en-minuscules>/<nom-projet-en-minuscules>`. Aucun chemin absolu codé en dur.
- **DEC-002 — Table de correspondance des agents.** Ajouter à la skill une table **nom ↔ fonction ↔ UUID** des agents du workflow `core`, accompagnée de la convention de nommage `<nom> - <fonction>`. Cette table sert à recréer la liste des agents, rechercher un UUID et router les délégations. Les UUID y figurent comme référence de l'état courant, **toujours à revérifier via `multica agent list --output json`** ; ne jamais deviner ni inventer un UUID. **Aucun agent ne duplique cette table** : tout agent qui en a besoin (notamment le coordinateur `Architecture Solution & Intégration`) se réfère à la skill.
- **DEC-003 — Procédure de création d'un nouveau projet.** Ajouter à la skill la procédure ordonnée : (1) créer le projet dans le workspace, (2) ajouter le repository aux ressources du projet, (3) demander une description complète servant à la fois la description du projet workspace et le `README.md`, (4) créer la structure du projet sur le disque, (5) créer les agents du workflow `core` absents, (6) créer/importer les skills du workflow `core` absentes.
- **DEC-004 — Export dans le dépôt.** Exporter la skill à l'emplacement canonique [`plugins/architecture-assistant/skills/project-defaults/`](../plugins/architecture-assistant/skills/project-defaults/) (spec Agent Plugins v1.0.0), avec les fichiers auxiliaires existants (pipeline, `.gitignore`, `scripts/`).
- **DEC-005 — Retrait de toute duplication.** Le coordinateur `Architecture Solution & Intégration` renvoie explicitement à la skill pour la correspondance des agents et la création de projet, sans porter la table lui-même.

## Conséquences

### Positives

- **POS-001** : la skill devient portable — plus aucun chemin absolu spécifique à un hôte ; l'emplacement de travail est résolu par `${ROOT_DIRECTORY}`, cohérent avec le reste du dépôt.
- **POS-002** : une **source unique** pour la correspondance des agents du workflow `core` — recréation de la liste d'agents, recherche d'UUID et routage A2A s'appuient sur un seul document, réduisant le risque de tables divergentes.
- **POS-003** : la création d'un nouveau projet est **outillée et reproductible** (projet, repository, description, structure, agents, skills), avec la description saisie une seule fois et réutilisée (workspace + `README.md`).
- **POS-004** : la skill est disponible dans le dépôt (plugin `architecture-assistant`), donc versionnée, revue et réimportable dans tout workspace.

### Négatives

- **NEG-001** : les UUID inscrits dans la table sont un instantané ; ils doivent être revérifiés via `multica agent list --output json` avant toute mention. Atténuation : la skill l'exige explicitement et lie chaque agent à son fichier de définition (source de vérité du rôle).
- **NEG-002** : double emplacement de la skill (workspace + dépôt) à garder synchronisé lors des évolutions futures. Atténuation : le dépôt est l'emplacement canonique ; la mise à jour du workspace se fait par réimport/mise à jour de la skill.

## Alternatives étudiées

### ALT-001 — Porter la table de correspondance dans la définition du coordinateur (comme le Tech Lead Homelab)

Placer la table nom ↔ fonction ↔ UUID directement dans `architecture-solution-integration-agent.md`, à l'image de `tech-lead-homelab-agent.md`.

**Raison du rejet** : la demande impose une **source unique réutilisable** servant aussi à recréer la liste d'agents et à créer un projet — ce qui dépasse le rôle d'un seul agent. Loger la table dans un agent la rendrait non réutilisable et créerait une duplication à maintenir. La skill est l'emplacement neutre et partageable.

### ALT-002 — Conserver le chemin racine littéral et ne documenter `${ROOT_DIRECTORY}` qu'en commentaire

Garder `/nfs/workspace/alithya/...` comme valeur par défaut et mentionner la variable à côté.

**Raison du rejet** : maintiendrait un couplage à un hôte et une ambiguïté sur la source de vérité du chemin. La variable d'environnement, déjà employée ailleurs dans le dépôt, doit être l'unique convention.

## Notes d'implémentation

- **IMP-001** : [`plugins/architecture-assistant/skills/project-defaults/SKILL.md`](../plugins/architecture-assistant/skills/project-defaults/SKILL.md) — skill mise à jour (chemin `${ROOT_DIRECTORY}`, table de correspondance des agents, convention `<nom> - <fonction>`, procédure de création de projet, règles d'application) ; fichiers auxiliaires exportés (`bitbucket-pipeline.yml`, `.gitignore`, `scripts/`).
- **IMP-002** : [`core/agents/architecture-solution-integration-agent.md`](../core/agents/architecture-solution-integration-agent.md) — le coordinateur renvoie à la skill `project-defaults` pour la correspondance des agents et la création de projet ; aucune table dupliquée. Mise à jour miroir des instructions de l'agent dans le workspace.
- **IMP-003** : [`core/agents/README.md`](../core/agents/README.md) — README des agents du workflow `core` (rôles génériques → fichiers, renvoi à la skill `project-defaults` pour la correspondance nom ↔ fonction ↔ UUID).
- **IMP-004** : la skill du workspace (`project-defaults`) est mise à jour pour refléter le contenu exporté ; un `SKILL.md` du dépôt n'est pas découvert automatiquement à l'exécution — il doit être importé/mis à jour dans le workspace.
- **IMP-005** : validation humaine — ADR au statut `Proposed`, `accepté par`/`accepté le` laissés vides tant que l'humain n'a pas validé.

## Références

- **REF-001** : [`plugins/architecture-assistant/skills/project-defaults/SKILL.md`](../plugins/architecture-assistant/skills/project-defaults/SKILL.md) — skill créée/mise à jour par cette décision.
- **REF-002** : [`core/agents/`](../core/agents/) — définitions des agents du workflow `core` (source de vérité des rôles).
- **REF-003** : [`homelab/agents/tech-lead-homelab-agent.md`](../homelab/agents/tech-lead-homelab-agent.md) — modèle de table de correspondance (workflow Homelab), à l'origine du format retenu.
- **REF-004** : [AGENTS.md](../AGENTS.md) — standards du dépôt et règle de routage entre workflows ; emplacement canonique des skills sous `plugins/<nom>/skills/`.
