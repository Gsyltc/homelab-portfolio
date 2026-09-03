# Protocole — scopes & axes d'exécution (Homelab)

Table partagée référencée par le [`conductor.md`](../conductor.md) et les fiches de stage. Le routage repose sur un **scope** nommé (parcours d'étapes déterministe et auditable) et deux **axes indépendants** — **Depth** (détail des artefacts) et **Stratégie de vérification** (intensité du QA Docker).

Miroir Homelab de [`core/common/protocols/scopes-and-axes.md`](../../../core/common/protocols/scopes-and-axes.md), avec les **7 scopes spécifiques au Homelab**.

> **Source d'identité vs vue lisible.** L'**identité** de chaque scope (nom, `depth`, `verification`, `keywords`, `branch`) est portée en données, **un fichier par scope**, sous [`../../scopes/`](../../scopes/README.md) (contrat amont « Scopes »). Ce document reste la **vue lisible** consolidée — table des scopes, axes, ordre de désambiguïsation, matrice stage × scope. **En cas d'écart sur l'identité d'un scope, le fichier `homelab/scopes/<name>.md` fait foi.** L'appartenance (quels stages tournent sous un scope) est transposée sur le champ `scopes:` des fiches de stage.

## Table des scopes

| Scope | Intention type | Traitement |
| --- | --- | --- |
| [`stack-update`](../../scopes/stack-update.md) *(défaut)* | Modification d'une stack existante | Parcours standard complet |
| [`new-stack`](../../scopes/new-stack.md) | Création complète d'une nouvelle stack | Complet + Depth comprehensive + vérification renforcée (plancher sécurité) |
| [`config-change`](../../scopes/config-change.md) | Variable existante, sans impact sécurité (≈ « allégé ») | Chemin court, Depth minimale, vérification advisory |
| [`security-patch`](../../scopes/security-patch.md) | Tout impact sécurité (auth, réseau, exposition, secrets, hardening, Traefik) | **Architecte de sécurité Homelab pilote**, plancher renforcé, sensors sécurité bloquants |
| [`infra-terraform`](../../scopes/infra-terraform.md) | Infra Terraform / Proxmox | Accent Spécialiste Terraform, compose ignoré |
| [`n8n`](../../scopes/n8n.md) | Toute demande n8n — **branche autonome** | Court-circuit immédiat → Expert n8n |
| [`home-assistant`](../../scopes/home-assistant.md) | Toute demande Home Assistant — **branche autonome** | Court-circuit immédiat → Expert Home Assistant |

Défaut : `stack-update`. **Invariants non négociables quel que soit le scope** (aucun scope ne les désactive) : règle absolue n8n, sélection auto d'authentification, validation humaine granulaire, aucune action à impact sans validation explicite, Terraform ne déploie jamais, aucun secret, jamais `${SNI}`, un seul traitement par stack, piste d'audit, contrôle sécurité minimal.

## Auto-détection & désambiguïsation

Scope auto-détecté par mots-clés (FR / EN) puis **confirmé explicitement** avant démarrage (jamais de démarrage silencieux). Les mots-clés déclencheurs sont **déclarés en données** dans le champ `keywords:` de chaque fichier [`../../scopes/<name>.md`](../../scopes/README.md) (source d'identité). Ordre de priorité en cas de correspondances multiples (**le niveau le plus élevé l'emporte**, héritage direct de la règle « allégé vs complet ») :

`n8n` = `home-assistant` (branches autonomes, court-circuit immédiat) > `security-patch` > `new-stack` > `infra-terraform` > `stack-update` > `config-change`

**Le doute ne bascule jamais vers `config-change`** : dès qu'un seul déclencheur d'un scope plus élevé s'applique — ou en cas de doute sur l'impact sécurité — le scope supérieur s'impose. L'auto-détection est un **plancher** : la confirmation humaine peut monter le contrôle, jamais le descendre sans trace.

## Axes

- **Axe 1 — Depth** : `minimal` / `standard` / `comprehensive` (détail des artefacts : docker-compose, config Terraform, documentation). Contrôle *combien on écrit*.
- **Axe 2 — Stratégie de vérification** : `advisory` / `standard` / `renforcé` (**intensité du QA Docker** et du contrôle qualité central). Contrôle *à quel point on vérifie*. Distinct de la Depth.
  - `advisory` — validité YAML + cohérence de base (syntaxe seule), signalée sans bloquer.
  - `standard` — QA Docker complet : compatibilité Swarm (`deploy`), réseaux/volumes/secrets, hardening standard, cohérence Traefik (`traefik-manager-read`).
  - `renforcé` — vérification `standard` **plus** audit de sécurité approfondi (secrets `_FILE`, exposition, permissions, absence de `${SNI}`, revue durcissement).

Les valeurs par défaut ci-dessous sont la **projection lisible** des champs `depth` / `verification` des fichiers de scope. **Le fichier `homelab/scopes/<name>.md` fait foi.**

| Scope | Depth défaut | Vérification défaut |
| --- | --- | --- |
| `stack-update` | standard | standard |
| `new-stack` | comprehensive | renforcé *(plancher — jamais abaissé)* |
| `config-change` | minimal | advisory |
| `security-patch` | comprehensive | renforcé *(plancher — jamais abaissé)* |
| `infra-terraform` | standard | standard |
| `n8n` | standard | standard |
| `home-assistant` | standard | standard |

**Points d'override** : à l'invocation, à la confirmation de scope, ou à un verification gate (relever seulement). **Garde-fou sécurité** : sur `security-patch` / `new-stack`, `depth` ≥ `standard` et vérification ≥ `renforcé` ne sont **jamais** abaissables ; tout re-scoping abaissant le contrôle exige une validation humaine tracée (voir [`governance-security.md`](governance-security.md)).

## Matrice stage × scope

Légende : ✅ activé · ➖ allégé / au juste nécessaire · ❌ ignoré · 🔒 renforcé · ⏭ branche autonome (ne passe pas par ce flux). Stages nommés par leur slug (voir [`../stages/`](../stages/)).

| Stage | `stack-update` | `new-stack` | `config-change` | `security-patch` | `infra-terraform` | `n8n` | `home-assistant` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Initialisation (0.x) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Idéation (1.x) | ✅ | ✅ | ➖ | ✅ | ✅ | ⏭ | ⏭ |
| `n8n-absolute-rule` | ✅ | ✅ | ✅ | ✅ | ✅ | 🔒 déclenche | ✅ |
| `intake-framing` | ✅ | ✅ | ➖ | ✅ | ✅ | ⏭ | ⏭ |
| `swarm-proxmox-arbitration` | ➖ | ✅ | ❌ | ➖ | ✅ | ⏭ | ⏭ |
| `required-parameters-collection` | ✅ | ✅ | ➖ | ✅ | ➖ | ⏭ | ⏭ |
| `autonomy-mode` | ✅ | ✅ | ➖ | ✅ | ✅ | ⏭ | ⏭ |
| `docker-compose-creation` | ✅ | ✅ | ➖ | ✅ | ❌ | ⏭ | ⏭ |
| `docker-compose-qa` | ✅ | ✅ 🔒 | ➖ | ✅ 🔒 | ❌ | ⏭ | ⏭ |
| `terraform-configuration` | ➖ | ✅ | ❌ | ➖ | ✅ | ⏭ | ⏭ |
| `n8n-branch` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `home-assistant-branch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `central-quality-control` | ✅ | ✅ 🔒 | ➖ | ✅ 🔒 | ✅ | ✅ | ✅ |
| Validation (4.x) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Ce que change chaque scope.** Un scope allégé (`config-change`) réduit le **nombre d'étapes** (Idéation resserrée, cadrage resserré, moins de contrôles intermédiaires) ; les scopes complets appliquent l'intégralité des phases 0 à 4. Dans tous les cas, la validation humaine avant toute action à impact et la répartition des rôles restent inchangées. **Un scope joue sur le nombre d'étapes, jamais sur qui les exécute** : alléger ne transfère jamais la responsabilité d'un spécialiste vers le Tech Lead.

Affectation des agents par scope, renforcements sécurité (`security-patch` / `new-stack` plancher renforcé + sensors bloquants, branches autonomes n8n / Home Assistant) : voir [`governance-security.md`](governance-security.md).

## Non applicable ici (tooling amont)

Pas de compilation `scope-grid.json`, pas de moteur TypeScript, pas de champs `runner` / `freeform_default` : l'exécution passe par **Multica** (mentions UUID, `trigger_outcomes`, statut d'issue, verrou metadata, piste d'audit), pas par le harness AI-DLC. On adopte la **forme déclarative** sans importer le moteur.
