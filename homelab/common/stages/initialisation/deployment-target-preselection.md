---
slug: deployment-target-preselection
phase: initialisation
execution: ALWAYS
condition: "Always executes pour une demande de stack"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [cibles_disponibles]
consumes: [{artifact: detection_stack_existante_vs_nouvelle, required: true}, {artifact: lien_documentation_officielle, required: true}]
requires_stage: [labels-audit-init]
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Stack détectée + documentation officielle (lue à l'étape 3 de l'amorçage)"
outputs: "Cibles de déploiement disponibles : Docker (image) et/ou Proxmox (script Helper-Scripts)"
---

# Pré-sélection de la cible de déploiement (Docker / Proxmox)

## Objectif

Lister les cibles disponibles, Docker et Proxmox, pour que l'humain choisisse au gate léger.

## Steps

### Step 1 — Stack existante

Si `stack-detection` a trouvé la stack, consigner sa cible actuelle (`terraform/swarm` → Docker, `terraform/services` → Proxmox). Aucune recherche. Fin du stage.

### Step 2 — Docker

Depuis la documentation officielle : image publiée (registry + nom). Consigner l'image, ou « aucune image Docker ».

### Step 3 — Proxmox

Rechercher un script Proxmox VE Helper-Scripts. Le site `https://community-scripts.org/` est rendu côté client et répond HTTP 200 pour tout slug : ne pas conclure d'après sa recherche ou son statut HTTP. Source de vérité : le dépôt `community-scripts/ProxmoxVE`, dossier `ct/`.

1. Lister les variantes de nom : nom de la stack, avec/sans tiret ou underscore (`sync-in`, `syncin`), nom du dépôt upstream, mot-clé principal.
2. Lister `ct/` (`https://api.github.com/repos/community-scripts/ProxmoxVE/contents/ct`) et filtrer, sans tenir compte de la casse, sur chaque variante.
3. Confirmer par `https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/<slug>.sh` (200 = existe). Vérifier que la ligne `# Source:` pointe vers le dépôt upstream de la stack (écarte les homonymes).
4. Compléter par la page `https://community-scripts.org/scripts/<slug>` et une recherche web (scripts « testing » inclus).
5. Conclure « aucun script trouvé » seulement si les étapes 2 et 3 sont négatives pour toutes les variantes.

Consigner le lien du script, ou « aucun script trouvé » + variantes testées.

## Sensors

Outputs: `cibles_disponibles` consigné sur l'issue et dans la section `cibles` de `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/preselection.json` (format : sensor [`initial-proposal`](../../../sensors/sensors/initial-proposal.md)). Présenté au point 3 de [`intent-scope-approval`](../ideation/intent-scope-approval.md). Bloquant si absent sur `new-stack` / `infra-terraform` (voir [`gates.md`](../../../sensors/gates.md)).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (préférences Docker / Proxmox par type de stack) tracés, remontés **en fin de workflow**, dans un message séparé ([`closure`](../validation/closure.md)).
