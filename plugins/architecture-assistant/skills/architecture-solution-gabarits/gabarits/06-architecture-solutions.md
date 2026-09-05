## Architectures de solution

<!-- 
Cette section décrit **l'architecture de solution** : la solution dans son écosystème global (systèmes logiciels, acteurs, systèmes externes, intégrations), **à haut niveau**.
**L'architecture logicielle** de chaque système logiciel est documentée **séparément** dans `architecture-detaillee/<software_system>/` (un document d'architecture détaillée par système logiciel : composants, données, infrastructure, sécurité, défauts).
Les diagrammes de cette section restent **à haut niveau** ; les diagrammes détaillés (composants, séquences, données, déploiement) sont **ajoutés à la demande** dans les documents d'architecture détaillée. Chaque décision d'architecture est tracée dans un ADR et chaque patron retenu est référencé dans la matrice de suivi du `02-objectifs.md`.
-->

### Description de l'architecture de solution

<!-- Décrire, à haut niveau, la solution : les systèmes logiciels qui la composent, les systèmes externes en interaction, les principaux échanges (flux) entre eux et le contexte d'exploitation. Cette description alimente le diagramme système (landscape). -->

### Liste des diagrammes d'architecture

<!-- Les diagrammes de cette section sont **à haut niveau** (écosystème, contexte des systèmes logiciels). Les diagrammes détaillés sont ajoutés **à la demande** dans les documents d'architecture détaillée (`architecture-detaillee/<software_system>/`) et référencés ici. -->

| ID      | Type                          | Niveau | Description                                                          |
| ------- | ----------------------------- | ------ | -------------------------------------------------------------------- |
| DIA-001 | Diagramme système (Landscape) | Élevé  | Diagramme représentant l'ensemble de l'éco-système global            |
| DIA-002 | Diagramme de contexte         | Élevé  | Contexte du Software System 1 (SYS-001) et ses interactions directes |
| DIA-003 | Diagramme de contexte         | Élevé  | Contexte du Software System 2 (SYS-002) et ses interactions directes |
| DIA-004 | Diagramme de séquence         | Élevé  | Séquence du scénario d'exécution SC-001                              |
| DIA-005 | Diagramme de séquence         | Élevé  | Séquence du scénario d'exécution SC-002                              |

**Tableau 21. Liste des diagrammes d'architecture**

### Diagramme système (DIA-001)

#### Description

<!-- Décrire la solution dans son écosystème global, à haut niveau. -->

#### Diagramme

![Diagramme du système](embed:landscape)

#### Liste des acteurs

| ID      | Nom de l'acteur | Description                            |
| ------- | --------------- | -------------------------------------- |
| ACT-001 | Utilisateurs    | Représente l'ensemble des utilisateurs |

**Tableau 22. Liste des acteurs**

#### Liste des systèmes

<!-- Un système logiciel par ligne. Le document d'architecture détaillée de chaque système est référencé dans la dernière colonne. -->

| ID      | Nom du système             | Description                         | Architecture détaillée                                                              |
| ------- | -------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------- |
| SYS-001 | Application 1              | Système logiciel permettant         | `architecture-detaillee/software_system_1/0000-document-architecture-detatillee.md` |
| SYS-002 | Application 2              | Système logiciel                    | `architecture-detaillee/software_system_2/0000-document-architecture-detatillee.md` |
| SYS-003 | Active Directory - Alithya | Gestionnaire d'identités et d'accès | —                                                                                   |

**Tableau 23. Liste des systèmes applicatifs**

### Software System 1 (SYS-001) — Diagramme de contexte (DIA-002)

#### Description — Software System 1 (SYS-001)

<!-- Décrire le contexte du système logiciel 1 et ses entités en interactions directes (niveau élevé). -->

#### Diagramme — Software System 1 (SYS-001)

![Diagramme de contexte](embed:Context_1)

#### Architecture détaillée — Software System 1 (SYS-001)

<!-- 
Les composants, le modèle de données, l'infrastructure et la sécurité du Software System 1 sont documentés dans `architecture-detaillee/software_system_1/` (introduction `0001-introduction.md`, composants `0005-composants.md`, base de données `0006-database.md`, infrastructure `0007-infrastructure.md`, sécurité `0008-securite.md`). Les diagrammes détaillés sont ajoutés à la demande dans ces documents.
-->

### Software System 2 (SYS-002) — Diagramme de contexte (DIA-003)

#### Description — Software System 2 (SYS-002)

<!-- Décrire le contexte du système logiciel 2 et ses entités en interactions directes (niveau élevé). -->

#### Diagramme — Software System 2 (SYS-002)

![Diagramme de contexte](embed:Context_2)

#### Architecture détaillée — Software System 2 (SYS-002)

<!-- 
Les composants, le modèle de données, l'infrastructure et la sécurité du Software System 2 sont documentés dans `architecture-detaillee/software_system_2/` (introduction `0001-introduction.md`, composants `0005-composants.md`, base de données `0006-database.md`, infrastructure `0007-infrastructure.md`, sécurité `0008-securite.md`). Les diagrammes détaillés sont ajoutés à la demande dans ces documents.
-->

