# Leader Election

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/leader-election). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Coordonner les actions d'une application distribuée en élisant une instance comme leader, qui gère un ensemble d'instances collaboratrices (ex. tâches planifiées, coordination).

## Quand l'envisager

- Lorsqu'une seule instance doit exécuter une tâche (ex. jobs planifiés, gestion des leases).
- Pour éviter les exécutions dupliquées ou conflictuelles dans un cluster.
- Pour la coordination d'instances dans un déploiement distribué.

## Quand ne PAS l'envisager

- Lorsque les instances sont indépendantes et ne nécessitent pas de coordination.
- Si la haute disponibilité du leader n'est pas requise.
- Lorsque l'élection introduit plus de complexité que le problème à résoudre.

## Prérequis

### Logiciel

- Mécanisme d'élection/lease (ex. ZooKeeper, etcd, Cosmos DB lease, SQL) et logique de renouvellement.

### Infrastructure

- Service de coordination disponible (consensus) ; monitoring du leader.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Évite les exécutions concurrentes et les conflits. | Complexité de mise en œuvre (leases, scénarios de partition). |
| Bascule (failover) du leader en cas de panne. | Dépendance à un service de coordination. |
| Coordination simple pour les tâches distribuées. | Fenêtre de failover pendant l'élection. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Bascule automatique et coordination sans exécution concurrente. |

## Source

[Patron Leader Election – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/leader-election)
