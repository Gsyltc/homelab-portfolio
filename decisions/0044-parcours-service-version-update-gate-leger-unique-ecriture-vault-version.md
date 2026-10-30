# Parcours `service-version-update` : gate léger unique (A1) couvrant écriture Vault `VERSION` + déploiement Kestra, et exception d'écriture Vault étroite

---
auteurs: Mika (agent)
accepté par : sylvain.rodgers
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** — en attente de validation humaine granulaire explicite (sylvain.rodgers) en revue de PR. Au passage *Proposed → Accepted*, renseigner `accepté le`. Pas de merge autonome sur `main`. Ce changement est **documentaire** (contrat `homelab/common/`, scopes, skill `homelab-vault-access`) : les invariants de gouvernance-sécurité restent **préservés à l'identique** (voir § Conséquences / POS-005).

## Contexte

Le Homelab dispose déjà de l'amorce d'un flux de mise à jour de service sur nouvelle version :

- **Autopilot `Service Update Webhook - DevOps`** (id `e207439d-ca28-4bd9-8379-1cceb10ee409`) : sur réception d'un webhook `{service, version, github}`, il détecte le type de service (Docker Swarm vs Proxmox), lit la version actuelle dans Vault (clé `VERSION`, lecture seule), analyse la page Release GitHub, détecte les breaking changes, crée l'issue d'analyse en `backlog` et la passe `blocked` en cas de breaking change. **Il n'exécute jamais la mise à jour** — c'est le **point d'entrée** d'analyse, pas l'exécutant.
- **HOM-262** (« Mise à jour du service traefik : version 3.8.0 ») : exemple d'analyse d'impact réussie (détection d'une version RC / non stable, recommandation d'une version stable, source GitHub Release). C'est le **standard de qualité attendu** pour l'analyse d'impact.

Jusqu'ici, ce flux n'était **pas** porté par le contrat vivant du workflow Homelab (`homelab/common/`) : aucun **scope** ne le nommait, aucune **fiche de stage** ne décrivait l'analyse d'impact de version ni l'application gardée de la mise à jour, et la skill `homelab-vault-access` était en **lecture seule** — alors que l'application d'une montée de version suppose d'écrire la clé `VERSION` dans Vault. Deux décisions de conception devaient être tranchées et tracées :

1. **Combien de gates humains** entre une analyse OK et le service effectivement déployé ? Un enchaînement naïf aurait multiplié les validations (une pour Vault, une pour Kestra), alourdissant un parcours pourtant simple quand l'analyse ne révèle **aucun** enjeu.
2. **Jusqu'où ouvrir l'écriture Vault** sans éroder le principe « lecture seule » qui protège les secrets du Homelab ?

L'humain (sylvain.rodgers) a tranché ces deux points (décisions A1 et B ci-dessous), avec ADR à l'appui.

## Décision

**Ajouter au workflow Homelab un parcours `service-version-update`** porté par le contrat vivant, en quatre volets.

1. **Nouveau scope `service-version-update`** ([`homelab/scopes/service-version-update.md`](../homelab/scopes/service-version-update.md)) : Depth `standard`, vérification `standard`, mots-clés FR/EN (« nouvelle version », « mise à jour version », « bump », « release », « update version »…). Spécialisation ciblée de `stack-update` pour « un service existant, une nouvelle version disponible ». Inséré dans l'**ordre de désambiguïsation** (`homelab/scopes/README.md` et [`homelab/common/protocols/scopes-and-axes.md`](../homelab/common/protocols/scopes-and-axes.md)) : `… > infra-terraform > service-version-update > stack-update > config-change`. **Report de priorité préservé** : si la montée de version a un impact sécurité, `security-patch` **l'emporte** (plancher `comprehensive` / `renforcé`, sensors sécurité bloquants).

2. **Décision A1 — gate humain léger unique.** Après une analyse d'impact **OK** (aucun breaking change, aucun enjeu de configuration), un **seul** point de validation **léger** (`human_gate: light`). Sur acceptation, l'**écriture Vault de `VERSION`** **ET** le **déploiement Kestra** sont **tous deux autorisés en une seule étape** — pas d'aller-retour, pas de double validation. Matérialisée par deux fiches de stage :
   - [`version-impact-analysis`](../homelab/common/stages/ideation/version-impact-analysis.md) (phase Idéation, `human_gate: none`) : reprend la logique autopilot / HOM-262 ; produit `analyse_impact_version` ; **`blocked`** si enjeu ; report de priorité `security-patch` si impact sécurité.
   - [`version-update-application`](../homelab/common/stages/validation/version-update-application.md) (phase Validation, `human_gate: light`) : **porte le gate léger unique A1** ; sur acceptation, écrit `VERSION` dans Vault puis enchaîne le déploiement sans nouvelle validation ; produit `version_ecrite_vault` et `depot_fichiers_confirme`.
   - [`kestra-deployment`](../homelab/common/stages/validation/kestra-deployment.md) **étendu proprement** : scope `service-version-update` ajouté ; `requires_stage` devient `[file-deposit, version-update-application]`, les deux voies étant **mutuellement exclusives par scope** (clarifié dans le corps, Step 3) ; le `consumes` `depot_fichiers_confirme` est inchangé — il est désormais produit soit par `file-deposit` (parcours standard), soit par `version-update-application` (ce parcours). Aucune régression pour les autres scopes.

