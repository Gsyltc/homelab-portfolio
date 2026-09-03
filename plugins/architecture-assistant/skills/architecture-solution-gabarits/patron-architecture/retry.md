# Retry

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Permettre aux applications de gérer les défaillances temporaires anticipées en réessayant les opérations échouées (avec délais adaptatifs), sans amplifier la panne.

## Quand l'envisager

- Lors des appels à des services ou ressources exposés à des pannes transitoires.
- Pour gérer les erreurs réseau, timeouts, erreurs 429/5xx.
- En complément du Circuit Breaker pour les pannes persistantes.

## Quand ne PAS l'envisager

- Pour des erreurs permanentes (4xx, erreurs métier) qui ne seront pas corrigées en réessayant.
- Lorsque le retry risque d'amplifier la charge d'un service en défaillance (sans circuit breaker).
- Si l'opération n'est pas idempotente et que le retry causerait des doublons.

## Prérequis

### Logiciel

- Bibliothèque de retries (ex. Polly, Resilience4j) avec délais exponentiels, jitter et limites.

### Infrastructure

- Monitoring des échecs et des taux de retry pour ajuster la politique.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Résilience aux pannes transitoires sans intervention manuelle. | Risque d'augmentation de la charge en cas de panne prolongée (sans circuit breaker). |
| Améliore la disponibilité perçue. | Latence ajoutée lors des retries. |
| Simple à implémenter. | Nécessite des opérations idempotentes ou une gestion des doublons. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Gestion des défaillances transitoires et récupération automatique. |

## Source

[Patron Retry – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
