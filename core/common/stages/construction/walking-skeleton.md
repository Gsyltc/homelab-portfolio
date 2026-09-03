---
slug: walking-skeleton
phase: construction
execution: ALWAYS
condition: "Always executes — premier jalon de bout en bout, avant toute autonomie"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Infrastructure Windows, OpenSpec Expert]
mode: mob
summary_confirmation: required
reviewer: Reviewer de sécurité
review_class: adversarial
review_artifact: walking-skeleton.md
human_gate: granular
produces: [walking_skeleton_valide, mode_execution_choisi]
consumes: [{artifact: conception_cible_validee, required: true}, {artifact: decision_conception, required: true}]
requires_stage: [design-and-decisions]
sensors: [required-sections, diagram-validity]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Conception cible et décisions structurantes validées"
outputs: "Première tranche de bout en bout validée + mode d'exécution (gated / autonome) choisi une fois"
---

# Walking skeleton et choix du mode d'exécution

## Objectif
Valider la plus petite tranche de bout en bout, puis fixer le rythme de validation du reste du lot.

## Steps
### Step 1 — Produire le walking skeleton (mob)
Plus petit livrable **de bout en bout** prouvant que l'ossature tient (dans notre contexte documentaire : première vue d'architecture + sa décision de conception, ou premier module IaC / spec OpenSpec) ; les `support_agents` travaillent en `mob` contre le brouillon du lead. Il passe **obligatoirement** par la validation granulaire humaine et le **contrôle sécurité adversarial** (aucune autonomie avant lui).

### Step 2 — La question, posée une seule fois
Après validation du walking skeleton, poser **une seule** question pour le reste de la Construction : rythme **gated à chaque étape** *(défaut)* ou **autonome jusqu'au prochain point de synchronisation**. La réponse est consignée sur l'issue ; elle ne se présume jamais (pas de réponse ⇒ gated) ; un nouveau lot re-pose la question.

## Sensors
Outputs: walking skeleton validé + mode d'exécution consigné.
Imports: `required-sections`, `diagram-validity`.
Review artifact: `walking-skeleton.md` porte la section `## Review` ajoutée par le Reviewer de sécurité.

## Learn
Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs d'ossature, choix de mode d'exécution récurrents, recommandations de sécurité) ; les remonter au **gate humain granulaire** ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit. Divergence tracée vs le journal `memory.md` d'AI-DLC (voir [ADR-0009](../../../../decisions/0009-alignement-fiches-de-stage-sur-ai-dlc.md)).
