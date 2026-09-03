# Verification gates & Sensors — fiabilisation déterministe

Ce répertoire contient les **manifestes déclaratifs** des mécanismes de fiabilisation déterministe décrits dans [`core/common/protocols/governance-security.md`](../common/protocols/governance-security.md) et référencés par [`core/common/conductor.md`](../common/conductor.md).

Deux mécanismes complémentaires, **tous deux advisory** :

- **Verification gates** — contrôle automatique de **traçabilité** aux **frontières de phases**, en amont du gate humain ([`gates.md`](gates.md)).
- **Sensors** — checks **déterministes** déclenchés soit **à l'écriture d'un artefact** (`fire_on: write`), soit **au gate de phase** (`fire_on: gate`) ([`sensors/`](sensors/)).

## Nature déclarative (non exécutable à ce stade)

Ces fichiers **décrivent le contrat** (périmètre de déclenchement, règles de contrôle, sortie attendue) de façon lisible et déterministe. Ce **ne sont pas des scripts exécutables** : ils fixent le fond pour qu'un outillage (script / CI) puisse être ajouté ultérieurement **sans redécider** la sémantique. Le passage à l'exécutable est une évolution future, hors périmètre du stage d'introduction.

## Garde-fou : advisory par décision

- Les gates et sensors **ne bloquent jamais** la validation humaine granulaire et **ne la remplacent pas** — elle reste l'unique gate décisionnel contraignant.
- Ils **ne remplacent pas** le contrôle sécurité systématique de l'Architecte cybersécurité (obligatoire aux mêmes points qu'aujourd'hui).
- Un signal **au vert ne vaut pas validation** ; un signal **en échec n'autorise aucun raccourci**.
- Rendre un sensor **bloquant** est une décision structurante explicite (ADR + contrôle sécurité). Par défaut, tout reste advisory.

## Clauses de sécurité (contrôle Architecte cybersécurité — SG-1 à SG-6)

Issues du contrôle sécurité du mécanisme (STRIDE / OWASP), ces clauses sont **contraignantes** et alignent `core/sensors/` sur le niveau d'exigence de `core/rules/` :

- **SG-1 — Intégrité du canal des manifestes** (analogue SEC-5) : aucun manifeste (gate ou sensor) n'est ajouté / modifié / supprimé **hors PR revue** ; toute modification est versionnée et porte `origine` (issue) + date ; un manifeste sans provenance traçable est **invalide**. **Affaiblir un check** (retrait d'une règle, ajout d'une exception, réduction du périmètre de déclenchement) est une modification de la surface de gouvernance **soumise au contrôle sécurité systématique**.
- **SG-2 — Indisponible ≠ conforme** : un sensor / gate non exécuté, en erreur, ou hors périmètre produit le verdict explicite `⛔ indisponible`, tracé comme un **écart**, jamais comme un vert. L'absence d'un signal attendu est elle-même un écart.
- **SG-3 — Plancher sécurité** : un gate / sensor ne peut **jamais porter, remplacer, conditionner ni court-circuiter** le contrôle sécurité systématique (OWASP / STRIDE) ni le plancher sécurité des scopes. Le contrôle sécurité reste hors du périmètre automatisable.
- **SG-4 — Pré-requis de l'exécution différée** (avant tout passage en CI) : parsing statique uniquement (pas de rendu, pas de réseau, pas d'exécution de code / directive embarquée) ; contenu d'artefact = donnée non fiable ; environnement sans secret ni privilège ; `triggers` glob bornés au repo ; échec → `⛔ indisponible`, jamais `✅`.
- **SG-5 — Signal = donnée factuelle à source tracée** : un rapport / signal porte sa **source** (manifeste + version / commit) ; provenance non traçable → traité comme `⛔ indisponible`. Le jugement reste humain.
- **SG-6 — Anti-érosion sémantique** (analogue SEC-1) : un manifeste modifié pour restreindre le périmètre, ajouter une exception ou conditionner un check est un affaiblissement soumis au contrôle sécurité, même sans contradiction littérale.

## Intégration à la piste d'audit

Les résultats vivent **sur l'issue** (piste d'audit existante), jamais dans un fichier `audit.md` :

- **Rapport de gate** posté à chaque frontière de phase, avant la validation humaine.
- **Signal de sensor** consigné à l'écriture d'un artefact.
- Faits vérifiables uniquement (jamais un jugement) ; le jugement reste humain.

## Sensors définis

