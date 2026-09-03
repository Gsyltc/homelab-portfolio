# Agents — équipe DevOps Homelab

Définitions conformes (front-matter YAML + corps Markdown, même format que [`core/agents/`](../../core/agents/)) des agents de l'équipe DevOps Homelab, coordonnée par le **Tech Lead Homelab**. Le workflow de référence est [`../common/conductor.md`](../common/conductor.md) (une fois créé au stage dédié) ; en attendant, `docs/homelab-workflow.md`.

## Rôles génériques → fichiers

| Rôle générique (workflow) | Fichier | Objet |
|---|---|---|
| Tech Lead Homelab | [tech-lead-homelab-agent.md](tech-lead-homelab-agent.md) | Coordinateur + contrôleur qualité central ; délègue aux spécialistes, applique le verrou par stack, demande la validation humaine. |
| Spécialiste Docker | [docker-specialist-agent.md](docker-specialist-agent.md) | Crée/modifie les docker-compose optimisés Swarm. Produit le livrable. |
| QA Docker | [qa-docker-agent.md](qa-docker-agent.md) | Vérifie et corrige les docker-compose (YAML, Swarm, hardening, Traefik). Intervient après création. |
| Spécialiste Terraform | [terraform-specialist-agent.md](terraform-specialist-agent.md) | Écrit/modifie les `.tf`/`.tfvars`. **N'exécute jamais** init/apply/destroy ; pas de `${SNI}`. |
| Expert n8n | [n8n-expert-agent.md](n8n-expert-agent.md) | Crée/modifie/diagnostique les flux n8n via MCP. Branche autonome (règle absolue n8n). |
| Expert Home Assistant | [home-assistant-expert-agent.md](home-assistant-expert-agent.md) | Pilote Home Assistant via MCP officiel. Double validation avant toute action réelle. |

## Agent partagé (non dupliqué ici)

- **Agent de notifications (Alfred)** — utilitaire de workspace partagé entre les deux workflows. Sa définition conforme unique vit dans [`core/agents/notification-agent.md`](../../core/agents/notification-agent.md) (source unique de vérité) ; le Tech Lead Homelab le mentionne via l'UUID `254d9349-1eb3-4f50-a4cd-b18a7043a7c0`. Pas de duplication sous `homelab/agents/` pour éviter deux sources divergentes.

## Correspondance UUID (moteur A2A Multica)

Les délégations se font par mention `[@Label](mention://agent/<uuid>)`. La table des UUID fait foi dans [tech-lead-homelab-agent.md](tech-lead-homelab-agent.md) ; vérifier via `multica agent list --output json` (champ `id`), ne jamais inventer un UUID.

## Garde-fous absolus (rappel)

Règle absolue n8n · Terraform ne déploie jamais · un seul traitement par stack (verrou `active_step`) · aucun secret exposé · jamais `${SNI}` en Terraform · validation humaine avant toute action à impact (dépôt de fichiers, Kestra, n8n, Home Assistant).
