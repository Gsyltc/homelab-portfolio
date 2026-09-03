# Passage à 5 phases et mode d'autonomie en Production et Contrôle — Homelab

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : multica.gaston (validation humaine — ALI-205)
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> En attente de validation humaine granulaire sur l'issue ALI-205. Passe `Accepted` sur le feu vert de `multica.gaston` (nomenclature déjà validée au Stage 1, cf. ADR-0013 §3).

## Contexte

Le workflow `docs/homelab-workflow.md` était structuré en **3 phases** (`Cadrage et Paramètres` → `Production et Contrôle` → `Validation et Déploiement`). L'analyse comparative avec AI-DLC 2.0 (issue parente ALI-200) a identifié deux écarts structurels, comblés au Stage 5 (ALI-205) :

- **A — 5 phases** : AI-DLC 2.0 structure le cycle en `Initialization → Ideation → Inception → Construction → Operation`. Manquaient **Initialization** (bootstrap déterministe : détection « stack existante vs nouvelle », lecture du verrou de concurrence par stack, vérification anticipée des prérequis de déploiement, pose des labels — **sans gate humain**) et **Ideation** (cadrage amont léger : capture d'intention, faisabilité / arbitrage Docker Swarm vs Proxmox, auto-détection + confirmation du scope, pré-sélection du type d'authentification, gate humain léger).
- **G — Mode d'autonomie en Construction** : AI-DLC pose, après le premier jalon fonctionnel (« walking skeleton »), une **question d'autonomie posée une seule fois** (gated à chaque étape vs autonome jusqu'au prochain point de synchronisation), avec **halt-and-ask systématique sur échec**. Absent du workflow Homelab, qui validait tout systématiquement — sûr, mais lourd pour les `config-change`.

Ce stade est le **miroir Homelab** de la décision prise pour `core-workflow.md` ([ADR-0006](0006-passage-5-phases-et-mode-autonomie-construction.md), issue ALI-189). Les arbitrages de cadrage (Stage 1, [ADR-0013](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)) fixent le cadre :

- **Nomenclature métier Homelab** validée par l'humain au Stage 1 (§3 de l'ADR-0013), avec **tableau de correspondance** vers les 5 phases AI-DLC : `Initialisation / Idéation / Cadrage et Paramètres / Production et Contrôle / Validation et Déploiement`.
- **Compatibilité ascendante** : les deux phases amont s'ajoutent devant, les trois phases historiques restent inchangées (périmètre), aucune référence existante n'est cassée ; les libellés historiques restent des alias.
- Le mode d'autonomie touche directement le principe « aucune action à impact sans validation humaine » : il est donc soumis au **contrôle sécurité** (Architecte de sécurité Homelab / QA Docker) et strictement borné par les invariants.

La question « le mode d'autonomie est-il applicable dans notre gouvernance A2A, où l'humain valide déjà granulairement ? » est tranchée ci-dessous : **adopté, mais adapté** — l'autonomie regroupe le *moment* de la validation, jamais sa granularité, et ne touche jamais aux invariants.

## Décision

**Adopter la structure à 5 phases AI-DLC** (nomenclature Homelab) et **introduire le mode d'autonomie en Production et Contrôle**, dans le strict respect des invariants de gouvernance A2A du Homelab.

### 1. Structure à 5 phases

`Initialisation (Phase 0) → Idéation (Phase 1) → Cadrage et Paramètres (Phase 2) → Production et Contrôle (Phase 3) → Validation et Déploiement (Phase 4)`.

- **Initialisation (Phase 0)** — bootstrap **déterministe, sans gate humain** : (0.1) détection « stack existante vs nouvelle » (fait consigné, non validé) ; (0.2) lecture du verrou de concurrence par stack (`active_step`) ; (0.3) vérification **anticipée advisory** des prérequis de déploiement (`[répertoire de travail]`, accessibilité Kestra) ; (0.4) pose des labels `Homelab` / `Docker Swarm`, initialisation de la piste d'audit et chargement paresseux des règles `global`. La seule sollicitation humaine possible est un garde-fou déterministe (prérequis manifestement absent), pas un gate.
- **Idéation (Phase 1)** — cadrage amont **léger** : (1.1) capture d'intention (entrée brute) ; (1.2) faisabilité / arbitrage Docker Swarm vs Proxmox amorcé, auto-détection + confirmation du scope, pré-sélection de `${auth_type}` si la doc est connue ; (1.3) **gate humain léger** approuvant intention + périmètre. Aucune production détaillée ni ADR à ce stade. **Réutilise les rôles existants** (Tech Lead pour la capture et le cadrage amont) — aucun nouveau rôle.
- **Cadrage et Paramètres (Phase 2)**, **Production et Contrôle (Phase 3)**, **Validation et Déploiement (Phase 4)** — les trois phases historiques, **périmètre inchangé** ; seule la numérotation est décalée (§1.x → §2.x, §2.x → §3.x, §3.x → §4.x).

