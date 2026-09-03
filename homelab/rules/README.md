# Règles persistantes — mémoire du workflow Homelab

Ce répertoire contient la **mémoire de règles multi-couches** alimentée par la **boucle d'apprentissage** du workflow Homelab.
Les règles capitalisent les **corrections humaines validées** afin qu'un agent (QA Docker, Spécialiste Docker, Spécialiste Terraform, Expert N8n, Expert Home Assistant) ne répète pas la même erreur d'une stack à l'autre. Elles sont des **fichiers Markdown versionnés**, lisibles au démarrage de chaque workflow (chargement paresseux — voir plus bas).

Pendant Homelab de [`../../core/rules/`](../../core/rules/README.md) : même forme déclarative, identifiants stables, rubriques topicales — **couches et conventions spécifiques au Homelab** (Docker Swarm / Proxmox / Terraform / Traefik / n8n / Home Assistant).

## Alignement sur le contrat amont et le modèle core

Cette mémoire de règles est alignée sur :

- Le contrat amont **« Rules and the Learning Loop »** (*Harness Engineer Guide*, `awslabs/aidlc-workflows`).
- La mémoire de règles `core/rules/` (ADR [`decisions/0004`](../../decisions/0004-boucle-apprentissage-et-regles-persistantes.md), [`decisions/0011`](../../decisions/0011-alignement-memoire-de-regles-sur-ai-dlc.md)).

**Divergences assumées et tracées** dans [`decisions/0015`](../../decisions/0015-learning-loop-et-regles-persistantes-homelab.md) :

- **Chaîne à 4 couches core** `workspace > project > phase > scope` → ici **4 couches Homelab** `global > stack > phase > scope` :
  - `workspace` → **`global`** : renommé pour refléter la portée Homelab (invariants et conventions valables pour tout le Homelab, pas le workspace Multica entier).
  - `project` → **`stack`** : dans le Homelab, l'unité de travail est la **stack** (portainer, traefik, gitea, …), pas un « projet » abstrait. Même rôle, nommage métier.
  - `phase` et `scope` : conservés à l'identique (cohérence structurelle avec `core/rules/`).
- **Emplacement** : `homelab/rules/` (miroir de `core/rules/`, cohérent avec `homelab/scopes/`, `homelab/agents/`).
- **Phases** : comme le core, la couche `phase` a **trois fichiers** (`cadrage`, `production`, `validation`) correspondant aux 3 phases actuelles du workflow Homelab. Sera étendue à 5 fichiers au Stage 5 (passage à 5 phases). L'`initialisation` est bootstrap-only et **ne porte pas** de fichier de règles.
- **Scopes** : les 7 scopes Homelab de [`homelab/scopes/`](../scopes/README.md) (`stack-update`, `new-stack`, `config-change`, `security-patch`, `infra-terraform`, `n8n`, `home-assistant`).

## Couches (de la plus forte à la plus faible précédence)

| Couche | Fichier | Portée | Chargement | Correspondance core |
| --- | --- | --- | --- | --- |
| `global` | [`global.md`](global.md) | Invariants et conventions Homelab valables partout | Au démarrage (toujours actif) | `workspace` |
| `stack` | `stacks/<stack>.md` | Spécifique à une stack (portainer, traefik, gitea, …) | Au démarrage, uniquement la stack courante | `project` |
| `phase` | `phases/<phase>.md` (`cadrage`, `production`, `validation`) | Par phase du workflow | À la demande, quand la phase est déclenchée | `phase` |
| `scope` | `scopes/<scope>.md` (les 7 scopes Homelab) | Par scope | À la demande, quand le scope est confirmé | `scope` |

