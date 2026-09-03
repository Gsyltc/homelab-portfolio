# Backends for Frontends

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Créer des services backend dédiés à chaque front-end (web, mobile, tablette) afin d'adapter précisément les API et le traitement aux besoins de chaque interface, au lieu d'une API générale unique.

## Quand l'envisager

- Lorsque des front-ends différents ont des besoins d'API, de format ou de volume différents.
- Pour éviter qu'une API générique ne devienne un compromis inefficace pour tous les clients.
- Quand des équipes distinctes gèrent des front-ends distincts et doivent évoluer indépendamment.

## Quand ne PAS l'envisager

- Lorsqu'un seul front-end est concerné.
- Si les clients consomment la même API avec des besoins identiques.
- Lorsque le surcoût de plusieurs backends (déploiement, maintenance) n'est pas justifié.

## Prérequis

### Logiciel

- Services backend distincts par front-end ou interfaces d'API dédiées.

### Infrastructure

- Plateforme de déploiement des backends ; idéalement un composant de routage de la couche front-end vers le backend approprié.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Optimisation de l'API et du traitement par client. | Multiples backends à construire et opérer. |
| Évolutions indépendantes de chaque backend. | Risque de duplication de logique entre les backends. |
| Réduction des échanges de données inutiles (payloads adaptés). | Répartition des responsabilités à clarifier entre équipes. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Isolation des pannes par front-end : l'impact d'un backend est limité à son interface. |
| Sécurité | Surface et contrôles d'accès adaptés à chaque type de client. |
| Efficacité des performances | API et payloads optimisés par front-end. |

## Source

[Patron Backends for Frontends – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends)
