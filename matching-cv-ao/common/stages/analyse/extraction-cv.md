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
produces: [cv-profils, cv-eligibilite]
consumes: [{artifact: cv-available, required: true}, {artifact: ao-profils-recherches, required: true}]
requires_stage: [chargement-cv, parse-ao]
sensors: [disponibilite-complete, equivalence-mifi]
scopes: [standard, format-cv]
inputs: "Inventaire des CV disponibles (pièces jointes de l'issue + analyses existantes)"
outputs: "Profils CV structurés (JSON versionné, dernière version) + fiches d'analyse Markdown versionnées (racine `cv/`, anciennes fiches archivées dans `cv/archives/`) + verdict d'éligibilité vis-à-vis de l'AO (`cv-eligibilite` : possibles / à vérifier / exclus + raisons, sans transmission des CV) ; copie de travail des CV sources supprimée après extraction"
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
- renseigner l'objet **`mifi`** (équivalence MIFI) de chaque collaborateur selon les **4 états** d'`equivalence_requise` (`non_requise` | `oui` | `non` | `a_verifier`) : diplôme canadien → `non_requise` (`niveau_equivalent_qc` = niveau tel quel) ; MIFI mentionné → `oui` + `niveau_equivalent_qc` + `reference_mifi` ; études étrangères sans MIFI → `a_verifier`. **Ne rien inventer** : pour **chaque** collaborateur en `a_verifier`, **poser une mention humaine** sur l'issue demandant de trancher (le CV ne permet pas de conclure). Après réponse humaine, passer l'état à `oui` (avec niveau) ou `non` et fixer `source: "humain"` ;
- renseigner `date_derniere_modification` avec **la date du jour** de l'analyse (ISO `AAAA-MM-JJ`), jamais la date du fichier source ;
- renseigner `source_cv` (`fichier`, `provenance: "issue-attachment"`, `conserve: false`) pour tracer la pièce jointe traitée **avant sa suppression** ;
- **journaliser sur l'issue**, **avant suppression**, le(s) nom(s) de la/des pièce(s) jointe(s) traitée(s) (seule trace d'audit de l'original) ;
- **archiver** : avant d'écrire la fiche du jour, **déplacer** toute fiche d'analyse Markdown antérieure présente à la racine de `cv/` dans le sous-répertoire **`cv/archives/`** ;
- **créer un fichier Markdown d'analyse versionné** `<AAAA-MM-JJ>-<nom>-<prenom>.md` à la racine du répertoire `cv/` du candidat (`<AAAA-MM-JJ>` = date du jour ISO ; `<nom>`/`<prenom>` en minuscules, cohérents avec le répertoire `<nom-prenom>/cv/`) ;
- **écrire le JSON d'analyse versionné** `<nom>-<prenom>-<AAAA-MM-JJ>.json` à la racine de `cv/`, **sans écraser** les versions antérieures (historique conservé) ; renseigner `analyse_json` avec ce chemin ;
- **une fois les livrables écrits et vérifiés, supprimer la copie de travail téléchargée** (aucun original n'est écrit dans `cv/`). **Ne jamais supprimer la copie de travail avant** d'avoir écrit et vérifié le Markdown et le JSON versionné ;
- produire le JSON `collaborateurs` (voir la fiche du Gestionnaire CV pour la sélection de la dernière version JSON pour le matching et la journalisation d'audit) ;
- **en fin de tâche, rendre le résultat en mentionnant en retour le Coordinateur** `[@Coordinateur Matching](mention://agent/<UUID-COORDINATEUR>)` (mention agent valide), pas seulement en répondant dans le fil — une réponse simple ne réveille pas le Coordinateur ; puis vérifier les `trigger_outcomes`. Ne jamais deviner ni coder en dur l'UUID : le résoudre à chaque fois via `multica agent list --output json` et l'injecter dans la mention.

### Step 2 — Sélection d'éligibilité vis-à-vis de l'AO
Une fois les profils extraits et **vérifiés à jour et cohérents**, le Gestionnaire CV applique le **filtre d'éligibilité en amont du matching** au regard des `profils_recherches` / exigences de l'AO (`ao-profils-recherches`, produit par `parse-ao`) :

- évaluer chaque collaborateur sur **3 axes vis-à-vis de l'AO** — **Études**, **MIFI (si nécessaire)**, **Expériences** — plus un contrôle de **cohérence / fraîcheur** du CV ;
- classer chaque collaborateur dans **un** des **3 états** : `possible` (retenu), `a_verifier` (arbitrage humain requis — ex. MIFI non tranché, **ne rien inventer**), `exclu` (écarté définitivement, avec raisons) ;
- produire le JSON **`eligibilite`** (artefact `cv-eligibilite`) : `collaborateurs_possibles` (`nom` + `analyse_json` de la dernière version JSON retenue), `collaborateurs_a_verifier` (`nom` + `raisons` `{axe, detail}`), `collaborateurs_exclus` (`nom` + `raisons` `{axe, detail}`). Axes de raison : `etudes | mifi | experiences | coherence | fraicheur_cv` ;
- pour un collaborateur `mifi.equivalence_requise = a_verifier` **non tranché**, le classer `a_verifier` (jamais `exclu` de force) et **poser/entretenir une mention humaine** — ne rien inventer ;
- **Garde-fou — ne pas transmettre les CV** : au coordinateur, ne remonter que le verdict `eligibilite` + la référence `analyse_json` des retenus. Ni sources, ni fiches Markdown, ni JSON complet ne circulent (voir [`../../../agents/gestionnaire-cv-agent.md`](../../../agents/gestionnaire-cv-agent.md), `## Garde-fou — non-transmission des CV`).

### Step 3 — Contrôle du livrable
Vérifier que le JSON contient bien la liste `collaborateurs` avec les champs : `nom`, `date_derniere_modification` (= date du jour), `source_cv` (fichier + `provenance: "issue-attachment"` + `conserve: false`), `analyse_markdown` (chemin créé à la racine de `cv/`), `analyse_json` (chemin JSON versionné), `competences` (objets `{nom, mois_experience, derniere_utilisation}`), `experience`, `etudes`, `mifi` (objet `{equivalence_requise, diplome_origine, pays_etudes, niveau_equivalent_qc, reference_mifi, source, commentaire}` avec `equivalence_requise` ∈ {`non_requise`, `oui`, `non`, `a_verifier`}), `disponibilite` (objet **obligatoire** `{date_disponibilite, taux_utilisation}`). Vérifier également que le JSON contient l'objet **`eligibilite`** à 3 états (`collaborateurs_possibles` / `collaborateurs_a_verifier` / `collaborateurs_exclus`), que chaque `a_verifier` et `exclu` porte au moins une **raison** (`axe` + `detail`), et que chaque `possible` porte une référence `analyse_json`. Vérifier qu'un fichier `<AAAA-MM-JJ>-<nom>-<prenom>.md` (racine de `cv/`) et un fichier `<nom>-<prenom>-<AAAA-MM-JJ>.json` versionné ont bien été créés par candidat, que les fiches Markdown antérieures ont été déplacées dans `cv/archives/`, et que la **copie de travail téléchargée a bien été supprimée** (aucun original écrit dans `cv/`) une fois les livrables produits. Signaler les écarts.

### Step 4 — Validation humaine légère
Présenter à l'humain : nombre de collaborateurs analysés, pièce(s) jointe(s) source(s) traitée(s) puis supprimée(s) (nom, journalisé avant suppression), chemins des fichiers d'analyse Markdown créés et des JSON versionnés, synthèse des profils extraits. **Présenter le statut d'équivalence MIFI par collaborateur** (`equivalence_requise` + `niveau_equivalent_qc`) et **lister explicitement les collaborateurs en `a_verifier`** pour lesquels une réponse humaine est attendue (le CV ne permet pas de trancher — ne rien inventer). **Présenter le verdict d'éligibilité vis-à-vis de l'AO** en distinguant clairement les **retenus** (`possible`), les **à vérifier** (`a_verifier`, avec raisons + arbitrage humain attendu) et les **exclus** (`exclu`, avec raisons par axe). Demander validation.

## Sensors
Outputs: `cv-profils`, `cv-eligibilite` → Phase Analyse (gate: light). `cv-eligibilite` porte le verdict d'éligibilité vis-à-vis de l'AO (3 états) et alimente le matching (seuls les `possible` sont scorés).
Imports: `disponibilite-complete` (advisory) — contrôle la présence de `disponibilite.{date_disponibilite, taux_utilisation}` à la frontière Analyse → Matching ; `equivalence-mifi` (advisory) — contrôle la présence et la cohérence de l'objet `mifi` (4 états d'`equivalence_requise`) et signale les collaborateurs en `a_verifier` à la frontière Analyse → Matching.

## Learn
Documenter sur l'issue les choix d'extraction et les validations/rejets humains.
