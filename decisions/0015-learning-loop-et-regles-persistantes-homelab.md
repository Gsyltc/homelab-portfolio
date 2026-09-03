# Boucle d'apprentissage et règles persistantes — Homelab

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : multica.gaston
accepté le : 2026-09-03
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — validation humaine explicite obtenue (multica.gaston, « Ok stage 3, Go » sur ALI-203 le 2026-09-03). L'humain a par ailleurs demandé de **ne pas créer l'agent Multica** « Architecte de sécurité Homelab » : le rôle reste décrit et référencé par les artefacts (`homelab/agents/security-architect-homelab-agent.md`), sans matérialisation d'un agent Multica exécutable (cf. IMP-006).

## Contexte

Le workflow Homelab (`docs/homelab-workflow.md`) capitalise ses décisions structurantes en ADR, mais **ne capitalisait pas les corrections humaines récurrentes** : une correction apportée par le QA Docker ou un spécialiste sur une stack pouvait devoir être répétée sur la suivante. L'analyse comparative avec AI-DLC 2.0 (issue parente ALI-200) a identifié cet écart (mécanisme **D** — Learning loop).

Le mécanisme équivalent pour `core-workflow.md` est documenté dans les ADR [0004](0004-boucle-apprentissage-et-regles-persistantes.md) (*Accepted*) et [0011](0011-alignement-memoire-de-regles-sur-ai-dlc.md) (*Accepted*), avec une mémoire de règles à 4 couches `workspace > project > phase > scope` sous `core/rules/`.

Le Stage 3 de la refonte Homelab (ALI-203, parente ALI-200) porte ce mécanisme au contexte Homelab : conventions Docker/Swarm, conventions Terraform, patterns de hardening récurrents, choix Traefik — en cohérence avec la gouvernance A2A du workflow Homelab (validation humaine granulaire, piste d'audit sur l'issue, garde-fous absolus) et avec les scopes Homelab du Stage 2 ([ADR-0014](0014-scopes-homelab-et-axes-depth-verification.md)).

## Décision

**Introduire une mémoire de règles multi-couches et une boucle d'apprentissage** capitalisant les corrections humaines validées en règles persistantes, dans le respect des invariants de gouvernance du Homelab.

### 1. Couches — quatre couches Homelab, nommage métier

La chaîne de précédence est **`global > stack > phase > scope`** — miroir structurel de `core/rules/` (`workspace > project > phase > scope`), avec un **nommage adapté au contexte Homelab** :

| Couche Homelab | Correspondance core | Fichier | Portée |
| --- | --- | --- | --- |
| `global` | `workspace` | `homelab/rules/global.md` | Invariants et conventions Homelab valables partout |
| `stack` | `project` | `homelab/rules/stacks/<stack>.md` | Spécifique à une stack (portainer, traefik, gitea, …) |
| `phase` | `phase` | `homelab/rules/phases/<phase>.md` | Par phase du workflow |
| `scope` | `scope` | `homelab/rules/scopes/<scope>.md` | Par scope (les 7 scopes Homelab) |

**Justification du renommage** :
- `workspace` → `global` : la mémoire de règles Homelab couvre le périmètre Homelab, pas le workspace Multica entier (qui a son propre `core/rules/workspace.md`). `global` dit « partout dans le Homelab ».
- `project` → `stack` : dans le Homelab, l'unité de travail est la **stack** Docker Swarm (portainer, traefik, gitea, …). Le nommage `stack` est plus naturel que `project` pour les agents et l'humain.

### 2. Emplacement — `homelab/rules/`

