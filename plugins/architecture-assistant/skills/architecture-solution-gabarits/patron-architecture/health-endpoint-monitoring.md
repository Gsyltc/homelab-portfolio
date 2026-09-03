# Health Endpoint Monitoring

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Implémenter des vérifications fonctionnelles dans une application, accessibles via des endpoints exposés, que des outils externes interrogent à intervalles réguliers pour vérifier la santé du système.

## Quand l'envisager

- Pour détecter rapidement les défaillances de l'application et de ses dépendances.
- Pour alimenter les outils de surveillance, d'alerting et de load balancing.
- Pour valider la disponibilité de bout en bout (y compris les dépendances).

## Quand ne PAS l'envisager

- Lorsque la surveillance de la disponibilité peut être assurée par l'infrastructure seule (pings).
- Si les endpoints de santé eux-mêmes ne sont pas sécurisés ou peuvent être abusés.

## Prérequis

### Logiciel

- Endpoints de santé (ex. /health) avec vérifications des dépendances critiques et temps de réponse.

### Infrastructure

- Outil de monitoring/alerting (ex. Application Insights, CloudWatch, Prometheus) et capacité de test externe.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Détection proactive des pannes. | Les vérifications doivent refléter la vraie disponibilité (faux positifs). |
| Alimente l'auto-récupération (reboots, élimination de la rotation, load balancer). | Coût et exposition des endpoints de santé. |
| Visibilité sur les dépendances critiques. | Tests synthétiques à concevoir et maintenir. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Détection rapide des pannes et déclenchement de la récupération. |
| Excellence opérationnelle | Observabilité de la santé de l'application et de ses dépendances. |
| Efficacité des performances | Mesure des temps de réponse des endpoints critiques. |

## Source

[Patron Health Endpoint Monitoring – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring)
