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
outputs: "Existence vérifiée sur le système de fichiers `${WORK_DIRECTORY}` pour TOUTE demande (terraform/swarm, terraform/services, docker/stacks) ; nature consignée (existante → modification/mise à jour vs nouvelle stack) et type consigné (Docker Swarm vs Proxmox) d'après la localisation trouvée ; mise à jour de version avec service introuvable → issue blocked"
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

### Step 2 — OBLIGATOIRE : vérifier l'existence sur le système de fichiers (toute demande)

**Pour TOUTE demande**, la nature « existante vs nouvelle » est tranchée par le **système de fichiers** de `${WORK_DIRECTORY}`,
**jamais** par les seuls mots de la demande (un verbe comme « déployer », « créer » ou
« lancer » n'implique pas qu'il s'agit d'une nouvelle stack). Rechercher le service sous **tous**
les emplacements conventionnels (voir [`../validation/file-deposit.md`](../validation/file-deposit.md)) :

- `${WORK_DIRECTORY}/terraform/swarm/<service>` → configuration **Docker Swarm** ;
- `${WORK_DIRECTORY}/terraform/services/<service>` → configuration **service Proxmox** ;
- `${WORK_DIRECTORY}/docker/stacks/<domaine>/<service>.yml` → **docker-compose** de la stack
  (le domaine n'est pas connu a priori : balayer les sous-répertoires de
  `${WORK_DIRECTORY}/docker/stacks/`, p. ex. `administration/`, `applications/`, `monitoring/`…).

Le **type** (Docker Swarm vs Proxmox) est tranché par la **localisation** du fichier trouvé,
jamais supposé. La recherche se fait sur la **variable réelle `${WORK_DIRECTORY}`** résolue dans
l'environnement de l'agent, **jamais** dans un checkout du dépôt du workflow ni un autre
répertoire de travail.

### Step 3 — Déterminer la nature à partir du résultat du Step 2

- **Au moins un artefact trouvé** (`.tfvars` et/ou docker-compose) ⇒ la stack **existe** : la
  nature est une **modification / mise à jour** (`service-version-update` / `stack-update` /
  `config-change` / `security-patch`, tranché en Idéation). Consigner les chemins exacts trouvés
  et le type détecté. **Ne jamais classer en `new-stack` lorsqu'un artefact existe.**
- **Aucun artefact trouvé** sous aucun des emplacements ci-dessus ⇒ la nature est une
  **création** de nouvelle stack (`new-stack`). Consigner explicitement les emplacements balayés
  (preuve de l'absence).
- **Mise à jour de version avec service introuvable** (nature = mise à jour de version annoncée
  mais aucun artefact détecté) → **halt-and-ask** : passer l'issue en **`blocked`** et **demander
  à l'humain** par une mention explicite (service introuvable sous ces chemins, confirmer
  l'emplacement). **Ne jamais deviner le type ni poursuivre** sans réponse.

### Step 4 — Consigner (sans valider)

Consigner le fait en commentaire (piste d'audit) : nature retenue, emplacements balayés, chemins
trouvés et type détecté. Il **oriente** l'auto-détection du scope en Idéation (`stack-update` /
`config-change` / `security-patch` / `service-version-update` vs `new-stack`) sans figer la
décision. Ce n'est **pas** un gate.

## Sensors

Outputs: fait de détection consigné sur l'issue, appuyé sur la vérification d'existence du Step 2 effectuée pour **toute** demande (balayage de `${WORK_DIRECTORY}/terraform/swarm`, `${WORK_DIRECTORY}/terraform/services` et `${WORK_DIRECTORY}/docker/stacks/*`). Aucun gate humain (bootstrap déterministe). **Exception — halt-and-ask** : pour une mise à jour de version, si la stack est introuvable sous aucun de ces emplacements, l'issue passe `blocked` et l'humain est interrogé par mention explicite ; aucune suite n'est engagée sans réponse.
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : tenir le journal des candidats-règles sur l'issue. Stage d'Initialisation (bootstrap déterministe) → **saute** l'interaction liée au gate humain ; aucune règle n'est écrite hors du cycle capture → confirmation humaine → contrôle de conflit.
