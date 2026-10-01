---
name: presentation-targeting
description: "Repère, dans les documents d'architecture du projet (DAS découpée en fichiers Markdown, décisions, modèles, vues), où se trouve l'information à récolter pour une présentation client, en s'appuyant sur le front-matter des gabarits d'architecture et la structure des documents — sans lecture exhaustive. Utiliser en amont de la génération pour cibler les chapitres et charger uniquement les sections utiles (réduction des coûts)."
---

Skill de **ciblage de l'information** pour préparer une présentation client à moindre coût. Objectif : savoir **où** se trouve l'information à récolter, analyser et présenter, **sans tout lire**. Les sources ciblées sont les **documents d'architecture du projet**. Complète `client-presentation-generation` (qui structure et produit).

## Sources : les documents d'architecture du projet

Le ciblage porte **exclusivement** sur les livrables d'architecture validés du projet, organisés selon `project-defaults` :

- `documentation/` — la **Documentation d'Architecture de Solution (DAS)**, découpée en fichiers fixes `001` et `01`–`15` (gabarits `architecture-solution-gabarits`), plus les **sous-répertoires d'architecture détaillée** : `architecture-logicielle/`, `architecture-donnee/`, `architecture-infra/`, `architecture-securite/` (et d'autres sous-répertoires par domaine/système le cas échéant).
- `decisions/` — les ADR (décisions structurantes).
- `models/` et `views/` — modèles et vues de diagrammes.

Ne jamais réinventer le contenu : partir de ces documents validés.

> **Présentations techniques** : l'information détaillée se trouve **souvent dans les sous-répertoires de `documentation/`** (ex. `documentation/architecture-securite/` pour le détail sécurité, `architecture-logicielle/` pour le logiciel, `architecture-infra/` pour l'infrastructure). La DAS racine (`01`–`15`) donne la synthèse ; **descendre dans le sous-répertoire de domaine** pour le détail. Cibler d'abord la synthèse, puis le détail.

## Principe

Charger d'abord les **métadonnées légères** (front-matter des gabarits, table des matières, titres de sections) plutôt que le contenu complet. N'ouvrir en entier que les sections réellement nécessaires aux chapitres retenus. Ce ciblage réduit le volume lu et le coût de production.

Le ciblage s'appuie idéalement sur un **front-matter présent dans les gabarits d'architecture** (champs de type `theme`, `types_presentation`, `domaine`, `sujets`, `sensibilite`). Le champ **`sujets` reflète les titres de niveau 2 (`##`) et 3 (`###`)** du document et est **maintenu à jour quand ces titres changent** : il donne le sommaire ciblable des sections/sous-sections, ce qui permet de mapper un chapitre de présentation directement vers la ou les sections concernées. Cette adaptation des gabarits `architecture-solution-gabarits` fait l'objet d'une **issue dédiée** (voir backlog). Tant qu'elle n'est pas livrée, se rabattre sur les **titres de sections et la table de correspondance ci-dessous** pour localiser l'information.

## Étape 1 — Établir la cible

