---
id: required-sections-architecture
kind: deterministic
command: "python3 core/scripts/sensors/required_sections_architecture.py"
default_severity: advisory
description: "Vérifie que les fichiers et sections mandatory de l'architecture — DAS et architecture détaillée (chapitre architecture-securite/) — sont présents et non vides."
category: document-shape
fire_on: gate
matches: "{documentation/*.md,documentation/**/*.md}"
origine: ALI-218
---

# Sensor `required-sections-architecture` — sections requises de l'architecture (DAS et détaillée)

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie que les **fichiers et rubriques mandatory** de la **DAS** et de l'**architecture détaillée** (chapitre `architecture-securite/`) sont présents et non vides. **Advisory** (`default_severity: advisory`).

Issu de la scission du sensor unique `required-sections` (HOM-285) : deux manifestes, un pour les ADR ([`required-sections-adr`](required-sections-adr.md)), un pour l'architecture (celui-ci), pour éviter les confusions entre types de documents.

## Contrat de vérification (`checks`)

```yaml
checks:
  das:                                         # fichiers DAS mandatory portés en propre (Option A, ADR-0025) — indépendants des gabarits (ADR-0012, NEG-004)
    fichiers_mandatory:                        # présents ET non vides dans le répertoire documentation/ du projet, au gate
      - fichier: "001-document-architecture-solution.md"    # page de garde
        sections:
          - "Métadonnées du document"
          - "Historique du document"
          - "Arrimages"
          - "Structure de la documentation"
      - fichier: "01-introduction.md"
        sections:
          - "Contexte"
          - "Périmètre"                        # sous-rubriques : Dans le périmètre / Hors périmètre
          - "Parties prenantes"
      - fichier: "02-objectifs.md"
        sections:
          - "Objectifs de la solution"
          - "Exigences non-fonctionnelles (NFRs)"
          - "Matrice de suivi"                 # traçabilité patrons ↔ piliers ↔ exigences
      - fichier: "06-architecture-solutions.md"
        sections:
          - "Description de l'architecture de solution"
          - "Liste des diagrammes d'architecture"
      - fichier: "08-contraintes.md"
        sections:
          - "Lois et règlementations"
          - "Conformités"
      - fichier: "10-cycle_vie_donnees.md"
        sections:
          - "Gouvernance de données"
          - "Classification des données"
      - fichier: "11-securite.md"
        sections:
          - "Sécurité applicative"
          - "Frontières de confiance"
          - "Sécurité Infrastructure"
          - "Gestion des identités et des accès (GIA)"
    non_vide: true                             # une section présente mais vide (aucun contenu propre) = écart
  securite:                                    # volet architecture de sécurité détaillée — chapitre `architecture-securite/` du répertoire documentation/
    fichiers_mandatory:                        # fichiers du chapitre, où qu'il soit niché sous documentation/ (ex. documentation/architecture-securite/ ou documentation/architecture-detaillee/origin/architecture-securite/)
      - fichier: "architecture-securite/01-surfaces-et-actifs.md"
        sections:
          - "Surfaces d'attaque"
      - fichier: "architecture-securite/02-menaces-stride.md"
        sections:
          - "Matrice de synthèse STRIDE par surface"
      - fichier: "architecture-securite/03-risques-owasp.md"
        sections:
          - "Table de couverture OWASP Top 10"
    non_vide: true
```

## Volet `das:` — fichiers et sections mandatory de la DAS (Option A — manifeste autonome)

