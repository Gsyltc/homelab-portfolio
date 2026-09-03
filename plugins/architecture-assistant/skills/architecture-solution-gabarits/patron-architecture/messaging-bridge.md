# Messaging Bridge

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/messaging-bridge). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Construire un intermédiaire (pont) pour permettre la communication entre des systèmes de messagerie incompatibles (protocoles, formats ou clouds différents).

## Quand l'envisager

- Lorsqu'il faut connecter des systèmes de messagerie hétérogènes (ex. Azure Service Bus ↔ AWS SQS, Kafka ↔ bus).
- Pour réutiliser des messages existants sans réécrire les systèmes sources.
- Lors de migrations ou de fusions d'infrastructures de messagerie.

## Quand ne PAS l'envisager

- Lorsqu'un seul système de messagerie peut être standardisé.
- Si la traduction des messages peut être faite directement chez le consommateur.
- Lorsque le pont introduit plus de complexité que la coexistence des systèmes.

## Prérequis

### Logiciel

- Composant de pont (bridge) réalisant la traduction des protocoles et formats, avec gestion des erreurs.

### Infrastructure

- Accès réseau et accréditations vers les deux systèmes de messagerie ; surveillance du pont.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Interopérabilité entre systèmes hétérogènes. | Point de défaillance et de latence supplémentaire. |
| Évite la réécriture des systèmes existants. | Traduction de formats à maintenir. |
| Facilite les migrations incrémentales. | Complexité de monitoring et de reprise. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Optimisation des coûts | Réutilisation des systèmes existants au lieu d'une réécriture coûteuse. |
| Excellence opérationnelle | Gouvernance centralisée de l'interconnexion des messageries. |

## Source

[Patron Messaging Bridge – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/messaging-bridge)
