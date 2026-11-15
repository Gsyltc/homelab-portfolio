---
slug: review-and-notification
phase: validation
execution: ALWAYS
condition: "Always executes — passage in_review + notification revue prête"
lead_agent: Tech Lead Homelab
support_agents: [Agent de notifications]
mode: subagent
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [issue_in_review, notification_revue_prete]
consumes: [{artifact: prerequis_deploiement_verifies, required: true}]
requires_stage: [deployment-prereqs-check]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Livrables contrôlés et conformes"
outputs: "Issue passée en in_review + notification ntfy « revue prête »"
---

# Passage en revue et notification

## Objectif

Signaler à l'humain qu'une configuration contrôlée est prête à être revue.

## Steps

### Step 1 — Passer l'issue en revue

Quand Docker et Terraform sont contrôlés et conformes **et** que la revue sécurité ([`security-delegation`](../production/security-delegation.md)) est close, le Tech Lead passe l'issue en `in_review` (`multica issue status <issue-id> in_review`). **`in_review` signifie « prêt à être revu par l'humain »** et l'issue y demeure jusqu'à ce que l'humain statue.

### Step 2 — Demander la notification (Tech Lead uniquement)

Le Tech Lead demande à l'**Agent de notifications** (mention valide) une notification « revue par un humain prête », au format de [`output-format.md`](../../protocols/output-format.md) § 5 (prénom, phase, stack : `<Prénom>, merci de valider les livrables de la phase de <phase> pour la stack <stack>`). Les gates des phases précédentes déclenchent la même notification, chacune par le Tech Lead. **Les spécialistes n'appellent jamais l'Agent de notifications directement.**

## Sensors

Outputs: issue `in_review` + notification envoyée. Aucun gate humain à ce stage (le gate est porté par `human-granular-validation`).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles éventuels tracés, remontés **en fin de workflow**, dans un message séparé ([`closure`](closure.md)).
