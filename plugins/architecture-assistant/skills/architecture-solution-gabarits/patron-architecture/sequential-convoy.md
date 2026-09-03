# Sequential Convoy

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/sequential-convoy). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Traiter un ensemble de messages liés dans un ordre défini sans bloquer les autres groupes de messages, en utilisant des sessions ou des partitions par groupe.

## Quand l'envisager

- Lorsque des messages liés doivent être traités dans l'ordre (ex. événements d'une même entité).
- Pour garantir l'ordre tout en permettant le parallélisme entre groupes.
- Lorsque l'ordre est important pour la cohérence des données métier.

## Quand ne PAS l'envisager

- Lorsque l'ordre de traitement n'a pas d'importance.
- Si tous les messages peuvent être traités en parallèle sans contrainte d'ordre.
- Lorsque la capacité du mécanisme de séquençage limite inutilement le débit.

## Prérequis

### Logiciel

- Messagerie avec sessions/partitions (ex. Azure Service Bus sessions, Kafka partitions, SQS FIFO).

### Infrastructure

- Infrastructure de messagerie avec support d'ordre par groupe et monitoring des groupes bloqués.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Ordre de traitement garanti pour les groupes liés. | Limite le parallélisme à l'intérieur d'un groupe. |
| Parallélisme entre groupes indépendants. | Gestion des sessions et des groupes nécessaire. |
| Simplifie la logique de cohérence. | Risque de blocage si un message d'un groupe est en erreur. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Cohérence des données garantie par l'ordre de traitement des messages liés. |

## Source

[Patron Sequential Convoy – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/sequential-convoy)
