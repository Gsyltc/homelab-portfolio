---
name: cv-generation
description: >
    Génération et mise à jour d'un CV livrable du workflow Matching, **au format DOCX par défaut** (à partir des gabarits fournis : CV long, CV court, format client spécifique) — le **format Markdown reste possible uniquement sur demande explicite de l'humain**. Production à partir des données d'analyse extraites (JSON versionné). Charger avant toute production ou modification de CV. Un CV DOCX est produit à partir d'un gabarit fourni — jamais inventé — et toute écriture n'intervient qu'après validation humaine explicite.
keywords: [generation cv, mise a jour cv, cv docx, cv markdown, gabarit cv, cv long, cv court, format client, ajout competences, mise a jour experience, versionnage cv]
---

# Génération / mise à jour de CV (DOCX à partir des gabarits fournis)

Cette compétence porte la production et la mise à jour d'un **CV livrable** à partir des **données déjà extraites** par la compétence `cv-analyse` (JSON versionné + fiche d'analyse Markdown du jour). Le format **par défaut est le DOCX** (rempli depuis un **gabarit fourni** : CV long / CV court / format client spécifique) ; un **CV livrable au format Markdown** reste possible **uniquement sur demande explicite de l'humain**. Elle est chargée par l'agent **Gestionnaire CV** et alimente le stage de **mise à jour CV** (phase Clôture) du workflow Matching.

Elle n'invente **jamais** de contenu ni de gabarit, et n'écrit **qu'après validation humaine explicite**.

## Distinction fondamentale — fiche d'analyse vs CV livrable

Deux artefacts distincts ne doivent **jamais** être confondus :

| Artefact | Format | Rôle | Producteur |
| --- | --- | --- | --- |
| **Fiche d'analyse** | **Markdown** (`<AAAA-MM-JJ>-<nom>-<prenom>.md`) + JSON versionné | **Mémoire interne persistante** du CV (données structurées, MIFI, localisation, disponibilité) — jamais un livrable client | `cv-analyse` (stage `extraction-cv`) |
| **CV livrable** | **DOCX par défaut** (depuis un gabarit fourni) · **Markdown sur demande explicite** de l'humain | **Document présentable** remis à l'humain / au client | `cv-generation` (stage `mise-a-jour-cv`) |

La fiche d'analyse Markdown et le JSON restent la **source de données** (mémoire) ; le **CV livrable est un DOCX par défaut** rempli depuis un gabarit fourni. On ne livre jamais la fiche d'analyse Markdown telle quelle comme CV.

## Format du CV livrable (DOCX par défaut ; Markdown sur demande explicite)

- **Par défaut : DOCX** — produit à partir d'un des **gabarits fournis** (CV long / CV court / format client spécifique). C'est le format retenu en l'absence de demande contraire.
- **Markdown : uniquement sur demande explicite de l'humain** — lorsque l'humain **demande explicitement** un CV livrable au format Markdown, produire un **document Markdown présentable** (distinct de la fiche d'analyse : c'est un livrable mis en forme pour l'humain, pas la mémoire interne) à partir des données du JSON courant, nommé `<nom>-<prenom>-cv-<AAAA-MM-JJ>.md` à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv` (sans écraser l'historique ni la fiche d'analyse). Le Markdown livrable **ne s'appuie pas sur un gabarit DOCX** ; il n'est produit **que** sur demande explicite — jamais par défaut, jamais en substitution silencieuse d'un gabarit DOCX manquant (gabarit DOCX manquant ⇒ halt-and-ask, pas de repli Markdown automatique).

## Gabarits fournis (jamais inventés)

La production DOCX s'appuie **exclusivement** sur les **gabarits fournis par l'humain**. Trois types de gabarits sont pris en charge :

| Type de gabarit | Usage | Nom de fichier attendu |
| --- | --- | --- |
| **CV long** | CV détaillé complet | `cv-long.docx` |
| **CV court** | CV synthétique / résumé | `cv-court.docx` |
| **Format client spécifique** | Gabarit imposé par un client (souvent lié à un AO) | `format-client-<client>.docx` |

- **Emplacement des gabarits** : `${ROOT_DIRECTORY}/gabarits/cv/` (racine de travail du workspace). Ce répertoire est la **source unique** des gabarits ; ils sont **fournis par l'humain** (déposés dans ce répertoire ou attachés à l'issue via `multica attachment`).
- **Ne jamais inventer un gabarit** : si le gabarit demandé est **absent**, **halt-and-ask** — poser une **mention humaine** demandant le gabarit (ou son emplacement) et **attendre** ; ne pas fabriquer une mise en page de substitution.
- **Choix du gabarit** : sauf indication contraire de l'humain, produire le **CV long** par défaut. Pour un livrable destiné à un client précis (ex. réponse à un AO), utiliser le **format client spécifique** si le client l'impose (`format-client-<client>.docx`) ; sinon **demander** lequel des trois types produire.
- **Respect strict du gabarit** : n'écrire que dans les emplacements/champs prévus par le gabarit (mise en page, styles, sections, ordre). Ne pas altérer la charte du gabarit.

