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
- **`architecture-solution-gabarits`** : porte désormais le **gabarit d'état de
  la checklist d'architecture** (`gabarits/00-checklist-architecture.md`),
  déplacé depuis `core/common/protocols/gabarits/`. C'est un **fichier d'état de
  processus** (copié en `documentation/00-checklist-architecture.md`), **pas** un
  fichier DAS : la **présence** est vérifiée en Initialization (stage
  `directory-check`, Step 3) et, **si absente**, l'init idempotente (copie du
  gabarit, 0 %) est **déléguée à la skill propriétaire** (par propriétaire,
  **sans couplage `core → plugin`**) ; règles de tenue (barème 80/10/10) en
  source unique dans `core/common/protocols/architecture-checklist.md`. Règle
  d'or **3-bis** ajoutée au `SKILL.md` (ADR-0047, HOM-286).
- **`architecture-solution-gabarits` — `SKILL.md` condensé** (HOM-286) : prose
  réduite au minimum sans perte, puces multi-niveaux, retrait des apartés et
  notes de processus, description resserrée. Les **20 règles d'or** et leurs
  numéros (dont `3-bis`, `5-bis`, 16, 17, 19, 20) sont **préservés** pour ne pas
  casser les renvois externes (gabarits, ADR). Objectif : économie de tokens.
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
