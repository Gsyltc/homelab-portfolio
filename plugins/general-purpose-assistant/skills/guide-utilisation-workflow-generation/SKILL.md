---
name: guide-utilisation-workflow-generation
description: "Mode opératoire pour produire et mettre à jour les guides d'utilisation des workflows (core, homelab, matching-cv-ao) au format PDF. Définit la trame éditoriale, les conventions des diagrammes d'interaction, la charte graphique (couleurs inspirées de Dalí), le pied de page, le gabarit HTML de construction et la commande de régénération (WeasyPrint). Utiliser à chaque création ou mise à jour d'un guide-utilisation-workflow-<workflow>.pdf."
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
5. **A2A** — comment les agents collaborent. Inclut **obligatoirement** une sous-section **5.1 — États & interactions** : un **diagramme de séquence** à couloirs d'acteurs (au minimum Humain, coordinateur, les acteurs qui *construisent* chacun dans leur couloir, l'acteur qui *vérifie* / QA, et l'acteur de *notification*) ; voir « Conventions des diagrammes d'interaction » plus bas.
6. **Utilisation avec Multica** — exécution autour de l'issue (mentions, piste d'audit, pièces jointes).
7. **Agnosticité & autres harnais** — forme déclarative portable ; couche d'adaptation par harnais (Multica, Claude, Codex, OpenCode, Hermes, Deepseek, Kiro).
8. **Annexe — les scopes en détail** — une **fiche par scope** du workflow (intention, mots-clés, axes Depth/Vérification par défaut, garde-fous propres) accompagnée d'un **diagramme d'état du flux spécifique au scope** mettant en avant les **interactions A2A et Humain** ; précédée d'un diagramme d'ensemble de l'ordre de priorité / désambiguïsation des scopes et d'une **légende commune** des diagrammes. Adapter la liste et le contenu des scopes au workflow visé (p. ex. les 7 scopes Homelab) à partir de `<workflow>/scopes/`.

Public visé : **non technique** (prospects, parties prenantes). Lecture simple, paragraphes définis, puces, tableaux, diagrammes.

## Conventions des diagrammes d'interaction (sections 5.1 & 8)

Ces conventions **font partie de la trame** et doivent être conservées à chaque régénération :

- **Code couleur des flèches** — **A2A** (agent → agent) en `--brand2` (vert-sarcelle) ; **Agent ↔ Humain** en `--accent` (ocre) ; **boucle de retour** (RENVOI / Modify-Redo / escalade) en terracotta `#b07a4f`, trait pointillé ; **gate / validation** = losange `--accent` (symbole ◆ dans les libellés courts).
- **Section 5.1 (diagramme d'ensemble)** — diagramme de séquence : lignes de vie verticales par acteur, **flèches strictement horizontales** reliant deux lignes de vie (jamais de flèche « dans le vide » ni oblique), gates en losanges, et une **colonne « état de l'issue »** à droite (p. ex. `todo → in_progress → in_review → done`, bascule `blocked`). Les acteurs qui construisent et l'acteur QA ont **chacun leur couloir distinct** ; l'étape de **notification** est explicite.
- **Section 8 (un diagramme par scope)** — un **diagramme d'état / flux** compact par fiche de scope, montrant le **chemin propre au scope** (délégations A2A, points de validation humaine, boucles de retour, court-circuits des branches autonomes, escalades). Mettre en avant **qui parle à qui** (A2A) et **où l'humain décide** (Agent ↔ Humain). Une **légende** commune précède les fiches.
- **Fidélité à la source** — comme tout le guide, ces diagrammes sont dérivés de la source du workflow (`conductor.md`, `stages/`, `protocols/`, `scopes/`, `agents/`, `sensors/`, `rules/`) ; ne rien inventer.

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
2. **Adapter le contenu** au workflow visé à partir de sa **source unique** `<workflow>/common/conductor.md`, ses fiches de stage `<workflow>/common/stages/` et ses protocoles `<workflow>/common/protocols/` (plus `scopes/`, `rules/`, `sensors/`, `agents/`). Ne rien inventer ; rester fidèle à la source. **Conserver les sections obligatoires de la trame**, dont la **sous-section 5.1 (États & interactions)** et l'**annexe « Les scopes en détail » (section 8)** avec **un diagramme d'état par scope** — en respectant les « Conventions des diagrammes d'interaction ».
3. **Ne référencer que le workflow visé** — aucune référence aux autres workflows (cloisonnement, `AGENTS.md`).
4. **Régénérer le PDF** avec WeasyPrint :
   ```sh
   weasyprint fichier-de-travail.html docs/guide-utilisation-workflow-<workflow>.pdf
   ```
5. **Vérifier le rendu** (nombre de pages, lisibilité, pas de débordement) avant livraison. **Contrôler spécifiquement** : le diagramme 5.1 (flèches horizontales alignées sur les lignes de vie, couloirs distincts, notification présente) et l'annexe (un diagramme de flux par scope, légende présente, code couleur A2A / Humain respecté).
6. **Ne conserver que le PDF** dans `docs/` ; le HTML de travail reste un élément de construction (non versionné dans `docs/`).

## Garde-fous

- Modifications dans le dépôt local sur une **branche git dédiée** à l'issue ; **aucun commit, PR ou push sans accord explicite de l'humain**.
- Aucun secret dans les livrables. Diagrammes générés en code (SVG) à syntaxe valide.
