---
slug: intent-scope-approval
phase: ideation
execution: ALWAYS
condition: "Always executes — gate humain léger"
lead_agent: Tech Lead Homelab
support_agents: []
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: light
produces: [intention_perimetre_approuves, scope_confirme, arbitrage_swarm_proxmox, label_cible_pose, fqdn_valide, auth_type_valide, database_service_valide]
consumes: [{artifact: intention_capturee, required: true}, {artifact: scope_propose, required: true}, {artifact: axes_proposes, required: true}, {artifact: cibles_disponibles, required: true}, {artifact: auth_type_preselectionne, required: true}, {artifact: database_service_preselectionne, required: true}]
requires_stage: [scope-detection, deployment-target-preselection, auth-preselection, database-preselection]
sensors: [initial-proposal]
scopes: [stack-update, new-stack, config-change, security-patch, infra-terraform]
inputs: "Intention capturée, scope + axes proposés"
outputs: "Intention + périmètre approuvés (gate léger), scope confirmé"
---

# Approbation de l'intention et du périmètre (gate humain léger)

## Objectif

Valider *qu'on part dans la bonne direction* et confirmer le scope, avant d'engager le Cadrage.

## Steps

### Step 1 — Présenter la proposition initiale

C'est la **première sollicitation de l'humain** : tout ce qui précède s'exécute sans question (sauf intention ambiguë, `intent-capture`). Un seul message, au format suivant, chaque point numéroté et validé séparément (Keep / Modify / Redo) :

```
1. Intention : <reformulation>
2. Scope : <scope> — axes Depth <…> / vérification <…>
3. Cible de déploiement :
   - Proxmox : <lien du script Helper-Scripts>      (si disponible)
   - Docker Swarm : <image>                         (si disponible)
4. FQDN : <valeur complète, ex. sync-in.jeedom-gaston.ovh> — ce domaine te convient-il ?
5. Authentification recommandée : <type> — <justification + lien doc> | à trancher : <options>
6. Base de données recommandée : <postgres (mutualisé) | mariadb | … | none> — <justification + lien doc> | à trancher : <options>
```

Point 3 : options issues de [`deployment-target-preselection`](../initialisation/deployment-target-preselection.md), seules les disponibles sont listées. Deux options → l'humain choisit. Une seule → elle est retenue, l'indiquer (ex. « Docker Swarm retenu, aucun script Proxmox trouvé — variantes testées : … »). Stack existante → cible actuelle. Ne jamais présumer le choix.
Point 4 : valeur calculée selon la règle `${fqdn}` de [`required-parameters-collection`](../cadrage/required-parameters-collection.md), jamais un gabarit. Point 5 : résultat de [`auth-preselection`](../initialisation/auth-preselection.md). Point 6 : résultat de [`database-preselection`](../initialisation/database-preselection.md). Points 3 à 6 : stacks uniquement.

### Step 2 — Gate léger (Keep / Modify / Redo)

L'humain approuve ou ajuste. C'est un gate **léger** : il valide *quoi* et *jusqu'où*, pas *comment* (les paramètres détaillés sont figés en Cadrage). Sur les scopes légers (`config-change`), ce gate reste **resserré** mais n'est jamais supprimé. Rien n'engage le Cadrage tant que l'intention et le périmètre ne sont pas approuvés et le scope confirmé (l'auto-détection est un plancher : la confirmation peut monter le contrôle, jamais le descendre sans trace).

### Step 3 — Poser le label de cible

Une fois la cible validée au point 3, poser sur l'issue (et sur ses sous-issues de livrable) le label correspondant : **Docker Swarm** → `Docker Swarm` ; **Proxmox** → `Proxmox`. Jamais avant cette validation.

## Sensors

Outputs: intention + périmètre approuvés, scope confirmé, cible (`arbitrage_swarm_proxmox`), `${fqdn}`, `${auth_type}` et `${database_service}` validés (repris en Cadrage sans redemander). Imports: `initial-proposal` (gate — ✅ requis avant de poster la proposition ; bloquant sur `new-stack` / `infra-terraform`). Frontière **Idéation → Cadrage** : gate `artefacts-presents` (intention, scope confirmé) + approbation périmètre tracée — voir [`homelab/sensors/gates.md`](../../../sensors/gates.md).
Imports: none.

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : ce stage **porte le gate humain léger** d'Idéation — le Tech Lead y remonte les candidats-règles capturés depuis `intent-capture`, formulés en règles courtes (couche + portée proposées). L'humain garde ✅ / rejette ❌ / reformule 💬 chaque candidat séparément ; persistance des apprentissages **confirmés** dans `homelab/rules/` (jamais dans le run courant — application au prochain workflow).
