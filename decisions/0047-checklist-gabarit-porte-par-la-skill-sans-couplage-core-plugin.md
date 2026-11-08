# Gabarit d'état de la checklist porté par la skill `architecture-solution-gabarits`, sans couplage `core → plugin`

---
auteurs: Sylvain Goubaud
accepté par : "Sylvain Goubaud"
accepté le : "2026-11-08"
supersedes: ""
superseded_by: ""

---

## Status

Accepted

## Date de création

2026-11-06

## Contexte

La **checklist d'architecture** est un processus de suivi du workflow `core` : un fichier d'état versionné `documentation/00-checklist-architecture.md`, dont la logique (structure imposée, barème 80/10/10, écriture sur faits vérifiés) a sa **source unique** dans le protocole `core/common/protocols/architecture-checklist.md`, et dont le **gabarit d'état** servait de modèle à l'initialisation.

Jusqu'ici, ce gabarit vivait dans `core` : `core/common/protocols/gabarits/00-checklist-architecture.md`. Ce placement était un **choix assumé** d'ADR-0042 (NEG-002, repris par la chaîne 0042 → 0043 → 0045) : garder le processus `core` **self-contained**, sans **couplage `core → plugin`**, « à réévaluer si une consolidation des gabarits est décidée ». L'initialisation idempotente du fichier d'état était alors portée par le stage `directory-check` (Phase 0, `core`), qui **copiait** le gabarit depuis ce chemin `core`.

L'humain demandeur (multica.gaston, HOM-273 / HOM-286) décide cette réévaluation : le gabarit doit être **porté par la skill `architecture-solution-gabarits`** (où vivent déjà les autres gabarits de `documentation/`), **mais sans introduire de couplage `core → plugin`** — contrainte explicite et non négociable. Déplacer simplement le gabarit dans la skill et faire lire son chemin par `directory-check` créerait précisément le couplage refusé. La contrainte impose donc de **sortir de `core` la responsabilité d'initialisation** de la checklist.

