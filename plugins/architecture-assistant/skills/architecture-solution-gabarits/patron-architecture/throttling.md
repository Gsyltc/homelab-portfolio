# Throttling

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/throttling). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Contrôler la consommation des ressources par les applications, locataires ou services, en régulant le taux d'utilisation pour préserver la disponibilité.

## Quand l'envisager

- Pour garantir que les ressources critiques restent disponibles pour tous les consommateurs.
- Pour appliquer des quotas et prévenir la monopolisation des ressources.
- Pour protéger les backends et les coûts.

## Quand ne PAS l'envisager

- Lorsque la capacité est largement suffisante et la charge maîtrisée.
- Si le throttling dégrade inutilement l'expérience sans protéger quoi que ce soit.

## Prérequis

### Logiciel

- Mécanisme de throttling (par tenant/service) avec politique de refus ou de mise en file (200/429/503).

### Infrastructure

- Point de contrôle (passerelle, proxy) et monitoring de l'utilisation.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Préserve la disponibilité et l'équité entre consommateurs. | Peut rejeter ou retarder des requêtes légitimes. |
| Contrôle des coûts et de la consommation. | Configuration et réglage complexes. |
| Protège les dépendances en aval. | Impact sur l'expérience utilisateur en cas de mauvaise calibration. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Prévention de la surcharge et maintien de la disponibilité. |
| Sécurité | Prévention des abus et des dénis de service par épuisement des ressources. |
| Optimisation des coûts | Maîtrise de la consommation et des coûts. |
| Efficacité des performances | Répartition de l'accès aux ressources. |

## Source

[Patron Throttling – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/throttling)
