---
auteurs: Sylvain Goubaud
parties_prenantes: ""
accepte_par: Sylvain Goubaud
accepte_le: "2026-11-14"
supersedes: ""
superseded_by: ""
---

# Suppression du walking skeleton du workflow `homelab` et question du mode d'exécution posée au Cadrage

## Status

Accepted

## Date de création

2026-11-14

## Contexte

Le stage `autonomy-mode` (Production) exigeait qu'une « première tranche » du lot (walking skeleton : premier `.tfvars` ou squelette du compose) passe la QA, le contrôle qualité central et la validation granulaire avant toute autonomie. Les stages `terraform-configuration` et `docker-compose-creation` consommaient l'artefact `walking_skeleton_valide` : ils ne démarraient qu'après cette validation. Aucun stage ne produisait donc la tranche : la dépendance était circulaire.

Le lot d'une stack ne compte que deux livrables (`.tfvars` et compose). Chacun passe ensuite la QA systématique, le contrôle qualité central, la délégation sécurité et la validation humaine granulaire. Le walking skeleton refaisait ce cycle pour un seul fichier et ajoutait deux sollicitations de l'humain (validation de la tranche, puis question du mode).

## Décision

- Le walking skeleton est **supprimé** du workflow `homelab`.
- La question du **mode d'exécution** (gated par défaut, ou autonome jusqu'au prochain point de synchronisation) est posée dans le **message unique** de `required-parameters-collection` (Cadrage). Les options et la règle « pas de réponse ⇒ gated » restent définies dans `autonomy-mode` (source unique).
- `autonomy-mode` applique le mode choisi (artefact `mode_execution_applique`) et conserve le halt-and-ask systématique. Il n'a plus de gate humain ni de revue propre.
- `terraform-configuration` et `docker-compose-creation` consomment `mode_execution_applique` au lieu de `walking_skeleton_valide` et démarrent en parallèle.
- Le sensor `required-parameters` contrôle la présence de `mode_execution` (`gated` | `autonome`) dans `parametres.json`.

## Conséquences

### Positives

- **POS-001** : la dépendance circulaire disparaît ; la Production peut démarrer.
- **POS-002** : deux sollicitations de l'humain en moins sur le chemin nominal.
- **POS-003** : le parallèle Terraform / Docker est préservé.

### Négatives

- **NEG-001** : plus de validation intermédiaire sur une tranche avant la production complète. Mitigation : QA systématique, contrôle qualité central, délégation sécurité et validation humaine granulaire inchangés ; mode gated par défaut ; halt-and-ask inchangé.

## Alternatives étudiées

- **ALT-001** : conserver le walking skeleton en le faisant produire par `autonomy-mode` (le `.tfvars` seul d'abord, puis le compose). Rejetée : perte du parallèle Terraform / Docker et une sollicitation de plus, pour un contrôle déjà assuré en aval.

## Notes d'implémentation

- **IMP-001** : `homelab/common/stages/production/autonomy-mode.md` réécrit (mode + halt-and-ask) ; `terraform-configuration.md`, `docker-compose-creation.md`, `required-parameters-collection.md`, `conductor.md`, `protocols/stage-protocol.md` alignés.
- **IMP-002** : sensor `required-parameters` (manifeste, script, tests) : clé `mode_execution`.
- **IMP-003** : périmètre limité à `homelab`. Invariants de gouvernance (SG-1..6, SEC-1..5) inchangés.

## Références

- **REF-001** : [ADR-0051 - Sensors Homelab exécutables](0051-sensors-homelab-executables-python-et-hooks.md) — harnais du sensor `required-parameters`.
