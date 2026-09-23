---
slug: parse-ao
phase: analyse
execution: ALWAYS
condition: "Always executes"
lead_agent: Analyste RFP
support_agents: []
mode: subagent
summary_confirmation: optional
reviewer: null
review_class: advisory
review_artifact: ""
human_gate: light
produces: [ao-exigences, ao-profils-recherches, ao-expertise-firme]
consumes: [{artifact: ao-pdf-received, required: true}, {artifact: clients-contextes, required: false}]
requires_stage: [chargement-cv]
sensors: [expertise-firme]
scopes: [standard, complex, express]
inputs: "PDF d'AO + chemin du répertoire + référentiel des contextes clients (`${ROOT_DIRECTORY}/clients/*.json`, si disponible)"
outputs: "Résumé AO (JSON) + exigences + profils recherchés + évaluation d'expertise de firme (`ao-expertise-firme`, non bloquante — gate humaine légère si minimums non atteints)"
---

# Analyse de l'AO

## Objectif
Parser le PDF d'appel d'offres, en extraire les exigences fonctionnelles et techniques, identifier les profils recherchés, et — lorsque l'AO exige une **expertise/expérience de firme** — évaluer si la firme y répond à partir du référentiel des contextes clients (`${ROOT_DIRECTORY}/clients/*.json`), de façon **non bloquante** (gate humaine légère si les minimums ne sont pas atteints).

