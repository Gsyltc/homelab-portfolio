---
name: new-stack
depth: comprehensive
verification: renforcé
keywords: [création, nouvelle stack, nouveau service, déployer, mettre en place, installer, création stack, new stack, création de service]
description: "Création complète d'une nouvelle stack — parcours complet, Depth comprehensive, QA renforcé"
---

# Scope `new-stack`

Création complète d'une **nouvelle stack** (docker-compose et/ou configuration Terraform d'une
stack qui n'existe pas encore). C'est le cas le plus exigeant : toutes les étapes des phases 1 à 3
s'exécutent, y compris l'arbitrage Docker Swarm vs Proxmox (§1.3), la collecte exhaustive des
paramètres (§1.4) et la sélection automatique du type d'authentification.

Axes par défaut : Depth **`comprehensive`** (compose et Terraform détaillés, documentation
complète) et vérification **`renforcé`** (QA Docker complet + audit de sécurité approfondi :
secrets `_FILE`, exposition, permissions, absence de `${SNI}`, durcissement).

**Garde-fou non abaissable** : `depth` ≥ `standard` et `verification` ≥ `renforcé` ne peuvent
jamais être abaissés par override sur ce scope — une création de stack touche par nature au réseau,
aux secrets et à l'exposition.

**Livrable Terraform non abaissable** : sur `new-stack`, la configuration Terraform (`livrable_tfvars`,
stage [`terraform-configuration`](../common/stages/production/terraform-configuration.md)) fait partie
du **garde-fou non abaissable** et **conditionne la clôture**. Elle ne peut être ni sautée, ni reportée,
ni déclarée « non requise » par le Tech Lead : son absence est un **écart bloquant** (gate
`phase3-phase4`, artefact `livrable_tfvars_present`). Le domaine / FQDN d'exposition y est écrit
**en clair** (ex. `https://<service>.<domaine-homelab>`), **jamais `${SNI}`** (invariant SEC-1, sensor
[`terraform-no-sni`](../sensors/sensors/terraform-no-sni.md) **bloquant** sur ce scope). Toute levée est
une **décision humaine explicite tracée**, jamais une décision du Tech Lead seul.

Appartenance : voir la matrice scope × phase de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md) et le champ `scopes:`
des fiches de stage ([`../common/stages/`](../common/stages/), livrées au Stage 7).
