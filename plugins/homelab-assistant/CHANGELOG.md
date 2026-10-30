# Changelog — homelab-assistant

Format basé sur [Keep a Changelog](https://keepachangelog.com/) ; versionnage
[SemVer](https://semver.org/).

## [Non publié]

### Added
- **Skill `homelab-vault-access` — écriture encadrée de la clé `VERSION`** (parcours
  `service-version-update`, HOM-263). Nouvelle **Étape 3** : écriture en read-modify-write de la
  **seule** clé `VERSION` du montage `env_variables/data/<service>`, préservant toutes les autres
  clés ; corps POST via stdin (jamais en argument visible), vérification sans divulgation, token
  révoqué en fin. C'est le **seul** cas d'écriture autorisé de la skill (jamais le montage
  `services/`, jamais une autre clé), gardé par le **gate léger unique (A1)** du stage
  `version-update-application`. `description` du front-matter mise à jour en conséquence ; règle
  de sécurité ABSOLUE n° 7 ajoutée (écriture = exception unique). Voir `decisions/0044-…`.
- Skill `terraform-qa` — vérification adversariale d'une configuration Terraform
  (`.tf`/`.tfvars`) : structure HCL, conformité au template de stack, cohérence
  des variables (dont `cloudflare_dns_nb`), absence de `${SNI}` et de secret en
  clair, absence d'exécution Terraform. Skill agnostique du workflow (voir
  `decisions/0028-…`). Rattaché à l'agent **Analyste QA** dans le cadre de la
  réorganisation du workflow (`decisions/0027-…`). Ligne ajoutée au mapping des
  skills de `README.md`.

### Changed
- **Renommage `QA Docker` → `Analyste QA`** dans le mapping des skills de
  `README.md` : l'agent QA couvre désormais les livrables Docker Compose **et**
  Terraform (skill `terraform-qa` en plus de `docker-composer` /
  `dockerfile-validator`). Voir `decisions/0027-…` (réorganisation Phase 3 :
  Terraform avant compose, QA élargi au Terraform).

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
  Décision et actions de ré-intégration tracées dans `decisions/0024-…`.
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
