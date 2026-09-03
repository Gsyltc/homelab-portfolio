---
title: Scopes Homelab — un fichier par scope (source d'identité)
contract: Contrat amont « Scopes » (miroir de core/scopes/, adapté au Homelab)
---

# Scopes Homelab — un fichier de données par scope

Cette couche porte l'**identité** de chaque scope du workflow Homelab, en données déclaratives.
Elle est le pendant Homelab de [`../../core/scopes/`](../../core/scopes/README.md) : même forme
déclarative, vocabulaire et scopes **spécifiques au Homelab** (Docker Swarm / Proxmox / Terraform /
n8n / Home Assistant).

## Le contrat en deux moitiés

Un scope se déclare en **deux endroits**, et cette séparation est l'idée maîtresse :

1. **L'identité** vit dans son propre fichier — `homelab/scopes/<name>.md` (un fichier par scope,
   à l'image de `homelab/sensors/` et de `core/scopes/`). Il porte le nom du scope, ses
   métadonnées de routage (`keywords`) et ses **valeurs par défaut** d'axes (`depth`,
   niveau de vérification → `verification`).
2. **L'appartenance** (quels stages s'exécutent sous ce scope) vit **transposée sur les
   stages** : chaque fiche de stage (`homelab/common/stages/<phase>/<slug>.md`, produite au
   Stage 7) nommera dans son front-matter `scopes:` les scopes sous lesquels elle s'exécute. Un
   stage qui ne nomme pas un scope est ignoré (`SKIP`) sous ce scope ; les stages
   d'**Initialisation** nomment **tous** les scopes (ils s'exécutent toujours).

La liaison entre les deux est le **nom du scope**. L'appartenance est ainsi déclarée **une seule
fois, sur le stage**, jamais redéclarée dans sept blocs de scope séparés.

> **Ordre de livraison.** Les fiches de stage `homelab/common/stages/` sont créées au **Stage 7**
> (modèle conductor / stages / protocols). En attendant, la **vue lisible** — matrice scope × phase
> ci-dessous — porte l'appartenance de façon consolidée et lisible, adossée aux **3 phases
> actuelles** de `docs/homelab-workflow.md` ; elle sera re-projetée sur les 5 phases au Stage 5,
> puis transposée sur le champ `scopes:` des fiches de stage au Stage 7.

> **Source d'identité.** Ces fichiers sont la **source d'identité** des scopes. La matrice
> ci-dessous et la section « Scopes » de [`../../docs/homelab-workflow.md`](../../docs/homelab-workflow.md)
> restent des **vues lisibles** ; en cas d'écart sur l'identité d'un scope (nom, depth, mots-clés,
> vérification), **le fichier de scope fait foi**.

## Schéma du front-matter

```yaml
name: <scope>                 # requis — nom du scope (= stem du fichier)
depth: minimal|standard|comprehensive     # requis — détail des artefacts par défaut
verification: advisory|standard|renforcé  # requis — intensité du QA Docker par défaut
branch: false|autonome                    # optionnel — branche autonome (n8n / Home Assistant)
keywords: [ ... ]             # optionnel — déclencheurs d'auto-détection FR / EN (liste plate)
description: "<une ligne>"    # optionnel — libellé court (vue d'aide / lisible)
```

Le corps Markdown qui suit le front-matter porte l'**intention en prose** : pourquoi ces stages,
pourquoi ceux-là sont allégés, ignorés ou renforcés.

## Les deux axes

