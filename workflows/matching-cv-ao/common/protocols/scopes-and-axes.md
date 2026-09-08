# Protocole — scopes & axes d'exécution

Table partagée référencée par le [`conductor.md`](../conductor.md) et les fiches de stage. Le routage repose sur un **scope** nommé (parcours d'étapes déterministe et auditable) et un **axe** — **Depth** (détail des artefacts).

> **Source d'identité vs vue lisible.** L'**identité** de chaque scope est portée en données, **un fichier par scope**, sous [`../../scopes/`](../../scopes/). Ce document reste la **vue lisible** consolidée.

## Table des scopes

| Scope | Intention type | Traitement |
| --- | --- | --- |
| [`standard`](../../scopes/standard.md) *(défaut)* | AO de complexité moyenne | Parcours standard complet |
| [`complex`](../../scopes/complex.md) | AO multi-profils, exigences nombreuses | Parcours complet + approfondissement |
| [`express`](../../scopes/express.md) | AO simple, 1-2 profils | Chemin court, allégé |

Défaut : `standard`. **Invariants non négociables quel que soit le scope** : validation humaine granulaire, piste d'audit, communication JSON↔Markdown.

## Auto-détection & désambiguïsation

Scope auto-détecté par mots-clés (FR / EN) puis **confirmé explicitement** avant démarrage. Les mots-clés déclencheurs sont **déclarés en données** dans le champ `keywords:` de chaque fichier [`../../scopes/<name>.md`](../../scopes/). Ordre de priorité en cas de correspondances multiples :

`complex` > `express` > `standard`

## Axe — Depth

- **Depth** : `minimal` / `standard` / `comprehensive` (détail des artefacts).

| Scope | Depth défaut |
| --- | --- |
| `standard` | standard |
| `complex` | comprehensive |
| `express` | minimal |

## Matrice stage × scope

Légende : ✅ activé · ➖ allégé / optionnel · ❌ ignoré.

| Stage | `standard` | `complex` | `express` |
| --- | --- | --- | --- |
| Initialisation (0.x) | ✅ | ✅ | ✅ |
| Analyse (1.x) | ✅ | ✅ | ✅ |
| Matching (2.x) | ✅ | ✅ 🔒 | ➖ |
| Validation (3.x) | ✅ | ✅ | ✅ |
| Clôture (4.x) | ✅ | ✅ | ✅ |
| Validation humaine granulaire | ✅ | ✅ | ✅ |

Aucun scope ne désactive la validation humaine granulaire, la piste d'audit ou la communication JSON↔Markdown (invariants).
