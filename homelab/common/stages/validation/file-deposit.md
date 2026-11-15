---
slug: file-deposit
phase: validation
execution: CONDITIONAL
condition: "Après validation humaine explicite, sur confirmation des chemins — N/A pour branches n8n / HA"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: explicit
produces: [depot_fichiers_confirme]
consumes: [{artifact: validation_humaine_explicite, required: true}, {artifact: prerequis_deploiement_verifies, required: true}]
requires_stage: [human-granular-validation]
sensors: [version-livrables, vault-secret-exists]
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Configuration validée + prérequis §répertoire vérifiés + fichiers du répertoire de relecture `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/`"
outputs: "Fichiers déplacés vers les répertoires de travail, vérifiés ; répertoire de relecture nettoyé"
---

# Dépôt des fichiers dans les répertoires de travail (sur confirmation)

## Objectif

Déposer les livrables validés aux emplacements conventionnels, sur confirmation explicite.

## Steps

### Step 1 — Proposer les chemins et attendre confirmation

> Prérequis : la variable `[répertoire de travail]` a été vérifiée ([`deployment-prereqs-check.md`](deployment-prereqs-check.md)).

**Source** : répertoire de relecture `.a-valider/<id-tâche>/<stack>/` ([`review-directory.md`](../../protocols/review-directory.md)).

Avant de proposer le dépôt, le Tech Lead lance `version-livrables` sur `.a-valider/<id-tâche>/<stack>/versions.json` ; sur écart, il ne propose pas le dépôt (retour en Production).

Les chemins de destination sont **proposés dans le message de validation finale** ([`human-granular-validation`](human-granular-validation.md) Step 1, décision 2) ; **la confirmation explicite de cette décision** autorise le déplacement, sans second message. Chemins proposés :

- docker-compose : `${WORK_DIRECTORY}/docker/stacks/[domaine]/[nom-stack].yml` (domaine = valeur `domain` du `config.tfvars` ; convention `<stack>.yml`).
- Terraform : `${WORK_DIRECTORY}/terraform/[type]/[nom-de-la-stack]/config.tfvars` (type = `swarm` si Docker Swarm, `service` si Proxmox ; créer le répertoire s'il n'existe pas).

### Step 2 — Déplacer depuis `.a-valider/`

Après confirmation, **déplacer** (et non copier) les fichiers depuis `.a-valider/<id-tâche>/<stack>/` vers leurs emplacements définitifs. `parametres.json` et `preselection.json` ne sont pas déposés : ils sont supprimés avec le répertoire au Step 4. Ne jamais écraser un fichier existant sans l'avoir signalé à l'humain.

### Step 3 — Vérifier après déplacement

Vérifier les fichiers déplacés : présence à l'emplacement définitif et **`sha256` identique à la version validée** (`versions.json`, déjà contrôlé par `version-livrables` avant le déplacement ; le déplacement ne change pas le contenu). Si l'empreinte correspond, **aucun sensor d'écriture n'est relancé** (`plaintext-secret`, `terraform-no-sni`, `yaml-validity` : verdicts déjà valables pour ce `sha256`). Si elle diffère, le fichier n'est pas déposé : retour en Production. Le seul sensor lancé au dépôt est `vault-secret-exists`.

### Step 3 bis — Écrire les clés Vault (uniquement si la décision 3 du gate final est « oui »)

Hors « oui » explicite à la décision 3 (**absence de réponse = non**), **aucune clé n'est écrite**. Le « oui » vaut pour la liste `vault` (noms et catégories) montrée avec la décision : **une liste modifiée après le « oui » annule l'accord** et la décision est reposée. Sur « oui », le Tech Lead écrit les clés de la liste `vault` de `parametres.json` (noms validés au Cadrage) via la skill `homelab-vault-access` (§ « Écriture encadrée des clés d'une nouvelle stack », [ADR-0054](../../../../decisions/0054-ecriture-vault-creation-cles-nouvelle-stack.md)), après validation du nom de stack (celui de l'`active_step`) et des noms de clés. La catégorie de chaque clé vient de `parametres.json` (`generable`, `variable`, `humain` par défaut) :

- **Créables** : secrets **générables** (clé de chiffrement, secrets JWT, mot de passe de base sans autre usage imposé) générés localement, et variables non secrètes dont la valeur est connue et validée (URL publique, nom de base, issuer, identifiant). Écrits **uniquement s'ils n'existent pas** (jamais d'écrasement).
- **Non créables par le Tech Lead** (restent à l'humain, listées dans le compte rendu par nom) : valeur choisie par l'humain (mot de passe de compte admin), valeur issue d'un système tiers (client secret OIDC créé par Authentik après déploiement Terraform), valeur dérivée de plusieurs autres (URL de connexion contenant un mot de passe).
- **Trace sur l'issue** : nom de chaque clé et statut (`écrite` | `existante, non modifiée` | `à créer par l'humain` | `échec`), **jamais une valeur**. Token révoqué en fin d'opération.
- `vault-secret-exists` contrôle ensuite l'existence des clés écrites (existence seule).

### Step 4 — Nettoyer le répertoire de relecture

Une fois la vérification réussie, supprimer `.a-valider/<id-tâche>/<stack>/` (puis `.a-valider/<id-tâche>/` s'il est vide). En cas d'échec de vérification, **conserver** le répertoire de relecture et le signaler à l'humain.

Exclusion git et règles du répertoire : [`review-directory.md`](../../protocols/review-directory.md).

## Sensors

Outputs: dépôt confirmé + fichiers vérifiés. Action à impact → validation humaine explicite requise (invariant).
Imports: `version-livrables` (gate — lancé **avant le déplacement**, Step 1 : fichiers identiques à la version validée), `vault-secret-exists` (gate — existence seule, **jamais** la valeur).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (conventions de chemins de dépôt) tracés, remontés **en fin de workflow**, dans un message séparé ([`closure`](closure.md)).
