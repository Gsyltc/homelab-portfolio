# Strangler Fig

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Migrer incrémentalement un système existant en remplaçant progressivement des morceaux de fonctionnalités par de nouvelles applications et services, jusqu'au remplacement complet.

## Quand l'envisager

- Lors de la modernisation ou de la migration d'un système legacy vers une nouvelle architecture.
- Pour réduire le risque d'une migration « big bang ».
- Pour livrer de la valeur progressivement tout en migrer.

## Quand ne PAS l'envisager

- Lorsqu'une réécriture complète immédiate est viable et moins coûteuse.
- Si les fonctionnalités du système existant ne peuvent pas être migrées par morceaux.
- Lorsque le système legacy doit être totalement remplacé sans période de coexistence.

## Prérequis

### Logiciel

- Mécanisme de routage/bascule entre ancien et nouveau (facade, proxy, feature flags) et stratégie de coexistence.

### Infrastructure

- Capacité d'exécution parallèle des deux systèmes et monitoring de la migration.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Risque réduit (migration incrémentale). | Période de coexistence et de double exécution. |
| Livraison de valeur continue pendant la migration. | Complexité de gestion du routage et de l'état partagé. |
| Reversibilité partielle (rollback par morceau). | Durée de migration plus longue. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Migration progressive réduisant les risques de défaillance d'ensemble. |
| Optimisation des coûts | Réutilisation et remplacement incrémental plutôt que réécriture massive. |
| Excellence opérationnelle | Modernisation continue et gouvernée de la plateforme. |

## Source

[Patron Strangler Fig – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig)