Sur le volet `das:`, le sensor vérifie qu'au gate de phase, chacun des **7 fichiers mandatory** de la documentation d'architecture de solution est **présent** dans le répertoire `documentation/` du projet (les fichiers `.md` y sont déposés directement) et **non vide** (contenu propre, gabarit renseigné — les commentaires HTML `<!-- … -->` et les cellules d'exemple ne comptent pas comme contenu). Fichiers et sections retenus par l'humain (multica.gaston, ALI-218) :

| Fichier | Thème | Pourquoi mandatory |
| --- | --- | --- |
| `001-document-architecture-solution.md` | Page de garde, historique, arrimages, structure | Point d'entrée du DAS : sans métadonnées / historique / arrimages, le document n'est pas identifiable ni traçable |
| `01-introduction.md` | Contexte, périmètre, parties prenantes | Sans contexte ni périmètre, l'architecture n'a pas de cadrage vérifiable |
| `02-objectifs.md` | Objectifs, NFRs, matrice de suivi patrons↔piliers | Ancre la traçabilité exigences ↔ patrons ↔ piliers Well-Architected |
| `06-architecture-solutions.md` | Architecture de solution, diagrammes | Cœur du DAS : la solution dans son écosystème |
| `08-contraintes.md` | Lois, conformités, contraintes technologiques | Contraintes réglementaires (Loi 25, normes) structurantes pour l'architecture |
| `10-cycle_vie_donnees.md` | Cycle de vie et classification des données | Gouvernance et classification des données, requises par les contraintes du `08` |
| `11-securite.md` | Sécurité applicative, frontières de confiance, sécurité infrastructure, gestion des identités et des accès | Volet sécurité de conception de la DAS : la section « Frontières de confiance » n'est conforme que si son diagramme est présent et valide |

Les autres fichiers (`03`, `04`, `05`, `07`, `09`, `12`–`15`) restent **recommandés** mais **hors périmètre mandatory** de ce check ; leur absence n'est pas signalée par ce sensor.

## Volet `securite:` — architecture détaillée (chapitre d'architecture de sécurité)

Ce volet porte les **trois sections du chapitre d'architecture de sécurité** qui ne vivent pas dans la DAS : surfaces d'attaque, modélisation STRIDE et modélisation OWASP. Il complète le volet `das:` (dont `11-securite.md` porte les quatre sections de `11-securite.md`) : ensemble, ils forment les **sept sections** de l'**architecture de sécurité détaillée** décomptées par la checklist.

| Fichier du chapitre | Section mandatory | Pourquoi mandatory |
| --- | --- | --- |
| `architecture-securite/01-surfaces-et-actifs.md` | Surfaces d'attaque | Ancre de tout le chapitre : les menaces STRIDE et les fiches OWASP y renvoient par identifiant de surface |
| `architecture-securite/02-menaces-stride.md` | Matrice de synthèse STRIDE par surface | Modélisation des menaces du socle toujours actif, appliquée à chaque surface |
| `architecture-securite/03-risques-owasp.md` | Table de couverture OWASP Top 10 | Couverture du référentiel OWASP du socle toujours actif, risque par risque |

Les fichiers sont attendus dans le **répertoire `architecture-securite/`** du répertoire `documentation/` du projet, **où qu'il soit niché** (par exemple `documentation/architecture-securite/` ou `documentation/architecture-detaillee/<système>/architecture-securite/`) : le contrat porte sur le nom du répertoire et le nom du fichier, pas sur sa profondeur. Un fichier absent, vide ou réduit au contenu du gabarit est un écart.

### Règle de cohérence gabarit ↔ manifeste (matérialisation NEG-004, ADR-0012)

En **Option A**, la liste des fichiers et sections mandatory est portée **en propre par ce manifeste**, indépendamment des gabarits des skills `architecture-solution-gabarits` et `architecture-securite-gabarits` (aucun couplage `core → plugin`). La contrepartie est une **cohérence à maintenir à deux endroits** : toute évolution du découpage ou du titre d'une section dans un gabarit mandatory (`gabarits/001`, `01`, `02`, `06`, `08`, `10`, `11` de la DAS ; `gabarits/01-surfaces-et-actifs`, `02-menaces-stride`, `03-risques-owasp` du chapitre sécurité) **doit être répercutée ici** dans la même PR. Cette synchronisation est une modification de la surface de gouvernance : elle relève de SG-1 / SG-6 (versionnée, tracée, sous contrôle sécurité si elle affaiblit le check).

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

Un **fichier mandatory absent** (répertoire `documentation/` pour la DAS, chapitre `architecture-securite/` pour l'architecture détaillée) est un écart au même titre qu'une section manquante ou vide (SG-2 : l'absence d'un signal attendu est elle-même un écart).

```
Sensor required-sections-architecture — <fichier>   (source : core/sensors/sensors/required-sections-architecture.md @ <commit>)
- verdict : ✅ conforme | ⚠️ fichiers mandatory manquants : <liste> | ⚠️ rubriques manquantes/vides : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : n'empêche pas l'écriture, ne remplace pas la validation humaine ni le contrôle sécurité. Le passage à bloquant est une décision ADR + contrôle sécurité (Architecte cybersécurité).
