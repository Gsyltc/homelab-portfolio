---
slug: auth-preselection
phase: ideation
execution: CONDITIONAL
condition: "Exécuté si la documentation officielle est déjà connue et précise les types d'authentification"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: optional
reviewer: null
review_class: none
human_gate: none
produces: [auth_type_preselectionne]
consumes: [{artifact: intention_capturee, required: true}]
requires_stage: [scope-detection]
sensors: []
scopes: [stack-update, new-stack, security-patch]
inputs: "Documentation officielle (si déjà connue)"
outputs: "Type d'authentification pré-sélectionné (valeur de cadrage, figée en Cadrage)"
---

# Pré-sélection du type d'authentification

## Objectif

Amorcer le choix du type d'authentification comme valeur de cadrage, sans le figer.

## Steps

### Step 1 — Appliquer la règle d'auto-sélection

Si la documentation officielle est déjà connue, appliquer la règle d'auto-sélection `${auth_type}` selon l'ordre de priorité — **le premier disponible ET gratuit l'emporte** : `oidc → saml → ldap → forwardauth → local` (détail dans [`../cadrage/required-parameters-collection.md`](../cadrage/required-parameters-collection.md)).

### Step 2 — En cas de doute

**En cas de doute → demander à l'humain** et attendre. Le doute ne bascule jamais vers un choix implicite. La valeur reste **de cadrage** ; elle est figée en Cadrage (`required-parameters-collection`).

## Sensors

Outputs: `${auth_type}` pré-sélectionné consigné (valeur de cadrage). Aucun gate humain à ce stage.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (patterns d'auth par famille d'applications) tracés, remontés au gate léger. La règle d'auto-sélection est un **invariant** (non abaissable par une règle apprise — SEC-1).
