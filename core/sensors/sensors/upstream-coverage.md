# Sensor `upstream-coverage` — couverture amont *(prioritaire)*

Check déterministe déclenché à l'**écriture d'un ADR, d'une DAS ou d'un livrable** : vérifie que le livrable **référence explicitement sa demande amont** (issue d'origine et, le cas échéant, ADR parent / décision de cadrage). **Advisory**.

```yaml
id: upstream-coverage
type: sensor
nature: advisory
priority: prioritaire
origine: ALI-188
triggers:
  - "decisions/[0-9][0-9][0-9][0-9]-*.md"     # ADR
  - "documentations/*.md"                      # DAS
  - "livrables/**/*.md"                        # livrables détaillés
checks:
  reference_amont:
    # au moins une référence vers l'issue d'origine
    issue: "ALI-[0-9]+ | HOM-[0-9]+"
    # pour un ADR : au moins une entrée Références reliant issue et/ou ADR liés
    adr_references_non_vide: true
  absence_orphelin: true                       # recoupe le contrôle 3 du verification gate
output: "signalement si aucune référence amont détectée (artefact potentiellement orphelin)"
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor upstream-coverage — <fichier>   (source : core/sensors/sensors/upstream-coverage.md @ <commit>)
- verdict : ✅ référence amont présente (<issue / ADR>) | ⚠️ aucune référence amont détectée | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : informe sur un artefact potentiellement orphelin, ne bloque pas. Recoupe le contrôle « absence d'artefact orphelin » du verification gate.
