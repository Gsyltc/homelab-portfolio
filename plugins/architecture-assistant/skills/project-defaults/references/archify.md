# Archify — diagrammes HTML/SVG pour présentations client (fichier de référence)

> Fichier de référence de la skill `project-defaults`, **chargé uniquement au besoin** —
> lorsqu'on produit des diagrammes **pour une présentation client** (agent
> « Camille - Présentation client »). À ne pas confondre avec l'intégration des
> diagrammes dans la DAS, qui passe par Structurizr + kroki
> ([`kroki-diagrammes.md`](kroki-diagrammes.md), [`structurizr.md`](structurizr.md)).

Archify (skill `archify`, source `github.com/tt-a1i/archify`, MIT) produit des diagrammes **HTML autoportants à SVG inline** : thèmes clair/sombre, animation de trace optionnelle, export PNG/JPEG/WebP/SVG/WebM. Entrée en langage naturel ou Mermaid (`flowchart`, `sequenceDiagram`, `stateDiagram`).

## Quand l'utiliser (et quand ne pas l'utiliser)

- **Utiliser** : visualiser une architecture, un workflow, une séquence d'appels, un flux de données / lignage, une machine à états — **pour la lecture humaine d'une présentation**. Aussi adapté aux sujets « du quotidien » (processus d'approbation, parcours, etc.).
- **Ne pas utiliser** : pour l'**intégration d'un diagramme dans la DAS** (→ Structurizr + kroki, vue `image` + `embed:`), ni pour des graphiques numériques / tableaux de bord.

## Les 5 types (Type router)

| Type           | Pour                                                            |
| -------------- | -------------------------------------------------------------- |
| `architecture` | Composants, services, frontières cloud/sécurité, infra         |
| `workflow`     | Processus, gates d'approbation, runbooks, CI/CD                |
| `sequence`     | Chaînes d'appels API, cycles de requête, échanges asynchrones  |
| `dataflow`     | Pipelines, ETL/ELT, lignage, gouvernance                       |
| `lifecycle`    | Transitions d'états/statuts, attentes, états terminaux         |

En cas d'ambiguïté : `node bin/archify.mjs guide "<scénario>" --json`.

## Flux d'auteur (fast path)

1. Choisir le type depuis la demande.
2. Lire le schéma et l'exemple du type (références internes de la skill `archify`) avant d'écrire ; IDs/wording/layout **neufs** (les exemples enseignent la forme, pas les faits).
3. Écrire le candidat complet (`candidate.json`), `meta.quality_profile = "showcase"` par défaut.
4. Finaliser en **une** commande (porte unique) :

   ```bash
   node bin/archify.mjs finalize <type> <candidate.json> <output.html> --quality showcase --json
   ```

   Un reçu « passing » prouve que les gates `validate`, `deliver`, `check` strict et `browser-check` sont passés. Un **exit non nul n'est jamais un succès** : lire le reçu, réparer la gate en échec, relancer.

Chaque nouvelle demande de diagramme a son propre dossier `.archify/<type>-<slug>-<YYYYMMDD-HHMMSS>/` (versions antérieures préservées).

## Garde d'authenticité (installation)

Lancer d'abord le `bin/archify.mjs` fourni par la skill. N'installer qu'en l'absence du CLI, **uniquement** depuis la source officielle `github.com/tt-a1i/archify` (`v3.0.1`). **Ne jamais** installer le paquet npm homonyme `archify@0.0.4` (risque de typosquatting).

## Sortie

Rendre le HTML validé (chemin), le type, le résumé de validation, le reçu d'artefact, l'état de preuve navigateur et l'état **réel** de la revue visuelle. Ne jamais revendiquer un succès pour une commande en échec ni une inspection visuelle non réalisée.

## Rappel de cloisonnement

Archify sert la **restitution** (présentations). La **documentation d'architecture** (DAS) reste produite via Structurizr + kroki ; un diagramme Archify ne remplace pas une vue `image` `embed:` dans la DAS.
