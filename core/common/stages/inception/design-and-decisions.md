---
slug: design-and-decisions
phase: inception
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecte de solution
support_agents: [Architecte de données, Architecte AWS, Infrastructure Windows, OpenSpec Expert]
mode: mob
summary_confirmation: required
reviewer: Reviewer de sécurité
review_class: adversarial
review_artifact: decisions/<NNNN>-<titre>.md
human_gate: granular
produces: [decision_conception, diagramme_principal, conception_cible_validee]
consumes: [{artifact: besoins_traces, required: true}, {artifact: decoupage_livrables, required: true}]
requires_stage: [deliverables-breakdown]
sensors: [required-sections, upstream-coverage, diagram-validity, data-lifecycle]
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

> **Branche git dédiée par ADR (projet Git).** Chaque ADR est **portée par sa propre branche git dédiée**, nommée **`<adr>/<nom de l'adr>`** — préfixe littéral `adr/` suivi du nom de l'ADR en kebab-case (ex. `adr/0039-choix-base-de-donnees`). La branche est créée **avant d'écrire ou de modifier** le document `decisions/<NNNN>-<titre>.md`, et son nom est consigné sur l'issue (piste d'audit). Elle **complète** la branche d'issue `feature/<id-issue>-<slug-court>` du stage [`../initialization/git-detection.md`](../initialization/git-detection.md) : une issue qui produit **plusieurs** ADR ouvre **une branche `adr/<nom>` par ADR**. Comme tout travail git du workflow, **aucun commit / push / PR sans accord explicite de l'humain**. Hors projet Git (`Git: Non`), cette règle est sans objet.

> **Données** : le lead (Architecte de solution) **délègue à l'Architecte de données** les tâches relatives aux données au besoin. L'Architecte de données produit le document **Cycle de vie des données** (`documentation/10-cycle_vie_donnees.md`) — cycle de vie, gouvernance, classification, renseigné selon les données du projet — puis le remet à l'Architecte de solution. L'**Architecte de solution valide** ce livrable ; le sensor `data-lifecycle` (advisory) **assiste** cette validation en factualisant la présence et le renseignement du document, mais **ne la bloque pas** — l'Architecte de solution reste seul juge et peut demander une correction sur la base d'un écart.

### Step 2 — Contrôle sécurité obligatoire (revue adversariale)

À chaque modification d'architecture, le coordinateur sollicite le **Reviewer de sécurité**, **attend son analyse** (OWASP / STRIDE), intègre ses recommandations avant toute validation. Revue **adversariale, non substituable** (plancher SG-3). Normes spécifiques uniquement si explicitement demandées. Voir [`../../protocols/reviewer.md`](../../protocols/reviewer.md).

### Step 3 — Contrôle de cohérence

Vérifier la correspondance documentation ↔ décisions structurantes, l'absence de conflits ; demander les corrections aux agents responsables.

### Step 4 — Validation granulaire humaine

Présenter **chaque choix séparément** (choix, justification, alternative) ; boucle Keep / Modify / Redo. Ne pas avancer sur un élément non validé.

### Step 5 — Analyse de dette technique (Architecte de solution)

Évaluer le potentiel de réduction de dette et consigner des recommandations justifiées avec la décision (ou un registre de dette en annexe si aucune décision).

> Si OpenSpec activé : cette phase se matérialise par une **proposition OpenSpec** créée par l'OpenSpec Expert, qui notifie le coordinateur à `in_review`.

### Reflet du cycle de vie de l'ADR sur le statut d'issue (contexte Multica uniquement)

> **Source unique.** Cette correspondance ADR → statut d'issue est **spécifique à Multica** (elle s'appuie sur le statut d'issue comme machine à états du run et sur le statut personnalisé `ADR Proposée`). Elle fait **autorité ici** et n'est **pas dupliquée** ailleurs : les autres fichiers du workflow s'y réfèrent. **Hors contexte Multica, cette étape est sautée** (aucun statut d'issue à refléter) — le cycle de vie de l'ADR reste porté par le seul champ `## Status` du document de décision.

Lorsqu'une **décision structurante (ADR)** est traitée **sous Multica**, le statut de l'issue qui la porte **reflète le cycle de vie de l'ADR** (champ `## Status` du document `decisions/<NNNN>-<titre>.md`). L'agent qui fait évoluer le champ `## Status` de l'ADR **met à jour le statut de l'issue dans le même temps** (`multica issue status <id> <statut>`), de sorte que le tableau montre l'ADR là où elle en est :

| Statut de l'ADR (`## Status`) | Statut de l'issue Multica | Catégorie | Déclencheur |
| --- | --- | --- | --- |
| `Proposed` (Proposée) | **`ADR Proposée`** (`adr_propos_e`) | `in_progress` | L'ADR est posée en proposition et **nécessite une décision humaine** : déplacer l'issue dans `ADR Proposée`. |
| — (en cours de traitement par un agent) | **`in_progress`** | `in_progress` | Un agent **traite l'ADR** (production / révision / instruction de la décision) : déplacer l'issue dans `in_progress`. |
| `Accepted` (Acceptée) | **`in_review`** | `in_review` | L'ADR est acceptée et le livrable attend la revue / l'acceptation : déplacer l'issue dans `in_review`. |

**Règles d'application** :

- Cette correspondance **ne remplace jamais** la validation humaine granulaire ni le contrôle sécurité : passer en `ADR Proposée` **signale** qu'une décision humaine est attendue, sans l'anticiper (le statut `ADR Proposée` relève de la catégorie `in_progress` — l'acceptation reste un acte humain, jamais écrit automatiquement). L'écriture du champ `## Status` à `Accepted` suit l'arbitrage humain de l'étape 4 (Keep / Modify / Redo) et seulement lui.
- Le passage à `in_review` est **cohérent avec le retour A2A** : l'agent délégataire qui remet le livrable passe déjà l'issue en `in_review` (voir la « Checklist de sortie de stage » de [`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md)). Pour une issue portant une ADR, `in_review` correspond donc à l'ADR `Accepted` remise pour acceptation.
- Les **autres invariants restent intacts** : décision structurante tracée dans `decisions/`, piste d'audit sur l'issue, mention humaine obligatoire sur blocage — voir [`../../protocols/governance-security.md`](../../protocols/governance-security.md).

## Sensors

Outputs: conception + décisions validées. Frontière **Inception → Construction** : gate `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin`.
Imports: `required-sections`, `upstream-coverage`, `diagram-validity`, `data-lifecycle`.
Upstream targets: `besoins_traces` (required), `decoupage_livrables` (required) — couverture amont vérifiée à l'écriture de la décision / conception.
Données : `data-lifecycle` vérifie `documentation/10-cycle_vie_donnees.md` (présent + renseigné selon les données du projet). **Advisory pour tous** : il **assiste** la revue **Architecte de solution → Architecte de données** et **alerte** le coordinateur au verification gate, **sans jamais bloquer** ni la validation de l'Architecte de solution ni le gate humain.
Review artifact: la **décision structurante** (`decisions/<NNNN>-<titre>.md`) porte la section `## Review` ajoutée par le Reviewer de sécurité.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de conception, arbitrages récurrents, recommandations de sécurité) ; les remonter au **gate humain granulaire** ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit (toute règle `workspace` repasse au contrôle sécurité).
