# Ambassador

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/ambassador). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Créer des services auxiliaires (« ambassadeurs ») qui envoient les requêtes réseau au nom d'un service ou d'une application consommateur, pour centraliser la gestion des communications sortantes (connexions, retries, observabilité, sécurité).

## Quand l'envisager

- Pour factoriser la gestion des appels réseau sortants (pool de connexions, retries, timeouts, métriques) hors du code métier.
- Lorsque des clients multilingues ou hétérogènes doivent partager un même comportement de communication (ex. retries, TLS, authentification).
- Pour déployer des changements de communication sans redéployer les services consommateurs (sidecar associé).

## Quand ne PAS l'envisager

- Lorsque le réseau est fiable et le nombre de consommateurs réduit (le patron ajoute une couche et une latence).
- Si les clients ont déjà une bibliothèque client mature qui encapsule retries et observabilité.
- Dans les systèmes à très faible latence où chaque saut réseau supplémentaire est critique.

## Prérequis

### Logiciel

- Bibliothèque ou conteneur d'ambassadeur (ex. Envoy, Istio sidecar) compatible avec le runtime des consommateurs.

### Infrastructure

- Orchestrateur de conteneurs ou plateforme permettant l'injection du sidecar dans le pod/la VM (ex. Kubernetes, Service Fabric).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Découple la logique de communication du code métier. | Ajoute un saut réseau et de la latence. |
| Offre un comportement cohérent (retries, monitoring, sécurité) à tous les clients. | Complexité d'opération supplémentaire (déploiement, mise à jour du sidecar). |
| Permet d'évoluer la couche de communication indépendamment des consommateurs. | Risque de divergence entre l'ambassadeur et le client réel si la configuration n'est pas alignée. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Retries, timeouts et failover centralisés : gestion des pannes transitoires côté communication. |
| Sécurité | TLS, authentification et filtrage sortant centralisés, contrôle de la surface d'exposition. |

## Source

[Patron Ambassador – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/ambassador)
