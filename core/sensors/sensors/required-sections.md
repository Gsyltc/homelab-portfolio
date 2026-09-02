# Sensor `required-sections` — sections requises *(prioritaire)*

Check déterministe déclenché à l'**écriture d'une décision structurante ou d'une DAS** : vérifie que les **rubriques obligatoires** du gabarit sont présentes et non vides. **Advisory**.

```yaml
id: required-sections
type: sensor
nature: advisory
priority: prioritaire
origine: ALI-188
triggers:
  - "decisions/[0-9][0-9][0-9][0-9]-*.md"     # décision structurante
  - "**/*das*.md"                              # documentation d'architecture (DAS)
checks:
  decision_structurante:                       # rubriques dérivées des décisions structurantes existantes
    entete_meta: [auteurs, "accepté par", "accepté le"]
    sections:
      - Status
      - Contexte
      - Décision
      - "Conséquences"        # sous-rubriques : Positives / Négatives
      - "Alternatives étudiées"
      - "Références"
    non_vide: true
  das:
    sections:
      - titre
      - "contexte / objectif"
      - "vues (fonctionnelle / technique)"
      - "décisions liées (décisions structurantes)"
      - risques
    non_vide: true
output: "liste des rubriques manquantes ou vides (advisory)"
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor required-sections — <fichier>   (source : core/sensors/sensors/required-sections.md @ <commit>)
- verdict : ✅ conforme | ⚠️ rubriques manquantes/vides : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : n'empêche pas l'écriture, ne remplace pas la validation humaine ni le contrôle sécurité. Le passage à bloquant est une décision structurante + contrôle sécurité.
