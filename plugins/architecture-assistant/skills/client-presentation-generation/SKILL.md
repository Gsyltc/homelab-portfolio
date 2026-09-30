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

Chaque gabarit décrit les **chapitres nécessaires** au type, les **sources d'architecture** à cibler (fichiers DAS), et le rappel du **patron narratif**.

## Quand utiliser

- Structurer et produire une présentation client d'un type donné à partir des documents d'architecture validés.
- Sélectionner le gabarit correspondant au type, ne conserver que les chapitres pertinents aux sujets demandés.

## Règles d'or

1. **Un gabarit par type** : sélectionner le fichier de `gabarits/` correspondant au type ; ne pas fusionner les types.
2. **Cibler avant de produire** : localiser l'information dans les documents d'architecture via `presentation-targeting` (front-matter) ; ne charger que les sections utiles.
3. **Fidélité à la source** : n'inventer ni chiffres, ni garanties, ni fonctionnalités absents des livrables validés ; en cas de doute, remonter au coordinateur.
4. **Lisibilité d'abord** : titres clairs, une idée par section/diapositive, visuels et tableaux, progression logique. Appliquer le patron `Contexte → Objectifs → Moyens → Méthodes → Résultats` quand adapté.
5. **Diagrammes Archify** : produits avec la skill `archify` (générés en code, syntaxe validée avant export) ; réutiliser ceux des livrables, produire une version simplifiée si nécessaire.
6. **Nomenclature client** (Technique/Fonctionnelle) : nommer chaque domaine selon la nomenclature du client.
7. **Charte graphique client** : appliquer couleurs, logo, typographie et gabarit fournis ; à défaut, gabarit neutre validé.
8. **Format contraint par type** : respecter la colonne « Formats » du tableau (Technique/Fonctionnelle = HTML dynamique uniquement). Demander le format si plusieurs sont autorisés et non précisé.
9. **Confidentialité** : jamais de secret, d'identifiant ni de donnée interne non destinée au client ; tenir compte de la sensibilité des sources.
10. **Langue** : celle du destinataire (français par défaut).

## Formats de sortie

- **HTML dynamique** : fichier autoportant (CSS/JS inline si possible), diagrammes produits avec la skill **`archify`** (SVG inline, thèmes clair/sombre, export PNG/JPEG/WebP/SVG/WebM), responsive.
- **PowerPoint (.pptx)** — recommandation (tokens minimisés + compatibilité) :
  - **Par défaut : Marp** (Markdown → PPTX). Le contenu est rédigé en **Markdown compact** (peu de tokens), converti de façon **déterministe** en `.pptx` ; thèmes CSS pour la charte ; bonne compatibilité PowerPoint/LibreOffice/Keynote.
  - **Quand le client fournit un gabarit `.pptx`** : **Pandoc** avec `--reference-doc <gabarit-client.pptx>` (reprend la charte, les masques et polices du client).
  - Éviter `python-pptx` sauf mise en page programmatique précise : la génération élément par élément est beaucoup plus verbeuse (coûteuse en tokens).
  - Dans tous les cas, produire un **intermédiaire Markdown** (source unique, réutilisable pour HTML et PPTX) plutôt que d'émettre l'OOXML à la main.

## Arrimage avec les autres skills

- `presentation-targeting` : repère, dans les documents d'architecture du projet, où se trouve l'information (front-matter des gabarits d'architecture).
- `architecture-solution-gabarits` : lecture des documents d'architecture source (DAS).
- `archify` : production des diagrammes dynamiques (HTML/SVG, thèmes, export PNG/JPEG/WebP/SVG/WebM) ; accepte des exigences en langage naturel ou du Mermaid (flowchart, sequenceDiagram, stateDiagram).
- `project-defaults` : structure du projet et emplacement d'archivage des livrables.
