# CQRS

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Séparer les opérations de lecture des opérations d'écriture (mise à jour) en utilisant des interfaces distinctes, voire des modèles et des magasins de données séparés.

## Quand l'envisager

- Lorsque les lectures et les écritures ont des exigences de performance et de scalabilité très différentes.
- Pour des modèles de domaine complexes avec des charges de lecture/écriture déséquilibrées.
- Pour faire évoluer indépendamment les chemins de lecture et d'écriture.

## Quand ne PAS l'envisager

- Pour des CRUD simples où la séparation n'apporte pas de bénéfice.
- Lorsque la complexité de synchronisation (matérialisation, CQRS events) dépasse le bénéfice.
- Si la cohérence forte entre les lectures et les écritures est obligatoire.

## Prérequis

### Logiciel

- Modèles de lecture et d'écriture distincts ; éventuellement des magasins de données séparés et une synchronisation (ex. Event Sourcing).

### Infrastructure

- Magasins de données adaptés aux deux charges (optimisé lecture vs écriture) et canal de synchronisation si séparés.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Optimisation indépendante des lectures et des écritures. | Complexité accrue (deux modèles, synchronisation). |
| Scalabilité et évolutions découplées. | Cohérence éventuelle à gérer. |
| Contrats d'écriture simplifiés (commande plutôt que CRUD). | Nécessite une discipline de conception solide. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Efficacité des performances | Optimisation indépendante de la charge de lecture et de la charge d'écriture. |

## Source

[Patron CQRS – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
