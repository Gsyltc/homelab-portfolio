# Claim Check

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/claim-check). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Diviser un message volumineux en un « claim check » (ticket) et un payload, pour ne pas saturer un bus de messages : le payload est stocké ailleurs et référencé par le ticket.

## Quand l'envisager

- Lorsque les messages dépassent la taille limite du bus (ex. 256 Ko pour Azure Service Bus).
- Pour transférer de gros blobs ou documents via une messagerie.
- Lorsqu'on veut limiter le trafic réseau du bus de messages.

## Quand ne PAS l'envisager

- Lorsque les messages sont petits et dans la limite du bus.
- Si l'infrastructure de stockage du payload ajoute plus de complexité que le problème à résoudre.

## Prérequis

### Logiciel

- Client de stockage (ex. Blob Storage, S3) et logique claim check dans producteur/consommateur.

### Infrastructure

- Stockage persistant pour les payloads avec mécanismes de nettoyage (purge/expiration).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Réduit la charge et la taille des messages sur le bus. | Latence et appels supplémentaires pour récupérer le payload. |
| Évite les limites de taille des files. | Gestion du cycle de vie du stockage et nettoyage nécessaire. |
| Sépare le transfert (léger) du contenu (lourd). | Point de défaillance supplémentaire (le stockage). |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Soulage le bus de messages, réduit les risques de saturation et d'échec de remise. |
| Sécurité | Contrôle des accès au stockage des payloads (les tickets ne portent pas les données). |
| Optimisation des coûts | Réduction de la bande passante et des coûts de messagerie. |
| Efficacité des performances | Améliore le débit du bus en limitant la taille des messages. |

## Source

[Patron Claim Check – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/claim-check)
