---
title: Scopes — un fichier par scope (source d'identité)
---

# Scopes — un fichier de données par scope

Cette couche porte l'**identité** de chaque scope, en données déclaratives.

## Le contrat en deux moitiés

Un scope se déclare en **deux endroits** :

1. **L'identité** vit dans son propre fichier — `scopes/<name>.md` (un fichier par scope). Il porte le nom du scope, ses métadonnées de routage (`keywords`) et ses **valeurs par défaut** d'axes (`depth`).
2. **L'appartenance** (quels stages s'exécutent sous ce scope) vit **transposée sur les stages** : chaque fiche de stage nomme dans son front-matter `scopes:` les scopes sous lesquels elle s'exécute.

La liaison entre les deux est le **nom du scope**.

## Schéma du front-matter

```yaml
name: <scope>                 # requis — nom du scope (= stem du fichier)
depth: minimal|standard|comprehensive   # requis — détail des artefacts par défaut
keywords: [ ... ]             # optionnel — déclencheurs d'auto-détection FR / EN
description: "<une ligne>"    # optionnel — libellé court
skeleton: on|off              # optionnel
```

## Garde-fous (non désactivables par un scope)

- Validation humaine granulaire, piste d'audit, communication JSON↔Markdown — **aucun scope ne les désactive**.
- Auto-détection = **plancher** : la confirmation humaine peut monter le contrôle, jamais le descendre sans validation tracée.

## Ordre de désambiguïsation

`complex` > `express` > `standard`

Défaut : **`standard`** en l'absence de mot-clé détecté.
