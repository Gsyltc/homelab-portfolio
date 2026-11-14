---
slug: autonomy-mode
phase: production
execution: ALWAYS
condition: "Always executes — applique le mode d'exécution choisi en Cadrage"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [mode_execution_applique]
consumes: [{artifact: parametres_requis_complets, required: true}, {artifact: mode_execution_choisi, required: true}]
requires_stage: [required-parameters-collection]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Paramètres requis complets + mode d'exécution choisi en Cadrage"
outputs: "Mode d'exécution appliqué au lot"
---

# Mode d'exécution du lot

## Objectif

Fixer le rythme de validation de la Production et les cas d'arrêt.

## Steps

### Step 1 — Mode d'exécution (source unique)

Options proposées dans le message unique de [`required-parameters-collection`](../cadrage/required-parameters-collection.md) :

- **gated** *(défaut)* : validation granulaire à chaque étape de production ;
- **autonome jusqu'au prochain point de synchronisation** : la validation granulaire est regroupée en un point de synchronisation (l'humain valide en bloc, **toujours choix par choix**).

Réponse consignée sur l'issue, **jamais présumée** (pas de réponse ⇒ gated). Un nouveau lot **re-pose** la question. Ce stage applique la réponse, sans nouvelle question.

Stages concernés par le mode : `terraform-configuration`, `docker-compose-creation`, `quality-assurance`, `central-quality-control`. Non concernés : l'arrêt sécurité de `security-delegation` et le halt-and-ask (Step 2), qui s'appliquent dans les deux modes, et la validation humaine granulaire finale (`human-granular-validation`), toujours posée.

### Step 2 — Halt-and-ask systématique + réversibilité

Quel que soit le mode, l'exécution **s'arrête et interroge l'humain** sur : échec / impossibilité d'un livrable ; écart ou contrôle de sécurité requis ; gate / sensor en écart, bloquant, ou `⛔ indisponible` ; décision structurante nouvelle non cadrée ; toute **action à impact / destructive** (dépôt, Kestra, n8n, Home Assistant) — **jamais autonome**. Retour en gated possible à tout point de synchronisation. Sur `security-patch` / `new-stack`, le plancher `renforcé` et le halt-and-ask sécurité restent **pleins**.

## Sensors

Outputs: mode appliqué consigné. Aucun gate humain à ce stage.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (choix de mode récurrents) tracés, remontés au **gate humain granulaire** ; persistance des apprentissages **confirmés** dans `homelab/rules/` via capture → confirmation humaine → contrôle de conflit.
