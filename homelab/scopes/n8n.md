---
name: n8n
depth: standard
verification: standard
branch: autonome
keywords: [n8n]
description: "Toute demande n8n — branche autonome, délégation IMMÉDIATE à l'Expert N8n (règle absolue §1.1)"
---

# Scope `n8n`

Toute demande concernant **n8n** (création, modification, diagnostic, optimisation d'un flux ;
mot « n8n » dans la demande, un titre d'issue ou une référence de flux).

**Règle absolue n8n (§1.1) — préservée telle quelle, non désactivable par aucun scope.** Dès que
« n8n » apparaît, le Tech Lead **délègue IMMÉDIATEMENT** à l'Expert N8n par mention valide, avec
mission claire, et **arrête** le flux stack. **Aucune exception, pas même l'analyse** : le Tech
Lead n'exécute rien lui-même. Cette bascule court-circuite l'auto-détection de tout autre scope —
`n8n` est **prioritaire** (au même rang que `home-assistant`).

Branche **autonome** : une demande n8n ne passe **pas** par le Spécialiste Docker / QA Docker /
Spécialiste Terraform. L'Expert N8n propose, applique après feu vert du Tech Lead **puis validation
humaine**, et mentionne le Tech Lead en fin de travail.

Axes par défaut : Depth `standard`, vérification `standard` (adaptés au contrôle propre au domaine
n8n ; le QA Docker « compose » ne s'applique pas à cette branche).

**Validation humaine granulaire préservée** : aucune application réelle d'un flux sans feu vert
humain explicite.

Appartenance : voir la matrice scope × phase de
[`../../docs/homelab-workflow.md`](../../docs/homelab-workflow.md) et, à terme, le champ `scopes:`
des fiches de stage (`../common/stages/`, Stage 7).
