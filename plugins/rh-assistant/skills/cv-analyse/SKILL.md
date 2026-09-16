---
name: cv-analyse
description: >
    Analyse d'un CV source (PDF/DOCX fourni en pièce jointe d'issue) du workflow Matching : extraction structurée vers livrables versionnés (fiche Markdown du jour + JSON), archivage, traçabilité, équivalence MIFI, localisation, disponibilité, et sélection d'éligibilité amont (Études et Localisation STRICTS/éliminatoires) vis-à-vis d'un AO. Charger avant toute extraction de CV ou classement d'éligibilité.
keywords: [analyse cv, extraction cv, eligibilite, mifi, localisation, disponibilite, versionnage cv, filtre eligibilite]
---

# Analyse de CV

Cette compétence porte tout le détail opératoire de l'**extraction d'un CV** et de la **sélection d'éligibilité** vis-à-vis d'un AO pour le workflow Matching. Elle est chargée par l'agent **Gestionnaire CV** et alimente le stage d'**extraction CV** (phase Analyse) du workflow Matching.

Les CV sources sont **fournis en pièces jointes de l'issue**, analysés, puis leur copie de travail est **supprimée** (les originaux ne sont **jamais conservés**). Les livrables d'analyse (fiche **Markdown** du jour + **JSON** versionnés) sont écrits dans `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv`.

> **Enracinement des chemins** : tous les chemins relatifs sont **enracinés sur `${ROOT_DIRECTORY}`** (répertoire de travail du workspace) ; ne jamais utiliser un chemin absolu hors `${ROOT_DIRECTORY}` ni un relatif non enraciné.

> **Fiche d'analyse ≠ CV livrable** : la fiche Markdown et le JSON produits ici sont la **mémoire interne** (données structurées), **jamais** un livrable client. Le **CV livrable** présentable est produit **au format DOCX par défaut, à partir d'un gabarit fourni** (Markdown possible **sur demande explicite de l'humain**) par la compétence [`../cv-generation/SKILL.md`](../cv-generation/SKILL.md) (gabarits dans `${ROOT_DIRECTORY}/gabarits/cv/`).

## Règle de sélection de la source CV

Dans cet ordre :

1. **CV PDF/DOCX en pièce jointe de l'issue** → extraire les données de ce fichier (nouvelle analyse) : fiche Markdown du jour + JSON versionné, journaliser le nom de la pièce jointe, puis supprimer la copie de travail. La pièce jointe **prime toujours** : c'est une nouvelle version.
2. **Analyse nécessitant un CV, aucune pièce jointe** → utiliser la **dernière version déjà extraite** :
   - flux A2A → **dernière version JSON** (`<nom>-<prenom>-<AAAA-MM-JJ>.json`) ;
   - fichier à télécharger pour l'humain → **fiche d'analyse Markdown** courante (du jour).
3. **Ni pièce jointe ni analyse antérieure** → CV **manquant** : le signaler (pas de matching possible pour ce collaborateur).

> Vaut pour les scopes `standard`, `complex`, `express`. Le scope `format-cv` (traitement CV seul) s'applique au cas 1 (extraction d'une pièce jointe fournie).

## Structure du répertoire `cv/`

Les CV sources ne sont **pas stockés**. `cv/` ne contient que les livrables d'analyse (mémoire) et les **CV livrables DOCX** produits depuis les gabarits :

```
${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/
├── archives/                                     # anciennes fiches Markdown d'analyse
├── <AAAA-MM-JJ>-<nom>-<prenom>.md                # dernière analyse Markdown (courante, mémoire)
├── <nom>-<prenom>-<AAAA-MM-JJ>.json              # analyses JSON versionnées (mémoire)
└── <nom>-<prenom>-<type-gabarit>-<AAAA-MM-JJ>.docx # CV livrable (DOCX par défaut ; Markdown …-cv-<AAAA-MM-JJ>.md sur demande) — produit par cv-generation
```

