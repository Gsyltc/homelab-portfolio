---
slug: auth-preselection
phase: initialisation
execution: ALWAYS
condition: "Always executes pour une demande de stack"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [auth_type_preselectionne]
consumes: [{artifact: detection_stack_existante_vs_nouvelle, required: true}, {artifact: lien_documentation_officielle, required: true}]
requires_stage: [deployment-target-preselection]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Stack détectée + documentation officielle (lue à l'étape 3 de l'amorçage)"
outputs: "Type d'authentification recommandé + justification"
---

# Pré-sélection du type d'authentification

## Objectif

Recommander le type d'authentification, pour que l'humain le valide au gate léger.

## Steps

### Step 1 — Stack existante

Si `stack-detection` a trouvé la stack, consigner le type actuel, déduit de sa configuration (règle de la skill `configuration-applications`, [`authentification.md`](../../../../plugins/homelab-assistant/skills/configuration-applications/references/authentification.md)). Fin du stage.

### Step 2 — Nouvelle stack

Lire la section authentification de la documentation officielle (OIDC / OAuth / SSO, désactivation de l'auth locale). Appliquer la règle d'auto-sélection (source unique : Step 2 de [`required-parameters-collection`](../cadrage/required-parameters-collection.md)). Consigner le type recommandé et sa justification (lien vers la section de la doc). En cas de doute, lister les options : l'humain tranche au gate léger.

## Sensors

Outputs: `auth_type_preselectionne` consigné sur l'issue et dans la section `auth` de `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/preselection.json` (format : sensor [`initial-proposal`](../../../sensors/sensors/initial-proposal.md)). Sans objet (ex. `infra-terraform`) : `sans_objet` + raison. Présenté au point 5 de [`intent-scope-approval`](../ideation/intent-scope-approval.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (patterns d'auth par famille d'applications) tracés, remontés **en fin de workflow**, dans un message séparé ([`closure`](../validation/closure.md)). La règle d'auto-sélection est un **invariant** (non abaissable par une règle apprise — SEC-1).
