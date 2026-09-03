---
name: home-assistant
depth: standard
verification: standard
branch: autonome
keywords: [home assistant, home-assistant, HA, entité, scène, automatisation, script HA]
description: "Toute demande Home Assistant — branche autonome, délégation à l'Expert Home Assistant"
---

# Scope `home-assistant`

Toute demande concernant **Home Assistant** (entités, scènes, automatisations, scripts) via le
serveur MCP officiel.

Branche **autonome** : une demande Home Assistant ne passe **pas** par le Spécialiste Docker / QA
Docker / Spécialiste Terraform. Le Tech Lead délègue à l'**Expert Home Assistant**, qui propose ;
la séquence est **proposition → vérification par le Tech Lead → validation humaine explicite →
seulement ensuite modification réelle**. L'Expert Home Assistant mentionne le Tech Lead en fin de
travail.

`home-assistant` est **prioritaire** dans la désambiguïsation (au même rang que `n8n`) : il
court-circuite l'auto-détection des scopes stack dès qu'une tâche Home Assistant est identifiée.

Axes par défaut : Depth `standard`, vérification `standard` (adaptés au domaine Home Assistant ;
le QA Docker « compose » ne s'applique pas à cette branche).

**Validation humaine granulaire préservée** : aucune modification réelle sans feu vert humain
explicite.

Appartenance : voir la matrice scope × phase de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md) et le champ `scopes:`
des fiches de stage ([`../common/stages/`](../common/stages/), livrées au Stage 7).
