---
name: recherche-repas
description: "Référentiel et mécanique de recherche de recettes pour la planification de repas avec les appareils de cuisine disponibles. Fournit le registre extensible des appareils (un fichier de référence par appareil sous appareils/ : sources, accessoires, livres de recettes, emplacement des recettes), la mécanique de diversification RANDOMISÉE des sources (répartir un lot de plats sur plusieurs sources différentes — ex. 3 plats d'un PDF, 1 d'un site, 1 d'un second site), l'emplacement et le FORMAT des fichiers de données (repas retenus, repas exclus, ingrédients refusés) avec leur front matter de résumé, le format de l'emplacement de recette à conserver, et la mécanique d'extraction des ingrédients pour 4 personnes. Les RÈGLES (composition nutritionnelle, unités, boucle de proposition/validation, lazy loading, validation humaine) sont portées par l'agent qui utilise cette skill. Se déclenche sur : repas, recette, menu, planification de repas, appareil de cuisine, robot cuiseur, Companion, Moulinex, cuisine, courses, ingrédients, plat équilibré, varier les sources, diversifier les recettes."
---

# Recherche de repas — référentiel et mécanique

Cette skill fournit **la mécanique et les référentiels** nécessaires à la recherche de recettes et à la planification de repas : registre des appareils, emplacement et format des fichiers de données, format de l'emplacement de recette, extraction des ingrédients.

## Appareils de cuisine — registre extensible

La skill est **générique** : elle ne connaît aucun appareil « en dur ». Chaque appareil (robot cuiseur, four, friteuse, etc.) est décrit dans son **propre fichier de référence** sous `appareils/`. Ajouter un appareil = ajouter un fichier ; rien d'autre à changer.

```
appareils/
├── README.md                 # gabarit + comment ajouter un appareil
├── <appareil>.md             # 1 fichier de référence par appareil
└── <appareil>/               # (optionnel) livres de recettes embarqués de cet appareil
    └── *.pdf
```

Chaque fichier d'appareil `appareils/<appareil>.md` décrit **au minimum** :

- le **nom** de l'appareil et son identifiant (slug) ;
- les **sources de recettes** (sites, livres embarqués, chemins) ;
- les **accessoires / modes de cuisson** disponibles (contrainte de faisabilité) ;
- l'**emplacement des recettes** (livre + page, URL, fichier) pour que l'humain puisse les réaliser.

### Sélection des appareils (mécanique)

- **Par défaut** : puiser dans **tous** les appareils décrits sous `appareils/`.
- **Si un appareil précis est demandé** (ex. « 5 recettes pour le Companion ») : n'utiliser que les sources et accessoires de **cet appareil**, sans mélange.
- Si l'appareil demandé est absent de `appareils/`, le signaler et proposer de l'ajouter (nouveau fichier) plutôt que d'inventer ses capacités.

### Contrainte de faisabilité

Ne retenir que des recettes réalisables avec les **accessoires / modes réellement listés** dans le fichier de l'appareil retenu. Sinon, écarter la recette ou proposer une adaptation compatible.

### Diversification randomisée des sources (mécanique)

Un appareil expose plusieurs **sources** de recettes (livre PDF embarqué, site officiel n°1, site officiel n°2, …). Pour un lot de `N` suggestions, **ne pas puiser toutes les recettes à la même source** : répartir les `N` plats sur **plusieurs sources différentes**, de façon **aléatoire** (la répartition change d'un lot à l'autre).

Mécanique à appliquer à chaque lot de `N` suggestions :

1. **Construire l'ensemble des sources disponibles** :
   - Par défaut (tous appareils) : réunir les sources de **tous** les appareils de `appareils/` ; chaque source reste identifiée par son appareil (pour la faisabilité et l'emplacement de recette). La diversification porte alors aussi bien sur les **sources** que sur les **appareils**.
   - Si un appareil précis est imposé : réunir uniquement les sources de **cet** appareil (PDF embarqué + ses sites). La diversification porte sur les sources de ce seul appareil.
2. **Tirer une répartition aléatoire** des `N` plats sur les sources disponibles :
   - Viser **au moins 2 sources distinctes** dès que `N ≥ 2` et qu'au moins 2 sources existent. Un plus grand nombre de sources distinctes est bienvenu mais non requis.
   - Autoriser qu'une source fournisse **plusieurs** plats (ex. pour `N = 5` : 3 plats d'un PDF, 1 d'un site, 1 d'un second site), mais **éviter** qu'une seule source fournisse la **totalité** du lot si d'autres sources sont disponibles.
   - La répartition exacte (quelle source fournit combien de plats) est **tirée au hasard** à chaque lot, dans le respect des contraintes ci-dessus.
