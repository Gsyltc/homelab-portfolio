---
name: cv-analyse
description: >
    Analyse d'un CV source (PDF/DOCX fourni en pièce jointe d'issue) du workflow Matching : extraction structurée vers livrables versionnés (fiche Markdown du jour + YAML des données CV), archivage, traçabilité, équivalence MIFI, localisation, disponibilité, sélection d'éligibilité amont (Études, Localisation et Certifications requises STRICTES/éliminatoires) vis-à-vis d'un AO, et maintenance du référentiel des contextes clients (sociétés) `${ROOT_DIRECTORY}/clients/<nom-client>.json` lorsqu'un CV long en contient (contexte + mandats réalisés — complète/enrichit, jamais d'écrasement aveugle). Charger avant toute extraction de CV ou classement d'éligibilité.
keywords: [analyse cv, extraction cv, eligibilite, mifi, localisation, disponibilite, type collaborateur, type de collaborateur, alithya, recrutement, offre conditionnelle, non disponible, versionnage cv, format yaml cv, filtre eligibilite, certifications, certification requise, prerequis, contexte client, clients json, mandats, expertise firme, referentiel clients]
---

# Analyse de CV

Cette compétence porte tout le détail opératoire de l'**extraction d'un CV** et de la **sélection d'éligibilité** vis-à-vis d'un AO pour le workflow Matching. Elle est chargée par l'agent **Gestionnaire CV** et alimente le stage d'**extraction CV** (phase Analyse) du workflow Matching.

Les CV sources sont **fournis en pièces jointes de l'issue**, analysés, puis leur copie de travail est **supprimée** (les originaux ne sont **jamais conservés**). Les livrables d'analyse (fiche **Markdown** du jour + **données CV YAML** versionnées) sont écrits dans `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`.

> **Enracinement des chemins** : tous les chemins relatifs sont **enracinés sur `${ROOT_DIRECTORY}`** (répertoire de travail du workspace) ; ne jamais utiliser un chemin absolu hors `${ROOT_DIRECTORY}` ni un relatif non enraciné.

