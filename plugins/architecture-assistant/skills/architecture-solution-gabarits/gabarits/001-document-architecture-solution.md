# Document d'architecture de solution (DAS)

> Page de garde du document d'architecture de solution. Ce fichier est le point d'entrée de la documentation d'architecture et reste stable : les contenus détaillés vivent dans les fichiers thématiques `01-` à `15-`. Conserver le découpage des fichiers et la structure des sections.

## Métadonnées du document

| Champ                         | Valeur                              |
| ----------------------------- | ----------------------------------- |
| **Titre**                     | Document d'architecture de solution |
| **Version**                   | V1.0                                |
| **Statut**                    | Brouillon / En revue / Approuvé     |
| **Date de la dernière revue** | YYYY-MM-DD                          |
| **Propriétaire**              | Architecte de solution intégrateur  |
| **Approbateur**               | Responsable produit / Client        |
| **Dossier**                   | `documentation/`                    |

**Tableau 1. Métadonnées du document**

## Historique du document

> Mettre à jour cet historique à **chaque** modification de la documentation. La version la plus récente figure en première ligne.

| **Version** | **Date**   | **Statut** | **Description / Motif du changement** | **Auteurs**                                 | **Approbateur**            |
| ----------- | ---------- | ---------- | ------------------------------------- | ------------------------------------------- | -------------------------- |
| V1.0        | YYYY-MM-DD | Approuvé   | Version initiale                      | Nom de l'Architecte de Solution Intégrateur | Nom du Responsable produit |

**Tableau 2. Historique des modifications**

> **Règle de versionnement** : incrément mineur (ex. V1.1) pour toute modification ; incrément majeur (ex. V2.0) pour tout changement structurel ou toute décision d'architecture majeure (tracée dans un ADR).

## Arrimages

> Répartition des responsabilités selon la matrice RACI :
> **R** = Réalise · **A** = Approuve · **C** = Consulté · **I** = Informé.
> L'architecte de solution intégrateur assure la cohérence globale de l'ensemble des fichiers.

| Rôles                              | Nom | Implication (R/A/C/I) | Documents concernés          |
| ---------------------------------- | --- | --------------------- | ---------------------------- |
| Architecte de solution intégrateur |     | R                     | DAS complet, arrimage global |
| Architecte de solution             |     | R / C                 | Thématiques `01` à `15`      |
| Architecte logiciel                |     | C                     | `06`, `09`, `14`             |
| Architecte de données              |     | C                     | `10`, `13`                   |
| Architecte de sécurité             |     | C                     | `08`, `11`, `15`             |
| Architecte DevOps / Infrastructure |     | C                     | `05`, `09`, `13`, `15`       |
| Chef de projet                     |     | C / I                 | `05`, `09`                   |
| Responsable produit                |     | A                     | DAS complet                  |
| Analyste fonctionnel               |     | C                     | `01`, `02`, `03`             |
| Responsable Affaires               |     | C / A                 | `02`, `03`, `10`             |
| Responsable Légal                  |     | C                     | `08`, `10`                   |
| Lead Assurance Qualité             |     | C / R                 | `14`                         |

**Tableau 3. Arrimage des rôles**

## Lexique

> Le lexique est la source de vérité de la terminologie utilisée dans l'ensemble des fichiers de documentation. Toute nouvelle définition doit y être ajoutée et tout terme employé dans un fichier doit être cohérent avec cette liste.

| **Terme ou acronyme** | **Définitions**                                                            |
| --------------------- | -------------------------------------------------------------------------- |
| DAS                   | Document d'architecture de solution                                        |
| ADR                   | Architecture Decision Record – enregistrement de décision d'architecture   |
| CI/CD                 | Intégration Continue / Déploiement Continu                                 |
| PR                    | Pull Request                                                               |
| MR                    | Merge Request – Demande de fusion de code source                           |
| IaC                   | Infrastructure as Code                                                     |
| NFR                   | Exigence non-fonctionnelle (performance, sécurité, fiabilité, etc.)        |
| WAF                   | Well-Architected Framework                                                 |
| RTO                   | Recovery Time Objective – objectif de temps de reprise après sinistre      |
| RPO                   | Recovery Point Objective – point de reprise maximal acceptable des données |
| SLA / SLO / SLI       | Accord / Objectif / Indicateur de niveau de service                        |
| PoLP                  | Principe du moindre privilège (Principle of Least Privilege)               |
| UC                    | Cas d'utilisation                                                          |
| WBS                   | Work Breakdown Structure – structure de découpage du projet                |
| DPD                   | Délégué à la protection des données                                        |

