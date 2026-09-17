# Workflow Matching Appels d'Offres ↔ CV des collaborateurs

> **Pour l'humain qui pilote une demande** : voir le guide d'utilisation du workflow. Ce README est la documentation technique de structure.

## Vue d'ensemble

Ce workflow A2A permet de :

1. **Analyser des appels d'offres (AO)** reçus en PDF d'un client
2. **Analyser les CV des collaborateurs** (CV sources fournis en **pièces jointes de l'issue**, supprimés après extraction — non stockés)
3. **Faire le match** entre les profils recherchés dans l'AO et les profils CV, avec un **score pondéré**
4. **Remplir une grille d'évaluation client** (fournie par l'humain) après validation des profils
5. **Permettre la mise à jour et la production des CV** par le Gestionnaire CV — **CV livrable au format DOCX (par défaut) produit à partir des gabarits fournis** (CV long, CV court, format client spécifique), **Markdown sur demande explicite de l'humain**

## Structure

```
matching-cv-ao/
├── common/
│   ├── conductor.md                    # Instructions du coordinateur (source unique)
│   ├── protocols/
│   │   ├── stage-definition.md         # Schéma du front-matter d'une fiche de stage
│   │   ├── stage-protocol.md           # Cycle générique d'exécution d'un stage
│   │   ├── governance-security.md      # Gouvernance A2A & garde-fous
│   │   ├── reviewer.md                 # Protocole de revue (cohérence)
│   │   └── scopes-and-axes.md          # Scopes & axes d'exécution
│   └── stages/
│       ├── initialisation/
│       │   ├── reception-ao.md         # Réception du PDF d'AO
│       │   └── chargement-cv.md        # Vérification des CV disponibles
│       ├── analyse/
│       │   ├── parse-ao.md             # Analyse de l'AO (Analyste RFP)
│       │   └── extraction-cv.md        # Extraction des CV (Gestionnaire CV)
│       ├── matching/
│       │   ├── croisement-profils.md   # Croisement profils ↔ exigences
│       │   └── classement-profils.md   # Classement final
│       ├── validation/
│       │   ├── presentation-resultats.md # Validation granulaire des profils
│       │   └── remplissage-grille.md   # Remplissage grille d'évaluation
│       └── cloture/
│           ├── livraison.md            # Livraison finale
│           └── mise-a-jour-cv.md       # Mise à jour des CV
├── scopes/                             # Source d'identité des scopes
│   ├── README.md
│   ├── standard.md                     # Scope par défaut
│   ├── complex.md                      # AO multi-profils
│   ├── express.md                      # AO simple
│   └── format-cv.md                    # Traitement CV seul (sans AO ni matching)
├── sensors/                            # Verification gates & sensors
│   ├── README.md
│   ├── gates.md                        # Gates aux frontières de phases
│   ├── disponibilite.md                # Sensor advisory — disponibilité complète (Analyse → Matching)
│   ├── equivalence-mifi.md             # Sensor advisory — équivalence MIFI (Analyse → Matching)
│   ├── localisation.md                 # Sensor advisory — localisation complète / ville candidat (Analyse → Matching)
│   └── expertise-firme.md              # Sensor advisory — expertise de firme vs référentiel clients/ (Analyse → Matching, gate humaine légère non bloquante)
├── agents/
│   ├── coordinateur-matching-agent.md  # Coordinateur Matching
│   ├── analyste-rfp-agent.md           # Analyste RFP
│   ├── gestionnaire-cv-agent.md        # Gestionnaire CV (instructions slim → charge les skills cv-analyse / cv-generation du plugin rh-assistant)
│   └── matcher-profils-agent.md        # Matcher Profils
└── README.md
```

> Les compétences du Gestionnaire CV vivent désormais dans le **plugin `rh-assistant`**
> (compétences `cv-analyse` et `cv-generation` — voir la section « Compétences (skills) »).

## Compétences (skills)

Le détail opératoire des agents est porté par des **compétences réutilisables** du **plugin `rh-assistant`**, tandis que les fiches d'agent restent volontairement **slim** (rôle, orchestration, garde-fous). Le **Gestionnaire CV** s'appuie sur les compétences suivantes ; la compétence **`contexte-client`** est **partagée** (producteur : Gestionnaire CV ; consommateurs : Analyste RFP et `cv-generation`) :

