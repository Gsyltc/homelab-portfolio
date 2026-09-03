# Materialized View

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Générer des vues pré-remplies (matérialisées) sur les données d'un ou plusieurs magasins lorsque les données sont mal formatées pour les requêtes requises, afin d'optimiser les lectures.

## Quand l'envisager

- Lorsque les requêtes sont complexes ou coûteuses sur les données source.
- Pour optimiser les lectures répétées et les rapports.
- Pour combiner des données de plusieurs sources en une vue unique.
- En combinaison avec CQRS/Event Sourcing (projections de lecture).

## Quand ne PAS l'envisager

- Lorsque les données source répondent déjà efficacement aux requêtes.
- Si la fraîcheur des données de la vue doit être immédiate (cohérence forte).
- Lorsque le coût de maintenance de la vue dépasse le bénéfice.

## Prérequis

### Logiciel

- Mécanisme de construction et de rafraîchissement des vues (projections, pipelines).

### Infrastructure

- Stockage des vues matérialisées et processus de synchronisation (ETL, events).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Performances de lecture fortement améliorées. | Cohérence éventuelle (latence de rafraîchissement). |
| Découplage du modèle de lecture du modèle source. | Stockage et coût de maintenance supplémentaires. |
| Consolidation de sources hétérogènes. | Complexité de mise à jour des vues. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Efficacité des performances | Optimisation des lectures et des requêtes coûteuses. |

## Source

[Patron Materialized View – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view)
