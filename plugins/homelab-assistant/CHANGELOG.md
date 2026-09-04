# Changelog — homelab-assistant

Format basé sur [Keep a Changelog](https://keepachangelog.com/) ; versionnage
[SemVer](https://semver.org/).

## [1.0.0]

### Added
- Manifeste `plugin.json` conforme Agent Plugins v1.0.0 (schéma fermé :
  `$schema` + `name` + métadonnées autorisées uniquement).
- `mcp.json` avec `mcpServers: {}` (aucun serveur MCP homelab confirmé — voir
  `README.md`).
- 5 skills homelab sous `skills/`, chacun avec un `SKILL.md` conforme Agent
  Skills et ses fichiers annexes :
  - `configuration-applications` (+ `references/`)
  - `docker-composer` (+ `references/`)
  - `dockerfile-validator` (+ `scripts/`, `references/`, `examples/`, `tests/`)
  - `homelab-vault-access`
  - `traefik-manager-read`
- `README.md` documentant le mapping des skills (par **fonction** d'agent), le
  statut MCP et les règles de sécurité.

### Changed (corrections HOM-147 — cohérence workflow ↔ skills)
- **A2** — Retrait de **SAML** et **LDAP** de la sélection d'authentification
  (skill `configuration-applications` : `SKILL.md`, `references/authentification.md`,
  `references/template-stack.md`). Ordre ramené à `oidc → forwardauth → local`.
  Décision et actions de ré-intégration tracées dans `decisions/0020-…`.
- **A4** — Note ajoutée à `docker-composer/references/network.md` : `${SNI}`
  autorisée dans les labels compose, **interdite** dans les livrables Terraform.
- **A5 / A6** — La skill `docker-composer` est déclarée **source unique** de la
  règle des services mutualisés (Traefik/Redis-Valkey/PostgreSQL) et de la liste
  des réseaux Traefik ; le workflow la référence au lieu de la réénoncer.
- **A7** — `dockerfile-validator` : périmètre précisé (stacks *build-from-source*
  uniquement).

### Removed
- **A3** — La skill `ntfy-notifications` n'est **plus** embarquée ici : elle est
  **mutualisée** et conservée dans le plugin `general-purpose-assistant` (son
  porteur, l'Agent de notifications, est un agent partagé `core/`).

### Security
- Aucun secret committé : tous les identifiants (Vault AppRole, clé API Traefik)
  sont référencés via variables d'environnement, jamais leurs valeurs.