| Compétence | Rôle |
| --- | --- |
| `cv-analyse` | Extraction d'un CV source (pièce jointe) → livrables versionnés (Markdown du jour + JSON), archivage, versionnage, MIFI, localisation, disponibilité, **sélection d'éligibilité** (Études, Localisation & Certifications requises STRICTES/éliminatoires). **Producteur** du référentiel des contextes clients (via `contexte-client`) |
| `contexte-client` | **Gestion du référentiel des contextes clients** `${ROOT_DIRECTORY}/clients/<nom-client>.json` (source unique : schéma, nommage, maintenance) — contexte des sociétés + mandats réalisés par la firme. **Producteur : Gestionnaire CV** (CV long, enrichi sans écrasement, mandats dédoublonnés) ; **consommateurs en lecture seule : Analyste RFP** (expertise de firme) et `cv-generation` (bloc « Contexte de l'organisation » du CV long) |
| `cv-generation` | Production / mise à jour d'un **CV livrable au format DOCX (par défaut)** à partir des données extraites et des **gabarits fournis** (CV long / CV court / format client spécifique, dans `${ROOT_DIRECTORY}/gabarits/cv/`, jamais inventés) — **Markdown sur demande explicite** —, **après validation humaine** |

Le **schéma JSON complet** des analyses CV et les conventions de nommage/versionnage vivent dans `cv-analyse` (source unique) ; le **schéma du référentiel `clients/<nom-client>.json`** vit dans `contexte-client` (source unique) ; `cv-generation` et `rfp-analyse` s'y réfèrent sans dupliquer. Ces compétences sont fournies par le plugin `rh-assistant` et rattachées aux agents ; le workflow les référence **par leur nom**, sans dépendre de leur emplacement physique.

## Phases

| Phase | N° | Description | Gate humain |
| --- | --- | --- | --- |
| **Initialisation** | 0 | Réception AO + vérification CV | Non (bootstrap déterministe) |
| **Analyse** | 1 | Parsing AO + extraction CV | Léger |
| **Matching** | 2 | Croisement profils ↔ exigences + classement | Advisory |
| **Validation** | 3 | Validation granulaire + remplissage grille | Granulaire (Keep/Modify/Redo) |
| **Clôture** | 4 | Livraison + mise à jour CV si demandée | Explicite |

## Scoring pondéré

| Critère | Poids |
| --- | --- |
| Compétences techniques | 50% |
| Expérience en projets | 35% |
| Études | 10% |
| Disponibilité | 5% |

## Équivalence MIFI & conformité études (client gouvernemental)

Chaque profil CV porte un objet `mifi` (équivalence des diplômes — contexte gouvernemental Québec) à **4 états** d'`equivalence_requise` : `non_requise` (diplôme canadien), `oui` (MIFI obtenu), `non` (étranger sans équivalence), `a_verifier` (non déterminable → **mention humaine**, ne rien inventer). Voir l'agent `Gestionnaire CV`.

Pour un **AO gouvernemental** (`ao.client_gouvernemental = true`), le niveau d'études requis est un **critère de conformité éliminatoire** : le Matcher croise niveau requis + équivalence MIFI + politique de compensation de l'AO (`equivalence_diplomes`) et **exclut** du classement tout collaborateur **non conforme** (`recommandation = "exclu"`, motif explicite). Cette conformité **n'altère pas** les poids du scoring immuable. Les exclusions sont **reportées dans le classement et le rapport final de livraison**. Un état `a_verifier` sur un AO gouvernemental est **signalé à l'humain**, sans exclusion automatique. Voir l'agent `Matcher Profils`.

## Localisation géographique & proximité (≤ 70 km)

Chaque AO porte un objet `localisation_travail` renseigné par l'Analyste RFP : `mode` ∈ {`teletravail`, `sur_site`, `hybride`, `non_precise`}, et — pour un travail `sur_site`/`hybride` — la `ville_site` (au minimum), l'`adresse_site` si disponible, et un `rayon_km` de proximité (**70 km par défaut**). Chaque profil CV porte un objet `localisation` avec la **ville du candidat** (`localisation.ville`), champ **obligatoire** contrôlé par le sensor `localisation-complete`. Si le CV ne contient pas la ville, le Gestionnaire CV **pose une mention humaine** (ne rien inventer).

Le Gestionnaire CV applique la **localisation comme 4ᵉ axe du filtre d'éligibilité** (en plus d'Études, MIFI, Expériences) : pour un AO `sur_site`/`hybride`, un collaborateur situé à **plus de `rayon_km` (70 km par défaut)** de la `ville_site` est **`exclu`** (axe `localisation`, ex. AO `Montréal` / candidat à `Québec`). Une **ville de candidat manquante** classe le collaborateur `a_verifier` (jamais `exclu` de force) avec mention humaine. En `teletravail`/`non_precise`, ce critère **ne s'applique pas**. Comme les autres exclusions d'éligibilité, cette décision est prise **en amont** du Matcher et **n'altère pas** les poids du scoring immuable ; elle est propagée au classement et au rapport final. Voir l'agent `Gestionnaire CV`.

