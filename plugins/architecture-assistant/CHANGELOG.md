# Changelog — architecture-assistant

Format basé sur [Keep a Changelog](https://keepachangelog.com/) ; versionnage
[SemVer](https://semver.org/).

## [Non publié]

### Added
- **`README.md`** documentant le plugin : structure Agent Plugins v1.0.0, mapping
  des skills par **domaine et fonction** (architecture de solution, cycle
  OpenSpec/SDD, cybersécurité, architecture de données, présentation/avant-vente,
  transverse), statut MCP et règles de sécurité (HOM-278).
- **`mcp.json`** avec `mcpServers: {}` (aucun serveur MCP requis — valide selon
  la spec v1.0.0 §7.2.1) (HOM-278).
- **`CHANGELOG.md`** (ce fichier) pour tracer les modifications du plugin
  (HOM-278).

### Changed
- Alignement du plugin sur le standard du dépôt (modèle `homelab-assistant`) :
  `plugin.json` + `mcp.json` + `README.md` + `CHANGELOG.md` à la racine, skills
  conformes **Agent Skills** vérifiées par `scripts/validate_skills.sh`
  (20 skills, 0 échec) (HOM-278).

## [0.1.0]

### Added
- Manifeste `plugin.json` conforme Agent Plugins v1.0.0 (schéma fermé :
  `$schema` + `name` + métadonnées autorisées uniquement).
- Skills d'architecture de solution et de données sous `skills/`, chacune avec
  un `SKILL.md` conforme Agent Skills, regroupées par domaine :
  - **Architecture de solution** : `architecture-solution-gabarits`,
    `create-architecture-decision-record`, `aws-solution-architect`,
    `azure-solution-architect`, `windows-infrastructure-administration`,
    `project-defaults`.
  - **Cycle OpenSpec (SDD)** : `openspec-workflow`, `openspec-context-loading`,
    `openspec-proposal-creation`, `openspec-implementation`,
    `openspec-archiving`.
  - **Cybersécurité** : `cybersecurite`, `architecture-securite-gabarits`.
  - **Architecture de données** : `data-warehouse-ops`, `analytics-engineer`.
  - **Présentation & avant-vente** : `presentation-targeting`,
    `client-presentation-generation`, `sales-deck-generation`,
    `cdae-ai-eligibilite`.
  - **Transverse** : `git-delivery`.

### Security
- Aucun secret committé : les identifiants d'accès cloud et Git sont référencés
  via variables d'environnement / paramètres, jamais leurs valeurs.
