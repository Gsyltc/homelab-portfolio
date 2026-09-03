---
name: express
depth: minimal
verification: standard
review_cap: advisory
keywords: [express, petit changement, quick, rapide, mineur, trivial, correction rapide]
description: "Petit changement clair, faible risque — chemin court ; lourd ignoré (sauf action à impact)"
skeleton: off
---

# Scope `express`

Petit changement clair et à faible risque : **chemin court**, les stages lourds sont ignorés.

**Garde-fou R1** : l'allègement est réservé aux changements **sans impact runtime / production**.
Dès qu'un `express` déploie ou effectue une action à impact (Operation ≠ ignorée), le stage
`deliverables-breakdown` repasse à activé et la vérification remonte à `standard` minimum
([ADR-0003](../../decisions/0003-scopes-et-axes-depth-verification.md)).

Axes par défaut : Depth `minimal`, vérification `standard` (le contrôle reste au niveau standard).
`review_cap: advisory` matérialise le plafond de revue allégé du chemin court sur les stages
non liés à la sécurité — sans jamais relever ni contourner le plancher OWASP / STRIDE.

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md).
