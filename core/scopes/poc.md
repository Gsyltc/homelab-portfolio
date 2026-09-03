---
name: poc
depth: minimal
verification: advisory
review_cap: advisory
keywords: [PoC, preuve de concept, proof of concept, prototype, jetable, spike, expérimentation]
description: "Preuve de concept jetable — allégé, Depth minimale, non promouvable tel quel"
skeleton: off
---

# Scope `poc`

Preuve de concept **jetable**. Parcours allégé, Depth minimale, vérification `advisory`. Un PoC est
**non promouvable tel quel** : toute reprise en `feature` / `mvp` / `enterprise` **re-déclenche le
contrôle sécurité complet** du scope cible.

Axes par défaut : Depth `minimal`, vérification `advisory` → **`review_cap: advisory`** (plafond de
classe de revue conforme AI-DLC). **Le plancher OWASP / STRIDE reste actif** : `➖` ne signifie
jamais un contrôle sécurité nul, seules la profondeur et la rigueur sont allégées.

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md).
