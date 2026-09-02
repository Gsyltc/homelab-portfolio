# Passage à 5 phases et mode d'autonomie en Construction

---
auteurs: Sylvain G.
accepté par : ""
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

## Contexte

Le workflow `docs/core-workflow.md` était structuré en **3 phases** (Inception / Construction / Operation), présentées comme une réinterprétation d'AI-DLC. L'analyse comparative (issue parente ALI-184, cadrage ALI-185, [ADR-0001](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)) a identifié deux écarts structurels, comblés au Stage 5 (ALI-189) :

- **A — 5 phases** : AI-DLC 2.0 structure le cycle en `Initialization → Ideation → Inception → Construction → Operation`. Manquaient **Initialization** (bootstrap déterministe : vérification du répertoire projet, détection brownfield / greenfield, initialisation de l'état et de la piste d'audit, **sans gate humain**) et **Ideation** (cadrage amont léger : capture d'intention, faisabilité / contraintes, définition de périmètre, maquettes si UI, approbation).
- **G — Mode d'autonomie en Construction** : AI-DLC pose, après le premier jalon fonctionnel (« walking skeleton »), une **question d'autonomie posée une seule fois** (gated à chaque étape vs autonome), avec **halt-and-ask systématique sur échec**. Absent du workflow.

Les arbitrages de cadrage (Stage 1) fixent le cadre de ce stade :

- **Q3** — nomenclature **AI-DLC 5 phases** adoptée, avec conservation des libellés historiques comme **alias** ([ADR-0002](0002-strategie-compatibilite-et-terminologie.md)).
- **Q2** — **compatibilité ascendante** : Initialization et Ideation s'ajoutent en amont, les trois phases historiques restent inchangées, aucune référence existante n'est cassée.
- **Q6** — le contrôle sécurité (Architecte cybersécurité) est sollicité sur les mécanismes touchant la posture de sécurité ; le mode d'autonomie touche directement le principe « aucune action à impact sans validation humaine », il est donc soumis au contrôle sécurité.

La question spécifique « le mode d'autonomie est-il applicable dans notre gouvernance A2A, où l'humain valide déjà granulairement ? » est tranchée ci-dessous : **adopté, mais adapté** — l'autonomie regroupe le *moment* de la validation, jamais sa granularité, et ne touche jamais aux invariants.

## Décision

**Adopter la structure à 5 phases AI-DLC** et **introduire le mode d'autonomie en Construction**, dans le strict respect des invariants de gouvernance A2A.

### 1. Structure à 5 phases

`Initialization → Ideation → Inception → Construction → Operation`.

- **Initialization (Phase 0)** — bootstrap **déterministe, sans gate humain** : vérification du répertoire projet (seule sollicitation humaine possible : répertoire introuvable, garde déterministe et non gate), détection brownfield / greenfield (fait consigné, non validé), initialisation de la piste d'audit et chargement paresseux des règles toujours actives.
- **Ideation (Phase 1)** — cadrage amont **léger** : capture de l'intention (entrée brute), faisabilité / contraintes, auto-détection + confirmation du scope et des axes, maquettes **conditionnelles (UI uniquement, sinon N/A)**, puis **gate humain léger** approuvant intention + périmètre. Aucune production détaillée ni ADR à ce stade. **Réutilise les agents existants** (coordinateur pour la capture, Architecte de solution pour les maquettes) — aucun nouveau rôle.
- **Inception (Phase 2)**, **Construction (Phase 3)**, **Operation (Phase 4)** — les trois phases historiques, **périmètre inchangé** ; seule la numérotation est décalée par l'ajout des deux phases amont.

Un **tableau de correspondance (alias)** est intégré à `core-workflow.md` : les libellés historiques restent valides, et les couches de règles `phase` (`core/rules/phases/{inception,construction,operation}.md`) restent nommées par le **nom** de phase (pas le numéro), donc inchangées.

### 2. Mode d'autonomie en Construction

- **Walking skeleton** — plus petite tranche **de bout en bout** validée par l'humain (dans notre contexte documentaire : première vue d'architecture + ADR, ou premier module IaC / spec OpenSpec). Il passe **obligatoirement** par la validation granulaire et le contrôle sécurité (aucune autonomie avant lui).
- **La question, posée une seule fois** — après validation du walking skeleton, le coordinateur demande, pour le reste du lot de Construction : rythme **gated à chaque étape** *(défaut)* ou **autonome jusqu'au prochain point de synchronisation**. En mode autonome, les livrables **du même lot déjà cadré** s'enchaînent sans re-valider chaque étape ; la validation granulaire est **regroupée** en un point de synchronisation (fin de lot) — l'humain valide alors **en bloc, mais toujours choix par choix**. La réponse est consignée sur l'issue, ne se présume jamais (pas de réponse ⇒ gated), et un nouveau lot re-pose la question.
- **Halt-and-ask systématique sur échec** — quel que soit le mode, l'exécution s'arrête et interroge l'humain sur : (1) échec / impossibilité d'un livrable, (2) écart ou contrôle de sécurité requis, (3) verification gate / sensor en écart ou `⛔ indisponible`, (4) décision structurante nouvelle non cadrée, (5) action à impact / destructive (jamais autonome — relève d'Operation).

### 3. Garde-fous (invariants non contournables)

Le mode autonome **regroupe le moment de la validation, il ne la supprime pas**. Restent intacts : validation humaine granulaire (jamais fusionnée en « tout ou rien »), contrôle sécurité systématique (jamais court-circuité ni différé), piste d'audit au fil de l'eau, **aucune action à impact en autonomie** (Operation reste sous validation explicite), et **réversibilité** (retour en gated possible à tout point de synchronisation). Cohérence avec les scopes : plancher `renforcé` et halt-and-ask sécurité pleins sur `security-patch` / `enterprise`.

### 4. Diagrammes

Les deux diagrammes Mermaid de `core-workflow.md` (vue d'ensemble des phases + points de synchronisation A2A) sont mis à jour pour refléter les 5 phases et le mode d'autonomie. **Syntaxe validée** (parse Mermaid v11 : flowchart-v2 et sequence — sans erreur).

## Conséquences

### Positives

- **POS-001** : Alignement structurel complet sur AI-DLC 2.0 (les 7 écarts A→G du cadrage sont désormais tous traités).
- **POS-002** : Initialization rend explicite et déterministe le bootstrap (répertoire, brownfield / greenfield) auparavant implicite dans « Chargement du contexte au démarrage ».
- **POS-003** : Ideation évite d'engager l'Inception sur une base non viable (cadrage amont léger avant conception détaillée).
- **POS-004** : Le mode d'autonomie réduit la charge de validation sur les lots à faible risque **sans** sacrifier la granularité (regroupée, jamais supprimée) ni la sécurité.
- **POS-005** : Compatibilité ascendante préservée — aucune référence existante cassée ([ADR-0002](0002-strategie-compatibilite-et-terminologie.md)) ; couches de règles `phase` inchangées.

### Négatives

- **NEG-001** : Deux phases supplémentaires alourdissent nominalement le parcours ; atténué par le caractère déterministe / léger d'Initialization et d'Ideation et par les scopes (`poc` / `express` allègent l'Ideation).
- **NEG-002** : Le mode d'autonomie introduit une variabilité du rythme de validation ; atténué par le défaut **gated** (pas de réponse ⇒ gated), le halt-and-ask systématique et la traçabilité du choix sur l'issue.
- **NEG-003** : Coexistence temporaire de la numérotation ancienne (dans les références en cours) et nouvelle ; atténuée par le tableau de correspondance.

## Alternatives étudiées

### ALT-001 - Conserver 3 phases, ne pas ajouter Initialization / Ideation

**Raison du rejet** : laisse l'écart A ouvert ; le bootstrap resterait implicite et le cadrage amont non formalisé, contraire à Q3 (nomenclature AI-DLC 5 phases) validé au cadrage.

### ALT-002 - Écarter le mode d'autonomie au profit de la validation systématique actuelle

Conserver la validation granulaire à chaque étape, sans option autonome.

**Raison du rejet** : l'autonomie AI-DLC est adaptable à notre gouvernance sans en éroder les invariants (elle regroupe le moment de validation, pas sa granularité) et apporte un gain réel sur les lots à faible risque. Le maintien du **défaut gated** préserve intégralement le comportement actuel pour qui ne l'active pas.

### ALT-003 - Mode autonome sans halt-and-ask ni garde-fous sécurité

Laisser les agents enchaîner librement une fois l'autonomie choisie.

**Raison du rejet** : contournerait le contrôle sécurité systématique et la validation des actions à impact — violation directe des invariants non négociables. Le halt-and-ask et les garde-fous sont **constitutifs** du mode, pas optionnels.

## Notes d'implémentation

- **IMP-001** : Phases renumérotées dans `core-workflow.md` — Inception `1.x → 2.x`, Construction `2.x → 3.x`, Operation `3.x → 4.x` ; Initialization `0.x`, Ideation `1.x` ajoutées. Références internes mises à jour (points de contrôle sécurité §2.5 / §3.2 ; matrice stage × scope ; frontières des verification gates).
- **IMP-002** : Matrice des **verification gates** ([ADR-0005](0005-verification-gates-et-sensors.md), IMP-003 de l'[ADR-0003](0003-scopes-et-axes-depth-verification.md)) alignée sur les 5 frontières de phases (ajout des frontières Entrée → Initialization, Initialization → Ideation, Ideation → Inception).
- **IMP-003** : Matrice **stage × scope** ([ADR-0003](0003-scopes-et-axes-depth-verification.md)) enrichie des lignes Initialization (`0.x`) et Ideation (`1.x`) et renumérotée pour Inception / Construction / Operation.
- **IMP-004** : Diagrammes Mermaid mis à jour et **syntaxe validée** (parse Mermaid v11 sans erreur : flowchart-v2 + sequence).
- **IMP-005** : Contrôle sécurité (Architecte cybersécurité) sollicité sur le diff réel avant validation humaine, en particulier sur le mode d'autonomie (garde-fous : validation granulaire préservée, contrôle sécurité non court-circuité, aucune action à impact en autonomie, halt-and-ask sécurité).

## Références

- **REF-001** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [ADR-0002 - Stratégie de compatibilité et terminologie](0002-strategie-compatibilite-et-terminologie.md)
- **REF-003** : [ADR-0003 - Scopes et axes Depth / vérification](0003-scopes-et-axes-depth-verification.md)
- **REF-004** : [ADR-0005 - Verification gates et Sensors](0005-verification-gates-et-sensors.md)
- **REF-005** : Issue ALI-189 (Stage 5 — Passage à 5 phases + mode d'autonomie Construction) ; issue parente ALI-184 ; cadrage ALI-185.
- **REF-006** : [AI-DLC workflows (awslabs)](https://github.com/awslabs/aidlc-workflows)
