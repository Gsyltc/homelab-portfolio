# Deployment Stamps

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/deployment-stamp). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Déployer plusieurs copies indépendantes des composants d'application, y compris les magasins de données, pour obtenir évolutivité, isolation des locataires et reprise rapide par déploiement de nouvelles instances.

## Quand l'envisager

- Pour des solutions multi-locataires nécessitant une isolation ou une évolutivité par « stamp ».
- Lorsqu'il faut provisionner rapidement de nouvelles capacités dans de nouvelles régions.
- Pour des applications à forte scalabilité géographique ou par locataire.

## Quand ne PAS l'envisager

- Pour des applications simples à charge faible et peu de locataires.
- Lorsque le coût de gestion de plusieurs stamps (données, configuration) n'est pas justifié.
- Si les données doivent être globalement cohérentes entre les stamps.

## Prérequis

### Logiciel

- Modèle d'application déployable de façon répétable (IaC) et gestion de la configuration par stamp.

### Infrastructure

- Infrastructure en code (Terraform, ARM/Bicep, CloudFormation) et registre de locataires (tenant-to-stamp mapping).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Isolation et résilience par stamp. | Complexité opérationnelle (plusieurs stamps, données réparties). |
| Scalabilité quasi linéaire par ajout de stamps. | Coût de duplication des ressources. |
| Redéploiement rapide d'une région ou d'un locataire. | Gestion du partitionnement et du routage des locataires. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Excellence opérationnelle | Déploiements reproductibles et standardisés via l'infrastructure en code. |
| Efficacité des performances | Mise à l'échelle horizontale par ajout de stamps. |

## Source

[Patron Deployment Stamps – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/deployment-stamp)
