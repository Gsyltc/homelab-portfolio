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
Gabarit d'état de la checklist d'architecture. À copier en `documentation/00-checklist-architecture.md` au sein du répertoire d'un projet, lors de l'initialisation (Phase 0).

Processus et règles : source unique dans `core/common/protocols/architecture-checklist.md` (structure imposée, calcul du %, barème 80/10/10, écriture, vérification de conformité, mapping Livrables → documents, gate ≥ 80 %).

Règles de tenue :
- % par élément (barème homogène) : `% = 80 × (sections conformes / total sections) + 10·(revue pair) + 10·(acceptation humaine)`, arrondi à l'entier.
- Terme 80 % = sections mandatory présentes et non vides (contrat `required-sections`, source unique). Total dynamique : une nouvelle section/fichier mandatory s'ajoute au dénominateur.
- Revue pair (+10 %) = verdict du reviewer dédié POSTÉ. Acceptation humaine (+10 %) = annonce humaine explicite. Aucun agent ne s'auto-accepte.
- % section = moyenne des % éléments de la section ; % global = moyenne des % de tous les éléments. Arrondis à l'entier.
- Gate : < 80 % ⇒ bloqué ; ≥ 80 % ⇒ déblocage possible (lancement soumis à décision humaine ; revue pair + acceptation possibles en parallèle).
- Chaque évolution de % est tracée sur l'issue (piste d'audit).
- Ce fichier est un livrable : aucune note de génération / méta-production (réf. décision 0040).
- Ne jamais deviner : un % ne résulte que d'une vérification objective ; en cas de doute, ne pas créditer, informer l'humain.
-->

**% global :** 0 %

## Cadrage — 0 %

| Élément | Sections conformes / total | Revue pair | Acceptation humaine | % |
| --- | --- | --- | --- | --- |
| Cadrage | 0 / 1 | ✗ | ✗ | 0 % |

## Besoins (MoSCoW) — 0 %

| Élément | Sections conformes / total | Revue pair | Acceptation humaine | % |
| --- | --- | --- | --- | --- |
| Entreprises et affaires | 0 / 1 | ✗ | ✗ | 0 % |
| Solutions | 0 / 1 | ✗ | ✗ | 0 % |
| Technologique | 0 / 1 | ✗ | ✗ | 0 % |
| Sécurité | 0 / 1 | ✗ | ✗ | 0 % |

## Livrables — 0 %

Pour chaque livrable, le terme **80 %** est proportionnel aux **sections mandatory présentes et non vides** (contrat `required-sections`, source unique ; total **dynamique**). Les sous-tableaux détaillent le décompte.

| Élément | Sections conformes / total | Revue pair | Acceptation humaine | % |
| --- | --- | --- | --- | --- |
| Architecture de solution (DAS) | 0 / 7 | ✗ | ✗ | 0 % |
| Architecture Logicielle détaillée | 0 / 1 | ✗ | ✗ | 0 % |
| Architecture de données détaillée | 0 / 1 | ✗ | ✗ | 0 % |
| Architecture de sécurité détaillée | 0 / 1 | ✗ | ✗ | 0 % |
| Architecture infrastructure détaillée | 0 / 1 | ✗ | ✗ | 0 % |

### Détail — Architecture de solution (DAS)

Fichiers mandatory du DAS (contrat `required-sections`, volet `das:`). Le **total** suit le contrat : toute évolution du manifeste `required-sections` met à jour le dénominateur (ne pas figer ici une liste divergente).

| Fichier mandatory | Présent et non vide |
| --- | --- |
| `001-document-architecture-solution.md` | ✗ |
| `01-introduction.md` | ✗ |
| `02-objectifs.md` | ✗ |
| `06-architecture-solutions.md` | ✗ |
| `08-contraintes.md` | ✗ |
| `10-cycle_vie_donnees.md` | ✗ |
| `11-securite.md` | ✗ |

### Détail — autres livrables détaillés

Livrables suivis comme une unité (terme 80 % atteint lorsque le document attendu est présent et conforme ; contrat de sections dans la source indiquée).

| Élément | Document(s) attendu(s) | Contrat de sections | Présent et conforme |
| --- | --- | --- | --- |
| Architecture Logicielle détaillée | `00-architecture-detaillee.md` | gabarit DAS `00-architecture-detaillee` | ✗ |
| Architecture de données détaillée | `10-cycle_vie_donnees.md` + modèles | sensor `data-lifecycle` | ✗ |
| Architecture de sécurité détaillée | `11-securite.md` (STRIDE / OWASP) | `required-sections`, `11-securite.md` | ✗ |
| Architecture infrastructure détaillée | `09-deploiement.md` + diagrammes | gabarit DAS `09-deploiement` | ✗ |

## Projets — 0 %

| Élément | Sections conformes / total | Revue pair | Acceptation humaine | % |
| --- | --- | --- | --- | --- |
| Planification | 0 / 1 | ✗ | ✗ | 0 % |
| Coûts | 0 / 1 | ✗ | ✗ | 0 % |
| Risques | 0 / 1 | ✗ | ✗ | 0 % |
| Exploitation | 0 / 1 | ✗ | ✗ | 0 % |
| Arrimages | 0 / 1 | ✗ | ✗ | 0 % |
