# Publisher-Subscriber

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Permettre à une application d'annoncer des événements à plusieurs consommateurs de manière asynchrone, sans coupler les expéditeurs aux récepteurs.

## Quand l'envisager

- Pour notifier plusieurs consommateurs d'un même événement sans les connaître.
- Pour découpler les producteurs et les consommateurs d'événements.
- Pour ajouter de nouveaux consommateurs sans modifier les producteurs.

## Quand ne PAS l'envisager

- Lorsqu'un seul consommateur est concerné (un file direct suffit).
- Si la livraison synchrone et l'acquittement immédiat sont requis.
- Lorsque la complexité du bus n'est pas justifiée.

## Prérequis

### Logiciel

- Bus événementiel ou topic (ex. Azure Event Grid, Service Bus Topics, SNS, Kafka) et contrats d'événements.

### Infrastructure

- Infrastructure de messagerie fiable, persistante, avec gestion des erreurs (DLQ) et monitoring.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Couplage faible entre producteurs et consommateurs. | Latence de livraison (asynchrone). |
| Évolutivité et ajout de consommateurs simple. | Complexité de gestion des événements (versioning, ordre, idempotence). |
| Traitement asynchrone et parallèle. | Surcharge de traitement pour les événements non consommés. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Livraison asynchrone robuste et reprise des événements en erreur (DLQ). |
| Sécurité | Contrôle des accès à la publication et à l'abonnement. |
| Optimisation des coûts | Consommation à la demande, réduction des appels synchrones coûteux. |
| Excellence opérationnelle | Gouvernance centralisée des événements et de leurs contrats. |
| Efficacité des performances | Traitement parallèle et asynchrone des événements. |

## Source

[Patron Publisher-Subscriber – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber)
