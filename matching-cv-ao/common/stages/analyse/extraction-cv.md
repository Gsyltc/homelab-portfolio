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
inputs: "Inventaire des CV disponibles (pièces jointes de l'issue + analyses existantes)"
outputs: "Profils CV structurés (JSON versionné, dernière version) + fiches d'analyse Markdown versionnées (racine `cv/`, anciennes fiches archivées dans `cv/archives/`) ; copie de travail des CV sources supprimée après extraction"
---

# Extraction des CV

## Objectif
Récupérer les CV sources des collaborateurs **fournis en pièces jointes de l'issue** (via `multica attachment`), en extraire les informations structurées (compétences avec ancienneté, expérience, études, disponibilité), produire les livrables versionnés dans `cv/`, puis **supprimer la copie de travail téléchargée** (les originaux ne sont **pas conservés**). La date de dernière modification reportée est **toujours la date du jour**.

> **Extraction conditionnée par la fourniture d'un CV** (voir la règle de sélection de la source CV dans [`../../../agents/gestionnaire-cv-agent.md`](../../../agents/gestionnaire-cv-agent.md)) : l'extraction ne s'exécute que **pour les collaborateurs dont un CV PDF/DOCX est joint à l'issue**. Pour un collaborateur sans pièce jointe, **aucune nouvelle extraction** n'est faite : le matching réutilisera la **dernière version déjà extraite** (JSON en flux A2A, Markdown si un fichier doit être téléchargé pour l'humain).

## Steps
### Step 1 — Délégation au Gestionnaire CV
Mentionner le Gestionnaire CV avec mission claire :
- pour chaque collaborateur, **récupérer le(s) CV source(s) depuis les pièces jointes de l'issue** (via `multica attachment` ; jamais en ouvrant une URL de ressource Multica) et en extraire les informations structurées ;
- pour **chaque compétence**, renseigner le **nombre de mois d'expérience** (`mois_experience`) et la **date de dernière utilisation** (`derniere_utilisation`) ;
- renseigner **obligatoirement** la **disponibilité** de chaque collaborateur comme objet `disponibilite` avec `date_disponibilite` (date ISO `AAAA-MM-JJ`) et `taux_utilisation` (en %, 0–100) ;
- renseigner `date_derniere_modification` avec **la date du jour** de l'analyse (ISO `AAAA-MM-JJ`), jamais la date du fichier source ;
- renseigner `source_cv` (`fichier`, `provenance: "issue-attachment"`, `conserve: false`) pour tracer la pièce jointe traitée **avant sa suppression** ;
- **journaliser sur l'issue**, **avant suppression**, le(s) nom(s) de la/des pièce(s) jointe(s) traitée(s) (seule trace d'audit de l'original) ;
- **archiver** : avant d'écrire la fiche du jour, **déplacer** toute fiche d'analyse Markdown antérieure présente à la racine de `cv/` dans le sous-répertoire **`cv/archives/`** ;
- **créer un fichier Markdown d'analyse versionné** `<AAAA-MM-JJ>-<nom>-<prenom>.md` à la racine du répertoire `cv/` du candidat (`<AAAA-MM-JJ>` = date du jour ISO ; `<nom>`/`<prenom>` en minuscules, cohérents avec le répertoire `<nom-prenom>/cv/`) ;
- **écrire le JSON d'analyse versionné** `<nom>-<prenom>-<AAAA-MM-JJ>.json` à la racine de `cv/`, **sans écraser** les versions antérieures (historique conservé) ; renseigner `analyse_json` avec ce chemin ;
- **une fois les livrables écrits et vérifiés, supprimer la copie de travail téléchargée** (aucun original n'est écrit dans `cv/`). **Ne jamais supprimer la copie de travail avant** d'avoir écrit et vérifié le Markdown et le JSON versionné ;
- produire le JSON `collaborateurs` (voir la fiche du Gestionnaire CV pour la sélection de la dernière version JSON pour le matching et la journalisation d'audit) ;
- **en fin de tâche, rendre le résultat en mentionnant en retour le Coordinateur** `[@Coordinateur Matching](mention://agent/<UUID-COORDINATEUR>)` (mention agent valide), pas seulement en répondant dans le fil — une réponse simple ne réveille pas le Coordinateur ; puis vérifier les `trigger_outcomes`. Ne jamais deviner ni coder en dur l'UUID : le résoudre à chaque fois via `multica agent list --output json` et l'injecter dans la mention.

### Step 2 — Contrôle du livrable
Vérifier que le JSON contient bien la liste `collaborateurs` avec les champs : `nom`, `date_derniere_modification` (= date du jour), `source_cv` (fichier + `provenance: "issue-attachment"` + `conserve: false`), `analyse_markdown` (chemin créé à la racine de `cv/`), `analyse_json` (chemin JSON versionné), `competences` (objets `{nom, mois_experience, derniere_utilisation}`), `experience`, `etudes`, `disponibilite` (objet **obligatoire** `{date_disponibilite, taux_utilisation}`). Vérifier qu'un fichier `<AAAA-MM-JJ>-<nom>-<prenom>.md` (racine de `cv/`) et un fichier `<nom>-<prenom>-<AAAA-MM-JJ>.json` versionné ont bien été créés par candidat, que les fiches Markdown antérieures ont été déplacées dans `cv/archives/`, et que la **copie de travail téléchargée a bien été supprimée** (aucun original écrit dans `cv/`) une fois les livrables produits. Signaler les écarts.

### Step 3 — Validation humaine légère
Présenter à l'humain : nombre de collaborateurs analysés, pièce(s) jointe(s) source(s) traitée(s) puis supprimée(s) (nom, journalisé avant suppression), chemins des fichiers d'analyse Markdown créés et des JSON versionnés, synthèse des profils extraits. Demander validation.

## Sensors
Outputs: `cv-profils` → Phase Analyse (gate: light).
Imports: `disponibilite-complete` (advisory) — contrôle la présence de `disponibilite.{date_disponibilite, taux_utilisation}` à la frontière Analyse → Matching.

## Learn
Documenter sur l'issue les choix d'extraction et les validations/rejets humains.
