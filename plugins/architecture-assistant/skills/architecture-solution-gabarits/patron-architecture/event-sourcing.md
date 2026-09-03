# Event Sourcing

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Utiliser un magasin en append-only (journal d'événements) pour enregistrer la série complète des événements décrivant les actions sur les données d'un domaine, au lieu de stocker uniquement l'état courant.

## Quand l'envisager

- Pour préserver une trace d'audit complète et rejouable des changements.
- Pour reconstruire l'état à tout moment ou analyser le passé.
- Dans les domaines où l'historique des événements a de la valeur (financier, conformité).
- En combinaison avec CQRS pour alimenter des vues matérialisées.

## Quand ne PAS l'envisager

- Pour des systèmes simples où l'état courant suffit.
- Lorsque la complexité du journal et de la relecture dépasse le besoin.
- Si le volume d'événements est énorme et que la reconstruction est trop coûteuse sans snapshot.

## Prérequis

### Logiciel

- Magasin d'événements (append-only) et gestion des versions d'événements ; projection de vues (read models).

### Infrastructure

- Stockage persistant pour les événements et stratégie de snapshot/compaction pour la relecture.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Traçabilité et auditabilité complètes. | Complexité conceptuelle et opérationnelle. |
| Reconstruction d'états et analyse historique possibles. | Évolution de schémas d'événements à gérer (versioning). |
| Source de vérité unique et rejouable. | Latence de la reconstruction sans projections. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Traçabilité intégrale, reconstruction d'état et rejeu après sinistre. |
| Efficacité des performances | Écritures append-only efficaces et projections de lecture optimisées (avec CQRS). |

## Source

[Patron Event Sourcing – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
