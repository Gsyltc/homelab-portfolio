---
name: openspec-workflow
description: "Workflow complet OpenSpec (SDD) : templates d'artefacts, structure d'arborescence, format de specs GIVEN/WHEN/THEN, procédures d'initialisation, proposition, application et archivage. Utiliser pour créer ou gérer une arborescence OpenSpec dans un projet."
---

# OpenSpec Workflow

Skill de référence pour appliquer la méthode OpenSpec (Spec-Driven Development) dans un projet.
OpenSpec est un framework léger de spécifications piloté par l'IA, où les specs vivent dans le code et servent d'alignement entre humains et agents.

## Philosophie

- Fluide, pas rigide
- Itératif, pas waterfall
- Simple, pas complexe
- Conçu pour le brownfield (projets existants), pas seulement le greenfield
- Scalable du projet personnel à l'entreprise

## Arborescence OpenSpec

Après initialisation (`openspec init`), la structure suivante est créée à la racine du projet :

```
openspec/
├── config.json              ← Configuration du projet OpenSpec
├── specs/                   ← Spécifications vivantes, organisées par capacité
│   └── <capability-name>/
│       └── spec.md          ← Requirements + scénarios pour cette capacité
└── changes/                 ← Propositions de changements (en cours)
    ├── <change-name>/       ← Un changement = un dossier
    │   ├── proposal.md      ← Pourquoi ce changement, ce qui change
    │   ├── design.md        ← Décisions techniques, approche retenue
    │   ├── tasks.md         ← Checklist d'implémentation par phase
    │   └── specs/           ← Deltas de specs (ajouts/modifications)
    │       └── <capability>/
    │           └── spec.md
    └── archive/             ← Changements terminés et archivés
        └── YYYY-MM-DD-<change-name>/
            └── ...          ← Même structure que le changement actif
```

## Template : config.json

```json
{
  "version": "1.0",
  "language": "fr",
  "spec_dir": "openspec/specs",
  "changes_dir": "openspec/changes"
}
```

## Template : spec.md (spécification d'une capacité)

```markdown
# <capability-name> Specification

## Purpose

<Description concise de la capacité métier couverte par cette spec.>

## Requirements

### Requirement: <Nom du requirement>

The system SHALL <comportement attendu décrit de manière précise>.

#### Scenario: <Nom du scénario>

- **GIVEN** <contexte initial / état du système>
- **WHEN** <action ou événement déclencheur>
- **THEN** <résultat attendu / comportement observable>
- **AND** <condition additionnelle si nécessaire>

### Requirement: <Autre requirement>

The system SHALL <autre comportement>.

#### Scenario: <Cas nominal>

- **GIVEN** <contexte>
- **WHEN** <action>
- **THEN** <résultat>

#### Scenario: <Cas d'erreur>

- **GIVEN** <contexte>
- **WHEN** <action invalide>
- **THEN** <gestion d'erreur attendue>
```

## Template : proposal.md

```markdown
# Proposal: <nom-du-changement>

## Summary

<Une phrase décrivant le changement proposé.>

## Motivation

<Pourquoi ce changement est nécessaire. Quel problème résout-il ?>

## Scope

### In scope

- <Ce qui est inclus dans ce changement>

### Out of scope

- <Ce qui est explicitement exclu>

## Impact

### Specs affected

- `openspec/specs/<capability>/spec.md` — <nature de la modification>

### Components affected

- <Fichiers/modules/services impactés>

## Open Questions

- <Questions non résolues à clarifier avant implémentation>
```

## Template : design.md

```markdown
# Design: <nom-du-changement>

## Approach

<Description de l'approche technique retenue.>

## Alternatives Considered

### Alternative 1: <nom>

- **Pros:** <avantages>
- **Cons:** <inconvénients>
- **Why rejected:** <raison du rejet>

## Technical Decisions

### Decision 1: <sujet>

- **Choice:** <option retenue>
- **Rationale:** <justification>

## Dependencies

- <Dépendances techniques nécessaires>

## Risks

- <Risques identifiés et mitigations>
```

## Template : tasks.md

```markdown
# Tasks: <nom-du-changement>

## Phase 1: <nom de la phase>

- [ ] 1.1 <Tâche descriptive>
- [ ] 1.2 <Tâche descriptive>
- [ ] 1.3 <Tâche descriptive>

## Phase 2: <nom de la phase>

- [ ] 2.1 <Tâche descriptive>
- [ ] 2.2 <Tâche descriptive>

## Phase 3: Validation

- [ ] 3.1 Vérifier que les specs sont respectées
- [ ] 3.2 Mettre à jour les specs principales si nécessaire
- [ ] 3.3 Archiver le changement
```

## Procédures

### Initialiser OpenSpec dans un projet

1. Créer le dossier `openspec/` à la racine du projet
2. Créer `openspec/config.json` avec le template ci-dessus
3. Créer `openspec/specs/` (vide, les specs se créent au fil de l'eau)
4. Créer `openspec/changes/` (vide)
5. Créer `openspec/changes/archive/` (vide)
6. Ajouter un `.gitkeep` dans les dossiers vides si nécessaire

### Proposer un changement

1. Nommer le changement en kebab-case descriptif (ex: `add-dark-mode`, `session-expiration`)
2. Créer `openspec/changes/<nom>/`
3. Rédiger `proposal.md` — décrire le pourquoi et le quoi
4. Identifier les capacités impactées et créer `specs/<capability>/spec.md` dans le dossier du changement
5. Rédiger `design.md` — documenter l'approche technique
6. Rédiger `tasks.md` — découper en phases et tâches concrètes
7. **Faire valider le plan avant toute implémentation**

### Appliquer un changement

1. Suivre les tâches de `tasks.md` dans l'ordre des phases
2. Cocher chaque tâche au fur et à mesure (`- [x]`)
3. Mettre à jour les specs si des ajustements sont nécessaires en cours de route

### Archiver un changement terminé

1. Déplacer le dossier du changement vers `openspec/changes/archive/YYYY-MM-DD-<nom>/`
2. Fusionner les deltas de specs dans les specs principales (`openspec/specs/`)
3. Vérifier la cohérence globale des specs

## Conventions de nommage

- **Capabilities** : kebab-case, nom de la capacité métier (ex: `auth-session`, `checkout-payment`, `user-profile`)
- **Changes** : kebab-case, verbe + objet (ex: `add-remember-me`, `fix-session-timeout`, `migrate-to-postgres`)
- **Requirements** : titre court commençant par un nom (ex: "Session expiration", "Password complexity")
- **Scénarios** : titre descriptif du cas (ex: "Default session timeout", "Invalid password attempt")

## Mots-clés réservés (en anglais)

| Mot-clé | Usage |
|---------|-------|
| SHALL | Exigence obligatoire |
| SHOULD | Recommandation |
| MAY | Option |
| GIVEN | Contexte du scénario |
| WHEN | Action/événement déclencheur |
| THEN | Résultat attendu |
| AND | Condition additionnelle |

## Bonnes pratiques

- Les specs sont des documents vivants : les mettre à jour à chaque changement
- Un changement = un dossier isolé, même s'il impacte plusieurs capabilities
- Toujours faire valider `proposal.md` avant de commencer l'implémentation
- Les specs restent dans le repo git, aux côtés du code
- Garder les specs simples et concrètes — éviter le sur-engineering documentaire
- Créer les specs au fil de l'eau, pas toutes d'un coup pour un projet existant
