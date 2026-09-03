---
name: infra-terraform
depth: standard
verification: standard
keywords: [terraform, proxmox, infrastructure, infra, tfvars, provider, VM, LXC, réseau infra, community-scripts]
description: "Infra Terraform / Proxmox — accent Spécialiste Terraform, Terraform ne déploie jamais"
---

# Scope `infra-terraform`

Travaux d'infrastructure centrés **Terraform / Proxmox** (variables de stack `.tfvars`, ressources
VM / LXC, arbitrage Proxmox vs Docker Swarm §1.3). Accent sur le **Spécialiste Terraform**, qui
prépare uniquement les fichiers `.tf` / `.tfvars`.

Axes par défaut : Depth `standard`, vérification `standard`.

**Garde-fous absolus rappelés (insensibles au scope) :**

- **Terraform ne déploie JAMAIS** : `terraform init/apply/destroy` sont interdits au Spécialiste
  Terraform ; il ne produit que les fichiers, jamais l'exécution.
- **Jamais `${SNI}`** dans un livrable Terraform (vérifié en Phase 2 et par le sensor dédié,
  Stage 4).
- Aucun secret en clair dans les `.tfvars` livrés.

**Escalade sécurité.** Si le travail Terraform touche l'authentification, l'exposition, les
secrets ou le réseau de façon structurante, il **remonte** vers `security-patch` (vérification
`renforcé`). Le doute ne descend jamais.

Appartenance : voir la matrice scope × phase de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md) et le champ `scopes:`
des fiches de stage ([`../common/stages/`](../common/stages/), livrées au Stage 7).
