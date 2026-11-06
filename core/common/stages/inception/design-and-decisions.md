---
slug: design-and-decisions
phase: inception
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecte de solution
support_agents: [Architecte de données, Architecte AWS, Architecte Azure, Infrastructure Windows, OpenSpec Expert]
mode: mob
summary_confirmation: required
reviewer: Reviewer de sécurité
review_class: adversarial
review_artifact: decisions/<NNNN>-<titre>.md
human_gate: granular
produces: [decision_conception, diagramme_principal, conception_cible_validee]
consumes: [{artifact: besoins_traces, required: true}, {artifact: decoupage_livrables, required: true}, {artifact: verdict_impact_structurant, required: true}, {artifact: verdict_methodologie, required: false}]
requires_stage: [deliverables-breakdown]
sensors: [required-sections, upstream-coverage, diagram-validity, data-lifecycle, claim-sources]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Besoins tracés + découpage en livrables"
outputs: "Conception cible + décisions structurantes validées granulairement par l'humain, après contrôle sécurité"
---

# Conception d'architecture, décisions structurantes et contrôle sécurité

## Objectif

Produire la conception cible et les décisions structurantes, contrôlées en sécurité et validées granulairement.

> **Style du livrable.** Tout document produit par ce stage suit le style concis (information strictement nécessaire, puces multi-niveaux, texte aéré ; tableaux des gabarits conservés) — source unique [`document-style`](../../protocols/document-style.md) (règle `RULE-WS-007`).

> **ADR obligatoire sur impact structurant (non contournable).**
> - Verdict d'impact structurant = **`Oui`** ([`intake-framing`](intake-framing.md), Step 5) ⇒ l'**issue ADR existe déjà** : créée au découpage ([`deliverables-breakdown`](deliverables-breakdown.md), Step 3), **avant** tout livrable, comme **issue parente** de la décision.
> - Si OpenSpec est activé : la phase OpenSpec préalable (OpenSpec Expert) et sa gate légère d'intention (`human_gate: light`) ont eu lieu **en amont** de l'ADR ([`deliverables-breakdown`](deliverables-breakdown.md), Step 3.0). Ce stage ne les conduit pas ; la gate légère ne remplace jamais la gate granulaire de l'ADR (Step 4).
> - Ce stage conduit l'issue ADR : production mob → revues → `ADR Proposée` → décision humaine granulaire.
> - L'orchestration des issues (blocage de l'origine, gate, sous-issues de livrable, clôture) appartient à [`deliverables-breakdown`](deliverables-breakdown.md).
> - Garde-fou ([`conductor`](../../conductor.md), [`governance-security`](../../protocols/governance-security.md)) : pas d'impact structurant sans ADR ; OpenSpec toujours en amont de l'ADR. Verdict `Oui` sans issue ADR ⇒ **halt-and-ask** du coordinateur.

## Steps

### Step 1 — Production de la conception (mob)

Les `support_agents` travaillent **en parallèle contre le brouillon du lead** (Architecte de solution), en une ronde d'objection bornée (`mode: mob`) : vues fonctionnelle / technique, choix, alternatives, risques.

Chaque décision structurante est **tracée** dans `decisions/`.

> **Données**
> - Le lead délègue au besoin les tâches données à l'Architecte de données.
> - L'Architecte de données produit le document **Cycle de vie des données** (`documentation/10-cycle_vie_donnees.md`) : cycle de vie, gouvernance, classification, selon les données du projet.
> - L'Architecte de solution **valide** ce livrable ; il est seul juge et peut exiger une correction.
> - Le sensor `data-lifecycle` (advisory) factualise la présence et le renseignement du document, sans jamais bloquer.

### Step 2 — Revues (cohérence puis sécurité)

Les deux revues sont **séquentielles** (cohérence puis sécurité) et transitent par le lead, auteur de l'ADR.

