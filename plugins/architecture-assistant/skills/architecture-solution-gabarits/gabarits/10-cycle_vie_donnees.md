## Cycle de vie des données

<!-- 
Cette section décrit le **cycle de vie des données** de la solution, de leur **intégration** jusqu'à leur **archivage/épuration**, en cohérence avec les objectifs et exigences du `02-objectifs.md` et du `03-besoins_affaires_exigences.md`.
Elle décline les contraintes du `08-contraintes.md` (Loi 25, normes `NOR-001`…`NOR-004`) pour les données, et vérifie la **couverture d'un patron** du répertoire `patron-architecture/`. Chaque donnée classée est identifiée (`DON-001`, `DON-002`, …).
-->
### Gouvernance de données

<!-- Décrire les mécanismes de gouvernance des données de la solution : propriétaires des données (définis avec le secteur d'affaires client), registre des données, lignes directrices de gestion. -->

#### Inventaire / référentiel des données

<!-- Inventaire des données de la solution : il **alimente la classification** (section suivante) et se **relie à `12-volumetries.md`** pour les volumes. Rédigé avec le secteur d'affaires client et les architectes de données. -->

| ID      | Entité / donnée                          | Système source | Format | Volume (estimé) | Alimente (classification) |
| ------- | ---------------------------------------- | -------------- | ------ | --------------- | ------------------------- |
| DON-000 | A définir durant la conception détaillée |                |        | (voir `13`)     | DON-001, …                |

**Tableau 49. Inventaire / référentiel des données**

#### Intégration des données

<!-- 
Cette section décrit l'ensemble des aspects permettant l'intégration des données au travers de l'ensemble de la solution.
La solution utilise un Data Warehouse ? Data Fabric ? Data Lake ? etc.
La solution nécessite des fonctions de caching de données ? de réplication de données ? d'ETL/ELT ?
La solution nécessite des fonctions d'IA, de traitement massif de données en parallèle ? etc.
Préciser les mécanismes d'intégration (API, files d'attente, événements) et l'outillage, en arrimage avec le patron d'intégration choisi (ex. Transactional Outbox/Inbox).
-->
#### Virtualisation des données

<!-- Cette section doit être remplie si les données sont virtualisées/regroupées de façon logique au sein de la solution/organisation (ex. vue virtuelle, data mesh, lakehouse). -->

#### Traçabilité des données

<!-- 
Cette section doit être remplie si un mécanisme de traçabilité des données est mis en place ainsi que les données tracées — requis par la Loi 25 (registre des incidents) et la norme `NOR-001`.
Décrire le **data lineage** (provenance et transformations d'une donnée) et le **registre des traitements** (finalités, responsables, accès), ainsi que la journalisation d'audit.
-->
#### Sécurisation des données

<!--
Cette section décrit comment les données sont sécurisées afin d'assurer la durabilité (chiffrement au repos et en transit, contrôles d'accès, moindre privilège — en lien avec `11-securite.md`).
Ex. : réplication de données, sauvegarde, Data Sharding, etc.
-->
### Gestion du consentement sur l'utilisation des données

<!--
Cette section décrit les moyens utilisés pour la gestion du consentement de la capture et l'utilisation des données.
En arrimage avec l'obligation de **consentement** de la Loi 25 (déclinée au `08-contraintes.md`). Pour chaque traitement, préciser les **Finalités**, la **Base légale**, la **Durée**, les moyens de **Révocation** et le **Registre des consentements** (horodatage, version de la politique, traçabilité de l'exercice des droits).
-->
| ID      | Traitement / données                     | Finalités | Base légale (Loi 25) | Durée | Révocation | Registre des consentements |
| ------- | ---------------------------------------- | --------- | -------------------- | ----- | ---------- | -------------------------- |
| CON-001 | A définir durant la conception détaillée |           |                      |       |            |                            |

**Tableau 50. Gestion du consentement sur l'utilisation des données**

### Classification des données

<!--
Cette section décrit l'ensemble des données ayant un caractère important (restreint, confidentiel, secret, etc.).
La classification des données est un élément clé du dossier. Elle permet de s'assurer que l'ensemble des normes, lois et réglementations sont connues et ont été prises en compte.
**La classification est définie par le responsable du projet côté client.**
La colonne **Taxonomie** s'aligne sur la taxonomie d'entreprise : **public / interne / confidentiel / secret**. Chaque donnée est identifiée (`DON-001`, …), porte un **Propriétaire de la donnée** et un **Responsable de la protection** (DPD / délégué), et sa contrainte peut référencer une norme du `08-contraintes.md` (ex. `NOR-002` PIPEDA).
-->
| ID      | Nom                                      | Description | Taxonomie (public/interne/confidentiel/secret) | Renseignement personnel | Confidentialité | Propriétaire de la donnée | Responsable protection | Contrainte |
| ------- | ---------------------------------------- | ----------- | ---------------------------------------------- | ----------------------- | --------------- | ------------------------- | ---------------------- | ---------- |
| DON-001 | A définir durant la conception détaillée |             |                                                |                         |                 |                           |                        |            |

