---
slug: autonomy-mode
phase: production
execution: ALWAYS
condition: "Always executes — walking skeleton puis question du mode, une seule fois par lot"
lead_agent: Tech Lead Homelab
support_agents: [Spécialiste Docker, QA Docker]
mode: pipeline
summary_confirmation: required
reviewer: QA Docker
review_class: adversarial
review_artifact: walking-skeleton.md
human_gate: granular
produces: [walking_skeleton_valide, mode_execution_choisi]
consumes: [{artifact: parametres_requis_complets, required: true}]
requires_stage: [required-parameters-collection]
sensors: [yaml-validity, swarm-deploy-section]
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Paramètres requis complets"
outputs: "Walking skeleton validé + mode d'exécution (gated / autonome) choisi une fois"
---

# Walking skeleton et choix du mode d'autonomie

## Objectif

Valider la plus petite tranche cohérente, puis fixer le rythme de validation du reste du lot.

## Steps

### Step 1 — Walking skeleton (premier jalon validé)

La plus petite tranche cohérente du lot (ex. squelette du docker-compose vérifié par le QA Docker, ou premier `.tfvars`) passe **obligatoirement** par le QA Docker ([`docker-compose-qa.md`](docker-compose-qa.md)), le contrôle qualité central ([`central-quality-control.md`](central-quality-control.md)) et la validation granulaire. **Aucune autonomie avant ce jalon.**

### Step 2 — La question, posée une seule fois

Après validation du walking skeleton, le Tech Lead demande, pour le **reste du lot déjà cadré** : rythme **gated à chaque étape** *(défaut)* ou **autonome jusqu'au prochain point de synchronisation**. En autonome, la validation granulaire est **regroupée** en un point de synchronisation (l'humain valide en bloc, **toujours choix par choix**). Réponse consignée sur l'issue, **jamais présumée** (pas de réponse ⇒ gated), un nouveau lot **re-pose** la question.

### Step 3 — Halt-and-ask systématique + réversibilité

Quel que soit le mode, l'exécution **s'arrête et interroge l'humain** sur : échec / impossibilité d'un livrable ; écart ou contrôle de sécurité requis ; gate / sensor en écart, bloquant, ou `⛔ indisponible` ; décision structurante nouvelle non cadrée ; toute **action à impact / destructive** (dépôt, Kestra, n8n, Home Assistant) — **jamais autonome**. Retour en gated possible à tout point de synchronisation. Sur `security-patch` / `new-stack`, le plancher `renforcé` et le halt-and-ask sécurité restent **pleins**.

## Sensors

Outputs: walking skeleton validé + mode consigné.
Imports: `yaml-validity` (write), `swarm-deploy-section` (gate).
Review artifact: `walking-skeleton.md` porte la section `## Review` du QA Docker (revue adversariale, plancher SG-3).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs d'ossature, choix de mode récurrents) tracés, remontés au **gate humain granulaire** ; persistance des apprentissages **confirmés** dans `homelab/rules/` via capture → confirmation humaine → contrôle de conflit.
