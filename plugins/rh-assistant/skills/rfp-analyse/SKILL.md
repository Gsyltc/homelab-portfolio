---
name: rfp-analyse
description: >
    Analyse d'un appel d'offres (AO) du workflow Matching : parsing du PDF/DOCX fourni, extraction structurée des exigences (fonctionnelles, techniques, organisationnelles) et des profils recherchés, détection du caractère gouvernemental et de la politique d'équivalence des diplômes, détection du mode de travail et de la localisation du site (rayon de proximité), production du résumé versionné en JSON et sauvegarde dans le répertoire de l'AO. Charger avant toute analyse d'appel d'offres.
keywords: [analyse ao, appel d'offres, rfp, parse ao, exigences, profils recherches, scoring implicite, equivalence diplomes, client gouvernemental, localisation travail, rayon proximite, certifications requises, certification prerequis]
---

# Analyse d'appel d'offres (AO)

Cette compétence porte tout le détail opératoire de l'**analyse d'un appel d'offres** pour le workflow Matching : parsing du document, extraction des exigences et des profils recherchés, détection du contexte gouvernemental / équivalence des diplômes, détection du mode de travail / localisation, puis production du résumé structuré en JSON. Elle est chargée par l'agent **Analyste RFP** et alimente le stage [`parse-ao`](../../../../matching-cv-ao/common/stages/analyse/parse-ao.md) (phase Analyse) du workflow Matching.

L'AO source est fourni **en pièce jointe de l'issue** (PDF/DOCX) ou dans le **contenu de l'issue**. Le livrable (résumé JSON) est écrit dans `${ROOT_DIRECTORY}/ao/<client>/<titre-ao>/`.

## Responsabilités opératoires

1. **Parser le document d'AO** fourni par le Coordinateur (pièce jointe récupérée via `multica attachment`, jamais en ouvrant une URL de ressource Multica ; ou contenu de l'issue).
2. **Extraire les exigences** : fonctionnelles, techniques, organisationnelles. Identifier les **critères de scoring** explicites et implicites de l'AO.
3. **Identifier les profils recherchés** : compétences requises, expérience souhaitée, études, **certifications requises** et disponibilité. Renseigner `etudes_requises` de chaque profil avec le **niveau requis** (ex. `Baccalauréat`) et `certifications_requises` avec les certifications exigées/souhaitées (chacune avec sa `criticite` — une certification `obligatoire` est un **prérequis éliminatoire** traité en amont par l'éligibilité).
4. **Détecter le caractère gouvernemental** du client (`client_gouvernemental`) et, le cas échéant, la **politique d'équivalence des diplômes** acceptée par l'AO (`equivalence_diplomes`).
5. **Détecter le mode de travail** (`localisation_travail`) et, pour un travail sur site / hybride, la **localisation du site** (rayon de proximité).
6. **Créer les dossiers si absents** — toujours au bon chemin : `${ROOT_DIRECTORY}/ao/<client>/<titre-ao>/` (`client` = nom du client, `titre-ao` = slug du titre).
7. **Sauvegarder le résumé JSON** dans ce répertoire.

> **Ne jamais inventer.** Toute donnée non présente dans l'AO reste `non_precise` / `null` avec, si utile, une mention humaine pour lever le doute. Aucune exigence, aucun profil, aucun niveau d'études, aucune localisation ne se fabrique.

## Format de sortie (JSON → Agent)

```json
{
  "ao": {
    "client": "<nom du client>",
    "titre": "<titre de l'AO>",
    "date_reception": "<YYYY-MM-DD>",
    "contexte": "<résumé du contexte>",
    "client_gouvernemental": true,
    "equivalence_diplomes": {
      "acceptee": "oui | non | non_precise",
      "mecanisme": "<ex. 'compensation des études', 'MIFI', 'équivalence DEC'>",
      "compensation_annees_par_annee_manquante": "<nb d'années d'xp par année d'études manquante, ex. 3>",
      "reference_ao": "<citation/section de l'AO — ne jamais inventer>"
    },
    "localisation_travail": {
      "mode": "teletravail | sur_site | hybride | non_precise",
      "ville_site": "<ville du site de travail — requise si sur_site/hybride, sinon null>",
      "adresse_site": "<adresse complète du site si disponible, sinon null>",
      "rayon_km": 70,
      "reference_ao": "<citation/section de l'AO — ne jamais inventer>"
    }
  },
  "exigences": [
    {
      "id": "EX-001",
      "type": "technique|fonctionnelle|organisationnelle",
      "description": "<description>",
      "criticite": "obligatoire|souhaitee|nice-to-have"
    }
  ],
  "profils_recherches": [
    {
      "id": "PR-001",
      "intitule": "<intitulé du poste>",
      "competences_requises": ["<compétence>"],
      "experience_requise": "<description>",
      "etudes_requises": "<niveau/formation requis, ex. Baccalauréat>",
      "certifications_requises": [
        {
          "nom": "<intitulé exact de la certification, ex. AWS Certified Solutions Architect – Associate>",
          "organisme": "<organisme émetteur si précisé, ex. AWS, sinon null>",
          "criticite": "obligatoire | souhaitee | nice-to-have",
          "reference_ao": "<citation/section de l'AO — ne jamais inventer>"
        }
      ],
      "disponibilite": "<immédiate|<durée>>"
    }
  ],
  "scoring_implicite": [
    {
      "critere": "<critère identifié dans l'AO>",
      "poids_implicite": "<fort|moyen|faible>",
      "justification": "<pourquoi ce poids>"
    }
  ]
}
```

## Champs `client_gouvernemental` et `equivalence_diplomes` (contexte gouvernemental Québec)

`client_gouvernemental` (booléen) indique si le client est un organisme gouvernemental. Pour un AO gouvernemental, le niveau d'études requis est un **critère de conformité éliminatoire** : un collaborateur non conforme peut être **exclu** du classement par le Matcher (voir [`matcher-profils-agent.md`](../../../../matching-cv-ao/agents/matcher-profils-agent.md)). `equivalence_diplomes` documente la **politique d'équivalence** acceptée par l'AO :

- `acceptee` : `oui` (l'AO accepte une équivalence/compensation), `non` (niveau strict exigé), ou `non_precise` (l'AO ne dit rien) ;
- `mecanisme` : nature de l'équivalence (ex. « compensation des études », « MIFI », « équivalence DEC ») ;
- `compensation_annees_par_annee_manquante` : nb d'années d'expérience pertinente compensant **une** année d'études manquante (ex. `3` → un BAC requis peut être compensé par ~3 ans d'xp par année manquante) ;
- `reference_ao` : citation/section de l'AO qui fonde la politique.

