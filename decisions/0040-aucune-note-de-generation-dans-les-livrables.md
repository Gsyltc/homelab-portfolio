# Aucune note de génération / méta-production dans les livrables — invariant source unique (workflow Matching)

---
auteurs: Gestionnaire CV (agent)
accepté par : sylvain.rodgers
accepté le : "2026-10-23"
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — option **source unique + ADR** retenue explicitement par sylvain.rodgers
> (gate EXPE-121, via le Coordinateur Mika). Portage de l'invariant **« Aucune note de génération /
> méta-production dans les livrables »** en **source unique** dans le protocole de gouvernance du workflow
> Matching (`matching-cv-ao/common/protocols/governance-security.md`), plutôt que par duplication dans
> chaque compétence. Évolution **documentaire** du workflow (invariant + renvois), **sans** modification du
> schéma des données CV, des poids de scoring ni d'aucune posture de sécurité. Tous les invariants de
> gouvernance existants (validation humaine granulaire, piste d'audit, « ne rien inventer »,
> non-transmission des CV, absence de secret) sont **préservés**.

## Contexte

Le **Gestionnaire CV** (workflow `matching-cv-ao`) produit un **CV livrable** (DOCX par défaut à partir d'un
gabarit fourni ; Markdown sur demande explicite de l'humain) via la compétence `cv-generation`. Rien, dans
cette compétence, n'interdisait d'y inscrire des **notes de génération / méta-production** : mentions
« généré par l'agent / par l'IA », résumé de ce que l'agent a fait, liens ou identifiants de tâches/issues
(`mention://…`, numéros de tickets), SHA de commit, horodatages de génération, descripteurs d'outil. Ces
notes polluent un livrable qui ne devrait porter **que l'information métier du candidat**.

Un **précédent exact** existait déjà côté plugin `architecture-assistant`, mais **par compétence** :

- `plugins/architecture-assistant/skills/client-presentation-generation/SKILL.md` — règle 14
  « Aucune note de génération / méta-production dans le rendu » et checklist associée ;
- `plugins/architecture-assistant/skills/architecture-solution-gabarits/SKILL.md` — interdiction des
  mentions de méta-génération, SHA de commit et identifiants de tâche de suivi dans les livrables.

La mission EXPE-121 demandait de **combler le trou** côté Gestionnaire CV. Une **première application**
(tour 1) a porté la règle **par compétence** (règle d'or + garde-fou dupliqués dans `cv-generation`, renvoi
dans `cv-analyse`), en signalant l'alternative **source unique** au choix de l'auteur de l'issue. Au gate,
**sylvain.rodgers a tranché : source unique + ADR**. Cette ADR acte ce choix et la réécriture associée.

Le protocole `matching-cv-ao/common/protocols/governance-security.md` est déjà la **source unique** des
invariants non contournables du workflow Matching et de plusieurs règles transverses (schéma du message A2A,
catégories décisionnelles non-retenus/exclus) ; c'est l'emplacement naturel de ce nouvel invariant.

## Décision

**Porter l'invariant en source unique dans le protocole de gouvernance du workflow Matching**, et faire
**renvoyer** les compétences concernées vers cette source, sans dupliquer le corps de la règle.

1. **Source unique** — `matching-cv-ao/common/protocols/governance-security.md` :
   - nouvelle section **« Aucune note de génération / méta-production dans les livrables (source unique) »**
     décrivant l'interdiction (livrable = information métier uniquement ; proscription des mentions de
     méta-génération, résumé d'actions de l'agent, liens/identifiants `mention://…` ou de tickets, SHA de
     commit, horodatages, lignes de version-process, commentaires de processus) et la **frontière
     livrable ↔ traçabilité** (traçabilité légitime sur l'issue et en mémoire interne, interdite dans le
     livrable) ;
   - rappel dans **§ Invariants non contournables** comme **point 7**, renvoyant à la section détaillée.

2. **Renvois sans duplication** :
   - `plugins/rh-assistant/skills/cv-generation/SKILL.md` — la **Règle d'or** et le **garde-fou** renvoient
     à la source unique (invariant 7 / cette ADR) et se bornent à **l'application au CV livrable** ; le
     corps normatif n'est plus dupliqué.
   - `plugins/rh-assistant/skills/cv-analyse/SKILL.md` — la note de **renvoi** pointe vers la source unique
     et confirme que la règle **ne s'applique pas** à la fiche d'analyse ni au YAML (artefacts internes où
     la traçabilité reste légitime).

### Périmètre

- Porte sur la **production des livrables** du workflow Matching (CV livrable en premier lieu ; la
  formulation couvre présentation/document par cohérence transverse).
- **Hors périmètre** : la **fiche d'analyse interne** et le **YAML** (`cv-analyse`) et la **piste d'audit de
  l'issue**, où la traçabilité (format, gabarit, version, validation, identifiants de suivi) reste
  **légitime et requise**.

## Conséquences

### Positives

- **POS-001** : **source unique** — l'invariant est défini une seule fois ; `cv-generation` et `cv-analyse`
  y renvoient sans divergence possible. Toute compétence/fiche future (présentations, autres livrables du
  workflow Matching) s'y réfère par son nom.
