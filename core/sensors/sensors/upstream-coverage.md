---
id: upstream-coverage
kind: deterministic
command: "non-exécutable (advisory documentaire) — voir ADR-0010"
default_severity: advisory
description: "Vérifie que le livrable référence explicitement sa demande amont (issue d'origine, ADR parent le cas échéant)."
category: document-shape
fire_on: gate
matches: "{decisions/[0-9][0-9][0-9][0-9]-*.md,documentations/**/*.md,livrables/**/*.md}"
origine: ALI-188
---

# Sensor `upstream-coverage` — couverture amont *(prioritaire)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie que les livrables de l'étape (évalués **en ensemble**) **référencent explicitement leur demande amont** — issue d'origine et, le cas échéant, ADR parent / décision de cadrage. **Advisory** (`default_severity: advisory`). Recoupe le contrôle `absence-orphelin` du verification gate (`gates.md`).

## Contrat de vérification (`checks`)

```yaml
checks:
  reference_amont:
    # au moins une référence vers l'issue d'origine
    issue: "ALI-[0-9]+ | HOM-[0-9]+"
    # pour un ADR : au moins une entrée Références reliant issue et/ou ADR liés
    adr_references_non_vide: true
  absence_orphelin: true                       # recoupe le contrôle 3 du verification gate
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor upstream-coverage — <fichier>   (source : core/sensors/sensors/upstream-coverage.md @ <commit>)
- verdict : ✅ référence amont présente (<issue / ADR>) | ⚠️ aucune référence amont détectée | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : informe sur un artefact potentiellement orphelin, ne bloque pas. Recoupe le contrôle « absence d'artefact orphelin » du verification gate.
