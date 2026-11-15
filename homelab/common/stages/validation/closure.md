---
slug: closure
phase: validation
execution: ALWAYS
condition: "Always executes — clôture après validation humaine"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [issue_close]
consumes: [{artifact: validation_humaine_explicite, required: true}, {artifact: depot_fichiers_confirme, required: false}, {artifact: deploiement_kestra_si_demande, required: false}]
requires_stage: [file-deposit]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, n8n, home-assistant]
inputs: "Validation humaine + dépôt / déploiement"
outputs: "Issue passée à Done, récapitulatif des livrables et emplacements"
---

# Clôture

## Objectif

Clore l'issue uniquement après la validation humaine, avec récapitulatif.

## Steps

### Step 1 — Passer à Done après validation humaine

Passer l'issue à **Done** **uniquement** après la validation humaine, avec le récapitulatif des livrables et leur emplacement. `Done` reste une décision humaine.

### Step 2 — Capitalisation des règles (fin de workflow, message séparé)

Les candidats-règles ne sont **jamais** présentés pendant un gate de validation de livrable. Ils sont consignés sur l'issue au fil du workflow (balise `[candidat-règle]`) puis remontés **une seule fois, ici**, **dans un message distinct** de celui de la validation des livrables, du dépôt et du déploiement.

- **Quand** : après la décision finale de l'humain sur les livrables (validation, dépôt, déploiement ou refus), jamais avant.
- **Forme** : [`output-format`](../../protocols/output-format.md), une décision par candidat (règle courte, couche et portée proposées, **proposition par défaut**), réponse ✅ Keep / 💬 Modify / ❌ Redo par candidat. Une notification courte accompagne le message (`<Prénom>, merci de statuer sur les règles proposées de la phase de clôture pour la stack <stack>`).
- **Aucun candidat** : aucun message, aucune notification.
- **Après réponse** : contrôle de conflit à l'admission, contrôle sécurité de l'Architecte de sécurité Homelab pour toute règle `global` ou touchant la sécurité, écriture dans `homelab/rules/` avec identifiant, date et lien vers l'issue. Une règle écrite s'applique au **prochain** workflow, jamais au run courant. Le candidat sans réponse n'est **pas** écrit.
- Ce message ne bloque pas la clôture : `Done` reste la décision humaine du Step 1.

## Sensors

Outputs: issue close + récapitulatif. Frontière **Validation → Clôture** : gate `artefacts-presents` (validation explicite, dépôt confirmé, déploiement si demandé) + sensor `vault-secret-exists` — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : bilan des candidats-règles du workflow ; persistance des apprentissages **confirmés** dans `homelab/rules/` (application au prochain workflow, jamais au run courant).
