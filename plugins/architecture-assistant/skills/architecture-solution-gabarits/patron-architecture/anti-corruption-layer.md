# Anti-Corruption Layer

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Implémenter une façade ou une couche d'adaptation entre une application moderne et un système existant (legacy), pour protéger la nouvelle conception de la « pollution » des modèles et protocoles du système historique.

## Quand l'envisager

- Lors d'une migration ou d'une modernisation vers de nouveaux modèles de domaine.
- Pour intégrer des systèmes existants dont les contrats, formats ou sémantiques ne correspondent pas aux besoins de la nouvelle solution.
- Pour isoler les changements d'un système legacy afin qu'ils n'impactent pas la nouvelle application.

## Quand ne PAS l'envisager

- Lorsque le système legacy est complètement remplacé et mis hors service.
- Si aucun transfert d'information entre l'existant et le nouveau système n'est requis.
- Lorsque l'adaptation peut être réalisée directement dans le système existant.

## Prérequis

### Logiciel

- Composant de traduction/adaptation (couche d'antiqui-corruption) avec les définitions des modèles de données des deux systèmes.

### Infrastructure

- Canaux d'intégration vers le système existant (API, files de messages, bases de données partagées).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Isolation sémantique : le domaine de la nouvelle solution reste pur. | Couche supplémentaire à concevoir, maintenir et tester. |
| Réduit l'impact des évolutions du système legacy. | Coût de traduction (latence et effort) pour chaque échange. |
| Permet une migration incrémentale (combinable avec Strangler Fig). | Risque de duplication logique entre la couche d'adaptation et les systèmes. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Excellence opérationnelle | Contrôle et gouvernance des intégrations : la couche d'adaptation centralise les règles de traduction et facilite les opérations. |

## Source

[Patron Anti-Corruption Layer – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer)
