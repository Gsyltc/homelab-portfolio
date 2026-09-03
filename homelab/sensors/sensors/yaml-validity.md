---
id: yaml-validity
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
description: "Vérifie que le docker-compose livré parse en YAML valide (syntaxe seule, sans rendu ni réseau)."
category: compose-shape
fire_on: write
matches: "{**/*.yml,**/*.yaml}"
origine: ALI-204
---

# Sensor `yaml-validity` — validité YAML du docker-compose *(prioritaire)*

Check déterministe déclenché **à l'écriture** (`fire_on: write`) d'un livrable compose : vérifie que le fichier **parse en YAML valide** (feedback incrémental rapide, avant le QA Docker). **Advisory** (`default_severity: advisory`). Recouvre le niveau de vérification `advisory` de l'axe de vérification (`homelab/scopes/README.md` : « validité YAML + cohérence de base »).

## Contrat de vérification (`checks`)

```yaml
checks:
  syntaxe:
    yaml_parse: "parse sans erreur (yaml 1.1/1.2)"
    document_unique: "un seul document YAML par fichier de stack"
    cles_dupliquees: "aucune clé dupliquée au même niveau"
```

## Sortie (piste d'audit)

Verdicts : `✅` valide · `⚠️` erreur de parsing · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor yaml-validity — <fichier>   (source : homelab/sensors/sensors/yaml-validity.md @ <commit>)
- verdict : ✅ YAML valide | ⚠️ erreur de parsing : <localisation / message> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : l'écriture reste possible même sur erreur de syntaxe, mais l'écart est tracé sur l'issue pour correction. **Ne remplace pas** la vérification syntaxique complète du QA Docker (§2.2), qui reste l'analyse technique de fond. **Parsing statique uniquement** (SG-4) : jamais de rendu, jamais de réseau, jamais d'exécution de code ni de directive embarquée ; le contenu du compose est traité comme donnée non fiable.