Les **gabarits DOCX fournis** (CV long / CV court / format client) vivent dans `${ROOT_DIRECTORY}/gabarits/cv/` — voir [`../cv-generation/SKILL.md`](../cv-generation/SKILL.md). Le format **par défaut du CV livrable est le DOCX** ; le **Markdown** n'est produit que **sur demande explicite de l'humain**.

- **Sources (PDF, DOCX)** : **non stockés**. Fournis en pièces jointes de l'issue, récupérés via `multica attachment`, puis copie de travail **supprimée**.
- **`archives/`** : anciennes fiches d'analyse Markdown (déplacées à chaque nouvelle analyse).
- **Racine de `cv/`** : la fiche Markdown courante (du jour), les JSON versionnés (**mémoire persistante**) et les **CV livrables** (DOCX produits depuis les gabarits ; Markdown sur demande explicite).

## Traitement des CV sources

1. Récupérer le(s) fichier(s) attaché(s) via `multica attachment` (jamais en ouvrant une URL de ressource Multica). La copie téléchargée est une copie de travail privée, transitoire.
2. Extraire et produire les livrables (Markdown du jour + JSON versionné) dans `cv/`.
3. **Journaliser sur l'issue, AVANT suppression**, le(s) nom(s) du/des fichier(s) source(s) (et date si disponible) — seule trace d'audit de l'original, non conservé.
4. Extraction **terminée et vérifiée** → **supprimer la copie de travail**. Aucun original écrit dans `cv/`. Ne jamais supprimer avant d'avoir écrit et vérifié les livrables.

## Analyse versionnée (Markdown)

Fichier à la **racine de `cv/`**, versionné par la **date du jour** : `<AAAA-MM-JJ>-<nom>-<prenom>.md`.

- Préfixe `<AAAA-MM-JJ>` = **toujours la date du jour** de l'analyse (ISO). `<nom>`/`<prenom>` en minuscules, cohérents avec le répertoire. Même jour → écrase ; autre jour → nouveau fichier.
- **Archivage** : avant d'écrire la fiche du jour, déplacer toute fiche antérieure de la racine vers `archives/`.
- `date_derniere_modification` reportée = **toujours la date du jour**, jamais la date du fichier source.
- Contenu (Markdown lisible, aucun secret) : CV source traité (nom, journalisé avant suppression), compétences avec mois d'expérience + dernière utilisation, expérience (avec `date_debut`/`date_fin`, méthodologies et technologies mobilisées par mission), **grilles d'expérience par technologie et par méthodologie** (mois d'XP calendaires + dernière utilisation, issus des agrégats collaborateur), études, équivalence MIFI (état, `niveau_equivalent_qc`, `reference_mifi`, commentaire — signaler les `a_verifier` en attente humaine), disponibilité (date + taux %), localisation (ville, région/pays — signaler ville manquante en attente humaine), langues.
- Ce fichier est un **livrable humain** : Markdown uniquement, aucun secret.

## Versionnage JSON

Fichier à la racine de `cv/` : `<nom>-<prenom>-<AAAA-MM-JJ>.json`. **Jamais écrasé** (historique conservé).

- Même jour → met à jour le fichier du jour ; autre jour → nouveau fichier.
- **Dernière version** = date encodée dans le nom la plus récente ; à défaut (dates égales), mtime la plus récente. **Seule la dernière version** est croisée avec un AO ; les versions antérieures ne le sont **jamais**.
- **Journaliser** sur l'issue le fichier JSON retenu (nom + date) et la liste des versions écartées (piste d'audit).
- **CV par défaut (scopes `standard`/`complex`/`express`)** : flux A2A → dernière version JSON ; flux de gate humain → fiche Markdown courante.

## Format de sortie (JSON → Agent)

