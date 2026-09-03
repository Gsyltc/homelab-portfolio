# Choreography

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/choreography). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Laisser chaque service décider quand et comment une opération d'affaires est traitée, via des événements, sans dépendre d'un orchestrateur central.

## Quand l'envisager

- Pour des processus distribués à nombreuses étapes sans dépendance temporelle stricte.
- Lorsqu'on veut éviter un point central de défaillance (orchestrateur).
- Dans une architecture événementielle (event-driven) où les services réagissent aux événements.

## Quand ne PAS l'envisager

- Pour des processus avec des étapes strictement séquentielles et transactionnelles.
- Lorsque la traçabilité de bout en bout est difficile à garantir.
- Si les services ne peuvent pas gérer l'ambiguïté des événements dupliqués ou hors ordre.

## Prérequis

### Logiciel

- Bus événementiel (ex. Event Grid, Event Hubs, Kafka) et gestion des événements (versioning, idempotence).

### Infrastructure

- Infrastructure de messagerie fiable et persistante ; observabilité distribuée (correlation IDs).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Pas d'orchestrateur central ni de point de défaillance unique. | Visibilité et débogage plus complexes. |
| Couplage faible entre services. | Risque d'incohérences si les événements ne sont pas gérés (idempotence, ordre). |
| Évolutivité et évolutions locales des services. | Répartition des responsabilités plus diffuse à documenter. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Excellence opérationnelle | Observabilité et gestion des événements standardisées, processus pilotés par les événements. |
| Efficacité des performances | Traitement parallèle et asynchrone des étapes. |

## Source

[Patron Choreography – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/choreography)