> **Format des données CV = YAML** (décision [ADR-0034](../../../../decisions/0034-format-yaml-donnees-cv.md), EXPE-81). Les **données structurées du CV** (profils `cv-profils`, verdict d'éligibilité `cv-eligibilite`, fichier d'analyse versionné) sont portées en **YAML** — plus léger en tokens que le JSON (~25 % de moins, mesure réelle dans l'ADR) tout en restant lisible à l'audit. Le fichier d'analyse versionné porte l'extension **`.yaml`** et le champ de référence est **`analyse_yaml`**. La **fiche Markdown** du jour (lisible pour l'humain) et le **référentiel des contextes clients** `clients/<nom-client>.json` (hors périmètre CV) sont **inchangés**.

> **Fiche d'analyse ≠ CV livrable** : la fiche Markdown et le YAML produits ici sont la **mémoire interne** (données structurées), **jamais** un livrable client. Le **CV livrable** présentable est produit **au format DOCX par défaut, à partir d'un gabarit fourni** (Markdown possible **sur demande explicite de l'humain**) par la compétence `cv-generation` (gabarits dans `${ROOT_DIRECTORY}/gabarits/cv/`).

## Règle de sélection de la source CV

Dans cet ordre :

1. **CV PDF/DOCX en pièce jointe de l'issue** → extraire les données de ce fichier (nouvelle analyse) : fiche Markdown du jour + YAML versionné, journaliser le nom de la pièce jointe, puis supprimer la copie de travail. La pièce jointe **prime toujours** : c'est une nouvelle version.
2. **Analyse nécessitant un CV, aucune pièce jointe** → utiliser la **dernière version déjà extraite** :
   - flux A2A → **dernière version YAML** (`<YYYY-mm-dd>-<nom>.yaml`, seul YAML à la racine de `cv/`) ;
   - fichier à télécharger pour l'humain → **fiche d'analyse Markdown** courante (du jour).
   - > **Contrôle de fraîcheur du cache réutilisé (OBLIGATOIRE).** Le YAML réutilisé est un **cache** : avant de le retenir pour le matching, contrôler l'**âge de l'analyse** via `date_derniere_modification` (= date de la dernière extraction). Écart > **seuil de péremption de l'analyse** (`SEUIL_PEREMPTION_ANALYSE`, **12 mois** par défaut) entre la date du jour et `date_derniere_modification` ⇒ classer le collaborateur **`a_verifier`** (axe `fraicheur_cv`) **+ mention humaine** « analyse ancienne (dernière extraction le `<AAAA-MM-JJ>`) — CV toujours à jour ? Fournir un CV récent en pièce jointe si nécessaire ». **Ne jamais scorer silencieusement** une analyse périmée ni la « rafraîchir » soi-même (aucune nouvelle extraction sans pièce jointe fournie). Le cache reste utilisable en attendant la réponse humaine, mais le verdict d'éligibilité porte l'alerte. Après réponse humaine confirmant que le CV est à jour, le collaborateur repasse `possible` (le cache est validé) ; sinon l'humain fournit un CV récent (retour au cas 1).
3. **Ni pièce jointe ni analyse antérieure** → CV **manquant** : le signaler (pas de matching possible pour ce collaborateur).

> Vaut pour les scopes `standard`, `complex`, `express`. Le scope `format-cv` (traitement CV seul) s'applique au cas 1 (extraction d'une pièce jointe fournie).

## Structure du répertoire `cv/`

Les CV sources ne sont **pas stockés**. `cv/` ne contient que les livrables d'analyse (mémoire) et les **CV livrables DOCX** produits depuis les gabarits :

```
${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/
├── archives/                                     # anciennes analyses (fiches Markdown ET YAML des versions antérieures)
├── <YYYY-mm-dd>-<nom>.md                         # dernière analyse Markdown (courante, mémoire — seule à la racine)
├── <YYYY-mm-dd>-<nom>.yaml                        # dernières données CV YAML (courantes, mémoire — seul YAML à la racine)
└── <YYYY-mm-dd>-<nom>-<type-gabarit>.docx         # CV livrable (DOCX par défaut ; Markdown <YYYY-mm-dd>-<nom>-cv.md sur demande) — produit par cv-generation
```

> **Nommage daté unifié `<YYYY-mm-dd>-<nom>`** : les deux artefacts d'analyse (fiche Markdown et données YAML) et le CV livrable partagent le même **préfixe daté `<YYYY-mm-dd>`** (toujours la **date du jour** ISO, cohérente avec `date_derniere_modification`) suivi du **slug `<nom>`** (minuscule, cohérent avec le segment `<nom-prenom>` du répertoire). Fiche d'analyse : `<YYYY-mm-dd>-<nom>.md` ; données CV : `<YYYY-mm-dd>-<nom>.yaml` ; CV livrable : `<YYYY-mm-dd>-<nom>-<type-gabarit>.docx` (ou `<YYYY-mm-dd>-<nom>-cv.md`).

> **Seule la dernière analyse à la racine (couple YAML + Markdown)** : la racine de `cv/` ne contient qu'**un seul couple** `<YYYY-mm-dd>-<nom>.{yaml,md}` — la dernière analyse. **Avant** d'écrire une nouvelle analyse, **toutes** les versions antérieures des **deux** artefacts (YAML **et** Markdown) sont **déplacées dans `archives/`**. L'historique est **conservé** dans `archives/` ; la « dernière version » est donc **triviale** (le seul couple à la racine), sans règle de tri par date/mtime.

Les **gabarits DOCX fournis** (CV long / CV court / format client) vivent dans `${ROOT_DIRECTORY}/gabarits/cv/` — voir la compétence `cv-generation`. Le format **par défaut du CV livrable est le DOCX** ; le **Markdown** n'est produit que **sur demande explicite de l'humain**.

- **Sources (PDF, DOCX)** : **non stockés**. Fournis en pièces jointes de l'issue, récupérés via `multica attachment`, puis copie de travail **supprimée**.
- **`archives/`** : anciennes analyses des deux formats — fiches Markdown **et** YAML des versions antérieures, déplacés à chaque nouvelle analyse.
- **Racine de `cv/`** : la **dernière** analyse uniquement — un seul couple `<YYYY-mm-dd>-<nom>.md` (fiche Markdown courante) + `<YYYY-mm-dd>-<nom>.yaml` (**données CV courantes**, mémoire persistante) — et les **CV livrables** (DOCX produits depuis les gabarits ; Markdown sur demande explicite).

## Traitement des CV sources

1. Récupérer le(s) fichier(s) attaché(s) via `multica attachment` (jamais en ouvrant une URL de ressource Multica). La copie téléchargée est une copie de travail privée, transitoire.
2. Extraire et produire les livrables (Markdown du jour + YAML versionné) dans `cv/`.
3. **Journaliser sur l'issue, AVANT suppression**, le(s) nom(s) du/des fichier(s) source(s) (et date si disponible) — seule trace d'audit de l'original, non conservé.
4. Extraction **terminée et vérifiée** → **supprimer la copie de travail**. Aucun original écrit dans `cv/`. Ne jamais supprimer avant d'avoir écrit et vérifié les livrables.

## Analyse versionnée (Markdown)

Fichier à la **racine de `cv/`**, nommé par le **préfixe daté du jour** : `<YYYY-mm-dd>-<nom>.md`.

- Préfixe `<YYYY-mm-dd>` = **toujours la date du jour** de l'analyse (ISO). `<nom>` = slug minuscule cohérent avec le segment `<nom-prenom>` du répertoire. Même jour → écrase le fichier du jour ; autre jour → nouvelle fiche (la précédente est archivée).
- **Archivage (seule la dernière à la racine)** : avant d'écrire la fiche du jour, déplacer **toute** fiche d'analyse Markdown antérieure présente à la racine vers `archives/`. À la racine ne subsiste que la fiche courante.
- `date_derniere_modification` reportée = **toujours la date du jour**, jamais la date du fichier source.
- Contenu (Markdown lisible, aucun secret) : CV source traité (nom, journalisé avant suppression), compétences avec mois d'expérience + dernière utilisation, expérience (avec `date_debut`/`date_fin`, méthodologies et technologies mobilisées par mission, et le **détail des projets** de chaque expérience — un ou plusieurs projets avec `nom`, `date_debut`/`date_fin` et `responsabilites`), **grilles d'expérience par technologie et par méthodologie** (mois d'XP calendaires + dernière utilisation, issus des agrégats collaborateur), **études** (une ou plusieurs, chacune avec niveau, formation, établissement, année d'obtention), **certifications** (liste distincte des études — chacune avec intitulé, organisme, année, expiration éventuelle), équivalence MIFI (état, étude concernée, `niveau_equivalent_qc`, `reference_mifi`, commentaire — signaler les `a_verifier` en attente humaine), type de collaborateur (alithya / recrutement / offre conditionnelle / non disponible — signaler un type non déterminé en attente humaine), disponibilité (date + taux %), localisation (ville, région/pays — signaler ville manquante en attente humaine), langues.
- Ce fichier est un **livrable humain** : Markdown uniquement, aucun secret.

## Versionnage YAML

Fichier à la racine de `cv/` : `<YYYY-mm-dd>-<nom>.yaml`. **Seule la dernière analyse** reste à la racine (couple YAML + Markdown) ; l'historique est conservé dans `archives/`.

- Préfixe `<YYYY-mm-dd>` = **toujours la date du jour** de l'analyse (ISO) ; `<nom>` = slug minuscule cohérent avec le répertoire. Même jour → met à jour le fichier du jour ; autre jour → nouveau fichier (le précédent est archivé).
- **Archivage (seul le YAML courant à la racine)** : **avant** d'écrire le YAML du jour, déplacer **tout** YAML d'analyse antérieur présent à la racine vers `archives/` (comme pour la fiche Markdown). À la racine ne subsiste qu'**un seul** YAML — la **dernière version**.
- **Dernière version** = l'**unique** YAML à la racine (règle triviale : plus de tri par date/mtime pour départager plusieurs versions racine). **Seule la dernière version** est croisée avec un AO ; les versions antérieures (dans `archives/`) ne le sont **jamais**.
- **Journaliser** sur l'issue le fichier YAML retenu (nom + date) et la liste des versions déplacées dans `archives/` (piste d'audit).
- **CV par défaut (scopes `standard`/`complex`/`express`)** : flux A2A → dernière version YAML ; flux de gate humain → fiche Markdown courante.

## Format de sortie (YAML — données CV)

Les données CV (`cv-profils` + verdict `eligibilite`) sont sérialisées en **YAML** (bloc, non *flow* sauf listes courtes), plus léger que le JSON (~25 % de tokens en moins — mesure réelle [ADR-0034](../../../../decisions/0034-format-yaml-donnees-cv.md)) tout en restant lisible à l'audit. **Mêmes champs, même sémantique** que l'ancien JSON — rien n'est ajouté, retiré ni renommé, hormis `analyse_json` → **`analyse_yaml`** (le fichier versionné est désormais `.yaml`).

```yaml
collaborateurs:
  - nom: <prénom nom>
    date_derniere_modification: "<AAAA-MM-JJ — TOUJOURS la date du jour de l'analyse>"  # quoté (date ISO complète)
    source_cv: {fichier: <pièce jointe traitée, journalisée avant suppression>, provenance: issue-attachment, conserve: false}
    analyse_markdown: <chemin vers <YYYY-mm-dd>-<nom>.md (racine de cv/)>
    analyse_yaml: <chemin vers <YYYY-mm-dd>-<nom>.yaml (racine de cv/)>
    competences:
      - {nom: <compétence>, mois_experience: 0, derniere_utilisation: "<AAAA-MM>"}
    experience:
      - client: <client>
        role: <rôle>
        date_debut: "<AAAA-MM>"
        date_fin: "<AAAA-MM | present>"
        duree_mois: 0
        jours_personnes: 0
        methodologies: [<méthodologie>]
        technologies: [<technologie>]
        description: <courte>
        projets:
          - nom: <nom du projet>
            date_debut: "<AAAA-MM>"
            date_fin: "<AAAA-MM | present>"
            responsabilites: [<responsabilité tenue sur le projet>]
    technologies:
      - {nom: <technologie>, mois_experience: 0, derniere_utilisation: "<AAAA-MM>"}
    methodologies:
      - {nom: <méthodologie>, mois_experience: 0, derniere_utilisation: "<AAAA-MM>"}
    etudes:
      - {niveau: <diplôme>, formation: <formation>, etablissement: <établissement>, annee_obtention: "<AAAA ou null>"}
    certifications:
      - {nom: <intitulé de la certification>, organisme: <organisme émetteur>, annee_obtention: "<AAAA ou null>", date_expiration: "<AAAA-MM | null si sans expiration>", reference: "<identifiant / n° de certification ou null>"}
    mifi:
      equivalence_requise: non_requise | oui | non | a_verifier
      etude_concernee: <niveau/formation de l'étude de etudes[] visée par l'équivalence, ou null>
      diplome_origine: <diplôme d'origine>
      pays_etudes: <pays>
      niveau_equivalent_qc: <DEC | BAC | Maîtrise | Doctorat | ... si MIFI présent, sinon null>
      reference_mifi: <n° / mention MIFI ou null>
      source: cv | humain
      commentaire: <précision, ex. "MIFI non mentionné — à confirmer par l'humain">
    type_collaborateur: alithya | recrutement | offre_conditionnelle | non_disponible
    disponibilite: {date_disponibilite: "<AAAA-MM-JJ>", taux_utilisation: 0}
    localisation: {ville: <OBLIGATOIRE>, region: <province/région ou null>, pays: <pays ou null>, source: cv | humain}
    langues: [<langue>]
eligibilite:
  collaborateurs_possibles:
    - {nom: <prénom nom>, analyse_yaml: <chemin YAML versionné retenu>}
  collaborateurs_a_verifier:
    - nom: <prénom nom>
      raisons:
        - {axe: "etudes | mifi | experiences | localisation | certifications | disponibilite | coherence | fraicheur_cv", detail: "<ex. 'MIFI a_verifier — arbitrage humain requis' ; 'fraicheur_cv — analyse réutilisée du <AAAA-MM-JJ>, > 12 mois, CV à jour ?'>"}
  collaborateurs_exclus:
    - nom: <prénom nom>
      raisons:
        - {axe: "etudes | mifi | experiences | localisation | certifications | disponibilite | coherence | fraicheur_cv", detail: <raison précise vis-à-vis de l'AO>}
```

### Règles de validité YAML (données CV)

Le YAML des données CV **doit rester parsable sans ambiguïté de type**. Règles obligatoires (vérifiées par parse) :

1. **Dates ISO complètes `AAAA-MM-JJ` → toujours entre guillemets** (`date_derniere_modification`, `disponibilite.date_disponibilite`) : non quotées, elles sont interprétées comme des **objets date** par le parseur, pas comme des chaînes. Ex. `date_derniere_modification: "2026-09-29"`.
2. **Dates partielles `AAAA-MM` et `present` → entre guillemets** (`date_debut`, `date_fin`, `derniere_utilisation`, `certifications[].date_expiration`) : par cohérence et pour éviter toute coercition. Ex. `date_fin: "2023-06"`, `date_fin: "present"`.
3. **Valeurs numériques restant des chaînes → entre guillemets** (`annee_obtention: "2015"`, `certifications[].reference: "AWS-SAA-12345"` ou purement numérique) : sinon interprétées comme des entiers. Les vrais nombres (`mois_experience`, `duree_mois`, `jours_personnes`, `taux_utilisation`) restent **non quotés**.
4. **Booléens réservés** : `conserve: false` est un vrai booléen (correct). En revanche, les valeurs d'énum `oui`/`non` de `mifi.equivalence_requise` restent des **chaînes** (sûres) ; **ne jamais** employer `yes/no/on/off` comme valeur libre (ils deviendraient des booléens).
5. **Notation *flow* (`[...]` / `{...}`)** : mettre entre guillemets toute valeur contenant `${...}`, `:` suivi d'un espace, une virgule, `{` ou `}`. `null` (ou champ omis) pour l'absence. **Au moindre doute, guillemeter.**

### Champs obligatoires et règles

- **`competences`** : chaque compétence porte obligatoirement `mois_experience` (durée cumulée en mois) et `derniere_utilisation` (mois/année de dernière mobilisation) — alimentent le calcul de compatibilité côté Matcher.
- **`experience`** : chaque expérience (mission chez un `client`) porte ses propres `date_debut` et `date_fin` au format `AAAA-MM` (`date_fin: "present"` si la mission est en cours), en plus de `duree_mois`. Ces dates sont **celles de l'expérience elle-même** et sont **indépendantes des projets** : elles ne sont ni bornées ni déduites des dates des projets (une expérience peut couvrir des périodes sans projet détaillé). Elle porte aussi `methodologies` et `technologies` (listes des méthodologies/technologies mobilisées sur cette mission). **Ne rien inventer** : une méthodologie/technologie non mentionnée dans le CV n'est pas ajoutée ; si aucune n'est mentionnée pour l'expérience, mettre `[]`.
- **`experience[].projets`** : une expérience contient **un ou plusieurs projets** (liste `projets[]`). Chaque projet porte obligatoirement : `nom` (intitulé du projet), `date_debut` et `date_fin` au format `AAAA-MM` (`date_fin: "present"` si le projet est en cours), et `responsabilites` (liste des responsabilités tenues sur ce projet). Les dates d'un projet lui sont propres et **n'ont pas à recouvrir toute la période de l'expérience** ni à en respecter les bornes. **Ne rien inventer** : nom, date ou responsabilité de projet absents du CV ⇒ **mention humaine**, jamais fabriqués ; si le CV ne détaille aucun projet pour l'expérience, mettre `projets: []`.
- **`technologies` / `methodologies` (agrégats collaborateur)** : listes d'objets `{ nom, mois_experience, derniere_utilisation }` consolidant, au niveau du collaborateur, toutes les technologies/méthodologies apparaissant dans les `experience[]`.
  - `mois_experience` = **union calendaire** des périodes `date_debut`→`date_fin` de **toutes les expériences** où la techno/méthodo apparaît, exprimée en **nombre de mois distincts couverts** (unité `mois_experience`, cohérente avec `competences`). **Pas de double comptage** : deux expériences simultanées (ou chevauchantes) partageant une même techno ne comptent le mois commun **qu'une seule fois** ; l'union des intervalles mensuels est calculée avant de sommer. `date_fin: "present"` = jusqu'au mois courant. Ne jamais exprimer en années décimales dans le YAML.
  - `derniere_utilisation` = mois le plus récent (`AAAA-MM`) parmi les `date_fin` des expériences où la techno/méthodo apparaît (`present` → mois courant).
  - `[]` si aucune techno/méthodo n'apparaît dans les expériences — **ne rien inventer**.
  - Ces agrégats sont **informatifs** (remplissage de grilles, présentation humaine) et alimentent le Matcher pour la couverture technos/méthodos vis-à-vis de l'AO.
- **`etudes` (liste)** : un collaborateur porte **une ou plusieurs études** (`etudes[]`). Chaque étude porte `niveau` (diplôme), `formation`, `etablissement` et `annee_obtention` (`AAAA` ou `null`). C'est le **niveau le plus élevé** parmi `etudes[]` — après équivalence MIFI tranchée — qui sert au critère strict Études. **Ne rien inventer** : une étude non mentionnée n'est pas ajoutée ; aucune étude dans le CV ⇒ `etudes: []` + mention humaine si l'AO exige un niveau.
- **`certifications` (liste, distincte des études)** : les certifications professionnelles (ex. PMP, AWS, Scrum, ITIL) sont portées par une liste **séparée** `certifications[]`, **jamais** mélangées à `etudes[]`. Chaque certification porte `nom`, `organisme`, `annee_obtention` (`AAAA`/`null`), `date_expiration` (`AAAA-MM`/`null`) et `reference` (`null` si absent). Les certifications **ne relèvent pas** de l'équivalence MIFI ni du critère strict Études. Elles jouent **deux rôles** vis-à-vis de l'AO : (1) elles alimentent la couverture **Compétences** côté Matcher ; (2) lorsqu'une certification est marquée **`obligatoire`** dans l'AO (`profils_recherches[].certifications_requises` avec `criticite: "obligatoire"`), elles servent au **critère strict Certifications requises** du filtre d'éligibilité (voir § Sélection d'éligibilité). **Ne rien inventer** : aucune certification ⇒ `certifications: []` ; une certification **expirée** (`date_expiration` dépassée à la date du jour) n'est **pas** considérée comme détenue pour le critère strict.
- **`date_derniere_modification` / `source_cv` / `analyse_yaml`** : `date_derniere_modification` = toujours la date du jour. `source_cv` documente la pièce jointe (`provenance: "issue-attachment"`, `conserve: false`) — seule trace de l'entrée supprimée. `analyse_yaml` pointe vers le fichier YAML courant (`<YYYY-mm-dd>-<nom>.yaml`, seul YAML à la racine) ; seule la dernière version est croisée avec un AO.
- **`type_collaborateur`** (obligatoire — qualifie la disponibilité) : **statut du collaborateur** vis-à-vis de la firme, qui **conditionne sa disponibilité** pour le matching. Quatre valeurs (`enum`), mutuellement exclusives :
  - `alithya` — **collaborateur interne Alithya** (salarié en poste). **Disponible** pour le matching selon sa `disponibilite` (`date_disponibilite` + `taux_utilisation`).
  - `recrutement` — **profil en cours de recrutement** (candidat non encore embauché). **Disponible conditionnellement** à l'embauche ; à présenter à l'humain comme tel.
  - `offre_conditionnelle` — **disponibilité conditionnée à l'obtention de l'offre** (le collaborateur ne serait mobilisé que si l'AO est remporté). **Disponible conditionnellement**.
  - `non_disponible` — **collaborateur non disponible** (ne peut pas être positionné sur l'AO, quelle que soit sa `disponibilite`). **Écarté du matching** : l'axe de sélection d'éligibilité classe ce collaborateur **`exclu`** (axe `disponibilite`, `detail` = « type_collaborateur = non_disponible »), sans validation humaine préalable.
  - **Ne rien inventer** : si le type n'est pas déterminable depuis le CV / le contexte de l'issue, **poser une mention humaine** demandant le type de collaborateur et laisser le champ à `null` en attendant ; après réponse humaine, renseigner la valeur. Présence contrôlée par le sensor advisory `disponibilite-complete` (voir ce sensor). Le type `alithya`/`recrutement`/`offre_conditionnelle` **n'exclut jamais** de lui-même : il qualifie la disponibilité présentée à l'humain ; seul `non_disponible` écarte le collaborateur.
- **`disponibilite`** (obligatoire) : `date_disponibilite` (ISO) + `taux_utilisation` (0–100). Un CV sans disponibilité complète est incomplet. Présence contrôlée par le sensor advisory `disponibilite-complete` à la frontière Analyse → Matching. Le champ `type_collaborateur` **qualifie** cette disponibilité (voir ci-dessus) : un collaborateur `non_disponible` est écarté quelle que soit sa `disponibilite`.
- **`localisation`** (obligatoire — ville) : `ville` requise, `region`/`pays` optionnels. **Si absente du CV, ne rien inventer** : poser une **mention humaine** demandant la ville, laisser `null` en attendant ; après réponse → renseigner `ville`, `source: "humain"`. Base du critère de proximité (70 km) pour AO `sur_site`/`hybride`. Présence contrôlée par le sensor advisory `localisation-complete`.
- **`mifi`** (équivalence MIFI — contexte gouvernemental Québec) — 4 états d'`equivalence_requise` :
  - `non_requise` — diplôme canadien : `niveau_equivalent_qc` = niveau tel quel.
  - `oui` — MIFI possédé : conserver `niveau_equivalent_qc` reconnu + `reference_mifi` si disponible.
  - `non` — études à l'étranger **sans** MIFI : pas d'équivalence, diplôme non comparable au niveau québécois.
  - `a_verifier` — indéterminable : **mention humaine** (ne rien inventer) ; après réponse → `oui` (+ niveau) ou `non`, `source: "humain"`.
  Règle : diplôme canadien → `non_requise` ; MIFI mentionné → `oui` + niveau ; études étrangères sans MIFI → `a_verifier` + mention humaine. Présence/cohérence contrôlées par le sensor advisory `equivalence-mifi`. L'équivalence MIFI porte sur **une étude de `etudes[]`** (renseigner `etude_concernee` — le diplôme étranger visé) et **jamais** sur une certification. Lorsque plusieurs études existent, l'équivalence est évaluée sur celle qui conditionne le niveau requis par l'AO.

## Référentiel des contextes clients (`${ROOT_DIRECTORY}/clients/<nom-client>.json`)

Certains CV — en particulier les **CV longs** — décrivent, pour chaque mandat, le **contexte de l'organisation cliente** (la société où le collaborateur est intervenu) en plus des réalisations du collaborateur. Le Gestionnaire CV **capitalise** cette information dans le **référentiel des contextes clients** `${ROOT_DIRECTORY}/clients/<nom-client>.json` (un fichier par client : contexte de la société + mandats réalisés), pour alimenter l'analyse d'**expertise de firme** de l'Analyste RFP et le bloc « Contexte de l'organisation » du CV long.

- **Quand (condition impérative)** : cette maintenance n'est **activée que si le CV analysé contient un contexte client** — c'est le **seul déclencheur**. Un CV **sans** contexte client ne déclenche **aucune** activation ni écriture dans `clients/`. Le Gestionnaire CV vérifie d'abord cette présence.
- **Comment** : **créer/compléter** le fichier du client — **enrichir sans écraser aveuglément** le `contexte`, **ajouter/fusionner** (dédoublonner) les mandats — **ne rien inventer**.

> **Source unique** — le **schéma complet** de `clients/<nom-client>.json`, les conventions de **nommage** (slug), les **règles de maintenance** (enrichissement, dédoublonnage) et le **contrat de lecture** vivent dans la compétence dédiée `contexte-client`. S'y référer et **ne pas dupliquer** ici. Cette compétence `cv-analyse` en est le **producteur** (côté Gestionnaire CV) et charge `contexte-client` avant toute écriture dans `clients/`.

## Sélection d'éligibilité (objet `eligibilite`)

Filtre appliqué **en amont du matching** pour que le Matcher ne score que les profils pertinents : il **classe**, il ne note pas.

**Pré-requis — CV à jour et cohérents.** Vérifier que chaque CV analysé est à jour et cohérent : champs obligatoires renseignés (compétences avec `mois_experience`/`derniere_utilisation`, expérience, `etudes[]` — une ou plusieurs, `certifications[]` — liste distincte, `mifi`, `disponibilite`, `localisation`). Incohérence/donnée manquante bloquante → axe `coherence` (ou `fraicheur_cv`).

**Contrôle de fraîcheur de l'analyse réutilisée (axe `fraicheur_cv`).** Lorsque le collaborateur est traité par **réutilisation d'un YAML déjà extrait** (cas 2 de la § Règle de sélection de la source CV — aucune pièce jointe fournie), contrôler l'**âge de l'analyse** : écart entre la **date du jour** et `date_derniere_modification` (date de la dernière extraction) supérieur au **seuil de péremption `SEUIL_PEREMPTION_ANALYSE` (12 mois par défaut)** ⇒ classer le collaborateur **`a_verifier`** (axe `fraicheur_cv`, `detail` = « analyse ancienne du `<AAAA-MM-JJ>` — CV toujours à jour ? ») **+ mention humaine**. C'est un contrôle **distinct** de la règle de fraîcheur des **compétences** du Matcher (> 10 ans sur `derniere_utilisation`, portant sur les compétences *à l'intérieur* d'un CV) : ici, c'est l'**âge de l'analyse réutilisée** (le cache) qui est contrôlé, pas l'ancienneté d'une compétence. **Ne jamais scorer silencieusement** un cache périmé. Ce cas relève de `a_verifier` (arbitrage humain), non d'`exclu` : le cache reste utilisable en attendant la réponse humaine (repasse `possible` si le CV est confirmé à jour, ou l'humain fournit un CV récent → nouvelle extraction). Une extraction **fraîche** (cas 1, pièce jointe traitée le jour même) n'est **jamais** concernée par ce contrôle.

**Cinq axes vis-à-vis de l'AO** (`profils_recherches` / exigences produits par `parse-ao`). **Études, Localisation et Certifications requises sont STRICTS et ÉLIMINATOIRES** : tranchés (donnée connue/confirmée) et non atteints ⇒ `exclu` **automatique**, sans validation humaine préalable. Ils ne restent `a_verifier` **que** tant que la donnée est **non tranchée** (**ne rien inventer** : donnée manquante ⇒ mention humaine, jamais d'exclusion sur donnée inconnue) :