## Steps
### Step 1 — Délégation à l'Analyste RFP
Déléguer à l'Analyste RFP selon la **procédure de délégation A2A définie une seule fois dans `stage-protocol` (temps 2)** : JSON de mission joint (type `delegation` du message A2A) + commentaire **minimal** = mention active `[@Analyste RFP](mention://agent/<uuid>)` + nom du fichier JSON joint. La mission — parser le PDF d'AO, extraire exigences et profils recherchés, produire le JSON structuré, sauvegarder dans `${ROOT_DIRECTORY}/ao/<client>/<titre-ao>` — vit **dans le JSON joint**, pas en prose dans le fil. Le JSON de mission cadre notamment : **détecter le caractère gouvernemental du client** (`client_gouvernemental`) et, le cas échéant, la **politique d'équivalence des diplômes** acceptée par l'AO (`equivalence_diplomes` : mécanisme, compensation en années d'xp par année d'études manquante, `reference_ao`) — exemple : « Niveau requis Baccalauréat — Équivalence DEC + 3 années d'xp par année d'études manquante ». **Détecter le mode de travail** (`localisation_travail.mode` ∈ {`teletravail`, `sur_site`, `hybride`, `non_precise`}) et, pour un travail `sur_site`/`hybride`, **extraire l'adresse du site** (`ville_site` au minimum, `adresse_site` si disponible) avec le `rayon_km` de proximité (défaut `70`) — ex. « présence sur site à Montréal ». **Ne jamais inventer** : si l'AO ne précise pas, `acceptee: "non_precise"` / `mode: "non_precise"` et champs à `null`. Renseigner `etudes_requises` de chaque profil recherché avec le niveau requis. **Détecter les certifications requises** (`profils_recherches[].certifications_requises`) : pour chaque certification citée dans l'AO, renseigner `nom` (libellé exact), `organisme` (si précisé), `criticite` (`obligatoire` = prérequis/exigé → **critère d'éligibilité éliminatoire** en amont ; `souhaitee`/`nice-to-have` = non éliminatoire) et `reference_ao` — ex. « Prérequis : certification AWS Certified Solutions Architect – Associate » ⇒ `criticite: "obligatoire"`. **Ne rien inventer** : aucune certification ⇒ `certifications_requises: []` ; caractère exigé/souhaité ambigu ⇒ `criticite: "souhaitee"` + mention humaine (jamais d'`obligatoire` inféré sans base explicite). **Évaluer l'expertise de firme** lorsque l'AO exige une **expérience/expertise de firme** (mandats similaires, secteur, technologies ou contexte comparables) : croiser cette exigence avec le **référentiel des contextes clients** `${ROOT_DIRECTORY}/clients/*.json` (contexte des sociétés + mandats réalisés par la firme, maintenu par le Gestionnaire CV) et produire l'objet `expertise_firme` (`exigee`, `criteres_attendus`, `couverture` appuyée sur des preuves du référentiel, `verdict` ∈ {`conforme`, `minimums_non_atteints`, `indeterminable`}, `gate_humaine` ∈ {`aucune`, `legere`}). **Analyse NON bloquante** : elle n'arrête jamais le workflow ; si les minimums ne sont pas atteints (`verdict` ≠ `conforme`), positionner `gate_humaine: "legere"` + `detail_gate`. **Ne rien inventer** : couverture uniquement d'après le référentiel `clients/` (référentiel vide/insuffisant ⇒ `non_couvert`/`indeterminable`, jamais une expertise supposée).

### Step 2 — Contrôle du livrable
Vérifier que le JSON retourné contient bien les champs : `ao` (metadata, dont `client_gouvernemental`, `equivalence_diplomes` avec `acceptee` ∈ {`oui`, `non`, `non_precise`}, et `localisation_travail` avec `mode` ∈ {`teletravail`, `sur_site`, `hybride`, `non_precise`} et `ville_site` non nul si `mode` ∈ {`sur_site`, `hybride`}), `exigences` (liste), `profils_recherches` (liste, dont `etudes_requises` renseigné et `certifications_requises` — liste, `[]` si aucune — dont chaque entrée porte `nom`, `criticite` ∈ {`obligatoire`, `souhaitee`, `nice-to-have`} et `reference_ao`), et `expertise_firme` (objet dont `exigee` ∈ {`oui`, `non`, `non_precise`}, `couverture` appuyée sur `clients/*.json`, `verdict` ∈ {`conforme`, `minimums_non_atteints`, `indeterminable`}, `gate_humaine` ∈ {`aucune`, `legere`} — `legere` + `detail_gate` renseigné si `verdict` ≠ `conforme`). Signaler les écarts.

### Step 3 — Validation humaine légère (gate)
Le coordinateur présente à l'humain un **récap Markdown détaillé** — le JSON joint (`resume-ao.json`) reste la source/audit, l'humain n'en lit jamais le brut mais reçoit une restitution lisible et complète. Le récap reprend **en clair** : **pour un AO gouvernemental**, la politique d'équivalence des diplômes détectée (`equivalence_diplomes`) **ou son absence** (`non_precise` — ne rien inventer) ; le **mode de travail** (`localisation_travail.mode`) et, pour `sur_site`/`hybride`, la ville/adresse du site + le **rayon de proximité** (70 km par défaut) ; les **certifications requises** en distinguant `obligatoire` (éliminatoire) de `souhaitee`/`nice-to-have`, ou l'absence (`[]`) ; l'**évaluation d'expertise de firme** (`expertise_firme` — `verdict` + couverture). **Cette analyse ne bloque pas** : si `verdict` ∈ {`minimums_non_atteints`, `indeterminable`} (`gate_humaine: "legere"`), **signaler le point + demander une confirmation légère** (poursuivre malgré le manque, ou compléter le référentiel `clients/`) sans arrêt automatique. Demander validation (Keep/Modify/Redo).

### Step 4 — Retour de délégation A2A (OBLIGATOIRE — dernière action)
> ⛔ Le stage n'est **pas terminé** tant que ce Step n'est pas accompli. Voir la **checklist de sortie de stage** du protocole `stage-protocol`.

En toute fin de tâche, l'**Analyste RFP** applique la **procédure de retour de délégation définie une seule fois dans `stage-protocol` (temps 3 + checklist de sortie de stage)** : JSON de retour joint (type `retour` du message A2A) + commentaire **minimal** clos par le lien de mention **actif** vers l'assigneur (le **Coordinateur Matching**) + le nom du fichier JSON — ici `[@Coordinateur Matching](mention://agent/<uuid>) — resume-ao.json`, sans reformuler le livrable en prose. La résolution d'UUID, l'anti-wake, l'incident EXPE-58 et la vérification `trigger_outcomes` sont couverts par ce protocole (ne pas les redétailler).

## Sensors
Outputs: `ao-exigences`, `ao-profils-recherches`, `ao-expertise-firme` → Phase Analyse (gate: light). `ao-expertise-firme` porte l'évaluation d'expertise de firme (non bloquante) et déclenche une **gate humaine légère** si les minimums ne sont pas atteints.
Imports: `expertise-firme` (advisory) — contrôle l'objet `expertise_firme` de l'AO au regard du référentiel `${ROOT_DIRECTORY}/clients/*.json` et signale, sans bloquer, un `verdict` ≠ `conforme` (gate humaine légère) — voir le sensor `expertise-firme`.

## Learn
Documenter sur l'issue les choix d'extraction et les validations/rejets humains.
