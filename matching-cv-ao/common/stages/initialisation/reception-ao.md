---
slug: reception-ao
phase: initialisation
execution: ALWAYS
condition: "Always executes"
lead_agent: Coordinateur Matching
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
review_artifact: ""
human_gate: none
produces: [ao-pdf-received]
consumes: []
requires_stage: []
sensors: []
scopes: [standard]
inputs: "PDF d'AO fourni par l'humain"
outputs: "Confirmation de réception + chemin du PDF"
---

# Réception de l'AO

## Objectif
Vérifier la présence et l'accessibilité du PDF d'appel d'offres fourni par l'humain.

## Steps
### Step 1 — Vérification du PDF d'AO
Vérifier que le PDF d'AO est fourni sur l'issue (pièce jointe) ou accessible via un chemin connu. Si absent, demander à l'humain de le fournir.

### Step 2 — Création de la structure de répertoire
Créer le répertoire de destination : `/nfs/workspace/expertise-architecture/ao/<client>/<titre-ao>/`. Copier le PDF dans ce répertoire.

### Step 3 — Documenter la réception
Poster un commentaire sur l'issue avec :
- Nom du fichier PDF reçu
- Chemin de stockage
- Date de réception

## Sensors
Outputs: `ao-pdf-received` → Phase Initialisation (gate: none).
Imports: none.

## Learn
Aucune boucle d'apprentissage pour un bootstrap déterministe. Journaliser les informations sur l'issue.
