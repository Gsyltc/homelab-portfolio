---
slug: croisement-profils
phase: matching
execution: ALWAYS
condition: "Always executes"
lead_agent: Matcher Profils
support_agents: []
mode: subagent
summary_confirmation: optional
reviewer: null
review_class: advisory
review_artifact: ""
human_gate: light
produces: [matching-resultats]
consumes: [{artifact: ao-profils-recherches, required: true}, {artifact: cv-profils, required: true}, {artifact: cv-eligibilite, required: true}]
requires_stage: [parse-ao, extraction-cv]
sensors: []
scopes: [standard, complex, express]
inputs: "Exigences AO + verdict d'éligibilité (`cv-eligibilite`, retenus uniquement) + profils CV (dernière version JSON, `cv-profils`) des seuls retenus"
outputs: "Scores et classement des profils (JSON)"
---

# Croisement profils ↔ exigences

## Objectif
Croiser les exigences de l'AO avec les profils des collaborateurs et calculer un score pondéré pour chaque profil. **Le Matcher ne score que les collaborateurs retenus par le Gestionnaire CV** (`eligibilite.collaborateurs_possibles` de `cv-eligibilite`) : les collaborateurs `exclu` et `a_verifier` du filtre d'éligibilité amont **ne sont pas scorés**, mais sont transmis tels quels au classement/livraison. Dans les scopes `standard`, `complex` et `express`, l'artefact CV croisé est la **dernière version JSON** de chaque retenu (`<nom>-<prenom>-<AAAA-MM-JJ>.json`, `cv-profils`, référencée par `analyse_json` dans `cv-eligibilite`) — flux entre agents ; les versions JSON antérieures et les fichiers sources (supprimés après extraction) ne sont jamais utilisés.

> **Filtre d'éligibilité amont (Gestionnaire CV)** : le Gestionnaire CV a déjà appliqué, en amont, une **sélection d'éligibilité vis-à-vis de l'AO** (axes Études / MIFI si nécessaire / Expériences / **Localisation si présence sur site requise** / **Certifications requises si l'AO exige une certification `obligatoire`**) produisant trois états — `possible`, `a_verifier`, `exclu`. Le Matcher **reçoit du coordinateur uniquement la liste des retenus** (`possible`) et **ne lit / ne score que ceux-là**. Les `exclu` et `a_verifier` sont des **non-retenus d'éligibilité**, distincts des exclus « conformité études » internes au Matcher ci-dessous, et sont propagés au classement et à la livraison avec leurs raisons (dont l'axe `localisation` : ex. « AO Montréal, candidat à Québec — > 70 km », ou ville manquante en `a_verifier` ; et l'axe `certifications` : ex. « AO exige AWS Certified Solutions Architect – Associate — non détenue »).

> **Source du CV pour le matching** : le Matcher lit lui-même la **dernière version JSON** des seuls retenus (`analyse_json` de `eligibilite.collaborateurs_possibles`) — les CV ne lui sont pas transmis par le Gestionnaire CV. Si un CV PDF/DOCX a été fourni dans l'issue pour un retenu, le stage `extraction-cv` en a d'abord produit une nouvelle version JSON — c'est elle qui est croisée. Si aucun CV n'a été fourni, le matching utilise directement la **dernière version JSON déjà extraite** (flux A2A). Voir la règle de sélection de la source CV dans l'agent `Gestionnaire CV`.

## Steps
### Step 1 — Délégation au Matcher Profils
Déléguer au Matcher Profils selon la **procédure de délégation A2A définie une seule fois dans `stage-protocol` (temps 2)** : JSON de mission joint (type `delegation` du message A2A) + commentaire **minimal** = mention active `[@Matcher Profils](mention://agent/<uuid>)` + nom du fichier JSON joint. La mission vit **dans le JSON joint**, pas en prose dans le fil : croiser **la dernière version JSON** des **seuls profils retenus par le Gestionnaire CV** (`eligibilite.collaborateurs_possibles`, référencés par leur `analyse_json` dans `cv-eligibilite`) avec les exigences AO, calculer le score pondéré (compétences 50%, expérience 35%, études 10%, disponibilité 5%), classer par score décroissant. Le critère **Compétences (50 %)** **regroupe compétences + technologies + méthodologies** : évaluer la **couverture** des compétences/technologies/méthodologies exigées par l'AO (connues vs manquantes) à partir des `competences` et des agrégats `technologies`/`methodologies` du profil — le regroupement se fait **à l'intérieur** de ce critère, sans nouveau poids. **Ne pas scorer** les collaborateurs `exclu` ni `a_verifier` du filtre d'éligibilité amont — les propager tels quels (avec leurs raisons) au classement.

