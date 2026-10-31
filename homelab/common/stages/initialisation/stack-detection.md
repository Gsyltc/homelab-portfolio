---
slug: stack-detection
phase: initialisation
execution: ALWAYS
condition: "Always executes — bootstrap déterministe"
lead_agent: null
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
human_gate: none
produces: [detection_stack_existante_vs_nouvelle, type_service_detecte]
consumes: []
requires_stage: []
sensors: []
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform, service-version-update, n8n, home-assistant]
inputs: "Demande brute"
outputs: "Nature consignée (mise à jour de version vs modification/correctif/patch vs nouvelle stack) ; pour une mise à jour de version : existence de la stack vérifiée et type consigné (Docker Swarm vs Proxmox), sinon issue blocked"
---

# Détection « stack existante vs nouvelle »

## Objectif

Déterminer de façon déterministe si la demande vise une stack existante ou une nouvelle stack.

## Steps

### Step 1 — Où chercher (localisation)

Le dépôt homelab-portfolio ne contient QUE le workflow ; les fichiers de
travail sont dans le workspace, aux emplacements définis par le workflow
(voir [`file-deposit.md`](../validation/file-deposit.md)). Une stack
existante se localise via ces emplacements, jamais dans le dépôt du workflow.

### Step 2 — Déterminer la nature

Analyser la demande pour trancher sa **nature** :

- **mise à jour de version** d'une stack existante (`service-version-update`) ;
- **modification** d'une stack existante — correctif / patch de sécurité (`stack-update` / `config-change` / `security-patch`) ;
- **création** d'une nouvelle stack (`new-stack`).

### Step 3 — Mise à jour de version : vérifier l'existence et consigner le type

**Uniquement si la nature est une mise à jour de version** : s'assurer que la stack **existe** dans
le répertoire de travail `${WORK_DIRECTORY}`. La recherche se fait dans :

- `${WORK_DIRECTORY}/terraform/swarm/<service>` → **stack Docker Swarm** ;
- `${WORK_DIRECTORY}/terraform/services/<service>` → **service Proxmox**.

Si le service **existe**, consigner qu'il s'agit d'un service **Docker Swarm** ou **Proxmox** (le
type est tranché par la localisation du fichier, jamais supposé). Si le service **n'est pas
détecté** des deux côtés → **halt-and-ask** : passer l'issue en **`blocked`** et **demander à
l'humain** par une mention explicite (service introuvable sous ces chemins, confirmer
l'emplacement). **Ne jamais deviner le type ni poursuivre** sans réponse.

### Step 4 — Consigner (sans valider)

Consigner le fait en commentaire (piste d'audit). Il **oriente** l'auto-détection du scope en Idéation (`stack-update` / `config-change` / `security-patch` / `service-version-update` vs `new-stack`) sans figer la décision. Ce n'est **pas** un gate.

## Sensors

Outputs: fait de détection consigné sur l'issue. Aucun gate humain (bootstrap déterministe). **Exception — halt-and-ask** : pour une mise à jour de version, si la stack est introuvable sous `${WORK_DIRECTORY}/terraform/swarm/<service>` et `${WORK_DIRECTORY}/terraform/services/<service>`, l'issue passe `blocked` et l'humain est interrogé par mention explicite ; aucune suite n'est engagée sans réponse.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : tenir le journal des candidats-règles sur l'issue. Stage d'Initialisation (bootstrap déterministe) → **saute** l'interaction liée au gate humain ; aucune règle n'est écrite hors du cycle capture → confirmation humaine → contrôle de conflit.
