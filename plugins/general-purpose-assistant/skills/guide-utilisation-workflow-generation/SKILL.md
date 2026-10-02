---
name: guide-utilisation-workflow-generation
description: "Mode opératoire pour produire et mettre à jour les guides d'utilisation des workflows (core, homelab, matching-cv-ao) au format PDF. Définit la trame éditoriale, la charte graphique (couleurs inspirées de Dalí), le pied de page, le gabarit HTML de construction et la commande de régénération (WeasyPrint). Utiliser à chaque création ou mise à jour d'un guide-utilisation-workflow-<workflow>.pdf."
---

# Génération des guides d'utilisation des workflows

Mode opératoire **unique** pour produire et **mettre à jour** les guides d'utilisation des workflows du dépôt. Garantit que chaque mise à jour suit **toujours le même mode opératoire** (même trame, même charte, même pied de page, même rendu).

## Livrable et emplacement

- **Format livré : PDF uniquement.** Le HTML est un **élément de construction**, pas un livrable : il n'est **pas conservé** dans `docs/`. Le gabarit de construction vit dans cette skill (`assets/gabarit-guide-workflow.html`).
- **Répertoire de stockage : `docs/`** (à la racine des guides existants).
- **Nommage du fichier : `guide-utilisation-workflow-<workflow>.pdf`** où `<workflow>` ∈ { `core`, `homelab`, `matching-cv-ao` }.

## Trame éditoriale (sections)

Reprendre cette trame pour chaque workflow (adapter le contenu, jamais la structure) :

1. **Contexte & objectifs** — ce qu'est le workflow, pourquoi, principe fondateur.
2. **Fonctionnement global** — les phases et l'exigence croissante de validation humaine.
3. **Les méthodes** — cycle d'une étape, boucle Keep / Modify / Redo, scopes & axes, mémoire de règles, garde-fous et contrôles automatiques.
4. **Agents & compétences** — rôles mobilisés et compétences partagées.
5. **A2A** — comment les agents collaborent.
6. **Utilisation avec Multica** — exécution autour de l'issue (mentions, piste d'audit, pièces jointes).
7. **Agnosticité & autres harnais** — forme déclarative portable ; couche d'adaptation par harnais (Multica, Claude, Codex, OpenCode, Hermes, Deepseek, Kiro).

Public visé : **non technique** (prospects, parties prenantes). Lecture simple, paragraphes définis, puces, tableaux, diagrammes.

## Charte graphique

Charte sobre inspirée des couleurs de *Réminiscence archéologique de l'Angélus de Millet* (Salvador Dalí). Couleurs **centralisées dans les variables CSS `:root`** du gabarit — réhabiller un guide = modifier ces variables, sans toucher au contenu :

| Variable | Rôle | Valeur |
| --- | --- | --- |
| `--brand` | Principal (titres, éléments forts) — vert-sarcelle crépusculaire | `#1f4a46` |
| `--brand2` | Secondaire — vert-sarcelle moyen | `#5c8475` |
| `--accent` | Accent — ocre / ambre (horizon doré) | `#cf8a3a` |
| `--ok` | État « Keep » — vert olive / cyprès | `#6a7636` |
| `--soft` / `--soft2` | Fonds — sable / crème | `#faf4e9` / `#f3e9d8` |
| `--ink` / `--muted` | Textes — brun chaud / taupe | `#2b2219` / `#7a6a56` |
| terracotta / sienne | Accent secondaire (ex. couches de mémoire) | `#b07a4f` |

- **Couverture** : ciel vert-sarcelle sombre fondant vers un horizon ocre bas (dégradé vertical), évoquant la plaine au crépuscule du tableau.
- **Pied de page** (toutes les pages de contenu, pas la couverture) : « **Auteur : Sylvain Goubaud · 2026** » à gauche, titre au centre, pagination à droite.
- **Diagrammes** : **SVG en ligne** dans le HTML (aucune dépendance externe, aucun réseau) ; les modifier directement dans le gabarit.

## Mode opératoire

1. **Copier le gabarit** `assets/gabarit-guide-workflow.html` vers un fichier de travail.
2. **Adapter le contenu** au workflow visé à partir de sa **source unique** `<workflow>/common/conductor.md`, ses fiches de stage `<workflow>/common/stages/` et ses protocoles `<workflow>/common/protocols/` (plus `scopes/`, `rules/`, `sensors/`, `agents/`). Ne rien inventer ; rester fidèle à la source.
3. **Ne référencer que le workflow visé** — aucune référence aux autres workflows (cloisonnement, `AGENTS.md`).
4. **Régénérer le PDF** avec WeasyPrint :
   ```sh
   weasyprint fichier-de-travail.html docs/guide-utilisation-workflow-<workflow>.pdf
   ```
5. **Vérifier le rendu** (nombre de pages, lisibilité, pas de débordement) avant livraison.
6. **Ne conserver que le PDF** dans `docs/` ; le HTML de travail reste un élément de construction (non versionné dans `docs/`).

## Garde-fous

- Modifications dans le dépôt local sur une **branche git dédiée** à l'issue ; **aucun commit, PR ou push sans accord explicite de l'humain**.
- Aucun secret dans les livrables. Diagrammes générés en code (SVG) à syntaxe valide.
