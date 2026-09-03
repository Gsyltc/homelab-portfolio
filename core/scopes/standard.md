---
name: standard
depth: standard
verification: standard
keywords: [architecture, conception, évolution, refonte, design, évolution architecture]
description: "Conception / évolution d'architecture « normale » — parcours standard complet (scope par défaut)"
skeleton: off
---

# Scope `standard` *(défaut)*

Parcours d'architecture complet pour une conception ou une évolution « normale ». C'est le
**scope par défaut** en l'absence de mot-clé détecté — aucune régression par rapport au parcours
d'architecture historique.

Tous les stages d'Ideation, Inception et Construction s'exécutent ; l'Operation est conditionnelle
(présente uniquement s'il y a une action à impact / un déploiement). Axes par défaut : Depth
`standard`, vérification `standard`. Aucun `review_cap` — pas d'abaissement au niveau du scope.

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md).
