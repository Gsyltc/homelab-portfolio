---
id: required-sections-adr
kind: deterministic
command: "python3 core/scripts/sensors/required_sections_adr.py"
default_severity: advisory
description: "Vérifie que les rubriques obligatoires de l'ADR sont présentes et non vides, et que sa forme (front matter, statut, puces codées, remplacement) est conforme au gabarit."
category: document-shape
fire_on: gate
matches: "decisions/[0-9][0-9][0-9][0-9]-*.md"
write_matches: "decisions/[0-9][0-9][0-9][0-9]-*.md"
origine: ALI-218
---

# Sensor `required-sections-adr` — sections requises des ADR

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie les **rubriques obligatoires** et la **forme** de chaque **ADR** de `decisions/` (gabarit de la skill `create-architecture-decision-record`). **Advisory** (`default_severity: advisory`). Déclenché aussi **à chaque écriture** d'un ADR (`write_matches`) par le hook d'écriture : la forme est vérifiée dès la création ou la modification, sans attendre le gate.

Issu de la scission du sensor unique `required-sections` (HOM-285) : deux manifestes (ADR / architecture : DAS et détaillée), pour éviter les confusions entre types de documents. L'autre : [`required-sections-architecture`](required-sections-architecture.md).

## Contrat de vérification (`checks`)

```yaml
checks:
  adr:                                         # rubriques dérivées du gabarit de la skill create-architecture-decision-record
    front_matter_en_tete: true                 # bloc `---` en tout début de fichier, avant le titre H1
    entete_meta: [auteurs, parties_prenantes, accepte_par, accepte_le, supersedes, superseded_by]
    status_valeurs: [Proposed, Accepted, Rejected, Superseded, Deprecated]   # un seul statut ; le mot-clé en tête fait foi
    codes_puces: {Positives: POS-NNN, Négatives: NEG-NNN, "Alternatives étudiées": ALT-NNN}
    coherence_remplacement: true               # `supersedes` / `superseded_by` renvoient à un ADR existant de decisions/
    sections:
      - Status                 # titre en anglais (compat Structurizr), statut unique retenu
      - "Date de création"      # date de création de l'ADR au format YYYY-MM-DD, sous Status
      - Contexte
      - Décision
      - "Conséquences"        # sous-rubriques obligatoires : Positives / Négatives
      - "Alternatives étudiées"
      - "Notes d'implémentation"
      - "Références"
    sections_depuis_2026_11_11:                # exigées pour les ADR dont la « Date de création » est >= 2026-11-11
      - "Critères de décision"
    non_vide: true
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor required-sections-adr — <fichier>   (source : core/sensors/sensors/required-sections-adr.md @ <commit>)
- verdict : ✅ conforme | ⚠️ rubriques manquantes/vides : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : n'empêche pas l'écriture, ne remplace pas la validation humaine ni le contrôle sécurité. Le passage à bloquant est une décision ADR + contrôle sécurité (Architecte cybersécurité).