> **Fraîcheur des compétences** : le Matcher doit **exclure du calcul de compatibilité toute compétence, technologie ou méthodologie non utilisée depuis plus de 10 ans** (champ `derniere_utilisation` — compétence ou agrégat techno/méthodo). Une exigence couverte uniquement par un élément périmé est considérée comme **non couverte**.

> **Conformité du niveau d'études (AO gouvernemental) — double check aval du filtre amont** : le filtre d'éligibilité du Gestionnaire CV ne supprime pas ce contrôle. Lorsque `ao.client_gouvernemental = true`, le Matcher doit **croiser le niveau d'études requis + l'équivalence MIFI (`mifi`) + la politique de compensation de l'AO** pour statuer la conformité de chaque **retenu** (bloc `conformite_etudes`) — il s'agit d'un **double contrôle en aval** du filtre d'éligibilité amont. Un retenu **non conforme** (`conforme = "non"`) est **exclu** du classement (`recommandation = "exclu"`, `motif_exclusion` renseigné, `score_total` écarté). Un retenu en `conforme = "a_verifier"` (MIFI non tranché) est **signalé à l'humain**, sans exclusion automatique. Cette règle **n'altère pas** les poids du scoring immuable (voir l'agent `Matcher Profils`).
>
> **Cohérence avec le filtre amont (critère Études strict).** Depuis que l'axe **Études** est un critère **strict et éliminatoire** au filtre d'éligibilité amont (Gestionnaire CV), un collaborateur dont le niveau d'études requis est **tranché et non atteint** (ex. équivalence MIFI tranchée `non`) est déjà **`exclu` en amont** et **ne parvient pas** au Matcher. Ce double contrôle aval reste néanmoins actif comme **filet de sécurité** pour tout retenu dont la non-conformité études n'aurait pas été captée en amont.

### Step 2 — Contrôle du livrable
Vérifier que le JSON contient la liste `resultats` avec les champs : `collaborateur`, `score_total`, détail par critère (dont `score_competences` — critère regroupant compétences + technologies + méthodologies : `competences_couvertes`/`competences_manquantes`, `technologies_couvertes`/`technologies_manquantes`, `methodologies_couvertes`/`methodologies_manquantes`, mois d'XP par techno/méthodo `mois_experience_technologies`/`mois_experience_methodologies`, et `competences_ignorees_peremption`), `conformite_etudes` (dont `conforme` et `motif_exclusion` si `conforme = "non"`, renseigné pour un AO gouvernemental), `recommandation` (valeur `exclu` possible), `justification`. Vérifier également que **seuls les retenus d'éligibilité** (`possible`) figurent dans `resultats`, et que les **non-retenus d'éligibilité** (`exclu` / `a_verifier` du Gestionnaire CV, avec leurs raisons) sont **propagés tels quels** vers le classement/livraison (distincts des exclus « conformité études » du Matcher).

### Step 3 — Gate advisory
Le coordinateur présente à l'humain un **récap Markdown limité à l'action** — les scores détaillés vivent dans le JSON joint (`matching-resultats.json`), l'humain n'en lit jamais le brut. Le récap pointe le JSON et se borne à ce qui appelle une décision : top 5 des profils retenus (score + recommandation), les profils **exclus** (`recommandation = "exclu"` — non-conformité études sur AO gouvernemental, avec motif) et ceux **à vérifier** (`conformite_etudes.conforme = "a_verifier"`, MIFI non tranché), et le rappel des **non-retenus d'éligibilité amont** (Gestionnaire CV — `exclu`/`a_verifier` avec raisons par axe, dont `localisation` > 70 km / ville manquante et `certifications` obligatoires non détenues). L'humain peut ajuster les poids ou demander un recalcul.

### Step 4 — Retour de délégation A2A (OBLIGATOIRE — dernière action)
> ⛔ Le stage n'est **pas terminé** tant que ce Step n'est pas accompli. Voir la **checklist de sortie de stage** du protocole `stage-protocol`.

En toute fin de tâche, le **Matcher Profils** applique la **procédure de retour de délégation définie une seule fois dans `stage-protocol` (temps 3 + checklist de sortie de stage)** : JSON de retour joint (type `retour` du message A2A — scores + classement, artefact `matching-resultats`) + commentaire **minimal** clos par le lien de mention **actif** vers l'assigneur (le **Coordinateur Matching**) + le nom du fichier JSON — ici `[@Coordinateur Matching](mention://agent/<uuid>) — matching-resultats.json`, sans reformuler le livrable en prose. La résolution d'UUID, l'anti-wake, l'incident EXPE-58 et la vérification `trigger_outcomes` sont couverts par ce protocole (ne pas les redétailler).

## Sensors
Outputs: `matching-resultats` → Phase Matching (gate: advisory).
Imports: none.

## Learn
Documenter sur l'issue les ajustements de scoring et les validations/rejets humains.
