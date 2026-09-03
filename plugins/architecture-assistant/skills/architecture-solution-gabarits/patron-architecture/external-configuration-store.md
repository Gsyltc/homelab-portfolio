# External Configuration Store

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/external-configuration-store). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Déplacer les informations de configuration hors du package de déploiement de l'application vers un emplacement centralisé, pour les mettre à jour sans redéploiement et les partager entre instances.

## Quand l'envisager

- Lorsque la configuration varie entre environnements ou change fréquemment.
- Pour partager la même configuration entre plusieurs instances ou applications.
- Pour mettre à jour la configuration à chaud (sans redéploiement ni redémarrage).
- Pour centraliser les secrets de manière sécurisée.

## Quand ne PAS l'envisager

- Lorsque la configuration est stable et spécifique à chaque instance.
- Si la configuration centralisée ajoute une dépendance et une latence inacceptables au démarrage.
- Pour des secrets très volatils qui changent à chaque démarrage (à stocker plutôt dans un coffre).

## Prérequis

### Logiciel

- Client de configuration (ex. Azure App Configuration, AWS AppConfig, etcd, consul) et stratégie de cache/fallback.

### Infrastructure

- Service de configuration centralisé hautement disponible ; gestion des accès et des secrets (Key Vault, Secrets Manager).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Mise à jour de configuration sans redéploiement. | Nouvelle dépendance d'infrastructure (disponibilité, latence). |
| Cohérence de configuration entre instances. | Sécurité de l'accès à la configuration à assurer. |
| Séparation entre code et configuration, gestion centralisée des secrets. | Risque de divergence si le cache/fallback n'est pas géré. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Excellence opérationnelle | Gestion centralisée et versionnée de la configuration, déploiements reproductibles. |

## Source

[Patron External Configuration Store – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/external-configuration-store)
