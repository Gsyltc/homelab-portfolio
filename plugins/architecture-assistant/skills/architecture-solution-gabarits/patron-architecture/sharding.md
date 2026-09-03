# Sharding

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/sharding). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Diviser un magasin de données en un ensemble de partitions horizontales (shards), chacune contenant un sous-ensemble des données, pour améliorer l'évolutivité et la disponibilité.

## Quand l'envisager

- Pour des magasins de données qui dépassent la capacité d'un seul nœud.
- Lorsqu'il faut améliorer l'évolutivité horizontale et la disponibilité.
- Pour répartir la charge et isoler les locataires.

## Quand ne PAS l'envisager

- Lorsqu'un seul nœud suffit pour la capacité et la charge.
- Si les requêtes nécessitent fréquemment des accès croisés entre shards.
- Lorsque la complexité de sharding dépasse les bénéfices (volumes modestes).

## Prérequis

### Logiciel

- Logique de partitionnement (clé de shard) et routage des accès (ex. partitionnement applicatif ou intégré).

### Infrastructure

- Plusieurs nœuds de stockage, répartition des shards et rebalancing.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Évolutivité horizontale et disponibilité accrues. | Complexité du partitionnement et du routage. |
| Isolation des locataires ou des domaines. | Requêtes croisées entre shards difficiles. |
| Répartition de la charge. | Rebalancing et répartition des données à gérer. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Disponibilité et capacité accrues par répartition des données. |
| Optimisation des coûts | Évolutivité par ajout de nœuds plutôt que sur-dimensionnement. |

## Source

[Patron Sharding – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/sharding)
