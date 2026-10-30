---
slug: kestra-deployment
phase: validation
execution: CONDITIONAL
condition: "Uniquement sur « oui » explicite de l'humain pour lancer le déploiement Kestra (gate explicite standard, ou gate léger unique A1 sur scope service-version-update)"
lead_agent: Tech Lead Homelab
support_agents: [Spécialiste Déploiement Kestra]
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [deploiement_kestra_si_demande]
consumes: [{artifact: depot_fichiers_confirme, required: true}]
requires_stage: [file-deposit, version-update-application]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, service-version-update]
inputs: "Fichiers déposés et vérifiés (parcours standard) ou autorisation A1 + Terraform existant (service-version-update)"
outputs: "Flux Kestra configure_service lancé (sur validation explicite uniquement)"
---

# Déploiement Kestra (sur validation explicite uniquement)

## Objectif

Lancer le déploiement uniquement après un « oui » explicite de l'humain.

## Steps

### Step 1 — Demander et attendre le « oui » explicite

Le Tech Lead demande si l'humain souhaite lancer le déploiement via **Kestra**. **Uniquement après un « oui » explicite** : lancer le flux Kestra `configure_service`. Les fichiers doivent rester téléchargeables pour vérification.

### Step 2 — Garde-fou absolu

**Aucun lancement du flux `configure_service` sans validation humaine explicite de la configuration complète.** Action à impact → jamais autonome (invariant).

### Step 3 — Pré-requis selon le scope (exclusifs)

Le pré-requis amont de ce stage dépend du scope et les deux voies sont **mutuellement exclusives** :

- **Parcours standard** (`stack-update`, `new-stack`, `config-change`, `security-patch`, `infra-terraform`) → pré-requis [`file-deposit`](file-deposit.md), qui produit `depot_fichiers_confirme` après la validation humaine granulaire explicite.
- **Parcours `service-version-update`** → pré-requis [`version-update-application`](version-update-application.md), dont le **gate léger unique (A1)** produit `depot_fichiers_confirme` et autorise, dans la même acceptation, l'écriture Vault `VERSION` **et** ce déploiement. Aucun nouveau dépôt de fichiers : le flux `configure_service` réutilise le **fichier Terraform existant** du service. Aucune **seconde** validation n'est demandée ici sur ce parcours — le gate A1 en amont fait foi.

## Sensors

Outputs: déploiement lancé (conditionnel). Gate humain **explicite** (action à impact).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (patterns de déploiement Kestra) tracés, remontés au gate explicite.
