---
name: service-version-update
depth: standard
verification: standard
keywords: [nouvelle version, mise à jour version, montée de version, bump, bump de version, release, nouvelle release, update version, version update, upgrade, mise à niveau, nouvelle version disponible, passage en version]
description: "Mise à jour d'un service existant sur une nouvelle version disponible (stack Docker Swarm ou service Proxmox) — analyse d'impact de version, écriture VERSION dans Vault, déploiement Kestra sous gate léger unique"
---

# Scope `service-version-update`

Mise à jour d'un **service existant** (stack Docker Swarm ou service Proxmox) vers une **nouvelle
version disponible** — montée de version d'image, bump déclenché par une release amont. Le point
d'entrée et le standard d'analyse d'impact de ce parcours sont tracés en
[`decisions/0044`](../../decisions/0044-parcours-service-version-update-gate-leger-unique-ecriture-vault-version.md).

C'est une **spécialisation ciblée** de `stack-update` : là où `stack-update` couvre toute
modification structurante d'une stack existante, `service-version-update` couvre le cas précis
« un service tourne déjà, une nouvelle version est sortie, on veut y passer ». Il porte un parcours
en **trois temps** :

1. **Analyse d'impact de version** — type de service (Docker Swarm vs Proxmox), lecture de la
   version actuelle dans Vault (clé `VERSION` ou `VERSION_<NOM_DU_SERVICE>`, lecture seule), analyse de la page Release GitHub,
   détection des breaking changes et des enjeux de configuration. Un enjeu détecté (breaking
   change, version non stable, migration de configuration) **bloque** le parcours : l'issue passe
   `blocked`, aucune suite n'est engagée sans arbitrage humain.
2. **Écriture de la version dans Vault** — mise à jour de la/des seule(s) clé(s) de version (`VERSION` ou `VERSION_<NOM_DU_SERVICE>`) du montage
   `env_variables/data/<service>` via la skill `homelab-vault-access` (exception d'écriture
   étroite, voir ci-dessous).
3. **Déploiement Kestra** — lancement du flux `configure_service` à partir du fichier Terraform du
   service (`terraform/swarm/<service>` pour Docker Swarm, `terraform/services/<service>` pour
   Proxmox).

```mermaid
flowchart TD
    IA[version-impact-analysis - IDEATION] -->|enjeu : breaking change / version non stable / migration| BL[Issue blocked - arbitrage humain]
    IA -->|impact securite| SP[Report de priorite - scope security-patch]
    IA -->|analyse OK| VA[version-update-application - VALIDATION]
    VA -->|gate leger unique - une seule acceptation| GATE{Humain accepte ?}
    GATE -->|non| NO[Aucune ecriture - aucun deploiement]
    GATE -->|oui| VW[Ecriture Vault VERSION - env_variables/data/service]
    VW --> KD[kestra-deployment - configure_service sur Terraform existant]
    KD --> DONE[Service deploye en nouvelle version]
```

## Convention des clés de version dans Vault

- **Stack à un seul service, ou services partageant la même version** : clé unique `VERSION`
  (`${VERSION:-<défaut>}` dans le compose).
- **Stack docker compose à plusieurs services avec des versions distinctes** : **une clé
  `VERSION_<NOM_DU_SERVICE>` par service** (nom en majuscules, ex. `VERSION_PROMETHEUS`,
  `VERSION_ALERTMANAGER`), référencée dans le compose par `${VERSION_<NOM_DU_SERVICE>:-<défaut>}`.
  Ce sont ces clés qui sont lues (Idéation) et écrites (Validation). Les anciens noms
  spécifiques (`DOCKER_<X>_IMAGE`…) ne sont plus utilisés.
- Si certains services d'une stack partagent la même version, ils partagent `VERSION` ; seuls les
  services à version distincte reçoivent une clé `VERSION_<NOM_DU_SERVICE>`.
- Une mise à jour ne cible que la/les clé(s) du ou des services concernés ; les autres clés de
  version sont préservées.

## Gate humain léger unique

Après une analyse d'impact **OK** (aucun breaking change, aucun enjeu de configuration), un **seul**
point de validation **léger** gouverne les temps 2 et 3. Sur acceptation, l'écriture Vault de
`VERSION` **et** le déploiement Kestra sont **tous deux autorisés en une seule étape** — pas
d'aller-retour, pas de double validation. Ce gate `light` est porté par le stage
[`version-update-application`](../common/stages/validation/version-update-application.md) ; il reste
**non supprimable** (aucune action à impact n'est autonome — invariant du conductor).

## Exception d'écriture Vault étroite

La skill `homelab-vault-access` reste en **lecture seule** pour tous les autres parcours. Ce scope
est le **seul** cas d'écriture autorisé, et uniquement pour écrire les clés de version (`VERSION` / `VERSION_<NOM_DU_SERVICE>`) du montage
`env_variables/data/<service>`. **Jamais** un secret du montage `services/`, jamais une autre clé qu'une clé de version.
L'écriture suit un pattern read-modify-write qui préserve toutes les autres clés ; la valeur
n'est **jamais** affichée, loggée ni transmise ; l'écriture est tracée sur l'issue (nom de clé
`VERSION` + statut seulement). Détail : `homelab-vault-access`.

## Report de priorité — `security-patch` l'emporte

Si la montée de version a un **impact sécurité** (correctif de CVE, durcissement, changement
d'authentification / d'exposition / de secrets), `security-patch` **l'emporte** sur ce scope dans
l'ordre de désambiguïsation : le plancher `comprehensive` / `renforcé` et les sensors sécurité
bloquants s'appliquent alors. `service-version-update` ne vaut que pour une montée de version
**sans** enjeu sécurité propre.

Axes par défaut : Depth `standard`, vérification `standard` (analyse d'impact de version,
cohérence du déploiement). Overridable à la hausse à la confirmation de scope — jamais abaissable
sans trace.

Appartenance : voir la matrice scope × phase de
[`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md) et le champ `scopes:`
des fiches de stage ([`../common/stages/`](../common/stages/)).
