# Protocole — scopes & axes d'exécution

Table partagée référencée par le [`conductor.md`](../conductor.md) et les fiches de stage. Le routage repose sur un **scope** nommé (parcours d'étapes déterministe et auditable) et deux **axes indépendants** — **Depth** (détail des artefacts) et **niveau de vérification** (rigueur du contrôle).

> **Source d'identité vs vue lisible.** L'**identité** de chaque scope (nom, `depth`, `keywords`, niveau de vérification → `review_cap`, `skeleton`) est portée en données, **un fichier par scope**, sous [`../../scopes/`](../../scopes/) (contrat AI-DLC « Scopes »). Ce document reste la **vue lisible** consolidée — table des scopes, axes, ordre de désambiguïsation, matrice stage × scope. **En cas d'écart sur l'identité d'un scope, le fichier `core/scopes/<name>.md` fait foi.** L'appartenance (quels stages tournent sous un scope) reste transposée sur le champ `scopes:` des fiches de stage.

## Table des scopes

| Scope | Intention type | Traitement |
| --- | --- | --- |
| [`standard`](../../scopes/standard.md) *(défaut)* | Conception / évolution d'architecture « normale » | Parcours standard complet |
| [`feature`](../../scopes/feature.md) | Ajout / évolution fonctionnelle | Inception ciblée + Construction, sécurité systématique |
| [`infra`](../../scopes/infra.md) | Infra / plateforme (AWS, réseau, Windows, migration) | Accent Architecte AWS / Administrateur infrastructure Windows, rollback obligatoire |
| [`security-patch`](../../scopes/security-patch.md) | Correction / durcissement de sécurité | **Architecte cybersécurité pilote**, périmètre resserré, traçabilité renforcée |
| [`mvp`](../../scopes/mvp.md) | Produit minimum viable | Cœur de valeur, Depth standard, dette technique tracée |
| [`poc`](../../scopes/poc.md) | Preuve de concept jetable | Allégé, Depth minimale, non promouvable tel quel |
| [`express`](../../scopes/express.md) | Petit changement clair, faible risque | Chemin court ; lourd ignoré (sauf action à impact) |
| [`enterprise`](../../scopes/enterprise.md) | Chantier structurant, fort impact / conformité | Complet + Depth comprehensive + normes conditionnelles |

Défaut : `standard`. **Invariants non négociables quel que soit le scope** (aucun scope ne les désactive) : validation humaine granulaire, décision structurante tracée, piste d'audit, contrôle sécurité minimal (OWASP / STRIDE).

## Auto-détection & désambiguïsation

Scope auto-détecté par mots-clés (FR / EN) puis **confirmé explicitement** avant démarrage (jamais de démarrage silencieux). Les mots-clés déclencheurs sont **déclarés en données** dans le champ `keywords:` de chaque fichier [`../../scopes/<name>.md`](../../scopes/) (source d'identité). Ordre de priorité en cas de correspondances multiples :

`security-patch` > `enterprise` > `infra` > `feature` > `mvp` > `poc` > `express` > `standard`

## Axes

- **Axe 1 — Depth** : `minimal` / `standard` / `comprehensive` (détail des artefacts).
- **Axe 2 — Vérification** : `advisory` / `standard` / `renforcé` (rigueur du contrôle ; remplace l'axe « test strategy » pour la documentation, mais **inclut une stratégie de tests dès qu'il y a du code / IaC**).

Les valeurs par défaut ci-dessous sont la **projection lisible** des champs `depth` / `verification` (→ `review_cap`) des fichiers de scope. **Le fichier `core/scopes/<name>.md` fait foi.**

| Scope | Depth défaut | Vérification défaut | `review_cap` (AI-DLC) |
| --- | --- | --- | --- |
| `standard` | standard | standard | *(absent)* |
| `feature` | standard | standard | *(absent)* |
| `infra` | standard | renforcé | *(absent)* |
| `security-patch` | standard | renforcé | *(absent — jamais abaissé)* |
| `mvp` | standard | standard | *(absent)* |
| `poc` | minimal | advisory | `advisory` |
| `express` | minimal | standard | `advisory` |
| `enterprise` | comprehensive | renforcé | *(absent — jamais abaissé)* |

**Mapping vérification → `review_cap`** : `advisory` → `advisory` ; `standard` / `renforcé` → *(absent, pas d'abaissement)*. Un `review_cap` abaisse la `review_class` d'un stage mais ne la relève jamais.

**Points d'override** : à l'invocation, à la confirmation de scope, ou à un gate (relever seulement). **Garde-fou sécurité** : un niveau lié à la sécurité ne peut jamais être abaissé ; sur `security-patch` / `enterprise`, Depth ≥ `standard` et vérification ≥ `renforcé` ; tout re-scoping abaissant le contrôle exige une validation humaine tracée (voir [`governance-security.md`](governance-security.md)).

## Matrice stage × scope

Légende : ✅ activé · ➖ allégé / optionnel · ❌ ignoré · 🔒 renforcé · *cond.* conditionnel. Stages nommés par leur slug (voir [`../stages/`](../stages/)).

| Stage | `standard` | `feature` | `infra` | `security-patch` | `mvp` | `poc` | `express` | `enterprise` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initialization (0.x) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ideation (1.x) | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ✅ |
| `intake-framing` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `existing-context-loading` | ➖ | ✅ | ✅ | ✅ | ➖ | ❌ | ➖ | ✅ |
| `requirements-analysis` | ✅ | ✅ | ✅ | ✅ 🔒 | ✅ | ➖ | ➖ | ✅ 🔒 |
| `deliverables-breakdown` | ✅ | ✅ | ✅ | ➖ | ✅ | ➖ | ➖ | ✅ |
| `design-and-decisions` | ✅ | ✅ | ✅ | ✅ 🔒 | ✅ | ➖ | ➖ | ✅ 🔒 |
| Revue de sécurité (Reviewer de sécurité) | ✅ | ✅ | ✅ | 🔒 pilote | ✅ | ➖ [^poc-sec] | ➖ | ✅ 🔒 |
| `detailed-deliverables` | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ✅ |
| `security-consistency-check` | ✅ | ✅ | ✅ | 🔒 | ✅ | ➖ | ➖ | ✅ 🔒 |
| `consolidation-handoff` | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ✅ | ✅ |
| Operation (4.x) | *cond.* | *cond.* | ✅ | *cond.* | *cond.* | ❌ | *cond.* | ✅ |
| Validation humaine granulaire | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

[^poc-sec]: `poc` — `➖` ne signifie **jamais** un contrôle sécurité nul : le **plancher OWASP / STRIDE reste actif** (invariant non désactivable par aucun scope). Seules la **profondeur** de l'analyse et la **rigueur de vérification** sont allégées, cohérent avec le caractère jetable du PoC. Un PoC est **non promouvable tel quel** : toute reprise en `feature` / `mvp` / `enterprise` **re-déclenche le contrôle sécurité complet** du scope cible (voir [`governance-security.md`](governance-security.md), garde-fous des scopes).

Affectation des agents par scope, renforcements sécurité (`security-patch` analyse d'impact, `enterprise` normes tracées, `express` pas d'allègement sur impact, `poc` non promouvable) : voir [`governance-security.md`](governance-security.md).
