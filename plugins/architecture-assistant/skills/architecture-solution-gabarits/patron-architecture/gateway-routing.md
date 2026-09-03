# Gateway Routing

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-routing). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Router les requêtes vers plusieurs services en utilisant un seul endpoint, en exposant un point d'entrée unique qui achemine selon la requête.

## Quand l'envisager

- Pour exposer plusieurs services via un endpoint unique.
- Pour router selon le contenu de la requête (URL, en-têtes, version d'API).
- Pour faciliter la gestion des versions d'API et la mise à l'échelle des backends.

## Quand ne PAS l'envisager

- Lorsque les clients doivent accéder directement aux services sans intermédiaire.
- Si le routage simple peut être fait au niveau DNS/load balancer sans passerelle applicative.

## Prérequis

### Logiciel

- Passerelle avec règles de routage (ex. Azure API Management, Application Gateway, ALB, Envoy, Traefik).

### Infrastructure

- Passerelle redondante et enregistrement DNS unique ; monitoring des routes.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Endpoint unique et API cohérente. | Point central de défaillance potentiel. |
| Routage flexible (versions, déploiements canary, A/B). | Latence et surcoût de traitement ajoutés. |
| Découplage entre clients et infrastructure des services. | Complexité de configuration des règles de routage. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Routage redondant et capacité de redirection en cas de défaillance d'un service. |
| Excellence opérationnelle | Gouvernance des routes et gestion centralisée des versions d'API. |
| Efficacité des performances | Acheminement efficace et équilibrage vers les services. |

## Source

[Patron Gateway Routing – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-routing)
