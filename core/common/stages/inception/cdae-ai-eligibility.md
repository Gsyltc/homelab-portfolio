---
slug: cdae-ai-eligibility
phase: inception
execution: CONDITIONAL
condition: "L'humain demande une évaluation d'éligibilité CDAE-IA (et, le cas échéant, une estimation du crédit)"
lead_agent: Architecte de solution
support_agents: []
mode: inline
summary_confirmation: required
reviewer: Reviewer de cohérence
review_class: advisory
review_artifact: cdae-ai-eligibilite.md
human_gate: granular
produces: [verdict_cdae_ai, estimation_credit_cdae_ai]
consumes: [{artifact: besoins_traces, required: true}]
requires_stage: [requirements-analysis]
sensors: []
scopes: [standard, feature, infra, mvp, enterprise]
inputs: "Demande explicite de l'humain + besoins tracés + informations société/employés fournies"
outputs: "Verdict CDAE-AI (Oui / Non / À déterminer) écrit dans la description du projet selon les règles ; estimation du crédit (si conditions réunies) placée avec les informations financières"
---

# Éligibilité CDAE-IA et estimation du crédit (à la demande)

## Objectif

Évaluer, sur demande de l'humain, l'éligibilité du projet au crédit d'impôt CDAE-IA et, à sa demande explicite, estimer le crédit possible.

## Steps

### Step 1 — Déclenchement à la demande

Ce stage **ne s'exécute que si l'humain le demande** (évaluation d'éligibilité CDAE-IA). Hors demande explicite, il est **sauté** (`N/A`). Charger la skill `cdae-ai-eligibilite` (source unique des conditions et de la méthode de calcul) uniquement à ce moment (chargement différé).

### Step 2 — Analyse d'éligibilité (Oui / Non / À déterminer)

L'Architecte de solution évalue le projet contre les **critères société et employés** définis dans la skill `cdae-ai-eligibilite` (source unique — ne pas les répéter ici) et conclut :

- **Oui** — critères applicables satisfaits.
- **Non** — au moins un critère déterminant non satisfait.
- **À déterminer** — informations manquantes : **lister précisément les éléments manquants et les demander à l'humain**. Ne jamais deviner.

### Step 3 — Écriture du verdict dans la description du projet

- `Oui` et description **sans** information `CDAE-AI: Oui / Non` → **ajouter `CDAE-AI: Oui`**.
- `Non` et description **sans** information `CDAE-AI: Oui / Non` → **ajouter `CDAE-AI: Non`**.
- `À déterminer` → **ne rien écrire** ; demander les informations manquantes.

**Idempotence** : ne jamais écraser une valeur `CDAE-AI` existante sans validation humaine. L'écriture dans la description du projet est une action à impact soumise à la validation humaine granulaire (Step 5).

### Step 4 — Estimation du crédit (conditionnelle)

N'estimer **que si les trois conditions** sont réunies : (1) demande explicite de l'humain pour le calcul, (2) la description porte `CDAE-AI: Oui`, (3) toutes les informations de calcul disponibles. Sinon, **indiquer les éléments manquants** à l'humain.

Appliquer la **méthode de calcul de la skill** `cdae-ai-eligibilite` (taux et proratisation — source unique, ne pas la répéter ici). Consigner l'estimation **avec les informations financières** dans `documentation/05-planification.md`, sous-section « Crédit d'impôt CDAE-IA (estimation) ». Estimation **informative, non contractuelle, sans valeur de conseil fiscal**.

### Step 5 — Validation granulaire humaine

Présenter séparément : le verdict d'éligibilité (et sa justification), l'écriture `CDAE-AI: Oui/Non` dans la description, et, le cas échéant, l'estimation chiffrée. Boucle Keep / Modify / Redo. Ne rien écrire dans la description ni ne figer d'estimation sans validation de l'élément concerné.

## Sensors

Outputs: verdict et (éventuelle) estimation consignés sur l'issue ; écriture `CDAE-AI: Oui/Non` dans la description du projet et estimation dans `documentation/05-planification.md`, après gate humain granulaire.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs d'éligibilité récurrents, informations systématiquement manquantes au calcul) ; les remonter au **gate humain granulaire** d'Inception ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit.
