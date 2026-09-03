# Valet Key

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/valet-key). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Utiliser un jeton ou une clé (valet key) pour fournir aux clients un accès direct et restreint à une ressource ou un service spécifique, sans passer par le serveur applicatif.

## Quand l'envisager

- Pour permettre l'upload/download direct de fichiers par les clients (ex. SAS, presigned URLs).
- Pour réduire la charge et la latence du serveur applicatif.
- Pour restreindre l'accès à des ressources précises avec expiration.

## Quand ne PAS l'envisager

- Lorsque le contrôle de chaque opération doit rester côté serveur.
- Si l'émission et la révocation des clés ne peuvent pas être gérées de façon sécurisée.
- Lorsque les clients ne peuvent pas être fiabilisés pour utiliser les clés correctement.

## Prérequis

### Logiciel

- Génération et signature de jetons (ex. SAS Azure, presigned URL AWS, JWT) avec permissions et expiration.

### Infrastructure

- Service de stockage ou de ressources supportant les accès délégués ; gestion des clés de signature.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Réduit la charge et la latence du serveur. | Contrôle moindre sur les opérations (hors serveur). |
| Accès direct et performant (bande passante). | Gestion de l'émission, de la révocation et de l'expiration. |
| Permissions fines et expirables. | Risque de fuite si les clés ne sont pas gérées de façon sécurisée. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Sécurité | Accès restreint et temporaire aux ressources, réduction de la surface de l'application. |
| Optimisation des coûts | Réduction de la charge du serveur et de la bande passante via le stockage. |
| Efficacité des performances | Transferts directs à haute bande passante sans intermédiaire. |

## Source

[Patron Valet Key – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/valet-key)
