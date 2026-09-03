# Gateway Aggregation

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Utiliser une passerelle pour agréger plusieurs requêtes individuelles en une seule requête, réduisant ainsi les interactions entre le client et le backend.

## Quand l'envisager

- Lorsqu'un client doit interroger plusieurs services pour accomplir une tâche.
- Pour réduire la latence et le nombre d'appels réseau côté client.
- Pour simplifier les API exposées au client.

## Quand ne PAS l'envisager

- Lorsque les services sont déjà agrégés ou que les appels sont rares.
- Si l'agrégation couplée introduit une dépendance indésirable entre les services.
- Lorsque la logique d'agrégation complexe est mieux gérée côté client.

## Prérequis

### Logiciel

- Composant de passerelle avec logique d'agrégation (orchestration d'appels aux services).

### Infrastructure

- Passerelle API (ex. Azure API Management, AWS API Gateway) ou serveur d'applications dédié, dimensionnée au trafic.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Réduction des allers-retours réseau et de la latence perçue. | Couplage de la passerelle à la logique métier. |
| API simplifiée pour les clients. | Point de défaillance et de goulot d'étranglement potentiel. |
| Masque la structure interne des services. | Complexité de maintenance de l'agrégation. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Réduction des points de défaillance réseau et des requêtes vers les backends. |
| Sécurité | Réduction de la surface d'exposition des backends. |
| Excellence opérationnelle | API cohérente et gouvernée par la passerelle. |
| Efficacité des performances | Moins de latence et d'appels réseau pour le client. |

## Source

[Patron Gateway Aggregation – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation)
