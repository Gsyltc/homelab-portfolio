# Alignement des scopes Homelab sur le contrat AI-DLC « un fichier par scope »

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : 2026-09-03
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — validation humaine explicite obtenue (multica.gaston, 2026-09-03, issue
> ALI-211) : les deux points soumis ont été confirmés — (1) inputs (keywords définitifs tels
> qu'en données, scope par défaut `stack-update`) **OK**, (2) **acceptation de l'ADR**. L'invariant
> est respecté (aucun ADR accepté sans validation humaine granulaire). Cet ADR **ne modifie aucune
> posture de sécurité** ni **aucune surface d'exécution** : les 7 fichiers de scope Homelab et le
> champ `scopes:` des 26 fiches de stage portaient déjà, dès leur production (ALI-202 → ADR-0014
> pour l'identité des scopes, ALI-207 → ADR-0018 pour la transposition sur les stages), la forme
> déclarative visée. Ce stage **vérifie** la conformité de façon outillée, **ne corrige aucune
> incohérence** (aucune trouvée) et **trace** les divergences assumées.

## Contexte

Le harness Homelab (dépôt `homelab-portfolio`, répertoire `homelab/`) porte **7 scopes**
spécifiques : `new-stack`, `stack-update` *(défaut)*, `config-change`, `security-patch`,
`infra-terraform`, `n8n`, `home-assistant`. Leur **identité** (nom, axes par défaut, mots-clés,
branche autonome) a été formalisée en données au **Stage 2** d'ALI-200 (issue ALI-202, tracée en
[ADR-0014](0014-scopes-homelab-et-axes-depth-verification.md)), en miroir de `core/scopes/`.

Le **Stage 3** de l'alignement AI-DLC du harness Homelab (issue **ALI-211**, parente ALI-208)
porte ces scopes sur le contrat **« un fichier par scope »** du *Harness Engineer Guide*
(`awslabs/aidlc-workflows`). C'est l'**équivalent Homelab** du travail fait pour le harness `core`
(issue ALI-196, tracée en [ADR-0010](0010-scopes-fichiers-par-scope-et-axes-review-cap.md)).

Le contrat comporte **deux moitiés** ([`homelab/scopes/README.md`](../homelab/scopes/README.md)) :

1. **L'identité** vit dans un fichier par scope — `homelab/scopes/<name>.md` — portant le
   front-matter `name` / `depth` / `verification` / (`branch`) / `keywords` / `description`.
2. **L'appartenance** (quels stages s'exécutent sous un scope) vit **transposée** sur le champ
   `scopes:` de chaque fiche de stage `homelab/common/stages/<phase>/<slug>.md` — déclarée **une
   seule fois, sur le stage**, jamais redéclarée dans sept blocs de scope.

**Constat d'entrée (particularité de ce stage)** : les 7 fichiers de scope existent déjà avec un
front-matter conforme (produits en ALI-202), et le champ `scopes:` est déjà transposé sur les
**26 fiches de stage** (produites en ALI-207). Le travail de ce stage est donc principalement de
**vérifier** la cohérence scope↔stage de façon systématique et **tracer les divergences
assumées** — pas de créer des fichiers manquants.

Contrainte de cadrage (ALI-208 / [ADR-0013](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)) :
adapter au moteur A2A **Multica**, sans importer le tooling amont non applicable (`scope-grid.json`,
moteur TypeScript, champs `runner` / `freeform_default`). Aucune régression sur les garde-fous
absolus du Homelab (règle absolue n8n, règle de départage).

## Décision

**Vérifier et confirmer l'alignement des 7 scopes Homelab et de leur appartenance transposée sur
les 26 fiches de stage sur le contrat « un fichier par scope »**, en traçant les divergences
maison assumées plutôt qu'en important le tooling amont.

### 1. Identité des scopes — conformité vérifiée

Les **7 fichiers** `homelab/scopes/<name>.md` portent un front-matter conforme au schéma
([`homelab/scopes/README.md`](../homelab/scopes/README.md)) :

- `name` = stem du fichier pour les 7 (vérifié programmatiquement) ;
- `depth` ∈ {`minimal`, `standard`, `comprehensive`} ; `verification` ∈ {`advisory`, `standard`,
  `renforcé`} — toutes valeurs valides ;
- `branch: autonome` présent sur `n8n` et `home-assistant` (les deux seules branches autonomes) ;
- `keywords` (FR / EN) et `description` renseignés sur les 7.

**Plancher sécurité non abaissable vérifié** : `new-stack` et `security-patch` portent bien
`depth: comprehensive` + `verification: renforcé`.

### 2. Appartenance transposée — cohérence scope↔stage vérifiée

Le champ `scopes:` des **26 fiches de stage** est croisé avec la matrice scope × phase de
[`homelab/common/protocols/scopes-and-axes.md`](../homelab/common/protocols/scopes-and-axes.md)
(présent = ✅/➖/🔒 ; absent = ❌/⏭). Résultat : **26/26 fiches conformes à la matrice**, aucun
scope orphelin, aucun doublon. Points clés confirmés :

