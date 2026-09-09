---
slug: chargement-cv
phase: initialisation
execution: ALWAYS
condition: "Always executes"
lead_agent: Coordinateur Matching
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
review_artifact: ""
human_gate: none
produces: [cv-available]
consumes: [{artifact: ao-pdf-received, required: true}]
requires_stage: [reception-ao]
sensors: []
scopes: [standard, format-cv]
inputs: "Confirmation de réception AO"
outputs: "Liste des CV disponibles (chemins `cv/originaux/`)"
---

# Chargement des CV

## Objectif
Vérifier l'existence et la disponibilité des CV sources des collaborateurs dans le sous-répertoire `cv/originaux/` du répertoire d'expertise.

## Steps
### Step 1 — Scan du répertoire CV
Scanner le répertoire `${ROOT_DIRECTORY}/` pour identifier les collaborateurs disposant d'un sous-répertoire `cv/`. Pour chacun, cibler le sous-répertoire **`cv/originaux/`** qui contient les CV sources (PDF, DOCX). Lister les chemins `cv/originaux/` disponibles.

### Step 2 — Vérification de complétude
Pour chaque collaborateur trouvé, vérifier que le répertoire **`cv/originaux/`** contient au moins un fichier CV source. Signaler les collaborateurs sans CV source.

Lorsque `cv/originaux/` contient **plusieurs versions**, identifier la **dernière version** (date encodée dans le nom du fichier ; à défaut, mtime la plus récente). C'est **cette seule version** qui sera analysée et croisée avec l'AO ; les versions antérieures sont ignorées.

### Step 3 — Documenter l'inventaire
Poster un commentaire sur l'issue avec :
- Nombre de CV trouvés
- Liste des collaborateurs et chemins, avec la **version retenue** (fichier + date) et le nombre de versions écartées
- Collaborateurs manquants (le cas échéant)

## Sensors
Outputs: `cv-available` → Phase Initialisation (gate: none).
Imports: none.

## Learn
Journaliser l'inventaire sur l'issue. Si des CV manquent, noter le cas.
