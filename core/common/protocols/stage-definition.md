# Protocole — définition d'un stage (schéma de front-matter)

Ce protocole fixe le **contrat** d'une fiche de stage (`stages/<phase>/<stage>.md`). Chaque fiche a **deux lecteurs qui ne se recouvrent jamais** : le **parseur** ne lit que le **front-matter YAML** (nœud de graphe : agents, mode, arêtes `consumes` / `produces`), l'**agent exécutant** ne lit que le **corps** (les trois compartiments `## Steps` / `## Sensors` / `## Learn`). Les agents y sont désignés par leur **fonction** (labels du workspace) ; aucun tooling exécutable n'est requis (conventions Markdown uniquement — pas de compilation `stage-graph.json`, non applicable Multica ; le graphe reste conceptuel via `consumes` / `produces` / `requires_stage`).

## Schéma du front-matter

```yaml
slug: <identifiant-du-stage>          # kebab-case, unique dans la phase, = nom de fichier
phase: <initialization|ideation|inception|construction|operation>
execution: <ALWAYS|CONDITIONAL>        # le stage s'exécute toujours, ou sous condition
condition: "<phrase décrivant la condition>"   # ex. "Brownfield détecté" ; "Always executes"
lead_agent: <fonction|null>            # fonction responsable ou null (coordinateur)
support_agents: [<fonction>, ...]      # fonctions en appui (peut être vide)
mode: <inline|subagent|pipeline|mob>   # topologie de communication (voir ci-dessous)
for_each: <artefact>                   # (optionnel) itération une-fois-par-instance ; omis ⇒ exécution unique
summary_confirmation: <required|optional|none>   # résumé confirmé avant d'avancer
reviewer: <fonction|null>              # fonction de revue (Reviewer de sécurité pour la sécurité, Reviewer de cohérence pour la cohérence)
review_class: <adversarial|advisory|none>        # nature de la revue indépendante (voir ci-dessous)
review_artifact: <nom-du-livrable-md>  # (si reviewer != null) livrable Markdown portant la section ## Review ajoutée
human_gate: <none|light|granular|explicit>       # gate humain applicable au stage (extension maison — force du gate)
produces: [<artefact>, ...]            # artefacts produits en sortie (arêtes avant)
consumes: [{artifact: <nom>, required: <true|false>}, ...]   # artefacts consommés en entrée (arêtes arrière)
requires_stage: [<slug>, ...]          # stages pré-requis (peut être vide)
sensors: [<nom-de-sensor>, ...]        # sensors importés (required-sections, upstream-coverage, diagram-validity)
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
| `lead_agent`, `support_agents`, `reviewer` | **fonctions** du workspace : Architecture Solution & Intégration (coordinateur), Architecte de solution, Architecte AWS, Administrateur infrastructure Windows, Architecte cybersécurité, Reviewer de cohérence, Reviewer de sécurité, OpenSpec Expert, Experte d'archivage, Agent de notifications — validées contre `core/agents/*.md` |
| `review_class`, `review_artifact` | nature de la revue et livrable qui porte sa section `## Review` |
| `human_gate` | matérialise les gates du workspace : `none` (Initialization), `light` (Ideation), `granular` (Inception / Construction), `explicit` (Operation) |

### `mode` — topologie de communication (qui parle à qui pendant le corps)

- `inline` — le stage s'exécute dans le contexte du coordinateur ; les `support_agents` éventuels sont des voix adoptées. Stages courts.
- `subagent` — le `lead_agent` est délégué à un contexte frais (hub-and-spoke) ; chaque support est dépêché en rayon aveugle aux autres.
- `pipeline` — les supports sont chaînés dans l'ordre déclaré, chacun voyant tout le travail amont. **Exige `support_agents` non vide.**
- `mob` — tous les supports travaillent **en parallèle** contre le brouillon du lead, en **une ronde d'objection bornée** (maillage). **Exige `support_agents` non vide.**

`support_agents` = **QUI** participe ; `mode` = **COMMENT**.

### `for_each` — itération

Nomme l'artefact dont les instances pilotent une exécution **une-fois-par-instance** (ex. `for_each: unit-of-work` : une exécution par livrable / unité de travail). **Omettre le champ** ⇒ exécution unique. L'agrégation se déduit du graphe, elle n'est pas déclarée.

### `review_class` — nature de la revue indépendante (vocabulaire amont)

- `adversarial` — revue **indépendante et non substituable** cherchant activement les failles : la **revue de sécurité** (Reviewer de sécurité, plancher SG-3 — OWASP / STRIDE). Ne peut être ni portée, ni remplacée, ni conditionnée par un autre contrôle.
- `advisory` — revue **consultative** préparant le gate humain : la **revue de cohérence** (Reviewer de cohérence — documentation ↔ décisions, conflits, complétude, conventions). Ne remplace jamais la validation humaine.
- `none` — aucune revue indépendante déclarée.

## Règles de cohérence (advisory)

- `execution: CONDITIONAL` ⇒ `condition` non vide et testable.
- `human_gate` cohérent avec la phase (voir table ci-dessus) ; un stage ne peut pas relever un gate au-dessus de sa phase sans décision structurante validée.
- `requires_stage` ne référence que des slugs existants (pas de dépendance orpheline — recoupe le contrôle `absence-orphelin` des gates).
- `mode: pipeline | mob` ⇒ `support_agents` non vide.
- `reviewer != null` ⇒ `review_class != none` **et** `review_artifact` renseigné ; `reviewer: null` ⇒ `review_class: none` et pas de `review_artifact`.
- `reviewer: Reviewer de sécurité` (⇒ `review_class: adversarial`) obligatoire dès que le stage produit ou modifie une **surface de sécurité** (instructions exécutables, frontières de délégation, contrôle de sécurité) — plancher SG-3.
- `sensors:` ne référence que des manifestes existants sous `core/sensors/sensors/` (pull-authoring, aucun id orphelin).

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
Upstream targets: <miroir de `consumes:` — présent uniquement si `upstream-coverage` importé>.
<exceptions propres au stage : sensor volontairement omis, propriété d'une sortie structurée>

## Learn
<contrat de boucle d'apprentissage — voir ci-dessous>
```

- **`## Steps`** — prose impérative : le travail métier du stage. Compartiment le plus édité quand on change *ce que fait* le stage sans toucher au graphe.
- **`## Sensors`** — résumé local compact : où atterrissent les sorties, `Imports:` qui **reflète** le front-matter `sensors:`, et `Upstream targets:` qui **reflète** `consumes:` **quand** `upstream-coverage` est importé. Le comportement partagé des sensors vit dans [`stage-protocol.md`](stage-protocol.md) (temps 4) ; ne consigner ici que les exceptions propres au stage.
- **`## Learn`** — pointe vers le **contrat de boucle d'apprentissage** du workspace : journal des candidats-règles sur l'issue pendant le travail, puis remontée et persistance des apprentissages **confirmés** au gate humain, dans [`core/rules/`](../../rules/README.md) (cycle capture → confirmation humaine → contrôle de conflit → écriture). Les stages d'Initialization tiennent le journal mais **sautent** l'interaction liée au gate (bootstrap déterministe).

Le corps est un **artefact de framework, immuable en forme** : la structure `## Steps` / `## Sensors` / `## Learn` n'est jamais réécrite par un workflow. La seule édition sanctionnée en cours de workflow est l'ajout d'un id de sensor à la liste `sensors:` du front-matter par la boucle d'apprentissage.
