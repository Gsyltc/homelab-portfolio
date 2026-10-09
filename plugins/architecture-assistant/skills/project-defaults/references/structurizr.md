# Structurizr — modèle C4 et vues de la DAS (fichier de référence)

> Fichier de référence de la skill `project-defaults`, **chargé uniquement au besoin** —
> lorsqu'on crée ou fait évoluer le modèle C4 et les vues d'un projet (répertoires
> `models/`, `views/`, `theme/` et le parent `workspace.dsl`). Pour l'**intégration**
> des diagrammes rendus par kroki dans la DAS, voir aussi
> [`kroki-diagrammes.md`](kroki-diagrammes.md).

Structurizr DSL est l'outil de référence du workflow `core` pour la modélisation d'architecture **en code**. Le **modèle reste la source de vérité** ; les vues n'en sont que des projections.

## Arborescence Structurizr d'un projet

```
<projet>/
├── workspace.dsl        # Parent : déclare model{} + views{}, inclut (!include) models/, views/, theme/
├── workspace.json       # Export Structurizr (généré ; ne pas éditer à la main)
├── models/              # Définitions du modèle (source de vérité)
│   ├── actors.dsl           # Personnes / rôles
│   ├── external_software.dsl# Systèmes externes
│   └── <systeme>/           # Conteneurs & composants par système
├── views/               # Vues (projections du modèle) — voir kroki-diagrammes.md pour la numérotation
└── theme/               # Styles & câblage outils
    ├── 0000-default-styles.dsl
    ├── 0001-project-styles.dsl
    └── 0002-external-tools.dsl   # kroki.url, plantuml.url, formats
```

## Règles

- **Modèle = source de vérité** : acteurs, systèmes, conteneurs, composants et liens vivent sous `models/`. Toute évolution d'une vue passe par `views/000X-*.dsl` ; on ne duplique jamais le modèle dans une vue.
- **Un seul `workspace.dsl` parent** : il porte les blocs `model {}` et `views {}` et **inclut** (`!include`) les fichiers de `models/`, `views/` et `theme/`. Les diagrammes C4 d'un projet vivent dans ce workspace unique (règle d'or 9 de `architecture-solution-gabarits` + convention `models/` de `project-defaults`).
- **Hiérarchie C4** : Contexte → Conteneurs → Composants → Code. Un fichier de vue par niveau (`0001`–`0004`) — voir [`kroki-diagrammes.md`](kroki-diagrammes.md) pour la numérotation et le regroupement par famille.
- **Thème** : réutiliser le thème du projet (`theme/0000-default-styles.dsl`, `theme/0001-project-styles.dsl`) ; ne pas réinventer un style quand le thème existe. Le câblage des moteurs de rendu externes (kroki, plantuml) est centralisé dans `theme/0002-external-tools.dsl`.

## Validation (obligatoire avant écriture finale)

Valider la syntaxe et la résolution des `!include` **avant** de livrer :

```sh
structurizr.sh validate -workspace workspace.dsl
```

## Export / visualisation

```sh
# Export des vues (exemples)
structurizr.sh export -workspace workspace.dsl -format mermaid         -output <dossier-export>
structurizr.sh export -workspace workspace.dsl -format plantuml/c4plantuml -output <dossier-export>
```

Alternativement, ouvrir `workspace.dsl` dans **Structurizr Lite** (Docker) pour une visualisation interactive.

## Traçabilité

À chaque ajout/retrait d'une vue, mettre à jour `views/README.md` (table des fichiers + table des vues avec la clé `embed:`) et l'index des diagrammes du `001` de la DAS (règle d'or 6 de `architecture-solution-gabarits`).