- **POS-002** : **cohérence de gouvernance** — l'invariant rejoint les invariants non contournables du
  workflow (point 7), au même niveau que la piste d'audit et la validation humaine, dont il précise la
  frontière (traçabilité sur l'issue, pas dans le livrable).
- **POS-003** : **alignement avec le précédent** architecture-assistant (règle 14 /
  `architecture-solution-gabarits`), désormais **remonté en source unique** côté Matching.
- **POS-004** : **invariants intacts** — validation humaine granulaire, piste d'audit, « ne rien inventer »,
  non-transmission des CV, absence de secret : inchangés (ajout uniquement).

### Négatives / points d'attention

- **NEG-001** : **double emplacement conceptuel** — le précédent architecture-assistant reste **par
  compétence** (règle 14 / `architecture-solution-gabarits`) tandis que le workflow Matching passe en source
  unique. Les deux formulations convergent ; une unification transverse (core) éventuelle est hors périmètre
  EXPE-121 et relèverait d'une décision ultérieure.
- **NEG-002** : **ancrage de l'invariant par workflow** — la source unique vit dans le protocole
  `matching-cv-ao` ; elle ne couvre pas d'office les plugins hors Matching. C'est cohérent avec le périmètre
  de l'issue (Gestionnaire CV) ; une remontée au `core` serait une décision séparée.

## Alternatives étudiées

### ALT-001 — Règle par compétence (duplication)

Porter la règle d'or + le garde-fou directement dans `cv-generation` (et un renvoi dans `cv-analyse`), comme
le fait le précédent architecture-assistant. **Appliquée au tour 1, puis écartée** par l'arbitrage humain :
la duplication expose à la dérive entre copies et ne donne pas de point d'autorité unique ; l'humain a
préféré la **source unique**.

### ALT-002 — Source unique sans ADR

Porter l'invariant en gouvernance sans tracer la décision. **Non retenue** : une décision structurante
(création d'un invariant non contournable) doit être **tracée par ADR** selon les conventions du workflow ;
c'est précisément l'option « source unique + **ADR** » retenue par l'humain.

### ALT-003 — Remontée directe au `core` (gouvernance transverse à tous les workflows)

Porter l'invariant dans `core/common/protocols/governance-security.md` pour couvrir tous les plugins.
**Non retenue à ce stade** : dépasse le périmètre EXPE-121 (Gestionnaire CV / workflow Matching) et
fusionnerait de facto avec le précédent architecture-assistant ; à envisager dans une décision dédiée si le
besoin transverse se confirme.

## Notes d'implémentation

- **IMP-001** : **source unique** — ajout de la section « Aucune note de génération / méta-production dans
  les livrables (source unique) » et de l'invariant **point 7** dans
  `matching-cv-ao/common/protocols/governance-security.md`.
- **IMP-002** : **renvois** — `plugins/rh-assistant/skills/cv-generation/SKILL.md` (Règle d'or + garde-fou
  réécrits en renvoi à la source unique, application au CV livrable) ;
  `plugins/rh-assistant/skills/cv-analyse/SKILL.md` (note de renvoi vers la source unique, confirmation
  artefact interne hors périmètre).
- **IMP-003** : **liens relatifs vérifiés** — depuis les skills `rh-assistant`,
  `../../../../matching-cv-ao/common/protocols/governance-security.md` et `../../../../decisions/…`
  résolvent ; depuis la gouvernance, `../../../decisions/…` résout.
- **IMP-004** : entrée `CHANGELOG.md` (`[Non publié] → Added` : invariant de gouvernance + ADR-0040).
- **IMP-005** : **aucun** changement de schéma des données CV, de poids de scoring ni de posture de
  sécurité ; ajout documentaire only.

## Références

- **REF-001** : EXPE-121 — mission « Interdire les notes de génération dans les CV produits par le
  Gestionnaire CV » ; **arbitrage humain** (sylvain.rodgers, 2026-10-23 : option « source unique + ADR »
  via le Coordinateur Mika).
- **REF-002** : [`matching-cv-ao/common/protocols/governance-security.md`](../matching-cv-ao/common/protocols/governance-security.md)
  — source unique de l'invariant (§ Aucune note de génération / méta-production dans les livrables ;
  § Invariants non contournables, point 7).
- **REF-003** : précédent architecture-assistant —
  `plugins/architecture-assistant/skills/client-presentation-generation/SKILL.md` (règle 14) ;
  `plugins/architecture-assistant/skills/architecture-solution-gabarits/SKILL.md` (méta-génération, SHA,
  identifiants de tâche).
- **REF-004** : compétences couplées —
  `plugins/rh-assistant/skills/cv-generation/SKILL.md` (renvoi + application CV livrable) ;
  `plugins/rh-assistant/skills/cv-analyse/SKILL.md` (renvoi + artefact interne hors périmètre).
- **REF-005** : invariants préservés — validation humaine granulaire, piste d'audit, « ne rien inventer »,
  non-transmission des CV, absence de secret (`governance-security`, `cv-analyse` § Garde-fou).
