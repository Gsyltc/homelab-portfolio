# Geode

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/geodes). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Déployer des services backend sur des nœuds géographiquement distribués ; chaque nœud peut traiter les requêtes de n'importe quelle région, avec réplication des données actives pour une haute disponibilité.

## Quand l'envisager

- Pour une disponibilité élevée et une faible latence à l'échelle mondiale.
- Lorsqu'une région peut absorber la charge des autres régions en cas de sinistre.
- Pour des données consultables depuis n'importe quel nœud (multi-région).

## Quand ne PAS l'envisager

- Lorsque les données sont régionalement contraintes (conformité, souveraineté).
- Si la réplication multi-région n'est pas justifiée par la disponibilité ou la latence requise.
- Lorsque les coûts de réplication et de multi-région dépassent les bénéfices.

## Prérequis

### Logiciel

- Application déployable en multi-région et gestion des conflits de données (réplication active).

### Infrastructure

- Magasins de données répliqués (actif/actif) et infrastructure réseau multi-région (DNS, CDN, routage).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Haute disponibilité (perte d'une région supportée). | Complexité de la réplication et de la cohérence des données. |
| Latence réduite pour les utilisateurs proches d'un nœud. | Coûts d'infrastructure élevés. |
| Évolutivité mondiale. | Gestion des conflits d'écriture entre régions. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Continuité de service multi-région et bascule en cas de sinistre. |
| Efficacité des performances | Latence réduite par proximité des utilisateurs. |

## Source

[Patron Geode – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/geodes)
