---
slug: scope-detection
phase: ideation
execution: ALWAYS
condition: "Always executes — auto-détection puis confirmation explicite du scope"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [scope_propose, axes_proposes]
consumes: [{artifact: intention_capturee, required: true}, {artifact: faisabilite_evaluee, required: false}]
requires_stage: [feasibility-arbitration]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Intention capturée + faisabilité"
outputs: "Scope auto-détecté + axes Depth / vérification proposés (confirmés au gate léger)"
---

# Auto-détection du scope et des axes

## Objectif

Router la demande vers un scope nommé et proposer ses axes d'exécution.

## Steps

### Step 1 — Auto-détecter le scope

Auto-détecter le scope par mots-clés (FR / EN, champ `keywords:` des fichiers [`homelab/scopes/`](../../../scopes/README.md)). En cas de correspondances multiples, **le niveau le plus élevé l'emporte** (voir [`../../protocols/scopes-and-axes.md`](../../protocols/scopes-and-axes.md)). **Le doute ne bascule jamais vers `config-change`.**

### Step 2 — Court-circuit des branches autonomes

Rappel : `n8n` / `home-assistant` court-circuitent immédiatement vers leur branche autonome (la règle absolue n8n s'applique dès qu'un déclencheur n8n est présent — voir [`../cadrage/n8n-absolute-rule.md`](../cadrage/n8n-absolute-rule.md)).

### Step 3 — Proposer les axes

Proposer les axes **Depth** et **vérification** par défaut du scope (projection lisible ; le fichier `homelab/scopes/<name>.md` fait foi). Le scope n'est **confirmé** qu'au gate léger (`intent-scope-approval`) — jamais de démarrage silencieux.

## Sensors

Outputs: scope + axes proposés consignés. Confirmation au gate léger.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de routage de scope) tracés, remontés au gate léger.
