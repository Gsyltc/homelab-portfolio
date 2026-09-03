---
id: claim-sources
kind: deterministic
command: "non-exécutable (advisory documentaire) — voir ADR-0010"
default_severity: advisory
description: "Vérifie que chaque affirmation retenue à la capture d'intention porte une source résoluble et que les hypothèses conservées correspondent à une confirmation humaine explicite."
category: provenance
fire_on: gate
matches: "{documentations/**/*.md,decisions/[0-9][0-9][0-9][0-9]-*.md}"
origine: ALI-198
---

# Sensor `claim-sources` — sources des affirmations *(prioritaire, doc-first)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie que **chaque affirmation retenue** dans l'intention capturée et la documentation d'architecture **porte une source résoluble** (issue d'origine, entrée humaine, ADR, demande brute consignée), et que les **hypothèses conservées** correspondent exactement à une **confirmation humaine explicite** tracée sur l'issue. **Advisory** (`default_severity: advisory`).

Adaptation doc-first du sensor AI-DLC `aidlc-claim-sources` (Intent Capture) : là où AI-DLC valide des *claims* horodatés dans un enregistrement d'intention, ce dépôt valide la **traçabilité des affirmations** de la DAS / des ADR vers la piste d'audit de l'issue et la demande brute consignée (voir la boucle de gouvernance A2A, `conductor.md`).

## Contrat de vérification (`checks`)

```yaml
checks:
  affirmations:
    source_resoluble: true            # chaque affirmation renvoie à une source (issue, entrée humaine, ADR, demande brute)
    valeurs_enregistrees:             # description / scope / hypothèses = inputs autoritaires
      description_conforme: true
      scope_confirme: true
  hypotheses_conservees:
    confirmation_humaine_explicite: true   # une hypothèse retenue = confirmation humaine tracée, jamais inférée
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor claim-sources — <fichier>   (source : core/sensors/sensors/claim-sources.md @ <commit>)
- verdict : ✅ affirmations sourcées | ⚠️ affirmation(s) sans source / hypothèse non confirmée : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : signale une affirmation non sourcée ou une hypothèse non confirmée, ne bloque pas. **Ne remplace pas** la confirmation humaine ni le contrôle sécurité (SG-3). Une hypothèse ne devient jamais un fait par absence de contradiction (SG-2 : l'absence de signal attendu est elle-même un écart).
