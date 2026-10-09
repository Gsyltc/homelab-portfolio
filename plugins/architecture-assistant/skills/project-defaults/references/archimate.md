# ArchiMate — modélisation d'entreprise (fichier de référence)

> Fichier de référence de la skill `project-defaults`, **chargé uniquement au besoin** —
> lorsqu'un projet exige une modélisation **d'architecture d'entreprise** en ArchiMate.
> Pour l'intégration des diagrammes dans la DAS, voir
> [`kroki-diagrammes.md`](kroki-diagrammes.md) ; pour le modèle de solution C4, voir
> [`structurizr.md`](structurizr.md).

ArchiMate (standard **The Open Group**, aligné TOGAF) est un langage de modélisation d'**architecture d'entreprise**. Il complète C4/Structurizr (centré solution logicielle) quand il faut relier les couches **Métier → Application → Technologie** et exprimer motivation, stratégie et implémentation.

## Quand l'utiliser (et quand ne pas l'utiliser)

- **Utiliser** : architecture d'entreprise, alignement métier/SI, cartographie de capacités, vues de motivation (parties prenantes, objectifs, exigences), feuilles de route de transformation (couche Implémentation & Migration), livrables à forte orientation TOGAF.
- **Ne pas utiliser à la place de C4** : pour l'architecture **de solution logicielle** détaillée (conteneurs/composants), rester sur C4/Structurizr ([`structurizr.md`](structurizr.md)). ArchiMate et C4 sont complémentaires, pas interchangeables.

## Couches et éléments (rappel)

| Couche                     | Éléments typiques                                                   |
| -------------------------- | ------------------------------------------------------------------- |
| **Motivation**             | Partie prenante, Driver, Évaluation, Objectif, Exigence, Contrainte, Principe |
| **Stratégie**              | Ressource, Capacité, Flux de valeur, Course of action               |
| **Métier (Business)**      | Acteur, Rôle, Processus, Fonction, Service métier, Objet métier     |
| **Application**            | Composant applicatif, Fonction, Service applicatif, Objet de données |
| **Technologie**            | Nœud, Device, Logiciel système, Service technologique, Artefact     |
| **Implémentation & Migration** | Package de travail, Livrable, Jalon, Plateau                    |

Relations clés : composition, assignation, réalisation, service (serving), flux, déclenchement, accès.

## Production — diagrammes générés en code

Conformément à la règle d'or 9 de `architecture-solution-gabarits`, les diagrammes sont **générés en code**. Deux voies selon l'outillage disponible :

- **Archi (modèle `.archimate`)** : outil de référence open source (archimatetool.com). Le modèle est la source de vérité ; exporter les vues en image/SVG pour l'intégration.
- **PlantUML-Archimate** (`@startuml` + `!include <archimate/Archimate>`) : écriture en code, rendu via le renderer **PlantUML**. Dans ce cas, l'intégration à la DAS suit la convention standard : vue `image` Structurizr `kroki plantuml <source.puml>` + `![…](embed:<clé>)` (voir [`kroki-diagrammes.md`](kroki-diagrammes.md)).

## Intégration à la DAS

- Diagramme ArchiMate rendu en PlantUML → **vue `image` kroki** (`kroki plantuml`) + `embed:` ; jamais de SVG inclus directement.
- Regroupement/numérotation : famille « autres diagrammes » (`0007`+) sauf si la vue relève des familles déjà fixées — voir [`kroki-diagrammes.md`](kroki-diagrammes.md).
- Source `.puml` / `.archimate` sous `documentation/ressources/<type>/` ou `models/` selon la voie retenue ; traçabilité `views/README.md` + index `001`.

## Rappel de cloisonnement

ArchiMate sert la **vue d'entreprise / l'alignement TOGAF** ; il ne remplace ni C4/Structurizr (solution), ni Archify (restitution de présentation).