3. **Respecter les autres règles** pendant le tirage : faisabilité (accessoires de l'appareil de la source), exclusions (`repas-exclus.md`), ingrédients refusés (`ingredients-refuses.md`), historique glissant 30 j, et préférences de protéines portées par l'agent. Si une source ne peut fournir son quota sous ces contraintes, **reporter** le reliquat sur une autre source disponible (sans jamais retomber sur une source unique si l'évitement reste possible).
4. **Tracer la source** de chaque suggestion via l'**emplacement de la recette** (livre + page, URL, ou chemin), comme déjà exigé : l'humain voit ainsi la variété des sources employées.

> Cette diversification est une **mécanique de sélection** : elle n'assouplit aucune règle de faisabilité, d'exclusion ou nutritionnelle. En l'absence d'alternative compatible, mieux vaut une source unique qu'une recette non conforme.

## Emplacement des fichiers de données

Toutes les données persistantes vivent sous `/nfs/workspace/datas/repas/`.

```bash
mkdir -p /nfs/workspace/datas/repas/recettes
```

```
/nfs/workspace/datas/repas/
├── repas-retenus.md        # repas retenus (front matter + tableau) — historique glissant 30 jours, avec emplacement de la recette
├── repas-exclus.md         # repas refusés définitivement
├── ingredients-refuses.md  # ingrédients interdits
└── recettes/               # livres de recettes et recettes individuelles collectés à l'usage
    └── (livres PDF, recettes .md…)
```

> Les livres embarqués avec un appareil (`appareils/<appareil>/`) peuvent être copiés dans `/nfs/workspace/datas/repas/recettes/` au premier usage pour consultation locale.

## Format des fichiers de données (front matter + corps)

Chaque fichier porte un **front matter** servant de résumé lisible en premier. *(L'ordre de lecture — front matter d'abord, corps à la demande — est une règle de l'agent ; ici on décrit seulement le schéma à respecter en écriture.)* Tenir le front matter synchronisé avec le corps à **chaque** écriture.

### `repas-retenus.md`

```markdown
---
type: repas-retenus
updated: 2026-10-17
rolling_window_days: 30
count: 2
oldest: 2026-10-16
newest: 2026-10-17
---

# Repas retenus

| Date       | Repas                     | Appareil             | Emplacement de la recette              |
|------------|---------------------------|----------------------|----------------------------------------|
| 2026-10-17 | Saumon vapeur et riz      | Companion de Moulinex | Companion XL — Recipebook FR, p. 42    |
| 2026-10-16 | Dahl de lentilles corail  | Companion de Moulinex | https://companionetmoi.com/...         |
```

- `count` = nombre d'entrées ; `oldest` / `newest` = bornes de dates ; `rolling_window_days` = fenêtre glissante (30).
- **Purge** (déclenchée par l'agent) : retirer toute ligne de date < aujourd'hui − 30 j, puis réécrire `updated`, `count`, `oldest`, `newest`.

### `repas-exclus.md`

Le front matter ne porte qu'un **résumé** (`type`, `updated`, `count`). La **liste des repas exclus reste dans le corps** (une entrée par ligne) et doit être chargée pour le filtrage dès que `count > 0`.

```markdown
---
type: repas-exclus
updated: 2026-10-17
count: 1
---

# Repas exclus (refus définitifs — ne JAMAIS proposer)

- Blanquette de veau
```

### `ingredients-refuses.md`

Le front matter ne porte qu'un **résumé** (`type`, `updated`, `count`). La **liste des ingrédients refusés reste dans le corps** (une entrée par ligne) et doit être chargée pour le filtrage dès que `count > 0`.

```markdown
---
type: ingredients-refuses
updated: 2026-10-17
count: 1
---

# Ingrédients refusés (ne JAMAIS proposer un plat en contenant)

- Noix de coco
```

## Emplacement de la recette — format à conserver

Pour chaque plat gardé, enregistrer où trouver la recette (dans la suggestion **et** dans `repas-retenus.md`) :

- **Appareil** concerné ;
- **Source précise** :
  - livre → **nom du livre + page/section** (ex. « Companion XL — Recipebook FR, p. 42 ») ;
  - site → **URL** directe de la recette ;
  - fichier → **chemin** (ex. `recettes/<fichier>.md`).

## Extraction des ingrédients (mécanique)

Pour un plat gardé, produire la liste d'achats :

- Conserver uniquement les **ingrédients principaux** et leur **quantité**.
- **Exclure les condiments** : sel, poivre, épices, huile, vinaigre, herbes d'assaisonnement, eau…
- Recalculer les quantités **pour 4 personnes** *(l'équivalence 1 plat = 4 portions est une règle de l'agent)*.

## Garde-fou de données

- `/nfs/workspace/datas/repas/` est la source de vérité : écrire immédiatement après chaque décision et garder chaque front matter synchronisé avec son corps.
- Ne jamais fusionner, pousser ni ouvrir de PR sur le dépôt `homelab-portfolio` sans validation explicite de l'humain.
