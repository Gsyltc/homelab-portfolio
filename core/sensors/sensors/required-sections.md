---
id: required-sections
kind: deterministic
command: "non-exécutable (advisory documentaire) — voir ADR-0010"
default_severity: advisory
description: "Vérifie que les rubriques obligatoires du gabarit d'ADR / DAS sont présentes et non vides."
category: document-shape
fire_on: gate
matches: "{decisions/[0-9][0-9][0-9][0-9]-*.md,documentations/**/*.md}"
origine: ALI-188
---

# Sensor `required-sections` — sections requises *(prioritaire)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie que les **rubriques obligatoires** du gabarit sont présentes et non vides sur chaque **ADR** ou **DAS** livré. **Advisory** (`default_severity: advisory`).

## Contrat de vérification (`checks`)

```yaml
checks:
  adr:                                         # rubriques dérivées du gabarit de la skill create-architecture-decision-record
    entete_meta: [auteurs, "accepté par", "accepté le", supersedes, superseded_by]
    sections:
      - Status                 # titre en anglais (compat Structurizr), statut unique retenu
      - Contexte
      - Décision
      - "Conséquences"        # sous-rubriques obligatoires : Positives / Négatives
      - "Alternatives étudiées"
      - "Notes d'implémentation"
      - "Références"
    non_vide: true
  das:
    sections:
      - titre
      - "contexte / objectif"
      - "vues (fonctionnelle / technique)"
      - "décisions liées (ADR)"
      - risques
    non_vide: true
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor required-sections — <fichier>   (source : core/sensors/sensors/required-sections.md @ <commit>)
- verdict : ✅ conforme | ⚠️ rubriques manquantes/vides : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : n'empêche pas l'écriture, ne remplace pas la validation humaine ni le contrôle sécurité. Le passage à bloquant est une décision ADR + contrôle sécurité (Architecte cybersécurité).
