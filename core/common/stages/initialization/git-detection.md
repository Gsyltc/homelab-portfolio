---
slug: git-detection
phase: initialization
execution: ALWAYS
condition: "Always executes — fait détecté, non validé"
lead_agent: null
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [contexte_git_consigne]
consumes: [{artifact: repertoire_projet_confirme, required: true}]
requires_stage: [directory-check]
sensors: []
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Répertoire projet confirmé, description du projet"
outputs: "Nature Git (Oui/Non) consignée"
---

# Détection Git

## Objectif

Déterminer de façon déterministe si le projet est sous Git avant toute création de fichiers.

## Steps

### Step 1 — Lire l'indicateur Git de la description du projet

Lire la description du projet (champ description du projet Multica).

- La description contient `Git : Oui` (variante tolérée : `Git: Oui`) → **projet Git** → consigner le fait et terminer le stage.
- La description contient `Git : Non` (variante tolérée : `Git: Non`) → **pas de gestion Git** → ne créer aucune branche ; consigner le fait et terminer le stage.
- L'information est **absente** → passer au Step 2.

### Step 2 — Détecter le dépôt sur disque (information absente)

Vérifier la présence d'un répertoire `.git/` à la racine du répertoire projet.

- `.git/` présent → **ajouter `Git: Oui`** à la description du projet (`multica project update`), consigner le fait et terminer le stage.
- `.git/` absent → **ajouter `Git: Non`** à la description du projet, ne créer aucune branche ; consigner le fait et terminer le stage.

L'écriture dans la description est un simple enrichissement de fait détecté (même pattern que l'inscription d'une méthodologie) ; elle n'écrase pas la description existante et n'appelle pas de gate humain.

## Sensors

Outputs: contexte Git (Oui/Non) consigné sur l'issue. Aucun gate humain (Initialization — bootstrap déterministe).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : tenir le journal des candidats-règles sur l'issue. Stage d'Initialization (bootstrap déterministe) → **saute** l'interaction liée au gate humain ; aucune règle n'est écrite hors du cycle capture → confirmation humaine → contrôle de conflit.
