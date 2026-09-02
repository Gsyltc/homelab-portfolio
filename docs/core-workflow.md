# core-workflow.md — document déplacé (stub de redirection)

> **Ce document n'est plus la source du workflow d'architecture.** Depuis le Stage 7 (ALI-192), le workflow est **structuré** en un triptyque **conductor / stages / protocols** dont la **source unique** est [`core/common/`](../core/common/conductor.md).
>
> Ce fichier est conservé comme **stub de redirection** pour ne casser aucune référence existante (compatibilité ascendante, tracée par une décision structurante dédiée). Il ne contient plus le contenu normatif : toute lecture doit se faire sur les fichiers canoniques ci-dessous.

## Nouvelle source unique

- **Point d'entrée** : [`core/common/conductor.md`](../core/common/conductor.md) — instructions du coordinateur (gouvernance A2A, boucle Keep/Modify/Redo aux gates, chargement du contexte, activation conditionnelle d'une méthodologie, invariants, points de synchronisation A2A).
- **Fiches de stage** : [`core/common/stages/<phase>/<stage>.md`](../core/common/stages/) — une fiche par étape des 5 phases, avec front-matter.
- **Protocoles transverses** : [`core/common/protocols/`](../core/common/protocols/).

## Table de correspondance (ancien contenu → nouvel emplacement)

| Section historique de `core-workflow.md` | Nouvel emplacement canonique |
| --- | --- |
| Priorité du workflow, rôle du coordinateur, principe « le workflow s'adapte au travail » | [`core/common/conductor.md`](../core/common/conductor.md) |
| Vue d'ensemble des 5 phases + tableau de correspondance (alias) | [`core/common/conductor.md`](../core/common/conductor.md) (§ « Les 5 phases et leurs stages ») |
| Détail de chaque phase / étape (Initialization → Operation) | [`core/common/stages/`](../core/common/stages/) (une fiche par stage) |
| Scopes, axes Depth / vérification, auto-détection, matrice stage × scope | [`core/common/protocols/scopes-and-axes.md`](../core/common/protocols/scopes-and-axes.md) (décision structurante dédiée) |
| Règles & boucle d'apprentissage (SEC-1..5) | [`core/common/protocols/governance-security.md`](../core/common/protocols/governance-security.md) + [`core/rules/`](../core/rules/README.md) (décision structurante dédiée) |
| Verification gates & Sensors (SG-1..6, caractère advisory) | [`core/common/protocols/governance-security.md`](../core/common/protocols/governance-security.md) + [`core/sensors/`](../core/sensors/README.md) (décision structurante dédiée) |
| Modèle de collaboration A2A (acteurs, règle de mention) | [`core/common/protocols/governance-security.md`](../core/common/protocols/governance-security.md) |
| Contrôle sécurité systématique, protocole de revue | [`core/common/protocols/reviewer.md`](../core/common/protocols/reviewer.md) |
| Schéma / contrat d'une étape, cycle d'exécution générique | [`core/common/protocols/stage-definition.md`](../core/common/protocols/stage-definition.md) · [`core/common/protocols/stage-protocol.md`](../core/common/protocols/stage-protocol.md) |
| Mode d'autonomie en Construction, walking skeleton | [`core/common/stages/construction/walking-skeleton.md`](../core/common/stages/construction/walking-skeleton.md) · [`core/common/stages/construction/detailed-deliverables.md`](../core/common/stages/construction/detailed-deliverables.md) (décision structurante dédiée) |
| Langue / format, piste d'audit sur l'issue, garde-fous | [`core/common/conductor.md`](../core/common/conductor.md) + [`core/common/protocols/governance-security.md`](../core/common/protocols/governance-security.md) |

## Note sur les références historiques

Les décisions structurantes antérieures mentionnent `docs/core-workflow.md` dans leur **prose historique** : ces références restent **valides et intactes** (ce sont des enregistrements immuables). Ce stub garantit que leurs liens continuent de résoudre. La décision de migration vers le triptyque est elle-même tracée par une décision structurante dédiée.
