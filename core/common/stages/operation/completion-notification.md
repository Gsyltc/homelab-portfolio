---
slug: completion-notification
phase: operation
execution: CONDITIONAL
condition: "Exécuté après réalisation et revue, sur demande du coordinateur"
lead_agent: Agent de notifications
support_agents: []
mode: subagent
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [notification_fin]
consumes: [{artifact: plan_ou_configuration_valide, required: false}]
requires_stage: [deployment-under-validation]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, express, enterprise]
inputs: "Tâche réalisée et passée en revue"
outputs: "Notification de fin de tâche à l'humain (canal porté par l'Agent de notifications)"
---

# Notification de fin

## Objectif

Notifier l'humain de la fin de la tâche, via l'Agent de notifications qui porte l'outil adapté au harnais.

## Steps

### Step 1 — Solliciter l'Agent de notifications

Une fois la tâche réalisée et revue, le coordinateur demande à l'**Agent de notifications** (délégué en `subagent`) d'envoyer une notification : message court (« L'issue a été réalisée »), identifiant de l'issue et lien si possible. Aucun secret dans la notification.

## Sensors

Outputs: notification envoyée (succès confirmé par l'Agent de notifications sur l'issue, selon le canal qu'il porte).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue tout candidat-règle (canal de notification, format récurrent) ; remontée et persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit (au gate d'Operation).
