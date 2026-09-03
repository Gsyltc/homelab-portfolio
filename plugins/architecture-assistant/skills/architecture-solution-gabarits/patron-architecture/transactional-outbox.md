# Transactional Outbox

> Patron d'intégration de microservices documenté par SoftwareMill dans « Microservices 101: Transactional Outbox and Inbox » (https://softwaremill.com/microservices-101/). Patron **complémentaire au catalogue des patrons de l'Azure Architecture Center, hors Well-Architected Framework**. Agnostic à la technologie : applicable sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Garantir la livraison (au moins une fois) des messages ou événements qu'un service doit publier, en rendant la publication **atomique avec la transaction métier** : le message est d'abord persisté dans une table « outbox » au sein de la même transaction, puis un processus d'arrière-plan le publie vers le broker ou le service cible. Le message ne peut donc pas être perdu en cas de panne entre le commit de la transaction et la publication.

## Quand l'envisager

- Pour notifier d'autres services (broker, autre microservice) après une transaction locale, sans risque de perdre le message en cas de panne.
- Lorsque la perte d'un message a des implications métier sérieuses (ex. des points de fidélité débités doivent déclencher l'envoi d'un prix).
- Pour éliminer le **couplage temporel** : l'émetteur n'a plus besoin que le broker ou le service cible soit disponible au moment de la transaction.
- Pour éviter les états incohérents : notification d'une transaction finalement annulée, ou message perdu après un commit réussi.

## Quand ne PAS l'envisager

- Lorsque la perte d'un message est acceptable (notification non critique, données non transactionnelles).
- Si le couplage synchrone et les volumes faibles rendent le pattern disproportionné.
- Si le coût d'implémentation (boilerplate, worker de publication, polling) n'est pas justifié par l'exigence de fiabilité.

## Prérequis

### Logiciel

- Table « outbox » dans la **même base de données** que les données métier : l'insertion du message fait partie de la transaction métier (INSERT atomique avec le commit).
- Abstraction d'enregistrement des messages (masquer le stockage en outbox au reste du code).
- Processus d'arrière-plan (worker) qui poll la table et publie les messages non envoyés, avec gestion des retries (marquer envoyé après accusé de réception).
- Option avancée : log tailing de la base (CDC, ex. Debezium) au lieu du polling.

### Infrastructure

- Base de données transactionnelle partagée avec les données métier.
- Verrouillage des lignes pour le parallélisme (ex. `SELECT ... FOR UPDATE SKIP LOCKED`) afin d'éviter la publication multiple d'un même message par plusieurs workers.
- Capacité de polling à haute fréquence (souvent < 1 s) et mécanisme de nettoyage de la table (suppression des messages envoyés).

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Garantie **at-least-once** : aucun message perdu en cas de panne (reprise après redémarrage). | Code standard (boilerplate) : abstraction + worker planifié. |
| Publication atomique avec la transaction métier, découplage temporel de l'émetteur. | Charge de polling sur la base de données et latence de livraison (compromis fréquence/latence). |
| Débit élevé via le parallélisme (plusieurs workers, lots). | Ne supprime pas les doublons : la déduplication reste à faire côté récepteur. |
| | Table qui peut enfler rapidement avec de gros volumes (nettoyage nécessaire). |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Livraison garantie des messages (at-least-once), reprise après panne sans perte, élimination du couplage temporel. |
| Efficacité des performances | Parallélisation de la publication (workers concurrents, lots) sans publication multiple. |

## Source

[Microservices 101: Transactional Outbox and Inbox – SoftwareMill](https://softwaremill.com/microservices-101/)

Ouvrage de référence : *Microservices Patterns* de Chris Richardson (transactional outbox).
