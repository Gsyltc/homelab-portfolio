---
name: security-patch
depth: standard
verification: renforcé
keywords: [sécurité, security, correctif, patch, vulnérabilité, CVE, durcissement, hardening, faille]
description: "Correction / durcissement de sécurité — Architecte cybersécurité pilote, périmètre resserré, traçabilité renforcée"
skeleton: off
---

# Scope `security-patch`

Correction ou durcissement de sécurité. L'**Architecte cybersécurité pilote** le travail ;
périmètre resserré, traçabilité renforcée, analyse d'impact / non-régression du correctif produite
avant toute recommandation (R2 de [ADR-0003](../../decisions/0003-scopes-et-axes-depth-verification.md)).

Axes par défaut : Depth `standard`, vérification **`renforcé`**. **Garde-fou non abaissable** :
`depth` ≥ `standard` et `verification` ≥ `renforcé` ne peuvent jamais être abaissés par override ;
**aucun `review_cap`** ne peut abaisser la revue sur ce scope (R3 / R7, garde-fou sécurité).

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md).
