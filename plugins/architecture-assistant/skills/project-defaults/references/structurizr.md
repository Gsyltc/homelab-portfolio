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

## Services cloud Azure : tag dédié + style thématisé (convention obligatoire)

> **Source unique de vérité** de la convention de représentation des services **Microsoft Azure** dans le modèle C4. L'**Architecte Azure** (skill [`azure-solution-architect`](../../azure-solution-architect/SKILL.md)) s'y réfère ; aucune autre fiche ne la duplique.

Dès qu'un **service Azure** apparaît dans le modèle C4 (élément `softwareSystem`, `container` ou `component`, **ainsi que les éléments de déploiement `deploymentNode` et `infrastructureNode`** représentant un service ou une ressource Azure — p. ex. Azure DevOps, API Management, App Service, Azure Functions, Cosmos DB, région/zone Azure, VNet, App Service Plan…), il porte **un tag dédié** et un **style thématisé** correspondant, afin d'afficher l'**icône officielle du service** et les couleurs Azure.

### Règle

1. **Taguer l'élément** avec un tag dédié au service, en **PascalCase sans espaces**, préfixé `Azure` lorsque le nom du service ne l'inclut pas déjà. Exemple : le service **« Azure DevOps »** → tag **`AzureDevOps`**.

   ```dsl
   # dans models/ (le modèle reste la source de vérité)
   azureDevOps = softwareSystem "Azure DevOps" "CI/CD et gestion de code" "AzureDevOps"
   ```

   Le **dernier argument** de la déclaration (`"AzureDevOps"`) est le **tag** porté par l'élément. Pour plusieurs tags, les séparer par une virgule (`"Azure,AzureDevOps"`).

   La règle vaut **identiquement pour les éléments de déploiement** `deploymentNode` et `infrastructureNode` (utilisés dans les vues de déploiement, `0004-deploiement.dsl`) : le **dernier argument** porte le tag du service / de la ressource Azure.

   ```dsl
   # dans le bloc de déploiement du modèle
   deploymentEnvironment "Production" {
       deploymentNode "Microsoft Azure" "" "Azure" "Azure" {
           deploymentNode "East US" "Région Azure" "Azure Region" "AzureRegion" {
               infrastructureNode "App Service Plan" "Plan d'hébergement" "Azure" "AzureAppServicePlan"
               deploymentNode "App Service" "Hébergement de l'app" "Azure App Service" "AzureAppService" {
                   containerInstance webApp
               }
           }
       }
   }
   ```

   Sur `deploymentNode` / `infrastructureNode`, le tag est l'**argument suivant la `technology`** (4ᵉ position : `nom`, `description`, `technology`, `tags`). Comme pour les autres éléments, plusieurs tags se séparent par une virgule.

2. **Garantir le style dans `theme/0001-project-styles.dsl`** : pour **chaque** tag de service Azure présent dans le modèle, il **doit** exister un bloc `element <Tag> { … }` dans `theme/0001-project-styles.dsl`. S'il manque, **l'ajouter** (ne jamais laisser un service Azure sans son style). Le style pointe vers l'**icône officielle du thème Azure de Structurizr** et applique les couleurs Azure :

   ```dsl
   element AzureDevOps {
       icon https://static.structurizr.com/themes/microsoft-azure-2024.07.15/azure-devops.png
       stroke #509aeb
       color #509aeb
   }
   ```

   Un bloc `element <Tag>` **s'applique à tout élément portant ce tag**, y compris un `deploymentNode` ou un `infrastructureNode` : un seul style par tag de service, qu'il soit utilisé dans une vue C4 logique ou dans une vue de déploiement. Exemple pour une ressource d'infrastructure Azure :

   ```dsl
   element AzureAppService {
       icon https://static.structurizr.com/themes/microsoft-azure-2024.07.15/app-services.png
       stroke #509aeb
       color #509aeb
   }
   ```

3. **Icônes = thème officiel Structurizr** : utiliser le thème Azure officiel **`microsoft-azure-2024.07.15`** (version publiée la plus récente — voir <https://github.com/structurizr/themes>). Base d'URL des icônes :

   ```
   https://static.structurizr.com/themes/microsoft-azure-2024.07.15/<service>.png
   ```

   Le `<service>` est le nom de fichier d'icône du thème (kebab-case), p. ex. `azure-devops.png`, `api-management-services.png`, `app-services.png`, `azure-cosmos-db.png`. Vérifier le nom exact dans le thème officiel ; **ne pas inventer** une URL d'icône. Couleurs Azure par défaut : `stroke` / `color` **`#509aeb`** (bleu Azure), ajustables au besoin par service.

### Portée et garde-fou

- Un **tag par service** distinct : deux services Azure différents ne partagent pas un même tag.
- **Zéro service Azure sans style** : avant de livrer/valider les diagrammes, s'assurer que chaque tag de service Azure du modèle a son `element <Tag>` dans `theme/0001-project-styles.dsl` (vérification incluse dans la validation DSL ci-dessous). Cela couvre **tous** les types d'éléments : `softwareSystem` / `container` / `component` **et** `deploymentNode` / `infrastructureNode`.
- Le `theme/0001-project-styles.dsl` reste la **source de style du projet** ; les tags vivent sur le **modèle** (`models/`, source de vérité), jamais recopiés dans une vue.


## Validation (obligatoire avant écriture finale)

Valider la syntaxe et la résolution des `!include` **avant** de livrer :

```sh
structurizr.sh validate -workspace workspace.dsl
```

> **Contrôle complémentaire (services Azure)** : vérifier que **chaque tag de service Azure** porté par un élément du modèle — `softwareSystem` / `container` / `component` **et** `deploymentNode` / `infrastructureNode` — possède bien son bloc `element <Tag> { … }` dans `theme/0001-project-styles.dsl` (voir « Services cloud Azure : tag dédié + style thématisé » ci-dessus). Un service Azure tagué sans style associé est un **écart** à corriger avant livraison.

## Export / visualisation

```sh
# Export des vues (exemples)
structurizr.sh export -workspace workspace.dsl -format mermaid         -output <dossier-export>
structurizr.sh export -workspace workspace.dsl -format plantuml/c4plantuml -output <dossier-export>
```

Alternativement, ouvrir `workspace.dsl` dans **Structurizr Lite** (Docker) pour une visualisation interactive.

## Traçabilité

À chaque ajout/retrait d'une vue, mettre à jour `views/README.md` (table des fichiers + table des vues avec la clé `embed:`) et l'index des diagrammes du `001` de la DAS (règle d'or 6 de `architecture-solution-gabarits`).
