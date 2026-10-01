---
name: client-presentation-generation
description: "Gabarits de présentations client par type (Executive, Entreprise/Affaires TOGAF, Technique/Fonctionnelle, Sécurité/Conformité) et règles de mise en forme, à partir des documents d'architecture validés du projet. Les gabarits sont dans le répertoire gabarits/ (un fichier par type). Utiliser pour structurer et produire une présentation client (HTML dynamique avec diagrammes Archify, et/ou PowerPoint) lisible pour l'humain."
---

# Gabarits de présentations client

Skill **portant les gabarits** de présentations client et les règles de mise en forme. Les gabarits se trouvent dans le répertoire `gabarits/` de cette skill, **un fichier par type de présentation**. Ne jamais réinventer le contenu technique : partir des **documents d'architecture validés du projet** (repérés via `presentation-targeting`) et les mettre en forme pour le public visé.

**Priorité absolue : la facilité de lecture pour l'humain** (compréhension immédiate du contexte, des objectifs et du sujet).

> La séquence de travail, les gates (périmètre, validation humaine), le contrôle sécurité et l'archivage sont portés par le **workflow** (`core/common/conductor.md`, `stages/`, `protocols/`), pas par cette skill.

## Contenu des gabarits

| Fichier (dans `gabarits/`) | Type de présentation | Formats | Diagrammes |
|---|---|---|---|
| `executive.md` | Executive (direction) | HTML dynamique et/ou PowerPoint | Archify (dynamique) ; statiques admis en PPTX |
| `entreprise-affaires.md` | Entreprise / Affaires (respect TOGAF) | HTML dynamique et/ou PowerPoint | Archify (dynamique) ; statiques admis en PPTX |
| `technique-fonctionnelle.md` | Technique / Fonctionnelle | **HTML dynamique uniquement** | **Archify** (dynamique) |
| `securite-conformite.md` | Sécurité / Conformité | HTML dynamique et/ou PowerPoint | Archify (dynamique) ; statiques admis en PPTX |

Chaque gabarit décrit les **chapitres nécessaires** au type, les **sources d'architecture** à cibler (fichiers DAS), et le rappel du **patron narratif**. Le **choix de la recette/type Archify** par type de présentation et par chapitre est porté **uniquement** par la [table de correspondance de la référence](references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique) ; les gabarits y renvoient sans la recopier.

## Sélection du diagramme Archify (avant production)

Archify expose **5 types (modes)** de diagramme (`architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`) et, par-dessus, **12 recettes** (recipes) : chaque recette répond à **une seule question technique** et s'appuie sur l'un des 5 types. **La recette est l'unité de sélection.** **Avant de créer un diagramme**, déterminer la **recette** (donc le type) en fonction du **contexte de la présentation** et du **public cible**. Ne jamais produire un diagramme sans avoir arrêté ce choix. Catalogue des 5 types, des 12 recettes, des compositions et de la trace : [`references/archify-diagram-types.md`](references/archify-diagram-types.md).

### Procédure (contexte + public cible → recette → type)

