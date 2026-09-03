# Cadrage de la refonte de homelab-workflow.md sur AI-DLC 2.0

---
auteurs: Mika (agent)
accepté par : Sylvain G.
accepté le : 2026-09-03
supersedes: ""
superseded_by: ""

---

## Status

Accepted

## Contexte

Le document `docs/homelab-workflow.md` du dépôt `homelab-portfolio` est le contrat commun d'orchestration multi-agents (A2A) des travaux du **Homelab** (stacks Docker Swarm / Proxmox, configuration Terraform, n8n, Home Assistant). Il est aujourd'hui structuré en **3 phases** (`Cadrage et Paramètres` → `Production et Contrôle` → `Validation et Déploiement`), coordonnées par le Tech Lead Homelab.

L'analyse comparative (issue parente [ALI-200](https://github.com/Gsyltc/homelab-portfolio)) et la lecture directe du workflow actuel (branche `main`, 36 Ko) mettent en évidence des écarts avec la méthodologie AI-DLC 2.0 d'AWS (`awslabs/aidlc-workflows/core`), analogues à ceux déjà traités pour `core-workflow.md` via ALI-184 :

- **A** — 5 phases (Initialization → Ideation → Inception → Construction → Operation) vs 3 phases actuelles ; **Initialization** (bootstrap déterministe : stack existante vs nouvelle, lecture du verrou de concurrence, prérequis §3.0 anticipés) et **Ideation** (capture d'intention, faisabilité, arbitrage Docker Swarm / Proxmox formalisé) manquent.
- **B** — Scopes nommés + auto-détection + matrice stage×scope ; chez nous seule une grille **binaire** « allégé vs complet » existe.
- **C** — Depth et stratégie de vérification comme deux axes indépendants ; absents chez nous.
- **D** — Learning loop alimentant des règles persistantes versionnées ; absent.
- **E** — Sensors : checks déterministes advisory (YAML, section `deploy` Swarm, secret en clair, `${SNI}`, cohérence Traefik, existence Vault) ; nos contrôles reposent sur le jugement du QA Docker et du Tech Lead.
- **F** — Verification gates : contrôle automatique de traçabilité aux frontières de phases ; absent.
- **G** — Mode d'autonomie en Construction pour les modifications légères ; validation systématique partout aujourd'hui.

Points déjà conformes à conserver : gouvernance A2A (Tech Lead coordonne, spécialistes produisent), règle absolue n8n, règle préalable de documentation officielle, sélection automatique du type d'authentification, contrôle de concurrence par stack (verrou metadata `active_step`), validation humaine granulaire, chargement optimisé du contexte, piste d'audit sur l'issue + labels systématiques, règle A2A (mention UUID valide + `trigger_outcomes` + reprise bornée), prérequis §3.0 (`[répertoire de travail]`, Kestra), garde-fous absolus (aucun secret, jamais `${SNI}` en Terraform livré, Terraform ne déploie jamais, un seul traitement par stack).

Cinq arbitrages structurants ont été soumis à l'humain sur l'issue parente et tranchés ; deux précisions de cadrage (modèle de scopes, nomenclature de phases) ont été confirmées sur l'issue de cadrage ALI-201.

## Décision

Faire évoluer `docs/homelab-workflow.md` pour l'aligner sur les mécanismes clés d'AI-DLC 2.0, **tout en conservant la gouvernance A2A propre au Homelab et tous ses garde-fous absolus**.

**Ampleur** : **refonte complète** (5 phases + tous les mécanismes A→G), calquée sur l'approche livrée pour `core-workflow.md` (ALI-184).

**Structure des artefacts** : le répertoire `homelab/` est créé en **miroir de `core/`** — `homelab/agents/` (déjà livré via PR #74), `homelab/scopes/`, `homelab/rules/`, `homelab/sensors/`, `homelab/common/{conductor.md, stages/<phase>/, protocols/}`. Chaque artefact est créé **au stage qui l'introduit**, pas tout d'avance. Les ADR correspondants sont tracés dans `decisions/`.

**Terminologie** : **nomenclature propre au Homelab**, avec un **tableau de correspondance** vers les 5 phases AI-DLC (compatibilité ascendante + alias, même stratégie que l'[ADR-0002](0002-strategie-compatibilite-et-terminologie.md) du core) :

| Phase AI-DLC | Nom Homelab | Origine dans l'existant |
| --- | --- | --- |
| Initialization | Initialisation | nouveau (bootstrap : détection stack, verrou, prérequis §3.0) |
| Ideation | Idéation | nouveau (intention, faisabilité, arbitrage Swarm/Proxmox §1.3) |
| Inception | Cadrage et Paramètres | Phase 1 actuelle |
| Construction | Production et Contrôle | Phase 2 actuelle |
| Operation | Validation et Déploiement | Phase 3 actuelle |

**Modèle de scopes** (point de départ du Stage 2, confirmé au cadrage) : traduction de la grille binaire en scopes nommés Homelab, défaut `stack-update`.

| Scope | Déclencheur | Depth défaut | Vérification défaut |
| --- | --- | --- | --- |
| `new-stack` | création complète de stack | comprehensive | renforcé |
| `stack-update` | modification de stack existante (défaut) | standard | standard |
| `config-change` | variable existante, sans impact sécurité (≈ « allégé ») | minimal | advisory |
| `security-patch` | tout impact sécurité (auth, réseau, secrets, hardening, Traefik) | comprehensive | renforcé |
| `n8n` | mot « n8n » → branche autonome, délégation immédiate | standard | standard |
| `home-assistant` | Home Assistant → branche autonome | standard | standard |
| `infra-terraform` | Terraform / Proxmox | standard | standard |

Règle de désambiguïsation conservée : le niveau le plus élevé l'emporte, `security-patch` prioritaire, le doute ne bascule jamais vers `config-change`. Auto-détection = plancher (la confirmation humaine peut monter, jamais descendre sans trace). Règle absolue n8n et sélection automatique d'authentification préservées telles quelles.

**Ordre d'exécution** (confirmé, aucune modification) : Stage 1 (cadrage, bloquant) → Stage 2 (scopes + axes) → Stage 3 (learning loop) → Stage 4 (gates + sensors) → Stage 5 (5 phases + mode autonomie) → Stage 6 (consolidation + validation finale) → Stage 7 (modèle conductor/stages/protocols).

**Coordinateur** : le **Tech Lead Homelab** (`homelab/agents/tech-lead-homelab-agent.md`, UUID A2A préservé), livré via PR #74.

**Adaptations vs AI-DLC amont** : scopes et sensors **spécifiques au Homelab** ; front-matter des fiches de stage adapté au moteur A2A Multica (agents Homelab, mentions UUID, `trigger_outcomes`, verrou metadata). Le **harness TypeScript AI-DLC** (compilation `scope-grid.json`, runner `bun`/`aidlc-*.ts`) est **écarté** : on adopte la forme déclarative sans importer le moteur, comme documenté dans `core/scopes/README.md`.

**Format de diagramme** : **Mermaid** (statu quo).

**Publication** : commit / PR sur `homelab-portfolio`, avec validation humaine granulaire à chaque gate ; aucune sous-issue close sans feu vert humain.

Le workflow d'architecture (`docs/core-workflow.md`) est **hors périmètre**.

## Conséquences

### Positives

- **POS-001** : Adaptativité réellement outillée (scopes + axes Depth/Vérification) au lieu d'une grille binaire.
- **POS-002** : Capitalisation des corrections récurrentes (conventions Docker/Terraform/QA) en règles persistantes.
- **POS-003** : Fiabilisation déterministe (sensors, gates advisory) sans alourdir la charge humaine ni retirer la souveraineté de la validation granulaire.
- **POS-004** : Cohérence structurelle avec `core/` (miroir de répertoires, ADR numérotés) tout en gardant l'identité opérationnelle Homelab.
- **POS-005** : Livraison de valeur par étapes ; workflow utilisable entre chaque stage.

### Négatives

- **NEG-001** : Complexité documentaire accrue (nouveaux mécanismes et artefacts `homelab/` à maintenir).
- **NEG-002** : Maintien d'un tableau de correspondance de phases (alias) tant que les anciens libellés circulent.
- **NEG-003** : Risque d'incohérence transitoire tant que les 5 phases ne sont pas en place, mitigé par l'introduction advisory / opt-in des nouveaux mécanismes.

## Alternatives étudiées

### ALT-001 - Refonte incrémentale légère (garder 3 phases)

Conserver les 3 phases et n'enrichir que la grille (scopes) + learning loop.

**Raison du rejet** : l'humain a demandé de calquer sur ALI-184 (refonte complète 5 phases + tous mécanismes). L'incrémental priverait le Homelab des phases Initialization/Ideation et du mode d'autonomie.

### ALT-002 - Nomenclature AI-DLC anglaise directe

Adopter `Initialization / Ideation / Inception / Construction / Operation` comme libellés.

**Raison du rejet** : l'humain a tranché pour une nomenclature propre au Homelab (français, vocabulaire métier existant). Correspondance assurée par tableau d'alias.

### ALT-003 - Importer le harness TypeScript AI-DLC

Reprendre le tooling `bun`/`aidlc-*.ts` et la compilation `scope-grid.json`.

**Raison du rejet** : l'exécution passe par Multica (mentions A2A, statut d'issue, verrou metadata), pas par le harness AI-DLC. On adopte la forme déclarative sans le moteur.

## Notes d'implémentation

- **IMP-001** : Chaque mécanisme fait l'objet de son propre ADR au stage qui l'introduit (scopes, learning loop, sensors/gates, 5 phases/autonomie, modèle conductor), en miroir des ADR 0003–0012 du core.
- **IMP-002** : Les artefacts `homelab/` sont créés au stage qui les introduit ; `homelab/agents/` est déjà livré (PR #74).
- **IMP-003** : Critère de réussite : `homelab-workflow.md` révisé et validé par l'humain, ADR correspondants tracés, aucune régression de la gouvernance A2A, de la validation humaine granulaire ni des garde-fous absolus.

## Références

- **REF-001** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [ADR-0002 - Stratégie de compatibilité et terminologie](0002-strategie-compatibilite-et-terminologie.md)
- **REF-003** : [AI-DLC workflows (awslabs)](https://github.com/awslabs/aidlc-workflows)
