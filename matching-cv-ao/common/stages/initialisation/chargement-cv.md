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
scopes: [standard, complex, express, format-cv]
inputs: "Confirmation de réception AO"
outputs: "Liste des CV disponibles (sources fournis en pièces jointes de l'issue + analyses existantes)"
---

# Chargement des CV

## Objectif
Recenser les CV **sources à traiter** — fournis en **pièces jointes de l'issue** — et les **analyses déjà produites** pour chaque collaborateur (JSON versionnés à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/`). Les originaux ne sont pas conservés : un collaborateur sans nouvelle pièce jointe mais disposant d'une analyse a déjà été traité.

## Steps
### Step 0 — Résoudre et verrouiller `${ROOT_DIRECTORY}`
Avant tout scan ou toute écriture, appliquer la **procédure d'enracinement `${ROOT_DIRECTORY}`** définie une seule fois dans `conductor.md` (§ Enracinement des chemins) : résoudre en chemin absolu depuis la variable d'environnement, vérifier qu'il est défini/absolu/existant et **pas** dans un répertoire de run éphémère (`/workdir/`, `/task-`, `/expe-…-<hash>/`) → sinon **halt-and-ask** (ne rien écrire, mention humaine). Journaliser sur l'issue le `${ROOT_DIRECTORY}` absolu retenu (trace d'audit).

### Step 1 — Recenser les sources et les analyses existantes
- **Sources à traiter** : lister les **pièces jointes de l'issue** (PDF, DOCX) fournies pour analyse (via `multica attachment --help` pour la récupération ; ne jamais ouvrir une URL de ressource Multica directement).
- **Analyses existantes** : scanner `${ROOT_DIRECTORY}/collaborateurs/` pour identifier, par collaborateur disposant d'un répertoire `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/`, les analyses présentes (JSON versionnés `<nom>-<prenom>-<AAAA-MM-JJ>.json` à la racine de ce répertoire `cv/`).

### Step 2 — Vérification de complétude (règle de sélection de la source CV)
Déterminer l'état par collaborateur concerné, selon la **règle de sélection de la source CV** (voir l'agent `Gestionnaire CV`) :
- **à extraire** : une pièce jointe CV (PDF/DOCX) est fournie sur l'issue → elle **prime** ; elle sera récupérée, analysée (nouvelle version), puis sa copie de travail **supprimée** ;
- **dernière version extraite** : aucune nouvelle pièce jointe mais au moins un JSON d'analyse présent → réutiliser la **dernière version déjà extraite** pour le matching (JSON pour le flux A2A ; Markdown si le fichier doit être téléchargé pour l'humain). Comportement normal, l'original ayant déjà été traité et supprimé ;
- **manquant** : ni pièce jointe ni analyse antérieure → signaler le collaborateur (pas de matching possible pour lui).

Si plusieurs pièces jointes sont fournies, elles sont toutes traitées comme sources de l'analyse à venir (aucune conservation d'historique d'originaux).

### Step 3 — Documenter l'inventaire (piste d'audit)
Tracer l'inventaire sur l'issue comme **artefact JSON joint** `cv-available` (`multica attachment`), portant :
- Nombre de collaborateurs et, pour chacun, l'état (à extraire / dernière version extraite / manquant)
- Pour les CV à extraire : liste des pièces jointes de l'issue (nom) — trace d'audit avant suppression
- Collaborateurs manquants (le cas échéant)

Stage `inline` sans gate humaine → **pas de récap Markdown**, pas de mention A2A ; le commentaire se limite à référencer l'artefact joint.

## Sensors
Outputs: `cv-available` → Phase Initialisation (gate: none).
Imports: none.

## Learn
Journaliser l'inventaire sur l'issue. Si des CV manquent, noter le cas.