- **Initialisation** (4 stages : `stack-detection`, `concurrency-lock-read`, `labels-audit-init`,
  `deployment-prereqs-precheck`) → **tous les 7 scopes** (ils s'exécutent toujours).
- **Branches autonomes** : `n8n-branch` → `[n8n]` uniquement ; `home-assistant-branch` →
  `[home-assistant]` uniquement. Les stages du flux stack (Idéation / Cadrage / Production hors
  branches) **ne nomment pas** `n8n` / `home-assistant` (marqueur ⏭ de la matrice — court-circuit
  amont), à l'exception des stages transverses qui nomment les 7 (Initialisation, `n8n-absolute-rule`,
  `central-quality-control`, gates de Validation).
- **Scope par défaut `stack-update`** présent dans toutes les fiches du flux stack (hors branches
  pures) — aucune régression du parcours Homelab historique.
- Deux fiches d'Idéation ont une appartenance **plus resserrée que la ligne générique « Idéation »**
  de la matrice, et c'est **cohérent** :
  - `feasibility-arbitration` → `[stack-update, new-stack, security-patch, infra-terraform]`
    (exclut `config-change` : un simple changement de variable ne déclenche pas d'arbitrage
    faisabilité / Swarm-Proxmox — aligné sur la ligne `swarm-proxmox-arbitration` de la matrice) ;
  - `auth-preselection` (CONDITIONAL) → `[stack-update, new-stack, security-patch]` (l'auth est
    sécurité-sensible : exclut `config-change` — sans impact sécurité par définition — et
    `infra-terraform` — infra Proxmox, pas d'auth applicative).

### 3. Règle de départage et règle absolue n8n — préservées

- **Règle de départage** (« le niveau le plus élevé l'emporte », « le doute ne bascule jamais vers
  `config-change` / l'allégé ») : préservée telle quelle dans
  [`homelab/scopes/README.md`](../homelab/scopes/README.md) et
  [`scopes-and-axes.md`](../homelab/common/protocols/scopes-and-axes.md). Ordre de priorité :
  `n8n` = `home-assistant` > `security-patch` > `new-stack` > `infra-terraform` > `stack-update`
  > `config-change`. Chaque scope à plancher (`security-patch`, `new-stack`, `infra-terraform`)
  porte en prose la règle d'escalade « le doute ne descend jamais ».
- **Règle absolue n8n (§1.1)** : préservée. Le scope `n8n` (`branch: autonome`, `keywords: [n8n]`)
  déclenche la délégation immédiate à l'Expert N8n ; le stage `n8n-absolute-rule` nomme les 7
  scopes (il s'exécute toujours, en premier) et `n8n-branch` est le seul stage sous `[n8n]`.

### 4. Réponses aux inputs requis de l'issue

- **Keywords définitifs par scope** — confirmés tels que portés en données dans le champ
  `keywords:` de chaque fichier (source d'identité, validés en ALI-202) : `new-stack` (création /
  nouvelle stack / new stack…), `stack-update` (modification / mise à jour / update…),
  `config-change` (variable / valeur / paramètre existant…), `security-patch` (sécurité / auth /
  secret / hardening / Traefik / CVE…), `infra-terraform` (terraform / proxmox / tfvars / VM /
  LXC…), `n8n` (`n8n`), `home-assistant` (home assistant / HA / entité / scène / automatisation…).
  Aucune modification de mots-clés à ce stage.
- **Scope par défaut confirmé** — **`stack-update`**, en l'absence de mot-clé détecté (déclaré en
  prose dans `stack-update.md` et le README ; le doute ne bascule jamais vers `config-change`).

### 5. Aucune correction nécessaire

Contrairement au Stage 2 (correction unique de `central-quality-control`), la vérification
scope↔stage n'a révélé **aucune incohérence** : identité conforme, appartenance conforme à la
matrice, invariants préservés. **Aucun fichier modifié** au titre de ce stage.

## Conséquences

### Positives

- **POS-001** : Les 7 scopes Homelab et leur appartenance transposée sur les 26 fiches de stage
  **confirmés conformes** au contrat « un fichier par scope », vérification **outillée et
  reproductible**.
- **POS-002** : Cohérence scope↔stage **vérifiée sans orphelin ni doublon** ; l'appartenance est
  déclarée une seule fois (sur le stage), sans redéclaration dans des blocs de scope.
- **POS-003** : Réponses explicites aux deux inputs de l'issue (keywords définitifs ; défaut
  `stack-update`), tracées comme décisions.
- **POS-004** : Règle de départage et règle absolue n8n **confirmées préservées** en données et en
  prose ; plancher sécurité (`new-stack` / `security-patch`) vérifié non abaissé.

### Négatives

- **NEG-001** : La matrice de [`scopes-and-axes.md`](../homelab/common/protocols/scopes-and-axes.md)
  reste une **vue lisible** dupliquant l'appartenance portée par le champ `scopes:` des stages :
  double maintenance à la main (le champ `scopes:` du stage fait foi ; la matrice est la vue).
- **NEG-002** : La vérification de cohérence reste **advisory** (script de contrôle local, pas de
  compilation `scope-grid.json` — non applicable Multica) ; elle dépend du script, non d'un moteur
  runtime.

## Alternatives étudiées

### ALT-001 — Redéclarer l'appartenance dans chaque fichier de scope (bloc `stages:`)

**Raison du rejet** : dupliquerait l'appartenance en sept endroits, à re-synchroniser à chaque
évolution de stage. Le contrat AI-DLC porte l'appartenance **sur le stage** (`scopes:`), déclarée
une seule fois ; c'est la forme retenue et déjà en place.

### ALT-002 — Aligner strictement les stages d'Idéation sur la ligne générique « Idéation » de la matrice

**Raison du rejet** : `feasibility-arbitration` et `auth-preselection` ont une appartenance
**volontairement plus resserrée** (justifiée : faisabilité/arbitrage inutile pour un
`config-change` ; auth sécurité-sensible et hors `infra-terraform`). L'aplatir introduirait des
étapes sans valeur et contredirait la ligne fine de la matrice (`swarm-proxmox-arbitration`).

### ALT-003 — Importer le tooling amont (`scope-grid.json`, moteur TypeScript)

**Raison du rejet** : non applicable — l'exécution passe par Multica (mentions UUID,
`trigger_outcomes`, statut d'issue, verrou metadata, piste d'audit). On adopte la seule forme
déclarative (cohérent avec ADR-0013 et ADR-0014).

