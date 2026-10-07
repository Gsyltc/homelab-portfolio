---
slug: detailed-deliverables
phase: construction
execution: ALWAYS
condition: "Always executes — rythme selon le mode d'exécution choisi"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Infrastructure Windows, OpenSpec Expert, Architecte Cybersécurité]
mode: mob
for_each: unit-of-work
summary_confirmation: required
reviewer: Reviewer de cohérence
review_class: advisory
review_artifact: livrable-<unite>.md
human_gate: granular
produces: [livrables_detailles]
consumes: [{artifact: walking_skeleton_valide, required: true}, {artifact: mode_execution_choisi, required: true}]
requires_stage: [walking-skeleton]
sensors: [required-sections, upstream-coverage, diagram-validity]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Walking skeleton validé + mode d'exécution"
outputs: "Livrables détaillés (documentation, diagrammes définitifs, coûts AWS, config infra, ou implémentation OpenSpec)"
---

# Production des livrables détaillés

## Objectif

Produire les livrables du lot cadré, au rythme fixé par le mode d'exécution — **une exécution par unité de travail** (`for_each: unit-of-work`).

## Steps

### Step 1 — Produire par livrable / agent (une fois par unité)

Le stage s'exécute **une fois par unité de travail** (`for_each: unit-of-work`). Chaque agent exécute son livrable (les `support_agents` travaillent en `mob` contre le brouillon du lead) ; en fin de travail, mentionne le coordinateur pour vérification. Documenter sur l'issue. L'agrégation des unités se déduit du graphe.

### Step 1.1 — Impact sécurité → sous-tâche dédiée à l'Architecte Cybersécurité

**Déclencheur.** Dès qu'un livrable **a un impact sur la sécurité** — surface de sécurité, contrôle, posture, classification de données, frontière de délégation ou instruction exécutable — même émergé en cours de production, une **sous-tâche de sécurité dédiée** est créée. C'est le pendant Construction de la délégation « Sécurité » du découpage ([`../inception/deliverables-breakdown.md`](../inception/deliverables-breakdown.md), Step 2 — **source unique** du rattachement, de la règle « une sous-issue par agent » et du contenu obligatoire de la mission).

**Qui signale, qui crée.** Le **lead de production (Architecte de solution) signale** l'impact ; il ne crée ni ne passe aucun statut. Le **coordinateur (Architecture Solution & Intégration)** crée la sous-tâche en **enfant de l'issue du livrable** et l'**assigne à l'Architecte Cybersécurité** (`--assignee-id`, UUID résolu via `multica agent list --output json`), avec mission cadrée et agent de retour en texte clair.

**Objet.** L'Architecte Cybersécurité mène l'**analyse de sécurité** (OWASP / STRIDE toujours actifs ; normes spécifiques sur demande explicite seulement) **et met à jour la documentation d'architecture de sécurité** (`documentation/architecture-securite/`, format des gabarits `architecture-solution-gabarits`) — la mise à jour de la DAS est un **livrable attendu**, pas un sous-produit de l'analyse.

**Chemin de contrôle.** La sous-tâche suit le **cycle de livrable à 3 stages** ([`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md)) : **revue du Reviewer de sécurité** (plancher SG-3, non substituable), retour à l'auteur, puis **gate humaine granulaire**. Invariants non redupliqués — voir [`governance-security.md`](../../protocols/governance-security.md), [`reviewer.md`](../../protocols/reviewer.md) et [`security-consistency-check.md`](security-consistency-check.md).

**Cas sans impact.** Aucun impact sécurité ⇒ aucune sous-tâche ; le lead de production **trace le constat sur l'issue** (choix documenté, non un oubli).

### Step 2 — Rythme de validation

- **Gated** *(défaut)* : chaque livrable validé granulairement avant de poursuivre.
- **Autonome** : livrables du même lot enchaînés ; validation granulaire **regroupée** en un point de synchronisation (l'humain valide en bloc, **toujours choix par choix**).

### Step 3 — Revue de cohérence (advisory)

À réception de chaque livrable, le coordinateur sollicite le **Reviewer de cohérence** (verdict consultatif : complétude, cohérence documentation ↔ décisions, conventions) avant le gate humain.

### Step 4 — Halt-and-ask systématique sur échec

S'arrêter et interroger l'humain sur : échec / impossibilité d'un livrable ; écart ou contrôle de sécurité requis ; gate / sensor en écart ou `⛔ indisponible` ; décision structurante nouvelle non cadrée ; action à impact / destructive (jamais autonome). L'autonomie ne court-circuite jamais le contrôle sécurité ni les actions à impact.

## Sensors

Outputs: livrables détaillés (une fois par unité).
Imports: `required-sections`, `upstream-coverage`, `diagram-validity`.
Upstream targets: `walking_skeleton_valide` (required), `mode_execution_choisi` (required) — couverture amont vérifiée à l'écriture de chaque livrable.
Review artifact: chaque `livrable-<unite>.md` porte la section `## Review` ajoutée par le Reviewer de cohérence.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de production, corrections récurrentes par type de livrable) ; les remonter au **gate humain granulaire** (regroupé en mode autonome, jamais fusionné) ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