## Certifications requises (prérequis éliminatoire)

Chaque profil recherché de l'AO peut porter des **certifications requises** (`profils_recherches[].certifications_requises`), renseignées par l'Analyste RFP : pour chaque certification, `nom` (libellé exact, ex. `AWS Certified Solutions Architect – Associate`), `organisme` si précisé, `criticite` ∈ {`obligatoire`, `souhaitee`, `nice-to-have`} et `reference_ao`. Chaque profil CV porte, **séparément des études**, une liste `certifications[]` (`nom`, `organisme`, `annee_obtention`, `date_expiration`, `reference`).

Le Gestionnaire CV applique les **certifications requises comme axe strict/éliminatoire du filtre d'éligibilité** (en plus d'Études, MIFI, Expériences, Localisation) : lorsqu'une certification de l'AO est marquée **`obligatoire`** (prérequis/exigée), tout collaborateur qui **ne détient pas** une certification correspondante **valide** (présente et non expirée ; un simple *coursework* ne compte pas) est **`exclu`** (axe `certifications`, ex. « AO exige AWS Certified Solutions Architect – Associate — non détenue »). Une certification `souhaitee`/`nice-to-have` **n'exclut jamais** (elle alimente la couverture Compétences côté Matcher). Une détention **non tranchée** (validité/expiration incertaine dans le CV) classe le collaborateur `a_verifier` (jamais `exclu` de force) avec mention humaine — **ne rien inventer**. Si l'AO n'exige aucune certification `obligatoire`, ce critère **ne s'applique pas**. Comme les autres exclusions d'éligibilité, cette décision est prise **en amont** du Matcher et **n'altère pas** les poids du scoring immuable ; elle est propagée au classement et au rapport final. Voir l'agent `Gestionnaire CV`.

## Contextes clients (sociétés) & expertise de firme

Le workflow capitalise le **contexte des sociétés clientes** et les **mandats réalisés par la firme** dans un référentiel partagé : **un fichier JSON par client** dans `${ROOT_DIRECTORY}/clients/<nom-client>.json`. La compétence dédiée **`contexte-client`** (plugin `rh-assistant`) en est la **source unique** (schéma, nommage, règles de maintenance et contrat de lecture). Chaque fichier porte le **nom du client**, son **contexte** (secteur, mission, enjeux) et la liste des **mandats réalisés** — pour chaque mandat : collaborateur, rôle, projet (si disponible), dates, jours-personnes, contexte du projet, tâches réalisées et technologies utilisées.

