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
Gabarit d'état de la checklist d'architecture. À copier en `documentation/00-checklist-architecture.md` au sein du répertoire d'un projet (fichier d'état de processus, non DAS).

Processus et règles de tenue (structure imposée, barème 80/10/10, conformité constatée, revue pair / acceptation humaine, écriture sur faits vérifiés, piste d'audit) : source unique dans `core/common/protocols/architecture-checklist.md`. Ne pas les rediter ici.

Usage du fichier : présenter l'ÉTAT, jamais le calcul — ni formule, ni opération, ni rappel du barème.
-->

**% global :** 0 %

## Cadrage — 0 %

| Élément | Conformité | Revue pair | Acceptation humaine | % |
| --- | --- | --- | --- | --- |
| Cadrage | non conforme | non | non | 0 % |

## Besoins (MoSCoW) — 0 %

| Élément | Conformité | Revue pair | Acceptation humaine | % |
| --- | --- | --- | --- | --- |
| Entreprises et affaires | non conforme | non | non | 0 % |
| Solutions | non conforme | non | non | 0 % |
| Technologique | non conforme | non | non | 0 % |
| Sécurité | non conforme | non | non | 0 % |

<!--
Conformité MoSCoW constatée via la priorisation amont (BA-…) et, si OpenSpec actif, la matrice de traçabilité du proposal.md. Processus et règles : source unique dans core/common/protocols/architecture-checklist.md (sections 2 et 6). Ce gabarit constate le résultat, il ne redéfinit pas la matrice.
-->

## Livrables — 0 %

Synthèse (une ligne par livrable, % issu du sous-tableau correspondant) :

| Élément | Sections conformes | Revue pair | Acceptation humaine | % |
| --- | --- | --- | --- | --- |
| Architecture de solution (DAS) | 0 / 7 | non | non | 0 % |
| Architecture Logicielle détaillée | 0 / n | non | non | 0 % |
| Architecture de données détaillée | 0 / n | non | non | 0 % |
| Architecture de sécurité détaillée | 0 / 7 | non | non | 0 % |
| Architecture infrastructure détaillée | 0 / n | non | non | 0 % |

### Architecture de solution (DAS) — 0 %

Sections requises : fichiers mandatory du DAS (sensor `required-sections-architecture`).

| Section requise (fichier DAS) | Conforme ? |
| --- | --- |
| `001-document-architecture-solution.md` | non |
| `01-introduction.md` | non |
| `02-objectifs.md` | non |
| `06-architecture-solutions.md` | non |
| `08-contraintes.md` | non |
| `10-cycle_vie_donnees.md` | non |
| `11-securite.md` | non |
| **Total** | **0 / 7** |

### Architecture Logicielle détaillée — 0 %

Sections requises : gabarit DAS `00-architecture-detaillee` (volet logiciel).

| Section requise | Conforme ? |
| --- | --- |
| _(à renseigner selon le contrat de sections du livrable)_ | non |
| **Total** | **0 / n** |

### Architecture de données détaillée — 0 %

Sections requises : sensor `data-lifecycle` + `10-cycle_vie_donnees.md` et modèles de données.

| Section requise | Conforme ? |
| --- | --- |
| _(à renseigner selon le contrat de sections du livrable)_ | non |
| **Total** | **0 / n** |

### Architecture de sécurité détaillée — 0 %

Sections requises : sept sections, réparties sur le chapitre `architecture-securite/` et le fichier `11-securite.md` (sensor `required-sections-architecture`).

| Section requise | Document | Conforme ? |
| --- | --- | --- |
| Surfaces d'attaque | `architecture-securite/01-surfaces-et-actifs.md` | non |
| Modélisation des menaces (STRIDE) | `architecture-securite/02-menaces-stride.md` | non |
| Modélisation OWASP | `architecture-securite/03-risques-owasp.md` | non |
| Sécurité applicative | `11-securite.md`, section « Sécurité applicative » | non |
| Frontières de confiance, avec diagramme | `11-securite.md`, section « Frontières de confiance » | non |
| Sécurité Infrastructure | `11-securite.md`, section « Sécurité Infrastructure » | non |
| Gestion des identités et des accès | `11-securite.md`, section « Gestion des identités et des accès (GIA) » | non |
| **Total** | | **0 / 7** |

### Architecture infrastructure détaillée — 0 %

Sections requises : gabarit DAS `09-deploiement` + diagrammes d'infrastructure.

| Section requise | Conforme ? |
| --- | --- |
| _(à renseigner selon le contrat de sections du livrable)_ | non |
| **Total** | **0 / n** |

## Projets — 0 %

Synthèse (Arrimages est décomposé par rôles mandatory — voir le sous-tableau dédié) :

| Élément | Conformité | Revue pair | Acceptation humaine | % |
| --- | --- | --- | --- | --- |
| Planification | non conforme | non | non | 0 % |
| Coûts | non conforme | non | non | 0 % |
| Risques | non conforme | non | non | 0 % |
| Exploitation | non conforme | non | non | 0 % |
| Arrimages | 0 / 5 rôles | non | non | 0 % |

### Arrimages — 0 %

Rôles mandatory : source unique dans la matrice « Arrimage des rôles » du DAS `001-document-architecture-solution.md`. Un rôle est conforme s'il est présent et nommé (colonne « Nom » renseignée). Dénominateur : 5 rôles, ou 6 si la Loi 25 est activée (le Responsable Légal entre alors au dénominateur).

| Rôle mandatory | Présent et nommé ? |
| --- | --- |
| Architecte de solution **ou** Architecte de solution intégrateur (l'un ou l'autre) | non |
| Chef de projet | non |
| Responsable produit | non |
| Responsable Affaires | non |
| Lead Assurance Qualité | non |
| Responsable Légal _(uniquement si Loi 25 activée — sinon hors dénominateur)_ | n/a |
| **Total** | **0 / 5** |