**Tableau 4. Lexique**

## Références documentaires

> Distinguer les références **internes** (produites dans le projet) des références **externes** (gabarits, normes, standards, autres projets). Les décisions d'architecture (ADR) sont indexées séparément.

| Réf    | Version | Date       | Description du document                     | Type (interne/externe) | Lien                                                                                                                                                                                                                                                                         |
| ------ | ------- | ---------- | ------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| REF-01 | V1.3    | 2024-05-01 | Estimé de projet - WBS                      | Interne                | [V1.3 - WBS - Estimé de projet.xlsx](https://grist.jeedom-gaston.ovh/o/pratiques/xr2qHq5wps9K/WBS-Template?utm_id=share-doc)                                                                                                                                                 |
| REF-02 | V1.0    | 2024-05-01 | Présentation d'architecture de solution     | Externe                | [Présentation globale.pptx](https://alithyaca.sharepoint.com/:p:/r/sites/msteams_3ce4e1_985940-Projets/Shared%20Documents/Projets/Gabarits/Pr%C3%A9sentation/Pr%C3%A9sentation%20globale.pptx?d=w9ae1ac719ded490eb5f8a79a34144117&csf=1&web=1&e=rj6yVw)                      |
| REF-03 | V1.0    | 2023-06-07 | Fiche de défaut d'architecture              | Externe                | [Fiche de défaut d'architecture.docx](https://alithyaca.sharepoint.com/:w:/r/sites/msteams_3ce4e1_985940-Projets/Shared%20Documents/Projets/Gabarits/Architecture/Fiche%20de%20d%C3%A9faut%20d%27architecture.docx?d=w4e6232fc487f4192b2e82f0f8bc8fb4b&csf=1&web=1&e=cVmxwn) |
| REF-04 | —       | —          | Registre des décisions d'architecture (ADR) | Interne                | À référencer                                                                                                                                                                                                                                                                 |

**Tableau 5. Références documentaires**

## Structure de la documentation

> La documentation d'architecture de solution est découpée en fichiers Markdown distincts, un par thème. **Chaque thème est traité dans le même fichier** : les modifications se font toujours en lisant, analysant puis modifiant les fichiers existants, jamais en recréant ou restructurant le découpage.

| Fichier                                 | Thème                                                                                                                        |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `001-document-architecture-solution.md` | Page de garde, historique, arrimages, lexique, références, index                                                             |
| `01-introduction.md`                    | Contexte, vision, périmètre, parties prenantes, hypothèses                                                                   |
| `02-objectifs.md`                       | Objectifs, piliers Well-Architected (Azure et AWS), matrice de suivi, critères de qualification                              |
| `03-besoins_affaires_exigences.md`      | Processus d'affaires, cas d'utilisation, critères d'acceptation                                                              |
| `04-risques.md`                         | Analyse des risques                                                                                                          |
| `05-planification.md`                   | Planification, efforts, coûts                                                                                                |
| `06-architecture-solutions.md`          | Architectures de solution, diagrammes, acteurs, systèmes, défauts d'architecture                                             |
| `07-choix-des-solutions.md`             | Solutions étudiées et choix                                                                                                  |
| `08-contraintes.md`                     | Lois, conformités, contraintes technologiques                                                                                |
| `09-deploiement.md`                     | Implantation, environnement, déploiement, DevSecOps                                                                          |
| `10-cycle_vie_donnees.md`               | Cycle de vie des données                                                                                                     |
| `11-securite.md`                        | Sécurité                                                                                                                     |
| `12-volumetries.md`                     | Volumétrie                                                                                                                   |
| `13-plan-qualite.md`                    | Plan de qualité                                                                                                              |
| `14-preventions-et-resilience.md`       | Prévention, reprise après sinistre, résilience                                                                               |
| `15-concepts-transverses.md`            | Concepts transverses (communication, erreurs, transactions, cache, persistance, observabilité, configuration, accessibilité) |

**Tableau 6. Structure de la documentation**

## Liste des images et diagrammes

> Index des diagrammes de la documentation avec le fichier et la section où ils se trouvent. À maintenir à chaque ajout ou modification d'un diagramme. Les diagrammes sont générés en code (PlantUML, Mermaid, Structurizr, BPMN, C4) et référencés ici.

| Fichier                        | Section                           | Diagramme                 | Description                       |
| ------------------------------ | --------------------------------- | ------------------------- | --------------------------------- |
| `01-introduction.md`           | Contexte                          | Diagramme de contexte     | Vue d'ensemble du contexte        |
| `04-risques.md`                | Tableau récapitulatif des risques | Récapitulatif des risques | Vue synthétique des risques       |
| `04-risques.md`                | Matrice de risques                | Matrice des risques       | Probabilité × impact              |
| `05-planification.md`          | Planification des tâches          | WBS                       | Livrables du projet               |
| `05-planification.md`          | Feuille de route                  | Timeline                  | Jalons et livraisons              |
| `06-architecture-solutions.md` | Diagramme système                 | Landscape                 | Éco-système global de la solution |
| `06-architecture-solutions.md` | Diagrammes de contexte            | Context                   | Contexte des systèmes logiciels   |
| `09-deploiement.md`            | Implantation de la solution       | Implantation              | Environnement de la solution      |
| `09-deploiement.md`            | Répartition des zones réseaux     | Réseau                    | Zones et flux réseau              |

**Tableau 7. Index des diagrammes**

## Liste des tableaux du document

> Index des tableaux de la documentation, groupé par fichier. **Numérotation globale et continue** : à maintenir à chaque ajout ou suppression d'un tableau.

| Fichier | Section                                           | N° tableau | Description                                       |
| ------- | ------------------------------------------------- | ---------- | ------------------------------------------------- |
| `001`   | Métadonnées du document                           | 1          | Métadonnées du document                           |
| `001`   | Historique du document                            | 2          | Historique des modifications                      |
| `001`   | Arrimages                                         | 3          | Arrimage des rôles (RACI)                         |
| `001`   | Lexique                                           | 4          | Lexique                                           |
| `001`   | Références documentaires                          | 5          | Références documentaires                          |
| `001`   | Structure de la documentation                     | 6          | Structure de la documentation                     |
| `001`   | Liste des images et diagrammes                    | 7          | Index des diagrammes                              |
| `001`   | Liste des tableaux du document                    | 8          | Index des tableaux                                |
| `01`    | Parties prenantes                                 | 9          | Parties prenantes                                 |
| `01`    | Hypothèses                                        | 10         | Hypothèses                                        |
| `02`    | Objectifs                                         | 11         | Objectifs d'affaires et d'architecture            |
| `02`    | Exigences non-fonctionnelles (NFRs)               | 12         | Exigences non-fonctionnelles                      |
| `02`    | Matrice de suivi                                  | 13         | Matrice Well-Architected (Azure et AWS)           |
| `02`    | Critères de qualification                         | 14         | Critères de qualification                         |
| `03`    | Liste des processus de la solution                | 15         | Liste des processus d'affaires                    |
| `03`    | Liste des cas d'utilisation                       | 16         | Liste des cas d'utilisation                       |
| `03`    | Cas d'utilisation (UC-001)                        | 17         | Détail du cas d'utilisation                       |
| `05`    | Récapitulatif des efforts                         | 18         | Efforts par rôle (estimation en trois points)     |
| `05`    | Efforts de développement                          | 19         | Efforts de développement (écart type)             |
| `05`    | Estimation des coûts                              | 20         | Estimation des coûts du projet                    |
| `06`    | Liste des diagrammes d'architecture               | 21         | Liste des diagrammes                              |
| `06`    | Liste des acteurs                                 | 22         | Liste des acteurs                                 |
| `06`    | Liste des systèmes                                | 23         | Liste des systèmes applicatifs                    |
| `06`    | Défauts d'architecture                            | 24         | Liste des défauts d'architecture                  |
| `06`    | Défaut d'architecture (DEF-001)                   | 25         | Détail du défaut d'architecture                   |
| `07`    | Récapitulatif des solutions étudiées              | 26         | Solutions recommandées                            |
| `07`    | Matrice de décision pondérée                      | 27         | Matrice de décision pondérée                      |
| `07`    | Comparaison des coûts                             | 28         | Comparaison des coûts                             |
| `07`    | Décision formelle                                 | 29         | Décision formelle (ADR)                           |
| `07`    | Solution recommandée (SOL-001)                    | 30         | Avantages et limitations                          |
| `07`    | Solution alternative 1 (SOL-002)                  | 31         | Avantages et limitations                          |
| `07`    | Solution alternative 2 (SOL-003)                  | 32         | Avantages et limitations                          |
| `08`    | Lois et règlementations                           | 33         | Lois et réglementations                           |
| `08`    | Référentiels et normes                            | 34         | Référentiels et normes                            |
| `08`    | Conformités                                       | 35         | Contraintes de conformité                         |
| `08`    | Persistance des données                           | 36         | Contraintes technologiques                        |
| `08`    | Portabilité                                       | 37         | Contraintes technologiques                        |
| `08`    | Contraintes serveur                               | 38         | Contraintes technologiques                        |
| `08`    | Contraintes clients                               | 39         | Contraintes technologiques                        |
| `08`    | Intégration / interopérabilité                    | 40         | Contraintes technologiques                        |
| `08`    | Licences / obsolescence                           | 41         | Contraintes technologiques                        |
| `08`    | Performance                                       | 42         | Contraintes technologiques                        |
| `08`    | Accessibilité                                     | 43         | Contraintes technologiques                        |
| `09`    | Implantation du système                           | 44         | Liste des systèmes infrastructure                 |
| `09`    | Coûts récurrents (licences et hébergement)        | 45         | Coûts récurrents – source de vérité               |
| `09`    | Environnements                                    | 46         | Environnements (dev/QA/staging/prod)              |
| `09`    | Chaîne CI/CD                                      | 47         | Portes de validation (gates) DevSecOps            |
| `10`    | Inventaire / référentiel des données              | 48         | Inventaire des données                            |
| `10`    | Gestion du consentement                           | 49         | Registre des consentements                        |
| `10`    | Classification des données                        | 50         | Classification des données                        |
| `10`    | Règles de conservation des données                | 51         | Règles de conservation                            |
| `10`    | Règles d'épuration des données                    | 52         | Règles d'épuration                                |
| `10`    | Règles d'archivage des données                    | 53         | Règles d'archivage                                |
| `10`    | Modèle d'information                              | 54         | Entités du modèle d'information                   |
| `06`    | Registre des interfaces externes / contrats d'API | 26         | Registre des interfaces externes / contrats d'API |
| `06`    | Matrice de satisfaction exigences → composants/vues | 73       | Matrice de satisfaction exigences → composants/vues |
| `06`    | Traçabilité inverse — composant → exigences satisfaites | 74    | Traçabilité inverse (composant → exigences)         |
| `11`    | Sécurité applicative                              | 56         | Vulnérabilités applicatives                       |
| `11`    | Sécurité Infrastructure                           | 57         | Vulnérabilités Infrastructure                     |
| `11`    | Gestion des identités et des accès                | 58         | Types d'accès – GIA                               |
| `12`    | Volumétrie d'affaires                             | 59         | Volumétrie d'affaires                             |
| `12`    | Volumétrie des données                            | 60         | Volumétrie des données                            |
| `12`    | Volumétrie infrastructure                         | 61         | Volumétrie infrastructure                         |
| `12`    | Volumétries applicatives                          | 62         | Volumétrie applicatives                           |
| `13`    | Pyramide de tests                                 | 63         | Pyramide de tests (couverture, outils, gates)     |
| `13`    | Test à la charge du développeur                   | 64         | Test de développement                             |
| `13`    | Plan assurance qualité                            | 65         | Plan d'assurance qualité                          |
| `13`    | Tests non-fonctionnels                            | 66         | Tests performance, sécurité, résilience           |
| `13`    | Environnements et données de test                 | 67         | Masquage / anonymisation                          |
| `13`    | Traçabilité exigences / UC → tests                | 68         | Traçabilité exigences / cas d'utilisation         |
| `14`    | Criticité par système / processus                 | 69         | Criticité (RTO/RPO)                               |
| `14`    | Indicateurs clés                                  | 70         | RTOs et RPOs                                      |
| `14`    | Niveau de services                                | 71         | SLO – objectifs de niveau de service              |
| `15`    | Concepts transverses                              | 72         | Concepts transverses                              |

**Tableau 8. Index des tableaux**

### Mappage préoccupations → vues (ISO 42010)

> Cette section établit la correspondance entre les préoccupations des parties prenantes (identifiées dans `01-introduction.md`) et les **vues** et **viewpoints** de l'architecture (référencés dans les gabarits `06-architecture-solutions.md`, `11-securite.md`, etc.), permettant la traçabilité bidirectionnelle exigences ↔ vues.

| Préoccupation | Vue/Viewpoint | Fichier gabarit | Description |
| ------------- | ------------- | --------------- | ----------- |
| ...           | ...           | ...             | ...         |

**Tableau 9. Mappage préoccupations → vues**