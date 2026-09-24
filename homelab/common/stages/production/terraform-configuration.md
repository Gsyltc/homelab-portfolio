---
slug: terraform-configuration
phase: production
execution: CONDITIONAL
condition: "OBLIGATOIRE et inconditionnelle sur scope ∈ {new-stack, infra-terraform} (livrable .tfvars non abaissable, conditionne la clôture) ; accentuée sous stack-update / security-patch ; ignorée sous config-change et branches autonomes"
lead_agent: Spécialiste Terraform
support_agents: []
mode: subagent
summary_confirmation: required
reviewer: null
review_class: none
human_gate: granular
produces: [livrable_tfvars]
consumes: [{artifact: parametres_requis_complets, required: true}, {artifact: walking_skeleton_valide, required: true}]
requires_stage: [autonomy-mode]
sensors: [terraform-no-sni, plaintext-secret]
scopes: [stack-update, new-stack, security-patch, infra-terraform]
inputs: "Paramètres collectés en Cadrage (§2.4) + walking skeleton validé"
outputs: "Fichiers .tf / .tfvars de la stack, téléchargeables (jamais d'apply)"
---

# Configuration Terraform (Spécialiste Terraform)

## Objectif

Préparer les variables Terraform de la stack, sans jamais déployer. **Ce stage passe avant le docker-compose** : les valeurs des variables Terraform proviennent des **paramètres collectés en Cadrage (§2.4)**, jamais d'une déduction depuis un docker-compose (qui n'existe pas encore à ce stade).

## Steps

### Step 1 — Déléguer après le walking skeleton

Après le walking skeleton validé ([`autonomy-mode.md`](autonomy-mode.md)), le Tech Lead ordonne au **Spécialiste Terraform** (mission + mention valide) de créer / modifier les **variables Terraform** de la stack (skill `configuration-applications`), cohérentes avec les **paramètres collectés en Cadrage (§2.4)** — auth, `cloudflare_dns_nb`, domaine / FQDN d'exposition, etc. — et non plus déduites d'un docker-compose en aval.

Sur scope `new-stack` / `infra-terraform`, ce stage est **obligatoire et inconditionnel** : le Tech Lead ne peut ni le sauter ni le déclarer « non requis ». Ne pas produire le livrable `.tfvars` sur ces scopes est un **écart bloquant** (frontière `phase3-phase4`), non une décision légitime d'un coordinateur (invariant — SEC-1).

### Step 2 — Produire les fichiers (jamais d'apply)

Préparer uniquement les fichiers `.tf` / `.tfvars` — **JAMAIS** `terraform init/apply/destroy` (invariant absolu). **Jamais `${SNI}`** : écrire les domaines / URLs en clair. Puis appliquer le **geste de fin de mission** [`../../protocols/producer-report.md`](../../protocols/producer-report.md) : ne joindre que le livrable `.tf` / `.tfvars` (aucun fichier de rapport), corps minimal (mention valide du Tech Lead + une ligne de statut), zéro prose. Sans mention valide → compte-rendu réputé non rendu, flux arrêté.

### Step 3 — Vérification QA en aval

Le livrable `.tfvars` produit passe **obligatoirement** par l'**Analyste QA** ([`quality-assurance.md`](quality-assurance.md), volet Terraform, skill `terraform-qa`) avant l'aiguillage du Tech Lead ([`central-quality-control.md`](central-quality-control.md)) : vérification systématique, jamais sautée. Sur défaut, l'Analyste QA émet un `RENVOI` vers le **Spécialiste Terraform** (agent créateur) via le rapport JSON ; il ne modifie jamais le livrable.

## Sensors

Outputs: livrable `.tfvars` téléchargeable, puis vérifié par l'Analyste QA. Gate humain granulaire.
Imports: `terraform-no-sni` (write — **bloquant sur `security-patch` / `new-stack`**, ALI-204), `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**).
Upstream targets: `parametres_requis_complets` (required), `walking_skeleton_valide` (required).

## Learn

L'interdiction `terraform apply`, l'interdiction `${SNI}` et le caractère **obligatoire du livrable `.tfvars` sur `new-stack` / `infra-terraform`** sont des **invariants** non abaissables (SEC-1).
