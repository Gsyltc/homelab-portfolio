# Changelog — medical-assistant

Format basé sur [Keep a Changelog](https://keepachangelog.com/) ; versionnage
[SemVer](https://semver.org/).

## [Non publié]

### Changed
- **`sportif-dossiers` allégée** : `SKILL.md` réduit à l'essentiel (rôle, fichiers, versionnage, garde-fous) ; le détail est déporté dans `references/` chargées à la demande (`construction-programme`, `adaptation-sep`, `suivi-et-progression`, `revue-hebdomadaire`, `export-pdf`). Ajouts : collecte des informations manquantes (2-3 questions max + hypothèses), phase/critères de passage, RPE/RIR/tempo/régression, suivi RPE et douleur EVA, progression ~10 %/semaine, gêne vs signal d'alarme, adaptations SEP. Script PDF corrigé (imports). Agent `coach-sportif-clinique-biboumed` aligné (HOM-295).
- `sportif-dossiers` : le coach a le **rôle de physiothérapeute** (bilans Berg, TUG, Ashworth, FSS/MFIS réalisés et consignés) ; `adaptation-sep.md` fusionné avec les règles de rééducation neurologique SEP (HOM-295).

### Added
- `sportif-dossiers/references/sep-safety-precautions.md` (contre-indications, red flags) et `sep-edss-fatigue.md` (EDSS, fatigue, équilibre) (HOM-295).
- `sportif-dossiers/scripts/check_sportif.py` : sensors Python (`conforme | ecart | indisponible`) vérifiant le format de `suivi-sportif.md` et l'archivage de `programme-sportif.md` ; format du suivi formalisé dans `references/suivi-et-progression.md`, usage dans `references/sensors.md` (HOM-295).

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
