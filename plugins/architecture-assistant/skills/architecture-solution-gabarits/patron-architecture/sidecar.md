# Sidecar

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Déployer des composants dans un processus ou un conteneur séparé pour fournir isolation et encapsulation (ex. mise en réseau, monitoring, configuration), attachés à l'application principale.

## Quand l'envisager

- Pour attacher des fonctionnalités transversales (proxy, TLS, observabilité, config) à une application sans la modifier.
- Lorsque les langages/frameworks hétérogènes nécessitent des capacités communes.
- Dans les environnements conteneurisés (Kubernetes) ou avec des langages différents.

## Quand ne PAS l'envisager

- Pour des fonctionnalités qui ne nécessitent pas d'isolation (processus séparé inutile).
- Lorsque le coût de ressources et la complexité du sidecar dépassent les bénéfices.
- Si le runtime ne supporte pas l'injection du sidecar.

## Prérequis

### Logiciel

- Runtime conteneurisé avec injection de sidecar (ex. Kubernetes, Service Mesh, Dapr).

### Infrastructure

- Orchestrateur de conteneurs et capacité réseau/service mesh.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Isolation et encapsulation des préoccupations transversales. | Consommation de ressources par sidecar. |
| Homogénéité des capacités entre langages hétérogènes. | Latence et complexité de déploiement. |
| Évolutions du sidecar sans modifier l'application. | Gestion du cycle de vie des sidecars. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Sécurité | Isolation des composants, TLS, politiques de réseau appliquées en un point. |
| Excellence opérationnelle | Capacités transversales standardisées et observabilité homogène. |

## Source

[Patron Sidecar – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar)
