---
slug: human-granular-validation
phase: validation
execution: ALWAYS
condition: "Always executes — validation humaine granulaire (issue reste in_review)"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [validation_humaine_explicite]
consumes: [{artifact: issue_in_review, required: true}]
requires_stage: [review-and-notification]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Configuration complète (Docker + Terraform), fichiers téléchargeables"
outputs: "Validation humaine explicite (ou demande de modifications → retour en Production)"
---

# Validation humaine granulaire

## Objectif

Obtenir la validation explicite, choix par choix, avant toute action à impact.

## Steps

### Step 1 — Soumettre la configuration complète

Le Tech Lead soumet à l'humain la **configuration complète** (Docker + Terraform), fichiers téléchargeables à l'appui, et demande une **validation explicite**. **L'issue reste en `in_review`** pendant toute cette phase ; rien n'avance sur un élément non validé (boucle Keep / Modify / Redo, chaque choix séparément).

### Step 2 — Modifications demandées → retour en Production

Si l'humain **demande des modifications** (rejet total ou partiel) → le Tech Lead repasse l'issue en `in_progress`, poursuit le workflow en intégrant les modifications (nouvelle itération des stages de Production concernés + re-contrôle central), puis repasse en `in_review` une fois la nouvelle version prête.

### Step 3 — Validation → dépôt

Si l'humain **valide** → poursuivre en [`file-deposit.md`](file-deposit.md).

## Sensors

Outputs: validation humaine explicite consignée. C'est le gate décisionnel **explicite** d'Operation — l'unique gate contraignant (invariant).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : ce stage **porte le gate explicite** — le Tech Lead y remonte les candidats-règles capturés en Production, formulés en règles courtes ; persistance des apprentissages **confirmés** dans `homelab/rules/` (jamais dans le run courant).