Mécanique OK / RENVOI : [`reviewer`](../../protocols/reviewer.md) (encadré « Le reviewer retourne toujours au spécialiste ») et [`stage-protocol`](../../protocols/stage-protocol.md) (« Cycle de livrable d'un spécialiste »).

Communs aux deux revues :

- **Où** : issue portant l'artefact revu — issue du livrable (modification documentaire standard) ou issue ADR dédiée (impact structurant) ; **jamais** l'issue d'origine ([`reviewer`](../../protocols/reviewer.md), encadré d'ouverture).
- **Qui** :
  - Tout spécialiste ou architecte peut solliciter le reviewer par mention A2A, pas seulement le coordinateur.
  - Le reviewer analyse et **poste lui-même** son verdict.
  - L'auteur de l'artefact n'est jamais son relecteur ([`reviewer`](../../protocols/reviewer.md), « Qui peut solliciter une revue » et « Séparation des rôles »).
- **Conduite** :
  - Intégrer les recommandations **avant** la validation humaine.
  - Revue requise manquante ⇒ la solliciter auprès du reviewer ; l'auteur ne la supplée jamais.

#### Step 2.1 — Revue de cohérence

Le Reviewer de cohérence vérifie la correspondance documentation ↔ décisions structurantes, l'absence de conflits et d'artefact orphelin.

#### Step 2.2 — Revue de sécurité (obligatoire, non substituable)

- Déclenchée à **chaque modification d'architecture**.
- Le Reviewer de sécurité analyse les risques (OWASP / STRIDE ; autres normes uniquement si explicitement demandées).
- Revue **adversariale**, plancher SG-3 : aucun autre contrôle ne peut la porter, la remplacer ni la court-circuiter.

### Step 3 — Analyse de dette technique (Architecte de solution)

Évaluer le potentiel de réduction de dette et consigner des recommandations justifiées avec la décision (ou un registre de dette en annexe si aucune décision).

> Si OpenSpec est activé : cette phase prend la forme d'une **proposition OpenSpec** créée par l'OpenSpec Expert, qui notifie le coordinateur à `in_review`.

### Step 4 — Validation granulaire humaine

Présenter **chaque choix séparément** (choix, justification, alternative) ; boucle Keep / Modify / Redo. Ne pas avancer sur un élément non validé.

## Flux ADR — impact structurant = Oui

L'orchestration d'ensemble appartient à [`deliverables-breakdown`](deliverables-breakdown.md) (Step 3) et n'est pas redécrite ici.

Ce stage conduit, sur l'**issue ADR** :

- **Production** (Step 1 — mob) par le lead ; issue en `in_progress`.
- **Revues** de cohérence puis de sécurité (Step 2), postées sur l'issue ADR ; issue en `in_review`.
  - Chaque reviewer retourne son verdict au **lead** (OK comme RENVOI), jamais à l'autre reviewer ni au coordinateur ([`reviewer`](../../protocols/reviewer.md)).
  - Sur **RENVOI** : le lead corrige, re-sollicite le même reviewer ; issue en `in_progress`.
- **Proposition** : après la revue de sécurité et sous le garde-fou de séparation des rôles, passage en `ADR Proposée`, puis gate humaine (section suivante et [`deliverables-breakdown`](deliverables-breakdown.md)).

### Reflet du cycle de vie de l'ADR sur le statut d'issue (contexte Multica uniquement)

> **Source unique, spécifique à Multica.**
> - Cette correspondance s'appuie sur le statut d'issue comme machine à états du run et sur le statut personnalisé `ADR Proposée`.
> - Elle fait **autorité ici** ; les autres fichiers du workflow s'y réfèrent sans la dupliquer.
> - **Hors Multica, cette étape est sautée** : le cycle de vie reste porté par le seul champ `## Status` du document de décision.

Sous Multica, le statut de l'issue ADR **reflète la phase du flux**. L'agent qui fait évoluer l'ADR met à jour le statut dans le même temps (`multica issue status <id> <statut>`).

