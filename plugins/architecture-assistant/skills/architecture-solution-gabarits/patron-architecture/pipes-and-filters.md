# Pipes and Filters

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Décomposer une tâche qui effectue un traitement complexe en une série d'éléments séparés et réutilisables (filtres) reliés par des canaux (pipes).

## Quand l'envisager

- Pour structurer un traitement en étapes distinctes, réutilisables et combinables.
- Lorsque chaque étape peut être mise à l'échelle ou modifiée indépendamment.
- Pour des pipelines de traitement de données ou de messages.

## Quand ne PAS l'envisager

- Lorsque le traitement est simple et ne mérite pas d'être découpé.
- Si le découpage ajoute de la latence ou de la complexité inutile.
- Lorsque les étapes doivent être atomiques et transactionnelles.

## Prérequis

### Logiciel

- Composants de filtres et de pipes (queues, flux) ; format de données intermédiaire stable.

### Infrastructure

- Canaux de transport entre filtres (files de messages, flux) dimensionnés au volume.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Réutilisabilité et testabilité des étapes. | Latence accrue entre les étapes. |
| Évolutivité indépendante des filtres. | Complexité de gestion des canaux. |
| Maintenabilité (étapes découplées). | Format de données intermédiaire à stabiliser et versionner. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Isolation et reprise par étape (chaque filtre peut être redémarré). |

## Source

[Patron Pipes and Filters – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters)
