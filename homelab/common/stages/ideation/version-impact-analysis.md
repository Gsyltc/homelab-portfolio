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
consumes: [{artifact: intention_capturee, required: true}]
requires_stage: [intent-capture]
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

### Step 1 — Identifier le type de service

Déterminer le type du service visé : **stack Docker Swarm** (fichier Terraform sous
`terraform/swarm/<service>`) ou **service Proxmox** (fichier Terraform sous
`terraform/services/<service>`). Le service **existe déjà** : aucun arbitrage Swarm / Proxmox
n'est rejoué.

### Step 2 — Lire la version actuelle dans Vault (lecture seule)

Via la skill [`homelab-vault-access`](../../../../plugins/homelab-assistant/skills/homelab-vault-access/SKILL.md),
lire la clé `VERSION` du montage `env_variables/data/<service>` — **en lecture seule à ce stade**.
La valeur n'est jamais affichée, loggée ni transmise : seul l'écart « version actuelle → version
visée » est consigné (sans divulguer d'autres clés). Aucune écriture n'a lieu en Idéation.

### Step 3 — Analyser la page Release GitHub

Analyser la **page Release GitHub** de la version visée (lien fourni dans l'intention) : notes de
version, **breaking changes**, migrations de configuration requises, et **stabilité de la version**
(écarter les versions RC / beta / non stables — recommander la dernière version **stable** si la
version visée ne l'est pas).

### Step 4 — Verdict et blocage

Produire l'artefact `analyse_impact_version` consignant : type de service, écart de version,
breaking changes détectés, enjeux de configuration, recommandation.

- **Enjeu détecté** (breaking change, version non stable, migration de configuration) → passer
  l'issue en **`blocked`**, poster l'analyse et la recommandation, et **ne pas** engager la suite
  sans arbitrage humain explicite tracé.
- **Impact sécurité détecté** (CVE, auth, exposition, secrets) → **report de priorité** : la
  demande relève de `security-patch` ; le signaler et re-router (plancher renforcé, sensors
  sécurité bloquants).
- **Analyse OK** (aucun breaking change, aucun enjeu de configuration) → le parcours peut se
  poursuivre vers la Validation, où le gate léger unique autorisera écriture Vault + Kestra.

## Sensors

Outputs: analyse d'impact de version consignée sur l'issue. Aucun gate humain à ce stage (analyse) ;
un enjeu détecté **bloque** l'issue (`blocked`) jusqu'à arbitrage humain. Le seul gate du parcours
est le gate léger unique porté par [`../validation/version-update-application.md`](../validation/version-update-application.md).
Imports: none.
Upstream targets: `intention_capturee` (intention : service + version visée).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : candidats-règles
(motifs de breaking change par service, signatures de versions non stables, sources de release
fiables) tracés sur l'issue, remontés au gate léger de Validation — jamais écrits dans le run courant.
