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

Dans ce scope (comme dans `complex` et `express`), le CV de chaque collaborateur est
sélectionné selon la **règle de sélection de la source CV** :

- **Si un CV PDF/DOCX est fourni en pièce jointe de l'issue** → il est **extrait** d'abord
  (nouvelle version), puis c'est cette version qui sert au matching.
- **Sinon** (aucun CV fourni pour une analyse qui en a besoin) → la **dernière version déjà
  extraite** est utilisée — jamais les fichiers sources (supprimés après extraction) :
  - **flux entre agents (A2A)** : la **dernière version JSON** (`<nom>-<prenom>-<AAAA-MM-JJ>.json`)
    est le seul artefact croisé avec un AO par le Matcher Profils ;
  - **fichier à télécharger pour l'humain** : la **fiche d'analyse Markdown** courante (du jour).

Règle complète et journalisation d'audit : voir
[`../agents/gestionnaire-cv-agent.md`](../agents/gestionnaire-cv-agent.md)
(§ Règle de sélection de la source CV, § Versionnage JSON).

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md).
