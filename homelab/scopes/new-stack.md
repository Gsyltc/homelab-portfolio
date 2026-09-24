---
name: new-stack
depth: comprehensive
verification: renforcé
keywords: [création, nouvelle stack, nouveau service, déployer, mettre en place, installer, création stack, new stack, création de service]
description: "Création complète d'une nouvelle stack — parcours complet, Depth comprehensive, QA renforcé"
---

# Scope `new-stack`

Création complète d'une **nouvelle stack** (docker-compose et configuration Terraform d'une
stack qui n'existe pas encore). C'est le cas le plus exigeant : toutes les étapes des phases 1 à 3
s'exécutent, y compris l'arbitrage Docker Swarm vs Proxmox (§1.3), la collecte exhaustive des
paramètres (§1.4) et la sélection automatique du type d'authentification.

Axes par défaut : Depth **`comprehensive`** (compose et Terraform détaillés, documentation
complète) et vérification **`renforcé`** (vérification QA complète + audit de sécurité approfondi :
secrets `_FILE`, exposition, permissions, absence de `${SNI}`, durcissement).

**Garde-fou non abaissable** : `depth` ≥ `standard` et `verification` ≥ `renforcé` ne peuvent
jamais être abaissés par override sur ce scope — une création de stack touche par nature au réseau,
aux secrets et à l'exposition.

**Livrable Terraform obligatoire (non abaissable).** Sur ce scope, le stage
`terraform-configuration` s'exécute **toujours** : le livrable `.tfvars` (`livrable_tfvars`) fait
partie intégrante du parcours et **conditionne la clôture**. Il ne peut être ni sauté ni traité
comme optionnel — pas même sur décision d'un agent coordinateur. Son absence est un **écart
bloquant** à la frontière Production → Validation (voir `gates.md`, frontière `phase3-phase4`),
cohérent avec le sensor `terraform-no-sni` déjà bloquant sur `new-stack`. Le domaine / FQDN
d'exposition y est écrit **en clair**, jamais via `${SNI}`.

Appartenance : voir la matrice scope × phase de `scopes-and-axes.md` et le champ `scopes:`
des fiches de stage (`homelab/common/stages/`, livrées au Stage 7).
