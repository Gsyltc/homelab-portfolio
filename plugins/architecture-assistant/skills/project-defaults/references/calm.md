# CALM — Common Architecture Language Model (fichier de référence)

> Fichier de référence de la skill `project-defaults`, **chargé uniquement au besoin** —
> lorsqu'un projet modélise son architecture en **CALM** (architecture-as-code). Pour
> l'intégration des diagrammes dans la DAS, voir [`kroki-diagrammes.md`](kroki-diagrammes.md) ;
> pour le modèle de solution C4, voir [`structurizr.md`](structurizr.md).

**CALM** (Common Architecture Language Model) est une spécification open source **FINOS**, portée par la communauté **Architecture as Code (AasC)**. Format **JSON déclaratif, lisible par la machine et par l'humain**, versionné, pour décrire des architectures logicielles — pensé notamment pour les environnements régulés (services financiers). Il aligne l'**intention de conception** avec ce qui est réellement construit (validation de conformité).

## Quand l'utiliser (et quand ne pas l'utiliser)

- **Utiliser** : architecture **as-code** versionnée et validable, contrôles/conformité attachés au modèle (environnements régulés), patrons réutilisables pré-approuvés, génération de documentation et de diagrammes à partir d'un modèle unique.
- **Ne pas utiliser à la place de C4** pour la vue solution détaillée si le projet est déjà sur Structurizr : CALM est un choix de modélisation à part entière ; demander le format souhaité avant de générer (règle d'or `architecture-solution-gabarits` / `project-defaults`).

## Concepts de base (schéma CALM)

Le schéma est un **JSON Schema modulaire, extensible et versionné** :

| Concept         | Rôle                                                                 |
| --------------- | -------------------------------------------------------------------- |
| **Nodes**       | Composants architecturaux distincts (types intégrés ou personnalisés) |
| **Relationships** | Connexions / interactions / dépendances entre nœuds                |
| **Interfaces**  | Points d'interaction exposés par un nœud                             |
| **Controls**    | Contrôles de domaine (sécurité, conformité) attachés à l'architecture |
| **Flows**       | Processus métier tracés à travers les relations                      |
| **Metadata / Decorators** | Métadonnées (déploiement, sécurité, métier)                |
| **Patterns**    | Structures réutilisables pré-approuvées                              |
| **Standards**   | Extensions d'organisation ajoutant des propriétés aux composants CALM |

Un modèle minimal porte `unique-id`, `name`, `description`, `nodes: []`, `relationships: []`.

## Outillage (toolchain AasC)

- **CLI CALM** : validation d'un modèle contre le méta-schéma et génération (docs/diagrammes) — p. ex. `calm validate …`, `calm generate …` (résoudre les sous-commandes exactes via `calm --help`).
- **CALM Hub** (`hub.calm.finos.org`), **CalmStudio** (éditeur visuel → JSON CALM validé), extension **VS Code**.
- Source officielle : `github.com/finos/architecture-as-code` ; documentation `calm.finos.org`.

## Validation (obligatoire avant écriture finale)

Comme pour tout diagramme généré en code (règle d'or 9), **valider le modèle** avant de livrer : exécuter la validation CALM (CLI) et corriger les erreurs/avertissements signalés avant intégration.

## Intégration à la DAS

- Un diagramme généré depuis un modèle CALM est intégré à la DAS selon la convention standard : si le rendu passe par un moteur supporté par kroki, utiliser une **vue `image` Structurizr** + `![…](embed:<clé>)` (voir [`kroki-diagrammes.md`](kroki-diagrammes.md)) ; jamais de SVG inclus directement.
- Modèle source (`.json` CALM) versionné sous `models/` ; traçabilité `views/README.md` + index `001` ; numérotation famille « autres » (`0007`+) sauf famille déjà fixée.

## Rappel de cloisonnement

CALM est un format de **modélisation d'architecture (as-code)** ; il ne remplace pas Archify (restitution de présentation) et coexiste avec C4/Structurizr et ArchiMate selon le format retenu pour le projet.
