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
consumes: [{artifact: besoins_traces, required: true}, {artifact: decoupage_livrables, required: true}, {artifact: verdict_impact_structurant, required: true}, {artifact: verdict_methodologie, required: false}]
requires_stage: [deliverables-breakdown]
sensors: [required-sections, upstream-coverage, diagram-validity, data-lifecycle]
scopes: [standard, feature, infra, security-patch, mvp, enterprise]
inputs: "Besoins tracés + découpage en livrables"
outputs: "Conception cible + décisions structurantes validées granulairement par l'humain, après contrôle sécurité"
---

# Conception d'architecture, décisions structurantes et contrôle sécurité

## Objectif

Produire la conception cible et les décisions structurantes, contrôlées en sécurité et validées granulairement.

> **ADR obligatoire sur impact structurant (non contournable).** Lorsque le verdict d'impact structurant ([`intake-framing`](intake-framing.md), Step 5) vaut **`Oui`**, l'**issue ADR a été créée en premier**, comme **issue parente** de la décision, au découpage ([`deliverables-breakdown`](deliverables-breakdown.md), Step 3) — **avant** tout livrable. Ce stage **conduit cette ou ces issues ADR** (production mob → revues → `ADR Proposée` → décision humaine granulaire) ; l'orchestration des issues (blocage de l'origine, gate, sous-issues de livrable après acceptation, clôture dérivée) est détaillée dans [`deliverables-breakdown`](deliverables-breakdown.md) et n'est pas redite ici. Garde-fou non contournable (voir [`../../conductor.md`](../../conductor.md) et [`../../protocols/governance-security.md`](../../protocols/governance-security.md)) : un impact structurant **ne peut jamais être traité sans ADR**. Si le verdict vaut `Oui` sans issue ADR, le coordinateur est en **halt-and-ask**.

## Steps

### Step 1 — Production de la conception (mob)

Les `support_agents` désignés travaillent **en parallèle contre le brouillon du lead** (Architecte de solution), en une ronde d'objection bornée (`mode: mob`) : vues fonctionnelle / technique, choix, alternatives, risques. Chaque décision structurante est **tracée** dans le registre de décisions du projet (`decisions/`).

> **Branche git dédiée par ADR (projet Git).** Chaque ADR est **portée par sa propre branche git dédiée**, nommée **`<adr>/<nom de l'adr>`** — préfixe littéral `adr/` suivi du nom de l'ADR en kebab-case (ex. `adr/0039-choix-base-de-donnees`). La branche est créée **avant d'écrire ou de modifier** le document `decisions/<NNNN>-<titre>.md`, et son nom est consigné sur l'issue (piste d'audit). Elle **complète** la branche d'issue `feature/<id-issue>-<slug-court>` du stage [`../initialization/git-detection.md`](../initialization/git-detection.md) : une issue qui produit **plusieurs** ADR ouvre **une branche `adr/<nom>` par ADR**. Comme tout travail git du workflow, **aucun commit / push / PR sans accord explicite de l'humain**. Hors projet Git (`Git: Non`), cette règle est sans objet.

> **Données** : le lead (Architecte de solution) **délègue à l'Architecte de données** les tâches relatives aux données au besoin. L'Architecte de données produit le document **Cycle de vie des données** (`documentation/10-cycle_vie_donnees.md`) — cycle de vie, gouvernance, classification, renseigné selon les données du projet — puis le remet à l'Architecte de solution. L'**Architecte de solution valide** ce livrable ; le sensor `data-lifecycle` (advisory) **assiste** cette validation en factualisant la présence et le renseignement du document, mais **ne la bloque pas** — l'Architecte de solution reste seul juge et peut demander une correction sur la base d'un écart.

### Step 2 — Revues (cohérence puis sécurité)

Les deux revues sont **séquentielles** (**cohérence puis sécurité**) et transitent par le spécialiste — ici le lead Architecte de solution, auteur de l'ADR (mécanique OK/RENVOI et enchaînement : [`../../protocols/reviewer.md`](../../protocols/reviewer.md), encadré « Le reviewer retourne toujours au spécialiste », et [`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md), « Cycle de livrable d'un spécialiste »).

Communs aux deux revues :

