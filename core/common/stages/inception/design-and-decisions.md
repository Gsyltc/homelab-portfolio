---
slug: design-and-decisions
phase: inception
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Administrateur infrastructure Windows, OpenSpec Expert]
mode: mob
summary_confirmation: required
reviewer: Reviewer de sécurité
review_class: adversarial
review_artifact: decisions/<NNNN>-<titre>.md
human_gate: granular
produces: [decision_conception, diagramme_principal, conception_cible_validee]
consumes: [{artifact: besoins_traces, required: true}, {artifact: decoupage_livrables, required: true}]
requires_stage: [deliverables-breakdown]
sensors: [required-sections, upstream-coverage, diagram-validity]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Besoins tracés + découpage en livrables"
outputs: "Conception cible + décisions structurantes validées granulairement par l'humain, après contrôle sécurité"
---

# Conception d'architecture, décisions structurantes et contrôle sécurité

## Objectif

Produire la conception cible et les décisions structurantes, contrôlées en sécurité et validées granulairement.

## Steps

### Step 1 — Production de la conception (mob)

Les `support_agents` désignés travaillent **en parallèle contre le brouillon du lead** (Architecte de solution), en une ronde d'objection bornée (`mode: mob`) : vues fonctionnelle / technique, choix, alternatives, risques. Chaque décision structurante est **tracée** dans le registre de décisions du projet (`decisions/`).

### Step 2 — Contrôle sécurité obligatoire (revue adversariale)

À chaque modification d'architecture, le coordinateur sollicite le **Reviewer de sécurité**, **attend son analyse** (OWASP / STRIDE), intègre ses recommandations avant toute validation. Revue **adversariale, non substituable** (plancher SG-3). Normes spécifiques uniquement si explicitement demandées. Voir [`../../protocols/reviewer.md`](../../protocols/reviewer.md).

### Step 3 — Contrôle de cohérence

Vérifier la correspondance documentation ↔ décisions structurantes, l'absence de conflits ; demander les corrections aux agents responsables.

### Step 4 — Validation granulaire humaine

Présenter **chaque choix séparément** (choix, justification, alternative) ; boucle Keep / Modify / Redo. Ne pas avancer sur un élément non validé.

### Step 5 — Analyse de dette technique (Architecte de solution)

Évaluer le potentiel de réduction de dette et consigner des recommandations justifiées avec la décision (ou un registre de dette en annexe si aucune décision).

> Si OpenSpec activé : cette phase se matérialise par une **proposition OpenSpec** créée par l'OpenSpec Expert, qui notifie le coordinateur à `in_review`.

## Sensors

Outputs: conception + décisions validées. Frontière **Inception → Construction** : gate `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin`.
Imports: `required-sections`, `upstream-coverage`, `diagram-validity`.
Upstream targets: `besoins_traces` (required), `decoupage_livrables` (required) — couverture amont vérifiée à l'écriture de la décision / conception.
Review artifact: la **décision structurante** (`decisions/<NNNN>-<titre>.md`) porte la section `## Review` ajoutée par le Reviewer de sécurité.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de conception, arbitrages récurrents, recommandations de sécurité) ; les remonter au **gate humain granulaire** ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit (toute règle `workspace` repasse au contrôle sécurité).
