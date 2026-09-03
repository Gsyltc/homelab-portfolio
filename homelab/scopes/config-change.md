---
name: config-change
depth: minimal
verification: advisory
keywords: [variable, valeur, paramètre existant, ajuster valeur, config-change, changement de variable, retouche]
description: "Modification d'une variable existante sans impact sécurité (≈ ancien « allégé ») — allégé, Depth minimale, QA advisory"
---

# Scope `config-change`

Modification d'une **variable existante** (valeur d'un paramètre déjà en place), **sans aucun
impact sécurité**. C'est l'héritier direct de l'ancien **« traitement allégé »** de la grille
binaire : parcours resserré, moins de contrôles intermédiaires, mais **jamais** de transfert de
responsabilité vers le Tech Lead ni de levée de la validation humaine avant action à impact.

Axes par défaut : Depth **`minimal`** (on ne réécrit que ce qui change) et vérification
**`advisory`** (validité YAML + cohérence de base, signalée sans bloquer).

**Garde-fou de bascule (hérité de la règle de départage).** Dès qu'un **doute sur l'impact
sécurité** apparaît, ou dès qu'un déclencheur d'un scope plus élevé s'applique (auth, réseau,
secrets, hardening, Traefik → `security-patch` ; création → `new-stack`), le travail **remonte**
vers ce scope. **Le doute ne bascule jamais vers `config-change`.** L'auto-détection est un
plancher : la confirmation humaine peut monter le contrôle, jamais le descendre sans trace.

Appartenance : voir la matrice scope × phase de
[`../../docs/homelab-workflow.md`](../../docs/homelab-workflow.md) et, à terme, le champ `scopes:`
des fiches de stage (`../common/stages/`, Stage 7).
