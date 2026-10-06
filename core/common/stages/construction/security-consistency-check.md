---
slug: security-consistency-check
phase: construction
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecture Solution & Intégration
support_agents: [Architecte Cybersécurité]
mode: inline
summary_confirmation: required
reviewer: Reviewer de sécurité
review_class: adversarial
review_artifact: controle-securite-coherence.md
human_gate: none
produces: [controle_securite_coherence]
consumes: [{artifact: livrables_detailles, required: true}]
requires_stage: [detailed-deliverables]
sensors: [required-sections]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Livrables détaillés"
outputs: "Contrôle sécurité + cohérence documentation ↔ décisions structurantes, corrections demandées le cas échéant"
---

# Contrôle cohérence et sécurité

## Objectif

Vérifier la cohérence et la sécurité des livrables avant consolidation.

## Steps

Les revues sont **séquentielles** (**cohérence puis sécurité**) et transitent par le spécialiste auteur du livrable (mécanique OK/RENVOI : [`../../protocols/reviewer.md`](../../protocols/reviewer.md), encadré « Le reviewer retourne toujours au spécialiste »).

### Step 1 — Revue de cohérence

Le `consistency-reviewer-agent` vérifie structure, complétude, qualité, format et cohérence des livrables avec les décisions structurantes.

### Step 2 — Revue de sécurité (revue adversariale)

Pour tout livrable modifiant l'architecture (mêmes règles que `design-and-decisions`), le **Reviewer de sécurité** mène l'analyse de posture ; l'Architecte cybersécurité (voix adoptée `inline`) la pilote. Plancher SG-3 : aucun gate / sensor advisory, aucune revue de cohérence ne remplace ce contrôle adversarial.

## Sensors

Outputs: contrôle sécurité + cohérence consignés.
Imports: `required-sections` (documents de décision / DAS).
Review artifact: `controle-securite-coherence.md` porte la section `## Review` ajoutée par le Reviewer de sécurité.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de non-conformité sécurité / cohérence récurrents) ; les remonter au **gate humain** de Construction ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit (toute règle touchant la sécurité repasse au contrôle sécurité).
