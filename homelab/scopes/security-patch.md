---
name: security-patch
depth: comprehensive
verification: renforcé
keywords: [sécurité, security, hardening, durcissement, secret, secrets, auth, authentification, exposition, permissions, Traefik, réseau, vulnérabilité, CVE, correctif sécurité, faille]
description: "Tout impact sécurité (auth, réseau, secrets, hardening, Traefik) — QA Docker renforcé, traçabilité accrue"
---

# Scope `security-patch`

**Toute modification à impact sécurité** — logicielle ou infrastructure : authentification, réseau,
exposition, secrets, hardening, permissions, routes Traefik. Correspond au déclencheur « Complet »
le plus sensible de l'ancienne grille. Périmètre resserré, traçabilité renforcée, analyse
d'impact / non-régression du correctif produite avant recommandation.

Axes par défaut : Depth **`comprehensive`**, vérification **`renforcé`** — le QA Docker mène un
audit de sécurité approfondi (secrets `_FILE`, absence de secret en clair, exposition minimale,
permissions, absence de `${SNI}` en Terraform, durcissement complet, cohérence Traefik via
`traefik-manager-read`).

**Garde-fou non abaissable** : `depth` ≥ `standard` et `verification` ≥ `renforcé` ne peuvent
**jamais** être abaissés par override. Tout re-scoping abaissant le contrôle d'un travail détecté
comme sécuritaire exige une **validation humaine explicite tracée** sur l'issue.

**Priorité de désambiguïsation.** En cas de correspondances multiples, `security-patch` l'emporte
sur `new-stack`, `infra-terraform`, `stack-update` et `config-change` (seules les branches
autonomes `n8n` / `home-assistant` court-circuitent en amont).

Appartenance : voir la matrice scope × phase de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md) et le champ `scopes:`
des fiches de stage ([`../common/stages/`](../common/stages/), livrées au Stage 7).
