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

Comme en `standard` et `complex`, ce scope suit la **règle de sélection de la source CV** (pièce jointe extraite en priorité, sinon dernière version déjà extraite : JSON pour le flux A2A, fiche Markdown du jour pour le téléchargement humain). Règle complète, versionnage et journalisation d'audit : compétence `cv-analyse` (plugin `rh-assistant`, § Règle de sélection de la source CV, § Versionnage JSON), chargée par l'agent `Gestionnaire CV`.

Appartenance : voir le champ `scopes:` de chaque fiche de stage et la matrice de
le protocole `scopes-and-axes`.
