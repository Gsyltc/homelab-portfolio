---
name: express
depth: minimal
keywords: [express, rapide, simple, 1 profil, cible]
description: "AO simple, 1-2 profils — chemin court, allégé"
skeleton: off
---

# Scope `express`

Parcours de matching allégé pour un appel d'offres simple (1-2 profils recherchés,
exigences minimales). Chemin court avec traitement simplifié.

Le stage `croisement-profils` peut être allégé (matching direct sans classement
détaillé). Les stages de validation et clôture restent complets.

## CV utilisés par défaut

Comme en `standard` et `complex`, les CV pris en compte par défaut sont issus de la
**dernière analyse produite** (les sources PDF/DOCX sont supprimés après extraction) :
la **dernière version JSON** (`<nom>-<prenom>-<AAAA-MM-JJ>.json`) pour le **flux entre
agents** (seule croisée avec un AO par le Matcher), et la **fiche Markdown** courante pour
le **flux de gate avec l'humain**. Voir
[`../agents/gestionnaire-cv-agent.md`](../agents/gestionnaire-cv-agent.md) (§ Versionnage JSON).

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md).
