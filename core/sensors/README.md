# Verification gates & Sensors — fiabilisation déterministe

Ce répertoire contient les **manifestes déclaratifs** des mécanismes de fiabilisation déterministe décrits dans [`core/common/protocols/governance-security.md`](../common/protocols/governance-security.md) et référencés par [`core/common/conductor.md`](../common/conductor.md).

Deux mécanismes complémentaires, **tous deux advisory** :

- **Verification gates** — contrôle automatique de **traçabilité** aux **frontières de phases**, en amont du gate humain ([`gates.md`](gates.md)).
- **Sensors** — checks **déterministes** déclenchés soit **à l'écriture d'un artefact** (`fire_on: write`), soit **au gate de phase** (`fire_on: gate`) ([`sensors/`](sensors/)).

## Nature : manifeste déclaratif + exécutable Python

Chaque manifeste fixe le **contrat** (périmètre de déclenchement, règles, sortie). Un **dispatcher Python** l'exécute de façon déterministe ([ADR-0046](../../decisions/0046-sensors-executables-python-et-hooks-agnostiques.md)).

> **Convention d'invocation.** Le harnais (`sensor.py`, manifestes, hook) vit dans ce dépôt — le **checkout `homelab-portfolio`** (le dépôt `core`) — **jamais** dans le dépôt du projet vérifié. Les commandes ci-dessous se lancent **depuis ce checkout**, désignant le script par un **chemin ancré** sur sa racine (`$CORE_HOME` = racine du checkout `core`), tandis que `--root <projet>` pointe le dépôt du projet à vérifier. Un chemin **relatif** (`core/scripts/sensor.py`) ne se résout que si le répertoire courant est déjà ce checkout ; lancé depuis le dossier du projet, il échoue en « script introuvable » (origine ORIG-425/ORIG-426).

| Commande | Rôle |
| --- | --- |
| `python3 "$CORE_HOME/core/scripts/sensor.py" list` | Sensors, script associé et état (`⛔` si script absent ou invalide) |
| `python3 "$CORE_HOME/core/scripts/sensor.py" --root <projet> fire <id> [--path <fichier>...]` | Exécute un sensor. Sans `--path` : balayage de gate sur le périmètre `matches` |
| `python3 "$CORE_HOME/core/scripts/sensor.py" --root <projet> gate <frontière> [--attest a,b]` | Rapport de vérification d'une frontière de [`gates.md`](gates.md) |
| `python3 "$CORE_HOME/core/scripts/sensor.py" report-check --stage <fiche> [--report-file F]` | Contrôle de gate du compte rendu : section `## Sensors` absente alors que la fiche de stage déclare `sensors:` non vide ⇒ `⚠️` écart (advisory) |
| `python3 "$CORE_HOME/core/scripts/sensors/<id avec _>.py" --root <projet> [--path <fichier>...]` | Exécute un sensor seul (ex. `required_sections_adr.py`) : un script par sensor |
| `python3 "$CORE_HOME/core/sensors/hooks/post_write.py"` | Hook d'écriture : lit le JSON du harnais sur stdin, lance les sensors `fire_on: write` |

Python 3.9+, bibliothèque standard uniquement. Tests : `python3 -m unittest discover -s core/scripts/tests`.

Le code retour est **0** même en écart (advisory). `--strict` renvoie 1 en cas d'écart ou de `⛔` : usage CI uniquement. `--format json` donne une sortie exploitable par un script.

Le dispatcher applique les clauses de sécurité dans le code :

- **SG-1** — manifeste sans `origine` ou `kind` invalide ⇒ `⛔`.
- **SG-2** — sensor inconnu, périmètre vide, fichier hors périmètre, erreur d'exécution ⇒ `⛔`.
- **SG-4** — parsing statique seul ; une inclusion distante est signalée, jamais suivie.
- **SG-5** — chaque rapport porte `manifeste @ commit` ; commit non traçable ⇒ `⛔` (surcharge : `SENSORS_SOURCE_COMMIT`).

### Portée des contrôles

Les contrôles sont des **faits de forme**, pas des jugements :

