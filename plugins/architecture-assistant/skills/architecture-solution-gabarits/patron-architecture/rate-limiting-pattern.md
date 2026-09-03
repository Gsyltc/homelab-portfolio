# Rate Limiting

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/rate-limiting-pattern). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Éviter ou minimiser les erreurs de throttling en contrôlant la consommation des ressources (nombre de requêtes par période) par les applications, locataires ou services.

## Quand l'envisager

- Pour protéger les services des surcharges et respecter les quotas.
- Pour contrôler l'utilisation des ressources par locataire ou client.
- Pour prévenir les abus et les dépassements de coûts.

## Quand ne PAS l'envisager

- Lorsque la capacité est illimitée et que la charge est maîtrisée.
- Si le rate limiting dégrade l'expérience de clients légitimes sans bénéfice.

## Prérequis

### Logiciel

- Mécanisme de rate limiting (par clé/tenant) et gestion des réponses 429/Retry-After.

### Infrastructure

- Point de contrôle centralisé (passerelle, load balancer) et monitoring de l'utilisation.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Protège les ressources et la disponibilité. | Peut rejeter des requêtes légitimes (faux positifs). |
| Équité entre les consommateurs. | Complexité de configuration des seuils. |
| Prévention des coûts excessifs et des abus. | Expérience utilisateur dégradée si mal calibré. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Protection des services contre la surcharge. |

## Source

[Patron Rate Limiting – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/rate-limiting-pattern)
