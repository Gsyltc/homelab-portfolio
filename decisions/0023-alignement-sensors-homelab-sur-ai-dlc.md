# Alignement des sensors Homelab sur le schéma de manifeste AI-DLC « Sensors »

---
auteurs: Mika (agent, en attente de validation humaine granulaire — multica.gaston)
accepté par : ""
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** — en attente de validation humaine explicite (multica.gaston) sur l'issue ALI-213. Le passage à *Accepted* suppose la validation humaine granulaire (invariant : aucun ADR accepté sans validation humaine). Aucun sensor n'est ajouté, modifié ni supprimé dans `homelab/sensors/` par cet ADR : il **vérifie et trace** la conformité des six manifestes déjà scaffoldés en [ADR-0016](0016-verification-gates-et-sensors-homelab.md) au contrat amont « Sensors » du *Harness Engineer Guide*. La vérification n'a trouvé **aucune non-conformité** ; aucune correction n'est nécessaire. Aucune posture de sécurité ni garde-fou de gouvernance n'est modifié (les bascules `blocking` de `plaintext-secret` / `terraform-no-sni` et l'activation de `vault-secret-exists` restent celles actées par l'ADR-0016 sur validation ALI-204).

## Contexte

Les mécanismes de fiabilisation déterministe du Homelab vivent sous [`homelab/sensors/`](../homelab/sensors/README.md), introduits par l'[ADR-0016](0016-verification-gates-et-sensors-homelab.md) (*Accepted*, issue ALI-204) : un manifeste de **verification gates** ([`gates.md`](../homelab/sensors/gates.md)) et **six manifestes de sensors** (un fichier par sensor sous [`sensors/`](../homelab/sensors/sensors/)), avec les six clauses de sécurité **SG-1 à SG-6** transposées du core.

Le Stage 5 de l'alignement AI-DLC du harness Homelab (issue ALI-213, parente ALI-208) porte ces sensors sur le contrat **« Sensors »** du *Harness Engineer Guide* (`awslabs/aidlc-workflows`). C'est le **miroir Homelab** de l'[ADR-0012](0012-alignement-sensors-sur-ai-dlc.md) (*Accepted*, issue ALI-198), qui a fait ce travail pour `core/sensors/`.

Le contrat amont fixe, pour un manifeste de sensor :

- **Un fichier Markdown à front-matter YAML** sous `core/sensors/`, **descripteur de capacité pur** : ce qu'est le check et comment il s'invoque, **jamais** quel stage l'utilise.
- **Cinq champs requis** : `id` (kebab-case, = stem du fichier), `kind` (`deterministic`, seule valeur acceptée aujourd'hui), `command` (préfixe d'invocation canonique), `default_severity` (`advisory` | `blocking`), `description` (une ligne).
- **Champs optionnels** : `category` (label libre), `fire_on` (`write` | `gate`, défaut `write`), `matches` (filtre de chemin ; requis en pratique pour `fire_on: write` — une entrée sans `matches` ne se déclenche jamais ; au gate, `matches` absent ⇒ tout livrable déclaré ; `matches: ""` rejeté au parse).
- **Sévérité** : `advisory` enregistre et laisse passer le gate ; `blocking` n'est **appliqué qu'au dispatch `gate`** (un sensor `write` peut déclarer `blocking` mais reste advisory dans cette version).
- **Liaison par pull-authoring** : le manifeste ne porte **aucun** champ de ciblage de stage (`applies_to:` supprimé) ; c'est la fiche de stage qui nomme le sensor par **id nu** dans son front-matter `sensors:`.

