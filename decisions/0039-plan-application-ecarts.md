# Plan d'application de l'ADR 0039 — arbitrage humain par écart

> Document de travail (branche `feature/orig-91-adr-0039-flux-a2a-new-stack`, issue ORIG-91).
> Objet : préparer l'application de l'ADR 0039 **sans** finaliser ni committer la moindre
> modification de fiche de stage / protocole / garde-fou tant que l'humain n'a pas arbitré
> chaque écart (granularité **Keep / Modify / Redo**), conformément à l'ADR
> (« aucune modification … tant que la décision n'est pas acceptée »), au critère
> d'acceptation (ADR *Proposed* → *Accepted* **une fois validé**) et aux invariants
> non abaissables (IMP-008 : SEC-1..5 / SG-1..6, validation humaine granulaire).
>
> **Aucun commit / PR / push n'est effectué sans accord explicite de l'humain.**

Pour chaque écart : la décision à arbitrer, l'édition concrète proposée (fichier + nature),
et l'impact sécurité/gouvernance à repasser par le contrôle sécurité le cas échéant.

---

## ÉCART-01 — Délégation Docker / Terraform (parallèle vs séquentiel)

- **Désiré** : délégation **parallèle** Docker + Terraform, attente des deux retours.
- **Documenté** : **séquentiel** (Terraform d'abord ; `.tfvars` = référence de cohérence du
  compose), via `requires_stage: [terraform-configuration]` dans
  `homelab/common/stages/production/docker-compose-creation.md`, et verrou « un seul
  traitement par stack » (`governance-security.md`, `conductor.md` §concurrence).
- **Arbitrage requis (choix humain)** :
  - **(A) Lever la dépendance de cohérence** → délégation parallèle réelle :
    - `docker-compose-creation.md` : retirer `requires_stage: [terraform-configuration]` et
      la dépendance `livrable_tfvars (required)` ; retirer la formulation « vient **après** la
      configuration Terraform ».
    - `conductor.md` §concurrence : adapter le verrou `active_step` pour autoriser **deux**
      délégations concurrentes sur la **même stack** (Docker + Terraform) tout en conservant
      l'unicité du livrable final. **⚠ Touche l'invariant « un seul traitement par stack »
      (NEG-002) → contrôle sécurité obligatoire (SEC-1 : risque de rejet pour érosion).**
  - **(B) Acter le séquentiel-par-conception** → documenter explicitement le choix dans l'ADR
    (section Décision) et **ne modifier aucun fichier** ; le flux désiré « parallèle » est
    requalifié en « séquentiel assumé » car la cohérence `.tfvars → compose` prime.
- **Recommandation agent** : **(B)**, car (A) érode un invariant (SEC-1) et la cohérence
  `.tfvars → compose` est un bénéfice de conception. À confirmer par l'humain.

## ÉCART-02 — Routage des `RENVOI` QA (direct vs via Tech Lead)

- **Désiré** : l'Analyste QA **mentionne directement** le spécialiste concerné (sans Tech Lead).
- **Documenté** : `verdict = RENVOI` (rapport JSON) + compte-rendu au Tech Lead, qui aiguille.
- **Édition proposée si retenu** :
  - `quality-assurance.md` (Step 4) : autoriser l'Analyste QA à mentionner **directement**
    l'agent créateur (Spécialiste Docker / Terraform) sur `verdict = RENVOI`, avec mention
    valide + rapport JSON joint ; copie d'information au Tech Lead.
  - `protocols/reviewer.md` (§ Fin de revue) + `governance-security.md` (§ Règle A2A) :
    documenter la boucle courte QA → spécialiste → QA.
  - `central-quality-control.md` : préciser que l'aiguillage macro du Tech Lead ne porte plus
    les RENVOI techniques (ils sont court-circuités vers le créateur).
- **⚠ Impact gouvernance (NEG-001)** : retire au Tech Lead le point de contrôle macro central
  et peut affaiblir la **piste d'audit centralisée** et le verrou « un seul traitement par
  stack » → **contrôle sécurité obligatoire (SEC-1)**. Préserver : audit sur l'issue, mention
  valide, `trigger_outcomes`.

## ÉCART-03 — Retour spécialiste → QA après correction

- **Désiré** : le spécialiste **mentionne obligatoirement l'Analyste QA** après correction.
- **Documenté** : le spécialiste rend compte au Tech Lead ; re-contrôle QA **via le Tech Lead**.
- **Édition proposée si retenu** :
  - `protocols/report-format.md` + `producer-report.md` : le geste de fin de mission du
    spécialiste, en cas de correction suite à `RENVOI`, cible **l'Analyste QA** (mention
    valide construite par le spécialiste) au lieu du Tech Lead.
  - `reviewer.md` : formaliser la boucle courte (cohérente avec ÉCART-02).
