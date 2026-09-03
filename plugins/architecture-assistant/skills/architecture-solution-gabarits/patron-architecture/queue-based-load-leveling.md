# Queue-Based Load Leveling

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Utiliser une file d'attente comme tampon entre une tâche et un service pour lisser les charges intermittentes et lourdes, évitant les pics de charge sur le service.

## Quand l'envisager

- Lorsque la charge de travail varie fortement (pics imprévisibles).
- Pour protéger un service backend de la surcharge.
- Pour permettre au service de traiter à son rythme et de mettre à l'échelle.

## Quand ne PAS l'envisager

- Lorsque la charge est constante et prévisible.
- Si la latence de file d'attente est inacceptable pour la tâche.
- Lorsque les exigences de réponse immédiate sont critiques.

## Prérequis

### Logiciel

- File d'attente (ex. Azure Queue Storage, Service Bus, SQS) et traitement asynchrone.

### Infrastructure

- File dimensionnée aux pics de charge ; capacité de mise à l'échelle des consommateurs.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Lisse les pics de charge et protège le backend. | Latence de traitement ajoutée (asynchrone). |
| Améliore la disponibilité sous charge variable. | Gestion de la file et de la consommation nécessaire. |
| Découplage entre producteurs et consommateurs. | Risque d'accumulation si la capacité de consommation est insuffisante. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Protection du backend contre les pics de charge. |
| Optimisation des coûts | Dimensionnement par la charge moyenne plutôt que par les pics. |
| Efficacité des performances | Répartition de la charge dans le temps. |

## Source

[Patron Queue-Based Load Leveling – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling)
