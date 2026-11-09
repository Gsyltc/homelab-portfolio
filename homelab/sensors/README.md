# Verification gates & Sensors Homelab — fiabilisation déterministe

Ce répertoire contient les **manifestes déclaratifs** des mécanismes de fiabilisation déterministe du workflow Homelab, référencés par le triptyque [`homelab/common/`](../common/conductor.md) (source unique — voir [`protocols/governance-security.md`](../common/protocols/governance-security.md), clauses SG-1..6) et coordonnés par le **Tech Lead Homelab**. Vue narrative historique (stub de redirection) : [`docs/homelab-workflow.md`](../../docs/homelab-workflow.md).

Deux mécanismes complémentaires, **tous deux advisory** :

- **Verification gates** — contrôle automatique de **traçabilité** aux **frontières de phases**, en amont du gate humain ([`gates.md`](gates.md)).
- **Sensors** — checks **déterministes** déclenchés soit **à l'écriture d'un artefact** (`fire_on: write`), soit **au gate de phase** (`fire_on: gate`) ([`sensors/`](sensors/)).

## Nature : manifeste déclaratif + exécutable Python

Chaque manifeste fixe le **contrat** (périmètre de déclenchement, règles, sortie). Un **dispatcher Python** l'exécute de façon déterministe, sur le modèle du workflow `core` ([ADR-0051](../../decisions/0051-sensors-homelab-executables-python-et-hooks.md), analogue de [ADR-0046](../../decisions/0046-sensors-executables-python-et-hooks-agnostiques.md) côté `core`). On garde la **forme déclarative** (le fond ne se redécide pas) **et** on l'exécute.

> **Convention d'invocation.** Le harnais (`sensor.py`, manifestes, hook) vit dans ce dépôt — le **checkout `homelab-portfolio`** — **jamais** dans le dépôt du projet vérifié. Les commandes ci-dessous se lancent **depuis ce checkout**, en désignant le script par un **chemin ancré** sur sa racine (`$CORE_HOME` = racine du checkout), tandis que `--root <projet>` pointe le dépôt du projet à vérifier. Un chemin **relatif** (`homelab/scripts/sensor.py`) ne se résout que si le répertoire courant est déjà ce checkout ; lancé depuis le dossier du projet, il échoue en « script introuvable ».

| Commande | Rôle |
| --- | --- |
| `python3 "$CORE_HOME/homelab/scripts/sensor.py" list` | Sensors, script associé, sévérité (et `override` par scope), état (`⛔` si script absent/invalide) |
| `python3 "$CORE_HOME/homelab/scripts/sensor.py" --root <projet> fire <id> [--path <fichier>...] [--scope <scope>]` | Exécute un sensor. Sans `--path` : balayage de gate sur le périmètre `matches`. `--scope` résout la sévérité conditionnelle |
| `python3 "$CORE_HOME/homelab/scripts/sensor.py" --root <projet> gate <frontière> [--scope <scope>] [--attest a,b]` | Rapport de vérification d'une frontière de [`gates.md`](gates.md) (gère `blocking_on_scope` / `conditional_on_scope` / `prerequis_40`) |
| `python3 "$CORE_HOME/homelab/scripts/sensors/<id avec _>.py" --root <projet> [--path <fichier>...]` | Exécute un sensor seul (ex. `yaml_validity.py`) : un script par sensor |
| `python3 "$CORE_HOME/homelab/sensors/hooks/post_write.py"` | Hook d'écriture : lit le JSON du harnais sur stdin, lance les sensors `fire_on: write` |

Python 3.9+, bibliothèque standard uniquement (aucune dépendance ; le parsing YAML des composes est assuré par un mini-analyseur **statique** interne, pas PyYAML). Tests : `python3 -m unittest discover -s homelab/scripts/tests`.

Le code retour est **0** même en écart (advisory). `--strict` renvoie 1 en cas d'écart ou de `⛔` : usage CI uniquement. `--format json` donne une sortie exploitable par un script.

### Sévérité conditionnelle par scope (ALI-204)

`plaintext-secret` et `terraform-no-sni` portent un bloc `severity_overrides` : **bloquants sur les scopes `security-patch` / `new-stack`**, advisory ailleurs. Le dispatcher résout la sévérité effective via `--scope <scope>` (ou la variable `SENSORS_SCOPE`) ; sur ces scopes, un écart est signalé **BLOQUANT** (à corriger ou lever explicitement et à tracer), conformément à la décision humaine + contrôle sécurité de l'Analyste QA (SG-1). La sévérité ne passe **jamais** par le code retour du dispatcher (toujours 0) : elle est portée par le rapport et le workflow.

### Hooks

Le hook lance, à chaque écriture de fichier, les sensors `fire_on: write` dont `matches` correspond. Il sort **toujours en 0**. `--sensors a,b` le restreint aux sensors déclarés par le stage actif ; `--scope <scope>` résout la sévérité conditionnelle.

