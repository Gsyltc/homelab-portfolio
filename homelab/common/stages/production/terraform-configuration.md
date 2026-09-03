---
slug: terraform-configuration
phase: production
execution: CONDITIONAL
condition: "Config Terraform requise (accentué sous infra-terraform / new-stack ; ignoré sous config-change et branches autonomes)"
lead_agent: Spécialiste Terraform
support_agents: []
mode: subagent
summary_confirmation: required
reviewer: null
review_class: none
human_gate: granular
produces: [livrable_tfvars]
consumes: [{artifact: parametres_requis_complets, required: true}, {artifact: rapport_qa_docker, required: false}]
requires_stage: [docker-compose-qa]
sensors: [terraform-no-sni, plaintext-secret]
scopes: [stack-update, new-stack, security-patch, infra-terraform]
inputs: "Paramètres collectés + travail QA Docker contrôlé"
outputs: "Fichiers .tf / .tfvars de la stack, téléchargeables (jamais d'apply)"
---

# Configuration Terraform (Spécialiste Terraform)

## Objectif

Préparer les variables Terraform de la stack, sans jamais déployer.

## Steps

### Step 1 — Déléguer après contrôle du QA Docker

Après contrôle du travail de QA Docker, le Tech Lead ordonne au **Spécialiste Terraform** (mission + mention valide) de créer / modifier les **variables Terraform** de la stack (skill `configuration-applications`), cohérentes avec les paramètres collectés.

### Step 2 — Produire les fichiers (jamais d'apply)

Préparer uniquement les fichiers `.tf` / `.tfvars` — **JAMAIS** `terraform init/apply/destroy` (invariant absolu). **Jamais `${SNI}`** : écrire les domaines / URLs en clair. Déposer le livrable **téléchargeable** et **mentionner le Tech Lead** (mention valide).

## Sensors

Outputs: livrable `.tfvars` téléchargeable. Gate humain granulaire.
Imports: `terraform-no-sni` (write — **bloquant sur `security-patch` / `new-stack`**, ALI-204), `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**).
Upstream targets: `parametres_requis_complets` (required).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (conventions Terraform, `.tfvars`, interdiction `${SNI}`) tracés, remontés au **gate humain granulaire** ; l'interdiction `terraform apply` et `${SNI}` sont des **invariants** (non abaissables — SEC-1).
