# Catalogue Archify — 5 types (modes) et 12 recettes

Référence établie à partir du **guide Archify** ([guide.html](https://tt-a1i.github.io/archify/guide.html)) et de la **source canonique des recettes** (`archify/recipes/scenarios.mjs`, Archify v3.0.1). Elle fait la distinction entre deux niveaux :

- **5 types (modes) de diagramme** — les lentilles de rendu typées, portées par un schéma (`architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`).
- **12 recettes (recipes)** — des **points de départ ciblés** du guide Archify ; chaque recette répond à **une seule question technique** et s'appuie sur l'un des 5 types.

> Formulation d'Archify : « **12 real-world recipes / 5 typed diagram modes** ». La **recette est l'unité de sélection** (elle porte la question et le périmètre) ; le **type** est le mode de rendu sous-jacent. Choisir d'abord la recette d'après la question, le type en découle.

Ce catalogue dit **quoi choisir et pourquoi** ; la **production** (syntaxe, thèmes, export, validation) reste portée par la skill `archify`.

## Les 5 types (modes)

| Type (`type` Archify) | Idéal pour | À préciser dans la demande |
|---|---|---|
| **`architecture`** | Composants, services, stockage, frontières, infrastructure | Périmètre, composants clés, chemin principal |
| **`workflow`** | CI/CD, approbations, appels d'outils, runbooks | Participants, ordre, branches, exceptions |
| **`sequence`** | Appels d'API, repli de cache, authentification, traces async | Appelants, appelés, retours, chronologie |
| **`dataflow`** | Pipelines, lignage, PII, consommateurs | Sources, transformations, stockages, frontières |
| **`lifecycle`** | États, retries, attentes, états terminaux | États, événements, chemins de retry et d'annulation |

## Les 12 recettes (unité de sélection)

Chaque recette répond à **une** question. Rapprocher la question du **contexte du chapitre** et du **public cible**, puis retenir la recette ; son `type` est indiqué.

| # | Recette (`id`) | Type | Question à laquelle elle répond |
|---|---|---|---|
| 1 | **System overview** (`system-overview`) | `architecture` | Qu'est-ce qui existe, qui en est propriétaire, et comment est-ce connecté ? |
| 2 | **Deployment ownership** (`deployment-ownership`) | `architecture` | Où s'exécute chaque charge de travail, et qu'est-ce qui franchit une frontière ? |
| 3 | **Agent tool-call loop** (`agent-tool-call`) | `workflow` | Comment un agent planifie, obtient l'autorisation, agit, récupère et rend compte ? |
| 4 | **Delivery workflow** (`delivery-workflow`) | `workflow` | Comment un changement passe-t-il sûrement du commit à la production ? |
| 5 | **Incident runbook** (`incident-runbook`) | `workflow` | Comment les intervenants détectent, trient, atténuent, vérifient et escaladent ? |
| 6 | **API request chain** (`api-request`) | `sequence` | Qui appelle qui, dans quel ordre, et que retourne-t-on ? |
| 7 | **Async roundtrip** (`async-roundtrip`) | `sequence` | Que se passe-t-il après le retour de la requête initiale ? |
| 8 | **Data lineage** (`data-lineage`) | `dataflow` | D'où viennent les données, comment changent-elles, qui les consomme ? |
| 9 | **Event-stream topology** (`event-stream`) | `dataflow` | Quels événements passent par quels topics, processeurs, groupes et chemins d'échec ? |
| 10 | **Object lifecycle** (`object-lifecycle`) | `lifecycle` | Quels états existent, quels événements font transiter, et comment cela se termine ? |
| 11 | **Deployment lifecycle** (`deployment-lifecycle`) | `lifecycle` | Dans quel état est une release, et que peut-il se passer ensuite ? |
| 12 | **Layout repair** (`layout-repair`) | `architecture` | Pourquoi un diagramme existant déborde/chevauche, et que corriger d'abord ? |

> Répartition par type : `architecture` (3 : #1, #2, #12) · `workflow` (3 : #3, #4, #5) · `sequence` (2 : #6, #7) · `dataflow` (2 : #8, #9) · `lifecycle` (2 : #10, #11).
> La recette **Layout repair** (#12) sert à **réparer** un diagramme existant, pas à en créer un nouveau sujet : l'utiliser en maintenance d'un livrable antérieur.

## Correspondance public/thème → recette (source unique)

Cette table est la **source unique** de la correspondance **type de présentation / thème → recette(s) Archify**. La skill `client-presentation-generation`, ses gabarits et `presentation-targeting` **s'y réfèrent sans la recopier**.

| Type de présentation (public) | Contexte / message typique | Recette(s) recommandée(s) → type | Composition | Trace `+trace` |
|---|---|---|---|---|
| **Executive** (direction) | Vue d'ensemble de la solution, bénéfices, jalons macro | **System overview** (→`architecture`) ; **Delivery workflow** pour les jalons (→`workflow`) | `classic` | Non (synthèse) |
| **Entreprise / Affaires** (TOGAF) | Alignement des couches, ownership, dépendances, plan de transition | **System overview** / **Deployment ownership** (→`architecture`) ; **Delivery workflow** (→`workflow`) ; **Deployment lifecycle** pour les états de transition (→`lifecycle`) | `blueprint` (ownership) sinon `classic` | Optionnelle : `+trace` si ownership/évidence à montrer |
| **Technique / Fonctionnelle** (équipes techniques) | Composants & intégrations, séquences d'appel, flux de données, cycles de vie, procédés | voir la table par chapitre technique ci-dessous | `signal-flow` (flux) ou `blueprint` (topologie) | Selon besoin technique |
| **Sécurité / Conformité** (RSSI, conformité, risque) | Zones de confiance, franchissements de frontières, gouvernance, preuve/audit | **Deployment ownership** (→`architecture`) ; **Data lineage** (isolation PII, →`dataflow`) ; **Incident runbook** (→`workflow`) | `blueprint` (frontières) | **Oui** recommandé (`+trace` : évidence d'audit) — sans détail exploitable |

### Détail par chapitre — présentation Technique / Fonctionnelle

| Chapitre | Question | Recette → type | Composition |
|---|---|---|---|
| Logiciel — composants/intégrations | « De quoi est composé le système ? » | **System overview** → `architecture` | `blueprint` |
| Logiciel — séquences d'appel | « Qui échange quoi et dans quel ordre ? » | **API request chain** / **Async roundtrip** → `sequence` | `signal-flow` |
| Data — flux/gouvernance | « Comment circulent les données ? » | **Data lineage** / **Event-stream topology** → `dataflow` | `signal-flow` |
| Infrastructure — topologie | « Où vivent les composants ? » | **Deployment ownership** → `architecture` | `blueprint` |
| Sécurité (détail) — zones de confiance | « Où sont les frontières / franchissements ? » | **Deployment ownership** (`+trace` possible) → `architecture` | `blueprint` |
| IA / procédés | « Par quelles étapes passe le procédé ? » | **Agent tool-call loop** → `workflow` | `signal-flow` |
| Cycle de vie d'un objet/état | « Par quels états passe l'objet ? » | **Object lifecycle** → `lifecycle` | `classic` |

> Ces tables sont un **point de départ** ; le **message réel** du chapitre prime. En cas d'hésitation entre deux recettes : `node bin/archify.mjs guide "<situation>" --json`.

## Compositions (styles de rendu) et trace

La composition adapte la **lisibilité** au public ; elle n'ajoute pas d'information.

| Composition / option | Effet | Quand la préférer |
|---|---|---|
| **`classic`** | Rendu épuré, lecture directe | Public de décision ou vue de synthèse (executive, affaires) |
| **`signal-flow`** | Met en évidence les flux/signaux | Vues techniques orientées flux/échanges (dataflow, sequence, workflow technique) |
| **`blueprint`** | Rendu « plan », propriété et frontières visibles | Vues d'architecture/déploiement avec ownership et zones |
| **`+trace`** | Ajoute une piste de preuve/évidence (audit, checks) | Quand il faut **démontrer la preuve** (sécurité/conformité, ownership de déploiement) |

## Règles d'usage

1. **Partir de la question** du chapitre → retenir **une recette** (unité de sélection) ; le `type` en découle.
2. **Rapprocher du public** pour fixer la composition (`classic` décision · `signal-flow`/`blueprint` technique) et l'activation de `+trace`.
3. **Une recette par diagramme** ; produire plusieurs diagrammes si plusieurs questions.
4. **`Layout repair`** = maintenance d'un diagramme existant, pas un nouveau sujet.
5. **Fidélité à la source** : le diagramme illustre un livrable d'architecture validé (repéré via `presentation-targeting`) ; ne rien inventer.
6. En cas de doute entre deux recettes, demander à la CLI Archify : `node bin/archify.mjs guide "<situation>" --json`.
