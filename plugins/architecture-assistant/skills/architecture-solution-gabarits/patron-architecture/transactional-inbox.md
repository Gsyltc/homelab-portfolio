# Transactional Inbox

> Patron d'intégration de microservices documenté par SoftwareMill dans « Microservices 101: Transactional Outbox and Inbox » (https://softwaremill.com/microservices-101/). Patron **complémentaire au catalogue des patrons de l'Azure Architecture Center, hors Well-Architected Framework**. Agnostic à la technologie : applicable sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Garantir qu'un message reçu est traité **au moins une fois sans perte ni doublon**, en persistant le message dans une table « inbox » et en l'acquittant (ACK) **avant** traitement, puis en le traitant par un processus d'arrière-plan qui déduplique et marque le traitement terminé. Complète le Transactional Outbox côté récepteur pour une garantie de bout en bout.

## Quand l'envisager

- Lorsque le traitement déclenché par le message est **long, coûteux ou de durée imprévisible** (timeouts de redélivrance, ex. visibilité SQS, timeout HTTP) : éviter de relancer des traitements concurrents coûteux.
- Pour garantir qu'aucun message n'est perdu : l'ACK n'est envoyé qu'après persistance du message, jamais avant.
- Pour **dédupliquer** les messages reçus (garantie at-least-once de l'émetteur ou du broker) et rejeter les redélivrances.
- Pour **rétablir l'ordre** des messages à l'aide d'identifiants monotones (détection de messages manquants).

## Quand ne PAS l'envisager

- Si le traitement est court et de durée prévisible : on peut acquitter après traitement, sans table intermédiaire.
- Si le traitement est naturellement idempotent et que les doublons n'ont pas de coût significatif.
- Si la latence ajoutée ou la charge supplémentaire sur la base de données est inacceptable.

## Prérequis

### Logiciel

- Table « inbox » avec **clé de déduplication** (identifiant unique du message) : dédupliquer avant insertion.
- Persistance du message + ACK avant traitement (crash-safe : le message reste disponible dans l'inbox en cas de panne).
- Processus d'arrière-plan (worker) qui sélectionne les messages à traiter, marque le traitement terminé (ou supprime la ligne) à la fin.
- Rejet des doublons et gestion des redélivrances (NACK ou code d'erreur si échec).

### Infrastructure

- Base de données transactionnelle persistante pour la table « inbox ».
- Verrouillage des lignes pour le parallélisme (ex. `SELECT ... FOR UPDATE SKIP LOCKED`) afin d'éviter que deux workers traitent le même message.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Aucune perte de message : ACK après persistance, traitement après reprise en cas de crash. | Latence accrue entre la réception et le traitement. |
| Déduplication des redélivrances (garantie at-least-once sans doublon). | Code standard (boilerplate) : table, worker, verrouillage. |
| Traitement à rythme maîtrisé et parallélisable ; restauration de l'ordre des messages. | Charge supplémentaire sur la base de données (polling). |
| | Une redélivrance pendant un traitement long peut déclencher un traitement concurrent malgré la déduplication. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Traitement garanti des messages (at-least-once sans perte), déduplication, reprise après panne, ordre restauré. |
| Efficacité des performances | Traitement à rythme maîtrisé et parallélisé sans traitement multiple d'un même message. |

## Source

[Microservices 101: Transactional Outbox and Inbox – SoftwareMill](https://softwaremill.com/microservices-101/)
