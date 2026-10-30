---
slug: version-update-application
phase: validation
execution: CONDITIONAL
condition: "Scope service-version-update, analyse d'impact OK (aucun breaking change / aucun enjeu de configuration)"
lead_agent: Tech Lead Homelab
support_agents: [Spécialiste Déploiement Kestra]
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: light
produces: [version_ecrite_vault, depot_fichiers_confirme]
consumes: [{artifact: analyse_impact_version, required: true}]
requires_stage: [version-impact-analysis]
sensors: [vault-secret-exists]
scopes: [service-version-update]
inputs: "Analyse d'impact de version OK (service, version visée, type de service, fichier Terraform existant)"
outputs: "Clé VERSION écrite dans Vault (env_variables/data/<service>) + déploiement Kestra autorisé — sous une seule acceptation humaine (gate léger unique)"
---

# Application de la mise à jour de version (gate léger unique)

## Objectif

Après une analyse d'impact OK, obtenir **une seule** acceptation humaine légère qui autorise **à la
fois** l'écriture de la clé `VERSION` dans Vault **et** le déploiement Kestra du service — sans
aller-retour ni double validation.

## Steps

### Step 1 — Présenter l'analyse et demander le gate léger unique

Le Tech Lead présente à l'humain, de façon concise : le service visé, l'écart de version (version
actuelle → version visée, **sans** divulguer d'autres clés Vault), le résultat de l'analyse
d'impact (aucun breaking change, aucun enjeu de configuration) et les **deux actions** qu'une
acceptation autorise en une seule étape :

1. l'**écriture de la clé `VERSION`** du montage `env_variables/data/<service>` dans Vault ;
2. le **déploiement Kestra** (`configure_service`) à partir du fichier Terraform **existant** du
   service (`terraform/swarm/<service>` pour Docker Swarm, `terraform/services/<service>` pour
   Proxmox).

C'est un gate **léger** (`human_gate: light`) et **unique** : **une seule**
acceptation couvre les deux actions. Il reste **non supprimable** — aucune action à impact n'est
autonome (invariant du conductor). Rien n'est écrit ni déployé tant que l'humain n'a pas accepté.

### Step 2 — Sur acceptation : écriture Vault de `VERSION` (exception d'écriture étroite)

Sur « oui » explicite, écrire la **seule** clé `VERSION` du montage `env_variables/data/<service>`
via la skill [`homelab-vault-access`](../../../../plugins/homelab-assistant/skills/homelab-vault-access/SKILL.md),
en **read-modify-write** (les autres clés sont relues puis réécrites à l'identique — jamais
écrasées). Garde-fous **non débordables** :

- **jamais** un secret du montage `services/`, **jamais** une autre clé que `VERSION` ;
- la valeur n'est **jamais** affichée, loggée ni transmise ;
- l'écriture est **tracée sur l'issue** : nom de clé `VERSION` + statut (écrite / échec) **seulement** ;
- le token Vault est **révoqué** en fin d'opération.

C'est le **seul** cas d'écriture autorisé de la skill (voir son `SKILL.md` § écriture encadrée).

### Step 3 — Enchaîner le déploiement Kestra (même acceptation)

La **même** acceptation autorise le déploiement : poursuivre en
[`kestra-deployment.md`](kestra-deployment.md) (flux `configure_service` à partir du fichier
Terraform existant). Aucune **nouvelle** validation n'est demandée — le gate léger unique couvre les temps 2
et 3. L'artefact `depot_fichiers_confirme` produit ici matérialise l'autorisation attendue par
`kestra-deployment` (le parcours `service-version-update` ne dépose pas de nouveaux fichiers : il
réutilise le Terraform existant).

### Step 4 — Garde-fou absolu

Aucune écriture Vault ni aucun lancement de `configure_service` **sans** l'acceptation humaine légère unique.
Un refus (ou une demande d'ajustement) n'écrit rien et ne déploie rien ; l'issue reste en
`in_review` jusqu'à décision.

## Sensors

Outputs: `VERSION` écrite (statut consigné, valeur jamais révélée) + déploiement Kestra lancé —
sous la **seule** acceptation légère unique. Gate humain **léger unique** : c'est le point de
validation du parcours `service-version-update`.
Imports: `vault-secret-exists` (confirme l'existence du chemin `env_variables/data/<service>` avant
écriture — voir [`homelab/sensors/README.md`](../../../sensors/README.md)).
Upstream targets: `analyse_impact_version` (analyse d'impact OK).

## Learn

Boucle d'apprentissage maison (voir [`homelab/rules/`](../../../rules/README.md)) : ce stage **porte
le gate léger unique** — le Tech Lead y remonte les candidats-règles capturés depuis
`version-impact-analysis`, formulés en règles courtes ; persistance des apprentissages **confirmés**
dans `homelab/rules/` (jamais dans le run courant).