- `diagram-validity` vérifie la structure (type de diagramme, délimiteurs, parenthésage), sans rendu.
- `claim-sources` et `traceability` reposent sur des motifs : `ALI-/HOM-/ORIG-<n>`, `BA-<n>`, `FR-/NFR-<n>`, liens Markdown, ADR cités.
- `traceability` échoue fermé (`⛔`) s'il ne trouve aucun identifiant amont.

### Hooks

Le hook lance, à chaque écriture de fichier, les sensors `fire_on: write` dont `matches` correspond, ainsi que les sensors `fire_on: gate` dont `write_matches` correspond (ex. `required-sections-adr`). Il sort **toujours en 0**. `--sensors a,b` le restreint aux sensors déclarés par le stage actif. `--audit-file <fichier>` ajoute le rapport à un `audit.md` append-only (hors Multica, ADR-0038).

Claude Code (`.claude/settings.json`) :

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/core/sensors/hooks/post_write.py\" --format claude" }
        ]
      }
    ]
  }
}
```

Kiro CLI (agent, `hooks.postToolUse`) — chemin **ancré** sur le checkout `core` (`$CORE_HOME`), afin que le hook se déclenche même quand le répertoire courant est le dépôt du projet vérifié (sinon « script introuvable », origine ORIG-425/ORIG-426) :

```json
{ "matcher": "fs_write", "command": "python3 \"${CORE_HOME:-.}/core/sensors/hooks/post_write.py\"" }
```

> Le repli `${CORE_HOME:-.}` conserve le comportement historique (chemin relatif au cwd) quand `$CORE_HOME` n'est pas défini et que l'agent tourne déjà depuis le checkout `core`.

Sous Multica, l'agent auteur lance `fire` lui-même au temps 4 du [`stage-protocol`](../common/protocols/stage-protocol.md) et poste le rapport sur l'issue. Le hook est de plus **branché par défaut** sur les **agents de production de livrables** (champ `hooks.postToolUse` de leur fiche, matcher `fs_write`) comme **filet déterministe** : il déclenche les sensors `fire_on: write` à chaque écriture, sans dépendre de la discipline manuelle au temps 4 (durcissement ORIG-418 ; périmètre documenté dans [`../agents/README.md`](../agents/README.md), « Hook d'écriture des sensors »). Le hook **ne remplace pas** le lancement explicite ni le compte rendu `## Sensors` — il reste **advisory** (code 0, jamais bloquant).

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

Onze sensors, alignés sur le contrat amont « Sensors » (schéma de manifeste `id` / `kind` / `command` / `default_severity` / `description` + `category` / `fire_on` / `matches`). Les `id` sont importés **par id nu** dans le champ `sensors:` des fiches de stage (pull-authoring).

