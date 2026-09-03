# Quarantine

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/quarantine). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Garantir que les actifs externes (dépendances, artefacts, modules) atteignent un niveau de qualité convenu par l'équipe avant que la charge de travail ne les consomme.

## Quand l'envisager

- Pour contrôler la qualité et la sécurité des dépendances et artefacts externes avant usage.
- Pour se protéger des fournisseurs ou sources non fiables.
- Pour appliquer des politiques de gouvernance des dépendances (SBOM, licence, sécurité).

## Quand ne PAS l'envisager

- Lorsque la chaîne d'approvisionnement est totalement maîtrisée et de confiance.
- Si le processus de quarantaine n'apporte pas de valeur (artefacts internes contrôlés).

## Prérequis

### Logiciel

- Processus et outils d'inspection (scan de vulnérabilités, analyse de licences, signature) et registre d'artefacts.

### Infrastructure

- Registre d'artefacts isolé (proxy/registre de quarantaine) et chaîne CI/CD avec gates.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Réduit les risques de sécurité et de qualité des dépendances. | Latence d'intégration des dépendances (revue). |
| Politique de consommation des actifs appliquée de façon uniforme. | Effort de processus et d'outillage. |
| Auditabilité de la chaîne d'approvisionnement. | Risque de blocage si la file de quarantaine n'est pas traitée. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Sécurité | Contrôle des dépendances et de la chaîne d'approvisionnement logicielle. |
| Excellence opérationnelle | Gouvernance et politiques d'approvisionnement appliquées et auditées. |

## Source

[Patron Quarantine – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/quarantine)
