---
id: style-concision
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
description: "Vérifie que les documents livrables respectent le style concis : paragraphes courts, phrases courtes, puces limitées en profondeur, tableaux hors gabarit sobres."
category: document-shape
fire_on: write
matches: "{documentation/*.md,decisions/[0-9][0-9][0-9][0-9]-*.md}"
origine: HOM-282
---

# Sensor `style-concision` — style des documents livrables

Check déterministe déclenché **à l'écriture** d'un document (`fire_on: write`). Il vérifie le respect du style défini par [`document-style`](../../common/protocols/document-style.md) (règle `RULE-WS-007`). **Advisory** (`default_severity: advisory`).

Il porte sur la **forme** uniquement : il ne juge ni le fond ni la pertinence de l'information.

## Contrat de vérification (`checks`)

```yaml
checks:
  paragraphe:
    lignes_max: 5                 # seuil d'alerte ; la cible du style est 3
  phrase:
    mots_max: 35
  puces:
    niveaux_max: 3
  tableau_hors_gabarit:           # les tableaux imposés par un gabarit sont exclus du contrôle
    colonnes_max: 5
    mots_par_cellule_max: 25
  exclusions:                     # contenus non évalués
    - blocs de code
    - front-matter
    - tableaux issus d'un gabarit
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor style-concision — <fichier>   (source : core/sensors/sensors/style-concision.md @ <commit>)
- verdict : ✅ style conforme | ⚠️ écart(s) : <liste : localisation + seuil dépassé> | ⛔ indisponible : <motif>
```

## Garde-fou

- Advisory : signale un écart de forme, ne bloque pas.
- Ne remplace ni la validation humaine granulaire ni le contrôle sécurité (SG-3).
- Concision sans perte : un écart de forme n'autorise jamais la suppression d'un risque, d'une norme ou d'une décision.
