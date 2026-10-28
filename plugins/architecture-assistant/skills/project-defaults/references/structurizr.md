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
    ├── <logo>.png            # Logo par défaut du projet (branding)
    ├── 0000-default-styles.dsl
    ├── 0001-project-styles.dsl
    └── 0002-external-tools.dsl   # kroki.url, plantuml.url, formats
```

## Règles

- **Modèle = source de vérité** : acteurs, systèmes, conteneurs, composants et liens vivent sous `models/`. Toute évolution d'une vue passe par `views/000X-*.dsl` ; on ne duplique jamais le modèle dans une vue.
- **Un seul `workspace.dsl` parent** : il porte les blocs `model {}` et `views {}` et **inclut** (`!include`) les fichiers de `models/`, `views/` et `theme/`. Les diagrammes C4 d'un projet vivent dans ce workspace unique (règle d'or 9 de `architecture-solution-gabarits` + convention `models/` de `project-defaults`).
- **Hiérarchie C4** : Contexte → Conteneurs → Composants → Code. Un fichier de vue par niveau (`0001`–`0004`) — voir [`kroki-diagrammes.md`](kroki-diagrammes.md) pour la numérotation et le regroupement par famille.
- **Thème** : réutiliser le thème du projet (`theme/0000-default-styles.dsl`, `theme/0001-project-styles.dsl`) ; ne pas réinventer un style quand le thème existe. Le câblage des moteurs de rendu externes (kroki, plantuml) est centralisé dans `theme/0002-external-tools.dsl`.
- **Logo par défaut du projet** : le fichier **PNG présent dans le répertoire `theme/`** est le **logo par défaut à utiliser pour le projet** (branding du workspace Structurizr / en-tête des vues). Le référencer depuis le thème (p. ex. propriété `structurizr.logo` du workspace / `theme/0001-project-styles.dsl`) plutôt que d'en introduire un autre. Ce logo projet est **distinct** des logos **par composant** (section « Style des composants » ci-dessous), qui proviennent du dépôt `dashboard-icons`.

## Syntaxe DSL : extension du modèle

- Utiliser `!element` et `!relationship` pour **étendre** un modèle. **Ne pas utiliser `!extend`.**
- `!element <identifiant> { ... }` permet d'**ajouter des enfants** (composants) à un conteneur ou système défini ailleurs.

## Règles de modélisation et de libellés (vues C4)

- **Toute modification du modèle est horodatée en commentaire DSL** : à chaque évolution du modèle (`models/`, `workspace.dsl`), ajouter un commentaire `// <AAAA-MM-JJ> — <description courte de la modification>` au plus près de l'élément/flux touché. Prose **limitée au maximum** (une ligne). Ce commentaire n'apparaît jamais dans un libellé rendu.

  ```dsl
  // 2026-10-28 — Ajout du conteneur de cache Redis devant l'API
  cache = container "Cache" "Cache applicatif" "Redis"
  ```

- **Descriptions d'éléments et de liens ≤ 30 caractères** dans les libellés rendus.
- **Aucun code, référence ou numéro dans les libellés rendus** : ni `INV-`, `CT-`, `CTR-SEC-`, `PINV-`, `RAT-`, `PLG-`, `IMP-`, `R-SEC-`, ni `ADR`, ni `DEC`, ni `§`. Uniquement l'**intention métier/technique**. La **traçabilité reste hors des libellés rendus** (commentaires DSL `// …`, DAS ou ADR).
- **Un seul lien par sens entre deux mêmes éléments** (vues statiques conteneur/composant) : consolider les interactions multiples d'un même sens en un libellé synthétique. **Exception** : une vue **dynamique** (séquence) peut répéter le même couple en étapes numérotées.
- **Tag `modified`** lorsqu'un élément ou un flux est **modifié** par une spécification/décision proposée.
- **Tag `deleted`** lorsqu'un élément ou un flux est **supprimé** par une spécification/décision proposée.
- **Tag `new`** pour les éléments/flux **nouveaux** (ou modifiés selon le contexte). Les styles `new`/`modified`/`deleted` sont définis dans `theme/0000-default-styles.dsl` — ne pas les redéfinir.

## Vues

