# Changelog — general-purpose-assistant

Format basé sur [Keep a Changelog](https://keepachangelog.com/) ; versionnage
[SemVer](https://semver.org/).

## [Non publié]

### Added
- **`README.md`** documentant le plugin : structure Agent Plugins v1.0.0, mapping
  des skills transverses par **fonction** (notifications, génération de guides,
  création de skills), statut MCP et règles de sécurité (HOM-278).
- **`mcp.json`** avec `mcpServers: {}` (aucun serveur MCP transverse requis —
  valide selon la spec v1.0.0 §7.2.1) (HOM-278).
- **`CHANGELOG.md`** (ce fichier) pour tracer les modifications du plugin
  (HOM-278).

### Changed
- Alignement du plugin sur le standard du dépôt (modèle `homelab-assistant`) :
  `plugin.json` + `mcp.json` + `README.md` + `CHANGELOG.md` à la racine, skills
  conformes **Agent Skills** vérifiées par `scripts/validate_skills.sh`
  (3 skills, 0 échec) (HOM-278).

## [0.1.0]

### Added
- Manifeste `plugin.json` conforme Agent Plugins v1.0.0 (schéma fermé :
  `$schema` + `name` + métadonnées autorisées uniquement).
- Skills transverses sous `skills/`, chacune avec un `SKILL.md` conforme Agent
  Skills :
  - `ntfy-notifications` — skill de notifications **mutualisée** (porteur : Agent
    de notifications, partagé `core/`).
  - `guide-utilisation-workflow-generation` (+ `assets/`) — génération des guides
    d'utilisation des workflows au format PDF.
  - `skill-authoring` — création et validation d'Agent Skills conformes
    agentskills.io.

### Security
- Aucun secret committé : les accès ntfy sont référencés via variables
  d'environnement (`NTFY_URL`, `NTFY_CHANNEL`, `NTFY_USER`, `NTFY_PASSWORD`),
  jamais leurs valeurs.
