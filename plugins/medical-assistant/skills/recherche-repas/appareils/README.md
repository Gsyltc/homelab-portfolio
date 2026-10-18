# Appareils de cuisine — fichiers de référence

Ce répertoire rend la skill `recherche-repas` **générique** : chaque appareil de cuisine utilisable par le chef y est décrit dans son **propre fichier** `<appareil>.md`. Pour ajouter un appareil, il suffit d'ajouter un fichier ici — aucune autre modification de la skill n'est nécessaire.

## Ajouter un appareil

1. Créer `appareils/<slug-appareil>.md` (ex. `four-vapeur.md`).
2. Renseigner le gabarit ci-dessous : nom, sources de recettes, accessoires/modes disponibles, emplacement des recettes.
3. (Optionnel) Déposer les livres de recettes embarqués dans `appareils/<slug-appareil>/` (ex. PDF).

## Gabarit d'un fichier d'appareil

```markdown
---
type: appareil-cuisine
slug: <slug-appareil>
nom: "<Nom lisible de l'appareil>"
---

# <Nom de l'appareil>

## Sources de recettes
1. Livre(s) embarqué(s) : `appareils/<slug>/<fichier>.pdf`
2. Site(s) officiel(s) : <URL>

## Accessoires / modes de cuisson disponibles
- <accessoire 1>
- <accessoire 2>

## Emplacement des recettes
Comment référencer une recette pour que l'humain la réalise :
- livre → nom du livre + page/section
- site → URL directe
- fichier → chemin
```

## Appareils présents

| Appareil | Fichier |
|---|---|
| Companion de Moulinex | [companion-moulinex.md](companion-moulinex.md) |
