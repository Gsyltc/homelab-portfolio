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

Processus et règles : source unique dans `core/common/protocols/architecture-checklist.md` (structure imposée, calcul du %, barème 80/10/10, écriture, vérification de conformité, mapping Livrables → documents, gate par élément).

Règles de tenue :
- % par élément (barème homogène, INDICATEUR d'avancement — pas le seul critère de gate) : `% = 80 × (sections conformes / total sections) + 10·(revue) + 10·(acceptation humaine)`. Arrondi à l'entier pour l'AFFICHAGE seulement ; la comparaison au seuil se fait sur la valeur non arrondie.
- Terme 80 % = sections mandatory présentes et non vides (contrat `required-sections`, source unique). Total dynamique. « Présent et non vide » est un plancher de forme, jamais un niveau de sécurité atteint.
- Revue (+10 %) = verdict du reviewer dédié POSTÉ, FAVORABLE, sans point bloquant ouvert, rattaché à la version courante. Pour les surfaces de sécurité (Besoins → Sécurité, Architecture de sécurité détaillée), c'est le verdict du REVIEWER DE SÉCURITÉ (SG-3) — la cohérence s'ajoute, jamais à la place.
- Acceptation humaine (+10 %) = annonce explicite d'un MEMBRE humain (auteur `member`, cité par identifiant), rattachée à la version courante. Un commentaire d'agent, même cité par un humain, ne compte pas.
- Rattachement version : tout changement d'un contenu mandatory remet revue ET acceptation à zéro (tracé sur l'issue).
- % section = moyenne des % éléments ; % global = moyenne des % de tous les éléments. La moyenne ne compense JAMAIS un élément faible au gate.
- Gate PAR ÉLÉMENT : débloquable seulement si conformité COMPLÈTE (toutes sections mandatory conformes) ; pour les surfaces de sécurité, verdict favorable du Reviewer de sécurité REQUIS AVANT le déblocage. Lancement soumis à décision humaine. Colonnes « Conf. complète » et « Revue sécu » affichées au gate.
- Chaque évolution de % est tracée sur l'issue (piste d'audit), avec preuve et version.
- Ce fichier est un livrable : aucune note de génération / méta-production (réf. décision 0040).
- Ne jamais deviner : un % ne résulte que d'une vérification objective ; en cas de doute, ne pas créditer, informer l'humain.
-->

**% global :** 0 %

> Le `%` est un **indicateur d'avancement**. Le **déblocage au gate** d'un élément exige la **conformité complète** (`Conf. complète = ✓`) et, pour les surfaces de sécurité (🔒), le **verdict favorable du Reviewer de sécurité** (`Revue sécu = ✓`) — jamais une moyenne.

## Cadrage — 0 %

| Élément | Sections conformes / total | Conf. complète | Revue (nature) | Acceptation humaine | Version évaluée | % |
| --- | --- | --- | --- | --- | --- | --- |
| Cadrage | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |

## Besoins (MoSCoW) — 0 %

| Élément | Sections conformes / total | Conf. complète | Revue (nature) | Acceptation humaine | Version évaluée | % |
| --- | --- | --- | --- | --- | --- | --- |
| Entreprises et affaires | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Solutions | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Technologique | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| 🔒 Sécurité | 0 / 1 | ✗ | ✗ (**sécurité** SG-3) | ✗ | — | 0 % |

🔒 = surface de sécurité : revue de sécurité (SG-3) **requise avant déblocage** ; non compensable par la moyenne.

## Livrables — 0 %

Pour chaque livrable, le terme **80 %** est proportionnel aux **sections mandatory présentes et non vides** (contrat `required-sections`, source unique ; total **dynamique**). Les sous-tableaux détaillent le décompte. `Conf. complète = ✓` seulement si **toutes** les sections mandatory sont conformes.

| Élément | Sections conformes / total | Conf. complète | Revue (nature) | Acceptation humaine | Version évaluée | % |
| --- | --- | --- | --- | --- | --- | --- |
| Architecture de solution (DAS) | 0 / 7 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Architecture Logicielle détaillée | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Architecture de données détaillée | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| 🔒 Architecture de sécurité détaillée | 0 / 1 | ✗ | ✗ (**sécurité** SG-3) | ✗ | — | 0 % |
| Architecture infrastructure détaillée | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |

### Détail — Architecture de solution (DAS)

Fichiers mandatory du DAS (contrat `required-sections`, volet `das:`). Le **total** suit le contrat : toute évolution du manifeste `required-sections` met à jour le dénominateur (ne pas figer ici une liste divergente). `11-securite.md` et `10-cycle_vie_donnees.md` comptent aussi, respectivement, dans « Architecture de sécurité détaillée » et « Architecture de données détaillée » (double comptage assumé).

| Fichier mandatory | Présent et non vide |
| --- | --- |
| `001-document-architecture-solution.md` | ✗ |
| `01-introduction.md` | ✗ |
| `02-objectifs.md` | ✗ |
| `06-architecture-solutions.md` | ✗ |
| `08-contraintes.md` | ✗ |
| `10-cycle_vie_donnees.md` | ✗ |
| `11-securite.md` 🔒 | ✗ |

### Détail — autres livrables détaillés

Livrables suivis comme une unité (terme 80 % atteint lorsque le document attendu est présent et conforme ; contrat de sections dans la source indiquée). « Présent et conforme » est un plancher de forme ; le fond relève de la revue.

| Élément | Document(s) attendu(s) | Contrat de sections | Présent et conforme |
| --- | --- | --- | --- |
| Architecture Logicielle détaillée | `00-architecture-detaillee.md` | gabarit DAS `00-architecture-detaillee` | ✗ |
| Architecture de données détaillée | `10-cycle_vie_donnees.md` + modèles | sensor `data-lifecycle` | ✗ |
| 🔒 Architecture de sécurité détaillée | `11-securite.md` (STRIDE / OWASP) | `required-sections`, `11-securite.md` | ✗ |
| Architecture infrastructure détaillée | `09-deploiement.md` + diagrammes | gabarit DAS `09-deploiement` | ✗ |

## Projets — 0 %

| Élément | Sections conformes / total | Conf. complète | Revue (nature) | Acceptation humaine | Version évaluée | % |
| --- | --- | --- | --- | --- | --- | --- |
| Planification | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Coûts | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Risques | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Exploitation | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
| Arrimages | 0 / 1 | ✗ | ✗ (cohérence) | ✗ | — | 0 % |
