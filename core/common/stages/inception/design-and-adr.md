---
slug: design-and-adr
phase: inception
execution: ALWAYS
condition: "Always executes"
lead_agent: Manuel
support_agents: [Florian, Admin, Fabien]
mode: multi-agent
summary_confirmation: required
reviewer: Xavier
review_class: granular
human_gate: granular
produces: [adr_conception, diagramme_principal, conception_cible_validee]
consumes: [{artifact: besoins_traces, required: true}, {artifact: decoupage_livrables, required: true}]
requires_stage: [deliverables-breakdown]
sensors: [required-sections, upstream-coverage, diagram-validity]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Besoins tracés + découpage en livrables"
outputs: "Conception cible + ADR validés granulairement par l'humain, après contrôle sécurité Xavier"
---

# Conception d'architecture, ADR et contrôle sécurité

## Objectif
Produire la conception cible et les ADR, contrôlés en sécurité et validés granulairement.

## Steps
### Step 1 — Production de la conception
Les agents désignés produisent leurs livrables (vues fonctionnelle / technique, choix, alternatives, risques) et **tracent chaque décision structurante dans un ADR**.

### Step 2 — Contrôle sécurité obligatoire (Xavier)
À chaque modification d'architecture, le coordinateur sollicite **Xavier** (`694a1a6f-9659-48ea-b45f-43ae6dc01706`), **attend son analyse**, intègre ses recommandations avant toute validation. Normes spécifiques uniquement si explicitement demandées. Voir [`../../protocols/reviewer.md`](../../protocols/reviewer.md).

### Step 3 — Contrôle de cohérence ADR
Vérifier la correspondance documentation ↔ ADR, l'absence de conflits ; demander les corrections aux agents responsables.

### Step 4 — Validation granulaire humaine
Présenter **chaque choix séparément** (choix, justification, alternative) ; boucle Keep / Modify / Redo. Ne pas avancer sur un élément non validé.

### Step 5 — Analyse de dette technique (Manuel)
Évaluer le potentiel de réduction de dette et consigner des recommandations justifiées dans l'ADR (ou un registre de dette en annexe si aucune décision).

> Si OpenSpec activé : cette phase se matérialise par une **proposition OpenSpec** créée par Fabien, qui notifie Sylvain à `in_review`.

## Gate / sortie
Conception + ADR validés. Frontière **Inception → Construction** : gate `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin` + sensors `required-sections` / `upstream-coverage` / `diagram-validity`.
