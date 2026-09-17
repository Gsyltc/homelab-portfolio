---
name: standard
depth: standard
keywords: [offre, appel d'offres, AO, matching, profil, recrutement, candidature]
description: "AO de complexité moyenne — parcours standard complet (scope par défaut)"
skeleton: off
---

# Scope `standard` *(défaut)*

Parcours de matching complet pour un appel d'offres de complexité moyenne. C'est le
**scope par défaut** en l'absence de mot-clé détecté.

Tous les stages des 5 phases s'exécutent. Depth par défaut : `standard`. Aucun
`review_cap` — pas d'abaissement au niveau du scope.

## CV utilisés par défaut

Comme en `complex` et `express`, ce scope suit la **règle de sélection de la source CV** (pièce jointe extraite en priorité, sinon dernière version déjà extraite : JSON pour le flux A2A, fiche Markdown du jour pour le téléchargement humain). Règle complète, versionnage et journalisation d'audit : compétence `cv-analyse` (plugin `rh-assistant`, § Règle de sélection de la source CV, § Versionnage JSON), chargée par l'agent `Gestionnaire CV`.

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
le protocole `scopes-and-axes`.
