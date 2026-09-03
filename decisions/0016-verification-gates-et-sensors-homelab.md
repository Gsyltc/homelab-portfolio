# Verification gates et Sensors déterministes advisory — Homelab

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : multica.gaston (validation humaine — ALI-204, 2026-09-03)
accepté le : 2026-09-03
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Validé par l'humain (multica.gaston) sur l'issue ALI-204, avec les quatre arbitrages tranchés : (1) sensors prioritaires confirmés, (2) `plaintext-secret` / `terraform-no-sni` **bloquants** sur `security-patch` / `new-stack`, (3) outillage = conventions + manifestes déclaratifs, (4) `vault-secret-exists` **activé** (existence seule).

## Contexte

Le workflow Homelab (`docs/homelab-workflow.md`) disposait de la **validation humaine granulaire**, du **QA Docker systématique** (§2.2) et du **contrôle qualité central** du Tech Lead (§2.6), mais **d'aucun contrôle automatique de traçabilité** aux frontières de phases ni de **check déterministe** à l'écriture d'un livrable. L'analyse comparative avec AI-DLC 2.0 (issue parente ALI-200) a identifié deux écarts — mécanisme **E** (Verification gates) et **F** (Sensors) — comblés au Stage 4 (ALI-204).

Le mécanisme équivalent pour `core-workflow.md` est documenté dans les ADR [0005](0005-verification-gates-et-sensors.md) (*Accepted*) et [0012](0012-alignement-sensors-sur-ai-dlc.md) (*Accepted*), avec des manifestes déclaratifs sous `core/sensors/` (un fichier par sensor + un manifeste de gates) et six clauses de sécurité SG-1 à SG-6.

Le Stage 4 de la refonte Homelab porte ce mécanisme au contexte Homelab : livrables **compose** (Docker Swarm) et **Terraform** (`.tfvars`), cohérence **Traefik**, secrets **Vault** — en cohérence avec la gouvernance A2A du workflow Homelab (validation humaine granulaire, QA Docker systématique, piste d'audit sur l'issue, garde-fous absolus), avec les scopes du Stage 2 ([ADR-0014](0014-scopes-homelab-et-axes-depth-verification.md)) et la boucle d'apprentissage du Stage 3 ([ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md)).

Les arbitrages (sensors prioritaires, advisory vs bloquant, outillage, sensor Vault) ont été **tranchés par l'humain** sur l'issue ALI-204 (validation du 2026-09-03) : sensors prioritaires confirmés, `plaintext-secret` / `terraform-no-sni` bloquants sur `security-patch` / `new-stack`, outillage = conventions + manifestes déclaratifs, `vault-secret-exists` activé en existence seule.

## Décision

**Introduire deux mécanismes de fiabilisation déterministe, tous deux advisory**, dans le respect des invariants de gouvernance A2A du Homelab.

### 1. Verification gates — traçabilité aux frontières de phases

À chaque **frontière de phase**, en amont du gate humain, un contrôle automatique de traçabilité en trois points : (1) présence des artefacts requis, (2) liaison paramètre / décision ↔ demande / paramètres §1.4 / ADR, (3) absence d'artefact orphelin. Frontières adossées aux **3 phases actuelles** du workflow Homelab (Cadrage / Production / Validation ; la matrice suivra l'ossature à 5 phases au Stage 5, [ADR-0013](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)). Manifeste : `homelab/sensors/gates.md`.

**Intégration des prérequis §3.0.** La frontière **Phase 2 → Phase 3** **anticipe** les prérequis de déploiement existants du §3.0 (`[répertoire de travail]` défini et non vide, flux Kestra `configure_service` accessible), pour éviter qu'un prérequis manquant ne fasse échouer silencieusement le dépôt (§3.3) ou ne bloque le §3.4. Le §3.0 reste par ailleurs le contrôle **bloquant** de référence du Tech Lead ; le gate n'est que son pendant advisory anticipé.

**En cas d'écart** : signalement dans un « Rapport de vérification » sur l'issue et proposition de revenir corriger, **sans blocage**.

