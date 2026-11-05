# Changelog — medical-assistant

Format basé sur [Keep a Changelog](https://keepachangelog.com/) ; versionnage
[SemVer](https://semver.org/).

## [Non publié]

### Added
- **`README.md`** documentant le plugin : structure Agent Plugins v1.0.0, mapping
  des skills par **fonction** (clinicien, biologiste, coach sportif,
  planification nutritionnelle, intégration domotique), statut MCP
  (serveur `home-assistant`) et règles de sécurité (HOM-278).
- **`CHANGELOG.md`** (ce fichier) pour tracer les modifications du plugin
  (HOM-278).

### Changed
- Alignement du plugin sur le standard du dépôt (modèle `homelab-assistant`) :
  `plugin.json` + `mcp.json` + `README.md` + `CHANGELOG.md` à la racine, skills
  conformes **Agent Skills** vérifiées par `scripts/validate_skills.sh`
  (7 skills, 0 échec) (HOM-278).

## [0.2.0]

### Added
- Manifeste `plugin.json` conforme Agent Plugins v1.0.0 (schéma fermé :
  `$schema` + `name` + métadonnées autorisées uniquement).
- `mcp.json` déclarant le serveur MCP **`home-assistant`** (`streamable-http`),
  consommé par la skill `home-assistant-calendrier`. Adresse et jeton
  externalisés en variables d'environnement (`HOMEASSISTANT_URL`,
  `HOMEASSISTANT_TOKEN`) — aucun secret committé.
- Skills médicales et para-médicales sous `skills/`, chacune avec un `SKILL.md`
  conforme Agent Skills :
  - `dossiers-medicaux` (+ `gabarits/`, `references/`)
  - `analyse-laboratoire`
  - `analyse-examens`
  - `suivi-morphologie`
  - `sportif-dossiers`
  - `recherche-repas` (+ `appareils/`)
  - `home-assistant-calendrier`

### Security
- Aucun secret committé : les accès Home Assistant sont référencés via variables
  d'environnement, jamais leurs valeurs.
- Les données de santé sensibles ne sont pas committées dans ce dépôt public ;
  les skills décrivent le traitement et l'archivage dans l'espace privé du
  patient.
