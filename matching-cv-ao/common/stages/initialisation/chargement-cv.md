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
outputs: "Liste des CV disponibles (sources à traiter dans `cv/originaux/` + analyses existantes)"
---

# Chargement des CV

## Objectif
Recenser, pour chaque collaborateur, les CV **sources à traiter** déposés dans le sous-répertoire `cv/originaux/` (dépôt temporaire, vidé après extraction) et les **analyses déjà produites** (JSON versionnés à la racine de `cv/`). Les originaux ne sont pas conservés : un collaborateur sans source dans `cv/originaux/` mais disposant d'une analyse a déjà été traité.

## Steps
### Step 1 — Scan du répertoire CV
Scanner le répertoire `${ROOT_DIRECTORY}/` pour identifier les collaborateurs disposant d'un sous-répertoire `cv/`. Pour chacun, relever :
- les **CV sources à traiter** présents dans **`cv/originaux/`** (PDF, DOCX) — dépôt temporaire ;
- les **analyses existantes** (JSON versionnés `<nom>-<prenom>-<AAAA-MM-JJ>.json` à la racine de `cv/`).

### Step 2 — Vérification de complétude
Pour chaque collaborateur, déterminer l'état :
- **source à traiter** : au moins un fichier dans `cv/originaux/` → sera lu puis **supprimé** par l'extraction ;
- **déjà analysé** : aucun source dans `cv/originaux/` mais au moins un JSON d'analyse présent → l'original a déjà été traité et supprimé (comportement normal) ;
- **manquant** : ni source ni analyse → signaler le collaborateur.

Si plusieurs fichiers sources sont présents dans `cv/originaux/`, ils sont tous traités comme sources de l'analyse à venir (aucune conservation d'historique d'originaux).

### Step 3 — Documenter l'inventaire
Poster un commentaire sur l'issue avec :
- Nombre de collaborateurs et, pour chacun, l'état (source à traiter / déjà analysé / manquant)
- Pour les sources à traiter : liste des fichiers présents dans `cv/originaux/` (nom + date) — trace d'audit avant suppression
- Collaborateurs manquants (le cas échéant)

## Sensors
Outputs: `cv-available` → Phase Initialisation (gate: none).
Imports: none.

## Learn
Journaliser l'inventaire sur l'issue. Si des CV manquent, noter le cas.
