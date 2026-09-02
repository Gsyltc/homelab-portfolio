# Protocole — définition d'un stage (schéma de front-matter)

Ce protocole fixe le **contrat** d'une fiche de stage (`stages/<phase>/<stage>.md`). Chaque fiche porte un **front-matter YAML** suivi d'un corps Markdown exécutable (`## Steps`). Adapté d'AI-DLC 2.0 (`core/aidlc-common/stages`) au moteur A2A Multica : les personas amont sont remplacées par les **labels d'agents du workspace**, et le tooling `bun` / `aidlc-*.ts` est **exclu** (conventions Markdown uniquement — [ADR-0005](../../../decisions/0005-verification-gates-et-sensors.md), [ADR-0007](../../../decisions/0007-adaptation-modele-conductor-stages-protocols.md)).

## Schéma du front-matter

```yaml
slug: <identifiant-du-stage>          # kebab-case, unique dans la phase
phase: <initialization|ideation|inception|construction|operation>
execution: <ALWAYS|CONDITIONAL>        # le stage s'exécute toujours, ou sous condition
condition: "<phrase décrivant la condition>"   # ex. "Brownfield détecté" ; "Always executes"
lead_agent: <label|null>               # agent responsable (label du workspace) ou null (coordinateur)
support_agents: [<label>, ...]         # agents en appui (peut être vide)
mode: <inline|subagent|multi-agent>    # exécution directe, déléguée, ou multi-agents
summary_confirmation: <required|optional|none>   # résumé confirmé avant d'avancer
reviewer: <label|null>                 # agent de revue (Xavier pour la sécurité, Sylvain pour la cohérence)
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

## Champs — origine et adaptation

| Champ | Origine amont | Adaptation A2A Multica |
| --- | --- | --- |
| `slug`, `phase`, `execution`, `condition` | conservés | inchangés |
| `mode`, `summary_confirmation` | conservés | inchangés |
| `produces`, `consumes`, `requires_stage` | conservés | inchangés (artefacts documentaires) |
| `sensors`, `scopes`, `inputs`, `outputs` | conservés | sensors/scopes = ceux déjà définis (`core/sensors/`, [ADR-0003](../../../decisions/0003-scopes-et-axes-depth-verification.md)) |
| `lead_agent`, `support_agents`, `reviewer` | personas amont (`aidlc-*-agent`) | **labels d'agents du workspace** : Sylvain (coordinateur), Manuel (solution), Florian (AWS), Admin (Windows), Xavier (sécurité), Fabien (OpenSpec), Nina (archivage), Alfred (notifications) |
| `review_class` | conservé | `advisory` / `granular` / `explicit` / `none` |
| `human_gate` | **ajouté** | matérialise les gates du workspace : `none` (Initialization), `light` (Ideation), `granular` (Inception / Construction), `explicit` (Operation) |
| *(champs `bun` / tooling)* | présents amont | **supprimés** — hors périmètre (conventions Markdown, non exécutable) |

## Règles de cohérence (advisory)

- `execution: CONDITIONAL` ⇒ `condition` non vide et testable.
- `human_gate` cohérent avec la phase (voir table ci-dessus) ; un stage ne peut pas relever un gate au-dessus de sa phase sans ADR.
- `requires_stage` ne référence que des slugs existants (pas de dépendance orpheline — recoupe le contrôle `absence-orphelin` des gates).
- `reviewer: Xavier` obligatoire dès que le stage produit ou modifie une **surface de sécurité** (instructions exécutables, frontières de délégation, contrôle de sécurité) — plancher SG-3.

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
