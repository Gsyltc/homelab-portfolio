# Cache-Aside

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Charger les données à la demande dans un cache depuis le magasin de données : à chaque lecture, le cache est consulté d'abord et le magasin n'est sollicité qu'en cas de « cache miss ».

## Quand l'envisager

- Pour des lectures fréquentes sur des données qui changent rarement.
- Lorsque la latence ou la charge du magasin de données est un problème.
- Pour améliorer les performances de lecture et la scalabilité de lectures.

## Quand ne PAS l'envisager

- Lorsque les données sont mises à jour très fréquemment (cohérence difficile).
- Si la tolérance à des données périmées (stale) n'est pas acceptable.
- Lorsque le volume de données est supérieur à la capacité raisonnable du cache.

## Prérequis

### Logiciel

- Client de cache (ex. Azure Cache for Redis, Memcached) et logique de chargement/rafraîchissement dans l'application.

### Infrastructure

- Service de cache à haute disponibilité ; capacité mémoire dimensionnée aux données à mettre en cache.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Latence de lecture réduite et charge du magasin de données diminuée. | Incohérence possible entre cache et magasin (TTL, invalidation). |
| Mise en œuvre simple. | Gestion du cycle de vie des clés et des évictions. |
| Évolutivité horizontale des lectures. | Risque de stampede du magasin en cas d'expiration massive simultanée. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Protection du magasin de données contre les surcharges de lecture ; reprise après éviction du cache. |
| Efficacité des performances | Réduction de la latence et augmentation du débit de lecture. |

## Source

[Patron Cache-Aside – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
