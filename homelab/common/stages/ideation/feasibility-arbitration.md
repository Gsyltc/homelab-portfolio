---
slug: feasibility-arbitration
phase: ideation
execution: ALWAYS
condition: "Always executes — faisabilité + recherche Helper-Scripts"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: optional
reviewer: null
review_class: none
human_gate: none
produces: [faisabilite_evaluee, recherche_helper_scripts]
consumes: [{artifact: intention_capturee, required: true}, {artifact: scope_propose, required: true}]
requires_stage: [scope-detection]
sensors: []
scopes: [stack-update, new-stack, security-patch, infra-terraform]
inputs: "Intention capturée + scope proposé"
outputs: "Faisabilité évaluée + recherche Helper-Scripts consignée"
---

# Faisabilité et recherche Helper-Scripts

## Objectif

Vérifier que la stack est déployable dans le Homelab et consigner la recherche Helper-Scripts.

## Steps

### Step 1 — Faisabilité

Existence d'images Docker, alternative Proxmox.

### Step 2 — Recherche Helper-Scripts (obligatoire, source unique)

Si le scope proposé (`scope-detection`) est `new-stack` / `infra-terraform`, **avant le gate `intent-scope-approval` et tout le Cadrage** : appliquer la **méthode de recherche** ci-dessous. Consigner sur l'issue le lien, ou « aucun script trouvé » + variantes testées (`recherche_helper_scripts`). Si le gate léger relève ensuite le scope vers l'un d'eux, la recherche est faite avant de passer en Cadrage. Le choix Swarm / Proxmox n'est **pas** fait ici : voir [`swarm-proxmox-arbitration`](../cadrage/swarm-proxmox-arbitration.md).

**Méthode de recherche :** Le site `https://community-scripts.org/` est rendu côté client et répond HTTP 200 pour tout slug : ne pas conclure d'après sa recherche ou son statut HTTP. Source de vérité : le dépôt `community-scripts/ProxmoxVE`, dossier `ct/`.

1. Lister les noms de variantes : nom de la stack, avec/sans tiret ou underscore (`sync-in`, `syncin`), nom du dépôt upstream, mot-clé principal.
2. Lister `ct/` (`https://api.github.com/repos/community-scripts/ProxmoxVE/contents/ct`) et filtrer, sans tenir compte de la casse, sur chaque variante.
3. Confirmer par `https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/<slug>.sh` (200 = existe). Vérifier que la ligne `# Source:` du script pointe vers le dépôt upstream de la stack (écarte les homonymes).
4. Compléter par la page `https://community-scripts.org/scripts/<slug>` et une recherche web (scripts « testing » inclus).
5. Conclure « aucun script trouvé » seulement si les étapes 2 et 3 sont négatives pour toutes les variantes.

## Sensors

Outputs: faisabilité + recherche consignées. Frontière Idéation → Cadrage : `recherche_helper_scripts` bloquant (voir [`gates.md`](../../../sensors/gates.md)). Aucun gate humain à ce stage.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de faisabilité, patterns Swarm/Proxmox récurrents) tracés, remontés au gate léger.
