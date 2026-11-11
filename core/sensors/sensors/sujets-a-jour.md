---
id: sujets-a-jour
kind: deterministic
command: "python3 core/scripts/sensors/sujets_a_jour.py"
default_severity: advisory
description: "Vérifie que le champ `sujets` du front-matter d'un document d'architecture reflète ses titres ## et ### (présence, absence de titre obsolète, ordre)."
category: document-shape
fire_on: write
matches: "documentation/**/*.md"
origine: HOM-300
---

# Sensor `sujets-a-jour` — sommaire de ciblage à jour

Check déterministe déclenché **à l'écriture** (`fire_on: write`) d'un fichier de documentation d'architecture. Il garantit que le **sommaire de ciblage** (`sujets`) du front-matter reste fidèle aux titres du document : c'est lui qui permet aux agents de décider **quels fichiers et sections lire, modifier ou créer** sans charger le corps (lazy loading). **Advisory** (`default_severity: advisory`).

Le sensor ne connaît pas les gabarits : il ne s'applique qu'aux documents qui **portent un champ `sujets`**. Les autres champs du front-matter et les règles de routage relèvent de la skill du gabarit (voir `architecture-solution-gabarits` et `architecture-securite-gabarits`).

## Contrat de vérification (`checks`)

```yaml
checks:
  perimetre: documents de documentation/**/*.md dont le front-matter porte un champ `sujets` (les autres sont hors périmètre, non signalés)
  titres_references: titres de niveau 2 (##) et 3 (###), hors blocs de code, commentaires HTML et front-matter
  ecarts:
    - titre ##/### absent de `sujets`
    - entrée de `sujets` sans titre ##/### correspondant
    - mêmes titres mais ordre différent de celui du document
  comparaison: insensible à la casse, aux emphases/backticks et à la numérotation de tête
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (aucun document avec `sujets` dans le périmètre : jamais lu comme conforme, SG-2). Source tracée (SG-5).

```
Sensor sujets-a-jour — <fichier>   (source : core/sensors/sensors/sujets-a-jour.md @ <commit>)
- verdict : ✅ conforme | ⚠️ `sujets` désynchronisé des titres ##/### : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : n'empêche pas l'écriture et ne remplace pas la validation humaine. Il vérifie la **cohérence** de `sujets`, pas la pertinence de son contenu.
