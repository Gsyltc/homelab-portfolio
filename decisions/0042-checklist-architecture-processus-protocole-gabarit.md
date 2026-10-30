# Checklist d'architecture comme processus à part — protocole dédié + gabarit d'état (workflow core)

---
auteurs: Architecture Solution & Intégration (agent)
accepté par : ""
accepté le : ""
supersedes: ""
superseded_by: "0043-checklist-architecture-avancement-en-pourcentage-bareme-80-10-10.md"

---

## Status

Superseded

## Date de création

2026-10-29

## Contexte

Le workflow `core` structure le cycle d'architecture en **5 phases** (`Initialization → Ideation → Inception → Construction → Operation`), sous gouvernance A2A du workspace. Jusqu'ici, l'**avancement de l'architecture** d'un projet (ce qui est cadré, exigé, livré, planifié) n'était **nulle part matérialisé** comme un état consolidé et vérifiable : il fallait le reconstituer en parcourant l'issue, les décisions et les fichiers de `documentation/`.

L'humain demandeur (sylvain.rodgers, ORIG-380) demande d'**ajouter au workflow `core` la gestion d'une checklist d'architecture persistante**, suivie tout au long des 5 phases, matérialisée par un **processus à part** (ni stage, ni livrable d'architecture : un processus de suivi) avec un **protocole dédié** et un **gabarit d'état**.

Plusieurs décisions cadrées en amont par l'humain fixent la forme :

1. **État** = fichier livrable versionné `documentation/00-checklist-architecture.md` ; changements d'état **aussi tracés sur l'issue** (piste d'audit).
2. **Forme** = **protocole dédié** `core/common/protocols/architecture-checklist.md` (source unique du cycle lecture/écriture) **+ gabarit d'état** versionné.
3. **Réutilisation des conventions existantes** : s'appuyer sur le sensor [`required-sections`](../core/sensors/sensors/required-sections.md) et la décision [`0040`](0040-aucune-note-de-generation-dans-les-livrables.md) (« aucune note de génération dans les livrables ») — ne pas recréer ces conventions.
4. **Calcul du %** par section et global, seul le statut `validé` comptant.

Introduire un **processus transverse** dans le triptyque `conductor / stages / protocols`, avec une **nouvelle source unique** (le protocole) raccordée au conductor et à un stage d'Initialization, **modifie la surface de gouvernance du workflow**. Au cadrage ([`intake-framing`](../core/common/stages/inception/intake-framing.md), Step 5), le verdict d'**impact structurant** est **Oui** (introduction d'un pattern transverse de suivi + nouvelle source unique de gouvernance). Le garde-fou « ADR d'abord » du [`conductor.md`](../core/common/conductor.md) impose donc de **tracer la décision par ADR**. Le précédent exact existe : [`0040`](0040-aucune-note-de-generation-dans-les-livrables.md) (invariant en source unique + ADR) et [`0025`](0025-durcissement-required-sections-das.md) (évolution de la surface `required-sections`).

## Décision

**Introduire la checklist d'architecture comme processus à part, avec le protocole [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) pour source unique, un gabarit d'état versionné, et un raccordement au conductor qui *pointe* vers le protocole sans dupliquer sa logique.**

1. **Protocole (source unique)** — `core/common/protocols/architecture-checklist.md` décrit : l'emplacement de l'état ; la **structure imposée** (Cadrage ; Besoins MoSCoW ; Livrables ; Projets) et les statuts par élément (`validé` · `en cours` · `refusé` · `non débuté`, défaut `non débuté`) ; le **calcul du %** par section et global (seul `validé` compte) ; l'**écriture sur approbation humaine** après **vérification de conformité** ; la **lecture sur demande** ; le **mapping élément Livrables → document(s) attendu(s)** qui **renvoie** à `required-sections` et `data-lifecycle` sans redéfinir leurs contrats.

2. **Gabarit d'état** — `core/common/protocols/gabarits/00-checklist-architecture.md`, front-matter aligné sur les gabarits DAS, tous les éléments à `non débuté` (0 %), destiné à être copié en `documentation/00-checklist-architecture.md` à l'initialisation.

3. **Raccordement** — le [`conductor.md`](../core/common/conductor.md) référence le protocole (section « Références ») et porte une section « Checklist d'architecture (état d'avancement) » qui **pointe** vers lui. Le stage [`directory-check`](../core/common/stages/initialization/directory-check.md) (Phase 0) initialise le fichier d'état de façon **idempotente** depuis le gabarit.

4. **Réutilisation sans duplication** — la vérification de conformité des Livrables s'appuie sur le sensor advisory `required-sections` (source unique du contrat de sections) ; l'interdiction de note de génération renvoie à la décision `0040`. La checklist ne redéfinit aucun de ces contrats.

### Périmètre

- Porte sur l'ajout **documentaire** d'un processus de suivi au workflow `core` (protocole + gabarit + renvois dans conductor et un stage).
- **Hors périmètre** : aucun changement des 5 phases, des scopes, des sensors existants, des gabarits DAS, ni d'aucune posture de sécurité. Le passage d'un sensor advisory à bloquant resterait une décision séparée.

## Conséquences

### Positives

- **POS-001** — **état consolidé et vérifiable** : l'avancement de l'architecture devient lisible d'un coup d'œil (% par section + global), avec un statut par élément.
- **POS-002** — **source unique** : le cycle lecture/écriture vit à un seul endroit ; le conductor et le stage d'init y renvoient sans divergence possible.
- **POS-003** — **garde-fous préservés** : la validation humaine granulaire reste le seul chemin vers `validé` ; la piste d'audit et la décision `0040` encadrent le fichier d'état ; les sensors restent advisory.
- **POS-004** — **cohérence du triptyque** : la checklist s'inscrit dans le modèle `conductor / stages / protocols` existant, comme processus transverse (à l'image de `output-format`).

### Négatives / points d'attention

- **NEG-001** — **cohérence à maintenir à deux endroits** : le mapping élément Livrables → document s'appuie sur `required-sections` et les gabarits DAS ; toute évolution de nommage/découpage de ces sources doit rester cohérente avec le tableau de mapping du protocole (les sources existantes font foi).
- **NEG-002** — **emplacement du gabarit** : le gabarit vit en `core/common/protocols/gabarits/` (self-contained, sans couplage `core → plugin`, conforme à l'esprit de l'Option A de `required-sections`), et non dans la skill DAS où vivent les autres gabarits de `documentation/`. Choix assumé pour garder le processus `core` autonome ; à réévaluer si une consolidation des gabarits est décidée.
- **NEG-003** — **tenue manuelle** : la mise à jour reste une action du coordinateur sur approbation humaine ; aucun automatisme ne recalcule le % (cohérent avec « ne jamais deviner » et la validation humaine granulaire).

## Alternatives étudiées

### ALT-001 — Suivi dans la piste d'audit de l'issue uniquement (pas de fichier d'état)

Garder l'avancement seulement en commentaires d'issue. **Non retenue** : l'humain demande un **livrable versionné** consolidé dans `documentation/`, lisible hors de l'issue et traçable dans le dépôt du projet.

### ALT-002 — Nouveau stage dédié plutôt qu'un protocole

Modéliser la checklist comme un stage. **Non retenue** : la checklist **suit** l'avancement tout au long des 5 phases, elle n'est pas une étape bornée d'une phase ; un **protocole transverse** (comme `output-format`) est la forme juste. Décision cadrée par l'humain (« processus à part, protocole dédié »).

### ALT-003 — Dupliquer les contrats de sections dans le protocole

Réécrire dans le protocole les sections mandatory des livrables. **Non retenue** : violerait la source unique `required-sections` (risque de dérive) ; le protocole **renvoie** aux sources existantes.

## Notes d'implémentation

- **IMP-001** — création de `core/common/protocols/architecture-checklist.md` (protocole sans front-matter, style aligné sur `output-format.md`).
- **IMP-002** — création de `core/common/protocols/gabarits/00-checklist-architecture.md` (front-matter aligné DAS, tous éléments `non débuté`, 0 %).
- **IMP-003** — raccordement `conductor.md` : entrée « Références » + section « Checklist d'architecture (état d'avancement) » (renvoi au protocole, sans duplication de logique).
- **IMP-004** — raccordement `directory-check.md` : `produces: checklist_architecture_initialisee`, Step 3 d'initialisation idempotente depuis le gabarit, ligne `outputs` mise à jour.
- **IMP-005** — liens relatifs vérifiés (résolution `realpath`) ; front-matter du gabarit validé (YAML).
- **IMP-006** — aucun changement des phases, scopes, sensors, gabarits DAS ni de posture de sécurité ; ajout documentaire uniquement.

## Références

- **REF-001** — ORIG-380 : mission « Workflow core — checklist d'architecture (protocole + gabarit d'état) » (décisions cadrées par sylvain.rodgers).
- **REF-002** — [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) : source unique du processus.
- **REF-003** — [`core/common/protocols/gabarits/00-checklist-architecture.md`](../core/common/protocols/gabarits/00-checklist-architecture.md) : gabarit d'état.
- **REF-004** — [`core/common/conductor.md`](../core/common/conductor.md) : raccordement (Références + section checklist).
- **REF-005** — [`core/common/stages/initialization/directory-check.md`](../core/common/stages/initialization/directory-check.md) : initialisation du fichier d'état (Phase 0).
- **REF-006** — [`core/sensors/sensors/required-sections.md`](../core/sensors/sensors/required-sections.md) : contrat de sections réutilisé (vérification de conformité des Livrables).
- **REF-007** — [`0040-aucune-note-de-generation-dans-les-livrables.md`](0040-aucune-note-de-generation-dans-les-livrables.md) : invariant « aucune note de génération » appliqué au fichier d'état.
- **REF-008** — [`intake-framing.md`](../core/common/stages/inception/intake-framing.md), Step 5 : déclencheur du verdict d'impact structurant (« ADR d'abord »).