**Ne jamais inventer** : si l'AO ne précise pas la politique d'équivalence, renseigner `acceptee: "non_precise"` et les autres champs à `null` (une mention humaine peut être posée pour lever le doute). Renseigner `etudes_requises` de chaque `profils_recherches` avec le **niveau requis** (ex. `Baccalauréat`).

## Champ `certifications_requises` (certification prérequis — critère éliminatoire)

Chaque `profils_recherches[].certifications_requises` liste les **certifications professionnelles exigées ou souhaitées** par l'AO pour le profil (ex. `AWS Certified Solutions Architect – Associate`, `PMP`, `Scrum Master`). Cette liste est **distincte** de `competences_requises` et de `etudes_requises` : une certification n'est ni une compétence générique, ni un niveau d'études.

Chaque entrée porte :

- `nom` : intitulé **exact** de la certification tel qu'écrit dans l'AO (ne pas normaliser à outrance — conserver le libellé qui permet la correspondance côté CV) ;
- `organisme` : organisme émetteur si l'AO le précise (ex. `AWS`, `PMI`, `Scrum.org`), sinon `null` ;
- `criticite` : `obligatoire` (prérequis / exigé — **critère d'éligibilité éliminatoire** en aval), `souhaitee`, ou `nice-to-have` ;
- `reference_ao` : citation/section de l'AO qui fonde l'exigence (piste d'audit — **ne jamais inventer**).

> **Certification `obligatoire` = prérequis éliminatoire.** Lorsqu'une certification est marquée `criticite: "obligatoire"` (formulée dans l'AO comme « prérequis », « requis », « exigé »), elle devient un **critère d'éligibilité STRICT et éliminatoire** appliqué **en amont** du scoring par le Gestionnaire CV (axe `certifications` du filtre d'éligibilité — voir la compétence `cv-analyse` et [`gestionnaire-cv-agent.md`](../../../../matching-cv-ao/agents/gestionnaire-cv-agent.md)) : un collaborateur qui **ne détient pas** cette certification est **exclu** du matching. Une certification `souhaitee`/`nice-to-have` **n'exclut pas** : elle alimente uniquement la couverture Compétences côté Matcher.

