---
name: cv-generation
description: >
    Génération et mise à jour d'un CV livrable du workflow Matching, **au format DOCX par défaut** (à partir des gabarits fournis : CV long, CV court, format client spécifique) — le **format Markdown reste possible uniquement sur demande explicite de l'humain**. Production à partir des données d'analyse extraites (YAML versionné). Charger avant toute production ou modification de CV. Un CV DOCX est produit à partir d'un gabarit fourni — jamais inventé — et toute écriture n'intervient qu'après validation humaine explicite.
keywords: [generation cv, mise a jour cv, cv docx, cv markdown, gabarit cv, cv long, cv court, format client, ajout competences, mise a jour experience, versionnage cv, donnees cv yaml]
---

# Génération / mise à jour de CV (DOCX à partir des gabarits fournis)

Cette compétence porte la production et la mise à jour d'un **CV livrable** à partir des **données déjà extraites** par la compétence `cv-analyse` (YAML versionné + fiche d'analyse Markdown du jour). Le format **par défaut est le DOCX** (rempli depuis un **gabarit fourni** : CV long / CV court / format client spécifique) ; un **CV livrable au format Markdown** reste possible **uniquement sur demande explicite de l'humain**. Elle est chargée par l'agent **Gestionnaire CV** et alimente le stage de **mise à jour CV** (phase Clôture) du workflow Matching.

Elle n'invente **jamais** de contenu ni de gabarit, et n'écrit **qu'après validation humaine explicite**.

## Distinction fondamentale — fiche d'analyse vs CV livrable

Deux artefacts distincts ne doivent **jamais** être confondus :

| Artefact | Format | Rôle | Producteur |
| --- | --- | --- | --- |
| **Fiche d'analyse** | **Markdown** (`<YYYY-mm-dd>-<nom>.md`) + YAML (`<YYYY-mm-dd>-<nom>.yaml`) | **Mémoire interne persistante** du CV (données structurées, MIFI, localisation, disponibilité) — jamais un livrable client | `cv-analyse` (stage `extraction-cv`) |
| **CV livrable** | **DOCX par défaut** (depuis un gabarit fourni) · **Markdown sur demande explicite** de l'humain | **Document présentable** remis à l'humain / au client | `cv-generation` (stage `mise-a-jour-cv`) |

La fiche d'analyse Markdown et le YAML restent la **source de données** (mémoire) ; le **CV livrable est un DOCX par défaut** rempli depuis un gabarit fourni. On ne livre jamais la fiche d'analyse Markdown telle quelle comme CV.

## Format du CV livrable (DOCX par défaut ; Markdown sur demande explicite)