Un **tableau de correspondance (alias)** est intégré à `homelab-workflow.md`. Les couches de règles `phase` ([`homelab/rules/phases/<phase>.md`](../homelab/rules/README.md)) restent nommées par le **nom** de phase (pas le numéro) — inchangées. Le prérequis de déploiement **§3.0 devient §4.0** ; son rôle de contrôle **bloquant** de référence en entrée de la phase de validation est **intégralement préservé**, complété d'un rappel advisory anticipé en §0.3. Le **verrou de concurrence par stack** est préservé et désormais explicitement **lu dès la Phase 0** (§0.2).

### 2. Mode d'autonomie en Production et Contrôle (§3.0)

- **Walking skeleton** — plus petite tranche cohérente du lot (squelette du docker-compose vérifié par le QA Docker, ou premier `.tfvars`) validée par l'humain. Il passe **obligatoirement** par le QA Docker (§3.2), le contrôle qualité central (§3.6) et la validation granulaire. **Aucune autonomie avant lui.**
- **La question, posée une seule fois** — après validation du walking skeleton, le Tech Lead demande, pour le reste du lot déjà cadré : rythme **gated à chaque étape** *(défaut)* ou **autonome jusqu'au prochain point de synchronisation**. En mode autonome, les livrables du même lot s'enchaînent sans re-valider chaque étape ; la validation granulaire est **regroupée** en un point de synchronisation (fin de lot) — l'humain valide alors **en bloc, mais toujours choix par choix**. La réponse est consignée sur l'issue, ne se présume jamais (pas de réponse ⇒ gated), et un nouveau lot re-pose la question.
- **Halt-and-ask systématique sur échec** — quel que soit le mode, l'exécution s'arrête et interroge l'humain sur : (1) échec / impossibilité d'un livrable ; (2) écart ou contrôle de sécurité requis ; (3) verification gate / sensor en écart, bloquant, ou `⛔ indisponible` ; (4) décision structurante nouvelle non cadrée ; (5) action à impact / destructive (dépôt de fichiers, flux Kestra) — **jamais autonome**, elle relève de la Phase 4.

### 3. Garde-fous (invariants non contournables)

Le mode autonome **regroupe le moment de la validation, il ne la supprime pas**. Restent intacts : validation humaine granulaire (jamais fusionnée en « tout ou rien »), **règle absolue n8n (§2.1)**, sélection auto d'authentification (§2.4), **verrou de concurrence par stack** (`active_step`), contrôle sécurité systématique (jamais court-circuité ni différé), piste d'audit au fil de l'eau, **aucune action à impact en autonomie** (dépôt de fichiers et flux Kestra restent sous validation explicite en Phase 4), **réversibilité** (retour en gated possible à tout point de synchronisation), Terraform ne déploie jamais, aucun secret, jamais `${SNI}`. Cohérence scopes : plancher `renforcé` et halt-and-ask sécurité **pleins** sur `security-patch` / `new-stack` ; le mode autonome n'abaisse jamais un niveau lié à la sécurité.

### 4. Diagrammes

