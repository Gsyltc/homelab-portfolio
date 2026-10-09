# Diagrammes = vues `image` Structurizr rendues par kroki (convention obligatoire)

> Fichier de référence de la skill `project-defaults`, **chargé uniquement au besoin** —
> lorsqu'il faut produire, intégrer ou réviser un diagramme dans la documentation
> d'architecture (DAS) d'un projet. La section `views/` du `SKILL.md` renvoie ici.

Tout diagramme **hors C4 natif** (PlantUML, Mermaid, BPMN, etc.) est intégré à la DAS **exclusivement** comme une **vue `image` Structurizr rendue par kroki**, jamais comme un SVG inclus directement.

## Règles

- **Règle d'intégration** : une vue `image * "<clé>" { kroki <renderer> <chemin-source> … }` est déclarée dans un fichier `views/000X-*.dsl`, puis référencée dans la DAS via `![…](embed:<clé>)`. **Proscrit** : inclure le SVG directement (`![](….svg)`).
- **La source est la vérité** : la vue `image` pointe vers le fichier source du diagramme (`.puml` / `.mmd` / `.bpmn`), généralement sous `documentation/ressources/<type>/`. Le diagramme est **généré en code** (règle d'or 9 de `architecture-solution-gabarits`) ; on ne versionne pas un rendu figé comme source d'intégration.
- **Câblage kroki** : les URL des moteurs de rendu sont déclarées **une seule fois** dans `theme/0002-external-tools.dsl` (bloc `properties` : `kroki.url`, `kroki.format`, `plantuml.url`, `plantuml.format`) et héritées par les vues ; ne pas coder d'URL en dur dans les vues.

## Renderer kroki par type de source

| Source   | Extension | Directive DSL             |
| -------- | --------- | ------------------------- |
| PlantUML | `.puml`   | `kroki plantuml <chemin>` |
| Mermaid  | `.mmd`    | `kroki mermaid <chemin>`  |
| BPMN 2.0 | `.bpmn`   | `kroki bpmn <chemin>`     |

(autres renderers kroki possibles selon le besoin ; même patron `kroki <renderer> <chemin>`.)

## Regroupement par famille et numérotation fixe

Les diagrammes d'une **même famille** sont **regroupés dans un seul fichier de vue** (une vue `image` par diagramme, portée `*` pour les vues autonomes non rattachées à un élément du modèle C4). Numérotation des fichiers `views/000X-*.dsl` :

- **Diagrammes C4**, groupés **par niveau**, un fichier par niveau : Contexte (`0001-contexte.dsl`), Conteneur (`0002-containers.dsl`), Composants (`0003-components.dsl`), Déploiement (`0004-deploiement.dsl`).
- **Affaires / Processus** → **`0005`** : un fichier unique (ex. `views/0005-processus-affaires.dsl`, portant PROC-001…PROC-00N).
- **Planification** (Gantt, timeline, feuille de route, WBS, PERT, etc.) → **`0006`** : un fichier unique regroupant **toutes** les vues de planification.
- **Autres diagrammes** → **numérotation à suivre** (`0007`, `0008`, … dans l'ordre d'ajout), un fichier par famille.

## Validation DSL obligatoire avant écriture finale

Valider la syntaxe (résolution des `!include`) **avant** de committer / livrer :

```sh
structurizr.sh validate -workspace workspace.dsl
```

## Traçabilité

À chaque ajout/retrait d'une vue, mettre à jour **`views/README.md`** (table des fichiers + table des vues avec la clé `embed:`) et l'**index des diagrammes du `001`** de la DAS (règle d'or 6 de `architecture-solution-gabarits`).

## Patrons de référence

- Vues C4 par niveau (`0001`–`0004`) ; **Affaires / Processus** → `0005` (`kroki bpmn`) ; **Planification** → `0006` (feuille de route, WBS, etc. ; `kroki plantuml`) ; autres familles à suivre (`0007`+).
- Pour un projet existant dont les vues ne suivent pas encore cette numérotation (p. ex. OAI-DLC), le réalignement — regrouper planification en `0006`, processus BPMN en `0005`, renuméroter les autres vues image et mettre à jour `views/README.md` + les `!include` de `workspace.dsl` — est à mener **comme travail de projet distinct**, pas par cette convention.

## Distinction avec `archify`

La skill `archify` produit des diagrammes HTML/SVG autoportants **pour les présentations client** (agent « Présentation client »). Elle ne remplace pas cette convention : l'**intégration des diagrammes dans la DAS** passe toujours par une vue `image` Structurizr + `embed:`.