Miroir de `core/rules/`, cohérent avec les autres surfaces déclaratives Homelab (`homelab/scopes/`, `homelab/agents/`). Pas de `homelab/memory/` (même justification que l'ADR-0011 Q2 pour `core/rules/` vs `core/memory/`).

### 3. Boucle d'apprentissage — calquée sur le core, adaptée aux acteurs Homelab

Le cycle de vie est identique au core (ADR-0004) : capture → remontée → confirmation humaine → contrôle de conflit → écriture → application au prochain workflow. Adaptations Homelab :

- **Acteurs de la capture** : QA Docker (conventions compose, hardening technique), Spécialiste Docker (patterns de construction), Spécialiste Terraform (conventions `.tfvars`), Expert N8n et Expert Home Assistant (conventions de branche), Architecte de sécurité Homelab (durcissement, revue sécurité), Tech Lead Homelab (remontée au point de validation).
- **Contrôle sécurité de la couche `global`** : assuré par l'**Architecte de sécurité Homelab** (nouveau rôle, `homelab/agents/security-architect-homelab-agent.md`). Distinct du QA Docker : le QA Docker vérifie la conformité technique du compose (YAML, Swarm, hardening technique) ; l'Architecte de sécurité porte le **jugement sécurité** (analyse de risque, durcissement, revue des choix d'exposition/authentification) et contrôle l'admission des règles `global` et sécurité (SEC-2 / SEC-4). Décision prise sur retour humain (ALI-203, commentaire du 2026-09-03).
- **Périmètre de sécurité — sécurité de base d'un homelab** : le contrôle porte sur le hardening et la sécurité de base (secrets, exposition réseau, permissions, durcissement Docker/Swarm, Traefik). Le Homelab n'a **aucune notion** de Loi 25, PCI DSS, GDPR/RGPD, LPRPDE ni de protection réglementée des données personnelles — ces normes ne s'appliquent pas et ne sont jamais introduites.
- **Portée par défaut** : `stack` (la plus étroite — un apprentissage est d'abord spécifique à la stack qui l'a fait naître). Promotion vers `global` = décision structurante + contrôle sécurité systématique (SEC-4).
- **Application différée** : identique au core — une règle apprise s'applique au **prochain** workflow, jamais en cours de route.

### 4. Déclencheur de capture — systématique avec garde-fous

À chaque validation granulaire, le Tech Lead Homelab **propose systématiquement** les candidats-règles détectés dans la piste d'audit. L'écriture reste subordonnée à une validation humaine explicite. Balise `[candidat-règle]` dans les commentaires sur l'issue.

### 5. Contrôle de conflit à l'admission

- **Précédence des couches** : `global > stack > phase > scope` — une règle basse ne contredit jamais une règle haute sans arbitrage humain.
- **Invariants non contournables** : aucune règle ne peut affaiblir la validation humaine granulaire, les ADR, la piste d'audit, la règle absolue n8n, la sélection auto d'authentification, les garde-fous absolus (Terraform ne déploie jamais, aucun secret, pas de `${SNI}`, un seul traitement par stack), ni les garde-fous sécurité des scopes. Rejet d'office si contradiction.
- **Clauses SEC-1 à SEC-5** : adaptées du core (ADR-0004), portant sur l'érosion sémantique (SEC-1), le périmètre fondé sur le risque (SEC-2), l'interdiction d'exploitation dans le run courant (SEC-3), la promotion vers `global` (SEC-4) et l'intégrité du canal d'écriture (SEC-5).

### 6. Règles seedées — invariants existants formalisés

La couche `global` est seedée avec **12 règles** (`RULE-GL-001` à `RULE-GL-012`) reprenant les invariants non négociables déjà en vigueur dans `homelab-workflow.md` : gouvernance (4), sécurité (3), conventions Docker/Swarm (2), règles métier Homelab (3 : n8n §1.1, authentification §1.4, documentation officielle).

### 7. Articulation avec la piste d'audit

La capture (candidats, décision humaine) reste tracée **sur l'issue** ; seule la règle acceptée est écrite sur disque dans `homelab/rules/`. La règle porte toujours le lien `_origine_ : ALI-NNN` vers l'issue qui l'a fait naître.

### 8. Phases — trois fichiers, extensible à cinq

La couche `phase` a actuellement **trois fichiers** (`cadrage`, `production`, `validation`), correspondant aux 3 phases actuelles du workflow Homelab. Sera étendue à 5 fichiers au Stage 5 (passage à 5 phases : ajout `initialisation` bootstrap-only sans fichier de règles, et `idéation`). Cohérent avec l'approche core (ADR-0011 IMP-002).

## Conséquences

### Positives

- **POS-001** : Les corrections humaines récurrentes du Homelab sont capitalisées ; le QA Docker et les spécialistes ne répètent plus la même correction d'une stack à l'autre.
- **POS-002** : Règles versionnées, diffables et revues comme tout artefact (PR, au même titre que les ADR).
- **POS-003** : Structure en miroir de `core/rules/` — cohérence structurelle inter-workflows, courbe d'apprentissage réduite.
- **POS-004** : Le nommage métier (`global`/`stack` au lieu de `workspace`/`project`) est plus naturel pour les agents et l'humain dans le contexte Homelab.
- **POS-005** : Le contrôle de conflit et les invariants non contournables empêchent une règle apprise d'affaiblir la posture de sécurité ou la gouvernance.
- **POS-006** : Les clauses SEC-1 à SEC-5 (adaptées du core) ferment les vecteurs de dérive de gouvernance.

### Négatives

- **NEG-001** : `homelab/rules/` est un nouvel artefact à maintenir et à tenir cohérent (risque de dérive atténué par l'idempotence et la revue en PR).
- **NEG-002** : Effort supplémentaire au point de validation (proposition des candidats, choix de couche/portée) — atténué par la systématisation et le nommage métier.
- **NEG-003** : Divergence de nommage avec `core/rules/` (`global` vs `workspace`, `stack` vs `project`) — atténuée par le tableau de correspondance explicite.

## Alternatives étudiées

### ALT-001 — Reprise littérale des couches core (`workspace/project/phase/scope`)

Utiliser les mêmes noms de couches que `core/rules/` pour maximiser la cohérence.

**Raison du rejet** : `workspace` est ambigu (le workspace Multica entier a déjà `core/rules/workspace.md`) et `project` ne parle pas au contexte Homelab (l'unité de travail est la stack, pas un projet abstrait). Le nommage métier est plus lisible pour les agents et l'humain, et le tableau de correspondance explicite suffit à préserver la traçabilité.

### ALT-002 — Règles en métadonnée d'issue / metadata Multica

Stocker les règles dans la metadata Multica au lieu du repo.

**Raison du rejet** : même raison que l'ADR-0004 ALT-001 — la metadata est par-issue, non versionnée, non partagée et déconseillée pour du contenu long ; elle ne permet ni la revue ni le chargement « au démarrage de chaque workflow ».

### ALT-003 — Pas de boucle d'apprentissage (corrections uniquement ad hoc)

Conserver le fonctionnement actuel sans capitalisation.

**Raison du rejet** : c'est exactement l'écart identifié avec AI-DLC 2.0 — les mêmes corrections sont répétées d'une stack à l'autre sans être formalisées.

## Notes d'implémentation

- **IMP-001** : Section « Règles & boucle d'apprentissage » ajoutée à `docs/homelab-workflow.md`, entre la section « Scopes et axes d'exécution » et le « Modèle de collaboration A2A ».
- **IMP-002** : Structure scaffoldée dans `homelab/rules/` — `README.md`, `global.md` (12 règles seedées), `phases/{cadrage,production,validation}.md`, `stacks/_template.md`, `scopes/_template.md`.
- **IMP-003** : Une règle nouvellement écrite s'applique au **prochain** workflow ; l'exécution en cours n'est jamais altérée.
- **IMP-004** : L'articulation `SENSOR_PROPOSED` → liaison de sensor sera articulée au Stage 4 (ALI-204 — Verification gates + Sensors).
- **IMP-005** : La couche `phase` sera étendue de 3 à 5 fichiers au Stage 5 (ALI-205 — passage à 5 phases).
- **IMP-006** : Nouveau rôle **Architecte de sécurité Homelab** scaffoldé (`homelab/agents/security-architect-homelab-agent.md`, périmètre sécurité de base d'un homelab, sans conformité réglementaire), contrôleur sécurité de la couche `global` et des règles sécurité (SEC-2 / SEC-4). Ajouté au roster `homelab/agents/README.md`. **Décision humaine (ALI-203, 2026-09-03) : ne PAS créer l'agent Multica correspondant.** Le rôle vit uniquement comme **définition documentaire** (fiche + référence dans les artefacts) ; aucun agent Multica exécutable n'est instancié, aucun UUID A2A n'est attribué. Si le besoin d'un agent exécutable émerge plus tard, il fera l'objet d'une décision et d'une création explicites.

## Références

- **REF-001** : Issue ALI-203 (Stage 3 — Learning loop + règles persistantes Homelab) ; issue parente ALI-200.
- **REF-002** : [ADR-0004 - Boucle d'apprentissage et règles persistantes multi-couches](0004-boucle-apprentissage-et-regles-persistantes.md)
- **REF-003** : [ADR-0011 - Alignement de la mémoire de règles sur AI-DLC](0011-alignement-memoire-de-regles-sur-ai-dlc.md)
- **REF-004** : [ADR-0013 - Cadrage de la refonte Homelab](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)
- **REF-005** : [ADR-0014 - Scopes Homelab et axes Depth/Vérification](0014-scopes-homelab-et-axes-depth-verification.md)
- **REF-006** : [AI-DLC — Harness Engineer Guide, « Rules and the Learning Loop »](https://awslabs.github.io/aidlc-workflows/harness-engineering/05-rules-and-the-loop/)
