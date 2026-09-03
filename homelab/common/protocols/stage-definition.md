# Protocole — définition d'un stage (schéma de front-matter)

Ce protocole fixe le **contrat** d'une fiche de stage (`stages/<phase>/<stage>.md`) du workflow Homelab. Chaque fiche a **deux lecteurs qui ne se recouvrent jamais** : le **parseur** ne lit que le **front-matter YAML** (nœud de graphe : agents, mode, arêtes `consumes` / `produces`), l'**agent exécutant** ne lit que le **corps** (les trois compartiments `## Steps` / `## Sensors` / `## Learn`). Les agents y sont désignés par leur **fonction** (rôles génériques du workflow) ; aucun tooling exécutable n'est requis (conventions Markdown uniquement — pas de compilation `stage-graph.json`, non applicable Multica ; le graphe reste conceptuel via `consumes` / `produces` / `requires_stage`).

Miroir Homelab de [`core/common/protocols/stage-definition.md`](../../../core/common/protocols/stage-definition.md), adapté aux 5 phases Homelab, aux 7 scopes et à l'équipe DevOps Homelab.

## Schéma du front-matter

```yaml
slug: <identifiant-du-stage>          # kebab-case, unique dans la phase, = nom de fichier
phase: <initialisation|ideation|cadrage|production|validation>
execution: <ALWAYS|CONDITIONAL>        # le stage s'exécute toujours, ou sous condition
condition: "<phrase décrivant la condition>"   # ex. "Demande n8n détectée" ; "Always executes"
lead_agent: <fonction|null>            # fonction responsable ou null (Tech Lead / coordinateur)
support_agents: [<fonction>, ...]      # fonctions en appui (peut être vide)
mode: <inline|subagent|pipeline|mob>   # topologie de communication (voir ci-dessous)
for_each: <artefact>                   # (optionnel) itération une-fois-par-instance ; omis ⇒ exécution unique
summary_confirmation: <required|optional|none>   # résumé confirmé avant d'avancer
reviewer: <fonction|null>              # fonction de revue (QA Docker pour la technique/sécurité, Architecte de sécurité Homelab pour le jugement sécurité)
review_class: <adversarial|advisory|none>        # nature de la revue indépendante (voir ci-dessous)
review_artifact: <nom-du-livrable>     # (si reviewer != null) livrable portant la section ## Review ajoutée
human_gate: <none|light|granular|explicit>       # gate humain applicable au stage (force du gate)
produces: [<artefact>, ...]            # artefacts produits en sortie (arêtes avant)
consumes: [{artifact: <nom>, required: <true|false>}, ...]   # artefacts consommés en entrée (arêtes arrière)
requires_stage: [<slug>, ...]          # stages pré-requis (peut être vide)
sensors: [<id-de-sensor>, ...]         # sensors importés par id nu (voir homelab/sensors/)
scopes: [<scope>, ...]                 # scopes où le stage est actif (voir scopes-and-axes.md)
inputs: "<description libre des entrées>"
outputs: "<description libre des sorties>"
```

## Champs

| Champ | Rôle |
| --- | --- |
| `slug`, `phase`, `execution`, `condition` | identité et condition d'exécution du stage |
| `mode`, `for_each`, `summary_confirmation` | topologie de communication, itération éventuelle, confirmation de résumé |
| `produces`, `consumes`, `requires_stage` | flux d'artefacts et dépendances (le graphe émerge de ces déclarations) |
| `sensors`, `scopes`, `inputs`, `outputs` | sensors importés, scopes actifs, entrées / sorties |
| `lead_agent`, `support_agents`, `reviewer` | **fonctions** de l'équipe : Tech Lead Homelab (coordinateur), Spécialiste Docker, QA Docker, Spécialiste Terraform, Expert n8n, Expert Home Assistant, Architecte de sécurité Homelab, Agent de notifications — validées contre [`homelab/agents/`](../../agents/README.md) |
| `review_class`, `review_artifact` | nature de la revue et livrable qui porte sa section `## Review` |
| `human_gate` | matérialise les gates du workflow : `none` (Initialisation), `light` (Idéation), `granular` (Cadrage / Production), `explicit` (Validation) |

### `mode` — topologie de communication (qui parle à qui pendant le corps)