- **Producteur — Gestionnaire CV** : lors de l'analyse d'un **CV long contenant un contexte client** (blocs « Contexte de l'organisation »/« Contexte du projet »), le Gestionnaire CV **crée ou complète/enrichit** `clients/<nom-client>.json` **via la compétence `contexte-client`** — **jamais d'écrasement aveugle** : le contexte est complété quand c'est pertinent, les mandats ajoutés ou dédoublonnés. Voir les compétences `contexte-client` (source unique) et `cv-analyse` (producteur), ainsi que l'agent `Gestionnaire CV`. Le contexte client alimente aussi le **CV long** (bloc « Contexte de l'organisation », en lecture seule côté génération).
- **Consommateur — Analyste RFP** : lorsqu'un AO exige une **expertise/expérience de firme** (mandats similaires, secteur, technologies ou contexte comparables), l'Analyste RFP **lit** le référentiel `clients/*.json` (compétence `contexte-client`, lecture seule) et produit un objet `expertise_firme` (`verdict` ∈ {`conforme`, `minimums_non_atteints`, `indeterminable`}). Voir les compétences `rfp-analyse` et `contexte-client`, ainsi que l'agent `Analyste RFP`.
- **Non bloquant + gate humaine légère** : cette évaluation **n'arrête jamais** le workflow. Si les minimums requis ne sont pas atteints, une **gate humaine légère** est levée (signalement + confirmation légère), doublée par le sensor advisory `expertise-firme`. L'humain reste seul décideur (poursuivre malgré le manque, ou compléter le référentiel `clients/`).

## Agents

| Agent | Rôle |
| --- | --- |
| **Coordinateur Matching** | Orchestre le flux complet, contrôle les livrables |
| **Analyste RFP** | Parse les PDF d'AO, extrait exigences + profils |
| **Gestionnaire CV** | Lit et met à jour les CV des collaborateurs |
| **Matcher Profils** | Croise profils ↔ exigences, calcule le score pondéré |

## Communication

- **Agent ↔ Agent** : JSON uniquement
- **Agent ↔ Humain** : Markdown uniquement

## Stockage

| Élément | Emplacement |
| --- | --- |
| CV sources (PDF, DOCX) | **Pièces jointes de l'issue** — récupérés via `multica attachment`, **supprimés après extraction** (non stockés) |
| **Gabarits CV fournis** (CV long / CV court / format client spécifique) | `${ROOT_DIRECTORY}/gabarits/cv/` — **fournis par l'humain, jamais inventés** |
| Anciennes fiches d'analyse Markdown | `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/archives/` |
| Fiche d'analyse Markdown courante (du jour, mémoire) | `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/<AAAA-MM-JJ>-<nom>-<prenom>.md` |
| Analyses JSON **versionnées** (mémoire ; seule la dernière sert au matching) | `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/<nom>-<prenom>-<AAAA-MM-JJ>.json` |
| **CV livrable** (DOCX par défaut depuis un gabarit ; Markdown sur demande explicite) | `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/<nom>-<prenom>-<type-gabarit>-<AAAA-MM-JJ>.docx` (ou `…-cv-<AAAA-MM-JJ>.md`) |
| Résumés AO | `${ROOT_DIRECTORY}/ao/<client>/<titre-ao>` |
| **Référentiel des contextes clients** (1 fichier par client — contexte de la société + mandats réalisés) | `${ROOT_DIRECTORY}/clients/<nom-client>.json` — **maintenu par le Gestionnaire CV** (CV long avec contexte client, complété/enrichi jamais écrasé) ; **exploité par l'Analyste RFP** pour l'expertise de firme |
| Grille d'évaluation | Fournie par l'humain — **ne jamais inventer** |

> **Enracinement des chemins (`${ROOT_DIRECTORY}`)** : le répertoire de travail du workspace est
> `${ROOT_DIRECTORY}`. **Tous les chemins relatifs du workflow sont enracinés sur `${ROOT_DIRECTORY}`**
> (collaborateurs, AO, gabarits) ; ne jamais utiliser un chemin absolu hors `${ROOT_DIRECTORY}` ni un chemin
> relatif non enraciné.

> **Format du CV livrable — DOCX par défaut, Markdown sur demande explicite** : le **CV livrable** remis à
> l'humain / au client est **par défaut un DOCX** produit à partir d'un des **gabarits fournis** (CV long, CV
> court, format client spécifique) rangés dans `${ROOT_DIRECTORY}/gabarits/cv/` — **jamais inventé** ; gabarit
> absent ⇒ halt-and-ask (pas de repli Markdown automatique). Le **format Markdown reste possible uniquement sur
> demande explicite de l'humain**. La fiche d'analyse Markdown et le JSON restent la **mémoire interne**
> (données), distincts du CV livrable. Voir la compétence `cv-generation`.

> **Organisation stricte du répertoire `cv/`** : les CV sources sont **fournis en pièces jointes de l'issue**,
> récupérés via `multica attachment` pour l'analyse puis **supprimés** — **les originaux ne sont pas conservés**
> ni stockés dans `cv/` ; leur nom est journalisé sur l'issue avant suppression (piste d'audit). Les anciennes
> fiches d'analyse Markdown sont déplacées dans `cv/archives/` ; la fiche Markdown du jour et les JSON
> versionnés restent à la racine de `cv/` et constituent la mémoire persistante du CV ; le **CV livrable DOCX**
> produit depuis un gabarit fourni y est également écrit (versionné). La date de dernière
> modification reportée dans les livrables est **toujours la date du jour** de l'analyse. Seule la **dernière
> version JSON** est croisée avec un AO (règle de sélection et journalisation détaillées dans
> l'agent `Gestionnaire CV`).

## Utilisation

1. Créer une issue avec le tag correspondant ou mentionner le Coordinateur Matching
2. Fournir le PDF d'AO en pièce jointe
3. Le workflow se déroule automatiquement avec des points de validation humaine
4. Fournir la grille d'évaluation client quand le workflow la demande
5. Valider les profils un par un (Keep/Modify/Redo)
6. Valider la livraison finale