**Ne jamais inventer** : si l'AO ne cite aucune certification, mettre `certifications_requises: []`. Si l'AO cite une certification sans dire clairement si elle est exigée ou seulement souhaitée, renseigner la `criticite` la plus prudente (`souhaitee`) et poser une **mention humaine** pour lever le doute — **jamais** de `obligatoire` inféré sans base explicite (l'éliminatoire ne se déduit pas).

## Champ `localisation_travail` (proximité géographique)

Objet renseigné pour statuer sur la contrainte de localisation du mandat. `mode` porte **4 valeurs** :

- `teletravail` — travail à distance : **aucune contrainte de proximité** ; `ville_site`/`adresse_site` = `null`.
- `sur_site` — présence sur site requise : `ville_site` (au minimum) **obligatoire**, `adresse_site` si disponible.
- `hybride` — présence partielle sur site : `ville_site` **obligatoire** (la contrainte de proximité s'applique comme pour `sur_site`).
- `non_precise` — l'AO ne précise pas le mode de travail : champs de localisation à `null` (**ne rien inventer** ; mention humaine possible).

`rayon_km` est le **rayon de proximité** au-delà duquel un collaborateur est exclu (par défaut `70`, sauf rayon explicite dans l'AO). Pour un AO `sur_site`/`hybride`, la localisation du candidat (ville) devient un **critère d'éligibilité** : un collaborateur situé à **plus de `rayon_km` (70 km par défaut)** de `ville_site` est **exclu** (voir [`gestionnaire-cv-agent.md`](../../../../matching-cv-ao/agents/gestionnaire-cv-agent.md) et [`matcher-profils-agent.md`](../../../../matching-cv-ao/agents/matcher-profils-agent.md)). En `teletravail`, ce critère ne s'applique pas.

## Stockage du livrable

- Répertoire de l'AO : `${ROOT_DIRECTORY}/ao/<client>/<titre-ao>/` — `client` = nom du client, `titre-ao` = slug du titre. **Créer les dossiers si absents.**
- Le résumé JSON structuré est écrit dans ce répertoire.
- Ne jamais coder en dur un chemin absolu : toujours partir de `${ROOT_DIRECTORY}`.
- La pièce jointe source (PDF/DOCX) est une **copie de travail transitoire** : elle n'est pas stockée dans le répertoire de l'AO ; journaliser son nom sur l'issue (piste d'audit).

## Contrôle du livrable (avant remise)

Vérifier que le JSON produit contient bien :

- `ao` (métadonnées) dont `client_gouvernemental`, `equivalence_diplomes` avec `acceptee` ∈ {`oui`, `non`, `non_precise`}, et `localisation_travail` avec `mode` ∈ {`teletravail`, `sur_site`, `hybride`, `non_precise`} et `ville_site` **non nul** si `mode` ∈ {`sur_site`, `hybride`} ;
- `exigences` (liste) ;
- `profils_recherches` (liste) dont `etudes_requises` renseigné pour chaque profil, et `certifications_requises` (liste, `[]` si aucune) dont chaque entrée porte `nom`, `criticite` ∈ {`obligatoire`, `souhaitee`, `nice-to-have`} et `reference_ao` ;
- `scoring_implicite` (liste) le cas échéant.

Signaler tout écart avant de remettre le livrable.

## Garde-fous

- **Ne jamais inventer** — exigence, profil, niveau d'études, équivalence, localisation absents ⇒ `non_precise`/`null` + mention humaine si pertinent ; jamais fabriqués.
- **Aucun secret** dans les livrables, commentaires ou notifications.
- **Communication** — Agent ↔ Agent en JSON uniquement ; Agent ↔ Humain en Markdown uniquement (règle du conductor, non redéfinie ici).
- **Périmètre** — cette compétence porte le *comment* opératoire de l'analyse d'AO ; la gouvernance A2A, la validation humaine granulaire, la piste d'audit sur l'issue et le retour de délégation au Coordinateur sont définis une seule fois dans le conductor du workflow Matching et ne sont pas répétés ici.
