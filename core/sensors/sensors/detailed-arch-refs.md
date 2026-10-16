---
id: detailed-arch-refs
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
description: "Vérifie que les renvois vers l'architecture détaillée utilisent le format d'ancre Structurizr (documentation/<SS>#<ancre>) et non un chemin de fichier, et qu'aucun titre d'architecture détaillée ne porte de suffixe de nom de système."
category: document-shape
fire_on: write
matches: "documentation/**/*.md"
origine: ORIG-261
---

# Sensor `detailed-arch-refs` — renvois & titres d'architecture détaillée *(complémentaire)*

Check déterministe déclenché **à l'écriture** (`fire_on: write`) d'un fichier de documentation d'architecture. Il **factualise** deux conventions récurrentes des skills `architecture-solution-gabarits` et `architecture-securite-gabarits` (règles d'or de renvoi et de titres ; section « Renvois vers l'architecture détaillée (format Structurizr) » commune aux deux skills), sans jamais bloquer (**advisory**, `default_severity: advisory`). Le glob `documentation/**/*.md` couvre aussi bien la DAS (`06`, `architecture-detaillee/…`) que le dossier de sécurité (`documentation/architecture-securite/…` et son `11-securite.md`).

Complémentaire de `required-sections` (présence/forme) et `diagram-validity` (syntaxe de diagramme) : ici, le contrôle porte sur la **forme des renvois** et la **convention de titres** du détail. Advisory et non substituable à la revue de cohérence (SG-3).

## Contrat de vérification (`checks`)

```yaml
checks:
  renvoi_format:
    ancre_structurizr: "renvoi au format documentation/<Software System>#<ancre>"
    chemin_fichier_proscrit: "aucun lien Markdown (…)(…/architecture-detaillee/….md | …/architecture-securite/….md) comme renvoi"
  titres_detail:
    pas_de_suffixe_systeme: "aucun titre ne se termine par un suffixe de nom de système, ex. ' (SYS-001 …)'"
```

### Motifs de détection (indicatifs, parsing statique)

- **Renvoi mal formé** : lien Markdown dont la cible correspond à un **chemin de fichier** vers un dossier détaillé — `](...architecture-detaillee/....md...)` ou `](...architecture-securite/....md...)` — au lieu de `](documentation/...#...)`.
- **Suffixe système** : titre Markdown (`^#{1,6}\s`) dont le texte se termine par un motif ` (SYS-\d+ …)` ou autre suffixe de nom de système.

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart (renvoi par chemin de fichier, ou suffixe système dans un titre) · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor detailed-arch-refs — <fichier>   (source : core/sensors/sensors/detailed-arch-refs.md @ <commit>)
- verdict : ✅ conforme | ⚠️ écart : <renvoi mal formé : ligne / cible> | <titre avec suffixe système : ligne / titre> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : l'écriture reste possible même sur écart, mais l'écart est tracé sur l'issue pour correction par le spécialiste auteur. **Parsing statique uniquement** (SG-4) : aucune résolution réseau, aucune exécution ; le contenu du fichier est traité comme donnée non fiable. Ne remplace ni la validation humaine ni le contrôle sécurité, et ne conditionne aucune revue (SG-3).