- `inline` — le stage s'exécute dans le contexte du Tech Lead ; les `support_agents` éventuels sont des voix adoptées. Stages courts (bootstrap, cadrage, aiguillage).
- `subagent` — le `lead_agent` est délégué à un contexte frais (hub-and-spoke) via une mention A2A ; chaque support est dépêché en rayon aveugle aux autres.
- `pipeline` — les supports sont chaînés dans l'ordre déclaré, chacun voyant tout le travail amont (ex. Spécialiste Docker → QA Docker → Spécialiste Terraform). **Exige `support_agents` non vide.**
- `mob` — tous les supports travaillent **en parallèle** contre le brouillon du lead, en **une ronde d'objection bornée**. **Exige `support_agents` non vide.**

`support_agents` = **QUI** participe ; `mode` = **COMMENT**.

### `for_each` — itération

Nomme l'artefact dont les instances pilotent une exécution **une-fois-par-instance** (ex. `for_each: livrable-stack` : une exécution par livrable). **Omettre le champ** ⇒ exécution unique.

### `review_class` — nature de la revue indépendante

- `adversarial` — revue **indépendante et non substituable** cherchant activement les failles : la **revue de sécurité Homelab** (QA Docker pour la sécurité technique compose / Traefik ; Architecte de sécurité Homelab pour le jugement de posture — hardening, secrets, exposition, permissions). Plancher SG-3. Ne peut être ni portée, ni remplacée, ni conditionnée par un gate/sensor advisory.
- `advisory` — revue **consultative** préparant le gate humain : le contrôle qualité central du Tech Lead (aiguillage GO / RENVOI, cohérence livrable ↔ demande / paramètres). Ne remplace jamais la validation humaine.
- `none` — aucune revue indépendante déclarée.

## Règles de cohérence (advisory)

- `execution: CONDITIONAL` ⇒ `condition` non vide et testable.
- `human_gate` cohérent avec la phase (voir table ci-dessus) ; un stage ne peut pas relever un gate au-dessus de sa phase sans décision structurante validée.
- `requires_stage` ne référence que des slugs existants (pas de dépendance orpheline — recoupe le contrôle `absence-orphelin` des gates).
- `mode: pipeline | mob` ⇒ `support_agents` non vide.
- `reviewer != null` ⇒ `review_class != none` **et** `review_artifact` renseigné ; `reviewer: null` ⇒ `review_class: none` et pas de `review_artifact`.
- `reviewer: QA Docker` (⇒ `review_class: adversarial`) obligatoire dès que le stage produit ou modifie une **surface de sécurité** (livrable compose / Terraform, hardening, exposition, Traefik) — plancher SG-3.
- `sensors:` ne référence que des manifestes existants sous [`homelab/sensors/sensors/`](../../sensors/README.md#sensors-définis) (pull-authoring, aucun id orphelin).

## Corps de la fiche — trois compartiments (ordre fixe)

Après le front-matter, le corps a **trois compartiments, toujours dans cet ordre** : `## Steps`, `## Sensors`, `## Learn`.

```md
# <Titre du stage>

## Objectif
<une phrase>

## Steps
### Step 1 — <titre>
<instructions impératives que l'agent suit>
### Step 2 — ...

## Sensors
Outputs: <où atterrissent les sorties + type de gate humain>.
Imports: <miroir du front-matter `sensors:` — `none` si vide>.
Upstream targets: <miroir de `consumes:` — présent uniquement si pertinent>.
<exceptions propres au stage>

## Learn
<contrat de boucle d'apprentissage — voir ci-dessous>
```

- **`## Steps`** — prose impérative : le travail métier du stage. Compartiment le plus édité quand on change *ce que fait* le stage sans toucher au graphe.
- **`## Sensors`** — résumé local compact : où atterrissent les sorties, `Imports:` qui **reflète** le front-matter `sensors:`, et `Upstream targets:` qui **reflète** `consumes:`. Le comportement partagé des sensors vit dans [`../../sensors/README.md`](../../sensors/README.md) ; ne consigner ici que les exceptions propres au stage.
- **`## Learn`** — pointe vers le **contrat de boucle d'apprentissage** du Homelab : journal des candidats-règles sur l'issue pendant le travail, puis remontée et persistance des apprentissages **confirmés** au gate humain, dans [`homelab/rules/`](../../rules/README.md) (cycle capture → confirmation humaine → contrôle de conflit → écriture). Les stages d'Initialisation tiennent le journal mais **sautent** l'interaction liée au gate (bootstrap déterministe).

Le corps est un **artefact de framework, immuable en forme** : la structure `## Steps` / `## Sensors` / `## Learn` n'est jamais réécrite par un workflow. La seule édition sanctionnée en cours de workflow est l'ajout d'un id de sensor à la liste `sensors:` du front-matter par la boucle d'apprentissage (déclencheur `SENSOR_PROPOSED`).
