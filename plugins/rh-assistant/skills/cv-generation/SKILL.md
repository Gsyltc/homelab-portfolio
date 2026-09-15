---
name: cv-generation
description: >
    Génération et mise à jour d'un CV / d'une fiche collaborateur du workflow Matching à partir des données d'analyse extraites (ajout de compétences, mise à jour d'expérience, production d'une fiche présentable). Charger avant toute production ou modification de CV. Toute écriture n'intervient qu'après validation humaine explicite.
keywords: [generation cv, mise a jour cv, fiche cv, ajout competences, mise a jour experience, versionnage cv]
---

# Génération / mise à jour de CV

Cette compétence porte la production et la mise à jour d'un CV ou d'une fiche collaborateur à partir des **données déjà extraites** par la compétence [`cv-analyse`](../cv-analyse/SKILL.md) (JSON versionné + fiche Markdown du jour). Elle est chargée par l'agent **Gestionnaire CV** et alimente le stage de **mise à jour CV** (phase Clôture) du workflow Matching.

Elle n'invente **jamais** de contenu et n'écrit **qu'après validation humaine explicite**.

## Prérequis

- Une **analyse existante** du collaborateur (dernière version JSON à la racine de `cv/`). Si aucune analyse n'existe, exécuter d'abord `cv-analyse` sur un CV source.
- Une **demande explicite du Coordinateur** décrivant la modification attendue (ajout de compétences, mise à jour d'expérience, production d'une fiche pour livraison).
- La **validation humaine** de la mise à jour **avant** toute écriture (gate obligatoire).

## Types d'opérations

1. **Ajout / mise à jour de compétences** — enrichir `competences[]` avec `mois_experience` et `derniere_utilisation`. Ne jamais fabriquer une durée ou une date : info manquante ⇒ mention humaine.
2. **Mise à jour d'expérience** — ajouter/corriger des entrées `experience[]` (client, projet, rôle, `duree_mois`, `jours_personnes`, description).
3. **Production d'une fiche présentable** — générer un document Markdown lisible par l'humain à partir du JSON courant (livrable humain, aucun secret).

## Procédure

1. **Charger la dernière analyse** — lire la dernière version JSON du collaborateur (règle de sélection : [`../cv-analyse/SKILL.md`](../cv-analyse/SKILL.md), § Versionnage JSON). Ne jamais partir d'une version antérieure ni d'un source supprimé.
2. **Appliquer la modification demandée** sur une copie de travail, sans écraser l'historique.
3. **Présenter la modification à l'humain** (Markdown, diff clair avant/après) et **attendre la validation explicite**. Aucune écriture avant accord.
4. **Écrire les livrables versionnés** une fois validé :
   - nouveau JSON `<nom>-<prenom>-<AAAA-MM-JJ>.json` à la racine de `cv/` (date du jour), sans écraser l'historique ;
   - nouvelle fiche Markdown du jour `<AAAA-MM-JJ>-<nom>-<prenom>.md`, en **archivant** la fiche antérieure dans `cv/archives/` ;
   - `date_derniere_modification` = **toujours la date du jour**.
5. **Journaliser sur l'issue** la nature de la modification, la version JSON produite et la validation humaine obtenue (piste d'audit).

## Contrat de données

Le **schéma JSON** (compétences, expérience, études, `mifi`, `disponibilite`, `localisation`, langues), les conventions de nommage et la structure du répertoire `cv/` sont ceux définis dans [`../cv-analyse/SKILL.md`](../cv-analyse/SKILL.md) — s'y référer et ne pas diverger.

## Garde-fous

- **Validation humaine obligatoire** avant toute écriture d'un CV mis à jour ou d'une fiche produite.
- **Ne rien inventer** — une donnée absente (durée, date, ville, MIFI) se demande via mention humaine ; jamais fabriquée.
- **Versionnage** — ne jamais écraser une version JSON antérieure ni la fiche archivée ; l'historique est conservé.
- **Non-transmission des CV** — comme pour l'analyse, ne pas faire circuler les CV complets en A2A ; seuls le verdict d'éligibilité et la référence `analyse_json` remontent au coordinateur (voir [`../cv-analyse/SKILL.md`](../cv-analyse/SKILL.md), § Garde-fou).
- **Aucun secret** dans les livrables, commentaires ou notifications.

## Communication

- **Agent ↔ Agent** : JSON uniquement.
- **Agent ↔ Humain** : Markdown uniquement (diff avant/après pour la validation).
