# Saga

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Gérer la cohérence des données à travers des microservices dans des scénarios de transactions distribuées, en enchaînant des transactions locales avec des compensations en cas d'échec.

## Quand l'envisager

- Pour des transactions distribuées qui s'étendent sur plusieurs services sans transaction globale atomique.
- Lorsque la cohérence éventuelle est acceptable.
- Dans les architectures de microservices où une opération traverse plusieurs services.

## Quand ne PAS l'envisager

- Lorsque des transactions atomiques locales suffisent.
- Si la cohérence forte immédiate est requise.
- Lorsque les étapes ont des effets irréversibles qui ne peuvent pas être compensés.

## Prérequis

### Logiciel

- Implémentation de saga (orchestrée ou chorégraphiée) avec étapes de compensation et gestion des événements.

### Infrastructure

- Coordination fiable (orchestrateur ou bus d'événements), journal des étapes et monitoring.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Cohérence des données dans les flux multi-services. | Complexité de conception et de gestion des compensations. |
| Évite les verrous et les transactions distribuées complexes. | Fenêtres d'incohérence temporaire. |
| Adapté aux microservices et aux architectures événementielles. | Debuggage et monitoring difficiles. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Cohérence des données en cas d'échec partiel d'un flux distribué. |

## Source

[Patron Saga – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga)
