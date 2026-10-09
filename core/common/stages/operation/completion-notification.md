---
slug: completion-notification
phase: operation
execution: CONDITIONAL
condition: "Exécuté après un déploiement / une administration, sur demande du coordinateur"
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
inputs: "Déploiement / administration réalisé"
outputs: "Notification de fin de déploiement à l'humain (canal porté par l'Agent de notifications)"
---

# Notification de fin de déploiement

## Objectif

Notifier l'humain de la fin du déploiement / de l'administration, via l'Agent de notifications qui porte l'outil adapté au harnais.

> **Distincte de la notification de fin de réalisation.** La notification « l'issue a été réalisée, fichiers / PR en attente » est envoyée **dès la mise à disposition** (fin de Construction, [`../construction/delivery-handoff.md`](../construction/delivery-handoff.md), Step 4). Ce stage-ci couvre la notification **post-déploiement**, uniquement lorsqu'un déploiement / une administration a eu lieu (`deployment-under-validation`). Si aucun déploiement n'est requis, ce stage est N/A et la seule notification du cycle est celle de la mise à disposition.

## Steps

### Step 1 — Solliciter l'Agent de notifications

Une fois le déploiement / l'administration réalisé et validé, le coordinateur demande à l'**Agent de notifications** (délégué en `subagent`) d'envoyer une notification : message court (« Déploiement réalisé »), identifiant de l'issue et lien si possible. Aucun secret dans la notification.

## Sensors

Outputs: notification envoyée (succès confirmé par l'Agent de notifications sur l'issue, selon le canal qu'il porte).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue tout candidat-règle (canal de notification, format récurrent) ; remontée et persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit (au gate d'Operation).
