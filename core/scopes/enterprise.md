---
name: enterprise
depth: comprehensive
verification: renforcé
keywords: [enterprise, entreprise, conformité, compliance, PCI DSS, GDPR, RGPD, Loi 25, LPRPDE, structurant, réglementaire]
description: "Chantier structurant, fort impact / conformité — complet + Depth comprehensive + normes conditionnelles"
skeleton: on
---

# Scope `enterprise`

Chantier structurant à fort impact ou à enjeu de conformité. Parcours **complet**, Depth
`comprehensive`, vérification **`renforcé`**.

- Point de contrôle obligatoire « **applicabilité des normes** » (PCI DSS / GDPR / Loi 25 /
  LPRPDE), décision tracée en ADR — y compris « aucune norme requise ».
- **Classification des données** traitées, pré-requis d'activation des normes.

**Garde-fou non abaissable** : `depth` ≥ `standard` et `verification` ≥ `renforcé` ; **aucun
`review_cap`** ne peut abaisser la revue.

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md).
