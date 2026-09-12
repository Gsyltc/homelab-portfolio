# Workflow Matching Appels d'Offres ↔ CV des collaborateurs

> **Pour l'humain qui pilote une demande** : voir le guide d'utilisation [`docs/guide-utilisation-workflow-matching.md`](../docs/guide-utilisation-workflow-matching.md). Ce README est la documentation technique de structure.

## Vue d'ensemble

Ce workflow A2A permet de :

1. **Analyser des appels d'offres (AO)** reçus en PDF d'un client
2. **Analyser les CV des collaborateurs** (CV sources fournis en **pièces jointes de l'issue**, supprimés après extraction — non stockés)
3. **Faire le match** entre les profils recherchés dans l'AO et les profils CV, avec un **score pondéré**
4. **Remplir une grille d'évaluation client** (fournie par l'humain) après validation des profils
5. **Permettre la mise à jour des CV** par le Gestionnaire CV

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
│   └── equivalence-mifi.md             # Sensor advisory — équivalence MIFI (Analyse → Matching)
├── agents/
│   ├── coordinateur-matching-agent.md  # Coordinateur Matching
│   ├── analyste-rfp-agent.md           # Analyste RFP
│   ├── gestionnaire-cv-agent.md        # Gestionnaire CV
│   └── matcher-profils-agent.md        # Matcher Profils
└── README.md
```

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

Chaque profil CV porte un objet `mifi` (équivalence des diplômes — contexte gouvernemental Québec) à **4 états** d'`equivalence_requise` : `non_requise` (diplôme canadien), `oui` (MIFI obtenu), `non` (étranger sans équivalence), `a_verifier` (non déterminable → **mention humaine**, ne rien inventer). Voir [`agents/gestionnaire-cv-agent.md`](agents/gestionnaire-cv-agent.md).

Pour un **AO gouvernemental** (`ao.client_gouvernemental = true`), le niveau d'études requis est un **critère de conformité éliminatoire** : le Matcher croise niveau requis + équivalence MIFI + politique de compensation de l'AO (`equivalence_diplomes`) et **exclut** du classement tout collaborateur **non conforme** (`recommandation = "exclu"`, motif explicite). Cette conformité **n'altère pas** les poids du scoring immuable. Les exclusions sont **reportées dans le classement et le rapport final de livraison**. Un état `a_verifier` sur un AO gouvernemental est **signalé à l'humain**, sans exclusion automatique. Voir [`agents/matcher-profils-agent.md`](agents/matcher-profils-agent.md).

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
| Anciennes fiches d'analyse Markdown | `${ROOT_DIRECTORY}/<nom-prenom>/cv/archives/` |
| Fiche d'analyse Markdown courante (du jour) | `${ROOT_DIRECTORY}/<nom-prenom>/cv/<AAAA-MM-JJ>-<nom>-<prenom>.md` |
| Analyses JSON **versionnées** (seule la dernière sert au matching) | `${ROOT_DIRECTORY}/<nom-prenom>/cv/<nom>-<prenom>-<AAAA-MM-JJ>.json` |
| Résumés AO | `${ROOT_DIRECTORY}/ao/<client>/<titre-ao>` |
| Grille d'évaluation | Fournie par l'humain — **ne jamais inventer** |

> **Organisation stricte du répertoire `cv/`** : les CV sources sont **fournis en pièces jointes de l'issue**,
> récupérés via `multica attachment` pour l'analyse puis **supprimés** — **les originaux ne sont pas conservés**
> ni stockés dans `cv/` ; leur nom est journalisé sur l'issue avant suppression (piste d'audit). Les anciennes
> fiches d'analyse Markdown sont déplacées dans `cv/archives/` ; seuls la fiche Markdown du jour et les JSON
> versionnés restent à la racine de `cv/` et constituent la mémoire persistante du CV. La date de dernière
> modification reportée dans les livrables est **toujours la date du jour** de l'analyse. Seule la **dernière
> version JSON** est croisée avec un AO (règle de sélection et journalisation détaillées dans
> [`agents/gestionnaire-cv-agent.md`](agents/gestionnaire-cv-agent.md)).

## Utilisation

1. Créer une issue avec le tag correspondant ou mentionner le Coordinateur Matching
2. Fournir le PDF d'AO en pièce jointe
3. Le workflow se déroule automatiquement avec des points de validation humaine
4. Fournir la grille d'évaluation client quand le workflow la demande
5. Valider les profils un par un (Keep/Modify/Redo)
6. Valider la livraison finale
