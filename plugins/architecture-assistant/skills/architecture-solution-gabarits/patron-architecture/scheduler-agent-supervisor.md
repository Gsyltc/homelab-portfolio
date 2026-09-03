# Scheduler Agent Supervisor

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/scheduler-agent-supervisor). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Coordonner un ensemble d'actions sur des services et ressources distribués : un planificateur déclenche des agents qui exécutent des tâches, supervisés par un superviseur qui gère les échecs.

## Quand l'envisager

- Pour orchestrer des tâches distribuées complexes (batchs, workflows).
- Lorsqu'il faut exécuter, surveiller et relancer des tâches de façon fiable.
- Pour des opérations planifiées qui traversent plusieurs systèmes.

## Quand ne PAS l'envisager

- Pour des tâches simples ponctuelles (cron suffit).
- Si l'infrastructure d'orchestration est disproportionnée par rapport au besoin.

## Prérequis

### Logiciel

- Orchestrateur de workflows/tâches (ex. Azure Logic Apps, Durable Functions, AWS Step Functions) et agents d'exécution.

### Infrastructure

- Capacité d'exécution distribuée et persistance de l'état des tâches.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Exécution fiable et reprise des tâches en échec. | Complexité de l'orchestration. |
| Coordination et surveillance centralisées. | Point de contrôle central à opérer et surveiller. |
| Répartition du travail entre agents. | Latence de coordination. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Exécution fiable et reprise des tâches distribuées. |
| Efficacité des performances | Répartition parallèle du travail. |

## Source

[Patron Scheduler Agent Supervisor – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/scheduler-agent-supervisor)