| Phase du flux | `## Status` de l'ADR | Statut de l'issue | Déclencheur |
| --- | --- | --- | --- |
| Production (mob) | `Proposed` | `in_progress` | Le lead et les `support_agents` produisent ou corrigent l'ADR. |
| Revues (cohérence puis sécurité) | `Proposed` | `in_review` | L'ADR est remise aux reviewers. |
| Proposée à l'humain | `Proposed` | `ADR Proposée` (`adr_propos_e`, catégorie `in_progress`) | Revue de sécurité intégrée ; décision humaine attendue. |
| Acceptation (Keep) | `Accepted` | `blocked` (parente) | Le coordinateur crée et lance les sous-issues de livrable, puis passe l'ADR en `blocked`. Elle reste ouverte jusqu'à la fin des sous-issues. |
| Rejet | `Rejected` | `cancelled` + issue d'origine `cancelled` (cascade) | Aucun livrable créé. Si OpenSpec était activé : specs préalables archivées (change → `openspec/changes/archive/`, sans fusion des deltas ; [`deliverables-breakdown`](deliverables-breakdown.md), Step 3.2). |
| Tous les livrables terminés | `Accepted` | `ADR Acceptée` (`adr_accept_e`, catégorie `done`), puis issue d'origine `done` | Quand toutes les sous-issues sont `done` : (1) livrables validés acheminés vers [`delivery-handoff`](../construction/delivery-handoff.md) (gate « commit + PR oui/non ? », mise à disposition, notification ; [`deliverables-breakdown`](deliverables-breakdown.md), Step 3.4) ; (2) ADR → `ADR Acceptée` ; (3) issue d'origine débloquée → `done`. Aucun acte humain au-delà du gate PR. |

**Règles d'application**

- **Séparation des rôles au passage en `ADR Proposée` (non contournable)** :
  - Le coordinateur ne pose `ADR Proposée` (ni ne ferme la boucle A2A) que si l'issue ADR porte **deux commentaires de revue distincts** : cohérence, postée par le Reviewer de cohérence ; sécurité, postée par le Reviewer de sécurité.
  - Aucun des deux n'est rédigé par le lead, auteur de l'ADR.
  - Revue du lead, ou intégrée seulement dans `## Review` de l'ADR sans commentaire indépendant du reviewer ⇒ condition non satisfaite : **halt-and-ask** et sollicitation du reviewer manquant.
  - Ce garde-fou complète le plancher SG-3, sans le remplacer.
- **Décision humaine** :
  - `ADR Proposée` **signale** qu'une décision est attendue, sans l'anticiper ; l'acceptation reste un acte humain.
  - `## Status` passe à `Accepted` ou `Rejected` uniquement après l'arbitrage humain de l'étape 4 (Keep / Modify / Redo).
  - L'acceptation ne passe **jamais** l'issue ADR à `done` : `ADR Acceptée` est dérivé (tous les livrables `done`) ; `cancelled` suit un rejet.
- **Boucles de correction** (revue de cohérence, Redo / Modify, recommandations de sécurité) : l'issue repasse en `in_progress`.
- **Filiation** : l'issue ADR est parente des sous-issues de livrable ([`deliverables-breakdown`](deliverables-breakdown.md), Step 3) et enfant de l'issue d'origine, bloquée dès la création de l'ADR (Step 3.1). Les issues de la gate sont décrites dans le tableau.
- **Invariants intacts** : décision tracée dans `decisions/`, piste d'audit sur l'issue, mention humaine obligatoire sur blocage ([`governance-security`](../../protocols/governance-security.md)).

## Sensors

- **Outputs** : conception + décisions validées.
- **Gate Inception → Construction** : `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin`.
- **Imports** : `required-sections`, `upstream-coverage`, `diagram-validity`, `data-lifecycle`, `claim-sources`.
- **Upstream targets** : `besoins_traces` (required), `decoupage_livrables` (required) — couverture amont vérifiée à l'écriture de la décision / conception.
- **Données** : `data-lifecycle` vérifie `documentation/10-cycle_vie_donnees.md` (présent + renseigné). Advisory pour tous : il assiste la revue Architecte de solution → Architecte de données et alerte le coordinateur au verification gate, sans jamais bloquer.
- **Review artifact** : la décision structurante (`decisions/<NNNN>-<titre>.md`) porte la section `## Review` ajoutée par le Reviewer de sécurité.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) :

- Tracer sur l'issue les candidats-règles (motifs de conception, arbitrages récurrents, recommandations de sécurité).
- Les remonter au **gate humain granulaire**.
- Persister les apprentissages **confirmés** dans `core/rules/` : capture → confirmation humaine → contrôle de conflit (toute règle `workspace` repasse au contrôle sécurité).
