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
outputs: "Rapport QA JSON (syntaxe, Swarm, hardening, Traefik) — verdict OK / RENVOI / BLOQUE + classification des problèmes (critical / warning / info) ; sur défaut, RENVOI au Spécialiste Docker"
---

# Vérification du docker-compose (QA Docker)

## Objectif

Vérifier et durcir (par le contrôle) le docker-compose avant toute suite — vérification jamais sautée. **Le QA ne modifie jamais le livrable** : sur défaut, il émet un RENVOI au Spécialiste Docker via le rapport JSON.

## Steps

### Step 1 — Déléguer au QA Docker

Le Tech Lead délègue au **QA Docker** (mission + mention valide). Ordre imposé : **tout compose passe par le QA Docker avant l'aiguillage du Tech Lead** ([`central-quality-control.md`](central-quality-control.md)).

### Step 2 — Analyser et classer (revue adversariale — plancher SG-3)

Analyser syntaxe, compatibilité Swarm, réseaux / volumes / secrets, hardening (skill `docker-composer`), classer les problèmes (critical / warning / info) et rédiger chaque point de façon **autosuffisante** (`constat` / `cause` / `correction` / `domaine_correction`) dans le rapport JSON (`report-format.schema.json`) : sur au moins un défaut, le `verdict` est `RENVOI` et le rapport JSON est renvoyé au **Spécialiste Docker** (agent créateur du livrable) pour correction ; sans défaut, `verdict = OK`. **La skill `dockerfile-validator` s'applique uniquement aux stacks *build-from-source*** (celles qui fournissent un `Dockerfile` construit localement, `build:` dans le compose) : elle valide alors le `Dockerfile`. Pour une stack tirant des **images publiées** (pas de `Dockerfile` à construire), `dockerfile-validator` ne s'applique pas. Le QA Docker porte le **contrôle sécurité technique** (revue adversariale) : sur `security-patch` / `new-stack`, vérification `renforcé` non abaissable.

### Step 3 — Cohérence Traefik

Vérifier via **`traefik-manager-read`** que services, middlewares et entrypoints sont cohérents (aucune `configErrors`). Présenter la conformité et, le cas échéant, le verdict `RENVOI` avec les `id` des points à corriger, puis **rendre compte au Tech Lead** (le QA construit lui-même son lien de retour — cf. Point 1). Le QA **ne présente aucun livrable modifié** : il ne produit qu'un rapport.

## Sensors

Outputs: rapport QA + cohérence Traefik. Gate humain granulaire.
Imports: `swarm-deploy-section` (gate), `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**), `traefik-coherence` (gate).
Review artifact: `rapport-qa-docker.md` porte la section `## Review` (revue adversariale du QA Docker, plancher SG-3).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de non-conformité récurrents, patterns de hardening, corrections QA répétées) tracés, remontés au **gate humain granulaire** ; toute règle touchant la sécurité repasse au contrôle sécurité (Architecte de sécurité Homelab, SEC-2/SEC-4).