### Scénarios d'exécution (Runtime View)

<!-- 
Décrire les **scénarios d'exécution critiques** de la solution : comment les systèmes logiciels, les acteurs et les systèmes externes interagissent à l'exécution pour produire les principaux comportements attendus. Cette vue correspond au Runtime View (arc42 §6) au niveau solution ; les séquences détaillées au niveau composants sont ajoutées à la demande dans `architecture-detaillee/<software_system>/`.

- SC-001 — <Nom du scénario 1 : <description de l'enchaînement à l'exécution, acteurs et systèmes impliqués>
- SC-002 — <Nom du scénario 2 : <description de l'enchaînement à l'exécution, acteurs et systèmes impliqués>
-->

#### Scénario d'exécution — <Nom du scénario 1<!-- (SC-001)

<!-- Décrire : déclencheur, acteurs et systèmes impliqués, principales étapes à l'exécution, données échangées, traitements en arrière-plan (le cas échéant). -->

![Diagramme de séquence — SC-001](embed:sequence_SC-001)

#### Scénario d'exécution — <Nom du scénario 2<!-- (SC-002)

<!-- Décrire : déclencheur, acteurs et systèmes impliqués, principales étapes à l'exécution, données échangées, traitements en arrière-plan (le cas échéant). -->

![Diagramme de séquence — SC-002](embed:sequence_SC-002)

<!-- Lier chaque scénario aux **patrons d'intégration** utilisés (ex. Transactional Outbox/Inbox pour les événements d'intégration, publish/subscribe) et à la **matrice de suivi** du `02-objectifs.md` (patron retenu ↔ exigence/pilier). -->

### Défauts d'architecture

<!-- Faire la liste des **défauts d'architecture de la solution** (niveau solution). Les défauts logiciels (détaillés) sont documentés dans `architecture-detaillee/<software_system>/0010-defaut-architecture.md`. -->

| ID      | Liste des défauts | Description |
| ------- | ----------------- | ----------- |
| DEF-001 |                   | Description |

**Tableau 24. Liste des défauts d'architecture**

#### DEF-001

| DEF-001            |                                                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Description        | Décrire les détails techniques du défaut, en précisant les parties concernées et les impacts sur les fonctionnalités      |
| Impacts potentiels | Décrire l'impact potentiel du défaut (ex. erreurs d'exécution, dysfonctionnements, comportements inattendus)              |
| Probabilité        | Évaluer la probabilité de reproduction du défaut (faible à élevée)                                                        |
| Gravité            | Évaluer la gravité du défaut (faible à élevée)                                                                            |
| Causes             | Décrire les causes potentielles du défaut (ex. erreur de conception, de codage, conflit de version)                       |
| Recommandations    | Recommander les actions à entreprendre, les délais à respecter et les facteurs permettant de reproduire le défaut         |
| Responsabilités    | Indiquer les personnes ou équipes responsables de la résolution et de la mise en œuvre des recommandations                |
| Date limite        | Indiquer la date limite pour la résolution ou la mise en œuvre des recommandations                                        |
| Suivi              | Indiquer les mesures de suivi pour s'assurer que le défaut a été résolu ou que les recommandations ont été mises en œuvre |

**Tableau 25. Détail du défaut d'architecture (DEF-001)**

### Registre des interfaces externes / contrats d'API

<!-- 
Cette section décrit le **registre des interfaces externes et des contrats d'API** de la solution (REST, SOAP, gRPC, MQTT, …) : fournisseur, consommateur, protocole, format, version du contrat et politique de versioning, sécurité, statut. Chaque interface est identifiée (`API-001`, …), reliée aux systèmes (`SYS-xxx`) et à la contrainte d'intégration (`CT-007` du `08-contraintes.md`). La sécurité de chaque interface (authentification, chiffrement) est détaillée dans `11-securite.md`.
-->

| ID      | Interface / API                          | Fournisseur | Consommateur(s) | Protocole | Format d'échange | Contrat (version) | Versioning / compatibilité | Sécurité | Statut |
| ------- | ---------------------------------------- | ----------- | --------------- | --------- | ---------------- | ----------------- | -------------------------- | -------- | ------ |
| API-001 | A définir durant la conception détaillée |             |                 |           |                  |                   |                            |          |        |

**Tableau 26. Registre des interfaces externes / contrats d'API**

<!-- Décrire la **politique de versioning** des interfaces (compatibilité ascendante, dépréciation, coexistence de versions) et référencer les **contrats** (OpenAPI, AsyncAPI, schémas) dans le répertoire de référence du projet.-->

### Évaluation de l'architecture

<!-- 
Cette section documente l'**évaluation de l'architecture de la solution** (conformance) vis-à-vis des exigences (`03-besoins_affaires_exigences.md`), des NFRs (`02-objectifs.md`), des critères de qualification (`02`) et des critères d'acceptation. L'évaluation suit une méthode structurée (revue, inspection, ATAM simplifiée) et produit un statut de conformité.
-->