- **⚠ Impact** : couplé à ÉCART-02 ; même exigence de contrôle sécurité (SEC-1) et de
  préservation de la piste d'audit.

## ÉCART-04 — Délégation sécurité séquentielle dédiée

- **Désiré** : étape **séquentielle dédiée** Tech Lead → Architecte de sécurité **après** la QA.
- **Documenté** : pas de stage distinct ; sécurité portée **pendant** la QA (QA technique +
  Architecte jugement).
- **Édition proposée si retenu** :
  - **Créer** `homelab/common/stages/production/security-delegation.md` (nouveau stage,
    `lead_agent: Tech Lead`, `reviewer: Architecte de sécurité Homelab`, `execution: CONDITIONAL`
    sur surface sécurité, `requires_stage: [quality-assurance]`, `human_gate: granular`).
  - `conductor.md` (tableau des phases, ligne « Production et Contrôle ») : insérer le stage
    après `quality-assurance` et avant `central-quality-control`.
  - `governance-security.md` : documenter la séquence QA → délégation sécurité.
- **⚠ Impact** : modifie la **surface de gouvernance sécurité** → **contrôle sécurité
  obligatoire (SG-1 / SG-6 : nouveau stage = modification de la surface de gouvernance)**.
  Invariant à préserver : le contrôle sécurité **précède toujours** la validation humaine.

## ÉCART-05 — « Gate renforcée » (écart MAJEUR, absent)

- **Désiré** : sur sécurité **critique / majeure**, Architecte → mention Tech Lead → mention
  humaine **« Gate renforcée »** → branchement :
  - l'humain **veut** les modifications → Tech Lead mentionne les spécialistes concernés
    (retour mention obligatoire) ;
  - l'humain **refuse** → Tech Lead télécharge le fichier pour **validation granulaire**.
- **Documenté** : **aucune** notion de « Gate renforcée » ni de branchement par gravité ;
  seuls existent le halt-and-ask sécurité (`autonomy-mode.md`) et la validation granulaire
  (`human-granular-validation.md`).
- **Édition proposée si retenu** :
  - **Créer** `homelab/common/stages/validation/reinforced-gate.md` (nouveau stage nommé
    « Gate renforcée », `human_gate: explicit`, déclenché par l'Architecte de sécurité sur
    gravité critique/majeure), formalisant l'escalade et le branchement conditionnel.
  - `autonomy-mode.md` (Step 3, halt-and-ask) + `human-granular-validation.md` : référencer
    la Gate renforcée comme escalade nommée venant **en complément** (jamais en remplacement)
    de la validation humaine granulaire — invariant préservé.
  - `conductor.md` + `sensors/gates.md` : documenter la frontière déclenchant la Gate renforcée.
