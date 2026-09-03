# Bulkhead

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Isoler les éléments d'une application dans des pools (cloisons) afin qu'une panne dans un pool n'affecte pas les autres : chaque pool dispose de ses propres ressources (connexions, threads, mémoire).

## Quand l'envisager

- Pour isoler des flux ou clients critiques des flux moins critiques dans une même application.
- Pour limiter la consommation de ressources d'un consommateur donné.
- Lorsque la tolérance aux pannes par segment (ex. par client, par service) est un besoin.

## Quand ne PAS l'envisager

- Lorsque les coûts de provisionnement de ressources supplémentaires sont prohibitifs.
- Si la complexité de gestion des pools n'apporte pas de bénéfice pour des flux homogènes.

## Prérequis

### Logiciel

- Gestion des pools de ressources dans le runtime (pools de connexions, limites de threads, conteneurs).

### Infrastructure

- Ressources suffisantes pour provisionner plusieurs pools ou instances isolées.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Contient les pannes et empêche les défaillances en cascade. | Augmente l'utilisation des ressources (réservation par pool). |
| Isolement des consommateurs bruyants. | Complexité d'opération et de dimensionnement accrue. |
| Améliore la disponibilité perçue des flux isolés. | Risque de sous-utilisation si les pools sont trop segmentés. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Contention des pannes : un pool en défaillance n'impacte pas les autres pools. |
| Sécurité | Limitation des ressources accessibles à chaque segment, réduction des risques d'épuisement mutualisé. |
| Efficacité des performances | Prévention d'un consommateur monopolisant les ressources au détriment des autres. |

## Source

[Patron Bulkhead – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead)