#### Méthode d'évaluation

<!-- Décrire la méthode utilisée (ex. revue d'architecture, inspection formelle, ATAM simplifiée, ARID, SAAM), les participants, la période. -->

#### Critères d'évaluation

| ID       | Critère | Source (exigence/NFR/critère) | Description | Priorité |
| -------- | ------- | ----------------------------- | ----------- | -------- |
| EVAL-001 | ...     | OBJ-ARC-001 / NFR-PERF-001    | ...         | Haute    |
| EVAL-002 | ...     | OBJ-ARC-002 / NFR-SEC-001     | ...         | Haute    |
| ...      | ...     | ...                           | ...         | ...      |

**Tableau 29. Critères d'évaluation de l'architecture**

#### Résultats de l'évaluation

| ID       | Critère | Résultat (Conforme / Partiellement / Non conforme / Non applicable) | Écarts constatés | Actions correctives / ADR | Statut |
| -------- | ------- | ------------------------------------------------------------------- | ---------------- | ------------------------- | ------ |
| EVAL-001 | ...     | ...                                                                 | ...              | ADR-xxx                   | ...    |
| EVAL-002 | ...     | ...                                                                 | ...              | ADR-xxx                   | ...    |
| ...      | ...     | ...                                                                 | ...              | ...                       | ...    |

**Tableau 30. Résultats de l'évaluation**

#### Statut global de conformité

<!-- Résumé : **Conforme** / **Conforme avec réserves** / **Non conforme**. Lister les réserves majeures, les ADR associés et le plan de remédiation. -->

---

<!-- Lier l'évaluation aux **tests non-fonctionnels** (`13-plan-qualite.md`), aux **défauts d'architecture** (`DEF-xxx` du `06`), et aux **ADR** tracés dans la skill `create-architectural-decision-record`. -->

### Satisfaction exigences → composants/vues

<!-- 
Cette section établit la **matrice de satisfaction** des exigences par l'architecture : pour chaque exigence fonctionnelle (`UC-xxx` du `03-besoins_affaires_exigences.md`) et non-fonctionnelle (`NFR-xxx` du `02-objectifs.md`), identifier le ou les **composants** (`SYS-xxx` du `06` et composants d'`architecture-detaillee/`) et les **vues** où elle est traitée, avec un **statut de couverture**. Elle complète la matrice de suivi du `02-objectifs.md` (patrons ↔ exigences), la traçabilité exigences/UC → tests du `13-plan-qualite.md` et le mappage préoccupations → vues du `001`. La traçabilité est **bidirectionnelle** (exigence → composant/vue, et composant → exigences satisfaites).
-->

#### Matrice de satisfaction exigences → composants/vues

<!-- 
Une ligne par exigence. Le **composant** est référencé par son système (`SYS-xxx`) et/ou son composant détaillé (`architecture-detaillee/<software_system>/`). La **vue** précise où l'exigence est traitée (vue contexte `DIA-xxx`, vue composants `0004-architecture-applicative.md`, vue exécution `SC-xxx`, vue sécurité `11-securite.md`, vue données `10-cycle_vie_donnees.md`, vue infrastructure `09-deploiement.md`). Statut : **Couvert / Partiel / Non couvert**.
-->
| Exigence | Composant(s) satisfaisant(s) | Vue(s) où traitée | Statut de couverture |
| ---------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------- |
| UC-001 | SYS-001 — `software_system_1` (composants `web_apps`, `database` du `0005-composants.md`) | Vue contexte (DIA-002) ; vue composants (`0004-architecture-applicative.md`) | Couvert |
| NFR-001 | SYS-001 — `09-deploiement.md` (INF-001) ; `11-securite.md` | Vue infrastructure (`0007-infrastructure.md`) ; vue sécurité (`11-securite.md`) | Partiel |
| ... | ... | ... | ... |

**Tableau 73. Matrice de satisfaction exigences → composants/vues**

#### Traçabilité inverse — composant → exigences satisfaites

<!-- 
Vue inversée : pour chaque composant (`SYS-xxx` / composant d'`architecture-detaillee/`), lister les exigences (`UC-xxx` / `NFR-xxx`) qu'il satisfait. Toute exigence en statut **Non couvert** (aucun composant, aucune vue) constitue un **écart** à traiter dans l'évaluation de l'architecture (`06`) et le plan de qualité (`13-plan-qualite.md`).
-->

| Composant                                              | Exigences satisfaites | Statut de couverture |
| ------------------------------------------------------ | --------------------- | -------------------- |
| SYS-001 — `software_system_1` (`web_apps`, `database`) | UC-001, NFR-001       | Couvert              |
| ...                                                    | ...                   | ...                  |

**Tableau 74. Traçabilité inverse — composant → exigences satisfaites**

<!-- 
Maintenir cette matrice à chaque évolution des exigences (`02`, `03`), de l'architecture (`06`, `architecture-detaillee/`) ou du plan de qualité (`13`). Référencer les écarts de couverture dans les critères d'évaluation (`EVAL-xxx` du `06`) et les ADR concernés.
-->