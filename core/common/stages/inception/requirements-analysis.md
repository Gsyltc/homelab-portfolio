---
slug: requirements-analysis
phase: inception
execution: ALWAYS
condition: "Always executes — profondeur adaptative"
lead_agent: Architecte de solution
support_agents: [Architecte AWS, Architecte Azure, Architecte Cybersécurité]
mode: subagent
summary_confirmation: required
reviewer: Reviewer de cohérence
review_class: advisory
review_artifact: besoins.md
human_gate: none
produces: [besoins_traces]
consumes: [{artifact: cadrage_confirme, required: true}, {artifact: synthese_contexte_existant, required: false}]
requires_stage: [intake-framing]
sensors: [upstream-coverage]
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Cadrage confirmé + contexte existant éventuel"
outputs: "Besoins fonctionnels et non fonctionnels tracés (profondeur selon Depth), classés MoSCoW et porteurs d'identifiants stables BA-…"
---

# Analyse des besoins (profondeur adaptative)

## Objectif

Recueillir les besoins au niveau de détail dicté par l'axe Depth.

## Steps

### Step 1 — Profondeur adaptative

- **Minimale** : demande simple et claire — documenter l'analyse d'intention.
- **Standard** : besoins fonctionnels et non fonctionnels (performance, sécurité, scalabilité, portabilité, maintenabilité).
- **Complète** : haut risque — besoins détaillés avec traçabilité.

### Step 1b — Priorisation MoSCoW et identifiants stables des besoins d'affaires

Chaque **besoin d'affaires** retenu porte :

- un **identifiant stable** `BA-…` (repris tel quel en aval — exigences, specs, ADR, livrables ; convention des identifiants amont du sensor [`../../../sensors/sensors/traceability.md`](../../../sensors/sensors/traceability.md)) ;
- une **priorité MoSCoW** explicite : `Must` / `Should` / `Could` / `Won't`.

Cette classification est la **source amont** de la traçabilité **spec ↔ besoin d'affaires ↔ exigence** :

- lorsqu'une **méthodologie OpenSpec est active** (verdict d'[`intake-framing`](intake-framing.md), Step 3), les besoins et leur priorité MoSCoW alimentent la **matrice de traçabilité MoSCoW** du `proposal.md` (skill `openspec-proposal-creation`, Step 6b) : chaque scénario / cas d'utilisation d'une spec renvoie à son besoin `BA-…` et à sa priorité ;
- la **matrice de traçabilité MoSCoW** est l'**élément récapitulatif** qui alimente l'élément **Besoins (MoSCoW)** de la checklist d'architecture ([`../../protocols/architecture-checklist.md`](../../protocols/architecture-checklist.md)).

**Ne jamais deviner** : si la priorité MoSCoW d'un besoin n'est pas claire, la **demander à l'humain** au gate granulaire d'Inception plutôt que de l'inventer. La priorité MoSCoW (priorité de livraison) est **distincte** du mot-clé EARS `SHALL`/`SHOULD`/`MAY` (caractère contraignant de la formulation) porté par l'exigence.

### Step 2 — Renforcement sécurité conditionnel

`security-patch` → couvrir a minima l'**analyse d'impact du correctif** (surface, effets de bord, non-régression). `enterprise` → **classification des données** + point de contrôle « applicabilité des normes ». Voir [`../../protocols/governance-security.md`](../../protocols/governance-security.md).

### Step 3 — Revue de cohérence (advisory)

Le coordinateur sollicite le **Reviewer de cohérence** (mention A2A, UUID résolu) à réception des besoins tracés ; verdict **consultatif** (complétude, cohérence avec le cadrage, conventions), demande de correction éventuelle avant le gate humain.

## Sensors

Outputs: besoins retenus documentés sur l'issue, **classés MoSCoW** et porteurs d'**identifiants stables `BA-…`** (source amont de la traçabilité spec ↔ besoin ↔ exigence).
Imports: `upstream-coverage`.
Upstream targets: `cadrage_confirme` (required), `synthese_contexte_existant` (optionnel) — couverture amont vérifiée à l'écriture des besoins.
Review artifact: `besoins.md` porte la section `## Review` ajoutée par le Reviewer de cohérence.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de besoins, seuils de profondeur, renforcements sécurité récurrents) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
