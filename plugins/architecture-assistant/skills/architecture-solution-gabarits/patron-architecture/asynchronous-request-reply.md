# Asynchronous Request-Reply

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/asynchronous-request-reply). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Découpler le traitement du backend de l'hôte front-end : le traitement long est fait en asynchrone, mais le front-end reçoit une réponse claire et rapide (acquittement + vérification de l'état par requête).

## Quand l'envisager

- Lorsque le backend a besoin de temps pour traiter une requête alors que le front-end attend une réponse rapide.
- Pour des opérations longues (génération de rapports, batch, appels à des services lents).
- Lorsqu'il faut fournir un acquittement immédiat puis notifier/permettre la consultation du résultat.

## Quand ne PAS l'envisager

- Lorsque la latence de traitement est faible et compatible avec un appel synchrone.
- Si le client ne peut pas gérer les états intermédiaires (pending/completed).
- Lorsque la complexité de la file et du suivi d'état n'est pas justifiée par le besoin.

## Prérequis

### Logiciel

- Composant de file d'attente ou de bus (ex. Azure Service Bus, Storage Queue, SQS) et mécanisme d'état de requête.

### Infrastructure

- API HTTP ou serveur exposant des endpoints de vérification d'état ; stockage persistant de l'état des requêtes.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Temps de réponse rapide pour l'utilisateur. | Plus grande complexité (suivi d'état, polling ou notification). |
| Lissage des pics de charge (traitement en file). | Latence totale de l'opération augmentée. |
| Découplage temporel entre le front-end et le backend. | Gestion nécessaire de l'expiration et de la purge des requêtes. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Efficacité des performances | Réduit la latence ressentie par l'utilisateur et équilibre la charge du backend. |

## Source

[Patron Asynchronous Request-Reply – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/asynchronous-request-reply)
