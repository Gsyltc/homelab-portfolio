---
name: stack-update
depth: standard
verification: standard
keywords: [modification, mise à jour, update, évolution, ajustement, stack existante, ajout service, changement]
description: "Modification d'une stack existante — parcours standard complet (scope par défaut)"
---

# Scope `stack-update` *(défaut)*

Modification ou évolution d'une **stack existante** (ajout/retrait de service, changement de
version d'image, ajustement de configuration structurante) sans qu'il s'agisse d'une création
complète ni d'une simple variable. C'est le **scope par défaut** en l'absence de mot-clé détecté —
aucune régression par rapport au parcours Homelab historique « traitement complet allégé au juste
nécessaire ».

Les phases de cadrage (Phase 1), de production et contrôle (Phase 2) et de validation/déploiement
(Phase 3) s'exécutent ; les étapes sans valeur pour une modification ciblée peuvent être allégées
par le Tech Lead, sans jamais transférer une responsabilité de spécialiste vers le Tech Lead.

Axes par défaut : Depth `standard`, vérification `standard` (QA Docker complet : Swarm `deploy`,
réseaux/volumes/secrets, hardening standard, cohérence Traefik). Overridable à la hausse à la
confirmation de scope.

Appartenance : voir la matrice scope × phase de
[`../../docs/homelab-workflow.md`](../../docs/homelab-workflow.md) et, à terme, le champ `scopes:`
des fiches de stage (`../common/stages/`, Stage 7).