- **Vue dynamique au périmètre « software system »** : pas de composants (uniquement des conteneurs). Pour représenter des composants → vue composant ou vue dynamique à **périmètre conteneur**.
- Vue conteneur de surface + vues composant par conteneur porteur.
- Titres et descriptions de vue **sans référence** (mêmes interdits que les libellés ci-dessus).

## Style des composants : tag dédié + logo thématisé (convention obligatoire)

> **Source unique de vérité** de la convention de représentation **visuelle** des composants (technologies, services, outils) dans le modèle C4. Elle s'applique à **tout type de composant** — pas seulement Azure. Les fiches spécifiques (p. ex. [`azure-solution-architect`](../../azure-solution-architect/SKILL.md)) s'y réfèrent ; aucune ne la duplique.

Dès qu'un **composant identifiable** (technologie, service, outil) apparaît dans le modèle C4 — élément `softwareSystem`, `container`, `component`, **ainsi que les éléments de déploiement `deploymentNode` et `infrastructureNode`** — on cherche à lui associer **un tag dédié** et un **style thématisé** affichant son **logo officiel**.

### Règle

1. **Taguer l'élément** avec un tag dédié, en **PascalCase sans espaces** (p. ex. `PostgreSQL`, `Redis`, `AzureDevOps`, `Nginx`). Le **dernier argument** de la déclaration porte le(s) tag(s) ; plusieurs tags se séparent par une virgule.

   ```dsl
   # dans models/ (le modèle reste la source de vérité)
   db     = container "Base de données" "Stockage relationnel" "PostgreSQL"
   cache  = container "Cache" "Cache applicatif" "Redis"
   devops = softwareSystem "Azure DevOps" "CI/CD et gestion de code" "AzureDevOps"
   ```

   La règle vaut **identiquement pour les éléments de déploiement** `deploymentNode` / `infrastructureNode` (vues de déploiement, `0004-deploiement.dsl`) : le tag est l'**argument suivant la `technology`** (4ᵉ position : `nom`, `description`, `technology`, `tags`).

   ```dsl
   deploymentEnvironment "Production" {
       deploymentNode "App Service" "Hébergement de l'app" "Azure App Service" "AzureAppService" {
           containerInstance webApp
       }
   }
   ```

2. **Trouver le logo sur le dépôt `dashboard-icons`** (homarr-labs). Base d'URL des logos PNG (kebab-case) :

   ```
   https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/<nom>.png
   ```

   Le `<nom>` est le nom d'icône en kebab-case, p. ex. `postgresql.png`, `redis.png`, `nginx.png`, `grafana.png`, `docker.png`, `azure-devops.png`. **Trouver le bon logo** (vérifier que l'URL répond `200`, ne jamais inventer un nom).

   **Règle de repli (obligatoire)** : **si le logo n'existe pas** sur ce dépôt (URL en `404`), alors **ni thème ni tag** pour cet élément — on le laisse au style par défaut, sans tag de style dédié. Ne jamais fabriquer une URL ni rattacher un logo approximatif.

3. **Garantir le style dans `theme/0001-project-styles.dsl`** : pour **chaque** tag de composant présent dans le modèle **et dont le logo a été trouvé**, il **doit** exister un bloc `element <Tag> { … }` pointant vers le logo. S'il manque, **l'ajouter**.

   ```dsl
   element PostgreSQL {
       icon https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/postgresql.png
   }
   element Redis {
       icon https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/redis.png
   }
   element AzureDevOps {
       icon https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/azure-devops.png
       stroke #509aeb
       color #509aeb
   }
   ```

   Un bloc `element <Tag>` **s'applique à tout élément portant ce tag**, y compris un `deploymentNode` / `infrastructureNode` : un seul style par tag. Des couleurs (`stroke` / `color`) peuvent être ajoutées par famille technologique (p. ex. bleu Azure `#509aeb`).

### Portée et garde-fou

- Un **tag par composant** distinct : deux composants différents ne partagent pas un même tag.
- **Zéro composant tagué sans style** : avant de livrer/valider, s'assurer que chaque tag de composant du modèle (dont le logo existe) a son `element <Tag>` dans `theme/0001-project-styles.dsl`. Cela couvre **tous** les types d'éléments : `softwareSystem` / `container` / `component` **et** `deploymentNode` / `infrastructureNode`.
- **Logo introuvable → aucun tag de style ni thème** : c'est la règle de repli, pas un écart.
- Le `theme/0001-project-styles.dsl` reste la **source de style du projet** ; les tags vivent sur le **modèle** (`models/`, source de vérité), jamais recopiés dans une vue.

