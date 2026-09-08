---
slug: extraction-cv
phase: analyse
execution: ALWAYS
condition: "Always executes"
lead_agent: Gestionnaire CV
support_agents: []
mode: subagent
summary_confirmation: optional
reviewer: null
review_class: advisory
review_artifact: ""
human_gate: light
produces: [cv-profils]
consumes: [{artifact: cv-available, required: true}]
requires_stage: [chargement-cv]
sensors: []
scopes: [standard]
inputs: "Inventaire des CV disponibles"
outputs: "Profils CV structurés (JSON, dernière version) + fiches d'analyse Markdown versionnées"
---

# Extraction des CV

## Objectif
Lire les CV des collaborateurs et en extraire les informations structurées (compétences avec ancienneté, expérience, études, disponibilité). Pour un matching, seule la **dernière version** de chaque CV est analysée.

## Steps
### Step 1 — Délégation au Gestionnaire CV
Mentionner le Gestionnaire CV avec mission claire :
- pour chaque collaborateur, **sélectionner la dernière version** du CV (date dans le nom de fichier, à défaut mtime la plus récente) et n'analyser que celle-ci ;
- lire cette version, extraire les informations structurées ;
- pour **chaque compétence**, renseigner le **nombre de mois d'expérience** (`mois_experience`) et la **date de dernière utilisation** (`derniere_utilisation`) ;
- produire le JSON `collaborateurs` ;
- **créer un fichier Markdown d'analyse versionné** `analyse-cv-<AAAA-MM-JJ>.md` dans le répertoire `cv/` du candidat.

### Step 2 — Contrôle du livrable
Vérifier que le JSON contient bien la liste `collaborateurs` avec les champs : `nom`, `version_cv` (fichier + date retenue), `analyse_markdown` (chemin créé), `competences` (objets `{nom, mois_experience, derniere_utilisation}`), `experience`, `etudes`, `disponibilite`. Vérifier qu'un fichier `analyse-cv-<date>.md` a bien été créé par candidat. Signaler les écarts.

### Step 3 — Validation humaine légère
Présenter à l'humain : nombre de collaborateurs analysés, version de CV retenue par candidat, chemins des fichiers d'analyse Markdown créés, synthèse des profils extraits. Demander validation.

## Sensors
Outputs: `cv-profils` → Phase Analyse (gate: light).
Imports: none.

## Learn
Documenter sur l'issue les choix d'extraction et les validations/rejets humains.
