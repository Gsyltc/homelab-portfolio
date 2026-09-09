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
sensors: [disponibilite-complete]
scopes: [standard, format-cv]
inputs: "Inventaire des CV disponibles"
outputs: "Profils CV structurés (JSON versionné, dernière version) + fiches d'analyse Markdown versionnées (racine `cv/`, anciennes fiches archivées dans `cv/archives/`)"
---

# Extraction des CV

## Objectif
Lire les CV sources des collaborateurs (dans `cv/originaux/`) et en extraire les informations structurées (compétences avec ancienneté, expérience, études, disponibilité). Pour un matching, seule la **dernière version** de chaque CV source est analysée. La date de dernière modification reportée est **toujours la date du jour**.

## Steps
### Step 1 — Délégation au Gestionnaire CV
Mentionner le Gestionnaire CV avec mission claire :
- pour chaque collaborateur, **sélectionner la dernière version** du CV source **dans `cv/originaux/`** (date dans le nom de fichier, à défaut mtime la plus récente) et n'analyser que celle-ci ;
- lire cette version, extraire les informations structurées ;
- pour **chaque compétence**, renseigner le **nombre de mois d'expérience** (`mois_experience`) et la **date de dernière utilisation** (`derniere_utilisation`) ;
- renseigner **obligatoirement** la **disponibilité** de chaque collaborateur comme objet `disponibilite` avec `date_disponibilite` (date ISO `AAAA-MM-JJ`) et `taux_utilisation` (en %, 0–100) ;
- renseigner `date_derniere_modification` avec **la date du jour** de l'analyse (ISO `AAAA-MM-JJ`), jamais la date du fichier source ;
- **archiver** : avant d'écrire la fiche du jour, **déplacer** toute fiche d'analyse Markdown antérieure présente à la racine de `cv/` dans le sous-répertoire **`cv/archives/`** ;
- **créer un fichier Markdown d'analyse versionné** `<AAAA-MM-JJ>-<nom>-<prenom>.md` à la racine du répertoire `cv/` du candidat (`<AAAA-MM-JJ>` = date du jour ISO ; `<nom>`/`<prenom>` en minuscules, cohérents avec le répertoire `<nom-prenom>/cv/`) ;
- **écrire le JSON d'analyse versionné** `<nom>-<prenom>-<AAAA-MM-JJ>.json` à la racine de `cv/`, **sans écraser** les versions antérieures (historique conservé) ; renseigner `analyse_json` avec ce chemin ;
- produire le JSON `collaborateurs` (voir la fiche du Gestionnaire CV pour la sélection de la dernière version JSON pour le matching et la journalisation d'audit) ;
- **en fin de tâche, rendre le résultat en mentionnant en retour le Coordinateur** `[@Coordinateur Matching](mention://agent/<UUID-COORDINATEUR>)` (mention agent valide), pas seulement en répondant dans le fil — une réponse simple ne réveille pas le Coordinateur ; puis vérifier les `trigger_outcomes`. Ne jamais deviner ni coder en dur l'UUID : le résoudre à chaque fois via `multica agent list --output json` et l'injecter dans la mention.

### Step 2 — Contrôle du livrable
Vérifier que le JSON contient bien la liste `collaborateurs` avec les champs : `nom`, `date_derniere_modification` (= date du jour), `version_cv` (fichier + date retenue depuis `cv/originaux/`), `analyse_markdown` (chemin créé à la racine de `cv/`), `analyse_json` (chemin JSON versionné), `competences` (objets `{nom, mois_experience, derniere_utilisation}`), `experience`, `etudes`, `disponibilite` (objet **obligatoire** `{date_disponibilite, taux_utilisation}`). Vérifier qu'un fichier `<AAAA-MM-JJ>-<nom>-<prenom>.md` (racine de `cv/`) et un fichier `<nom>-<prenom>-<AAAA-MM-JJ>.json` versionné ont bien été créés par candidat, et que les fiches Markdown antérieures ont été déplacées dans `cv/archives/`. Signaler les écarts.

### Step 3 — Validation humaine légère
Présenter à l'humain : nombre de collaborateurs analysés, version de CV source retenue par candidat (depuis `cv/originaux/`), chemins des fichiers d'analyse Markdown créés et des JSON versionnés, synthèse des profils extraits. Demander validation.

## Sensors
Outputs: `cv-profils` → Phase Analyse (gate: light).
Imports: `disponibilite-complete` — contrôle la présence obligatoire de `disponibilite.date_disponibilite` et `disponibilite.taux_utilisation` sur chaque profil, signalé à la frontière Analyse → Matching (advisory). Voir [`../../../sensors/disponibilite.md`](../../../sensors/disponibilite.md).

## Learn
Documenter sur l'issue les choix d'extraction et les validations/rejets humains.