| Sensor | Manifeste | `category` | `fire_on` | `default_severity` | Objet |
| --- | --- | --- | --- | --- | --- |
| `required-sections-adr` | [`sensors/required-sections-adr.md`](sensors/required-sections-adr.md) | document-shape | gate (+ écriture via `write_matches`) | advisory | Rubriques obligatoires et forme des ADR : front matter, statut unique, puces codées, remplacement cohérent, `Critères de décision` (HOM-285) |
| `required-sections-architecture` | [`sensors/required-sections-architecture.md`](sensors/required-sections-architecture.md) | document-shape | gate | advisory | Fichiers/sections **mandatory** de la DAS (`001`, `01`, `02`, `06`, `08`, `10`, `11`) et de l'architecture détaillée (`architecture-securite/` : surfaces, STRIDE, OWASP) présents et non vides (durci ALI-218, [ADR-0025](../../decisions/0025-durcissement-required-sections-das.md)) |
| `data-lifecycle` | [`sensors/data-lifecycle.md`](sensors/data-lifecycle.md) | document-shape | gate | advisory | Document **Cycle de vie des données** (`10-cycle_vie_donnees.md`) présent et renseigné (cycle de vie, gouvernance, classification) **selon les données du projet**. **Advisory** : assiste la revue **Architecte de solution → Architecte de données** et alerte le coordinateur, **sans jamais bloquer** (origine ALI-231) |
| `upstream-coverage` | [`sensors/upstream-coverage.md`](sensors/upstream-coverage.md) | document-shape | gate | advisory | Référence explicite à la demande amont (issue / ADR parent) |
| `diagram-validity` | [`sensors/diagram-validity.md`](sensors/diagram-validity.md) | document-shape | write | advisory | Syntaxe des diagrammes en code (Mermaid / PlantUML / Structurizr) |
| `sujets-a-jour` | [`sensors/sujets-a-jour.md`](sensors/sujets-a-jour.md) | document-shape | write | advisory | Le champ `sujets` du front-matter d'un document d'architecture reflète ses titres `##`/`###` (présence, titres obsolètes, ordre) — sommaire de ciblage pour le lazy loading |
| `detailed-arch-refs` | [`sensors/detailed-arch-refs.md`](sensors/detailed-arch-refs.md) | document-shape | write | advisory | Renvois vers l'architecture détaillée au format d'ancre Structurizr (`documentation/<SS>#<ancre>`, pas de chemin de fichier) et absence de suffixe de nom de système dans les titres du détail (origine ORIG-261) |
| `claim-sources` | [`sensors/claim-sources.md`](sensors/claim-sources.md) | provenance | gate | advisory | Chaque affirmation retenue porte une source résoluble ; hypothèses = confirmation humaine explicite |
| `style-concision` | [`sensors/style-concision.md`](sensors/style-concision.md) | document-shape | write | advisory | Style concis des documents livrables : paragraphes et phrases courts, puces limitées en profondeur, tableaux hors gabarit sobres (`RULE-WS-007`) |
| `traceability` | [`sensors/traceability.md`](sensors/traceability.md) | traceability | gate | advisory | Chaîne besoin (BA-…, MoSCoW) → exigence → scénario → ADR → livrable cohérente, sans orphelin dérivé |
| `checklist-progress` | [`sensors/checklist-progress.md`](sensors/checklist-progress.md) | progress | gate | advisory | **Restitue** l'avancement de la checklist d'architecture (`00-checklist-architecture.md`) — % global de la **solution**, du **cadrage**, des **besoins (MoSCoW)** et des **livrables** — lu par l'Architecte de solution intégrateur **avant chaque gate granulaire humaine en Construction**. Il **constate**, ne calcule ni n'écrit rien (barème 80/10/10 = source unique du protocole) ; aucun auto-accept (origine HOM-273) |

> `linter` et `type-check` (sensors AI-DLC de qualité de code) restent **N/A** tant que le dépôt ne produit ni code ni IaC ; ils seront ajoutés le jour où un livrable exécutable apparaît (repli « stratégie de tests » de l'axe de vérification.

## Format d'un manifeste de sensor (contrat amont)

Le front-matter est un **descripteur de capacité pur** (ce qu'est le check et comment il s'invoque) ; il ne cite jamais de stage. La liaison stage ↔ sensor vit côté stage (`sensors:`), c'est le **pull-authoring**.

```yaml
id: <identifiant>            # kebab-case, = stem du fichier (obligatoire)
kind: deterministic          # seule valeur acceptée aujourd'hui (obligatoire)
command: <commande d'invocation>  # (obligatoire) — python3 core/scripts/sensor.py fire <id>
default_severity: advisory   # advisory | blocking (obligatoire) — blocking = ADR + contrôle sécurité
description: <une ligne>     # description humaine (obligatoire)
category: <label libre>      # (optionnel) — document-shape | provenance | traceability
fire_on: gate                # (optionnel) write | gate — défaut : write
write_matches: <glob>        # (optionnel, sensor gate) déclenché aussi à l'écriture, par le hook, sur ce glob
matches: <glob>              # (optionnel) filtre de chemin ; au gate, glob absent ⇒ tout livrable
origine: ALI-<n>             # (maison, SG-1) provenance traçable — obligatoire côté gouvernance
```

Le corps (après le front-matter) porte le **contrat de vérification** (`checks`), la forme de la **sortie** advisory et les **garde-fous** — lisible et déterministe ; son exécution est assurée par `core/scripts/sensor.py`.