### 2. Sensors — checks déterministes advisory adaptés au Homelab

**Six sensors** déclaratifs (`homelab/sensors/sensors/`), déclenchés à l'écriture (`fire_on: write`) ou au gate de phase (`fire_on: gate`) :

- `yaml-validity` *(prioritaire, write)* — validité **YAML** du docker-compose livré.
- `swarm-deploy-section` *(prioritaire, gate)* — présence d'une section **`deploy`** compatible **Docker Swarm** sur chaque service.
- `plaintext-secret` *(prioritaire, write, sécurité)* — détection de **secret en clair** (mot de passe / token / clé API) ; signale l'**emplacement**, jamais la valeur.
- `terraform-no-sni` *(prioritaire, write, sécurité)* — absence de **`${SNI}`** dans les fichiers Terraform livrés.
- `traefik-coherence` *(complémentaire, gate)* — cohérence **Traefik**, en **référençant le check `traefik-manager-read` existant** (autorité : QA Docker, §2.2).
- `vault-secret-exists` *(actif, gate, sécurité)* — **existence** des secrets **Vault** référencés, en **lecture de présence uniquement** (jamais la valeur). Activé par décision humaine (ALI-204, arbitrage 4).

### 3. Sévérité — advisory par défaut, bloquant conditionnel sur les scopes sécuritaires

Gates et sensors sont **advisory par défaut** : ils ne bloquent pas et laissent une trace d'audit factuelle. **Décision confirmée (ALI-204, arbitrage 2)** : `plaintext-secret` et `terraform-no-sni` sont **bloquants sur les scopes `security-patch` / `new-stack`** (front-matter `severity_overrides`) — une détection y **arrête l'avancée du workflow** jusqu'à correction ou levée humaine explicite tracée ; ils restent advisory sur tous les autres scopes. Tous les autres sensors restent advisory.

Même bloquant, un sensor **ne remplace pas** la validation humaine granulaire (unique gate décisionnel de fond), le QA Docker systématique (§2.2) ni le contrôle qualité central du Tech Lead (§2.6) : bloquer force la correction ou une levée humaine tracée, sans décider à la place de l'humain. Un signal au vert ne vaut pas validation ; un signal en échec n'autorise aucun raccourci. Toute évolution de sévérité (bascule, périmètre de scopes) reste une décision structurante (ADR + contrôle sécurité QA Docker, SG-1).

### 4. Articulation avec le contrôle qualité central (§2.6) et la piste d'audit

Les signaux vivent **sur l'issue** (pas de fichier `audit.md`) : « Rapport de vérification » à chaque frontière (avant la validation humaine) et signal de sensor à l'écriture d'un livrable. Faits vérifiables uniquement ; le jugement reste humain. Le contrôle qualité central (§2.6) reste un aiguillage GO / RENVOI : les sensors lui fournissent des faits, sans se substituer à l'analyse technique du QA Docker. Un écart advisory récurrent peut alimenter un **candidat-règle** de la boucle d'apprentissage (`SENSOR_PROPOSED`, [`homelab/rules/`](../homelab/rules/README.md)), sans court-circuiter la validation — c'est la liaison annoncée par l'ADR-0015 (IMP-004).

### 5. Aucun secret exposé

`plaintext-secret` signale l'emplacement + le type de motif (jamais la valeur) ; `vault-secret-exists` vérifie l'existence via `homelab-vault-access` en **lecture de présence uniquement**. Aucun sensor ne lit, ne recopie ni ne transmet une valeur de secret (garde-fou « secrets » du chargement optimisé pour le contexte).

### 6. Outillage — conventions + manifestes déclaratifs (harness TypeScript écarté)

Les checks sont des **conventions documentées** dans le workflow, **accompagnées de manifestes déclaratifs** versionnés dans `homelab/sensors/` (un fichier par sensor + un manifeste de gates + un README). Ces manifestes **ne sont pas exécutables** à ce stade : ils fixent le contrat pour un outillage (script / CI) ultérieur, sans redécider le fond. Pas de harness TypeScript (`bun` / `aidlc-*.ts`) — cohérent avec le cadrage ([ADR-0013](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)).

