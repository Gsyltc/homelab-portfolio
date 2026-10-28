# Structurizr C4

## Structure
- Racine : `workspace.dsl`, `models/`, `views/`, `theme/`
- `!include theme/0000-default-styles.dsl`, `theme/0001-project-styles.dsl`, `theme/0002-external-tools.dsl`
- `!include theme/properties.dsl` dans `model`
- Réutiliser le thème du projet

## Syntaxe
- Utiliser `!element` et `!relationship` pour étendre. Ne pas utiliser `!extend`.
- `!element <identifiant> { ... }` permet d'ajouter des enfants à un conteneur/système défini ailleurs.

## Modélisation
- Imbrication composant ↔ conteneur ; scission ; nouveau conteneur porteur
- **Descriptions d'éléments et de liens ≤ 30 caractères.**
- **Aucun code, référence ou numéro dans les libellés rendus** : ni `INV-`, `CT-`, `CTR-SEC-`, `PINV-`, `RAT-`, `PLG-`, `IMP-`, `R-SEC-`, ni `ADR`, ni `DEC`, ni `§`. Uniquement intention métier/technique. Traçabilité hors libellés rendus.
- **Un seul lien par sens entre deux mêmes éléments** (vues statiques conteneur/composant). Consolider en un libellé synthétique. **Exception** : vue dynamique (séquence) peut répéter le même couple en étapes numérotées.
- Lorsqu'un élément ou un flux est **modifié** par une spécification/décision proposée → tag **`modified`**.
- Lorsqu'un élément ou un flux est **supprimé** par une spécification/décision proposée → tag **`deleted`**.
- Tag **`new`** pour éléments/flux nouveaux ou modifiés selon contexte.

## Vues
- Vue dynamique au périmètre « software system » : pas de composants (uniquement conteneurs). Pour composants → vue composant ou vue dynamique à périmètre conteneur.
- Vue conteneur de surface + vues composant par conteneur porteur.
- Titres/descriptions de vue sans référence.

## Thème
- Logo : `theme/<client>.png`
- Tags d'éléments cohérents (ex. `Externe` non `External`)
- Styles `new`/`modified`/`deleted` dans `theme/0000-default-styles.dsl` (ne pas redéfinir)

## Validation
Utiliser **toujours** l'image Docker `latest` :

```bash
docker run --rm -v "$(pwd)":/usr/local/structurizr structurizr/cli:latest validate -w workspace.dsl
```

Le volume monté est le répertoire de travail du projet (racine contenant `workspace.dsl`).

Boucle : **`validate`** puis **`export json`** avant commit.

## Contrôles post-export
1. **Aucune référence dans les libellés rendus**
```bash
grep -nE "(INV-[0-9]|CT-[0-9]|CTR-SEC-|PINV-|RAT-|PLG-|IMP-|R-SEC-|§[0-9]|ADR|DEC)" <export>
```

2. **Un seul lien par sens (vues statiques)** : extraire paires `(source->cible)`, trier, vérifier `uniq -d` vide. Exception : vues dynamiques.

Voir aussi la skill `structurizr-diagrams`.
