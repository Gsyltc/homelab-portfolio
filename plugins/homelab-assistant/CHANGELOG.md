# Changelog — homelab-assistant

Format basé sur [Keep a Changelog](https://keepachangelog.com/) ; versionnage
[SemVer](https://semver.org/).

## [1.0.0]

### Added
- Manifeste `plugin.json` conforme Agent Plugins v1.0.0 (schéma fermé :
  `$schema` + `name` + métadonnées autorisées uniquement).
- `mcp.json` avec `mcpServers: {}` (aucun serveur MCP homelab confirmé — voir
  `README.md`).
- 6 skills homelab sous `skills/`, chacun avec un `SKILL.md` conforme Agent
  Skills et ses fichiers annexes :
  - `configuration-applications` (+ `references/`)
  - `docker-composer` (+ `references/`)
  - `dockerfile-validator` (+ `scripts/`, `references/`, `examples/`, `tests/`)
  - `homelab-vault-access`
  - `ntfy-notifications`
  - `traefik-manager-read`
- `README.md` documentant le mapping des skills, le statut MCP et les règles de
  sécurité.

### Security
- Aucun secret committé : tous les identifiants (Vault AppRole, ntfy, clé API
  Traefik) sont référencés via variables d'environnement, jamais leurs valeurs.
