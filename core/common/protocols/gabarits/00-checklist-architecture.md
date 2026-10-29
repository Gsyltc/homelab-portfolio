---
doc_id: checklist-architecture
theme: Checklist d'architecture — état d'avancement
domaine: [transverse]
sujets:
  - Cadrage
  - Besoins (MoSCoW)
  - Livrables
  - Projets
types_presentation: [executive]
sensibilite: interne
togaf_layer: null
ordre_presentation: 0
---
# Checklist d'architecture — état d'avancement

<!--
Gabarit d'état à copier en `documentation/00-checklist-architecture.md` lors de l'initialisation (Phase 0). Les valeurs ci-dessous sont un INSTANTANÉ INITIAL (tout à 0 %), recalculé à chaque mise à jour.
Processus, barème, unité de décompte, gate et garde-fous : source unique dans `core/common/protocols/architecture-checklist.md`. Ne pas dupliquer ses règles ici.
-->

**% global :** 0 %

> Le `%` est un **indicateur d'avancement** (instantané recalculé). Le **gate** d'un élément (frontière `Inception → Construction`, advisory) exige la **conformité complète** (`Conf. complète = ✓`) et, pour les surfaces de sécurité (🔒), le **verdict favorable du Reviewer de sécurité** (`Revue sécu = ✓`) — jamais une moyenne. Détail : protocole §3, §6, §7.

## Cadrage — 0 %

| Élément | Sections conformes / total | Conf. complète | Revue (nature) | Acceptation humaine | Version évaluée | % |
| --- | --- | --- | --- | --- | --- | --- |
| Cadrage | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |

## Besoins (MoSCoW) — 0 %

| Élément | Sections conformes / total | Conf. complète | Revue (nature) | Acceptation humaine | Version évaluée | % |
| --- | --- | --- | --- | --- | --- | --- |
| Entreprises et affaires | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Solutions | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Technologique | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| 🔒 Sécurité | 0 / 1 *(convention)* | ✗ | ✗ (**sécurité** SG-3) | ✗ | — | 0 % |

🔒 = surface de sécurité : revue de sécurité (SG-3) **précède** le gate ; non compensable par la moyenne. `*(convention)*` = élément sans contrat de sections mandatory, `total = 1` par convention, conformité jugée par la revue de cohérence (protocole §6).

## Livrables — 0 %

Le terme **80 %** est proportionnel aux **sections mandatory présentes et non vides**, décomptées **à la section** (contrat `required-sections`, source unique ; total **dynamique**). `Conf. complète = ✓` seulement si **toutes** les sections mandatory sont conformes.

| Élément | Sections conformes / total | Conf. complète | Revue (nature) | Acceptation humaine | Version évaluée | % |
| --- | --- | --- | --- | --- | --- | --- |
| Architecture de solution (DAS) | 0 / 18 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Architecture Logicielle détaillée | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Architecture de données détaillée | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| 🔒 Architecture de sécurité détaillée | 0 / 2 | ✗ | ✗ (**sécurité** SG-3) | ✗ | — | 0 % |
| Architecture infrastructure détaillée | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |

### Détail DAS — sections mandatory par fichier (contrat `required-sections`, total 18)

Instantané du contrat au moment de la copie ; recalculé si le contrat évolue (ne pas figer une liste divergente).

| Fichier mandatory | Sections mandatory | Conformes / total |
| --- | --- | --- |
| `001-document-architecture-solution.md` | Métadonnées · Historique · Arrimages · Structure | 0 / 4 |
| `01-introduction.md` | Contexte · Périmètre · Parties prenantes | 0 / 3 |
| `02-objectifs.md` | Objectifs · NFRs · Matrice de suivi | 0 / 3 |
| `06-architecture-solutions.md` | Description · Liste des diagrammes | 0 / 2 |
| `08-contraintes.md` | Lois et règlementations · Conformités | 0 / 2 |
| `10-cycle_vie_donnees.md` | Gouvernance de données · Classification | 0 / 2 |
| `11-securite.md` 🔒 | Modélisation des menaces (STRIDE) · Sécurité applicative | 0 / 2 |

> Mapping des autres livrables (documents attendus, contrats, conventions `total = 1`) et double comptage de `11-securite.md` / `10-cycle_vie_donnees.md` : voir protocole §6. Non redupliqué ici.

## Projets — 0 %

| Élément | Sections conformes / total | Conf. complète | Revue (nature) | Acceptation humaine | Version évaluée | % |
| --- | --- | --- | --- | --- | --- | --- |
| Planification | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Coûts | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Risques | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Exploitation | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Arrimages | 0 / 1 *(convention)* | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