```json
{
  "collaborateurs": [
    {
      "nom": "<prénom nom>",
      "date_derniere_modification": "<AAAA-MM-JJ — TOUJOURS la date du jour de l'analyse>",
      "source_cv": { "fichier": "<pièce jointe traitée, journalisée avant suppression>", "provenance": "issue-attachment", "conserve": false },
      "analyse_markdown": "<chemin vers <AAAA-MM-JJ>-<nom>-<prenom>.md (racine de cv/)>",
      "analyse_json": "<chemin vers <nom>-<prenom>-<AAAA-MM-JJ>.json (racine de cv/)>",
      "competences": [ { "nom": "<compétence>", "mois_experience": 0, "derniere_utilisation": "<AAAA-MM>" } ],
      "experience": [ { "client": "<client>", "projet": "<projet>", "role": "<rôle>", "date_debut": "<AAAA-MM>", "date_fin": "<AAAA-MM | present>", "duree_mois": 0, "jours_personnes": 0, "methodologies": ["<méthodologie>"], "technologies": ["<technologie>"], "description": "<courte>" } ],
      "technologies": [ { "nom": "<technologie>", "mois_experience": 0, "derniere_utilisation": "<AAAA-MM>" } ],
      "methodologies": [ { "nom": "<méthodologie>", "mois_experience": 0, "derniere_utilisation": "<AAAA-MM>" } ],
      "etudes": { "niveau": "<diplôme>", "formation": "<formation>", "etablissement": "<établissement>" },
      "mifi": {
        "equivalence_requise": "non_requise | oui | non | a_verifier",
        "diplome_origine": "<diplôme d'origine>", "pays_etudes": "<pays>",
        "niveau_equivalent_qc": "<DEC | BAC | Maîtrise | Doctorat | ... si MIFI présent, sinon null>",
        "reference_mifi": "<n° / mention MIFI ou null>", "source": "cv | humain",
        "commentaire": "<précision, ex. 'MIFI non mentionné — à confirmer par l'humain'>"
      },
      "disponibilite": { "date_disponibilite": "<AAAA-MM-JJ>", "taux_utilisation": 0 },
      "localisation": { "ville": "<OBLIGATOIRE>", "region": "<province/région ou null>", "pays": "<pays ou null>", "source": "cv | humain" },
      "langues": ["<langue>"]
    }
  ],
  "eligibilite": {
    "collaborateurs_possibles": [ { "nom": "<prénom nom>", "analyse_json": "<chemin JSON versionné retenu>" } ],
    "collaborateurs_a_verifier": [ { "nom": "<prénom nom>", "raisons": [ { "axe": "etudes | mifi | experiences | localisation | coherence", "detail": "<ex. 'MIFI a_verifier — arbitrage humain requis'>" } ] } ],
    "collaborateurs_exclus": [ { "nom": "<prénom nom>", "raisons": [ { "axe": "etudes | mifi | experiences | localisation | coherence | fraicheur_cv", "detail": "<raison précise vis-à-vis de l'AO>" } ] } ]
  }
}
```

### Champs obligatoires et règles

