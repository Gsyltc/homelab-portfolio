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
consumes: [{artifact: parametres_requis_complets, required: true}, {artifact: mode_execution_applique, required: true}]
requires_stage: [autonomy-mode]
sensors: [terraform-no-sni, plaintext-secret]
scopes: [stack-update, new-stack, security-patch, infra-terraform]
inputs: "Paramètres collectés en Cadrage (§2.4) + mode d'exécution appliqué"
outputs: "Fichiers .tf / .tfvars de la stack, déposés dans `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/` (jamais d'apply)"
---

# Configuration Terraform (Spécialiste Terraform)

## Objectif

Préparer les variables Terraform de la stack, sans jamais déployer. Ce stage s'exécute **en parallèle** du docker-compose ([`docker-compose-creation.md`](docker-compose-creation.md)) : les valeurs proviennent des **paramètres collectés en Cadrage (§2.4)**, jamais d'une déduction depuis un docker-compose.

## Steps

### Step 1 — Déléguer

Une fois le mode d'exécution appliqué ([`autonomy-mode.md`](autonomy-mode.md)), le Tech Lead ordonne au **Spécialiste Terraform** (mission + mention valide) de créer / modifier les **variables Terraform** de la stack (skill `configuration-applications`).

- La délégation se fait **en parallèle** de celle au Spécialiste Docker (deux sous-issues `--stage 1`). Verrou par artefact : [`governance-security.md`](../../protocols/governance-security.md) § concurrence.
- Les variables sont cohérentes avec les **paramètres collectés en Cadrage (§2.4)** : auth, `cloudflare_dns_nb`, domaine / FQDN d'exposition, etc.
- La sous-issue Terraform passe en `in_progress` dès que son travail démarre. Cycle : [`stage-protocol.md` § Cycle de statut des sous-issues & barrière de stage](../../protocols/stage-protocol.md#cycle-de-statut-des-sous-issues--barrière-de-stage).

Sur scope `new-stack` / `infra-terraform`, ce stage est **obligatoire et inconditionnel** : le Tech Lead ne peut ni le sauter ni le déclarer « non requis ». Ne pas produire le livrable `.tfvars` sur ces scopes est un **écart bloquant** (frontière `phase3-phase4`), non une décision légitime d'un coordinateur (invariant — SEC-1).

### Step 2 — Produire les fichiers (jamais d'apply)

Préparer uniquement les fichiers `.tf` / `.tfvars` :

- **JAMAIS** `terraform init/apply/destroy` (invariant absolu).
- **Jamais `${SNI}`** : écrire les domaines / URLs en clair.

Livraison :

1. Déposer les fichiers dans le **répertoire de relecture** (voir ci-dessous).
2. Appliquer le **geste de fin de mission** [`producer-report.md`](../../protocols/producer-report.md) : joindre le livrable `.tf` / `.tfvars` **et** le message A2A `retour` (`retour-terraform-<stack>.yaml`).
3. Livrable produit et compte-rendu rendu : la sous-issue Terraform passe en `in_review` (en attente de vérification QA). Cycle : [`stage-protocol.md` § Cycle de statut des sous-issues & barrière de stage](../../protocols/stage-protocol.md#cycle-de-statut-des-sous-issues--barrière-de-stage).

### Step 3 — Vérification QA en aval

Le livrable `.tfvars` produit passe **obligatoirement** par l'**Analyste QA** ([`quality-assurance.md`](quality-assurance.md), volet Terraform, skill `terraform-qa`) avant l'aiguillage du Tech Lead ([`central-quality-control.md`](central-quality-control.md)) : vérification systématique, jamais sautée. Sur défaut, l'Analyste QA émet un `RENVOI` dans son rapport YAML adressé au **Tech Lead**, qui renvoie au Spécialiste Terraform après synthèse avec la revue sécurité ; la QA ne modifie jamais le livrable.

> **Répertoire de relecture.** Fichiers générés déposés uniquement dans `.a-valider/<id-tâche>/<stack>/` : [`review-directory.md`](../../protocols/review-directory.md).

## Sensors

Outputs: livrable `.tfvars` lisible dans `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/` (et joint à l'issue), puis vérifié par l'Analyste QA. Gate humain granulaire **selon le mode d'exécution** ([`autonomy-mode`](autonomy-mode.md)) : gated → validation à ce stage ; autonome → regroupée au point de synchronisation.
Imports: `terraform-no-sni` (write — **bloquant sur `security-patch` / `new-stack`**, ALI-204), `plaintext-secret` (write — **bloquant sur `security-patch` / `new-stack`**). L'auteur en est **propriétaire** : ses verdicts, avec le `sha256` du `.tfvars`, voyagent dans le YAML `retour` et sont repris par la QA ([`governance-security.md`](../../protocols/governance-security.md) § « Un contrôle, un propriétaire »).
Upstream targets: `parametres_requis_complets` (required), `mode_execution_applique` (required).

## Learn

L'interdiction `terraform apply`, l'interdiction `${SNI}` et le caractère **obligatoire du livrable `.tfvars` sur `new-stack` / `infra-terraform`** sont des **invariants** non abaissables (SEC-1).
