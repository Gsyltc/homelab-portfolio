# Circuit Breaker

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Gérer les défaillances qui peuvent prendre un temps variable à être corrigées, lors des connexions à un service ou une ressource distante : interrompre les appels vers un service en défaillance et basculer sur un comportement de repli.

## Quand l'envisager

- Pour les appels à des services distants ou des dépendances externes peu fiables.
- Pour éviter que les appels vers un service en panne n'attendent un timeout à chaque requête.
- Pour protéger le système de défaillances en cascade.

## Quand ne PAS l'envisager

- Pour les défaillances purement transitoires qui relèvent du Retry.
- Pour des appels locaux dans un même processus.
- Lorsque les appels ne présentent pas de risque de saturation (ressources abondantes).

## Prérequis

### Logiciel

- Bibliothèque ou implémentation de circuit breaker (ex. Polly, Resilience4j, Spring Cloud) et seuils de déclenchement configurés.

### Infrastructure

- Monitoring des appels (taux d'échec, latence) pour alimenter les seuils du circuit.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Réagit rapidement aux pannes et réduit la charge inutile d'un service défaillant. | Complexité de configuration des seuils (faux positifs/négatifs). |
| Protège contre les défaillances en cascade. | Latence et surcharge d'état supplémentaires. |
| Permet la récupération progressive (état half-open). | Risque de réponses de repli masquant des erreurs réelles. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Gestion des pannes persistantes, récupération progressive, prévention des cascades. |
| Efficacité des performances | Évite d'occuper des ressources sur des appels voués à l'échec. |

## Source

[Patron Circuit Breaker – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
