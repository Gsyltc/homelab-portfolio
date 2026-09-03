---
slug: intent-scope-approval
phase: ideation
execution: ALWAYS
condition: "Always executes — gate humain léger"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: light
produces: [intention_perimetre_approuves, scope_confirme]
consumes: [{artifact: intention_capturee, required: true}, {artifact: scope_propose, required: true}, {artifact: axes_proposes, required: true}]
requires_stage: [scope-detection]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Intention capturée, scope + axes proposés"
outputs: "Intention + périmètre approuvés (gate léger), scope confirmé"
---

# Approbation de l'intention et du périmètre (gate humain léger)

## Objectif

Valider *qu'on part dans la bonne direction* et confirmer le scope, avant d'engager le Cadrage.

## Steps

### Step 1 — Présenter à l'humain

Présenter : l'**intention** reformulée, le **scope** proposé, ses **axes** (Depth / vérification).

### Step 2 — Gate léger (Keep / Modify / Redo)

L'humain approuve ou ajuste. C'est un gate **léger** : il valide *quoi* et *jusqu'où*, pas *comment* (les paramètres détaillés sont figés en Cadrage). Sur les scopes légers (`config-change`), ce gate reste **resserré** mais n'est jamais supprimé. Rien n'engage le Cadrage tant que l'intention et le périmètre ne sont pas approuvés et le scope confirmé (l'auto-détection est un plancher : la confirmation peut monter le contrôle, jamais le descendre sans trace).

## Sensors

Outputs: intention + périmètre approuvés, scope confirmé. Frontière **Idéation → Cadrage** : gate `artefacts-presents` (intention, scope confirmé) + approbation périmètre tracée — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : ce stage **porte le gate humain léger** d'Idéation — le Tech Lead y remonte les candidats-règles capturés depuis `intent-capture`, formulés en règles courtes (couche + portée proposées). L'humain garde ✅ / rejette ❌ / reformule 💬 chaque candidat séparément ; persistance des apprentissages **confirmés** dans `homelab/rules/` (jamais dans le run courant — application au prochain workflow).
