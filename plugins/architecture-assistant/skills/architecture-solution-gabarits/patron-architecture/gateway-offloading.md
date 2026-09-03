# Gateway Offloading

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-offloading). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Décharger des fonctionnalités partagées ou spécialisées (TLS, authentification, mise en cache, logs) vers une passerelle proxy, pour alléger les backends.

## Quand l'envisager

- Pour centraliser des préoccupations transversales communes à plusieurs services (TLS, auth, CORS, throttling).
- Pour simplifier les backends et uniformiser leur interface.
- Pour réduire la charge des backends en déléguant le traitement à la passerelle.

## Quand ne PAS l'envisager

- Lorsque chaque backend a des besoins spécifiques qui rendent le déchargement inadapté.
- Si la passerelle devient trop volumineuse ou difficile à opérer.
- Lorsque la fonctionnalité doit être proche des données pour des raisons de performance ou de sécurité.

## Prérequis

### Logiciel

- Passerelle configurable (ex. Azure API Management, Application Gateway, AWS ALB/API Gateway, Envoy).

### Infrastructure

- Infrastructure de passerelle redondante ; gestion des certificats et des secrets (TLS, auth).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Uniformise et centralise les préoccupations transversales. | Dépendance à la passerelle (disponibilité, latence). |
| Simplifie les backends. | Complexité de configuration et d'exploitation. |
| Améliore la sécurité et la cohérence (terminaison TLS, auth centralisée). | Fonctionnalités de la passerelle limitées à ce qu'elle supporte. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Centralisation de la gestion des pannes et de la disponibilité (retries, timeouts). |
| Sécurité | Terminaison TLS, authentification et politiques de sécurité centralisées. |
| Optimisation des coûts | Réduction des ressources des backends (TLS, caching délégués). |
| Excellence opérationnelle | Gouvernance centralisée des API et des politiques. |
| Efficacité des performances | Caching et optimisations appliquées en un point. |

## Source

[Patron Gateway Offloading – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-offloading)
