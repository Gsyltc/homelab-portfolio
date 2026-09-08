# Protocole — scopes & axes d'exécution

Table partagée référencée par le [`conductor.md`](../conductor.md) et les fiches de stage. Le routage repose sur un **scope** nommé (parcours d'étapes déterministe et auditable) et un **axe** — **Depth** (détail des artefacts).

> **Source d'identité vs vue lisible.** L'**identité** de chaque scope est portée en données, **un fichier par scope**, sous [`../../scopes/`](../../scopes/). Ce document reste la **vue lisible** consolidée.

## Table des scopes

| Scope | Intention type | Traitement |
| --- | --- | --- |
| [`standard`](../../scopes/standard.md) *(défaut)* | AO de complexité moyenne | Parcours standard complet |
| [`complex`](../../scopes/complex.md) | AO multi-profils, exigences nombreuses | Parcours complet + approfondissement |
| [`express`](../../scopes/express.md) | AO simple, 1-2 profils | Chemin court, allégé |
| [`format-cv`](../../scopes/format-cv.md) | Traitement CV seul (sans AO ni matching) | Chargement + extraction/formatage/archivage + mise à jour CV |

Défaut : `standard`. **Invariants non négociables quel que soit le scope** : validation humaine granulaire, piste d'audit, communication JSON↔Markdown.

## Auto-détection & désambiguïsation

Scope auto-détecté par mots-clés (FR / EN) puis **confirmé explicitement** avant démarrage. Les mots-clés déclencheurs sont **déclarés en données** dans le champ `keywords:` de chaque fichier [`../../scopes/<name>.md`](../../scopes/). Ordre de priorité en cas de correspondances multiples :

`complex` > `express` > `standard`

Le scope `format-cv` porte des mots-clés très spécifiques au traitement CV seul
(`format cv`, `formatage cv`, `traitement cv`, `cv only`, `format-cv`…). Lorsqu'un de ces
mots-clés est détecté sans intention d'AO / matching, `format-cv` prime ; en cas de
co-occurrence avec des mots-clés d'AO / matching, l'ordre ci-dessus s'applique et la
confirmation humaine tranche.

## Axe — Depth

- **Depth** : `minimal` / `standard` / `comprehensive` (détail des artefacts).

| Scope | Depth défaut |
| --- | --- |
| `standard` | standard |
| `complex` | comprehensive |
| `express` | minimal |
| `format-cv` | standard |

## Matrice stage × scope

Légende : ✅ activé · ➖ allégé / optionnel · ❌ ignoré.

| Stage | `standard` | `complex` | `express` | `format-cv` |
| --- | --- | --- | --- | --- |
| Initialisation (0.x) | ✅ | ✅ | ✅ | ✅¹ |
| Analyse (1.x) | ✅ | ✅ | ✅ | ✅² |
| Matching (2.x) | ✅ | ✅ 🔒 | ➖ | ❌ |
| Validation (3.x) | ✅ | ✅ | ✅ | ❌ |
| Clôture (4.x) | ✅ | ✅ | ✅ | ✅³ |
| Validation humaine granulaire | ✅ | ✅ | ✅ | ✅ |

Aucun scope ne désactive la validation humaine granulaire, la piste d'audit ou la communication JSON↔Markdown (invariants).

> **Granularité `format-cv` (par stage, pas par phase entière).** Ce scope n'active qu'un stage par phase concernée :
> - ¹ Initialisation : `chargement-cv` ✅ ; `reception-ao` ❌.
> - ² Analyse : `extraction-cv` ✅ (produit la fiche d'analyse Markdown versionnée = archivage/formatage) ; `parse-ao` ❌.
> - ³ Clôture : `mise-a-jour-cv` ✅ ; `livraison` ❌.
>
> Les phases **Matching** (`croisement-profils`, `classement-profils`) et **Validation** (`remplissage-grille`, `presentation-resultats`) sont **entièrement ignorées**. Exactement trois stages déclarent `format-cv` : `chargement-cv`, `extraction-cv`, `mise-a-jour-cv`.
