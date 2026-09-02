---
slug: design-and-decisions
phase: inception
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Administrateur infrastructure Windows, OpenSpec Expert]
mode: multi-agent
summary_confirmation: required
reviewer: Architecte cybersécurité
review_class: granular
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
### Step 1 — Production de la conception
Les agents désignés produisent leurs livrables (vues fonctionnelle / technique, choix, alternatives, risques) et **tracent chaque décision structurante** dans le registre de décisions du projet.

### Step 2 — Contrôle sécurité obligatoire (Architecte cybersécurité)
À chaque modification d'architecture, le coordinateur sollicite l'**Architecte cybersécurité**, **attend son analyse**, intègre ses recommandations avant toute validation. Normes spécifiques uniquement si explicitement demandées. Voir [`../../protocols/reviewer.md`](../../protocols/reviewer.md).

### Step 3 — Contrôle de cohérence
Vérifier la correspondance documentation ↔ décisions structurantes, l'absence de conflits ; demander les corrections aux agents responsables.

### Step 4 — Validation granulaire humaine
Présenter **chaque choix séparément** (choix, justification, alternative) ; boucle Keep / Modify / Redo. Ne pas avancer sur un élément non validé.

### Step 5 — Analyse de dette technique (Architecte de solution)
Évaluer le potentiel de réduction de dette et consigner des recommandations justifiées avec la décision (ou un registre de dette en annexe si aucune décision).

> Si OpenSpec activé : cette phase se matérialise par une **proposition OpenSpec** créée par l'OpenSpec Expert, qui notifie le coordinateur à `in_review`.

## Gate / sortie
Conception + décisions validées. Frontière **Inception → Construction** : gate `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin` + sensors `required-sections` / `upstream-coverage` / `diagram-validity`.