**Précédence** : `global` > `stack` > `phase` > `scope`. Une règle d'une couche **ne peut pas contredire** une règle d'une couche supérieure sans arbitrage humain (contrôle de conflit à l'admission). Cette précédence explicite **préserve et renforce** l'invariant amont « conflit réglé à l'écriture, jamais au runtime ».

## Boucle d'apprentissage (learning loop)

### Cycle de vie d'une règle

1. **Capture** : pendant une étape, chaque correction / rejet / reformulation humaine sur un choix est un *candidat-règle* potentiel (tracé sur l'issue). Le QA Docker, les spécialistes et le Tech Lead Homelab génèrent des candidats quand ils corrigent une convention récurrente (ex. `_FILE` pour secrets, placement d'un healthcheck, réseau Traefik par défaut, `.tfvars` oublié).
2. **Remontée** : au point de validation humaine, le Tech Lead Homelab propose les candidats formulés en règles courtes, avec couche et portée proposées.
3. **Confirmation humaine** : l'humain garde ✅ / rejette ❌ / reformule 💬 chaque candidat séparément. Rien n'est écrit sans validation explicite.
4. **Contrôle de conflit à l'admission** : précédence des couches + invariants non contournables + (pour toute règle `global`) contrôle sécurité systématique par l'**Architecte de sécurité Homelab**.
5. **Écriture** : la règle acceptée est ajoutée au fichier de sa couche, avec un identifiant, la date et le lien vers l'issue d'origine.
6. **Application au prochain workflow** : une règle nouvellement écrite n'altère jamais l'exécution en cours ; elle prend effet au démarrage du **prochain** workflow.

### Déclencheurs de capture

La capture est **systématique** : à chaque validation granulaire, le Tech Lead Homelab propose les candidats-règles détectés dans la piste d'audit. L'écriture reste subordonnée à une validation humaine explicite (garde-fou).

Déclencheurs principaux :

- **Correction QA Docker** : le QA Docker corrige une convention → candidat (`_FILE` pour secrets, section `deploy` manquante, healthcheck mal placé, réseau Traefik par défaut).
- **Revue de l'Architecte de sécurité Homelab** : un durcissement ou une correction de sécurité récurrente (exposition, permissions, secrets, TLS Traefik) → candidat de portée sécurité.
- **Arbitrage humain** : l'humain tranche un point récurrent → candidat (ex. choix Swarm vs Proxmox pour un type de service, convention `.tfvars` pour un type de variable).
- **Correction Spécialiste** : un spécialiste (Docker, Terraform) corrige un pattern récurrent → candidat.
- **Échec de sensor** (Stage 4) : un check déterministe échoue de manière récurrente sur le même type d'erreur → candidat de liaison sensor (`SENSOR_PROPOSED`, articulé au Stage 4).

### Portée par défaut

**`stack`** (la plus étroite dans le contexte Homelab). La promotion vers `global` est une **décision structurante** soumise au contrôle sécurité systématique (SEC-4 adapté) — justifié par le fait que `global` porte les invariants non abaissables de tout le Homelab.

## Format d'une règle

Chaque règle est une entrée de liste avec un identifiant stable :

| Couche | Préfixe | Exemple |
| --- | --- | --- |
| `global` | `RULE-GL-NNN` | `RULE-GL-001` |
| `stack` | `RULE-ST-NNN` | `RULE-ST-001` |
| `phase` | `RULE-PH-NNN` | `RULE-PH-001` |
| `scope` | `RULE-SC-NNN` | `RULE-SC-001` |

```md
- **RULE-GL-001** — Tout docker-compose Swarm doit inclure une section `deploy` avec contraintes de placement.
  - _portée_ : global · _origine_ : ALI-000 · _ajoutée le_ : AAAA-MM-JJ
```

**Rubriques topicales** (convention alignée sur le contrat amont et sur `core/rules/`) : dans un fichier de couche, les règles se rangent sous des **rubriques topicales** en prose — par ex. `## Conventions Docker/Swarm`, `## Conventions Terraform`, `## Sécurité / Hardening`, `## Conventions Traefik`, `## Manière de travailler` — une règle = une puce sous la rubrique idoine. Les rubriques sont **indicatives** (à créer selon le besoin) ; l'identifiant `RULE-*`, la portée, l'origine et la date restent **obligatoires** (traçabilité, clause SEC-5 adaptée). Voir les gabarits [`stacks/_template.md`](stacks/_template.md) et [`scopes/_template.md`](scopes/_template.md).

## Invariants non contournables

Aucune règle apprise, à aucune couche, ne peut affaiblir :

- la **validation humaine granulaire** (avant toute action à impact : dépôt fichiers, flux Kestra) ;
- l'**ADR** sur chaque décision structurante ;
- la **piste d'audit** sur l'issue ;
- la **règle absolue n8n** (§1.1 — délégation immédiate, pas même l'analyse) ;
- la **sélection automatique du type d'authentification** (§1.4, `oidc → saml → ldap → forwardauth → local`) ;
- les **garde-fous absolus** : Terraform ne déploie jamais, aucun secret en clair, jamais `${SNI}` en Terraform livré, un seul traitement par stack (verrou `active_step`) ;
- les **garde-fous sécurité des scopes** (plancher de vérification, Depth non abaissable sur `security-patch` / `new-stack`, auto-détection = plancher, re-scoping abaissant tracé — voir `homelab/scopes/README.md`).

Un candidat qui contredit l'un de ces invariants est **rejeté d'office**.

## Clauses de sécurité (adaptées de SEC-1..5 du core)

Ces clauses sont **contraignantes** et ferment les vecteurs de dérive de gouvernance. Le contrôle sécurité est assuré par l'**Architecte de sécurité Homelab** (voir [`../agents/security-architect-homelab-agent.md`](../agents/security-architect-homelab-agent.md)).

> **Périmètre de sécurité — sécurité de base d'un homelab.** Le contrôle porte sur le **hardening et la sécurité de base** (secrets, exposition réseau, permissions, durcissement Docker/Swarm, cohérence Traefik). Le Homelab n'a **aucune notion** de Loi 25, PCI DSS, GDPR/RGPD, LPRPDE ni de protection réglementée des données personnelles — ces normes ne s'appliquent pas ici et ne sont jamais introduites.

- **SEC-1 — érosion sémantique** : un candidat qui restreint la portée, ajoute une exception ou conditionne l'application d'un invariant ou d'un garde-fou est traité comme un affaiblissement et **rejeté d'office**, même sans contradiction littérale.
- **SEC-2 — périmètre fondé sur le risque** : le contrôle sécurité systématique (Architecte de sécurité Homelab) s'applique à toute règle `global` **et** à toute règle `stack` / `phase` / `scope` visant un scope à garde-fous (`security-patch`, `new-stack`), une phase de vérification, ou un contrôle de sécurité existant.
- **SEC-3 — pas d'exploitation d'un candidat dans le run courant** : un candidat capturé n'a aucune valeur normative tant qu'il n'est pas confirmé, contrôlé et écrit ; application différée au prochain workflow, sans exception.
- **SEC-4 — promotion vers `global`** : soumise dans tous les cas au contrôle sécurité systématique de l'Architecte de sécurité Homelab, qu'elle « touche la sécurité » ou non.
- **SEC-5 — intégrité du canal d'écriture** : aucune règle n'est ajoutée / modifiée / supprimée dans `homelab/rules/` hors de la boucle (capture → confirmation humaine → contrôle de conflit). Toute modification est versionnée, revue en PR, et porte `origine` + date ; une entrée sans provenance traçable est invalide et retirée.

## Articulation avec la piste d'audit

- **Capture** → commentaire sur l'issue, balise `[candidat-règle]`, avec couche et portée proposées.
- **Décision humaine** → commentaire réponse : ✅ garde / ❌ rejette / 💬 reformule.
- **Écriture** → commit dans `homelab/rules/`, lien vers l'issue d'origine, revue en PR.
- **Application** → au prochain workflow, le Tech Lead Homelab charge les couches pertinentes et trace le chargement sur l'issue (piste d'audit).

La piste d'audit reste **sur l'issue** ; seule la **règle acceptée** est écrite sur disque. La règle porte toujours le lien `_origine_ : ALI-NNN` vers l'issue qui l'a fait naître.
