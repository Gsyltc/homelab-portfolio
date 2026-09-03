# Gatekeeper

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/gatekeeper). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Protéger les applications et services en utilisant une instance dédiée (gardien) qui valide et assainit les requêtes avant de les transférer aux backends privés.

## Quand l'envisager

- Pour protéger des backends qui ne doivent pas être exposés directement.
- Lorsqu'il faut valider, assainir et filtrer les requêtes entrantes (validation stricte, anti-injection).
- Pour segmenter l'accès entre la zone publique et la zone privée.

## Quand ne PAS l'envisager

- Lorsque la validation peut être réalisée directement dans le backend sans exposition publique.
- Si le gatekeeper devient le seul point d'entrée et introduit une latence ou une complexité non justifiée.

## Prérequis

### Logiciel

- Composant de validation/assainissement (gatekeeper) et règles de validation strictes.

### Infrastructure

- Réseau segmenté (DMZ), capacité de mise à l'échelle du gatekeeper et monitoring des requêtes.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Sécurise les backends en les isolant de l'exposition directe. | Point de défaillance et de goulot d'étranglement potentiel. |
| Validation et assainissement centralisés. | Latence ajoutée pour chaque requête. |
| Point d'entrée unique pour la surveillance et la protection. | Complexité de maintenance et de mise à jour. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Sécurité | Validation des entrées, protection des backends, réduction de la surface d'attaque. |
| Efficacité des performances | Déchargement du traitement de validation des backends. |

## Source

[Patron Gatekeeper – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/gatekeeper)
