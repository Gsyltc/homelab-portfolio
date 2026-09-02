---
name: homelab-stack-workflow
description: "Workflow de création et modification d'une stack Homelab : analyse, vérification images Docker vs script Proxmox (community-scripts.org), arbitrage humain Docker Swarm/Proxmox, collecte des paramètres (authentification, base de données, Valkey, HashiCorp Vault), délégation aux agents spécialisés, gestion Terraform, validation humaine; flux Kestra configure_service. Utiliser pour toute création ou modification de stack."
---
Workflow officiel à suivre pour TOUTE demande de création ou de modification d'une stack du Homelab. Ne jamais sauter d'étape ni deviner une information manquante.

## Étape 1 — Analyser la demande

- Identifier l'objectif : nouvelle stack ou modification d'une stack existante.
- Dégager les exigences : services, images, ports, volumes, réseaux, versions, dépendances.
- Consigner l'analyse dans le suivi de l'issue.

## Étape 2 — Vérifications préalables

Vérifier les deux points suivants AVANT toute suite :

1. **Images Docker** : les images Docker nécessaires à la stack existent-elles (Docker Hub, ghcr.io, registres officiels) ?
2. **Alternative Proxmox** : existe-t-il un script d'installation Proxmox équivalent sur https://community-scripts.org/ ?

**Règle de décision :**
- Si les DEUX existent (images Docker ET script Proxmox) → STOP. Demander à l'humain de choisir entre **Docker Swarm** et **Proxmox**, et attendre sa réponse explicite avant de continuer.
- Si seul l'un des deux existe → poursuivre avec la solution disponible et le signaler à l'humain.

## Étape 3 — Choix Docker Compose : collecte des informations puis délégation

Si le choix retenu est **Docker Compose** :

### 3a. Informations requises avant de lancer les agents

Vérifier que ces informations figurent dans l'issue. Si une seule manque, la demander à l'humain et ATTENDRE sa réponse — ne rien lancer tant qu'elles ne sont pas complètes :

1. **Type d'authentification ?** (`none`, `local`, `forwardauth`, `oidc`)
2. **Utilisation d'une base de données ?** (`postgres`, `mysql`, `mariadb`, `mongodb`, `none`)
3. **Utilisation du cache Valkey ?** (`true` / `false`)
4. **Création ou modification des variables d'environnement / secrets dans HashiCorp Vault ?** (un agent dédié sera créé plus tard pour cette tâche ; en attendant, le signaler à l'humain)

### 3b. Délégation

Appeler les agents concernés par commentaire sur l'issue avec mention valide (mission claire : objectif, périmètre, critères d'acceptation) :

- **Bob** : création ou modification du fichier docker-compose.
- **Kevin** : vérification du fichier généré et compatibilité Docker Swarm.

Contrôler ensuite leur travail avant toute passage en revue.

## Étape 4 — Variables Terraform

Lancer la création ou la modification de la configuration des variables Terraform correspondant à la stack (cohérence avec les paramètres collectés à l'étape 3).

## Étape 5 — Validation humaine puis Kestra

- Soumettre la configuration complète à l'humain pour validation explicite.
- **Uniquement lorsque l'humain a validé** : lancer le flux Kestra `configure_service`.

## Règles transverses

- Information requise manquante → demander à l'humain et attendre. Jamais de supposition.
- Chaque étape franchie est documentée dans le suivi de l'issue.
- Aucun lancement du flux Kestra sans validation humaine explicite.
