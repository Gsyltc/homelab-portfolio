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

Dans ce scope (comme dans `complex` et `express`), les CV des collaborateurs pris en
compte par défaut sont issus de la **dernière analyse produite** — jamais des fichiers
sources (PDF/DOCX supprimés après extraction) :

- **Flux entre agents (A2A)** : la **dernière version JSON** créée
  (`<nom>-<prenom>-<AAAA-MM-JJ>.json`) est le seul artefact croisé avec un AO par le
  Matcher Profils. Les versions JSON antérieures ne sont jamais utilisées.
- **Flux de gate avec l'humain** : la **fiche d'analyse Markdown** courante (du jour) est
  l'artefact présenté à l'humain aux points de validation.

Règle de sélection de la dernière version JSON et journalisation d'audit : voir
[`../agents/gestionnaire-cv-agent.md`](../agents/gestionnaire-cv-agent.md) (§ Versionnage JSON).

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md).