## Contexte client dans le CV long (bloc « Contexte de l'organisation »)

Le **CV long** comporte, pour chaque mandat, un bloc **« Contexte de l'organisation »** décrivant la société cliente. Ce contexte est capitalisé dans le **référentiel des contextes clients** `${ROOT_DIRECTORY}/clients/<nom-client>.json` — dont le **schéma et le contrat de lecture** sont définis dans la compétence dédiée `contexte-client` (source unique ; maintenu par le Gestionnaire CV via la compétence `cv-analyse`). Lors de la génération d'un **CV long**, renseigner le bloc « Contexte de l'organisation » de chaque mandat à partir du `contexte` du client correspondant dans `clients/<nom-client>.json` s'il est disponible ; à défaut, utiliser le contexte présent dans les données d'analyse du collaborateur. **Ne rien inventer** : contexte client indisponible ⇒ laisser le marqueur « à compléter » (jamais fabriqué). Cette réutilisation est en **lecture seule** : elle ne modifie **pas** le référentiel `clients/` ni la charte du gabarit.

## Prérequis

- Une **analyse existante** du collaborateur (dernière version JSON à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`). Si aucune analyse n'existe, exécuter d'abord `cv-analyse` sur un CV source.
- **En DOCX (défaut)** : le **gabarit DOCX fourni** correspondant au type demandé, présent dans `${ROOT_DIRECTORY}/gabarits/cv/` (sinon halt-and-ask). Sans objet pour un CV Markdown demandé explicitement (pas de gabarit).
- Une **demande explicite du Coordinateur** décrivant la modification/production attendue (type de CV, ajout de compétences, mise à jour d'expérience, format client).
- La **validation humaine** de la production/mise à jour **avant** toute écriture (gate obligatoire).

## Types d'opérations

1. **Ajout / mise à jour de compétences** — enrichir `competences[]` (données) avec `mois_experience` et `derniere_utilisation`. Ne jamais fabriquer une durée ou une date : info manquante ⇒ mention humaine.
2. **Mise à jour d'expérience** — ajouter/corriger des entrées `experience[]` (client, rôle, `date_debut`, `date_fin`, `duree_mois`, `jours_personnes`, description) et le **détail de leurs projets** `experience[].projets[]`. Une expérience peut porter **un ou plusieurs projets** ; chaque projet porte `nom`, `date_debut`, `date_fin` (`AAAA-MM`, `present` si en cours) et `responsabilites` (liste). Les dates de l'expérience restent indépendantes de celles des projets. Ne jamais fabriquer un nom, une date ou une responsabilité de projet : info manquante ⇒ mention humaine.
3. **Production d'un CV livrable** — **par défaut au format DOCX** à partir du **gabarit fourni** (CV long / CV court / format client) et des données du JSON courant ; **au format Markdown uniquement si l'humain le demande explicitement** (livrable humain, aucun secret).
4. **Mise à jour des études et certifications** — enrichir/corriger `etudes[]` (un collaborateur peut porter **plusieurs diplômes** : `niveau`, `formation`, `etablissement`, `annee_obtention`) et, **séparément**, `certifications[]` (plusieurs certifications : `nom`, `organisme`, `annee_obtention`, `date_expiration`, `reference`). Études et certifications restent **deux listes distinctes**, jamais fusionnées ; dans le CV livrable, les rendre en **deux sections séparées** (« Formation / Études » et « Certifications ») lorsque le gabarit le prévoit. Ne jamais fabriquer un diplôme, une certification, une année ou un organisme : donnée absente ⇒ mention humaine.

## Procédure

1. **Charger la dernière analyse** — lire la dernière version JSON du collaborateur (règle de sélection : la compétence `cv-analyse`, § Versionnage JSON). Ne jamais partir d'une version antérieure ni d'un source supprimé.
2. **Déterminer le format et le gabarit** — **par défaut : DOCX** → sélectionner le type demandé (CV long / CV court / format client) et **charger le gabarit fourni** depuis `${ROOT_DIRECTORY}/gabarits/cv/` (**absent ⇒ halt-and-ask**, mention humaine, ne rien inventer, **pas de repli Markdown automatique**). **Si l'humain a explicitement demandé un CV Markdown** → produire le livrable Markdown depuis les données du JSON, sans gabarit DOCX.
3. **Appliquer la modification / le remplissage** sur une copie de travail : en DOCX, injecter les données du JSON dans les emplacements prévus par le gabarit (sans altérer sa charte) ; en Markdown (sur demande), mettre en forme les données du JSON en un document présentable — sans écraser l'historique.
4. **Présenter la production à l'humain** (Markdown pour la conversation : diff clair avant/après des données injectées + format et, en DOCX, type de gabarit utilisé) et **attendre la validation explicite**. Aucune écriture avant accord.
5. **Écrire les livrables versionnés** une fois validé :
   - **CV livrable** — en **DOCX** (défaut) : `<nom>-<prenom>-<type-gabarit>-<AAAA-MM-JJ>.docx` (ex. `dupont-jean-cv-long-2026-09-15.docx`) ; en **Markdown** (sur demande explicite) : `<nom>-<prenom>-cv-<AAAA-MM-JJ>.md` — à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`, sans écraser l'historique ni la fiche d'analyse ;
   - mise à jour des **données** si modifiées : nouveau JSON `<nom>-<prenom>-<AAAA-MM-JJ>.json` (date du jour, sans écraser l'historique) et fiche d'analyse Markdown du jour `<AAAA-MM-JJ>-<nom>-<prenom>.md`, en **archivant** la fiche antérieure dans `cv/archives/` ;
   - `date_derniere_modification` = **toujours la date du jour**.
6. **Journaliser sur l'issue** la nature de la modification, le **format** (DOCX/Markdown) et, en DOCX, le **type de gabarit**, le fichier produit, la version JSON produite et la validation humaine obtenue (piste d'audit).

## Enracinement des chemins

Tous les chemins relatifs de cette compétence sont **enracinés sur `${ROOT_DIRECTORY}`** (répertoire de travail du workspace) : gabarits dans `${ROOT_DIRECTORY}/gabarits/cv/`, livrables et analyses dans `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`. Ne jamais utiliser de chemin absolu hors `${ROOT_DIRECTORY}` ni un chemin relatif non enraciné.

## Contrat de données

Le **schéma JSON** (compétences, expérience, `etudes[]` — une ou plusieurs études, `certifications[]` — liste **distincte** des études, `mifi`, `disponibilite`, `localisation`, langues), les conventions de nommage et la structure du répertoire `cv/` sont ceux définis dans la compétence `cv-analyse` — s'y référer et ne pas diverger.

## Garde-fous

- **Format du livrable : DOCX par défaut, Markdown sur demande explicite** — par défaut le CV livrable est un **DOCX** produit à partir d'un des gabarits fournis (CV long / CV court / format client). Le **Markdown** n'est produit **que** sur **demande explicite de l'humain**, jamais par défaut ni comme repli d'un gabarit DOCX manquant. **Ne jamais inventer** de gabarit ni de mise en page ; gabarit DOCX absent ⇒ halt-and-ask.
- **Validation humaine obligatoire** avant toute écriture d'un CV produit/mis à jour.
- **Ne rien inventer** — une donnée absente (durée, date, ville, MIFI) se demande via mention humaine ; jamais fabriquée.
- **Versionnage** — ne jamais écraser une version JSON antérieure, un CV livrable antérieur (DOCX ou Markdown) ni la fiche archivée ; l'historique est conservé.
- **Non-transmission des CV** — comme pour l'analyse, ne pas faire circuler les CV complets en A2A ; seuls le verdict d'éligibilité et la référence `analyse_json` remontent au coordinateur (voir la compétence `cv-analyse`, § Garde-fou).
- **Aucun secret** dans les livrables, commentaires ou notifications.

## Communication

- **Agent ↔ Agent** : JSON uniquement.
- **Agent ↔ Humain** : Markdown uniquement (diff avant/après pour la validation). Le **CV livrable** transmis à l'humain est un **DOCX** par défaut (pièce jointe / fichier), ou un **CV Markdown** si l'humain l'a explicitement demandé — dans les deux cas, distinct de la conversation Markdown.
