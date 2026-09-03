# Index Table

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/index-table). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Créer des index sur les champs des magasins de données que les requêtes référencent fréquemment, pour accélérer les recherches.

## Quand l'envisager

- Lorsque les requêtes de recherche ciblent des champs non-clés fréquemment.
- Pour des magasins de données dont la recherche par clé ne suffit pas (ex. NoSQL).
- Pour améliorer la latence des requêtes répétitives.

## Quand ne PAS l'envisager

- Lorsque les magasins de données supportent déjà des index natifs suffisants.
- Si le coût de maintenance des index et de duplication des données dépasse le bénéfice.
- Pour des volumes très faibles où les scans sont acceptables.

## Prérequis

### Logiciel

- Gestion des index applicatifs (tables d'index) ou index natifs du magasin.

### Infrastructure

- Stockage supplémentaire pour les index et processus de synchronisation/cohérence.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Accélération des requêtes de recherche. | Coût de stockage et de maintenance des index. |
| Réduction des scans coûteux. | Complexité de synchronisation (cohérence des index). |
| Améliore la scalabilité des lectures. | Surcoût d'écriture lors des mises à jour. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Réduction des dégradations de performance et de la charge sur les magasins. |
| Efficacité des performances | Latence de lecture réduite grâce aux index. |

## Source

[Patron Index Table – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/index-table)