Kiro CLI (agent, `hooks.postToolUse`) — chemin **ancré** sur le checkout (`$CORE_HOME`), afin que le hook se déclenche même quand le répertoire courant est le dépôt du projet vérifié :

```json
{ "matcher": "fs_write", "command": "python3 \"${CORE_HOME:-.}/homelab/sensors/hooks/post_write.py\"" }
```

> Le repli `${CORE_HOME:-.}` conserve le comportement historique (chemin relatif au cwd) quand `$CORE_HOME` n'est pas défini et que l'agent tourne déjà depuis le checkout.

Le hook est **branché par défaut** sur les **agents producteurs de livrables** homelab (champ `hooks.postToolUse`, matcher `fs_write`) comme **filet déterministe** : **Spécialiste Docker** (compose) et **Spécialiste Terraform** (`.tf`/`.tfvars`). Il déclenche les sensors `fire_on: write` à chaque écriture, sans dépendre de la discipline manuelle. Il **ne remplace pas** le lancement explicite des sensors au temps 4 du [`stage-protocol`](../common/protocols/stage-protocol.md) ni le compte rendu `## Sensors` — il reste **advisory** (code 0, jamais bloquant).

## Garde-fou : advisory par défaut, bloquant conditionnel (sécurité)

- La grande majorité des gates et sensors **ne bloquent jamais** : ils laissent une trace d'audit factuelle sans arrêter le flux.
- **Exception sécurité confirmée (ALI-204, arbitrage 2)** : `plaintext-secret` et `terraform-no-sni` sont **bloquants sur les scopes `security-patch` / `new-stack`** (`severity_overrides`) — une détection **arrête l'avancée du workflow** jusqu'à correction ou levée humaine explicite tracée. Partout ailleurs, ils restent advisory.
- Même bloquant, un sensor **ne remplace jamais** la **validation humaine granulaire** (unique gate décisionnel de fond), ni le **contrôle QA systématique** (§2.2), ni le contrôle qualité central du Tech Lead (§2.6) : bloquer, c'est forcer la correction ou une levée humaine tracée, pas décider à la place de l'humain.
- Un signal **au vert ne vaut pas validation** ; un signal **en échec n'autorise aucun raccourci**.
- Toute évolution de la sévérité d'un sensor (bascule bloquant/advisory, périmètre de scopes) est une décision structurante explicite (ADR + contrôle sécurité Analyste QA, SG-1).

## Clauses de sécurité (contrôle Analyste QA — SG-1 à SG-6)

Ces clauses sont **contraignantes** et alignent `homelab/sensors/` sur le niveau d'exigence de `homelab/rules/`. Le contrôle sécurité du mécanisme est assuré par l'**Analyste QA** (compétence hardening / sécurité compose / Traefik ; pas d'Architecte cybersécurité dédié dans l'équipe Homelab) :

- **SG-1 — Intégrité du canal des manifestes** (analogue SEC-5) : aucun manifeste (gate ou sensor) n'est ajouté / modifié / supprimé **hors PR revue** ; toute modification est versionnée et porte `origine` (issue) + date ; un manifeste sans provenance traçable est **invalide**. **Affaiblir un check** (retrait d'une règle, ajout d'une exception, réduction du périmètre de déclenchement) est une modification de la surface de gouvernance **soumise au contrôle sécurité**.
- **SG-2 — Indisponible ≠ conforme** : un sensor / gate non exécuté, en erreur, ou hors périmètre produit le verdict explicite `⛔ indisponible`, tracé comme un **écart**, jamais comme un vert. L'absence d'un signal attendu est elle-même un écart.
- **SG-3 — Plancher sécurité** : un gate / sensor ne peut **jamais porter, remplacer, conditionner ni court-circuiter** le contrôle QA systématique, le contrôle sécurité, la validation humaine granulaire, ni le plancher sécurité des scopes (`homelab/scopes/README.md`). Le contrôle sécurité reste hors du périmètre automatisable.
- **SG-4 — Pré-requis de l'exécution différée** (avant tout passage en CI) : parsing statique uniquement (pas de rendu, pas de réseau, pas d'exécution de code / directive embarquée) ; contenu d'artefact = donnée non fiable ; environnement sans secret ni privilège ; `matches` glob bornés au repo ; échec → `⛔ indisponible`, jamais `✅`. Pour `vault-secret-exists` : **lecture de présence uniquement**, jamais la valeur.
- **SG-5 — Signal = donnée factuelle à source tracée** : un rapport / signal porte sa **source** (manifeste + version / commit) ; provenance non traçable → traité comme `⛔ indisponible`. Le jugement reste humain.
- **SG-6 — Anti-érosion sémantique** (analogue SEC-1) : un manifeste modifié pour restreindre le périmètre, ajouter une exception ou conditionner un check est un affaiblissement soumis au contrôle sécurité, même sans contradiction littérale.

## Interdiction absolue : aucun secret exposé

Aucun sensor ne lit, ne recopie, n'affiche ni ne transmet la **valeur** d'un secret :