3. **Décision B — exception d'écriture Vault étroite.** La skill [`homelab-vault-access`](../plugins/homelab-assistant/skills/homelab-vault-access/SKILL.md) reste en **lecture seule** sauf pour ce parcours, et uniquement pour écrire la clé **`VERSION`** du montage `env_variables/data/<service>`. **Jamais** un secret du montage `services/`, jamais une autre clé. Nouvelle **Étape 3** (écriture encadrée) : pattern **read-modify-write** préservant toutes les autres clés, corps POST via stdin, vérification sans divulgation, token révoqué en fin. La valeur n'est jamais affichée, loggée ni transmise ; l'écriture est **tracée sur l'issue** (nom de clé `VERSION` + statut seulement). `description` du front-matter de la skill mise à jour ; **règle de sécurité ABSOLUE n° 7** ajoutée (écriture = exception unique, gardée par A1).

4. **Vues et traçabilité.** [`conductor.md`](../homelab/common/conductor.md) : table des 5 phases enrichie (`version-impact-analysis` en Idéation, `version-update-application` en Validation) et **note concise** pointant vers le fichier de scope (source d'identité) et vers le présent ADR — la narration détaillée et le diagramme Mermaid vivent dans le **fichier de scope** [`service-version-update.md`](../homelab/scopes/service-version-update.md), pas dans le conductor (qui reste léger). [`scopes-and-axes.md`](../homelab/common/protocols/scopes-and-axes.md) : table des scopes, ordre de désambiguïsation, table des axes et **matrice stage × scope** (nouvelle colonne `service-version-update` + lignes `version-impact-analysis`, `version-update-application`, `kestra-deployment`). Compteurs « 7 scopes » → « 8 scopes » propagés (stage-definition, rules/README, conductor). Bump `homelab-assistant` `1.0.0` → `1.1.0` + entrée CHANGELOG + ligne du mapping README mise à jour.

## Conséquences

### Positives

- **POS-001** : le flux déjà éprouvé par l'autopilot et HOM-262 est désormais **porté par le contrat vivant** (scope + stages + skill), auditable et routable comme les autres parcours.
- **POS-002** : le **gate léger unique A1** évite la double validation (Vault puis Kestra) sur un parcours simple, tout en préservant l'invariant « aucune action à impact sans validation humaine » (une acceptation **explicite** reste requise ; rien n'est autonome).
- **POS-003** : l'**analyse d'impact** bloque (`blocked`) tôt, en Idéation, sur breaking change / version non stable / migration — le standard HOM-262 est inscrit dans la fiche de stage.
- **POS-004** : l'**exception d'écriture Vault** est **étroite et explicite** (une clé, un montage, un parcours, un gate) — elle n'érode pas le principe de lecture seule pour le reste du workflow.
- **POS-005** : aucun invariant de [`governance-security.md`](../homelab/common/protocols/governance-security.md) modifié — Terraform ne déploie jamais, aucun secret en clair, jamais `${SNI}` dans un livrable Terraform, un seul traitement par artefact, piste d'audit sur l'issue, priorité `security-patch` préservée.

### Négatives

- **NEG-001** : `kestra-deployment.requires_stage` liste désormais **deux** slugs (`file-deposit`, `version-update-application`) exclusifs par scope. Une lecture purement mécanique du graphe (contrôle `absence-orphelin`) pourrait les croire **cumulatifs** ; l'exclusivité est explicitée dans le corps du stage (Step 3). Atténuation : les deux producteurs émettent le **même** artefact `depot_fichiers_confirme`, de sorte que le `consumes` requis reste satisfait quel que soit le scope actif.
- **NEG-002** : la skill `homelab-vault-access` n'est plus strictement « lecture seule ». Le périmètre d'écriture est réduit à l'extrême (clé `VERSION`, montage `env_variables`, gate A1) et une règle ABSOLUE dédiée l'encadre, mais la **policy AppRole** doit accorder la capability d'écriture sur `env_variables/data/<service>` pour que le temps 2 fonctionne — à provisionner par le propriétaire du workspace (hors périmètre documentaire).
- **NEG-003** : le parcours réutilise le **fichier Terraform existant** du service sans le régénérer ; si ce fichier est obsolète ou absent, le déploiement Kestra échouera. L'analyse d'impact doit donc vérifier l'existence du Terraform du service ; sinon, remonter à l'humain (jamais de supposition).

## Alternatives étudiées

### ALT-001 — Deux gates humains distincts (Vault, puis Kestra)

Demander une validation pour l'écriture Vault, **puis** une seconde pour le déploiement Kestra.