Les deux diagrammes Mermaid de `homelab-workflow.md` (vue d'ensemble des phases + points de synchronisation A2A) sont mis à jour pour refléter les 5 phases, le gate léger d'Idéation et le mode d'autonomie. **Syntaxe validée** (parse Mermaid v11 : flowchart + sequence — sans erreur).

## Conséquences

### Positives

- **POS-001** : Alignement structurel complet sur AI-DLC 2.0 (les écarts A→G de l'analyse comparative sont désormais tous traités : scopes, Depth/vérification, learning loop, gates & sensors, 5 phases, autonomie).
- **POS-002** : L'Initialisation rend explicite et déterministe le bootstrap (détection stack, lecture du verrou, prérequis anticipés, labels) auparavant implicite ou tardif.
- **POS-003** : L'Idéation évite d'engager le Cadrage détaillé sur une base non viable (faisabilité + arbitrage Swarm/Proxmox amont, scope confirmé tôt).
- **POS-004** : Le mode d'autonomie réduit la charge de validation sur les lots à faible risque (`config-change`) **sans** sacrifier la granularité (regroupée, jamais supprimée) ni la sécurité.
- **POS-005** : Compatibilité ascendante préservée — aucune référence cassée, libellés historiques valides comme alias, couches de règles `phase` inchangées, verrou de concurrence et prérequis de déploiement conservés.

### Négatives

- **NEG-001** : Deux phases supplémentaires alourdissent nominalement le parcours ; atténué par le caractère déterministe / léger d'Initialisation et d'Idéation et par les scopes (`config-change` allège l'Idéation).
- **NEG-002** : Le mode d'autonomie introduit une variabilité du rythme de validation ; atténué par le défaut **gated** (pas de réponse ⇒ gated), le halt-and-ask systématique, la réversibilité et la traçabilité du choix sur l'issue.
- **NEG-003** : Renumérotation des sections (§1.x → §2.x, etc.) dans les références en cours ; atténuée par le tableau de correspondance et la mise à jour de toutes les références internes.

## Alternatives étudiées

### ALT-001 — Conserver 3 phases, ne pas ajouter Initialisation / Idéation

**Raison du rejet** : laisse l'écart A ouvert ; le bootstrap resterait implicite et le cadrage amont non formalisé, contraire à la nomenclature 5 phases validée par l'humain au Stage 1 (ADR-0013 §3).

### ALT-002 — Écarter le mode d'autonomie au profit de la validation systématique actuelle

**Raison du rejet** : l'autonomie AI-DLC est adaptable à la gouvernance A2A Homelab sans en éroder les invariants (elle regroupe le moment de validation, pas sa granularité) et apporte un gain réel sur les `config-change`. Le maintien du **défaut gated** préserve intégralement le comportement actuel pour qui ne l'active pas.

### ALT-003 — Mode autonome sans halt-and-ask ni garde-fous sécurité

**Raison du rejet** : contournerait le contrôle sécurité systématique et la validation des actions à impact (dépôt de fichiers, Kestra) — violation directe des invariants non négociables. Le halt-and-ask et les garde-fous sont **constitutifs** du mode, pas optionnels.

## Notes d'implémentation

- **IMP-001** : Phases renumérotées dans `homelab-workflow.md` — Cadrage `1.x → 2.x`, Production `2.x → 3.x`, Validation `3.x → 4.x` ; Initialisation `0.x`, Idéation `1.x` ajoutées. Références internes mises à jour (règle n8n §2.1, auth §2.4, QA Docker §3.2, contrôle central §3.6, prérequis §4.0, validation §4.2, dépôt §4.3, Kestra §4.4).
- **IMP-002** : Matrice des **verification gates** ([ADR-0016](0016-verification-gates-et-sensors-homelab.md)) alignée sur les frontières des 5 phases (ajout des frontières Demande → Phase 0, Phase 0 → Phase 1, Phase 1 → Phase 2 ; l'ancienne frontière Phase 2 → Phase 3 devient Phase 3 → Phase 4 et conserve l'anticipation des prérequis §4.0).
- **IMP-003** : Matrice **scope × phase** ([ADR-0014](0014-scopes-homelab-et-axes-depth-verification.md)) re-projetée sur les 5 phases (lignes Initialisation `§0.x` et Idéation `§1.x` ajoutées, corps renuméroté §2.x / §3.x / Phase 4).
- **IMP-004** : Diagrammes Mermaid mis à jour et **syntaxe validée** (parse Mermaid v11 sans erreur : flowchart + sequence). Correctif : suppression d'un `;` dans un `Note over` du diagramme de séquence (séparateur d'instruction Mermaid).
- **IMP-005** : Le mode d'autonomie est soumis au **contrôle sécurité** (Architecte de sécurité Homelab / QA Docker) sur le diff réel avant validation humaine (garde-fous : validation granulaire préservée, contrôle sécurité non court-circuité, aucune action à impact en autonomie, halt-and-ask sécurité, plancher `renforcé` intact sur `security-patch` / `new-stack`).

## Références

- **REF-001** : [ADR-0006 — Passage à 5 phases et mode d'autonomie en Construction (core)](0006-passage-5-phases-et-mode-autonomie-construction.md) — décision miroir.
- **REF-002** : [ADR-0013 — Cadrage de la refonte homelab-workflow.md sur AI-DLC](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md) — nomenclature validée (§3).
- **REF-003** : [ADR-0014 — Scopes Homelab et axes Depth / vérification](0014-scopes-homelab-et-axes-depth-verification.md).
- **REF-004** : [ADR-0016 — Verification gates et Sensors — Homelab](0016-verification-gates-et-sensors-homelab.md).
- **REF-005** : Issue ALI-205 (Stage 5 — Passage à 5 phases + mode d'autonomie Homelab) ; issue parente ALI-200 ; cadrage ALI-201.
- **REF-006** : [AI-DLC workflows (awslabs)](https://github.com/awslabs/aidlc-workflows).
