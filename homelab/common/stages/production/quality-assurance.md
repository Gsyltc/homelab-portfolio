---
slug: quality-assurance
phase: production
execution: CONDITIONAL
condition: "Vérification systématique de chaque livrable produit — compose ET Terraform (jamais sautée) ; ignoré sous branches autonomes. Sous infra-terraform : vérification du seul livrable Terraform (pas de compose)."
lead_agent: Analyste QA
support_agents: []
mode: subagent
summary_confirmation: required
reviewer: Analyste QA
review_class: adversarial
review_artifact: rapport-qa.md
human_gate: granular
produces: [rapport_qa, coherence_traefik_verifiee, verdict_terraform]
consumes: [{artifact: livrable_tfvars, required: false}, {artifact: livrable_compose, required: false}]
requires_stage: [terraform-configuration, docker-compose-creation]
sensors: [swarm-deploy-section, plaintext-secret, traefik-coherence, terraform-no-sni]
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Livrables produits : docker-compose et / ou configuration Terraform (.tfvars)"
outputs: "Rapport QA JSON par livrable (compose : syntaxe, Swarm, hardening, Traefik ; Terraform : structure HCL, template, variables, absence de ${SNI}/secret) — verdict OK / RENVOI / BLOQUE + classification (critical / warning / info) ; sur défaut, RENVOI à l'agent créateur (Spécialiste Docker ou Spécialiste Terraform)"
---

# Vérification qualité des livrables (Analyste QA)

## Objectif

Vérifier et durcir (par le contrôle) chaque livrable de la stack avant toute suite — **docker-compose ET configuration Terraform** — vérification jamais sautée. **L'Analyste QA ne modifie jamais le livrable** : sur défaut, il émet un RENVOI vers l'agent **créateur** (Spécialiste Docker pour le compose, Spécialiste Terraform pour le `.tfvars`) via le rapport JSON.

> **Périmètre par scope.** Sur `new-stack` / `stack-update` / `security-patch` : l'Analyste QA vérifie le Terraform (produit en premier) **puis** le compose. Sous `infra-terraform` : il vérifie **uniquement le Terraform** (aucun compose n'est produit). Sous `config-change` : au juste nécessaire selon les livrables présents.

## Steps

### Step 1 — Déléguer à l'Analyste QA

Le Tech Lead délègue à l'**Analyste QA** (mission + mention valide). Ordre imposé : **tout livrable (compose ou Terraform) passe par l'Analyste QA avant l'aiguillage du Tech Lead** ([`central-quality-control.md`](central-quality-control.md)). Le Terraform étant produit avant le compose, il est vérifié en premier.

### Step 2 — Vérifier le Terraform (volet `.tfvars`, skill `terraform-qa`)

Sur les scopes produisant du Terraform, analyser le livrable `.tfvars` (skill `terraform-qa`) : structure HCL, conformité au template de configuration de stack, cohérence des variables (dont `cloudflare_dns_nb`), **absence de `${SNI}`** (domaines / URLs en clair — critique), **absence de secret en clair** (critique), absence de toute exécution Terraform. Classer les problèmes (critical / warning / info), rédiger chaque point de façon **autosuffisante** (`constat` / `cause` / `correction` / `domaine_correction`) dans le rapport JSON (`report-format.schema.json`) : sur au moins un défaut `critical` / `warning`, `verdict = RENVOI` vers le **Spécialiste Terraform** (agent créateur) ; sinon `verdict = OK`.

### Step 3 — Analyser et classer le compose (revue adversariale — plancher SG-3)

Sur les scopes produisant un compose, analyser syntaxe, compatibilité Swarm, réseaux / volumes / secrets, hardening (skill `docker-composer`), classer les problèmes (critical / warning / info) et rédiger chaque point de façon **autosuffisante** dans le rapport JSON : sur au moins un défaut, le `verdict` est `RENVOI` et le rapport JSON est renvoyé au **Spécialiste Docker** (agent créateur du livrable) pour correction ; sans défaut, `verdict = OK`. **La skill `dockerfile-validator` s'applique uniquement aux stacks *build-from-source*** (celles qui fournissent un `Dockerfile` construit localement, `build:` dans le compose) : elle valide alors le `Dockerfile`. Pour une stack tirant des **images publiées** (pas de `Dockerfile` à construire), `dockerfile-validator` ne s'applique pas. L'Analyste QA porte le **contrôle sécurité technique** (revue adversariale) sur les deux livrables : sur `security-patch` / `new-stack`, vérification `renforcé` non abaissable.

### Step 4 — Cohérence Traefik

Vérifier via **`traefik-manager-read`** que services, middlewares et entrypoints sont cohérents (aucune `configErrors`). Présenter la conformité et, le cas échéant, le verdict `RENVOI` avec les `id` des points à corriger, puis **rendre compte au Tech Lead** (l'Analyste QA construit lui-même son lien de retour — cf. Point 1). L'Analyste QA **ne présente aucun livrable modifié** : il ne produit qu'un rapport.

## Sensors

Outputs: rapport(s) QA (compose et / ou Terraform) + cohérence Traefik + verdict Terraform. Gate humain granulaire.
Imports: `swarm-deploy-section` (gate), `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**), `traefik-coherence` (gate), `terraform-no-sni` (write — **bloquant sur `security-patch` / `new-stack`**, ALI-204).
Review artifact: `rapport-qa.md` porte la section `## Review` (revue adversariale de l'Analyste QA, plancher SG-3).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de non-conformité récurrents compose ou Terraform, patterns de hardening, corrections QA répétées) tracés, remontés au **gate humain granulaire** ; toute règle touchant la sécurité repasse au contrôle sécurité (Architecte de sécurité Homelab, SEC-2/SEC-4).