- **`competences`** : chaque compétence porte obligatoirement `mois_experience` (durée cumulée en mois) et `derniere_utilisation` (mois/année de dernière mobilisation) — alimentent le calcul de compatibilité côté Matcher.
- **`experience`** : chaque expérience porte `date_debut` et `date_fin` au format `AAAA-MM` (`date_fin: "present"` si la mission est en cours), en plus de `duree_mois`. Elle porte aussi `methodologies` et `technologies` (listes des méthodologies/technologies mobilisées sur cette mission). **Ne rien inventer** : une méthodologie/technologie non mentionnée dans le CV n'est pas ajoutée ; si aucune n'est mentionnée pour l'expérience, mettre `[]`.
- **`technologies` / `methodologies` (agrégats collaborateur)** : listes d'objets `{ nom, mois_experience, derniere_utilisation }` consolidant, au niveau du collaborateur, toutes les technologies/méthodologies apparaissant dans les `experience[]`.
  - `mois_experience` = **union calendaire** des périodes `date_debut`→`date_fin` de **toutes les expériences** où la techno/méthodo apparaît, exprimée en **nombre de mois distincts couverts** (unité `mois_experience`, cohérente avec `competences`). **Pas de double comptage** : deux expériences simultanées (ou chevauchantes) partageant une même techno ne comptent le mois commun **qu'une seule fois** ; l'union des intervalles mensuels est calculée avant de sommer. `date_fin: "present"` = jusqu'au mois courant. Ne jamais exprimer en années décimales dans le JSON.
  - `derniere_utilisation` = mois le plus récent (`AAAA-MM`) parmi les `date_fin` des expériences où la techno/méthodo apparaît (`present` → mois courant).
  - `[]` si aucune techno/méthodo n'apparaît dans les expériences — **ne rien inventer**.
  - Ces agrégats sont **informatifs** (remplissage de grilles, présentation humaine) et alimentent le Matcher pour la couverture technos/méthodos vis-à-vis de l'AO.
- **`date_derniere_modification` / `source_cv` / `analyse_json`** : `date_derniere_modification` = toujours la date du jour. `source_cv` documente la pièce jointe (`provenance: "issue-attachment"`, `conserve: false`) — seule trace de l'entrée supprimée. `analyse_json` pointe vers le JSON versionné ; seule la dernière version est croisée avec un AO.
- **`disponibilite`** (obligatoire) : `date_disponibilite` (ISO) + `taux_utilisation` (0–100). Un CV sans disponibilité complète est incomplet. Présence contrôlée par le sensor advisory `disponibilite-complete` à la frontière Analyse → Matching.
- **`localisation`** (obligatoire — ville) : `ville` requise, `region`/`pays` optionnels. **Si absente du CV, ne rien inventer** : poser une **mention humaine** demandant la ville, laisser `null` en attendant ; après réponse → renseigner `ville`, `source: "humain"`. Base du critère de proximité (70 km) pour AO `sur_site`/`hybride`. Présence contrôlée par le sensor advisory `localisation-complete`.
- **`mifi`** (équivalence MIFI — contexte gouvernemental Québec) — 4 états d'`equivalence_requise` :
  - `non_requise` — diplôme canadien : `niveau_equivalent_qc` = niveau tel quel.
  - `oui` — MIFI possédé : conserver `niveau_equivalent_qc` reconnu + `reference_mifi` si disponible.
  - `non` — études à l'étranger **sans** MIFI : pas d'équivalence, diplôme non comparable au niveau québécois.
  - `a_verifier` — indéterminable : **mention humaine** (ne rien inventer) ; après réponse → `oui` (+ niveau) ou `non`, `source: "humain"`.
  Règle : diplôme canadien → `non_requise` ; MIFI mentionné → `oui` + niveau ; études étrangères sans MIFI → `a_verifier` + mention humaine. Présence/cohérence contrôlées par le sensor advisory `equivalence-mifi`.

## Sélection d'éligibilité (objet `eligibilite`)

Filtre appliqué **en amont du matching** pour que le Matcher ne score que les profils pertinents : il **classe**, il ne note pas.

**Pré-requis — CV à jour et cohérents.** Vérifier que chaque CV analysé est à jour et cohérent : champs obligatoires renseignés (compétences avec `mois_experience`/`derniere_utilisation`, expérience, études, `mifi`, `disponibilite`, `localisation`). Incohérence/donnée manquante bloquante → axe `coherence` (ou `fraicheur_cv`).

**Quatre axes vis-à-vis de l'AO** (`profils_recherches` / exigences produits par `parse-ao`). **Études et Localisation sont STRICTS et ÉLIMINATOIRES** : tranchés (donnée connue/confirmée) et non atteints ⇒ `exclu` **automatique**, sans validation humaine préalable. Ils ne restent `a_verifier` **que** tant que la donnée est **non tranchée** (**ne rien inventer** : donnée manquante ⇒ mention humaine, jamais d'exclusion sur donnée inconnue) :

