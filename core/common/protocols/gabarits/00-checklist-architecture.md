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

Processus et règles : source unique dans `core/common/protocols/architecture-checklist.md` (structure imposée, barème, écriture sur faits vérifiés).

Règles de tenue :
- Chaque élément porte un % d'avancement (0–100). Défaut : 0 %.
- La conformité se constate : une section ne compte que si elle est présente, non vide et documentée pour le projet ; en cas de doute, ne pas compter et informer l'humain.
- Revue pair et acceptation humaine : oui / non. L'acceptation ne s'ajoute que sur annonce humaine explicite.
- Chaque changement de % est tracé sur l'issue (piste d'audit), avec la composante modifiée.
- Ce fichier est un livrable : aucune note de génération / méta-production (réf. décision 0040).
- Ce fichier présente l'état, jamais le calcul : ni formule, ni opération, ni rappel du barème.
- Les sections requises par livrable sont portées par le contrat `required-sections` (source unique) ; ce gabarit en déploie les tables de suivi, sans redéfinir le contrat. En cas d'écart de nommage, `required-sections` fait foi.
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
Élément récapitulatif : la priorisation MoSCoW des besoins d'affaires est tracée en amont (stage inception requirements-analysis, identifiants stables BA-…). Lorsqu'une méthodologie OpenSpec est active, elle est consolidée dans la « Matrice de traçabilité MoSCoW » du proposal.md (chaîne spec ↔ besoin ↔ exigence, un scénario / cas d'utilisation par ligne), qui sert de récapitulatif pour constater la conformité des éléments ci-dessus. Processus et règles de conformité : source unique dans core/common/protocols/architecture-checklist.md (sections 2 et 6). Ce gabarit ne redéfinit pas la matrice ; il en constate le résultat.
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

Sections requises : fichiers mandatory du DAS (contrat `required-sections`, volet `das:`).

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

Sections requises : sept sections, réparties sur le chapitre `architecture-securite/` et le fichier `11-securite.md` (contrat `required-sections`, volets `das:` et `securite:`).

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