## Notes d'implémentation

- **IMP-001** : **7 fichiers** `homelab/scopes/<name>.md` vérifiés — `name` = stem, `depth` /
  `verification` dans les ensembles AI-DLC, `branch: autonome` sur `n8n` / `home-assistant`,
  plancher `comprehensive`/`renforcé` sur `new-stack` / `security-patch`.
- **IMP-002** : **26 fiches de stage** vérifiées — champ `scopes:` sans scope inconnu ni doublon,
  conforme à la matrice scope × phase, défaut `stack-update` présent hors branches pures,
  Initialisation = 7 scopes, branches autonomes isolées.
- **IMP-003** : Vérification **outillée et reproductible** via un script de contrôle (parsing
  front-matter des scopes + comparaison du champ `scopes:` des stages à la matrice de référence +
  invariants). Résultat final : **0 erreur, 0 avertissement**. Script de vérification local (non
  versionné ; reproductible à la vérification globale ALI-214).
- **IMP-004** : **Aucun fichier de scope ni de stage modifié** — la conformité étant vérifiée, ce
  stage ne produit qu'une trace de décision (le présent ADR) et la mise à jour des pointeurs
  d'index. Aucune régression.
- **IMP-005** : Numérotation — le présent ADR est **0021** (suivant le dernier numéro utilisé,
  `0020`, attribué à deux ADR déjà fusionnés sur `main` :
  `0020-alignement-fiches-de-stage-homelab-sur-ai-dlc.md` (ALI-210) et
  `0020-retrait-temporaire-saml-ldap-authentification.md`. Cette **collision 0020 pré-existante**
  n'est pas traitée ici — à consolider à la vérification globale ALI-214). Pointeurs `README.md`
  et `AGENTS.md` mis à jour vers `0001…0021`.
- **IMP-006** : Contrôle sécurité — cet ADR **ne déplace aucune fonction de verdict** ni surface
  d'exécution : plancher sécurité `new-stack` / `security-patch` inchangé, sensors sécurité
  bloquants inchangés, règle absolue n8n et validation humaine granulaire préservées. Le passage à
  *Accepted* requiert la validation humaine granulaire (invariant).

## Références

- **REF-001** : Issue ALI-211 (Stage 3 — Scopes Homelab : un fichier par scope, appartenance
  transposée) ; issue parente ALI-208.
- **REF-002** : [ADR-0014 - Scopes Homelab et axes Depth / Stratégie de vérification](0014-scopes-homelab-et-axes-depth-verification.md) (identité des 7 scopes, ALI-202).
- **REF-003** : [ADR-0010 - Scopes : un fichier par scope et axes / review_cap (core)](0010-scopes-fichiers-par-scope-et-axes-review-cap.md) (équivalent `core`, ALI-196).
- **REF-004** : [ADR-0018 - Adaptation du modèle conductor/stages/protocols au Homelab](0018-adaptation-modele-conductor-stages-protocols-homelab.md) (transposition `scopes:` sur les stages, ALI-207).
- **REF-005** : [ADR-0020 - Alignement des fiches de stage Homelab sur AI-DLC](0020-alignement-fiches-de-stage-homelab-sur-ai-dlc.md) (Stage 2 précédent, ALI-210).
- **REF-006** : [`homelab/scopes/README.md`](../homelab/scopes/README.md) et [`homelab/common/protocols/scopes-and-axes.md`](../homelab/common/protocols/scopes-and-axes.md) — schéma de front-matter, axes, désambiguïsation, matrice scope × phase.
- **REF-007** : [AI-DLC — Harness Engineer Guide (awslabs), core/scopes](https://github.com/awslabs/aidlc-workflows/tree/main/core/scopes)