- **Par défaut : DOCX** — produit à partir d'un des **gabarits fournis** (CV long / CV court / format client spécifique). C'est le format retenu en l'absence de demande contraire.
- **Markdown : uniquement sur demande explicite de l'humain** — lorsque l'humain **demande explicitement** un CV livrable au format Markdown, produire un **document Markdown présentable** (distinct de la fiche d'analyse : c'est un livrable mis en forme pour l'humain, pas la mémoire interne) à partir des données du YAML courant, nommé `<YYYY-mm-dd>-<nom>-cv.md` à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv` (sans écraser l'historique ni la fiche d'analyse). Le Markdown livrable **ne s'appuie pas sur un gabarit DOCX** ; il n'est produit **que** sur demande explicite — jamais par défaut, jamais en substitution silencieuse d'un gabarit DOCX manquant (gabarit DOCX manquant ⇒ halt-and-ask, pas de repli Markdown automatique).

## Règle d'or — aucune note de génération / méta-production dans le CV livrable

Cet invariant est défini **une seule fois** dans le protocole de gouvernance — [`governance-security.md`, invariant 7](../../../../matching-cv-ao/common/protocols/governance-security.md#aucune-note-de-génération--méta-production-dans-les-livrables-source-unique) (ADR-0040, EXPE-121) — et **ne doit pas être redupliqué ici** : s'y référer pour le périmètre et les proscriptions.

Appliqué au **CV livrable** (DOCX par défaut, Markdown sur demande) : le CV ne contient **que l'information métier du candidat** ; aucune note de génération / méta-production (« généré par l'agent / l'IA », résumé de ce que l'agent a fait, liens/identifiants `mention://…` ou de tickets, SHA de commit, horodatages, descripteur d'outil, ligne de version-process). « Ne rien inventer », le respect des gabarits et la validation humaine restent des disciplines de production — jamais un texte écrit dans le CV. La **traçabilité** (format, gabarit, version YAML, validation) se **journalise sur l'issue** et dans la mémoire interne (`cv-analyse`), **jamais dans le CV**.

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

Le **CV long** comporte, pour chaque mandat, un bloc **« Contexte de l'organisation »** décrivant la société cliente. Ce contexte est capitalisé dans le **référentiel des contextes clients** `${ROOT_DIRECTORY}/clients/<nom-client>.yaml` — dont le **schéma et le contrat de lecture** sont définis dans la compétence dédiée `contexte-client` (source unique ; maintenu par le Gestionnaire CV via la compétence `cv-analyse`). Lors de la génération d'un **CV long**, renseigner le bloc « Contexte de l'organisation » de chaque mandat à partir du `contexte` du client correspondant dans `clients/<nom-client>.yaml` s'il est disponible ; à défaut, utiliser le contexte présent dans les données d'analyse du collaborateur. **Ne rien inventer** : contexte client indisponible ⇒ laisser le marqueur « à compléter » (jamais fabriqué). Cette réutilisation est en **lecture seule** : elle ne modifie **pas** le référentiel `clients/` ni la charte du gabarit.

### Contrat de remplissage du jeton `{{CONTEXTE_ORGANISATION}}`

Dans les gabarits DOCX de CV long, le bloc « Contexte de l'organisation » de chaque mandat est matérialisé par le **jeton de gabarit** `{{CONTEXTE_ORGANISATION}}` (marqueur de substitution placé par le gabarit, typiquement juste après le libellé « Contexte de l'organisation »). Le remplissage de ce bloc consiste à **substituer** ce jeton par le texte de contexte résolu. Ce contrat est **obligatoire** et s'applique **mandat par mandat** :

1. **Résoudre le client du mandat vers son fichier référentiel** — à partir du **nom du mandat/client** tel qu'il figure dans les données d'analyse du collaborateur, calculer le fichier `clients/<slug>.yaml` attendu en appliquant la **règle de résolution nom → fichier** définie dans la compétence `contexte-client` (§ Résolution d'un nom de mandat/client vers son fichier). Cette règle normalise le libellé (minuscules, suppression des accents, retrait des alias entre parenthèses du type « (ex …) », espaces → tirets) avant de calculer le `slug`.
2. **Lire le `contexte` du client** dans `clients/<slug>.yaml` si le fichier existe (lecture seule).
3. **Substituer le jeton** :
   - **Contexte disponible** (dans `clients/<slug>.yaml` ou, à défaut, dans les données d'analyse du collaborateur) ⇒ remplacer `{{CONTEXTE_ORGANISATION}}` par ce texte.
   - **Contexte indisponible** (aucun fichier ne correspond après résolution, ou champ `contexte` vide) ⇒ remplacer `{{CONTEXTE_ORGANISATION}}` par le marqueur **« à compléter »** (jamais un contexte fabriqué) et **signaler le mandat concerné à l'humain** (mention).
4. **Jamais de jeton résiduel** — après substitution, **aucun** `{{CONTEXTE_ORGANISATION}}` (ni aucun autre `{{…}}`) ne doit subsister dans le DOCX livré (voir la procédure, étape de vérification post-génération).

> **Correspondance silencieuse interdite** : si la résolution nom → fichier n'aboutit à **aucun** fichier `clients/<slug>.yaml`, ne pas laisser le bloc vide ou le jeton en place sans trace — appliquer le repli « à compléter » **et** signaler le mandat à l'humain, afin que l'absence soit visible et non une omission silencieuse.

### Distinction des niveaux — contexte d'organisation (mandat) vs contexte de projet (projet)

Le CV distingue **deux niveaux** qu'il ne faut **jamais confondre** lors du remplissage des blocs de contexte :

| Niveau | Donnée source | Bloc du CV long | Cardinalité |
| --- | --- | --- | --- |
| **Mandat** = une entrée `experience[]` rattachée à **un client** | champ **`contexte`** (niveau racine) de `clients/<slug>.yaml` — contexte de la **société** | bloc **« Contexte de l'organisation »** (`{{CONTEXTE_ORGANISATION}}`) | **un mandat = un client = un seul bloc** « Contexte de l'organisation » |
| **Projet** = une entrée `experience[].projets[]` (un mandat peut en porter **plusieurs**) | champ **`contexte_projet`** (porté par `mandats[]` dans `clients/<slug>.yaml`, et au niveau projet côté données CV) | contexte au **niveau projet** | **un mandat → 0..n projets**, chacun avec son **propre** `contexte_projet` |

- **Ne jamais substituer l'un à l'autre** : le `contexte` (société) alimente **uniquement** le bloc « Contexte de l'organisation » au niveau **mandat** ; le `contexte_projet` alimente **uniquement** le contexte au niveau **projet**. N'utilisez jamais le contexte de projet pour remplir `{{CONTEXTE_ORGANISATION}}`, ni l'inverse.
- **Cardinalité** : pour un mandat, il y a **un seul** bloc « Contexte de l'organisation » (le client) ; les éventuels **projets** du mandat portent chacun **leur** contexte de projet. Ne pas fusionner les contextes de plusieurs projets dans le bloc d'organisation.
- **Ne rien inventer** (aux deux niveaux) : contexte indisponible (société **ou** projet) ⇒ marqueur « à compléter » + signalement humain ; jamais un contexte fabriqué, jamais un repli silencieux de l'un vers l'autre.

## Responsabilités, réalisations et biens livrables par mandat (section du CV livrable)

Le CV livrable restitue, **pour chaque expérience/mandat**, une section **« Responsabilités, réalisations et biens livrables »** alimentée par l'unique liste `experience[].responsabilites_realisations_livrables` des données CV (champ **au niveau de l'expérience**, regroupant les trois axes de la rubrique source du même nom). Ces informations décrivent la **contribution concrète** du collaborateur sur le mandat (ce dont il avait la charge, ce qu'il a accompli et les biens livrables produits) et doivent **impérativement figurer** dans le CV.

- **Alimentation** : à partir de la liste `responsabilites_realisations_livrables[]` de chaque expérience du YAML courant ; **ne rien inventer** — une liste vide (`[]`) ne produit aucune ligne fabriquée. Rendre les entrées sous forme de puces, **par mandat/expérience** (et non par projet : ce champ est porté au niveau de l'expérience).
- **Cohérence avec les gabarits (`${ROOT_DIRECTORY}/gabarits/cv/`)** : n'écrire que dans les emplacements prévus par le gabarit, sans altérer sa charte. Si le gabarit dispose déjà d'un emplacement « Responsabilités, réalisations et biens livrables » (ou équivalent), l'utiliser ; sinon, placer la section au plus près de la description du mandat concerné. **Si le gabarit n'offre aucun emplacement adapté** pour restituer cette liste, **ne pas inventer de mise en page** : **le signaler à l'humain** (mention) et attendre son arbitrage, plutôt que de forcer la charte.

## Rendu des projets/mandats dans le CV long (format « <client> - <projet> » en puces)

Dans le **CV long uniquement**, les projets/mandats se rendent en **puces** (bullet points), **une puce par projet**, au format **« <client> - <projet> »** — jamais une puce agrégée au niveau du client. Le couple provient des données CV : `<client>` = `experience[].client`, `<projet>` = `experience[].projets[].nom` (voir le schéma `experience[].projets[]` de `cv-analyse`). Cette règle s'applique à **deux endroits** du CV long :

- **Sommaire des réalisations** — dans le tableau/bloc « sommaire des réalisations », lister les projets/mandats en **puces** dès qu'il y en a **plusieurs**, chaque puce au format **« <client> - <projet> »**. Lorsqu'**un même client porte plusieurs projets**, produire **une puce par projet** (jamais une seule puce agrégée pour le client) : p. ex. `- Banque X - Refonte du portail`, `- Banque X - Migration cloud`.
- **Champ « projet » de chaque description de réalisation professionnelle** — dans la section par mandat/expérience, le champ **« projet »** suit la **même règle** : une **puce par projet** au format **« <client> - <projet> »** ; plusieurs projets d'un même client ⇒ une puce par projet.

- **Projet unique** : une expérience ne portant qu'un seul projet peut rester sur une **seule puce** au même format « <client> - <projet> » (la mise en puces devient obligatoire dès qu'il y en a plusieurs).
- **Ne rien inventer** : `experience[].projets[]` vide (`[]`) ou `client`/`projet` absent ⇒ **comportement existant préservé** — aucune puce fabriquée, pas de couple inventé (mention humaine si une donnée manque, conformément aux garde-fous), jamais de « <client> - » ou « - <projet> » tronqué.
- **Respect strict du gabarit** : n'écrire les puces que dans l'emplacement prévu par le gabarit `cv-long.docx` (sommaire des réalisations, champ « projet » du mandat). Si le gabarit n'offre aucun emplacement adapté, **ne pas inventer de mise en page** : le signaler à l'humain (mention) et attendre son arbitrage.

## Prérequis

- Une **analyse existante** du collaborateur (dernière version YAML à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`). Si aucune analyse n'existe, exécuter d'abord `cv-analyse` sur un CV source.
- **En DOCX (défaut)** : le **gabarit DOCX fourni** correspondant au type demandé, présent dans `${ROOT_DIRECTORY}/gabarits/cv/` (sinon halt-and-ask). Sans objet pour un CV Markdown demandé explicitement (pas de gabarit).
- Une **demande explicite du Coordinateur** décrivant la modification/production attendue (type de CV, ajout de compétences, mise à jour d'expérience, format client).
- La **validation humaine** de la production/mise à jour **avant** toute écriture (gate obligatoire).

## Types d'opérations

1. **Ajout / mise à jour de compétences** — enrichir `competences[]` (données) avec `mois_experience` et `derniere_utilisation`. Ne jamais fabriquer une durée ou une date : info manquante ⇒ mention humaine.
2. **Mise à jour d'expérience** — ajouter/corriger des entrées `experience[]` (client, rôle, `date_debut`, `date_fin`, `duree_mois`, `jours_personnes`, description), l'unique liste `experience[].responsabilites_realisations_livrables` (responsabilités + réalisations + biens livrables de l'expérience regroupés — rubrique source « Responsabilités, réalisations et biens livrables », **au niveau de l'expérience**) et le **détail de leurs projets** `experience[].projets[]`. Une expérience peut porter **un ou plusieurs projets** ; chaque projet porte `nom`, `date_debut`, `date_fin` (`AAAA-MM`, `present` si en cours) — les responsabilités/réalisations/livrables **ne sont pas portés par le projet**. Les dates de l'expérience restent indépendantes de celles des projets. Ne jamais fabriquer un nom ou une date de projet, ni une entrée de `responsabilites_realisations_livrables` : info manquante ⇒ `[]` + mention humaine si pertinent.
3. **Production d'un CV livrable** — **par défaut au format DOCX** à partir du **gabarit fourni** (CV long / CV court / format client) et des données du YAML courant ; **au format Markdown uniquement si l'humain le demande explicitement** (livrable humain, aucun secret).
4. **Mise à jour des études et certifications** — enrichir/corriger `etudes[]` (un collaborateur peut porter **plusieurs diplômes** : `niveau`, `formation`, `etablissement`, `annee_obtention`) et, **séparément**, `certifications[]` (plusieurs certifications : `nom`, `organisme`, `annee_obtention`, `date_expiration`, `reference`). Études et certifications restent **deux listes distinctes**, jamais fusionnées ; dans le CV livrable, les rendre en **deux sections séparées** (« Formation / Études » et « Certifications ») lorsque le gabarit le prévoit. Ne jamais fabriquer un diplôme, une certification, une année ou un organisme : donnée absente ⇒ mention humaine.

## Procédure

1. **Charger la dernière analyse** — lire la dernière version YAML du collaborateur (règle de sélection : la compétence `cv-analyse`, § Versionnage YAML). Ne jamais partir d'une version antérieure ni d'un source supprimé.
2. **Déterminer le format et le gabarit** — **par défaut : DOCX** → sélectionner le type demandé (CV long / CV court / format client) et **charger le gabarit fourni** depuis `${ROOT_DIRECTORY}/gabarits/cv/` (**absent ⇒ halt-and-ask**, mention humaine, ne rien inventer, **pas de repli Markdown automatique**). **Si l'humain a explicitement demandé un CV Markdown** → produire le livrable Markdown depuis les données du YAML, sans gabarit DOCX.
3. **Appliquer la modification / le remplissage** sur une copie de travail : en DOCX, injecter les données du YAML dans les emplacements prévus par le gabarit (sans altérer sa charte) — **y compris la substitution, mandat par mandat, du jeton `{{CONTEXTE_ORGANISATION}}`** du bloc « Contexte de l'organisation » du CV long (voir § Contrat de remplissage du jeton `{{CONTEXTE_ORGANISATION}}`) ; en Markdown (sur demande), mettre en forme les données du YAML en un document présentable — sans écraser l'historique.
4. **Vérification post-génération (obligatoire, avant présentation)** — sur la copie de travail produite :
   - **Aucun jeton résiduel (niveaux mandat ET projet)** : vérifier qu'il ne subsiste **aucun** marqueur `{{…}}` non substitué, ni au niveau **mandat** (en particulier `{{CONTEXTE_ORGANISATION}}`) ni au niveau **projet** (contexte de projet). Un jeton résiduel ⇒ corriger la substitution ; si la donnée est réellement absente, appliquer le repli « à compléter » (jamais fabriqué) et signaler à l'humain.
   - **Bon niveau de contexte** : vérifier que le bloc « Contexte de l'organisation » a été rempli depuis le `contexte` (société) et **non** depuis un `contexte_projet`, et réciproquement que les contextes de projet proviennent bien du niveau projet — aucune substitution croisée des deux niveaux (voir § Distinction des niveaux).
   - **Blocs « Contexte de l'organisation » du CV long** : pour **chaque mandat**, vérifier que le bloc est rempli lorsqu'un `contexte` existe au référentiel `clients/<slug>.yaml` (après résolution nom → fichier) ou dans les données d'analyse ; sinon qu'il porte le marqueur **« à compléter »** et que le mandat concerné est **signalé à l'humain** (mention). Aucun bloc ne doit rester vide ni conserver un jeton non substitué.
   - **Contextes de projet** : pour **chaque projet** d'un mandat, vérifier de même que le contexte de projet est rempli quand un `contexte_projet` existe, sinon « à compléter » + signalement humain.
   - Consigner dans la présentation à l'humain le résultat de cette vérification (mandats remplis depuis le référentiel, projets remplis, blocs en « à compléter » signalés).
5. **Présenter la production à l'humain** (Markdown pour la conversation : diff clair avant/après des données injectées + format et, en DOCX, type de gabarit utilisé) et **attendre la validation explicite**. Aucune écriture avant accord.
6. **Écrire les livrables versionnés** une fois validé :
   - **CV livrable** — en **DOCX** (défaut) : `<YYYY-mm-dd>-<nom>-<type-gabarit>.docx` (ex. `2026-09-15-dupont-jean-cv-long.docx`) ; en **Markdown** (sur demande explicite) : `<YYYY-mm-dd>-<nom>-cv.md` — à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`, sans écraser l'historique ni la fiche d'analyse ;
   - mise à jour des **données** si modifiées : nouveau YAML `<YYYY-mm-dd>-<nom>.yaml` et fiche d'analyse Markdown du jour `<YYYY-mm-dd>-<nom>.md` (date du jour), en **archivant** dans `cv/archives/` les versions antérieures des **deux** artefacts (YAML **et** Markdown) avant écriture — à la racine ne subsiste qu'un seul couple ;
   - `date_derniere_modification` = **toujours la date du jour**.
7. **Journaliser sur l'issue** la nature de la modification, le **format** (DOCX/Markdown) et, en DOCX, le **type de gabarit**, le fichier produit, la version YAML produite, le **résultat de la vérification post-génération** (jetons résiduels, mandats « à compléter » signalés) et la validation humaine obtenue (piste d'audit).

## Enracinement des chemins

Tous les chemins relatifs de cette compétence sont **enracinés sur `${ROOT_DIRECTORY}`** (répertoire de travail du workspace) : gabarits dans `${ROOT_DIRECTORY}/gabarits/cv/`, livrables et analyses dans `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`. Ne jamais utiliser de chemin absolu hors `${ROOT_DIRECTORY}` ni un chemin relatif non enraciné.

## Contrat de données

Le **schéma des données CV (YAML)** (compétences, expérience, `etudes[]` — une ou plusieurs études, `certifications[]` — liste **distincte** des études, `mifi`, `disponibilite`, `localisation`, langues), les conventions de nommage et la structure du répertoire `cv/` sont ceux définis dans la compétence `cv-analyse` — s'y référer et ne pas diverger.

## Garde-fous

- **Format du livrable : DOCX par défaut, Markdown sur demande explicite** — par défaut le CV livrable est un **DOCX** produit à partir d'un des gabarits fournis (CV long / CV court / format client). Le **Markdown** n'est produit **que** sur **demande explicite de l'humain**, jamais par défaut ni comme repli d'un gabarit DOCX manquant. **Ne jamais inventer** de gabarit ni de mise en page ; gabarit DOCX absent ⇒ halt-and-ask.
- **Validation humaine obligatoire** avant toute écriture d'un CV produit/mis à jour.
- **CV long — projets/mandats en puces « <client> - <projet> »** — dans le CV long, rendre les projets en **puces**, **une puce par projet** au format **« <client> - <projet> »** (jamais une puce agrégée par client), à la fois dans le **sommaire des réalisations** et dans le champ **« projet »** de chaque réalisation professionnelle (voir § Rendu des projets/mandats dans le CV long). Donnée absente ⇒ comportement existant préservé, aucune puce fabriquée.
- **Aucune note de génération / méta-production dans le CV livrable** — invariant source unique (gouvernance, invariant 7 ; voir § Règle d'or) : le CV ne porte **que l'information métier du candidat** ; la traçabilité (format, gabarit, version YAML, validation) se journalise **sur l'issue** et en mémoire interne, jamais dans le CV.
- **Ne rien inventer** — une donnée absente (durée, date, ville, MIFI) se demande via mention humaine ; jamais fabriquée.
- **Jetons de gabarit substitués, vérification post-génération obligatoire** — tout jeton `{{…}}` du gabarit (notamment `{{CONTEXTE_ORGANISATION}}` du bloc « Contexte de l'organisation » du CV long) doit être **substitué** mandat par mandat (voir § Contrat de remplissage). **Aucun `{{…}}` résiduel** ne doit subsister dans le livrable ; chaque bloc « Contexte de l'organisation » est rempli quand un contexte existe (référentiel `clients/` résolu via la règle nom → fichier, ou données d'analyse), sinon marqueur **« à compléter »** (jamais fabriqué) **+ signalement humain**. La vérification est une étape obligatoire avant présentation (procédure, étape 4).
- **Versionnage** — ne jamais écraser une version YAML antérieure, un CV livrable antérieur (DOCX ou Markdown) ni la fiche archivée ; l'historique est conservé.
- **Non-transmission des CV** — comme pour l'analyse, ne pas faire circuler les CV complets en A2A ; seuls le verdict d'éligibilité et la référence `analyse_yaml` remontent au coordinateur (voir la compétence `cv-analyse`, § Garde-fou).
- **Aucun secret** dans les livrables, commentaires ou notifications.

## Communication

Invariant YAML↔Markdown défini une seule fois dans `governance-security` / le conductor (non redéfini ici). **Spécificité de cette compétence** : le **CV livrable** transmis à l'humain est un **DOCX** par défaut (pièce jointe / fichier), ou un **CV Markdown** si l'humain l'a explicitement demandé — dans les deux cas distinct de la conversation Markdown (diff avant/après pour la validation).
