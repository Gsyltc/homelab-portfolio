---
name: cv-generation
description: >
    Génération et mise à jour d'un CV livrable du workflow Matching **au format DOCX**, à partir des données d'analyse extraites (JSON versionné) et des **gabarits fournis** (CV long, CV court, format client spécifique). Charger avant toute production ou modification de CV. Le CV livrable est un DOCX produit à partir d'un gabarit fourni — jamais inventé — et toute écriture n'intervient qu'après validation humaine explicite.
keywords: [generation cv, mise a jour cv, cv docx, gabarit cv, cv long, cv court, format client, ajout competences, mise a jour experience, versionnage cv]
---

# Génération / mise à jour de CV (DOCX à partir des gabarits fournis)

Cette compétence porte la production et la mise à jour d'un **CV livrable au format DOCX** à partir des **données déjà extraites** par la compétence [`cv-analyse`](../cv-analyse/SKILL.md) (JSON versionné + fiche d'analyse Markdown du jour) et des **gabarits DOCX fournis par l'humain**. Elle est chargée par l'agent **Gestionnaire CV** et alimente le stage de **mise à jour CV** (phase Clôture) du workflow Matching.

Elle n'invente **jamais** de contenu ni de gabarit, et n'écrit **qu'après validation humaine explicite**.

## Distinction fondamentale — fiche d'analyse vs CV livrable

Deux artefacts distincts ne doivent **jamais** être confondus :

| Artefact | Format | Rôle | Producteur |
| --- | --- | --- | --- |
| **Fiche d'analyse** | **Markdown** (`<AAAA-MM-JJ>-<nom>-<prenom>.md`) + JSON versionné | **Mémoire interne persistante** du CV (données structurées, MIFI, localisation, disponibilité) — jamais un livrable client | `cv-analyse` (stage `extraction-cv`) |
| **CV livrable** | **DOCX** | **Document présentable** remis à l'humain / au client, produit **à partir d'un gabarit fourni** | `cv-generation` (stage `mise-a-jour-cv`) |

La fiche d'analyse Markdown et le JSON restent la **source de données** (mémoire) ; le **CV livrable est toujours un DOCX** rempli depuis un gabarit fourni. On ne livre jamais la fiche d'analyse Markdown comme CV.

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

## Prérequis

- Une **analyse existante** du collaborateur (dernière version JSON à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`). Si aucune analyse n'existe, exécuter d'abord `cv-analyse` sur un CV source.
- Le **gabarit DOCX fourni** correspondant au type demandé, présent dans `${ROOT_DIRECTORY}/gabarits/cv/` (sinon halt-and-ask).
- Une **demande explicite du Coordinateur** décrivant la modification/production attendue (type de CV, ajout de compétences, mise à jour d'expérience, format client).
- La **validation humaine** de la production/mise à jour **avant** toute écriture (gate obligatoire).

## Types d'opérations

1. **Ajout / mise à jour de compétences** — enrichir `competences[]` (données) avec `mois_experience` et `derniere_utilisation`. Ne jamais fabriquer une durée ou une date : info manquante ⇒ mention humaine.
2. **Mise à jour d'expérience** — ajouter/corriger des entrées `experience[]` (client, projet, rôle, `duree_mois`, `jours_personnes`, description).
3. **Production d'un CV livrable DOCX** — générer le document **DOCX** à partir du **gabarit fourni** (CV long / CV court / format client) et des données du JSON courant (livrable humain, aucun secret).

## Procédure

1. **Charger la dernière analyse** — lire la dernière version JSON du collaborateur (règle de sélection : [`../cv-analyse/SKILL.md`](../cv-analyse/SKILL.md), § Versionnage JSON). Ne jamais partir d'une version antérieure ni d'un source supprimé.
2. **Sélectionner le gabarit** — déterminer le type demandé (CV long / CV court / format client) et **charger le gabarit fourni** depuis `${ROOT_DIRECTORY}/gabarits/cv/`. **Absent ⇒ halt-and-ask** (mention humaine, ne rien inventer).
3. **Appliquer la modification / le remplissage** sur une copie de travail, en injectant les données du JSON dans les emplacements prévus par le gabarit, sans écraser l'historique et sans altérer la charte du gabarit.
4. **Présenter la production à l'humain** (Markdown pour la conversation : diff clair avant/après des données injectées + type de gabarit utilisé) et **attendre la validation explicite**. Aucune écriture avant accord.
5. **Écrire les livrables versionnés** une fois validé :
   - **CV livrable DOCX** `<nom>-<prenom>-<type-gabarit>-<AAAA-MM-JJ>.docx` (ex. `dupont-jean-cv-long-2026-09-15.docx`) à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`, sans écraser l'historique ;
   - mise à jour des **données** si modifiées : nouveau JSON `<nom>-<prenom>-<AAAA-MM-JJ>.json` (date du jour, sans écraser l'historique) et fiche d'analyse Markdown du jour `<AAAA-MM-JJ>-<nom>-<prenom>.md`, en **archivant** la fiche antérieure dans `cv/archives/` ;
   - `date_derniere_modification` = **toujours la date du jour**.
6. **Journaliser sur l'issue** la nature de la modification, le **type de gabarit** et le fichier DOCX produit, la version JSON produite et la validation humaine obtenue (piste d'audit).

## Enracinement des chemins

Tous les chemins relatifs de cette compétence sont **enracinés sur `${ROOT_DIRECTORY}`** (répertoire de travail du workspace) : gabarits dans `${ROOT_DIRECTORY}/gabarits/cv/`, livrables et analyses dans `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`. Ne jamais utiliser de chemin absolu hors `${ROOT_DIRECTORY}` ni un chemin relatif non enraciné.

## Contrat de données

Le **schéma JSON** (compétences, expérience, études, `mifi`, `disponibilite`, `localisation`, langues), les conventions de nommage et la structure du répertoire `cv/` sont ceux définis dans [`../cv-analyse/SKILL.md`](../cv-analyse/SKILL.md) — s'y référer et ne pas diverger.

## Garde-fous

- **Livrable au format DOCX depuis un gabarit fourni** — le CV livrable est **toujours un DOCX** produit à partir d'un des gabarits fournis (CV long / CV court / format client). **Ne jamais inventer** de gabarit ni de mise en page ; gabarit absent ⇒ halt-and-ask.
- **Validation humaine obligatoire** avant toute écriture d'un CV produit/mis à jour.
- **Ne rien inventer** — une donnée absente (durée, date, ville, MIFI) se demande via mention humaine ; jamais fabriquée.
- **Versionnage** — ne jamais écraser une version JSON antérieure, un DOCX antérieur ni la fiche archivée ; l'historique est conservé.
- **Non-transmission des CV** — comme pour l'analyse, ne pas faire circuler les CV complets en A2A ; seuls le verdict d'éligibilité et la référence `analyse_json` remontent au coordinateur (voir [`../cv-analyse/SKILL.md`](../cv-analyse/SKILL.md), § Garde-fou).
- **Aucun secret** dans les livrables, commentaires ou notifications.

## Communication

- **Agent ↔ Agent** : JSON uniquement.
- **Agent ↔ Humain** : Markdown uniquement (diff avant/après pour la validation). Le **CV livrable** transmis à l'humain est un **DOCX** (pièce jointe / fichier), distinct de la conversation Markdown.
