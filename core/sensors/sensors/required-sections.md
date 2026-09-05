---
id: required-sections
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
description: "Vérifie que les rubriques obligatoires de l'ADR et les fichiers/sections mandatory de la DAS sont présents et non vides."
category: document-shape
fire_on: gate
matches: "{decisions/[0-9][0-9][0-9][0-9]-*.md,documentations/**/*.md}"
origine: ALI-188 (durcissement volet DAS : ALI-218)
---

# Sensor `required-sections` — sections requises *(prioritaire)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie que les **rubriques obligatoires** du gabarit sont présentes et non vides sur chaque **ADR** ou **DAS** livré. **Advisory** (`default_severity: advisory`).

## Contrat de vérification (`checks`)

```yaml
checks:
  adr:                                         # rubriques dérivées du gabarit de la skill create-architecture-decision-record
    entete_meta: [auteurs, "accepté par", "accepté le", supersedes, superseded_by]
    sections:
      - Status                 # titre en anglais (compat Structurizr), statut unique retenu
      - Contexte
      - Décision
      - "Conséquences"        # sous-rubriques obligatoires : Positives / Négatives
      - "Alternatives étudiées"
      - "Notes d'implémentation"
      - "Références"
    non_vide: true
  das:                                         # fichiers DAS mandatory portés en propre (Option A, ADR-0025) — indépendants des gabarits (ADR-0012, NEG-004)
    fichiers_mandatory:                        # présents ET non vides dans documentations/<projet>/ au gate
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
          - "Modélisation des menaces (STRIDE)"
          - "Sécurité applicative"
    non_vide: true                             # une section présente mais vide (aucun contenu propre) = écart
```

## Sections mandatory de la DAS (Option A — manifeste autonome)

Sur le volet `das:`, le sensor vérifie qu'au gate de phase, chacun des **7 fichiers mandatory** de la documentation d'architecture de solution est **présent** dans `documentations/<projet>/` et **non vide** (contenu propre, gabarit renseigné — les commentaires HTML `<!-- … -->` et les cellules d'exemple ne comptent pas comme contenu). Fichiers et sections retenus par l'humain (multica.gaston, ALI-218) :

| Fichier | Thème | Pourquoi mandatory |
| --- | --- | --- |
| `001-document-architecture-solution.md` | Page de garde, historique, arrimages, structure | Point d'entrée du DAS : sans métadonnées / historique / arrimages, le document n'est pas identifiable ni traçable |
| `01-introduction.md` | Contexte, périmètre, parties prenantes | Sans contexte ni périmètre, l'architecture n'a pas de cadrage vérifiable |
| `02-objectifs.md` | Objectifs, NFRs, matrice de suivi patrons↔piliers | Ancre la traçabilité exigences ↔ patrons ↔ piliers Well-Architected |
| `06-architecture-solutions.md` | Architecture de solution, diagrammes | Cœur du DAS : la solution dans son écosystème |
| `08-contraintes.md` | Lois, conformités, contraintes technologiques | Contraintes réglementaires (Loi 25, normes) structurantes pour l'architecture |
| `10-cycle_vie_donnees.md` | Cycle de vie et classification des données | Gouvernance et classification des données, requises par les contraintes du `08` |
| `11-securite.md` | Modélisation des menaces, sécurité applicative | Volet sécurité de conception (STRIDE / OWASP), plancher de gouvernance |

Les autres fichiers (`03`, `04`, `05`, `07`, `09`, `12`–`15`) restent **recommandés** mais **hors périmètre mandatory** de ce check ; leur absence n'est pas signalée par ce sensor.

### Règle de cohérence gabarit ↔ manifeste (matérialisation NEG-004, ADR-0012)

En **Option A**, la liste des fichiers et sections mandatory est portée **en propre par ce manifeste**, indépendamment des gabarits de la skill `architecture-solution-gabarits` (aucun couplage `core → plugin`). La contrepartie est une **cohérence à maintenir à deux endroits** : toute évolution du découpage ou du titre d'une section dans un gabarit mandatory (`gabarits/001`, `01`, `02`, `06`, `08`, `10`, `11`) **doit être répercutée ici** dans la même PR. Cette synchronisation est une modification de la surface de gouvernance : elle relève de SG-1 / SG-6 (versionnée, tracée, sous contrôle sécurité si elle affaiblit le check).

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

Sur le volet DAS, un **fichier mandatory absent** du répertoire `documentations/<projet>/` est un écart au même titre qu'une section manquante ou vide (SG-2 : l'absence d'un signal attendu est elle-même un écart).

```
Sensor required-sections — <fichier>   (source : core/sensors/sensors/required-sections.md @ <commit>)
- verdict : ✅ conforme | ⚠️ fichiers mandatory manquants : <liste> | ⚠️ rubriques manquantes/vides : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : n'empêche pas l'écriture, ne remplace pas la validation humaine ni le contrôle sécurité. Le passage à bloquant est une décision ADR + contrôle sécurité (Architecte cybersécurité).
