---
name: format-cv
depth: standard
keywords: [format cv, formatage cv, traitement cv, extraction cv, mise à jour cv, archivage cv, cv only, format-cv]
description: "Traitement CV seul — chargement, extraction/formatage/archivage, mise à jour (sans AO ni matching)"
skeleton: off
---

# Scope `format-cv`

Parcours **CV uniquement** : ce scope sert exclusivement au traitement des CV des
collaborateurs. Il n'y a **ni analyse d'appel d'offres, ni croisement/classement de
profils, ni remplissage de grille d'évaluation**.

## Stages actifs

Seuls trois stages s'exécutent sous ce scope :

- **`chargement-cv`** (Initialisation) — repérage / inventaire des CV sources à traiter (pièces jointes de l'issue) et des analyses existantes.
- **`extraction-cv`** (Analyse) — récupération des CV sources depuis les **pièces jointes de l'issue**, extraction des informations
  structurées (dont l'**équivalence MIFI** — objet `mifi` à 4 états, avec mention humaine pour tout `a_verifier`), production de la **fiche d'analyse Markdown versionnée** à la racine de `cv/` (anciennes
  fiches déplacées dans `cv/archives/`) et du **JSON d'analyse versionné**, puis **suppression de la copie de
  travail téléchargée** — le tout daté du **jour**.
- **`mise-a-jour-cv`** (Clôture) — mise à jour des CV, dans la même arborescence stricte.

> **Organisation stricte du répertoire `cv/`** (voir la fiche de l'agent
> [`../agents/gestionnaire-cv-agent.md`](../agents/gestionnaire-cv-agent.md)) : les **sources PDF/DOCX** sont
> **fournis en pièces jointes de l'issue** et **supprimés après extraction** (non conservés, non stockés dans
> `cv/`) · `cv/archives/` (anciennes fiches Markdown) · fiche Markdown du jour et JSON versionnés à la racine.
> La date de dernière modification reportée est **toujours la date du jour**.

Depth par défaut : `standard`. Aucun `review_cap` — pas d'abaissement au niveau du scope.

## Exclusions explicites

Sont **hors périmètre** de `format-cv` (stages ignorés) :

- `reception-ao`, `parse-ao` — réception / analyse d'appel d'offres ;
- `croisement-profils`, `classement-profils` — croisement profils ↔ exigences et classement ;
- `remplissage-grille`, `presentation-resultats` — remplissage de grille et présentation /
  validation granulaire liée au matching ;
- `livraison` — livraison finale liée au matching.

## Prérequis assoupli de `mise-a-jour-cv`

Sous `format-cv`, le stage `mise-a-jour-cv` ne dépend **pas** de `livraison-finale`
(hors périmètre) : il s'appuie sur les **CV extraits/validés** (`cv-profils`) produits par
`extraction-cv`. Voir la fiche [`../common/stages/cloture/mise-a-jour-cv.md`](../common/stages/cloture/mise-a-jour-cv.md).

## Garde-fous

Comme tout scope, `format-cv` ne désactive **aucun** invariant : validation humaine
granulaire, piste d'audit et communication JSON↔Markdown restent en vigueur.

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md).
