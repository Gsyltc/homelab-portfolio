---
slug: central-quality-control
phase: production
execution: ALWAYS
condition: "Always executes — aiguillage GO / RENVOI du Tech Lead sur chaque livrable"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: Tech Lead Homelab
review_class: advisory
review_artifact: controle-qualite-central.md
human_gate: granular
produces: [controle_qualite_central_go]
consumes: [{artifact: rapport_qa_docker, required: false}, {artifact: livrable_tfvars, required: false}, {artifact: flux_n8n_propose_ou_applique, required: false}, {artifact: modification_home_assistant_proposee_ou_appliquee, required: false}]
requires_stage: [docker-compose-qa]
sensors: [traefik-coherence]
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Livrables des spécialistes (compose vérifié, .tfvars, flux n8n, modif HA)"
outputs: "Aiguillage GO / RENVOI + décision de passage en Validation"
---

# Contrôle qualité central (Tech Lead — aiguillage GO / RENVOI)

## Objectif

Router chaque livrable (GO / RENVOI) au niveau macro, sans analyse technique de fond.

## Steps

### Step 1 — Contrôle macro (jamais technique)

Le Tech Lead vérifie uniquement : (a) le livrable répond-il à la demande et aux paramètres collectés ? (b) est-il du bon type et présent (compose / `.tfvars` avec les sections attendues, pas un rapport vide) — **jamais** la validité syntaxique, la compatibilité applicative ou les conventions, qui relèvent du QA Docker ; (c) un secret en clair saute-t-il aux yeux ? (d) le compte-rendu du spécialiste signale-t-il un blocage ?

### Step 2 — Ordre imposé et renvoi

Tout compose passe par le QA Docker ([`docker-compose-qa.md`](docker-compose-qa.md)) **avant** cet aiguillage. Le Tech Lead ne réalise **jamais** lui-même l'analyse de compatibilité, l'audit sécurité / hardening, la cohérence Traefik ni un correctif. Doute technique → renvoyer au spécialiste en décrivant le **symptôme** (« l'authentification risque d'échouer »), **sans** diagnostic ni solution. Livrable incomplet / hors-sujet → renvoyer avec la liste des manques.

## Sensors

Outputs: aiguillage GO / RENVOI consigné. Frontière **Production → Validation** : gate `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin` (voir [`homelab/sensors/gates.md`](../../../sensors/gates.md)).
Imports: `traefik-coherence` (gate).
Review artifact: `controle-qualite-central.md` porte la section `## Review` (advisory — revue portée par le **Tech Lead** lui-même ; le contrôle qualité central ne remplace jamais le contrôle sécurité ni la validation humaine, plancher SG-3).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de renvoi récurrents) tracés, remontés au **gate humain granulaire**.