- **Études (STRICT, éliminatoire)** — l'AO exige un niveau (ex. BAC / DEC). Si le niveau du collaborateur — **après équivalence MIFI tranchée** (`mifi.niveau_equivalent_qc` si `equivalence_requise` ∈ {`oui`, `non_requise`}) et toute compensation d'expérience **explicitement prévue par l'AO** — n'atteint pas ce niveau ⇒ **`exclu`** (axe `etudes`). Une équivalence **tranchée `non`** (études étrangères sans équivalence reconnue) face à un niveau exigé ⇒ **`exclu`** (axe `etudes`). Reste `a_verifier` **uniquement** si l'équivalence est **non tranchée** (`a_verifier`).
- **MIFI (si nécessaire)** — AO gouvernemental Québec exigeant un niveau d'études : équivalence disponible ? `equivalence_requise = a_verifier` **non tranché** ⇒ `a_verifier` (jamais `exclu` de force sur donnée non tranchée) + mention humaine. Équivalence **tranchée `non`** face à un niveau exigé bascule sur l'axe **Études strict** ⇒ `exclu`.
- **Expériences** — l'expérience recoupe-t-elle le domaine / les compétences clés de l'AO ?
- **Localisation (STRICT, éliminatoire si présence sur site)** — AO `localisation_travail.mode` ∈ {`sur_site`, `hybride`} : collaborateur ≤ `rayon_km` (**70 km par défaut**) entre `localisation.ville` et `localisation_travail.ville_site` ? Au-delà ⇒ **`exclu`** (axe `localisation`, ex. « AO Montréal, candidat à Québec — > 70 km »). Ville du candidat **manquante** (donnée non tranchée) ⇒ `a_verifier` (jamais `exclu` de force) + mention humaine. `mode = teletravail`/`non_precise` ⇒ critère **non applicable**. Doute proche du seuil ⇒ préférer `a_verifier` + mention humaine plutôt qu'une exclusion arbitraire.

**Trois états** (mutuellement exclusifs) :

- `possible` — **retenu**, transmis au Matcher. Reporté dans `collaborateurs_possibles` avec `nom` + `analyse_json` (dernière version JSON retenue).
- `a_verifier` — **arbitrage humain requis, uniquement** lorsqu'une donnée d'un critère est **non tranchée** (MIFI non tranché, ville manquante) : **ne rien inventer**, mention humaine. Reporté dans `collaborateurs_a_verifier` avec `nom` + `raisons` (`axe` + `detail`).
- `exclu` — **écarté définitivement**. Reporté dans `collaborateurs_exclus` avec `nom` + `raisons` précises. Inclut **tout critère STRICT Études ou Localisation tranché et non atteint** — exclusion automatique, sans validation humaine préalable.

Axes de raison : `etudes`, `mifi`, `experiences`, `localisation`, `coherence`, `fraicheur_cv`. Chaque `a_verifier` et `exclu` **doit** porter au moins une raison. Le verdict d'éligibilité est le seul artefact décisionnel remonté au coordinateur pour départager les profils avant matching.

## Garde-fou — non-transmission des CV

Ne **JAMAIS** transmettre au coordinateur les sources (supprimées), les fiches Markdown ni le JSON complet. Remonter uniquement :

- le **verdict d'éligibilité** (`eligibilite` : possibles / à vérifier / exclus + raisons) ;
- pour chaque **retenu** (`possible`), la **référence `analyse_json`** — c'est le Matcher qui lira lui-même cette dernière version JSON.

Le coordinateur transmet ainsi au Matcher **uniquement la liste des retenus** ; les données CV restent dans `cv/` et ne circulent pas en A2A.