- `plaintext-secret` signale l'**emplacement** et le **type de motif** (fichier + ligne + clé), **jamais** la valeur détectée.
- `vault-secret-exists` vérifie l'**existence** (chemin résolu ou non) via `homelab-vault-access` en **lecture de présence uniquement** — jamais la valeur, jamais dans un commentaire / livrable / notification (garde-fou « secrets » du chargement optimisé pour le contexte).

## Intégration à la piste d'audit

Les résultats vivent **sur l'issue** (piste d'audit existante), jamais dans un fichier `audit.md` :

- **Rapport de gate** posté à chaque frontière de phase, avant la validation humaine.
- **Signal de sensor** consigné à l'écriture d'un artefact (compose, `.tfvars`).
- Faits vérifiables uniquement (jamais un jugement) ; le jugement reste humain.
- Un écart advisory **récurrent** peut alimenter un **candidat-règle** de la boucle d'apprentissage ([`homelab/rules/`](../rules/README.md)) via le déclencheur `SENSOR_PROPOSED`, sans court-circuiter la validation.

## Sensors définis

Six sensors, alignés sur le contrat amont « Sensors » (schéma de manifeste `id` / `kind` / `command` / `default_severity` / `description` + `category` / `fire_on` / `matches` / `origine`). Les `id` seront importés **par id nu** dans le champ `sensors:` des fiches de stage (pull-authoring, Stage 7).

| Sensor | Manifeste | `category` | `fire_on` | `default_severity` | Objet |
| --- | --- | --- | --- | --- | --- |
| `yaml-validity` | [`sensors/yaml-validity.md`](sensors/yaml-validity.md) | compose-shape | write | advisory | Validité YAML du docker-compose livré |
| `swarm-deploy-section` | [`sensors/swarm-deploy-section.md`](sensors/swarm-deploy-section.md) | compose-shape | gate | advisory | Présence d'une section `deploy` compatible Swarm |
| `plaintext-secret` | [`sensors/plaintext-secret.md`](sensors/plaintext-secret.md) | security | write | advisory | Détection de secret en clair (emplacement, jamais la valeur) |
| `terraform-no-sni` | [`sensors/terraform-no-sni.md`](sensors/terraform-no-sni.md) | security | write | advisory | Absence de `${SNI}` dans les fichiers Terraform livrés |
| `traefik-coherence` | [`sensors/traefik-coherence.md`](sensors/traefik-coherence.md) | traefik | gate | advisory | Cohérence Traefik (référence `traefik-manager-read`) |
| `vault-secret-exists` | [`sensors/vault-secret-exists.md`](sensors/vault-secret-exists.md) | security | gate | advisory | Existence des secrets Vault référencés (jamais la valeur) — **actif** |

> **Sensors prioritaires** (confirmés ALI-204, arbitrage 1) : `yaml-validity`, `swarm-deploy-section`, `plaintext-secret`, `terraform-no-sni`. **Complémentaire** : `traefik-coherence`. `vault-secret-exists` est **actif** (arbitrage 4), en existence seule.
>
> **Sévérité — advisory par défaut, bloquant conditionnel** (confirmé ALI-204, arbitrage 2) : `plaintext-secret` et `terraform-no-sni` sont **bloquants sur les scopes `security-patch` / `new-stack`** (front-matter `severity_overrides`), advisory partout ailleurs. Sur ces scopes, une détection **arrête l'avancée** jusqu'à correction ou levée humaine explicite tracée. Contrôle sécurité assuré par l'Analyste QA (SG-1). Tous les autres sensors restent advisory.

## Format d'un manifeste de sensor (contrat amont)

Le front-matter est un **descripteur de capacité pur** (ce qu'est le check et comment il s'invoque) ; il ne cite jamais de stage. La liaison stage ↔ sensor vit côté stage (`sensors:`), c'est le **pull-authoring**.

```yaml
id: <identifiant>            # kebab-case, = stem du fichier (obligatoire)
kind: deterministic          # seule valeur acceptée aujourd'hui (obligatoire)
command: <commande d'invocation>  # (obligatoire) — python3 homelab/scripts/sensor.py fire <id>
default_severity: advisory   # advisory | blocking (obligatoire) — blocking global = ADR + contrôle sécurité
severity_overrides:          # (optionnel) sévérité conditionnelle par scope (ADR + contrôle sécurité)
  - scopes: [security-patch, new-stack]
    severity: blocking
description: <une ligne>     # description humaine (obligatoire)
category: <label libre>      # (optionnel) — compose-shape | security | traefik
fire_on: gate                # (optionnel) write | gate — défaut : write
matches: <glob>              # (optionnel) filtre de chemin ; au gate, glob absent ⇒ tout livrable
origine: ALI-<n>             # (SG-1) provenance traçable — obligatoire côté gouvernance
```

Le corps (après le front-matter) porte le **contrat de vérification** (`checks`), la forme de la **sortie** advisory et les **garde-fous** — lisible et déterministe ; son exécution est assurée par `homelab/scripts/sensor.py`.
