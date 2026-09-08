# Protocole — définition d'un stage (schéma de front-matter)

Ce protocole fixe le **contrat** d'une fiche de stage (`stages/<phase>/<stage>.md`). Chaque fiche a **deux lecteurs qui ne se recouvrent jamais** : le **parseur** ne lit que le **front-matter YAML** (nœud de graphe : agents, mode, arêtes `consumes` / `produces`), l'**agent exécutant** ne lit que le **corps** (les trois compartiments `## Steps` / `## Sensors` / `## Learn`). Les agents y sont désignés par leur **fonction** (labels du workspace) ; aucun tooling exécutable n'est requis (conventions Markdown uniquement).

## Schéma du front-matter

```yaml
slug: <identifiant-du-stage>          # kebab-case, unique dans la phase, = nom de fichier
phase: <initialisation|analyse|matching|validation|cloture>
execution: <ALWAYS|CONDITIONAL>        # le stage s'exécute toujours, ou sous condition
condition: "<phrase décrivant la condition>"
lead_agent: <fonction|null>            # fonction responsable ou null (coordinateur)
support_agents: [<fonction>, ...]      # fonctions en appui (peut être vide)
mode: <inline|subagent>                # topologie de communication
for_each: <artefact>                   # (optionnel) itération une-fois-par-instance
summary_confirmation: <required|optional|none>
reviewer: <fonction|null>
review_class: <adversarial|advisory|none>
review_artifact: <nom-du-livrable-md>
human_gate: <none|light|granular|explicit>
produces: [<artefact>, ...]
consumes: [{artifact: <nom>, required: <true|false>}, ...]
requires_stage: [<slug>, ...]
sensors: [<nom-de-sensor>, ...]
scopes: [<scope>, ...]
inputs: "<description libre des entrées>"
outputs: "<description libre des sorties>"
```

## Champs

| Champ | Rôle |
| --- | --- |
| `slug`, `phase`, `execution`, `condition` | identité et condition d'exécution du stage |
| `mode`, `for_each`, `summary_confirmation` | topologie de communication, itération éventuelle, confirmation de résumé |
| `produces`, `consumes`, `requires_stage` | flux d'artefacts et dépendances |
| `sensors`, `scopes`, `inputs`, `outputs` | sensors importés, scopes actifs, entrées / sorties |
| `lead_agent`, `support_agents`, `reviewer` | **fonctions** du workspace : Coordinateur Matching, Analyste RFP, Gestionnaire CV, Matcher Profils |
| `review_class`, `review_artifact` | nature de la revue et livrable qui porte sa section `## Review` |
| `human_gate` | gates du workspace : `none` (Initialisation), `light` (Analyse), `granular` (Validation), `explicit` (Clôture) |

### `mode` — topologie de communication

- `inline` — le stage s'exécute dans le contexte du coordinateur ; les `support_agents` éventuels sont des voix adoptées. Stages courts.
- `subagent` — le `lead_agent` est délégué à un contexte frais (hub-and-spoke) ; chaque support est dépêché en rayon aveugle aux autres.

### `for_each` — itération

Nomme l'artefact dont les instances pilotent une exécution **une-fois-par-instance**. **Omettre le champ** ⇒ exécution unique.

### `review_class` — nature de la revue

- `adversarial` — revue **indépendante et non substituable**.
- `advisory` — revue **consultative** préparant le gate humain.
- `none` — aucune revue indépendante déclarée.

## Règles de cohérence

- `execution: CONDITIONAL` ⇒ `condition` non vide et testable.
- `human_gate` cohérent avec la phase.
- `requires_stage` ne référence que des slugs existants.
- `mode: subagent` ⇒ `support_agents` non vide.
- `reviewer != null` ⇒ `review_class != none` **et** `review_artifact` renseigné.
- `sensors:` ne référence que des manifestes existants.

## Corps de la fiche — trois compartiments (ordre fixe)

```md
# <Titre du stage>

## Objectif
<une phrase>

## Steps
### Step 1 — <titre>
<instructions impératives>
### Step 2 — ...

## Sensors
Outputs: <où atterrissent les sorties + type de gate humain>.
Imports: <miroir du front-matter `sensors:` — `none` si vide>.

## Learn
<contrat de boucle d'apprentissage>
```