**Raison du rejet** : sur un parcours dont l'analyse d'impact a déjà statué « aucun enjeu », deux gates alourdissent sans valeur ajoutée (l'humain revalide une décision déjà prise). La décision A1 d'un **gate léger unique** couvrant les deux actions a été explicitement retenue par l'humain : une seule acceptation, pas d'aller-retour.

### ALT-002 — Réutiliser le scope `stack-update` sans scope dédié

Traiter la montée de version comme un `stack-update` ordinaire, sans nouveau scope ni nouvelles fiches de stage.

**Raison du rejet** : `stack-update` déclenche le parcours complet de production d'artefacts (compose, Terraform, QA) alors qu'une montée de version réutilise le Terraform **existant** et n'a besoin ni de génération de compose, ni de QA de stack. Un scope ciblé rend le parcours lisible, allège les étapes inutiles (matrice stage × scope), et permet d'y rattacher l'analyse d'impact de version et l'exception d'écriture Vault **sans** affecter `stack-update`.

### ALT-003 — Ouvrir l'écriture Vault largement (toutes clés `env_variables`)

Autoriser l'écriture de n'importe quelle clé du montage `env_variables/` pour cette skill.

**Raison du rejet** : surface d'écriture bien trop large pour le besoin (seule `VERSION` change lors d'une montée de version). La décision B retient une exception **étroite** — une clé, un montage, un parcours, un gate — qui préserve au maximum le principe de lecture seule et limite le rayon d'action en cas d'erreur.

## Notes d'implémentation

- **IMP-001** : scope [`service-version-update.md`](../homelab/scopes/service-version-update.md) créé ; inséré dans l'ordre de désambiguïsation et les tables de [`homelab/scopes/README.md`](../homelab/scopes/README.md) et [`scopes-and-axes.md`](../homelab/common/protocols/scopes-and-axes.md).
- **IMP-002** : fiches de stage [`version-impact-analysis.md`](../homelab/common/stages/ideation/version-impact-analysis.md) (Idéation, `human_gate: none`, `blocked` si enjeu) et [`version-update-application.md`](../homelab/common/stages/validation/version-update-application.md) (Validation, `human_gate: light` = gate A1, sensor `vault-secret-exists`) créées, front-matters conformes à [`stage-definition.md`](../homelab/common/protocols/stage-definition.md).
- **IMP-003** : [`kestra-deployment.md`](../homelab/common/stages/validation/kestra-deployment.md) étendu (scope + `requires_stage` + `condition` + Step 3 d'exclusivité).
- **IMP-004** : matrice stage × scope de `scopes-and-axes.md` : colonne `service-version-update` + lignes `version-impact-analysis` / `version-update-application` / `kestra-deployment` + note de lecture du parcours.
- **IMP-005** : skill [`homelab-vault-access/SKILL.md`](../plugins/homelab-assistant/skills/homelab-vault-access/SKILL.md) : Étape 3 d'écriture encadrée, `description` front-matter, règle ABSOLUE n° 7 ; `plugin.json` `1.0.0` → `1.1.0` ; entrée `CHANGELOG.md` ; ligne mapping `README.md`.
- **IMP-006** : [`conductor.md`](../homelab/common/conductor.md) : table des phases + note concise de renvoi vers le fichier de scope et l'ADR (pas de narration ni de diagramme dans le conductor), compteurs de scopes (7 → 8) propagés ; le diagramme Mermaid du parcours vit dans [`service-version-update.md`](../homelab/scopes/service-version-update.md).
- **IMP-007** : validation humaine granulaire à obtenir en revue de PR (passage *Proposed* → *Accepted*, renseigner `accepté le`) ; pas de merge autonome sur `main` ; provisionnement de la policy AppRole d'écriture (NEG-002) à confirmer par le propriétaire du workspace.

## Références

- **REF-001** : autopilot **`Service Update Webhook - DevOps`** (id `e207439d-ca28-4bd9-8379-1cceb10ee409`) — point d'entrée d'analyse du parcours.
- **REF-002** : **HOM-262** (mise à jour Traefik 3.8.0) — standard de qualité de l'analyse d'impact de version.
- **REF-003** : [`homelab/scopes/service-version-update.md`](../homelab/scopes/service-version-update.md) — identité du nouveau scope.
- **REF-004** : [`homelab/common/stages/validation/version-update-application.md`](../homelab/common/stages/validation/version-update-application.md) — stage portant le gate léger unique A1.
- **REF-005** : [`plugins/homelab-assistant/skills/homelab-vault-access/SKILL.md`](../plugins/homelab-assistant/skills/homelab-vault-access/SKILL.md) — exception d'écriture Vault étroite (clé `VERSION`).
- **REF-006** : [ADR-0016 — Verification gates et sensors (Homelab)](0016-verification-gates-et-sensors-homelab.md) — cadre des gates / sensors dont relève le gate léger A1.
- **REF-007** : [ADR-0017 — Passage à 5 phases et mode autonomie (Homelab)](0017-passage-5-phases-et-mode-autonomie-homelab.md) — structure des 5 phases où s'insèrent les deux nouveaux stages.