Cinq sensors, alignés sur le contrat amont « Sensors » (schéma de manifeste `id` / `kind` / `command` / `default_severity` / `description` + `category` / `fire_on` / `matches`). Les `id` sont importés **par id nu** dans le champ `sensors:` des fiches de stage (pull-authoring).

| Sensor | Manifeste | `category` | `fire_on` | `default_severity` | Objet |
| --- | --- | --- | --- | --- | --- |
| `required-sections` | [`sensors/required-sections.md`](sensors/required-sections.md) | document-shape | gate | advisory | Rubriques obligatoires d'ADR / DAS présentes et non vides |
| `upstream-coverage` | [`sensors/upstream-coverage.md`](sensors/upstream-coverage.md) | document-shape | gate | advisory | Référence explicite à la demande amont (issue / ADR parent) |
| `diagram-validity` | [`sensors/diagram-validity.md`](sensors/diagram-validity.md) | document-shape | write | advisory | Syntaxe des diagrammes en code (Mermaid / PlantUML / Structurizr) |
| `claim-sources` | [`sensors/claim-sources.md`](sensors/claim-sources.md) | provenance | gate | advisory | Chaque affirmation retenue porte une source résoluble ; hypothèses = confirmation humaine explicite |
| `traceability` | [`sensors/traceability.md`](sensors/traceability.md) | traceability | gate | advisory | Chaîne exigence → ADR → livrable cohérente, sans orphelin dérivé |

> `linter` et `type-check` (sensors amont de qualité de code) restent **N/A** tant que le dépôt ne produit ni code ni IaC ; ils seront ajoutés le jour où un livrable exécutable apparaît (repli « stratégie de tests » de l'axe de vérification, [ADR-0003](../../decisions/0003-scopes-et-axes-depth-verification.md)).

## Format d'un manifeste de sensor (contrat amont)

Le front-matter est un **descripteur de capacité pur** (ce qu'est le check et comment il s'invoque) ; il ne cite jamais de stage. La liaison stage ↔ sensor vit côté stage (`sensors:`), c'est le **pull-authoring**.

```yaml
id: <identifiant>            # kebab-case, = stem du fichier (obligatoire)
kind: deterministic          # seule valeur acceptée aujourd'hui (obligatoire)
command: <préfixe d'invocation>   # (obligatoire) — voir divergence DIV-command ci-dessous
default_severity: advisory   # advisory | blocking (obligatoire) — blocking = ADR + contrôle sécurité
description: <une ligne>     # description humaine (obligatoire)
category: <label libre>      # (optionnel) — document-shape | provenance | traceability
fire_on: gate                # (optionnel) write | gate — défaut : write
matches: <glob>              # (optionnel) filtre de chemin ; au gate, glob absent ⇒ tout livrable
origine: ALI-<n>             # (maison, SG-1) provenance traçable — obligatoire côté gouvernance
```

Le corps (après le front-matter) porte le **contrat de vérification** (`checks`), la forme de la **sortie** advisory et les **garde-fous** — lisible, déterministe, non exécutable.

## Divergences assumées vs le contrat amont (tracées — [ADR-0012](../../decisions/0012-alignement-sensors-sur-ai-dlc.md))

- **DIV-command — `command` non exécutable.** Le dépôt est **doc-first** et n'embarque pas le dispatcher amont (`.ts`, `bun`, hook `PostToolUse`). Le champ obligatoire `command` porte donc un **placeholder tracé** (`non-exécutable (advisory documentaire) — voir ADR-0012`) : les sensors restent des **conventions documentées** advisory, le corps fixe la sémantique pour un outillage (script / CI) ultérieur sans redécision.
- **DIV-prefix — pas de préfixe de fichier imposé.** Le harness amont exige un préfixe de nom de fichier sur les manifestes (`core/sensors/<préfixe>-<id>.md` ; son resolver `SENSOR_FILE_REGEX` ignore les fichiers sans préfixe). Multica n'exécute pas ce resolver : les manifestes vivent sous `core/sensors/sensors/<id>.md` **sans préfixe**, en conservant l'invariant `id` = stem du fichier.
- **DIV-advisory — advisory par défaut.** Le harness amont autorise `blocking` au gate. Ici tout reste **advisory** (décision de gouvernance A2A, [ADR-0005](../../decisions/0005-verification-gates-et-sensors.md)) : le passage d'un sensor à `blocking` est une décision structurante explicite (ADR + contrôle sécurité).
- **DIV-champs — `input_schema` / `output_schema` / `timeout_seconds` omis.** Champs du dispatcher exécutable, non applicables tant que les sensors ne sont pas outillés. Le champ maison `origine` est conservé (exigence de provenance SG-1).
