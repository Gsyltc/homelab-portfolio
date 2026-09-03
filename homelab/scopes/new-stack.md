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

Appartenance : voir la matrice scope × phase de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md) et le champ `scopes:`
des fiches de stage ([`../common/stages/`](../common/stages/), livrées au Stage 7).
