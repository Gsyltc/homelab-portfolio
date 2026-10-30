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

Processus et règles : source unique dans `core/common/protocols/architecture-checklist.md` (structure imposée, barème 80/10/10, calcul du %, écriture sur faits vérifiés, décompte par section mandatory des Livrables, mapping Livrables → documents).

Règles de tenue :
- Chaque élément porte un % d'avancement (0–100). Défaut : 0 %.
- Barème 80/10/10 par élément : % = 80 × (sections conformes / total sections mandatory) + 10 × (revue pair) + 10 × (acceptation humaine).
  - Hors Livrables (Cadrage, Besoins, Projets) : part 80 % binaire (0 ou 80) — élément présent et conforme = 80.
  - Livrables : part 80 % = 80 × (sections mandatory conformes / total), total = contrat required-sections (dénominateur dynamique).
  - revue pair et acceptation humaine valent 0 ou 10. L'acceptation (+10) ne s'ajoute QUE sur annonce humaine explicite.
- % section = moyenne des % de ses éléments ; % global = moyenne des % de tous les éléments. Arrondi à l'entier.
- Gate planification / réalisation : < 80 % ⇒ bloqué ; ≥ 80 % ⇒ déblocable (lancement soumis à décision humaine).
- Chaque changement de % est tracé sur l'issue (piste d'audit), avec la composante modifiée.
- Ce fichier est un livrable : aucune note de génération / méta-production (réf. décision 0040).
- Ne jamais deviner : une section ne compte conforme que si présente et non vide ; en cas de doute, ne pas compter, informer l'humain.
- Les sous-tableaux par section mandatory des Livrables s'appuient sur le contrat required-sections (source unique) ; en cas d'écart, le sensor fait foi.
- Arrimages (section Projets) est décomposé par rôles mandatory : part 80 % = 80 × (rôles présents et nommés / total). Total = 5 rôles, ou 6 si Loi 25 activée (Responsable Légal). Le couple Architecte de solution / intégrateur compte pour un seul rôle (l'un ou l'autre). Source de la liste : matrice RACI du DAS 001.
-->

**% global :** 0 %

## Cadrage — 0 %

| Élément | Sections conformes | Part 80 % | Revue pair (+10) | Acceptation humaine (+10) | % |
| --- | --- | --- | --- | --- | --- |
| Cadrage | — (unité suivie) | 0 | 0 | 0 | 0 % |

## Besoins (MoSCoW) — 0 %

| Élément | Sections conformes | Part 80 % | Revue pair (+10) | Acceptation humaine (+10) | % |
| --- | --- | --- | --- | --- | --- |
| Entreprises et affaires | — (unité suivie) | 0 | 0 | 0 | 0 % |
| Solutions | — (unité suivie) | 0 | 0 | 0 | 0 % |
| Technologique | — (unité suivie) | 0 | 0 | 0 | 0 % |
| Sécurité | — (unité suivie) | 0 | 0 | 0 | 0 % |

## Livrables — 0 %

Synthèse (une ligne par livrable, % issu du sous-tableau correspondant) :

| Élément | Part 80 % (sections) | Revue pair (+10) | Acceptation humaine (+10) | % |
| --- | --- | --- | --- | --- |
| Architecture de solution (DAS) | 0 | 0 | 0 | 0 % |
| Architecture Logicielle détaillée | 0 | 0 | 0 | 0 % |
| Architecture de données détaillée | 0 | 0 | 0 | 0 % |
| Architecture de sécurité détaillée | 0 | 0 | 0 | 0 % |
| Architecture infrastructure détaillée | 0 | 0 | 0 | 0 % |

### Architecture de solution (DAS) — 0 %

Part 80 % = 80 × (fichiers mandatory conformes / total). Total et sections mandatory : contrat `required-sections`, volet `das:` (7 fichiers mandatory — source unique, dénominateur dynamique).

| Section mandatory (fichier DAS) | Présente et conforme ? |
| --- | --- |
| `001-document-architecture-solution.md` | non |
| `01-introduction.md` | non |
| `02-objectifs.md` | non |
| `06-architecture-solutions.md` | non |
| `08-contraintes.md` | non |
| `10-cycle_vie_donnees.md` | non |
| `11-securite.md` | non |