- **Études (STRICT, éliminatoire)** — l'AO exige un niveau (ex. BAC / DEC). Si le **niveau le plus élevé parmi `etudes[]`** du collaborateur — **après équivalence MIFI tranchée** (`mifi.niveau_equivalent_qc` si `equivalence_requise` ∈ {`oui`, `non_requise`}) et toute compensation d'expérience **explicitement prévue par l'AO** — n'atteint pas ce niveau ⇒ **`exclu`** (axe `etudes`). Les **certifications** (`certifications[]`) **ne comptent pas** pour ce critère de niveau d'études. Une équivalence **tranchée `non`** (études étrangères sans équivalence reconnue) face à un niveau exigé ⇒ **`exclu`** (axe `etudes`). Reste `a_verifier` **uniquement** si l'équivalence est **non tranchée** (`a_verifier`).
- **MIFI (si nécessaire)** — AO gouvernemental Québec exigeant un niveau d'études : équivalence disponible ? `equivalence_requise = a_verifier` **non tranché** ⇒ `a_verifier` (jamais `exclu` de force sur donnée non tranchée) + mention humaine. Équivalence **tranchée `non`** face à un niveau exigé bascule sur l'axe **Études strict** ⇒ `exclu`.
- **Expériences** — l'expérience recoupe-t-elle le domaine / les compétences clés de l'AO ?
- **Localisation (STRICT, éliminatoire si présence sur site)** — AO `localisation_travail.mode` ∈ {`sur_site`, `hybride`} : collaborateur ≤ `rayon_km` (**70 km par défaut**) entre `localisation.ville` et `localisation_travail.ville_site` ? Au-delà ⇒ **`exclu`** (axe `localisation`, ex. « AO Montréal, candidat à Québec — > 70 km »). Ville du candidat **manquante** (donnée non tranchée) ⇒ `a_verifier` (jamais `exclu` de force) + mention humaine. `mode = teletravail`/`non_precise` ⇒ critère **non applicable**. Doute proche du seuil ⇒ préférer `a_verifier` + mention humaine plutôt qu'une exclusion arbitraire.
- **Certifications requises (STRICT, éliminatoire si l'AO exige une certification)** — pour **chaque** certification du profil recherché marquée `criticite: "obligatoire"` dans l'AO (`profils_recherches[].certifications_requises`), le collaborateur **doit** détenir une certification correspondante **valide** (présente dans son `certifications[]`, non expirée à la date du jour). Correspondance par `nom` (et `organisme` si renseigné), en tolérant les variantes de libellé usuelles d'une même certification. S'il **manque une certification obligatoire** (absente, ou uniquement présente sous forme expirée, ou remplacée par un simple *coursework*/formation non certifiante) ⇒ **`exclu`** (axe `certifications`, ex. « AO exige AWS Certified Solutions Architect – Associate — non détenue »). Une certification **`souhaitee`/`nice-to-have`** de l'AO **n'exclut jamais** (elle relève de la couverture Compétences côté Matcher). Le collaborateur reste `a_verifier` **uniquement** si la détention est **non tranchée** (ex. le CV mentionne la certification sans permettre de confirmer sa validité/expiration) : mention humaine, **ne rien inventer** — jamais d'exclusion sur donnée non tranchée, ni de certification supposée détenue sans base dans le CV. Si l'AO n'exige **aucune** certification `obligatoire`, ce critère est **non applicable**.
- **Disponibilité — type de collaborateur (STRICT, éliminatoire pour `non_disponible`)** — le champ `type_collaborateur` qualifie la disponibilité (voir § Champs obligatoires et règles). Un collaborateur **`non_disponible`** (tranché) est **`exclu`** (axe `disponibilite`, `detail` = « type_collaborateur = non_disponible ») **automatiquement**, sans validation humaine préalable, quelle que soit sa `disponibilite`. Les types `alithya`, `recrutement` et `offre_conditionnelle` **n'excluent pas** : ils qualifient la disponibilité présentée à l'humain (interne / à recruter / conditionnée à l'obtention de l'offre). Le collaborateur reste `a_verifier` **uniquement** si le type est **non tranché** (`type_collaborateur = null`, non déterminable) : mention humaine, **ne rien inventer** — jamais d'exclusion sur type inconnu.

**Trois états** (mutuellement exclusifs) :

- `possible` — **retenu**, transmis au Matcher. Reporté dans `collaborateurs_possibles` avec `nom` + `analyse_yaml` (dernière version YAML retenue).
- `a_verifier` — **arbitrage humain requis, uniquement** lorsqu'une donnée d'un critère est **non tranchée** (MIFI non tranché, ville manquante) **ou** lorsque l'analyse **réutilisée** (cache YAML, aucune pièce jointe) est **périmée** (âge > `SEUIL_PEREMPTION_ANALYSE`, 12 mois par défaut — axe `fraicheur_cv`) : **ne rien inventer**, mention humaine. Reporté dans `collaborateurs_a_verifier` avec `nom` + `raisons` (`axe` + `detail`).
- `exclu` — **écarté définitivement**. Reporté dans `collaborateurs_exclus` avec `nom` + `raisons` précises. Inclut **tout critère STRICT Études, Localisation ou Certifications requises tranché et non atteint** — exclusion automatique, sans validation humaine préalable.

Axes de raison : `etudes`, `mifi`, `experiences`, `localisation`, `certifications`, `disponibilite`, `coherence`, `fraicheur_cv`. Chaque `a_verifier` et `exclu` **doit** porter au moins une raison. Le verdict d'éligibilité est le seul artefact décisionnel remonté au coordinateur pour départager les profils avant matching.

## Garde-fou — non-transmission des CV

Ne **JAMAIS** transmettre au coordinateur les sources (supprimées), les fiches Markdown ni le YAML complet des données CV. Remonter uniquement :

- le **verdict d'éligibilité** (`eligibilite` : possibles / à vérifier / exclus + raisons) ;
- pour chaque **retenu** (`possible`), la **référence `analyse_yaml`** — c'est le Matcher qui lira lui-même cette dernière version YAML.

Le coordinateur transmet ainsi au Matcher **uniquement la liste des retenus** ; les données CV restent dans `cv/` et ne circulent pas en A2A.
