# Workflow Matching Appels d'Offres ↔ CV des collaborateurs

> **Pour l'humain qui pilote une demande** : voir le guide d'utilisation [`docs/guide-utilisation-workflow-matching.md`](../docs/guide-utilisation-workflow-matching.md). Ce README est la documentation technique de structure.

## Vue d'ensemble

Ce workflow A2A permet de :

1. **Analyser des appels d'offres (AO)** reçus en PDF d'un client
2. **Analyser les CV des collaborateurs** (stockés dans `/nfs/workspace/expertise-architecture/<nom-prenom>/cv`)
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
│   └── gates.md                        # Gates aux frontières de phases
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
| CV collaborateurs | `/nfs/workspace/expertise-architecture/<nom-prenom>/cv` |
| Résumés AO | `/nfs/workspace/expertise-architecture/ao/<client>/<titre-ao>` |
| Grille d'évaluation | Fournie par l'humain — **ne jamais inventer** |

## Utilisation

1. Créer une issue avec le tag correspondant ou mentionner le Coordinateur Matching
2. Fournir le PDF d'AO en pièce jointe
3. Le workflow se déroule automatiquement avec des points de validation humaine
4. Fournir la grille d'évaluation client quand le workflow la demande
5. Valider les profils un par un (Keep/Modify/Redo)
6. Valider la livraison finale