Contrainte de cadrage (ALI-208, miroir d'ALI-193/ALI-198) : adopter la **forme déclarative et les contrats** d'AI-DLC sans importer le tooling amont non applicable (`bun`, hooks `.ts`, `PostToolUse`, résolveur `loadSensors`, préfixe de fichier `aidlc-`, `dist/<harness>/`) ; **préserver** les invariants de gouvernance A2A (validation humaine granulaire, QA Docker systématique, piste d'audit sur l'issue, aucun secret exposé) ; toute divergence assumée est **tracée en décision structurante**.

Cet ADR répond aux inputs et critères d'acceptation de l'issue ALI-213 : (1) chaque sensor porte un manifeste conforme (`id`/`kind`/`command`/`default_severity`/`fire_on`/`matches`) ; (2) couverture minimale confirmée ; (3) sévérité par défaut et caractère advisory précisés ; (4) `fire_on`/`matches` vérifiés ; (5) divergences tracées.

## Décision

La structure établie par l'[ADR-0016](0016-verification-gates-et-sensors-homelab.md) est **vérifiée conforme** au contrat amont « Sensors » (moyennant les divergences assumées ci-dessous) et **conservée sans modification**. La vérification déterministe n'a trouvé **aucune non-conformité** : les six manifestes portent les cinq champs requis, `id` = stem du fichier, `kind: deterministic`, une sévérité valide, un `fire_on` valide et un `matches` présent (requis pour les sensors `write`) et non vide. Aucune correction de manifeste n'est nécessaire.

### 1. Les six sensors et leur conformité

Six sensors couvrent les checks demandés par l'issue (validité YAML compose, section `deploy` Swarm, secret en clair, absence de `${SNI}` Terraform, cohérence Traefik, existence des secrets Vault) :

| `id` | `kind` | `fire_on` | `default_severity` | `matches` | `category` |
| --- | --- | --- | --- | --- | --- |
| `yaml-validity` | deterministic | write | advisory | `{**/*.yml,**/*.yaml}` | compose-shape |
| `swarm-deploy-section` | deterministic | gate | advisory | `{**/*.yml,**/*.yaml}` | compose-shape |
| `plaintext-secret` | deterministic | write | advisory (+`severity_overrides` blocking) | `{**/*.yml,**/*.yaml,**/*.tf,**/*.tfvars}` | security |
| `terraform-no-sni` | deterministic | write | advisory (+`severity_overrides` blocking) | `{**/*.tf,**/*.tfvars}` | security |
| `traefik-coherence` | deterministic | gate | advisory | `{**/*.yml,**/*.yaml}` | traefik |
| `vault-secret-exists` | deterministic | gate | advisory | `{**/*.yml,**/*.yaml,**/*.tf,**/*.tfvars}` | security |

Tous portent en outre `command` (préfixe d'invocation, non-exécutable à ce stade) et `origine: ALI-204` (provenance traçable, gouvernance maison SG-1).

**Vérification de résolution des liaisons (pull-authoring).** Chaque id importé par les fiches de stage (`sensors: [...]`) et par `gates.md` se résout vers un manifeste existant. Références vivantes vérifiées : `docker-compose-creation` → `[yaml-validity, plaintext-secret]` ; `docker-compose-qa` → `[swarm-deploy-section, plaintext-secret, traefik-coherence]` ; `terraform-configuration` → `[terraform-no-sni, plaintext-secret]` ; `autonomy-mode` → `[yaml-validity, swarm-deploy-section]` ; `central-quality-control` → `[traefik-coherence]` ; `file-deposit` → `[vault-secret-exists]`. Aucune référence orpheline, aucun manifeste non importé bloquant.

### 2. Sévérité — advisory par défaut, bloquant conditionnel confirmé (inchangé)

La grande majorité des sensors restent **advisory** (trace d'audit, ne bloquent jamais). L'exception sécurité — `plaintext-secret` et `terraform-no-sni` **bloquants sur les scopes `security-patch` / `new-stack`** via `severity_overrides` — reste celle **tranchée par l'humain** en ALI-204 (arbitrage 2 « Oui ») et actée par l'[ADR-0016](0016-verification-gates-et-sensors-homelab.md). Cet ADR **ne modifie aucune sévérité** : il confirme que la posture existante est cohérente avec le contrat amont (blocking appliqué au dispatch, ici au gate de phase). `vault-secret-exists` reste **actif en existence seule** (arbitrage 4), advisory.

### 3. `fire_on` / `matches` — vérifiés conformes (inchangé)

Les `fire_on` distinguent le feedback incrémental à l'écriture (`yaml-validity`, `plaintext-secret`, `terraform-no-sni`) du contrôle au gate de phase (`swarm-deploy-section`, `traefik-coherence`, `vault-secret-exists`). Les `matches` ciblent bien les types de fichiers demandés par l'issue — `*.yml`/`*.yaml` pour le compose, `*.tf`/`*.tfvars` pour Terraform — et sont **présents et non vides** sur les six manifestes (invariant amont : un sensor `write` sans `matches` ne se déclencherait jamais).

## Divergences assumées et tracées

Cohérentes avec le contrat amont, ce ne sont pas des erreurs :

- **DIV-emplacement** : manifestes sous `homelab/sensors/sensors/` (et manifeste de gates `homelab/sensors/gates.md`), et non `core/sensors/`. Cohérent avec les autres surfaces déclaratives Homelab (`homelab/rules/`, `homelab/scopes/`, `homelab/agents/`), déjà tranché par l'[ADR-0016](0016-verification-gates-et-sensors-homelab.md).
- **DIV-préfixe** : pas de préfixe de fichier `aidlc-` (le résolveur amont `loadSensors` exige `aidlc-<id>.md` ; aucun résolveur amont n'est importé ici — l'exécution passe par Multica). Le nommage reste `id` = stem du fichier, esprit amont préservé.
- **DIV-command** : `command` est un texte descriptif « non-exécutable (advisory documentaire) », pas un argv réel. À ce stade les manifestes **décrivent le contrat** sans moteur d'exécution (pas de `bun`/hooks `.ts`) ; le passage à l'exécutable (script / CI) est une évolution future qui pourra être ajoutée **sans redécider** la sémantique. Miroir de la divergence `DIV-command` déjà tracée pour le core ([ADR-0012](0012-alignement-sensors-sur-ai-dlc.md)).
- **DIV-severity-overrides** : champ optionnel maison `severity_overrides` (sévérité conditionnelle par scope) absent du schéma amont, où `blocking` est global. Il matérialise la décision humaine ALI-204 (bloquant ciblé sur `security-patch`/`new-stack`) tout en gardant l'advisory par défaut ailleurs — décision structurante déjà actée ([ADR-0016](0016-verification-gates-et-sensors-homelab.md), SG-1).
- **DIV-vault-sensor** : sensor `vault-secret-exists` propre au Homelab (contexte Vault), absent de la liste amont des six sensors qui ship. Activé en **existence seule, jamais la valeur** (invariant de sécurité non négociable, garde-fou « aucun secret exposé »).
- **DIV-audit** : les signaux vivent **sur l'issue** (piste d'audit A2A), pas dans les shards `audit/` ni les fichiers `<record>/.aidlc-sensors/` de l'amont. Verdicts explicites `✅` / `⚠️` / `⛔ indisponible` (SG-2 : indisponible ≠ conforme), avec source tracée (SG-5).

## Conséquences

- **Positives** : les six sensors Homelab respectent le schéma de manifeste amont (`id`/`kind`/`command`/`default_severity`/`fire_on`/`matches` + `category`), la liaison par pull-authoring est vérifiée sans orphelin, et l'invariant « aucune valeur de secret exposée » est confirmé sur les deux sensors sécurité. La forme déclarative permettra d'ajouter un outillage exécutable ultérieurement sans redécider la sémantique.
- **Coûts / risques** : divergence de nommage (`homelab/sensors/` vs `core/sensors/`, absence de préfixe `aidlc-`) au prix d'une conformité de nommage pure — assumée pour préserver la cohérence des surfaces Homelab et éviter de casser les pointeurs vivants. Les sensors restent **non exécutables** à ce stade (documentaires) ; leur exécution effective est une évolution future hors périmètre.
- **Garde-fous préservés** : validation humaine granulaire, QA Docker systématique, contrôle qualité central du Tech Lead, clauses SG-1..6, aucun secret exposé. Un sensor au vert **ne vaut pas** validation ; un sensor en échec **n'autorise aucun raccourci**.

## Vérification

Contrôle déterministe des six manifestes (`homelab/sensors/sensors/*.md`) et des références de liaison (fiches de stage `homelab/common/stages/**/*.md` + `homelab/sensors/gates.md`) : **0 erreur, 0 avertissement**. Champs requis présents, `id` = stem, `kind: deterministic`, sévérité et `fire_on` valides, `matches` présent et non vide sur les sensors `write`, `origine` présent, toutes les références de sensors résolues.

## Références

- Contrat amont : *Harness Engineer Guide* — [Sensors](https://awslabs.github.io/aidlc-workflows/harness-engineering/06-sensors/) et [Sensor System](https://awslabs.github.io/aidlc-workflows/reference/07-sensor-system/).
- [ADR-0012](0012-alignement-sensors-sur-ai-dlc.md) — alignement des sensors `core/` sur AI-DLC (miroir amont, *Accepted*).
- [ADR-0016](0016-verification-gates-et-sensors-homelab.md) — introduction des verification gates et sensors Homelab (*Accepted*, ALI-204).
- [ADR-0014](0014-scopes-homelab-et-axes-depth-verification.md) / [ADR-0021](0021-alignement-scopes-homelab-sur-ai-dlc.md) — scopes Homelab (source des `severity_overrides` de scope).
- Issue ALI-213 (Stage 5, parente ALI-208).
