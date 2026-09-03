# Static Content Hosting

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/static-content-hosting). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Déployer du contenu statique (HTML, CSS, JS, images) vers un service de stockage cloud pour une livraison directe aux clients, sans serveur applicatif.

## Quand l'envisager

- Pour héberger des contenus statiques à fort trafic.
- Pour réduire les coûts et la charge des serveurs applicatifs.
- Pour distribuer le contenu via CDN à l'échelle mondiale.

## Quand ne PAS l'envisager

- Lorsque le contenu nécessite un traitement dynamique par serveur.
- Si les exigences de sécurité (droits d'accès, authentification) nécessitent un contrôle applicatif.

## Prérequis

### Logiciel

- Contenu statique préparé (build) et mécanisme de publication (CI/CD).

### Infrastructure

- Service de stockage (ex. Azure Blob/Static Web Apps, AWS S3) et CDN optionnel.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Coûts réduits (pas de serveurs applicatifs pour le statique). | Pas de traitement dynamique. |
| Haute disponibilité et distribution via CDN. | Gestion du cache et de l'invalidation nécessaire. |
| Simplicité d'échelle et de gestion. | Sécurité et contrôle d'accès à concevoir. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Optimisation des coûts | Réduction des coûts de calcul et d'hébergement. |

## Source

[Patron Static Content Hosting – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/static-content-hosting)