- **⚠ Impact** : création d'un **gate sécurité nommé** → **contrôle sécurité obligatoire
  (SG-1 : canal des manifestes de gouvernance ; SEC-1 : ne pas affaiblir la validation
  humaine granulaire — la Gate renforcée s'y **ajoute**, ne la remplace pas)**.

## ÉCART-06 — Branchement sécurité non critique

- **Désiré** : sur éléments **non critiques / non majeurs**, retour explicite au Tech Lead
  par mention (branchement par gravité formalisé).
- **Documenté** : couvert **implicitement** mais non formalisé.
- **Édition proposée si retenu** :
  - Dans le même stage sécurité (ÉCART-04) ou `reviewer.md` : formaliser les **deux
    branches** par gravité — critique/majeur → Gate renforcée (ÉCART-05) ; non critique →
    retour Tech Lead par mention valide + rapport JSON.
- **⚠ Impact** : cohérent avec ÉCART-04/05 ; contrôle sécurité au titre de la clarification du
  branchement de gravité.

---

## Point conforme (aucune action)

- **IMP-007** : le retour « phase QA passée » (QA → mention Tech Lead même sur verdict `OK`)
  est **déjà exigé** (`reviewer.md`, « Fin de revue »). Rien à changer.

## Invariants non abaissables (rappel — IMP-008)

Validation humaine granulaire · Terraform ne déploie jamais · aucun secret en clair ·
jamais `${SNI}` · un seul traitement par stack · piste d'audit sur l'issue. Toute évolution
touchant la sécurité (ÉCART-02/03/04/05/06) repasse par le contrôle sécurité
(Architecte de sécurité Homelab, SEC-1..5 / SG-1..6) **avant** d'être committée.

## Suite — arbitrage reçu (multica.gaston, 2026-10-04) et appliqué

Arbitrage humain :
- **ÉCART-01 = A (révisé)** : parallélisme Docker/Terraform via sous-issues `--stage 1` +
  barrière de stage ; verrou de concurrence requalifié **par artefact** (compose vs `.tfvars`) ;
  QA = point de réconciliation de cohérence. Fiches éditées : `docker-compose-creation`
  (retrait `requires_stage: [terraform-configuration]` et dépendance `livrable_tfvars`),
  `terraform-configuration` (parallèle, plus pré-requis amont), `conductor` +
  `governance-security` (verrou par artefact, invariant #5), `quality-assurance` (point de
  cohérence). *(Première décision B — séquentiel — révisée par l'humain.)*
- **ÉCART-02 / 03 = Confirmés** (boucle courte directe QA ↔ spécialistes).
- **ÉCART-04 = Confirmé** avec séquence : Tech Lead contrôle le travail finalisé **avant** le
  contrôle de sécurité (délégation sécurité séquentielle **après** le contrôle qualité central).
- **ÉCART-05** : « Gate renforcée » ≡ validation humaine granulaire (aucun gate distinct créé).
- **ÉCART-06 = Confirmé** (retour Tech Lead par mention sur gravité non critique).

Éditions appliquées sur la branche (non committées) :
1. `decisions/0039-...md` : statut `Proposed` → **`Accepted`**, champs d'acceptation renseignés,
   section « Arbitrage humain » ajoutée.
2. `homelab/common/stages/production/quality-assurance.md` : routage direct QA → spécialiste
   sur `RENVOI` (ÉCART-02/03).
3. `homelab/common/stages/production/security-delegation.md` : **nouveau stage** séquentiel
   Tech Lead → Architecte de sécurité, après le contrôle qualité central, avec branchement par
   gravité (ÉCART-04/05/06).
4. `homelab/common/stages/production/central-quality-control.md` : contrôle du travail finalisé
   avant la sécurité, plus d'aiguillage des `RENVOI` techniques (ÉCART-02/03/04).
5. `homelab/common/stages/validation/human-granular-validation.md` : « Gate renforcée » ≡
   validation granulaire (ÉCART-05).
6. `homelab/common/protocols/reviewer.md` : boucle courte QA ↔ spécialiste + diagramme réordonné
   (QA → contrôle central → délégation sécurité → validation humaine).
7. `homelab/common/protocols/governance-security.md` : séquence `new-stack` ADR 0039 + table des
   acteurs (QA renvoie direct, spécialistes mentionnent la QA en retour).
8. `homelab/common/protocols/report-format.md` : routage `RENVOI` direct QA ↔ spécialiste.
9. `homelab/common/conductor.md` : `security-delegation` ajouté à la Phase 3.

Reste à faire (sur **accord explicite** de l'humain) : **commit / PR / push**. Les invariants
(validation humaine granulaire, Terraform ne déploie jamais, aucun secret en clair, jamais
`${SNI}`, un seul traitement par stack, piste d'audit) sont préservés.