- **Où** : sur l'issue qui porte l'artefact revu — **issue du livrable** pour une modification documentaire standard, **issue ADR dédiée** sur impact structurant, **jamais** l'issue d'origine (détail et faute de flux : [`../../protocols/reviewer.md`](../../protocols/reviewer.md), encadré d'ouverture).
- **Qui** : **tout spécialiste ou architecte** peut solliciter le reviewer dédié par mention A2A — pas seulement le coordinateur ; le reviewer **analyse et poste lui-même** son verdict. L'**auteur de l'artefact n'est jamais son relecteur** (source unique : [`../../protocols/reviewer.md`](../../protocols/reviewer.md), encadrés « Qui peut solliciter une revue » et « Séparation des rôles »).
- **Conduite** : attendre l'analyse, intégrer les recommandations **avant** la validation humaine ; si une revue requise manque, elle est **sollicitée auprès du reviewer** — l'auteur ne la supplée jamais. Voir [`../../protocols/reviewer.md`](../../protocols/reviewer.md).

#### Step 2.1 — Revue de cohérence

`consistency-reviewer-agent` vérifie la correspondance documentation ↔ décisions structurantes, l'absence de conflits et d'artefact orphelin.

#### Step 2.2 — Revue de sécurité (obligatoire, non substituable)

Déclenchée à **chaque modification d'architecture**. `security-reviewer-agent` analyse les risques (OWASP / STRIDE ; normes spécifiques uniquement si explicitement demandées). Revue **adversariale, plancher SG-3** : aucun autre contrôle ne peut la porter, la remplacer ni la court-circuiter.

### Step 3 — Analyse de dette technique (Architecte de solution)

Évaluer le potentiel de réduction de dette et consigner des recommandations justifiées avec la décision (ou un registre de dette en annexe si aucune décision).

> Si OpenSpec activé : cette phase se matérialise par une **proposition OpenSpec** créée par l'OpenSpec Expert, qui notifie le coordinateur à `in_review`.

### Step 4 — Validation granulaire humaine

Présenter **chaque choix séparément** (choix, justification, alternative) ; boucle Keep / Modify / Redo. Ne pas avancer sur un élément non validé.

## Flux ADR — impact structurant = Oui

Sur **impact structurant**, l'orchestration d'ensemble (création de l'issue ADR parente, blocage de l'issue d'origine, gate humaine accept/refus, création des sous-issues de livrable, clôture dérivée) est **la propriété de [`deliverables-breakdown`](deliverables-breakdown.md) (Step 3)** et n'est pas redécrite ici. Ce stage conduit la **partie qui lui est propre** — la production puis les **deux revues de l'ADR**, sur l'**issue ADR** :

- **Production** (Step 1 — mob) par le lead Architecte de solution ; issue en `in_progress`.
- **Revue de cohérence** puis **revue de sécurité** (Step 2), postées **sur l'issue ADR** ; issue en `in_review`. Chaque reviewer retourne son verdict au **lead de l'issue ADR** (OK comme RENVOI) — jamais entre eux ni au coordinateur ([`../../protocols/reviewer.md`](../../protocols/reviewer.md)). Sur **RENVOI**, le lead corrige puis re-sollicite le même reviewer ; l'issue repasse en `in_progress`.
- Après la revue de sécurité et sous le garde-fou de séparation des rôles, le passage en **`ADR Proposée`** puis la **gate humaine** sont conduits selon le cycle de vie ci-dessous et [`deliverables-breakdown`](deliverables-breakdown.md).

Le reflet de ces phases sur le statut d'issue est détaillé dans la section suivante.

### Reflet du cycle de vie de l'ADR sur le statut d'issue (contexte Multica uniquement)

> **Source unique.** Cette correspondance ADR → statut d'issue est **spécifique à Multica** (elle s'appuie sur le statut d'issue comme machine à états du run et sur le statut personnalisé `ADR Proposée`). Elle fait **autorité ici** et n'est **pas dupliquée** ailleurs : les autres fichiers du workflow s'y réfèrent. **Hors contexte Multica, cette étape est sautée** (aucun statut d'issue à refléter) — le cycle de vie de l'ADR reste porté par le seul champ `## Status` du document de décision.

Lorsqu'une **décision structurante (ADR)** est traitée **sous Multica**, le statut de l'issue qui la porte **reflète la phase du flux** (production → revues → proposition → décision humaine). L'agent qui fait évoluer l'ADR **met à jour le statut de l'issue dans le même temps** (`multica issue status <id> <statut>`), de sorte que le tableau montre l'ADR là où elle en est :

| Phase du flux | Statut de l'ADR (`## Status`) | Statut de l'issue Multica | Catégorie | Déclencheur |
| --- | --- | --- | --- | --- |
| Production de la conception (mob) | `Proposed` (en cours de rédaction) | **`in_progress`** | `in_progress` | Le lead et les support_agents produisent / corrigent l'ADR : issue en `in_progress`. |
| Revues des agents (cohérence puis sécurité) | `Proposed` | **`in_review`** | `in_review` | L'ADR est remise aux revues (Reviewer de cohérence, puis Reviewer de sécurité) : issue en `in_review`. |
| ADR proposée à l'humain (après revue de sécurité) | `Proposed` | **`ADR Proposée`** (`adr_propos_e`) | `in_progress` | La revue de sécurité est intégrée ; l'ADR est posée en proposition et **nécessite une décision humaine** : issue en `ADR Proposée`. |
| Acceptation humaine (Keep) | `Accepted` | **`blocked`** (parente) | `in_progress` | L'humain accepte l'ADR au gate granulaire : le coordinateur crée alors les **sous-issues de livrable** (enfants) et les lance, puis passe l'issue ADR en **`blocked`**. L'issue ADR **reste ouverte** comme parente — l'acceptation **ne la passe pas** `done`, et elle ne peut reprendre qu'à la fin de ses sous-issues. |
| Rejet humain | `Rejected` | **`annulé`** (`cancelled`) + **issue d'origine `annulé`** (cascade) | `cancelled` | L'humain rejette l'ADR au gate granulaire : issue ADR en `annulé` ; aucun livrable n'est créé ; **l'issue d'origine qui a déclenché le flux est annulée en cascade** (`cancelled`). |
| Tous les livrables terminés | `Accepted` | **`done`** (ADR) puis **issue d'origine `done`** (cascade dérivée) | `done` | **Clôture dérivée** : quand **toutes** les sous-issues de l'ADR sont `done`, le coordinateur passe l'issue ADR à `done`, ce qui **débloque l'issue d'origine** (passée à `done`) — sans acte humain supplémentaire. |

**Règles d'application** :

- **Garde-fou de séparation des rôles au passage en `ADR Proposée` (non contournable).** Le coordinateur ne pose l'issue en `ADR Proposée` (ni ne ferme la boucle A2A) **que si l'issue ADR porte deux commentaires de revue distincts** — une revue de cohérence **postée par** `consistency-reviewer-agent` et une revue de sécurité **postée par** `security-reviewer-agent` — **dont l'auteur n'est, dans aucun des deux cas, le lead `Architecte de solution` auteur de l'ADR**. Une revue rédigée par le lead, ou intégrée uniquement dans la section `## Review` de l'ADR sans commentaire indépendant du reviewer sur l'issue, **ne satisfait pas** cette condition : le coordinateur est en **halt-and-ask** et sollicite le(s) reviewer(s) manquant(s) avant tout passage de phase. Ce garde-fou **complète** le plancher SG-3 (la revue de sécurité ne peut être ni portée ni remplacée par un autre contrôle) et ne le remplace pas.
- Cette correspondance **ne remplace jamais** la validation humaine granulaire ni le contrôle sécurité : passer en `ADR Proposée` **signale** qu'une décision humaine est attendue, sans l'anticiper (le statut `ADR Proposée` relève de la catégorie `in_progress` — l'acceptation reste un acte humain, jamais écrit automatiquement). L'écriture du champ `## Status` à `Accepted` ou `Rejected` suit l'arbitrage humain de l'étape 4 (Keep / Modify / Redo) et seulement lui. L'**acceptation ne passe pas l'issue ADR à `done`** : elle débloque la création des sous-issues puis passe l'issue ADR en `blocked` ; le passage de l'issue ADR à `done` est **dérivé** (tous les livrables `done`), celui à `annulé` suit un rejet.
- Les boucles de correction (demande de la revue de cohérence, Redo / Modify du gate humain, recommandations de la revue de sécurité à intégrer) **ramènent l'issue en `in_progress`** (retour en production).
- **ADR parente des sous-issues de livrable, elle-même sous-issue de l'issue d'origine.** L'issue ADR est l'**issue parente** des livrables (voir [`deliverables-breakdown`](deliverables-breakdown.md), Step 3) et l'**enfant de l'issue d'origine** qui a déclenché le flux (bloquée dès la création de l'ADR, Step 3.1). L'issue de la gate humaine commande la suite :
  - **Acceptée (Keep)** ⇒ le coordinateur **crée les sous-issues de livrable** (enfants de l'ADR, `backlog`, agent assigné), les **lance**, puis passe l'issue ADR en **`blocked`** ; elle reste bloquée tant que ses sous-issues tournent.
  - **Rejetée** ⇒ issue ADR en **`cancelled`** ; **aucun** livrable n'est créé ; **l'issue d'origine est annulée en cascade** (`cancelled`).
  - **Tous les livrables `done`** ⇒ clôture **dérivée** : l'issue ADR passe à `done`, puis l'**issue d'origine passe à `done`** (déblocage en cascade).
- Les **autres invariants restent intacts** : décision structurante tracée dans `decisions/`, piste d'audit sur l'issue, mention humaine obligatoire sur blocage — voir [`../../protocols/governance-security.md`](../../protocols/governance-security.md).

## Sensors

Outputs: conception + décisions validées. Frontière **Inception → Construction** : gate `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin`.
Imports: `required-sections`, `upstream-coverage`, `diagram-validity`, `data-lifecycle`.
Upstream targets: `besoins_traces` (required), `decoupage_livrables` (required) — couverture amont vérifiée à l'écriture de la décision / conception.
Données : `data-lifecycle` vérifie `documentation/10-cycle_vie_donnees.md` (présent + renseigné selon les données du projet). **Advisory pour tous** : il **assiste** la revue **Architecte de solution → Architecte de données** et **alerte** le coordinateur au verification gate, **sans jamais bloquer** ni la validation de l'Architecte de solution ni le gate humain.
Review artifact: la **décision structurante** (`decisions/<NNNN>-<titre>.md`) porte la section `## Review` ajoutée par le Reviewer de sécurité.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tracer sur l'issue les candidats-règles (motifs de conception, arbitrages récurrents, recommandations de sécurité) ; les remonter au **gate humain granulaire** ; persistance des apprentissages **confirmés** dans `core/rules/` via le cycle capture → confirmation humaine → contrôle de conflit (toute règle `workspace` repasse au contrôle sécurité).
