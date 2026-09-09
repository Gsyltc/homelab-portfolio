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
outputs: "Liste des CV disponibles (sources fournis en pièces jointes de l'issue + analyses existantes)"
---

# Chargement des CV

## Objectif
Recenser les CV **sources à traiter** — fournis en **pièces jointes de l'issue** — et les **analyses déjà produites** pour chaque collaborateur (JSON versionnés à la racine de `cv/`). Les originaux ne sont pas conservés : un collaborateur sans nouvelle pièce jointe mais disposant d'une analyse a déjà été traité.

## Steps
### Step 1 — Recenser les sources et les analyses existantes
- **Sources à traiter** : lister les **pièces jointes de l'issue** (PDF, DOCX) fournies pour analyse (via `multica attachment --help` pour la récupération ; ne jamais ouvrir une URL de ressource Multica directement).
- **Analyses existantes** : scanner `${ROOT_DIRECTORY}/` pour identifier, par collaborateur disposant d'un répertoire `cv/`, les analyses présentes (JSON versionnés `<nom>-<prenom>-<AAAA-MM-JJ>.json` à la racine de `cv/`).

### Step 2 — Vérification de complétude
Déterminer l'état par collaborateur concerné :
- **source à traiter** : une pièce jointe CV est fournie sur l'issue → sera récupérée, analysée, puis sa copie de travail **supprimée** ;
- **déjà analysé** : aucune nouvelle pièce jointe mais au moins un JSON d'analyse présent → l'original a déjà été traité et supprimé (comportement normal) ;
- **manquant** : ni pièce jointe ni analyse → signaler le collaborateur.

Si plusieurs pièces jointes sont fournies, elles sont toutes traitées comme sources de l'analyse à venir (aucune conservation d'historique d'originaux).

### Step 3 — Documenter l'inventaire
Poster un commentaire sur l'issue avec :
- Nombre de collaborateurs et, pour chacun, l'état (source à traiter / déjà analysé / manquant)
- Pour les sources à traiter : liste des pièces jointes de l'issue (nom) — trace d'audit avant suppression
- Collaborateurs manquants (le cas échéant)

## Sensors
Outputs: `cv-available` → Phase Initialisation (gate: none).
Imports: none.

## Learn
Journaliser l'inventaire sur l'issue. Si des CV manquent, noter le cas.
