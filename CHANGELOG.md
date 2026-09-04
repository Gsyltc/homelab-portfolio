# Changelog

Toutes les évolutions notables de ce dépôt sont consignées ici.

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
Les décisions structurantes sont tracées dans [`decisions/`](decisions/) (ADR numérotés) ;
ce fichier en donne la lecture chronologique côté produit.

## [v1.0-homelab] — 2026-09-04

Jalon **Homelab** : le workflow d'orchestration Homelab passe d'une forme narrative unique
(`docs/homelab-workflow.md`) à la **forme déclarative AI-DLC** (*Harness Engineer Guide* —
`awslabs/aidlc-workflows`) — un fichier par élément, front-matter YAML, découverte et
pull-authoring — **sans importer le tooling non applicable** (`bun`, hooks `.ts`,
`dist/<harness>/`). Toutes les divergences assumées sont tracées en décisions structurantes
et validées par l'humain (validation granulaire).

### Added
- **Harness Homelab déclaratif** sous [`homelab/`](homelab/) (modèle conductor / stages / protocols) :
  - `homelab/common/conductor.md` + **26 fiches de stage** sur 5 phases
    (`initialisation`, `ideation`, `cadrage`, `production`, `validation`), corps en
    3 compartiments (`## Steps` / `## Sensors` / `## Learn`) et front-matter normalisé
    (`mode`, `review_class`, `human_gate`, `sensors:`, `scopes:`, `produces`/`consumes`/`requires_stage`).
  - `homelab/scopes/` — **7 scopes** (`new-stack`, `stack-update`, `config-change`,
    `security-patch`, `n8n`, `home-assistant`, `infra-terraform`) ; identité en données
    (`name`, `depth`, `verification`, `keywords`).
  - `homelab/rules/` — mémoire de règles **multi-couches** `global > stack > phase > scope` +
    boucle d'apprentissage ; couche `phase` complétée à 4 fichiers (ajout de `phases/ideation.md`).
  - `homelab/sensors/` — **6 manifestes de sensors** conformes au schéma amont
    (`id`/`kind`/`command`/`default_severity`/`fire_on`/`matches`) : `yaml-validity`,
    `swarm-deploy-section`, `plaintext-secret`, `terraform-no-sni`, `traefik-coherence`,
    `vault-secret-exists`.
  - `homelab/agents/` — **7 définitions d'agents** DevOps Homelab (front-matter
    `disallowedTools: Task`, `tier`, skills) : Tech Lead, Spécialiste Docker, QA Docker,
    Spécialiste Terraform, Expert n8n, Expert Home Assistant, Architecte de sécurité.
- **Décisions structurantes** (toutes *Accepted* sur validation humaine granulaire) :
  - ADR-0013 — cadrage de la refonte du workflow Homelab sur AI-DLC.
  - ADR-0014 — scopes Homelab et axes Depth / Stratégie de vérification.
  - ADR-0015 — learning loop et règles persistantes Homelab.
  - ADR-0016 — verification gates et sensors Homelab.
  - ADR-0017 — passage à 5 phases et mode d'autonomie Homelab.
  - ADR-0018 — adaptation du modèle conductor / stages / protocols au Homelab.
  - ADR-0019 — alignement des définitions d'agents Homelab sur AI-DLC.
  - ADR-0020 — alignement des fiches de stage Homelab sur AI-DLC.
  - ADR-0021 — alignement des scopes Homelab sur AI-DLC.
  - ADR-0022 — alignement des rules Homelab sur AI-DLC.
  - ADR-0023 — alignement des sensors Homelab sur AI-DLC.
  - ADR-0024 — retrait temporaire de SAML / LDAP de la sélection d'authentification (HOM-147).
- **Plugin `homelab-assistant`** complété (Agent Plugins v1.0.0) : skills `docker-composer`,
  `dockerfile-validator`, `traefik-manager-read`, `configuration-applications`,
  `homelab-vault-access` ; `mcp.json` ; `README.md` (mapping skills ↔ fonctions d'agent).

### Changed
- **Documentation d'entrée** (`README.md`, `AGENTS.md`) : ajout de l'arborescence déclarative
  `homelab/` et de la description de ses 5 éléments (agents, stages, scopes, rules, sensors) ;
  index des décisions porté à `0001…0024`.
- `docs/homelab-workflow.md` converti en **stub de redirection** vers la source unique
  `homelab/common/` (compatibilité ascendante préservée).
- **HOM-147** — retrait de **SAML** et **LDAP** de l'ordre de sélection d'authentification
  (ramené à `oidc → forwardauth → local`), cohérence workflow ↔ skills (ADR-0024).

### Fixed (vérification globale finale — ALI-214)
- **Marqueurs de conflit Git résiduels** dans `decisions/0011-alignement-memoire-de-regles-sur-ai-dlc.md`
  supprimés (résolution retenant la version canonique *Accepted* — multica.gaston, 2026-09-03).
- **Collision de numérotation ADR-0020** résolue : l'ADR SAML/LDAP (HOM-147, postérieur) est
  renuméroté **0024** ; l'ADR « alignement des fiches de stage » (ALI-210, antérieur et référencé
  dans la chaîne 0019→0023) conserve **0020**. Références mises à jour
  (`homelab/common/stages/cadrage/required-parameters-collection.md`,
  `plugins/homelab-assistant/CHANGELOG.md`, note de l'ADR-0021).

### Verified (non-régression — garde-fous opérationnels préservés)
- Cohérence d'ensemble des 5 éléments : **0 erreur / 0 avertissement** — toutes les références
  croisées se résolvent (`sensors:` → manifestes, `scopes:` → fichiers de scope,
  `requires_stage` → slugs, `reviewer` → `display_name` d'agent), traçabilité
  `produces`/`consumes` sans arête arrière orpheline, invariant `reviewer: null ⇒ review_class: none`.
- Garde-fous absolus **non surchargeables** intacts : `RULE-GL-004` (un seul traitement par
  stack), `RULE-GL-005` (aucun secret en clair), `RULE-GL-006` (pas de `${SNI}` en Terraform),
  `RULE-GL-007` (Terraform ne déploie jamais — `.tfvars` seulement), `RULE-GL-010` (règle
  absolue n8n) ; clause SEC-1 (érosion sémantique → rejet d'office).
- Validation humaine avant dépôt / Kestra (`human_gate: explicit` sur `file-deposit` et
  `kestra-deployment`) ; documentation officielle d'abord (`conductor.md`).

## [V1.0] — 2026-09-03

Première version publiée du monorepo `homelab-portfolio` : plugins d'agents (Agent Plugins v1.0.0),
workflow d'architecture de solution sous `core/`, workflow Homelab sous forme narrative
(`docs/homelab-workflow.md`) et registre de décisions `0001…0012`.

[v1.0-homelab]: https://github.com/Gsyltc/homelab-portfolio/compare/V1.0...v1.0-homelab
[V1.0]: https://github.com/Gsyltc/homelab-portfolio/releases/tag/V1.0