**Tableau 51. Classification des données**

### Règles de conservation des données

<!--
Cette section décrit l'ensemble des règles de conservation des données. Elle permet de s'assurer que l'ensemble des règles sont connues et ont été prises en compte.
**Les règles de conservation sont définies par le secteur d'affaires du client.**
Toute règle de conservation doit être cohérente avec la durée de vie des données classées ci-dessus (`DON-001`, …) et avec les exigences du `02-objectifs.md`. Le **Type de donnée** doit correspondre à celui des tableaux d'épuration et d'archivage (vocabulaire commun).
-->
| ID      | Type de donnée                           | Type de règle (Légale, Affaire) | Durée de conservation | Responsable | Conformité (Loi 25 / `NOR-xxx`) |
| ------- | ---------------------------------------- | ------------------------------- | --------------------- | ----------- | ------------------------------- |
| CON-002 | A définir durant la conception détaillée |                                 |                       |             |                                 |

**Tableau 52. Règles de conservation des données**

### Règles d'épuration des données

<!-- 
Cette section décrit l'ensemble des règles d'épuration des données. Les règles d'épuration peuvent avoir un caractère légal ou réglementaire (ex. **Loi 25**).
Cette section permet de s'assurer que l'ensemble des normes, lois et réglementations ont été prises en compte.
**Les règles sont définies par le responsable du projet côté client.** Le **Type de donnée** doit correspondre à celui des tableaux de conservation et d'archivage.
-->
| ID      | Type de donnée                           | Type de règle | Délai d'épuration | Mode d'épuration | Responsable | Conformité (Loi 25 / `NOR-xxx`) |
| ------- | ---------------------------------------- | ------------- | ----------------- | ---------------- | ----------- | ------------------------------- |
| EPU-001 | A définir durant la conception détaillée |               |                   |                  |             |                                 |

**Tableau 53. Règles d'épuration des données**

### Règles d'archivage des données

<!-- 
Cette section décrit l'ensemble des règles d'archivage des données. Elle permet de s'assurer que l'ensemble des règles sont connues et ont été prises en compte.
**Les règles de conservation sont définies par le secteur d'affaires du client.** Le **Type de donnée** doit correspondre à celui des tableaux de conservation et d'épuration.
Préciser les **exigences techniques d'archivage** : stockage **WORM** (write once, read many), **immutabilité**, chiffrement, rétention légale, cohérence avec `12-volumetries.md`.
-->
| ID      | Type de donnée                           | Règles d'archivage | Type d'archivage | Délai d'archivage | Délai conservation des archives | Responsable | Conformité (Loi 25 / `NOR-xxx`) | Exigences techniques (WORM, immuabilité) |
| ------- | ---------------------------------------- | ------------------ | ---------------- | ----------------- | ------------------------------- | ----------- | ------------------------------- | ---------------------------------------- |
| ARC-001 | A définir durant la conception détaillée |                    |                  |                   |                                 |             |                                 |                                          |

**Tableau 54. Règles d'archivage des données**

### Modèle d'information de la solution

<!-- 
Cette section décrit le **modèle d'information de la solution** à haut niveau : les entités métier clés (`ENT-001`, …), leurs relations et les flux de données entre entités et systèmes. Elle se relie au **cycle de vie des données** (`DON-xxx` : classification, conservation, épuration, archivage), aux **volumétries** (`12-volumetries.md`) et aux modèles de données détaillés (`architecture-detaillee/<software_system>/0006-database.md`).
-->
![Diagramme du modèle d'information](embed:information_model)

| ID      | Entité                                   | Description | Relations principales | Propriétaire / responsable | Données associées (`DON-xxx`) | Système(s) (`SYS-xxx`) |
| ------- | ---------------------------------------- | ----------- | --------------------- | -------------------------- | ----------------------------- | ---------------------- |
| ENT-001 | A définir durant la conception détaillée |             |                       |                            |                               |                        |

**Tableau 55. Entités du modèle d'information**

<!-- Décrire les **flux de données** entre entités et systèmes (origine, destination, transformation) — à arrimer avec la vue d'exécution du `06-architecture-solutions.md` et la traçabilité des données du `10`. -->
