# Verification gates & Sensors Homelab — fiabilisation déterministe

Ce répertoire contient les **manifestes déclaratifs** des mécanismes de fiabilisation déterministe du workflow Homelab, référencés par le triptyque [`homelab/common/`](../common/conductor.md) (source unique — voir [`protocols/governance-security.md`](../common/protocols/governance-security.md), clauses SG-1..6) et coordonnés par le **Tech Lead Homelab**. Vue narrative historique (stub de redirection) : [`docs/homelab-workflow.md`](../../docs/homelab-workflow.md).

Pendant Homelab de [`../../core/sensors/`](../../core/sensors/README.md) : même forme déclarative, mêmes clauses de sécurité (SG-1 à SG-6), **gates, sensors et périmètres spécifiques au Homelab** (Docker Swarm / Proxmox / Terraform / Traefik / Vault). Décision tracée dans [ADR-0016](../../decisions/0016-verification-gates-et-sensors-homelab.md).

Deux mécanismes complémentaires, **tous deux advisory** :

- **Verification gates** — contrôle automatique de **traçabilité** aux **frontières de phases**, en amont du gate humain ([`gates.md`](gates.md)).
- **Sensors** — checks **déterministes** déclenchés soit **à l'écriture d'un artefact** (`fire_on: write`), soit **au gate de phase** (`fire_on: gate`) ([`sensors/`](sensors/)).

## Nature déclarative (non exécutable à ce stade)

Ces fichiers **décrivent le contrat** (périmètre de déclenchement, règles de contrôle, sortie attendue) de façon lisible et déterministe. Ce **ne sont pas des scripts exécutables** : ils fixent le fond pour qu'un outillage (script / CI) puisse être ajouté ultérieurement **sans redécider** la sémantique. Pas de harness TypeScript (`bun` / `aidlc-*.ts`), cohérent avec le cadrage ([ADR-0013](../../decisions/0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)) : on garde la **forme déclarative** sans importer le moteur. Le passage à l'exécutable est une évolution future, hors périmètre du stage d'introduction.

## Garde-fou : advisory par défaut, bloquant conditionnel (sécurité)

- La grande majorité des gates et sensors **ne bloquent jamais** : ils laissent une trace d'audit factuelle sans arrêter le flux.
- **Exception sécurité confirmée (ALI-204, arbitrage 2)** : `plaintext-secret` et `terraform-no-sni` sont **bloquants sur les scopes `security-patch` / `new-stack`** (`severity_overrides`) — une détection **arrête l'avancée du workflow** jusqu'à correction ou levée humaine explicite tracée. Partout ailleurs, ils restent advisory.
- Même bloquant, un sensor **ne remplace jamais** la **validation humaine granulaire** (unique gate décisionnel de fond), ni le **QA Docker systématique** (§2.2), ni le contrôle qualité central du Tech Lead (§2.6) : bloquer, c'est forcer la correction ou une levée humaine tracée, pas décider à la place de l'humain.
- Un signal **au vert ne vaut pas validation** ; un signal **en échec n'autorise aucun raccourci**.
- Toute évolution de la sévérité d'un sensor (bascule bloquant/advisory, périmètre de scopes) est une décision structurante explicite (ADR + contrôle sécurité QA Docker, SG-1).

## Clauses de sécurité (contrôle QA Docker — SG-1 à SG-6)

Adaptées du core (`core/sensors/README.md`), ces clauses sont **contraignantes** et alignent `homelab/sensors/` sur le niveau d'exigence de `homelab/rules/`. Le contrôle sécurité du mécanisme est assuré par le **QA Docker** (compétence hardening / sécurité compose / Traefik ; pas d'Architecte cybersécurité dédié dans l'équipe Homelab — même choix que l'[ADR-0015](../../decisions/0015-learning-loop-et-regles-persistantes-homelab.md)) :

- **SG-1 — Intégrité du canal des manifestes** (analogue SEC-5) : aucun manifeste (gate ou sensor) n'est ajouté / modifié / supprimé **hors PR revue** ; toute modification est versionnée et porte `origine` (issue) + date ; un manifeste sans provenance traçable est **invalide**. **Affaiblir un check** (retrait d'une règle, ajout d'une exception, réduction du périmètre de déclenchement) est une modification de la surface de gouvernance **soumise au contrôle sécurité**.
- **SG-2 — Indisponible ≠ conforme** : un sensor / gate non exécuté, en erreur, ou hors périmètre produit le verdict explicite `⛔ indisponible`, tracé comme un **écart**, jamais comme un vert. L'absence d'un signal attendu est elle-même un écart.
- **SG-3 — Plancher sécurité** : un gate / sensor ne peut **jamais porter, remplacer, conditionner ni court-circuiter** le QA Docker systématique, le contrôle sécurité, la validation humaine granulaire, ni le plancher sécurité des scopes (`homelab/scopes/README.md`). Le contrôle sécurité reste hors du périmètre automatisable.
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
> **Sévérité — advisory par défaut, bloquant conditionnel** (confirmé ALI-204, arbitrage 2) : `plaintext-secret` et `terraform-no-sni` sont **bloquants sur les scopes `security-patch` / `new-stack`** (front-matter `severity_overrides`), advisory partout ailleurs. Sur ces scopes, une détection **arrête l'avancée** jusqu'à correction ou levée humaine explicite tracée. Contrôle sécurité assuré par le QA Docker (ADR-0016, SG-1). Tous les autres sensors restent advisory.

## Format d'un manifeste de sensor (contrat amont)

Le front-matter est un **descripteur de capacité pur** (ce qu'est le check et comment il s'invoque) ; il ne cite jamais de stage. La liaison stage ↔ sensor vit côté stage (`sensors:`), c'est le **pull-authoring**.

```yaml
id: <identifiant>            # kebab-case, = stem du fichier (obligatoire)
kind: deterministic          # seule valeur acceptée aujourd'hui (obligatoire)
command: <préfixe d'invocation>   # (obligatoire) — non-exécutable à ce stade
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

Le corps (après le front-matter) porte le **contrat de vérification** (`checks`), la forme de la **sortie** advisory et les **garde-fous** — lisible, déterministe, non exécutable.
