---
slug: walking-skeleton
phase: construction
execution: ALWAYS
condition: "Always executes — premier jalon de bout en bout, avant toute autonomie"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Administrateur infrastructure Windows, OpenSpec Expert]
mode: multi-agent
summary_confirmation: required
reviewer: Architecte cybersécurité
review_class: granular
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
### Step 1 — Produire le walking skeleton
Plus petit livrable **de bout en bout** prouvant que l'ossature tient (dans notre contexte documentaire : première vue d'architecture + sa décision de conception, ou premier module IaC / spec OpenSpec). Il passe **obligatoirement** par la validation granulaire humaine et le contrôle sécurité (aucune autonomie avant lui).

### Step 2 — La question, posée une seule fois
Après validation du walking skeleton, poser **une seule** question pour le reste de la Construction : rythme **gated à chaque étape** *(défaut)* ou **autonome jusqu'au prochain point de synchronisation**. La réponse est consignée sur l'issue ; elle ne se présume jamais (pas de réponse ⇒ gated) ; un nouveau lot re-pose la question.

## Gate / sortie
Walking skeleton validé + mode d'exécution consigné.