| Composante | Valeur |
| --- | --- |
| Part 80 % = 80 × (conformes / total) | 0 |
| Revue pair (+10) | 0 |
| Acceptation humaine (+10) | 0 |
| **% élément** | **0 %** |

### Architecture Logicielle détaillée — 0 %

Part 80 % = 80 × (sections conformes / total). Sections attendues : gabarit DAS `00-architecture-detaillee` (volet logiciel). Renseigner les sections mandatory du livrable.

| Section mandatory | Présente et conforme ? |
| --- | --- |
| _(à renseigner selon le contrat de sections du livrable)_ | non |

| Composante | Valeur |
| --- | --- |
| Part 80 % = 80 × (conformes / total) | 0 |
| Revue pair (+10) | 0 |
| Acceptation humaine (+10) | 0 |
| **% élément** | **0 %** |

### Architecture de données détaillée — 0 %

Part 80 % = 80 × (sections conformes / total). Sections attendues : sensor `data-lifecycle` + `10-cycle_vie_donnees.md` et modèles de données.

| Section mandatory | Présente et conforme ? |
| --- | --- |
| _(à renseigner selon le contrat de sections du livrable)_ | non |

| Composante | Valeur |
| --- | --- |
| Part 80 % = 80 × (conformes / total) | 0 |
| Revue pair (+10) | 0 |
| Acceptation humaine (+10) | 0 |
| **% élément** | **0 %** |

### Architecture de sécurité détaillée — 0 %

Part 80 % = 80 × (sections conformes / total). Sections attendues : `required-sections`, fichier `11-securite.md` (STRIDE / sécurité applicative).

| Section mandatory | Présente et conforme ? |
| --- | --- |
| `Modélisation des menaces (STRIDE)` | non |
| `Sécurité applicative` | non |

| Composante | Valeur |
| --- | --- |
| Part 80 % = 80 × (conformes / total) | 0 |
| Revue pair (+10) | 0 |
| Acceptation humaine (+10) | 0 |
| **% élément** | **0 %** |

### Architecture infrastructure détaillée — 0 %

Part 80 % = 80 × (sections conformes / total). Sections attendues : gabarit DAS `09-deploiement` + diagrammes d'infrastructure.

| Section mandatory | Présente et conforme ? |
| --- | --- |
| _(à renseigner selon le contrat de sections du livrable)_ | non |

| Composante | Valeur |
| --- | --- |
| Part 80 % = 80 × (conformes / total) | 0 |
| Revue pair (+10) | 0 |
| Acceptation humaine (+10) | 0 |
| **% élément** | **0 %** |

## Projets — 0 %

Synthèse (Arrimages est décomposé par rôles mandatory — voir le sous-tableau dédié) :

| Élément | Sections conformes | Part 80 % | Revue pair (+10) | Acceptation humaine (+10) | % |
| --- | --- | --- | --- | --- | --- |
| Planification | — (unité suivie) | 0 | 0 | 0 | 0 % |
| Coûts | — (unité suivie) | 0 | 0 | 0 | 0 % |
| Risques | — (unité suivie) | 0 | 0 | 0 | 0 % |
| Exploitation | — (unité suivie) | 0 | 0 | 0 | 0 % |
| Arrimages | rôles mandatory (sous-tableau) | 0 | 0 | 0 | 0 % |

### Arrimages — 0 %

Part 80 % = 80 × (rôles mandatory conformes / total). Un rôle est **conforme** s'il est **présent et nommé** (colonne « Nom » renseignée) dans la matrice RACI « Arrimage des rôles » du DAS `documentation/001-document-architecture-solution.md` (source). Dénominateur : **5** rôles mandatory, **6** si la **Loi 25** est activée (le Responsable Légal entre alors au dénominateur).

| Rôle mandatory | Présent et nommé ? |
| --- | --- |
| Architecte de solution **ou** Architecte de solution intégrateur (l'un ou l'autre) | non |
| Chef de projet | non |
| Responsable produit | non |
| Responsable Affaires | non |
| Lead Assurance Qualité | non |
| Responsable Légal _(uniquement si Loi 25 activée — sinon hors dénominateur)_ | n/a |

| Composante | Valeur |
| --- | --- |
| Part 80 % = 80 × (conformes / total) | 0 |
| Revue pair (+10) | 0 |
| Acceptation humaine (+10) | 0 |
| **% élément** | **0 %** |
