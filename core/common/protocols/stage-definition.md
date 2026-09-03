# Protocole — définition d'un stage (schéma de front-matter)

Ce protocole fixe le **contrat** d'une fiche de stage (`stages/<phase>/<stage>.md`). Chaque fiche porte un **front-matter YAML** suivi d'un corps Markdown exécutable (`## Steps`). Les agents y sont désignés par leur **fonction** (labels du workspace) ; aucun tooling exécutable n'est requis (conventions Markdown uniquement).

## Schéma du front-matter

```yaml
slug: <identifiant-du-stage>          # kebab-case, unique dans la phase
phase: <initialization|ideation|inception|construction|operation>
execution: <ALWAYS|CONDITIONAL>        # le stage s'exécute toujours, ou sous condition
condition: "<phrase décrivant la condition>"   # ex. "Brownfield détecté" ; "Always executes"
lead_agent: <fonction|null>            # fonction responsable ou null (coordinateur)
support_agents: [<fonction>, ...]      # fonctions en appui (peut être vide)
mode: <inline|subagent|multi-agent>    # exécution directe, déléguée, ou multi-agents
summary_confirmation: <required|optional|none>   # résumé confirmé avant d'avancer
reviewer: <fonction|null>              # fonction de revue (Reviewer de sécurité pour la sécurité, Reviewer de cohérence pour la cohérence)
review_class: <advisory|granular|explicit|none>  # classe de revue attendue
human_gate: <none|light|granular|explicit>       # gate humain applicable au stage
produces: [<artefact>, ...]            # artefacts produits en sortie
consumes: [{artifact: <nom>, required: <true|false>}, ...]   # artefacts consommés en entrée
requires_stage: [<slug>, ...]          # stages pré-requis (peut être vide)
sensors: [<nom-de-sensor>, ...]        # sensors déclenchés à l'écriture (required-sections, upstream-coverage, diagram-validity)
scopes: [<scope>, ...]                 # scopes où le stage est actif (voir scopes-and-axes.md)
inputs: "<description libre des entrées>"
outputs: "<description libre des sorties>"
```

## Champs

| Champ | Rôle |
| --- | --- |
| `slug`, `phase`, `execution`, `condition` | identité et condition d'exécution du stage |
| `mode`, `summary_confirmation` | mode d'exécution et confirmation de résumé |
| `produces`, `consumes`, `requires_stage` | flux d'artefacts et dépendances |
| `sensors`, `scopes`, `inputs`, `outputs` | sensors déclenchés, scopes actifs, entrées / sorties |
| `lead_agent`, `support_agents`, `reviewer` | **fonctions** du workspace : Architecture Solution & Intégration (coordinateur), Architecte de solution, Architecte AWS, Administrateur infrastructure Windows, Architecte cybersécurité, Reviewer de cohérence, Reviewer de sécurité, OpenSpec Expert, Experte d'archivage, Agent de notifications |
| `review_class` | `advisory` / `granular` / `explicit` / `none` |
| `human_gate` | matérialise les gates du workspace : `none` (Initialization), `light` (Ideation), `granular` (Inception / Construction), `explicit` (Operation) |

## Règles de cohérence (advisory)

- `execution: CONDITIONAL` ⇒ `condition` non vide et testable.
- `human_gate` cohérent avec la phase (voir table ci-dessus) ; un stage ne peut pas relever un gate au-dessus de sa phase sans décision structurante validée.
- `requires_stage` ne référence que des slugs existants (pas de dépendance orpheline — recoupe le contrôle `absence-orphelin` des gates).
- `reviewer: Reviewer de sécurité` obligatoire dès que le stage produit ou modifie une **surface de sécurité** (instructions exécutables, frontières de délégation, contrôle de sécurité) — plancher SG-3.

## Corps de la fiche

Après le front-matter, le corps contient :

```md
# <Titre du stage>

## Objectif
<une phrase>

## Steps
### Step 1 — <titre>
<instructions exécutables>
### Step 2 — ...

## Gate / sortie
<artefacts de sortie + type de gate humain>
```