À partir de la fiche de périmètre (type de présentation, sujets, chapitres retenus), lister les **thèmes à couvrir** et, pour chacun, les **informations attendues** (ex. Entreprise/Affaires → besoins d'affaires, registres BAE, risques, CAPEX/OPEX, juridiction).

Pour chaque thème, noter aussi la **question** qu'il pose (structure, étapes, ordre temporel, flux de données, états) : elle prépare le **choix de la recette Archify** (parmi les 12, donc du type parmi les 5) fait à la génération (`client-presentation-generation` → `references/archify-diagram-types.md`). Le ciblage ne produit pas le diagramme ; il **transmet l'intention de diagramme** (recette pressentie) dans la carte de ciblage.

Le ciblage peut être **granulaire** : sélectionner **un ou plusieurs éléments spécifiques** à l'intérieur d'un thème plutôt que le thème entier — par exemple **un ou plusieurs besoins d'affaires précis** (par identifiant `BES-001`, `UC-001`… ou par section H2/H3 du `03-besoins_affaires_exigences.md`). La carte de ciblage retient alors les seules sections correspondantes.

## Étape 2 — Repérer les sources par front-matter

- Lire le **front-matter** de chaque fichier de la DAS (`documentation/001`, `01`–`15`) : champs `theme`, `types_presentation`, `domaine`, `sujets`, `sensibilite`, sans charger le corps.
- Filtrer les documents dont `types_presentation` contient le type visé et dont `theme` / `sujets` recoupent les chapitres retenus. Le champ **`sujets` (titres H2/H3)** sert d'ancrage au niveau section/sous-section, pour cibler directement le passage utile.
- Compléter avec les ADR (`decisions/`) pertinents et les diagrammes (`models/`, `views/`).
- Construire une **carte de ciblage** thème → document(s) → section(s), en ne retenant que les sources pertinentes.

### Correspondance de référence thème → fichier DAS

| Thème de présentation | Fichier(s) DAS candidat(s) |
| --- | --- |
| Contexte / vision / périmètre | `01-introduction.md` |
| Objectifs / piliers Well-Architected | `02-objectifs.md` |
| Besoins d'affaires / BAE / cas d'usage | `03-besoins_affaires_exigences.md` |
| Risques | `04-risques.md` |
| CAPEX / OPEX / planification / coûts | `05-planification.md` |
| Vue d'ensemble de la solution / diagrammes | `06-architecture-solutions.md` |
| Choix des solutions | `07-choix-des-solutions.md` |
| Juridiction / conformités / contraintes | `08-contraintes.md` |
| Déploiement / DevSecOps | `09-deploiement.md` |
| Cycle de vie & taxonomie des données / gouvernance données | `10-cycle_vie_donnees.md` |
| Normes de sécurité / STRIDE / gouvernance sécurité | `11-securite.md` |
| Volumétrie | `12-volumetries.md` |
| Plan de qualité | `13-plan-qualite.md` |
| Prévention / résilience / reprise | `14-preventions-et-resilience.md` |
| Concepts transverses (IA, observabilité, etc.) | `15-concepts-transverses.md` |
| Détail technique — logiciel | `documentation/architecture-logicielle/` |
| Détail technique — données | `documentation/architecture-donnee/` |
| Détail technique — infrastructure | `documentation/architecture-infra/` |
| Détail technique — sécurité | `documentation/architecture-securite/` |

> Cette table est un **point de départ** ; le front-matter réel du projet fait foi. Pour une **présentation technique**, descendre dans les **sous-répertoires de `documentation/`** (`architecture-logicielle/`, `architecture-donnee/`, `architecture-infra/`, `architecture-securite/`, etc.) : la DAS racine donne la synthèse, le sous-répertoire donne le détail. Suivre le front-matter de ces documents détaillés lorsqu'il est présent.

## Étape 3 — Charger uniquement l'utile

Pour chaque entrée de la carte de ciblage, ouvrir **seulement** les sections nécessaires. Éviter la lecture exhaustive. Noter les manques (thème sans source) pour arbitrage humain.

## Étape 4 — Restituer la carte de ciblage

Fournir au processus de génération (`client-presentation-generation`) une carte claire, incluant l'**intention de diagramme** (recette Archify pressentie d'après la question du thème ; choix définitif fait à la génération) :

```
Thème                     | Source (document)                     | Section / ancrage        | Recette pressentie (→ type)
------------------------- | ------------------------------------- | ------------------------ | ------------------------------
Vue d'ensemble solution   | documentation/06-architecture-solu... | ## Architecture          | <recette d'après la référence>
Besoins d'affaires        | documentation/03-besoins_affaires...  | ## Besoins d'affaires    | —
Dépendances initiatives   | documentation/05-planification.md     | ## Dépendances           | <recette d'après la référence>
Cycle de vie des données  | documentation/10-cycle_vie_donnees.md | ## Cycle de vie          | <recette d'après la référence>
...                       | ...                                   | ...                      | ...
```

- La colonne **Recette pressentie** est **indicative** et n'est **pas définie ici** : la renseigner en appliquant la question du thème à la **table de correspondance de [`references/archify-diagram-types.md`](../client-presentation-generation/references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique)** (source unique) ; `—` si le thème n'appelle pas de diagramme. Le **choix définitif** (recette → type + composition + trace) est arrêté à la génération selon le public. Ne pas recopier la correspondance ici.

- Marquer les thèmes **sans source identifiée** comme écart à arbitrer (ne rien inventer).
- Ne pas modifier les livrables source ; ce ciblage est en lecture seule.

## Règles

- **Lecture seule** : ne jamais modifier les documents d'architecture source.
- **Fidélité** : ne présenter que ce qui existe dans les livrables validés ; signaler les manques plutôt que de combler.
- **Coût maîtrisé** : privilégier front-matter et titres ; ne charger le contenu complet qu'à la demande et pour les seuls chapitres retenus.
- **Confidentialité** : ne pas extraire de secret ni de donnée interne non destinée au client ; tenir compte du champ `sensibilite` du front-matter.