Ce changement touche la **surface de gouvernance** du workflow (emplacement d'un gabarit de processus, déplacement d'une responsabilité d'un stage `core` vers une skill, inversion d'un invariant d'ADR-0042). Verdict d'**impact structurant : Oui** ⇒ ADR obligatoire (« ADR d'abord », `conductor.md`). Le présent ADR **complète et actualise** l'invariant de NEG-002 (sans superséder ADR-0042, déjà `Superseded` par 0043).

## Décision

**Déplacer le gabarit d'état de la checklist vers la skill `architecture-solution-gabarits` et retirer de `core` toute dépendance à ce gabarit : l'initialisation de la checklist quitte `core` et devient portée par son propriétaire (la skill / l'Architecte de solution intégrateur), désignée par propriétaire et non par chemin.**

1. **Déplacement du gabarit** — `core/common/protocols/gabarits/00-checklist-architecture.md` → `plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/00-checklist-architecture.md` (contenu inchangé). Le répertoire `core/common/protocols/gabarits/`, devenu vide, est supprimé.

2. **Invariant « aucun couplage `core → plugin` »** — `core` ne lit **jamais** un chemin de plugin. En conséquence :
   - le stage `core/common/stages/initialization/directory-check.md` (Phase 0) **vérifie la présence** du fichier d'état (simple existence de fichier, déterministe) et, **si absent**, **délègue l'initialisation à son propriétaire** (la skill) ; il ne **copie pas** le gabarit lui-même et ne connaît **aucun** chemin de plugin ;
   - le `conductor.md` (§ « Checklist d'architecture », puce **État**) et le protocole `architecture-checklist.md` (§ 1 et § 2) renvoient au gabarit **par propriétaire** (la skill), **sans chemin relatif** vers le plugin.

3. **Protocole en source unique dans `core`** — `core/common/protocols/architecture-checklist.md` **reste** la source unique du **processus** (logique, barème 80/10/10, conformité constatée, revue pair, acceptation humaine). Seul le **gabarit d'état** (tables de suivi) change de propriétaire ; la mécanique reste dans `core`.

4. **Présence vérifiée en Initialization, initialisation déléguée au propriétaire** — la **présence** de `documentation/00-checklist-architecture.md` est **vérifiée en phase d'Initialization** (stage `directory-check`, Phase 0, Step 3), par une simple vérification d'existence de fichier (déterministe, sans gabarit, sans chemin de plugin). Si le fichier est **absent**, l'**initialisation** idempotente (copie du gabarit, tous éléments à `0 %`, jamais d'écrasement) est **déléguée à son propriétaire** — la skill `architecture-solution-gabarits` (Architecte de solution intégrateur), **désignée par propriétaire et non par chemin**. `directory-check` produit désormais `checklist_architecture_verifiee`. La règle d'or **3-bis** du `SKILL.md` traite ce gabarit **à part** de la copie en lot de la DAS (fichier d'état de processus, **pas** un fichier DAS).

### Périmètre

- Déplacement documentaire du gabarit + retrait des dépendances `core` au gabarit + report de la responsabilité d'initialisation vers la skill (par propriétaire).
- **Hors périmètre** : la logique du protocole (inchangée), les 5 phases, les scopes, les sensors, les contrats `required-sections` / `data-lifecycle`, la posture de sécurité, la validation humaine granulaire. Le sensor `checklist-progress` (HOM-287) est une décision **distincte**.

## Conséquences

### Positives

- **POS-001** — **aucun couplage `core → plugin`** : `core` ne lit plus aucun chemin de plugin ; l'invariant est renforcé et explicite (contrainte humaine respectée).
- **POS-002** — **consolidation des gabarits** : le gabarit d'état vit désormais aux côtés des autres gabarits de `documentation/`, chez leur propriétaire naturel (la skill), avec son traitement d'initialisation spécifique (règle d'or 3-bis).
- **POS-003** — **source unique du processus préservée** : la logique (barème 80/10/10) reste dans `core/common/protocols/architecture-checklist.md` ; seul le modèle de fichier a changé de lieu.
- **POS-004** — **responsabilité claire** : l'initialisation appartient à l'Architecte de solution intégrateur (propriétaire du gabarit), désignée par propriétaire, pas par chemin.

### Négatives / points d'attention

- **NEG-001 (inversion de NEG-002, ADR-0042)** — le gabarit n'est **plus** self-contained dans `core` : le processus `core` **dépend d'un propriétaire externe** (la skill) pour l'initialisation du fichier d'état. Dépendance assumée et bornée à l'**initialisation** ; aucun chemin de plugin n'est lu depuis `core` (la dépendance est **par propriétaire**, sens plugin → core autorisé, sens core → plugin interdit).
- **NEG-002** — **séparation vérification / initialisation** : la **vérification de présence** reste en Phase 0 (`directory-check`, bootstrap déterministe), mais la **copie du gabarit** (initialisation si absent) est **déléguée au propriétaire** (la skill). `core` fait une simple vérification d'existence ; il ne copie pas le gabarit et ne lit aucun chemin de plugin. La bonne tenue de l'invariant repose donc sur cette délégation (le propriétaire doit être sollicitable à l'Initialization).
- **NEG-003** — **cohérence à maintenir** entre le `SKILL.md` (propriétaire, règle d'or 3-bis), le protocole (source unique) et le stage `directory-check` (vérification de présence, délégation d'init) ; les renvois par propriétaire doivent le rester (ne jamais réintroduire un chemin de plugin dans `core`).

## Alternatives étudiées

### ALT-001 — Déplacement complet avec lecture du chemin plugin par `directory-check` (A1)

Déplacer le gabarit dans la skill et faire lire son chemin par `directory-check`. **Non retenue** : recrée exactement le couplage `core → plugin` refusé par l'humain et par l'esprit d'ADR-0025 / 0042.

### ALT-002 — Statu quo (gabarit dans `core`, NEG-002 d'ADR-0042)

Garder le gabarit dans `core/common/protocols/gabarits/`. **Non retenue** : l'humain décide la consolidation des gabarits chez leur propriétaire (la skill), ce qu'ADR-0042 réservait explicitement à une réévaluation ultérieure.

### ALT-003 — Dupliquer le gabarit (skill + `core`)

Garder une copie dans `core` et une dans la skill. **Non retenue** : viole la source unique, dérive garantie entre deux copies.

## Notes d'implémentation

- **IMP-001** — `git mv core/common/protocols/gabarits/00-checklist-architecture.md plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/00-checklist-architecture.md` (contenu inchangé) ; suppression du répertoire `core/common/protocols/gabarits/` devenu vide.
- **IMP-002** — `directory-check.md` (Phase 0) : `produces` porte `checklist_architecture_verifiee` ; **Step 3** dédié « Vérifier la présence de la checklist d'architecture (initialiser si absente) » — présent ⇒ ne rien faire (idempotent) ; absent ⇒ initialisation **déléguée au propriétaire** (la skill), `core` ne copiant pas le gabarit et ne lisant aucun chemin de plugin ; ligne Sensors / note d'invariant mises à jour.
- **IMP-003** — `conductor.md` (puce **État**) et `architecture-checklist.md` (§ 1 et § 2) : renvoi au gabarit **par propriétaire** (skill), sans chemin de plugin.
- **IMP-004** — `intake-framing.md` (Inception) : **ne traite plus** la checklist (retrait de l'artefact `checklist_architecture_*` de `produces` et du step dédié) ; Step 2 rappelle que la présence est vérifiée en Initialization (`directory-check`, Step 3) ; Steps 1→5 remis dans leur ordre d'origine ; ligne Sensors Outputs mise à jour.
- **IMP-005** — `SKILL.md` : ligne `00-checklist-architecture.md` au tableau « Contenu des gabarits » (fichier d'état de processus, pas DAS) + règle d'or **3-bis** (init à part, idempotente, règles de tenue en source unique dans `core`).
- **IMP-006** — vérification : aucun chemin de plugin résiduel dans `core/` (`grep`), liens relatifs résolus après déplacement, `python3 -m unittest discover -s core/scripts/tests` reste vert.

## Références

- **REF-001** — HOM-273 (mission d'origine) / HOM-286 (sous-issue A, ce travail) : multica.gaston, contrainte « aucun couplage `core → plugin` ».
- **REF-002** — [`0042-checklist-architecture-processus-protocole-gabarit.md`](0042-checklist-architecture-processus-protocole-gabarit.md) : NEG-002 (emplacement du gabarit dans `core`), invariant ici inversé. ADR-0042 est `Superseded` par 0043.
- **REF-003** — [`0043-checklist-architecture-avancement-en-pourcentage-bareme-80-10-10.md`](0043-checklist-architecture-avancement-en-pourcentage-bareme-80-10-10.md) et [`0045-checklist-architecture-sections-requises-securite.md`](0045-checklist-architecture-sections-requises-securite.md) : chaîne d'évolution de la checklist.
- **REF-004** — [`0025-durcissement-required-sections-das.md`](0025-durcissement-required-sections-das.md) : esprit « Option A » (self-contained, sans couplage) dont cette décision ajuste l'application pour le gabarit de checklist.
- **REF-005** — [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) : source unique du processus (inchangée).
- **REF-006** — [`core/common/stages/initialization/directory-check.md`](../core/common/stages/initialization/directory-check.md) : vérification de présence (Phase 0, Step 3) et délégation d'initialisation au propriétaire. [`core/common/stages/inception/intake-framing.md`](../core/common/stages/inception/intake-framing.md) : ne traite plus la checklist (rappel que la présence est vérifiée en Initialization).
- **REF-007** — [`plugins/architecture-assistant/skills/architecture-solution-gabarits/SKILL.md`](../plugins/architecture-assistant/skills/architecture-solution-gabarits/SKILL.md) : nouveau propriétaire du gabarit (règle d'or 3-bis).