### 7. Contrôle sécurité — clauses SG-1 à SG-6, contrôleur = QA Docker

Six clauses **contraignantes** SG-1 à SG-6 (adaptées du core, ADR-0005) alignent `homelab/sensors/` sur le niveau d'exigence de `homelab/rules/` : intégrité du canal des manifestes (SG-1), indisponible ≠ conforme (SG-2), plancher sécurité non automatisable (SG-3), pré-requis de l'exécution différée (SG-4), signal = donnée factuelle à source tracée (SG-5), anti-érosion sémantique (SG-6). Le **contrôle sécurité du mécanisme est assuré par le QA Docker** (pas d'Architecte cybersécurité dédié dans l'équipe Homelab — même choix que l'ADR-0015).

## Conséquences

### Positives

- **POS-001** : Traçabilité contrôlée automatiquement aux frontières de phases ; l'humain valide le contenu, pas la plomberie.
- **POS-002** : Checks déterministes reproductibles (YAML, `deploy` Swarm, secret en clair, `${SNI}`, Traefik, existence Vault), à la place du seul jugement d'agent.
- **POS-003** : Le QA Docker et le Tech Lead sont soulagés des vérifications mécaniques ; ils se concentrent sur l'analyse technique et l'aiguillage.
- **POS-004** : Caractère advisory = aucun risque de blocage de la gouvernance ni de contournement du QA Docker, du contrôle sécurité ou de la validation humaine.
- **POS-005** : Matérialise l'axe de vérification de l'ADR-0014 et s'appuie sur la piste d'audit et la boucle d'apprentissage de l'ADR-0015 (cohérence de la refonte).
- **POS-006** : Structure en miroir de `core/sensors/` — cohérence structurelle inter-workflows, base outillable ultérieurement (CI) sans redécider la sémantique.
- **POS-007** : Les clauses SG-1 à SG-6 ferment les vecteurs de dérive (édition silencieuse d'un manifeste, fausse assurance sur signal manquant, automatisation d'un contrôle de sécurité, exfiltration de secret) ; `homelab/sensors/` atteint le niveau d'exigence de `homelab/rules/`.
- **POS-008** : Aucun secret exposé — `plaintext-secret` et `vault-secret-exists` opèrent sans jamais lire ni transmettre de valeur.

### Négatives

- **NEG-001** : `homelab/sensors/` est un nouvel artefact à maintenir cohérent avec le workflow, les scopes et les gabarits de livrables.
- **NEG-002** : Tant que non outillés, les checks reposent sur l'application disciplinée du Tech Lead et du QA Docker (advisory, non automatisé).
- **NEG-003** : Un signal advisory peut être perçu comme du bruit s'il n'est pas relié à une action ; d'où la trace factuelle et le lien avec la boucle d'apprentissage (`SENSOR_PROPOSED`).
- **NEG-004** : Le sensor `vault-secret-exists`, même en lecture de présence, ajoute une dépendance à `homelab-vault-access` ; **activé** (ALI-204, arbitrage 4), il opère strictement en existence seule, jamais la valeur.

## Alternatives étudiées

### ALT-001 — Sensors de sécurité bloquants par défaut

Rendre `plaintext-secret` et `terraform-no-sni` contraignants (bloquer l'avancée sur détection).

**Raison du rejet (par défaut) / décision retenue** : un check déterministe bloquant partout peut arrêter le workflow sur un faux positif (motif de secret dans un commentaire d'exemple, `${SNI}` cité hors Terraform livré) et empiéter sur la décision humaine. Retenu : advisory par défaut, **bloquant uniquement sur les scopes sécuritaires `security-patch` / `new-stack`** — décision confirmée par l'humain (ALI-204, arbitrage 2 « Oui ») et matérialisée par `severity_overrides` + contrôle sécurité QA Docker (SG-1). Le blocage force la correction ou une levée humaine tracée, sans décider à la place de l'humain.

### ALT-002 — Scripts exécutables (CI) dès l'introduction

Produire directement des scripts / hooks CI exécutables (linter YAML, scan de secrets).

**Raison du rejet** : figer une implémentation avant d'avoir stabilisé la sémantique (périmètres, frontières) et l'ossature de phases (Stage 5 à venir) créerait de la reprise. Retenu : conventions + manifestes déclaratifs, outillage ultérieur sans redécision du fond — cohérent avec l'ADR-0005 (core) et le cadrage ADR-0013.

### ALT-003 — Sensor Vault lisant la valeur pour vérifier la conformité

Autoriser `vault-secret-exists` à lire la valeur du secret (p. ex. vérifier un format).

**Raison du rejet** : contredit frontalement le garde-fou absolu « aucun secret lu / affiché / transmis ». Retenu : **existence seule** (lecture de présence), jamais la valeur. Le sensor est **activé** par décision humaine explicite tracée (ALI-204, arbitrage 4 « oui ») ; l'invariant « existence seule » reste non négociable.

### ALT-004 — Réimplémenter l'analyse Traefik dans le sensor

Faire de `traefik-coherence` un analyseur Traefik autonome.

**Raison du rejet** : duplication de l'autorité technique du QA Docker et du check `traefik-manager-read` existant, avec risque de divergence. Retenu : le sensor **référence** `traefik-manager-read` et se limite à consigner le verdict factuel + un contrôle de surface.

## Notes d'implémentation

- **IMP-001** : Mécanisme documenté dans la section « Verification gates & Sensors » de [`docs/homelab-workflow.md`](../docs/homelab-workflow.md), insérée entre « Règles & boucle d'apprentissage » et « Modèle de collaboration A2A » ; diagramme de vue d'ensemble et garde-fous mis à jour.
- **IMP-002** : Manifestes déclaratifs scaffoldés dans `homelab/sensors/` — [`README.md`](../homelab/sensors/README.md), [`gates.md`](../homelab/sensors/gates.md), `sensors/{yaml-validity,swarm-deploy-section,plaintext-secret,terraform-no-sni,traefik-coherence,vault-secret-exists}.md`.
- **IMP-003** : Frontières adossées aux 3 phases actuelles ; la matrice suivra l'ossature à 5 phases au Stage 5 (voir [ADR-0013](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)).
- **IMP-004** : Advisory par défaut ; **`plaintext-secret` et `terraform-no-sni` bloquants sur `security-patch` / `new-stack`** (confirmé ALI-204, arbitrage 2), matérialisé par `severity_overrides` dans les manifestes + garde-fou du scope (`homelab/scopes/README.md`) + contrôle sécurité QA Docker. Toute évolution ultérieure de sévérité = décision ADR + contrôle sécurité.
- **IMP-005** : Liaison `SENSOR_PROPOSED` → candidat-règle de la boucle d'apprentissage, annoncée par l'[ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md) (IMP-004) et articulée ici : un échec de sensor récurrent alimente un candidat-règle, sans court-circuiter la validation humaine (SEC-3 adapté).
- **IMP-006** : Contrôle sécurité (SG-1 à SG-6) assuré par le QA Docker ; provenance `origine: ALI-204` portée par chaque manifeste (SG-1 / SG-5).

## Références

- **REF-001** : Issue ALI-204 (Stage 4 — Verification gates + Sensors Homelab) ; issue parente ALI-200.
- **REF-002** : [ADR-0005 - Verification gates et Sensors déterministes advisory](0005-verification-gates-et-sensors.md)
- **REF-003** : [ADR-0012 - Alignement des sensors sur AI-DLC](0012-alignement-sensors-sur-ai-dlc.md)
- **REF-004** : [ADR-0013 - Cadrage de la refonte Homelab](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)
- **REF-005** : [ADR-0014 - Scopes Homelab et axes Depth/Vérification](0014-scopes-homelab-et-axes-depth-verification.md)
- **REF-006** : [ADR-0015 - Boucle d'apprentissage et règles persistantes Homelab](0015-learning-loop-et-regles-persistantes-homelab.md)
- **REF-007** : [AI-DLC workflows (awslabs) — core/sensors](https://github.com/awslabs/aidlc-workflows/tree/main/core)
