---
slug: version-impact-analysis
phase: ideation
execution: CONDITIONAL
condition: "Scope service-version-update — mise à jour d'un service existant sur une nouvelle version disponible"
lead_agent: Tech Lead Homelab
support_agents: [Spécialiste Docker, Spécialiste Terraform]
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: none
produces: [analyse_impact_version]
consumes: [{artifact: intention_capturee, required: true}, {artifact: type_service_detecte, required: true}]
requires_stage: [intent-capture, stack-detection]
sensors: []
scopes: [service-version-update]
inputs: "Intention capturée : service existant + nouvelle version visée (service, version, release GitHub)"
outputs: "Analyse d'impact de version consignée (type de service, version actuelle Vault, breaking changes / enjeux de config) ; issue blocked si enjeu détecté"
---

# Analyse d'impact de version

## Objectif

Déterminer si la montée de version d'un service existant est sûre à appliquer, ou si elle porte un
enjeu (breaking change, version non stable, migration de configuration) qui doit bloquer le parcours.

## Steps

### Step 1 — Réutiliser le type de service (déterminé en Initialisation)

Le **type** du service — **stack Docker Swarm** ou **service Proxmox** — a **déjà** été déterminé et consigné par le stage d'Initialisation [`stack-detection`](../initialisation/stack-detection.md). Ce stage le **réutilise tel
quel**, il ne le redétecte pas : le service **existe déjà** et le type est acquis.

### Step 2 — Lire la version actuelle dans Vault (lecture seule)

Via la skill [`homelab-vault-access`](../../../../plugins/homelab-assistant/skills/homelab-vault-access/SKILL.md), lire le **numéro de version actuelle** — clé `VERSION` du montage `env_variables/data/<service>` — **en lecture seule à ce stade**. La valeur n'est jamais affichée, loggée ni transmise : seul l'écart « version actuelle → version visée » est consigné (sans divulguer d'autres clés). Aucune écriture n'a lieu en Idéation.

### Step 3 — Analyser les impacts de la montée de version (page Release GitHub)

Analyser la **page Release GitHub** de la version visée (lien fourni dans l'intention) pour vérifier les **impacts** : **breaking changes**, migrations de configuration requises, et **stabilité de la version** (écarter les versions RC / beta / non stables — recommander la dernière version **stable** si la version visée ne l'est pas).

**Variables d'environnement — toujours relevées comme breaking change.** Toute **modification, ajout ou suppression** d'une **variable d'environnement** entre la version actuelle et la version visée (renommage, nouvelle variable obligatoire, variable retirée ou dépréciée, changement de valeur par défaut ou de format attendu) **doit être relevée** comme un breaking change, car elle impacte la configuration du service dans Vault / le fichier Terraform. Chaque variable concernée est listée avec l'action à mener (ajouter / mettre à jour / retirer la clé).

### Step 4 — Verdict et blocage

Produire l'artefact `analyse_impact_version` consignant : type de service, écart de version,
breaking changes détectés, enjeux de configuration, recommandation.

- **Enjeu détecté** (breaking change, version non stable, migration de configuration) → passer l'issue en **`blocked`**, poster l'analyse et la recommandation, et **ne pas** engager la suite sans arbitrage humain explicite tracé.
- **Impact sécurité détecté** (CVE, auth, exposition, secrets) → **report de priorité** : la demande relève de `security-patch` ; le signaler et re-router (plancher renforcé, sensors sécurité bloquants).
- **Analyse OK** (aucun breaking change, aucun enjeu de configuration) → le parcours peut se poursuivre vers la Validation, où le gate léger unique autorisera écriture Vault + Kestra.

## Format de compte-rendu (obligatoire, concis)

Le compte-rendu posté sur l'issue est **minimal et déterministe** — pas de narration de phases, pas de log d'étapes, pas de reproduction des notes de version. **Exactement** ce gabarit, et rien de plus :

```markdown
## Stack

- Service : <service>
- **Version cible** : <version visée> (actuelle : <version actuelle lue depuis Vault, clé `VERSION`>)
- **Scope** : service-version-update (mise à jour service existant)
- **Type** : <Docker Swarm | Proxmox> (déterminé en Initialisation par `stack-detection`)

## Breaking Change : ✅ **AUCUN breaking change détecté**
```

Règles de remplissage :

- **Type** — toujours `Docker Swarm` **ou** `Proxmox`, jamais « à déterminer » : il a été tranché en
  Initialisation par `stack-detection` (localisation du fichier Terraform) et est **réutilisé** ici.
- **Version actuelle** — toujours la valeur réelle lue dans Vault (Step 2) ; jamais « à
  déterminer ».
- **Breaking Change** — si **aucun** : conserver la ligne `✅ **AUCUN breaking change détecté**` telle quelle. Si **au moins un** : remplacer par une ligne d'en-tête puis **une liste à puces**,  chaque puce = un breaking change **et l'action à mener**. **Toute modification, ajout ou suppression de variable d'environnement** entre la version actuelle et la version visée **compte comme un breaking change** et figure dans la liste (une puce par variable, avec l'action : ajouter / mettre à jour / retirer la clé) :

  ```markdown
  ## Breaking Change : ⚠️ **Breaking changes détectés**

  - <breaking change 1> → action : <action à mener>
  - Variable d'environnement `<NOM_VARIABLE>` <ajoutée | modifiée | supprimée> → action : <ajouter / mettre à jour / retirer la clé dans Vault et le Terraform>
  ```

Aucun autre bloc n'est ajouté au compte-rendu (pas de « Phase 0 / Phase 1 », pas de tableau d'informations manquantes, pas de liste de prochaines étapes) : le type est acquis en Initialisation
(`stack-detection`), la version actuelle est lue au Step 2, et le reste du parcours est porté par le gate léger de Validation.

## Sensors

Outputs: analyse d'impact de version consignée sur l'issue. Aucun gate humain à ce stage (analyse) ;
un enjeu détecté (breaking change, version non stable, migration de configuration) **bloque** l'issue (`blocked`) jusqu'à arbitrage humain. Le halt-and-ask sur stack introuvable est porté en
amont par [`../initialisation/stack-detection.md`](../initialisation/stack-detection.md), pas ici. Le seul gate du parcours est le gate léger unique porté par [`../validation/version-update-application.md`](../validation/version-update-application.md).
Imports: none.
Upstream targets: `intention_capturee` (service + version visée), `type_service_detecte` (type Docker Swarm / Proxmox déterminé en Initialisation par `stack-detection`).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles (motifs de breaking change par service, signatures de versions non stables, sources de release fiables) tracés sur l'issue, remontés au gate léger de Validation — jamais écrits dans le run courant.
