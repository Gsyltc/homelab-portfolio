---
slug: kestra-deployment
phase: validation
execution: CONDITIONAL
condition: "Uniquement sur « oui » explicite de l'humain pour lancer le déploiement Kestra (gate explicite standard, ou gate léger unique sur scope service-version-update)"
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
inputs: "Fichiers déposés et vérifiés (parcours standard) ou autorisation du gate léger unique + Terraform existant (service-version-update)"
outputs: "Flux Kestra configure_service lancé (sur validation explicite uniquement)"
---

# Déploiement Kestra (sur validation explicite uniquement)

## Objectif

Lancer le déploiement uniquement après un « oui » explicite de l'humain.

## Steps

### Step 1 — Lire la réponse du gate final (« oui » explicite)

La question du déploiement est posée **dans le message de validation finale** ([`human-granular-validation`](human-granular-validation.md) Step 1, décision 4), avec l'environnement à préciser. Aucune question séparée après le dépôt.

- **« Oui » explicite uniquement** : lancer le flux Kestra `configure_service`.
  - Le « oui » atteste que les clés Vault de la stack existent (créées par l'humain, ou écrites par le Tech Lead sur « oui » à l'écriture des clés).
  - Le Tech Lead le vérifie à l'étape 2 avant tout lancement.
- **« Non » ou absence de réponse** : ne rien lancer ; les fichiers déposés restent en place.
- Réponse ambiguë (environnement manquant, par exemple) : seul cas où le Tech Lead repose la question.
- Les fichiers restent téléchargeables pour vérification.

> **Inputs MCP sur stack Docker Swarm (`deploy_stack` / `configure_service`).** Laisser `middleware` et `service_url` à leur valeur par défaut — ne jamais les renseigner ni les modifier. Le routage et le middleware d'authentification sont déjà portés par les labels Traefik du docker-compose (convention `docker-composer`, provider Swarm). Voir `RULE-GL-013` ([`../../../rules/global.md`](../../../rules/global.md)).

### Step 2 — Vérifier les clés Vault puis l'accès Kestra (prérequis du déploiement)

Après le « oui » (et après l'écriture des clés si la décision 3 était un « oui »), le Tech Lead contrôle dans l'ordre :

1. **Existence des clés Vault** listées au gate final (noms seuls, skill `homelab-vault-access`, jamais la valeur).
   - Clé absente : ne rien lancer, passer l'issue en `blocked` et signaler les clés manquantes à l'humain.
2. **Accessibilité du flux** `configure_service`, confirmée par le **Spécialiste Déploiement Kestra** (seul agent ayant l'accès Kestra), avant tout lancement.
   - Injoignable : ne rien lancer et le signaler à l'humain (dépôt manuel possible).

Dans tous les cas d'arrêt, les fichiers déposés restent en place.

### Step 3 — Garde-fou absolu

**Aucun lancement du flux `configure_service` sans validation humaine explicite de la configuration complète.** Action à impact → jamais autonome (invariant).

### Step 4 — Pré-requis selon le scope (exclusifs)

Le pré-requis amont de ce stage dépend du scope et les deux voies sont **mutuellement exclusives** :

- **Parcours standard** (`stack-update`, `new-stack`, `config-change`, `security-patch`, `infra-terraform`) → pré-requis [`file-deposit`](file-deposit.md), qui produit `depot_fichiers_confirme` après la validation humaine granulaire explicite.
- **Parcours `service-version-update`** → pré-requis [`version-update-application`](version-update-application.md), dont le **gate léger unique** produit `depot_fichiers_confirme` et autorise, dans la même acceptation, l'écriture Vault `VERSION` **et** ce déploiement. Aucun nouveau dépôt de fichiers : le flux `configure_service` réutilise le **fichier Terraform existant** du service. Aucune **seconde** validation n'est demandée ici sur ce parcours — le gate léger unique en amont fait foi.

## Sensors

Outputs: déploiement lancé (conditionnel). Gate humain **explicite** (action à impact).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (patterns de déploiement Kestra) tracés, remontés **en fin de workflow**, dans un message séparé ([`closure`](closure.md)).