## Validation (obligatoire avant écriture finale)

Valider la syntaxe et la résolution des `!include` **avant** de livrer. La **validation par défaut se fait avec l'image Docker** (toujours le tag `latest`) :

```sh
# Validation par défaut — image Docker `latest`
docker run --rm -v "$(pwd)":/usr/local/structurizr structurizr/cli:latest validate -w workspace.dsl
```

Le volume monté est le **répertoire de travail du projet** (racine contenant `workspace.dsl`).

Variante uniquement si une CLI locale est déjà installée et compatible :

```sh
# Variante CLI locale (si disponible)
structurizr.sh validate -workspace workspace.dsl
```

Boucle : **`validate`** puis **`export json`** avant commit.

> **Contrôle complémentaire (style des composants)** : vérifier que **chaque tag de composant** porté par un élément du modèle — `softwareSystem` / `container` / `component` **et** `deploymentNode` / `infrastructureNode` — dont le logo existe, possède bien son bloc `element <Tag> { … }` dans `theme/0001-project-styles.dsl`. Un composant tagué sans style associé est un **écart** à corriger ; un composant **sans logo trouvé** reste **légitimement sans tag ni style**.

### Contrôles post-export

À exécuter sur l'export (JSON/texte) avant commit :

1. **Aucune référence dans les libellés rendus** — interdits dans noms, descriptions, titres, libellés de relations, titres/descriptions de vues :

   ```bash
   grep -nE "(INV-[0-9]|CT-[0-9]|CTR-SEC-|PINV-|RAT-|PLG-|IMP-|R-SEC-|§[0-9]|ADR|DEC)" <export>
   ```

   Si trouvé → déplacer la référence vers un commentaire DSL (`// …`), la DAS ou un ADR.

2. **Un seul lien par sens (vues statiques)** : extraire les paires `(source -> cible)` des relations des vues statiques, trier, vérifier que `uniq -d` est vide. **Exception** : les vues dynamiques peuvent répéter le même couple en étapes numérotées.

## Export / visualisation

```sh
# Export des vues (exemples)
structurizr.sh export -workspace workspace.dsl -format mermaid         -output <dossier-export>
structurizr.sh export -workspace workspace.dsl -format plantuml/c4plantuml -output <dossier-export>
```

Alternativement, ouvrir `workspace.dsl` dans **Structurizr Lite** (Docker) pour une visualisation interactive.

## Exemple minimal (`workspace.dsl` + modèle)

```dsl
workspace {

    model {
        !include theme/properties.dsl

        user = person "Utilisateur" "Utilisateur du système"

        !include models/system.dsl
    }

    views {
        !include views/system-context.dsl
        !include views/system-container.dsl
        !include views/system-components.dsl

        styles {
            !include theme/0000-default-styles.dsl
            !include theme/0001-project-styles.dsl
            !include theme/0002-external-tools.dsl
        }
    }

}
```

```dsl
# models/system.dsl
system = softwareSystem "Système Exemple" "Description courte (<= 30)" {
    api = container "API" "Service API (<= 30)" {
        controller = component "Contrôleur" "Point d'entrée (<= 30)"
        service = component "Service métier" "Logique métier (<= 30)"
    }
    db = container "Base de données" "Stockage (<= 30)"
}

# Relation consolidée (un seul lien par sens)
user -> system "Utilise"
system.api.controller -> system.api.service "Orchestre"
system.api.service -> system.db "Lit et écrit" "new"

# Extension via !element (ajout de composant dans conteneur défini ailleurs)
# !element system.api {
#     validator = component "Validateur" "Validation (<= 30)" "new"
# }
# !relationship system.api.controller -> system.api.validator "Valide"
```

## Traçabilité

À chaque ajout/retrait d'une vue, mettre à jour `views/README.md` (table des fichiers + table des vues avec la clé `embed:`) et l'index des diagrammes du `001` de la DAS (règle d'or 6 de `architecture-solution-gabarits`).
