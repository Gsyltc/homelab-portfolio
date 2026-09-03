# Competing Consumers

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/competing-consumers). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Permettre à plusieurs consommateurs concurrents de traiter les messages reçus sur le même canal de messagerie, pour faire évoluer le traitement et améliorer le débit.

## Quand l'envisager

- Lorsque la charge de traitement des messages dépasse la capacité d'un seul consommateur.
- Pour atteindre l'évolutivité horizontale du traitement.
- Lorsque l'ordre de traitement n'est pas critique ou peut être géré par partitionnement.

## Quand ne PAS l'envisager

- Lorsqu'un ordre strict de traitement est requis (voir Sequential Convoy).
- Si les messages doivent être traités par un seul consommateur (ressources partagées).
- Lorsque le coût d'instances supplémentaires n'est pas justifié par la charge.

## Prérequis

### Logiciel

- Canal de messagerie qui remet chaque message à un seul consommateur (ex. Azure Service Bus, SQS).

### Infrastructure

- Plusieurs instances de consommateurs (pools) et capacité de scale-out.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Évolutivité horizontale du traitement des messages. | Gestion de l'ordre et de l'idempotence nécessaire. |
| Meilleure utilisation des ressources. | Complexité de coordination (sessions, partitions). |
| Résilience : si un consommateur échoue, les autres continuent. | Coût des instances supplémentaires. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Poursuite du traitement si un consommateur tombe ; gestion des échecs de message. |
| Optimisation des coûts | Mise à l'échelle élastique du traitement selon la charge. |
| Efficacité des performances | Augmentation du débit par le traitement parallèle. |

## Source

[Patron Competing Consumers – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/competing-consumers)
