# Compute Resource Consolidation

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/compute-resource-consolidation). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Consolider plusieurs tâches ou opérations dans une seule unité de calcul pour réduire les coûts et améliorer l'utilisation des ressources, au prix d'une réduction de la scalabilité fine.

## Quand l'envisager

- Lorsque l'utilisation des ressources de plusieurs petites unités de calcul est faible.
- Pour réduire les coûts d'infrastructure et la surface de gestion.
- Pour des tâches à faible charge et à besoins similaires.

## Quand ne PAS l'envisager

- Lorsque chaque tâche a des besoins de scalabilité indépendants et importants.
- Si la consolidation crée un point de défaillance unique ou une réduction de disponibilité inacceptable.
- Lorsque la gestion des versions et des déploiements de tâches disparates est problématique.

## Prérequis

### Logiciel

- Runtime unique capable d'héberger plusieurs tâches/processus (ex. instance de calcul, conteneur multi-services).

### Infrastructure

- Dimensionnement de l'unité consolidée (CPU/mémoire) pour l'ensemble des tâches hébergées.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Réduction des coûts d'infrastructure. | Scalabilité réduite par tâche. |
| Simplification des opérations et de la gestion. | Risque de contention et d'impact croisé entre tâches. |
| Meilleure utilisation des ressources. | Échec ou redéploiement affectant l'ensemble des tâches hébergées. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Optimisation des coûts | Réduction des coûts par une meilleure utilisation des ressources de calcul. |
| Excellence opérationnelle | Simplification de la gestion et du déploiement. |
| Efficacité des performances | Meilleure densité d'utilisation des ressources. |

## Source

[Patron Compute Resource Consolidation – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/compute-resource-consolidation)
