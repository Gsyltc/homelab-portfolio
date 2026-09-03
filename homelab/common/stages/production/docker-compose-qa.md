---
slug: docker-compose-qa
phase: production
execution: CONDITIONAL
condition: "Vérification systématique d'un livrable compose (jamais sautée) — ignoré sous infra-terraform et branches autonomes"
lead_agent: QA Docker
support_agents: []
mode: subagent
summary_confirmation: required
reviewer: QA Docker
review_class: adversarial
review_artifact: rapport-qa-docker.md
human_gate: granular
produces: [rapport_qa_docker, coherence_traefik_verifiee]
consumes: [{artifact: livrable_compose, required: true}]
requires_stage: [docker-compose-creation]
sensors: [swarm-deploy-section, plaintext-secret, traefik-coherence]
scopes: [stack-update, new-stack, config-change, security-patch]
inputs: "Livrable docker-compose"
outputs: "Rapport QA (syntaxe, Swarm, hardening, Traefik) + corrections appliquées / proposées"
---

# Vérification du docker-compose (QA Docker)

## Objectif

Vérifier, corriger et durcir le docker-compose avant toute suite — vérification jamais sautée.

## Steps

### Step 1 — Déléguer au QA Docker

Le Tech Lead délègue au **QA Docker** (mission + mention valide). Ordre imposé : **tout compose passe par le QA Docker avant l'aiguillage du Tech Lead** ([`central-quality-control.md`](central-quality-control.md)).

### Step 2 — Analyser et corriger (revue adversariale — plancher SG-3)

Analyser syntaxe, compatibilité Swarm, réseaux / volumes / secrets, hardening (skills `docker-composer`, `dockerfile-validator`), classer les problèmes (critical / warning / info), appliquer / proposer les corrections. Le QA Docker porte le **contrôle sécurité technique** (revue adversariale) : sur `security-patch` / `new-stack`, vérification `renforcé` non abaissable.

### Step 3 — Cohérence Traefik

Vérifier via **`traefik-manager-read`** que services, middlewares et entrypoints sont cohérents (aucune `configErrors`). Présenter les éléments modifiés / corrigés et la conformité, puis **mentionner le Tech Lead** (mention valide).

## Sensors

Outputs: rapport QA + cohérence Traefik. Gate humain granulaire.
Imports: `swarm-deploy-section` (gate), `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**), `traefik-coherence` (gate).
Review artifact: `rapport-qa-docker.md` porte la section `## Review` (revue adversariale du QA Docker, plancher SG-3).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de non-conformité récurrents, patterns de hardening, corrections QA répétées) tracés, remontés au **gate humain granulaire** ; toute règle touchant la sécurité repasse au contrôle sécurité (Architecte de sécurité Homelab, SEC-2/SEC-4).
