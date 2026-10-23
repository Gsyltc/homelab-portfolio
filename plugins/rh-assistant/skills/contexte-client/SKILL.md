---
name: contexte-client
description: >
    Gestion du référentiel des contextes clients (sociétés) du workflow Matching : source unique du schéma et des règles de `${ROOT_DIRECTORY}/clients/<nom-client>.yaml` (1 fichier par client — nom, contexte de la société, mandats réalisés par la firme). Décrit la maintenance côté producteur (Gestionnaire CV, lors de l'analyse d'un CV long contenant un contexte client : création/enrichissement sans écrasement aveugle, dédoublonnage des mandats) et le contrat de lecture côté consommateur (Analyste RFP, pour l'évaluation d'expertise de firme ; cv-generation, pour le bloc « Contexte de l'organisation » du CV long). Charger avant toute création, mise à jour ou lecture d'un fichier clients/<nom-client>.yaml.
keywords: [contexte client, contextes clients, societe, referentiel clients, clients yaml, mandats, expertise firme, experience firme, capitalisation mandats, enrichissement contexte, dedoublonnage mandats, contexte organisation]
---

# Gestion des contextes clients (référentiel `clients/`)

Cette compétence est la **source unique** du **référentiel des contextes clients** du workflow Matching : elle définit le **schéma**, le **stockage/nommage**, les **règles de maintenance** (enrichissement sans écrasement aveugle, dédoublonnage) et le **contrat de lecture** de `${ROOT_DIRECTORY}/clients/<nom-client>.yaml`.

Le référentiel `clients/` est **transverse aux collaborateurs** et **partagé entre agents** : il capitalise, **un fichier par client**, le **contexte de la société** et les **mandats réalisés par la firme** (via ses collaborateurs). Il est **distinct** des analyses CV `collaborateurs/<nom-prenom>/cv/…` (mémoire par collaborateur).

- **Producteur** — l'agent **Gestionnaire CV** (compétence `cv-analyse`) **crée/complète** ce référentiel lors de l'analyse d'un **CV (long) contenant un contexte client**.
- **Consommateurs** — l'agent **Analyste RFP** (compétence `rfp-analyse`) le **lit** pour évaluer l'**expertise de firme** face à un AO ; la compétence `cv-generation` le **lit** pour renseigner le bloc « Contexte de l'organisation » du **CV long** (lecture seule).

> **Activation (condition impérative)** — côté Gestionnaire CV, cette compétence n'est **activée que si un contexte client est présent dans le CV analysé** (blocs « Contexte de l'organisation » / « Contexte du projet » d'un mandat). **Aucune activation, aucune écriture dans `clients/`** pour un CV qui **ne contient pas** de contexte client : la présence d'un contexte client dans le CV est le **seul déclencheur**. Le Gestionnaire CV vérifie d'abord cette présence ; en son absence, il **n'active pas** `contexte-client` et poursuit l'extraction normale du CV.

> **Enracinement des chemins** : tous les chemins sont **enracinés sur `${ROOT_DIRECTORY}`** (racine persistante du workspace) ; ne jamais utiliser un chemin absolu hors `${ROOT_DIRECTORY}` ni un relatif non enraciné. Écrire uniquement sous `${ROOT_DIRECTORY}/clients/`, jamais dans le workdir du run.

## Stockage et nommage

- **Emplacement** : `${ROOT_DIRECTORY}/clients/<nom-client>.yaml` — **un fichier par client**. Créer le répertoire `clients/` s'il est absent.
- **`<nom-client>`** = **slug** du nom du client (minuscules, tirets ; sans accents ni caractères spéciaux). Exemples : « Santé Québec » → `sante-quebec.yaml` ; « Réseau de Transport de la Capitale » → `reseau-de-transport-de-la-capitale.yaml`.
- **Un client = un fichier** : ne jamais créer de doublon pour un même client. Rapprocher les **variantes de libellé** d'un même client vers un seul fichier (le `slug` fait foi).

## Résolution d'un nom de mandat/client vers son fichier

Le **nom du client/mandat** tel qu'il apparaît dans un CV ou dans les données d'analyse comporte souvent des **variantes de libellé** (casse, accents, alias historiques entre parenthèses, ponctuation). Pour retrouver — ou créer — le fichier `clients/<slug>.yaml` correspondant **sans échec silencieux**, appliquer la **règle de normalisation → slug** suivante, dans l'ordre :

1. **Minuscules** — passer tout le libellé en minuscules.
2. **Retrait des alias entre parenthèses** — supprimer les segments entre parenthèses, en particulier les alias historiques du type « (ex …) » / « (anciennement …) ». Exemple : `Naval Group (ex DCNS)` → `naval group`. Si le choix du libellé canonique est ambigu (deux noms concurrents sans parenthèses), conserver le libellé principal et **poser une mention humaine** plutôt que de deviner.
3. **Suppression des accents et caractères diacritiques** — `é`→`e`, `è`→`e`, `à`→`a`, `ô`→`o`, `ç`→`c`, etc.
4. **Remplacement des séparateurs par des tirets** — espaces, apostrophes, `&`, `/`, points et autres caractères non alphanumériques → `-` ; réduire les tirets consécutifs à un seul et retirer les tirets de début/fin.

Exemples : `Naval Group (ex DCNS)` → `naval-group` → `clients/naval-group.yaml` ; `Marine Nationale` → `marine-nationale` → `clients/marine-nationale.yaml` ; `Alithya` → `alithya` → `clients/alithya.yaml` ; `Santé Québec` → `sante-quebec` ; `Réseau de Transport de la Capitale` → `reseau-de-transport-de-la-capitale`.

> **Repli explicite si aucun fichier ne correspond** : si, après normalisation, **aucun** `clients/<slug>.yaml` n'existe, ne pas échouer en silence.
> - **Côté producteur** (Gestionnaire CV, lors d'une maintenance déclenchée par un CV contenant un contexte client) : **créer** le fichier `clients/<slug>.yaml` (cf. § Maintenance).
> - **Côté consommateur** (lecture seule — `cv-generation`, `rfp-analyse`) : traiter l'information comme **indisponible** (pour `cv-generation` : marqueur « à compléter » + signalement humain ; pour `rfp-analyse` : critère `non_couvert`/`indeterminable`), **sans** fabriquer ni créer de fichier.
>
> Le `slug` ainsi calculé est le **seul identifiant de rapprochement** : il doit être **cohérent** entre la création (producteur) et la lecture (consommateurs) pour éviter qu'un même client donne deux fichiers ou qu'une correspondance échoue silencieusement.

## Schéma `clients/<nom-client>.yaml`

```yaml
client: <nom du client / de la société>
slug: <nom-client slugifié — cohérent avec le nom de fichier>
contexte: <contexte du client (secteur, mission, taille, enjeux) — complété/enrichi au fil des CV, jamais écrasé aveuglément>
date_derniere_modification: "<AAAA-MM-JJ — date du jour de la dernière mise à jour>"
sources:
  - {collaborateur: <prénom nom>, cv_analyse_yaml: "<chemin du YAML d'analyse ayant alimenté ce fichier>", date: "<AAAA-MM-JJ>"}
mandats:
  - collaborateur: <prénom nom du collaborateur ayant réalisé le mandat>
    role: <rôle/fonction du collaborateur sur le mandat>
    projet: <nom du projet si disponible, sinon null>
    date_debut: "<AAAA-MM ou null>"
    date_fin: "<AAAA-MM | present | null>"
    jours_personnes: <nombre de jours-personnes du mandat, ou null>
    contexte_projet: <contexte du projet / du mandat>
    taches: ["<tâche réalisée>"]
    technologies: ["<technologie utilisée>"]
```

### Champs et règles

- **`client`** : nom lisible du client. **`slug`** : version slugifiée, **cohérente avec le nom de fichier** `<nom-client>.yaml`.
- **`contexte`** (contexte du client) : description de la société (secteur, mission, taille, enjeux).
- **`mandats[]`** : un objet par mandat réalisé par un collaborateur chez ce client. Chaque mandat porte **obligatoirement** :
  - **`collaborateur`** — prénom nom du collaborateur ayant réalisé le mandat ;
  - **`role`** — rôle/fonction tenu ;
  - **`projet`** — nom du projet **si disponible**, sinon `null` (ne rien inventer) ;
  - **`date_debut` / `date_fin`** — dates du mandat (`AAAA-MM` ; `present` si en cours ; `null` si absentes du CV) ;
  - **`jours_personnes`** — envergure en jours-personnes (`null` si absente) ;
  - **`contexte_projet`** — contexte du projet/mandat ;
  - **`taches`** — liste des tâches réalisées (`[]` si non détaillées) ;
  - **`technologies`** — liste des technologies utilisées (`[]` si non mentionnées).
- **`sources[]`** : trace des CV (analyses YAML) ayant alimenté le fichier — piste d'audit du référentiel, **sans transporter le CV**.
- **`date_derniere_modification`** = **toujours la date du jour** de la mise à jour.

## Maintenance (producteur — Gestionnaire CV)

Déclenchée **uniquement** lors de l'analyse d'un **CV (long) contenant un contexte client** (blocs « Contexte de l'organisation » / « Contexte du projet » d'un mandat). Un CV **sans** contexte client ne déclenche **aucune** écriture dans `clients/`.

1. **Repérer les sociétés clientes** décrites dans le CV (contexte de l'organisation) et leurs **mandats**.
2. Pour **chaque** société : calculer le `slug` et ouvrir `${ROOT_DIRECTORY}/clients/<slug>.yaml` — le **créer** s'il n'existe pas, sinon le charger.
3. **Enrichissement, jamais d'écrasement aveugle** :
   - **`contexte`** : **compléter** avec l'information pertinente **non redondante** apportée par le CV, **sans effacer** l'existant. Ne pas dupliquer une information déjà présente.
   - **`mandats[]`** : **dédoublonner** — un mandat **déjà présent** (même `collaborateur` + même `projet`/période) est **mis à jour/complété** ; un mandat **nouveau** est **ajouté**.
4. Renseigner **`date_derniere_modification`** = date du jour et **ajouter une entrée `sources[]`** (collaborateur + chemin du YAML d'analyse + date).
5. **Écrire** le fichier en **YAML valide** sous `${ROOT_DIRECTORY}/clients/` (jamais dans le workdir du run), puis **vérifier** son existence après écriture.
6. **Ne rien inventer** : une donnée absente du CV reste `null`/`[]` ; poser une **mention humaine** si une information ambiguë mérite confirmation. Aucun secret dans le référentiel.

> **Contrôle** : après maintenance, vérifier que `${ROOT_DIRECTORY}/clients/<slug>.yaml` a été **créé ou complété** (contexte enrichi sans écrasement, mandats ajoutés/fusionnés, `date_derniere_modification` = date du jour, `sources[]` mis à jour), en **JSON valide**, sous le `${ROOT_DIRECTORY}` absolu. Journaliser sur l'issue les fichiers `clients/` créés/mis à jour (piste d'audit).

## Contrat de lecture (consommateurs)

### Analyste RFP — évaluation d'expertise de firme

Lorsqu'un AO exige une **expertise/expérience de firme** (mandats similaires, secteur, technologies, contexte comparables), l'Analyste RFP **lit** le référentiel `${ROOT_DIRECTORY}/clients/*.yaml` pour statuer si la firme dispose de l'expérience requise, et produit l'objet `expertise_firme` (schéma, verdict et **gate humaine légère non bloquante** définis dans la compétence `rfp-analyse`).

- La **couverture** de chaque critère attendu doit être **appuyée sur des preuves factuelles** tirées de `clients/*.yaml` (client, chemin du fichier, mandats pertinents). **Ne rien inventer** : un référentiel **vide/insuffisant** ⇒ critère `non_couvert`/`indeterminable`, **jamais** une expertise supposée.
- Lecture **seule** : l'Analyste RFP **ne modifie pas** le référentiel `clients/` (sa maintenance est réservée au Gestionnaire CV).

### cv-generation — bloc « Contexte de l'organisation » du CV long

Lors de la génération d'un **CV long**, le bloc « Contexte de l'organisation » de chaque mandat — matérialisé dans le gabarit DOCX par le jeton `{{CONTEXTE_ORGANISATION}}` — est renseigné à partir du `contexte` du client correspondant dans `clients/<slug>.yaml` s'il est disponible (voir la compétence `cv-generation`, § Contrat de remplissage du jeton). Le rapprochement du nom de mandat vers son fichier suit la **règle de résolution nom → fichier** ci-dessus (§ Résolution d'un nom de mandat/client vers son fichier). Lecture **seule**, **ne rien inventer** (contexte indisponible, ou aucun fichier après résolution ⇒ marqueur « à compléter » + signalement humain), sans modifier le référentiel `clients/` ni la charte du gabarit.

## Garde-fous

- **Un fichier par client**, nommé par le `slug` du client ; jamais de doublon.
- **Enrichir, jamais écraser aveuglément** le `contexte` ; **dédoublonner** les mandats.
- **Ne rien inventer** — donnée absente ⇒ `null`/`[]` (+ mention humaine si utile).
- **Maintenance réservée au Gestionnaire CV** ; les autres agents sont en **lecture seule**.
- **Aucun secret** dans le référentiel ; chemins **enracinés sur `${ROOT_DIRECTORY}`** ; **YAML valide**.
- **Piste d'audit** sur l'issue (fichiers `clients/` créés/mis à jour, sources).