1. **Déterminer le contexte** : quelle **question** pose le chapitre / la diapositive ? (ex. « qu'est-ce qui existe et qui est propriétaire », « comment un changement va du commit à la prod », « qui appelle qui et dans quel ordre », « d'où viennent les données », « par quels états passe l'objet »).
2. **Déterminer le public cible** : direction, parties prenantes affaires, équipes techniques/fonctionnelles, ou sécurité/conformité — fixe le **niveau de détail**, la **composition** et l'opportunité de la **trace**.
3. **Choisir la recette** dont la question correspond (table des 12 recettes de la référence) ; **une recette par diagramme**. Son **type** en découle automatiquement.
4. **Choisir la composition** selon le public : `classic` (décision/synthèse) · `signal-flow` (flux techniques) · `blueprint` (architecture/déploiement avec frontières et ownership).
5. **Décider de la trace `+trace`** : l'activer pour **démontrer une preuve/évidence** (conformité, ownership) ; l'omettre pour une vue de synthèse.
6. **Confirmer la fidélité** : le diagramme illustre un livrable validé repéré via `presentation-targeting` ; ne rien inventer. En cas d'hésitation entre deux recettes : `node bin/archify.mjs guide "<situation>" --json`.

> **Correspondance public/thème → recette : source unique.** La table qui associe chaque **type de présentation / thème** à sa ou ses **recette(s)** (et le détail par chapitre technique) est portée **uniquement** par [`references/archify-diagram-types.md` → Correspondance public/thème → recette](references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique). Ne pas la recopier ici ni dans les gabarits : s'y référer.

Pour le **rendu HTML dynamique**, un **fichier d'instructions** est fourni : **`instructions/presentation-html-dynamique.md`**. Il guide la production de bout en bout (le HTML est construit par l'agent, section par section — il n'y a pas de fichier HTML modèle à copier) :

| Fichier | Rôle |
|---|---|
| `instructions/presentation-html-dynamique.md` | Instructions complètes : créer les sections requises **selon le type** de présentation, créer les diagrammes du **type `archify` adapté** (Architecture, Workflow, Sequence, Data Flow, Lifecycle), **reproduire la charte** (tokens `theme/`, logo inliné), garantir des **diagrammes bien conçus** (règles de géométrie R1–R5, pas de chevauchement), **densité** de contenu, **largeur de prose ≥ 70 %**, autoportance, accessibilité, étiquetage fictif/réel ; avec snippets de référence (CSS, moteur de slides, moteur de diagramme) et le rationnel des règles (défauts à éviter). |

Ce fichier décrit **comment produire** le HTML ; les fichiers par type (ci-dessus) décrivent **quels chapitres** retenir. Issu d'un test de référence validé par l'humain.

## Quand utiliser

- Structurer et produire une présentation client d'un type donné à partir des documents d'architecture validés.
- Sélectionner le gabarit correspondant au type, ne conserver que les chapitres pertinents aux sujets demandés.

## Règles d'or

1. **Un gabarit par type** : sélectionner le fichier de `gabarits/` correspondant au type ; ne pas fusionner les types.
2. **Cibler avant de produire** : localiser l'information dans les documents d'architecture via `presentation-targeting` (front-matter) ; ne charger que les sections utiles.
3. **Fidélité à la source** : n'inventer ni chiffres, ni garanties, ni fonctionnalités absents des livrables validés ; en cas de doute, remonter au coordinateur.
4. **Lisibilité d'abord** : titres clairs, une idée par section/diapositive, visuels et tableaux, progression logique. Appliquer le patron `Contexte → Objectifs → Moyens → Méthodes → Résultats` quand adapté.
5. **Diagrammes Archify** : **avant production, déterminer la recette** (parmi les 12, donc le type parmi les 5) + composition + trace, selon le contexte et le public — voir [Sélection du diagramme Archify](#sélection-du-diagramme-archify-avant-production) et [`references/archify-diagram-types.md`](references/archify-diagram-types.md). Produits avec la skill `archify` (générés en code, syntaxe validée avant export) ; réutiliser ceux des livrables, produire une version simplifiée si nécessaire. En **HTML dynamique**, les diagrammes doivent être **animés ET interactifs** et respecter les **règles de géométrie R1–R5** (bord-à-bord, aucun passage sous un nœud, grille aérée, étiquette hors pointe, aucun recouvrement colinéaire) — cf. `instructions/presentation-html-dynamique.md`.
6. **Nomenclature client** (Technique/Fonctionnelle) : nommer chaque domaine selon la nomenclature du client.
7. **Charte graphique client** : appliquer couleurs, logo, typographie et gabarit fournis. **Thème des présentations** : le thème de référence (styles de rendu des diagrammes — couleurs, formes, typographie, icônes) est porté par le répertoire `theme/` du projet, dont le fichier **`theme/0000-default-styles.dsl`** fixe les styles par défaut (formes, couleurs d'éléments et de relations). Partir de ce thème ; ne pas réinventer un style ni approximer une charte (si elle n'est pas accessible, la demander). À défaut de charte client, utiliser ce thème par défaut validé.
8. **Format contraint par type** : respecter la colonne « Formats » du tableau (Technique/Fonctionnelle = HTML dynamique uniquement). Demander le format si plusieurs sont autorisés et non précisé.
9. **Confidentialité** : jamais de secret, d'identifiant ni de donnée interne non destinée au client ; tenir compte de la sensibilité des sources.
10. **Langue** : celle du destinataire (français par défaut).
11. **HTML dynamique — exigences validées** (cf. `instructions/presentation-html-dynamique.md`) : fichier **unique autoportant** (aucune dépendance externe : CSS/JS/logo/SVG inline, pas de CDN) ; **gabarit générique** — les **sections dépendent du type** de présentation (reprendre les chapitres du gabarit du type) et le slot `.diagram-embed` accepte **tout type de diagramme `archify`** (Architecture, Workflow, Sequence, Data Flow, Lifecycle) ; **menu latéral gauche hiérarchique** (thème + sous-chapitres) ; **densité** adaptée au type (~180–250 mots/slide en Executive) ; **largeur de prose dynamique ≥ 70 %** (aucun `max-width:…ch` sur la prose) ; `prefers-reduced-motion` respecté.
12. **Données fictives étiquetées** : hors du principe « ne rien inventer », une démonstration/un test peut autoriser (sur accord humain explicite) des KPI/CAPEX-OPEX/feuille de route inventés — chacun **clairement étiqueté « démonstration »**, la méthode restant réelle ; ne jamais brouiller la frontière fictif/réel.

## Formats de sortie

- **HTML dynamique** : fichier **unique autoportant** (CSS/JS/logo/SVG **inline**, aucune dépendance externe ni CDN). **Suivre les instructions `instructions/presentation-html-dynamique.md`** (le HTML est construit section par section, pas de modèle à copier) : les **sections dépendent du type** de présentation choisi, et chaque diagramme utilise **le type `archify` adapté** (Architecture, Workflow, Sequence, Data Flow, Lifecycle) collé en SVG inline, ou le moteur natif « System overview » animé/interactif (filtres de canaux, survol/clic, flux animé, règles de géométrie R1–R5) pour les schémas nœuds/arêtes. Styles des diagrammes : partir du thème du projet (`theme/`, par défaut `theme/0000-default-styles.dsl`) — voir règle d'or [Charte graphique client](#règles-dor). Responsive, `prefers-reduced-motion` respecté. La skill **`archify`** reste la référence pour générer les diagrammes en code (export PNG/JPEG/WebP/SVG/WebM).
- **PowerPoint (.pptx)** — recommandation (tokens minimisés + compatibilité) :
  - **Par défaut : Marp** (Markdown → PPTX). Le contenu est rédigé en **Markdown compact** (peu de tokens), converti de façon **déterministe** en `.pptx` ; thèmes CSS pour la charte ; bonne compatibilité PowerPoint/LibreOffice/Keynote.
  - **Quand le client fournit un gabarit `.pptx`** : **Pandoc** avec `--reference-doc <gabarit-client.pptx>` (reprend la charte, les masques et polices du client).
  - Éviter `python-pptx` sauf mise en page programmatique précise : la génération élément par élément est beaucoup plus verbeuse (coûteuse en tokens).
  - Dans tous les cas, produire un **intermédiaire Markdown** (source unique, réutilisable pour HTML et PPTX) plutôt que d'émettre l'OOXML à la main.

## Arrimage avec les autres skills

- `references/archify-diagram-types.md` : **source unique** de la correspondance public/thème → recette → type Archify (5 types, 12 recettes, compositions, trace, détail par chapitre technique). SKILL.md et gabarits y renvoient **sans la recopier**.
- `presentation-targeting` : repère, dans les documents d'architecture du projet, où se trouve l'information (front-matter des gabarits d'architecture).
- `architecture-solution-gabarits` : lecture des documents d'architecture source (DAS).
- `archify` (skill importée dans le workspace ; source amont https://github.com/tt-a1i/archify) : production des diagrammes dynamiques (HTML/SVG, thèmes, export PNG/JPEG/WebP/SVG/WebM) ; accepte des exigences en langage naturel ou du Mermaid (flowchart, sequenceDiagram, stateDiagram). Le **choix du type** (recette/composition/trace) est cadré **uniquement** par [`references/archify-diagram-types.md`](references/archify-diagram-types.md) et sa [table de correspondance public/thème → recette](references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique). Les **styles de rendu** (couleurs, formes, typographie) proviennent du thème du projet (`theme/`, par défaut `theme/0000-default-styles.dsl`) — voir règle d'or [Charte graphique client](#règles-dor).
- `project-defaults` : structure du projet et emplacement d'archivage des livrables.
