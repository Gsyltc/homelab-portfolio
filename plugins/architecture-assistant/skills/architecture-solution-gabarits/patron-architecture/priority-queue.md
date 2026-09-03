# Priority Queue

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/priority-queue). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Prioriser les requêtes envoyées aux services afin que les requêtes de priorité élevée soient traitées plus rapidement que celles de priorité basse.

## Quand l'envisager

- Lorsque toutes les requêtes n'ont pas la même importance et que la capacité de traitement est limitée.
- Pour garantir que les opérations critiques soient traitées avant les opérations non critiques.
- Pour protéger les services de la surcharge pendant les pics.

## Quand ne PAS l'envisager

- Lorsque toutes les requêtes ont la même priorité.
- Si les requêtes de priorité basse pourraient ne jamais être traitées (famine) dans les conditions de charge.
- Lorsque l'ordre FIFO strict est requis.

## Prérequis

### Logiciel

- File de messages avec support de priorité ou plusieurs files (par niveau) et logique de routage.

### Infrastructure

- Files de messages dimensionnées et capacité de traitement suffisante pour les requêtes prioritaires.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Garantit le traitement des requêtes critiques. | Risque de famine des requêtes de priorité basse. |
| Améliore l'expérience des opérations importantes sous charge. | Complexité de gestion des files multiples. |
| Protège les services contre la saturation. | Nécessite des mécanismes de surveillance et d'anti-famine. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Traitement garanti des opérations critiques sous charge. |
| Efficacité des performances | Meilleure réactivité des requêtes prioritaires. |

## Source

[Patron Priority Queue – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/priority-queue)