Le routage repose sur un **scope** nommé (parcours d'étapes déterministe et auditable) et **deux
axes indépendants** :

- **Axe 1 — Depth** (`minimal` / `standard` / `comprehensive`) : détail des artefacts produits
  (docker-compose, config Terraform, documentation). Contrôle *combien on écrit*.
- **Axe 2 — Stratégie de vérification** (`advisory` / `standard` / `renforcé`) : **intensité du
  QA Docker** et du contrôle qualité central. Contrôle *à quel point on vérifie*.
  - `advisory` — validité YAML + cohérence de base (syntaxe seule), signalé sans bloquer.
  - `standard` — vérification complète : Swarm `deploy`, réseaux/volumes/secrets, hardening
    standard, cohérence Traefik (`traefik-manager-read`).
  - `renforcé` — vérification `standard` **plus** audit de sécurité renforcé (secrets `_FILE`,
    exposition, permissions, absence de `${SNI}` en Terraform, revue durcissement approfondie).

Les deux axes sont **indépendants** l'un de l'autre et du scope ; chaque scope porte des valeurs
par défaut **overridables** (voir points d'override plus bas).

## Garde-fous (non désactivables par un scope)

Rappel des invariants du workflow Homelab — **aucun scope ne les désactive** :

- **Validation humaine granulaire** avant toute action à impact (dépôt de fichiers, flux Kestra) —
  NON négociable, quel que soit le scope ou les axes.
- **Règle absolue n8n** (§1.1) : toute demande n8n déclenche le scope `n8n` et une délégation
  immédiate à l'Expert N8n — pas même l'analyse par le Tech Lead. Un scope ne peut pas la lever.
- **Sélection automatique du type d'authentification** (§1.4, `oidc → saml → ldap → forwardauth →
  local`) préservée telle quelle ; en cas de doute → humain.
- **Terraform ne déploie JAMAIS** (`terraform init/apply/destroy` interdits), **aucun secret en
  clair**, **jamais `${SNI}`** dans un livrable Terraform, **un seul traitement par stack**
  (verrou `active_step`) — garde-fous absolus, insensibles au scope.
- Sur `security-patch` / `new-stack` : `depth` ≥ `standard` et `verification` ≥ `renforcé` ne
  peuvent jamais être abaissés par override.
- **Auto-détection = plancher** : la confirmation humaine peut *monter* le contrôle, jamais le
  *descendre* sans validation tracée.

## Auto-détection & désambiguïsation

Scope auto-détecté par mots-clés (FR / EN, champ `keywords:` de chaque fichier) puis **confirmé
explicitement** avant démarrage (jamais de démarrage silencieux). En cas de correspondances
multiples, **le niveau le plus élevé l'emporte** ; ordre de priorité :

`n8n` = `home-assistant` (branches autonomes, court-circuit immédiat) > `security-patch` >
`new-stack` > `infra-terraform` > `stack-update` > `config-change`

**Le doute ne bascule jamais vers `config-change`** (héritage direct de la règle de départage
« allégé vs complet »). Défaut : **`stack-update`** en l'absence de mot-clé détecté.

## Points d'override

Les axes se relèvent (jamais s'abaissent sans trace) à trois moments : à l'invocation, à la
confirmation de scope, ou à un verification gate (Stage 4). Tout abaissement d'un niveau lié à la
sécurité exige une **validation humaine explicite tracée** sur l'issue.

## Non applicable ici (tooling amont)

Pas de compilation `scope-grid.json`, pas de moteur TypeScript, pas de champs `runner` /
`freeform_default` : l'exécution passe par **Multica** (mentions UUID, `trigger_outcomes`, statut
d'issue, verrou metadata, piste d'audit), pas par le harness AI-DLC. On adopte la **forme
déclarative** (un fichier par scope, front-matter, appartenance transposée) sans importer le moteur.

## Table des scopes

| Scope | Intention type | Depth défaut | Vérification défaut |
| --- | --- | --- | --- |
| [`stack-update`](stack-update.md) *(défaut)* | Modification d'une stack existante | standard | standard |
| [`new-stack`](new-stack.md) | Création complète d'une nouvelle stack | comprehensive | renforcé |
| [`config-change`](config-change.md) | Modification d'une variable existante (≈ « allégé ») | minimal | advisory |
| [`security-patch`](security-patch.md) | Tout impact sécurité (auth, réseau, secrets, hardening, Traefik) | comprehensive | renforcé |
| [`infra-terraform`](infra-terraform.md) | Infra Terraform / Proxmox | standard | standard |
| [`n8n`](n8n.md) | Toute demande n8n — branche autonome, délégation immédiate | standard | standard |
| [`home-assistant`](home-assistant.md) | Toute demande Home Assistant — branche autonome | standard | standard |

Voir la **matrice scope × phase** dans [`../../docs/homelab-workflow.md`](../../docs/homelab-workflow.md)
(section « Scopes et axes d'exécution ») pour l'activation étape par étape et l'affectation des agents.
