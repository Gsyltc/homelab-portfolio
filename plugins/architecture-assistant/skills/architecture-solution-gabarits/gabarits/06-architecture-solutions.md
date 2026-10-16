---
doc_id: das-06-architecture-solutions
theme: Architecture de solution, diagrammes
domaine: [solution, logiciel, infrastructure]
sujets:
  - Architectures de solution
  - Description de l'architecture de solution
  - Liste des diagrammes d'architecture
  - Diagramme système (DIA-001)
  - Software System 1 (SYS-001) — Diagramme de contexte (DIA-002)
  - Software System 2 (SYS-002) — Diagramme de contexte (DIA-003)
  - Scénarios d'exécution (Runtime View)
  - Défauts d'architecture
  - Registre des interfaces externes / contrats d'API
  - Évaluation de l'architecture
  - Satisfaction exigences → composants/vues
types_presentation: [technique, entreprise]
sensibilite: interne
togaf_layer: application
ordre_presentation: 6
---
## Architectures de solution

<!-- 
Cette section décrit **l'architecture de solution** : la solution dans son écosystème global (systèmes logiciels, acteurs, systèmes externes, intégrations), **à haut niveau**.
**L'architecture détaillée** de chaque système logiciel est documentée **séparément** sous `architecture-detaillee/<software_system>/`, répertoire organisé en **quatre sous-répertoires** (ordre NON NÉGOCIABLE) :
  - `architecture-logicielle/` — architecture logicielle détaillée (composants, séquences, défauts) ;
  - `architecture-infra/` — architecture infrastructure et DevOps détaillée ;
  - `architecture-donnees/` — architecture de données détaillée ;
  - `architecture-securite/` — architecture de sécurité détaillée.
**Ce qui relève du détail logiciel.** Passent en architecture détaillée logicielle (fichiers dédiés sous `architecture-detaillee/<software_system>/architecture-logicielle/`), **hors** de cette vue solution haut niveau : les éléments `conteneurs / sous-systèmes` de l'architecture ayant une documentation détaillée. Exemple : un `softwareSystem` possède un conteneur/sous-système `SYS-001` avec une documentation dédiée → c'est de l'architecture détaillée.
**Le modèle reste la source de vérité.** L'architecture détaillée d'un `softwareSystem` (ou conteneur de 1er rang) doit **être portée dans le modèle C4/Structurizr** (`models/`, `views/`) — conteneurs et composants modélisés comme éléments de 1er ordre, pas en simple prose Markdown. Cette DAS (table des conteneurs, renvois, `architecture-detaillee/<software_system>/`) **reflète** ce modèle.
Les diagrammes de cette section restent **à haut niveau** ; les diagrammes détaillés (composants, séquences, données, déploiement) sont **ajoutés à la demande** dans les documents d'architecture détaillée. Chaque décision d'architecture est tracée dans un ADR et chaque patron retenu est référencé dans la matrice de suivi du `02-objectifs.md`.
-->

### Description de l'architecture de solution

<!-- Décrire, à haut niveau, la solution : les systèmes logiciels qui la composent, les systèmes externes en interaction, les principaux échanges (flux) entre eux et le contexte d'exploitation. Cette description alimente le diagramme système (landscape). -->

### Liste des diagrammes d'architecture

<!-- Les diagrammes de cette section sont **à haut niveau** (écosystème, contexte des systèmes logiciels). Les diagrammes détaillés sont ajoutés **à la demande** dans les documents d'architecture détaillée (`architecture-detaillee/<software_system>/`) et référencés ici. **Index des diagrammes exhaustif** : l'index des diagrammes du `001` (Tab. 7) doit couvrir **à la fois** les diagrammes de l'architecture de solution **et** ceux des architectures détaillées, la colonne « Fichier » pointant la bonne vue (`06` pour la solution, `architecture-detaillee/<software_system>/…` pour le détail). -->

| ID      | Type                          | Niveau | Description                                                          |
| ------- | ----------------------------- | ------ | -------------------------------------------------------------------- |
| DIA-001 | Diagramme système (Landscape) | Élevé  | Diagramme représentant l'ensemble de l'éco-système global            |
| DIA-002 | Diagramme de contexte         | Élevé  | Contexte du Software System 1 (SYS-001) et ses interactions directes |
| DIA-003 | Diagramme de contexte         | Élevé  | Contexte du Software System 2 (SYS-002) et ses interactions directes |
| DIA-004 | Diagramme de séquence         | Détaillé | Séquence du scénario SC-001 — **niveau composant, en architecture détaillée** (`architecture-detaillee/<software_system>/architecture-logicielle/`) ; renvoi depuis le `06` |
| DIA-005 | Diagramme de séquence         | Détaillé | Séquence du scénario SC-002 — **niveau composant, en architecture détaillée** (`architecture-detaillee/<software_system>/architecture-logicielle/`) ; renvoi depuis le `06` |

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

#### Liste des systèmes / conteneurs logiques

<!--
**Chapeau de lecture (obligatoire, à conserver au-dessus de la table).** Expliquer au lecteur humain, avant la table :
(a) **ce qu'est la table** : le catalogue des **conteneurs de 1er rang** de la solution (systèmes logiciels et conteneurs logiques du diagramme système / de contexte) ;
(b) **la granularité** : une ligne par **conteneur de 1er rang**. Les **composants C4** d'un conteneur composite n'ont **pas** de ligne propre : ils redescendent au rang de composant **sous la ligne de leur conteneur**, tout en restant référencés par identifiant (`SYS-xxx`) pour la traçabilité ;
(c) **comment trouver la doc détaillée** : le **nom** d'un conteneur disposant d'une architecture détaillée est un **lien Markdown au format Structurizr** `documentation/<Software System>#<ancre>` (jamais un chemin de fichier, jamais une colonne « Fichier ») — la table est le **pont unique** solution ↔ détaillé ;
(d) **l'index complet des sujets non-conteneur** : les sujets transverses de l'architecture détaillée **logicielle** sans conteneur dédié sont listés dans la section « Architecture détaillée — renvois » juste sous la table ; les volets **données / sécurité / infrastructure** s'atteignent via `10-cycle_vie_donnees.md`, `11-securite.md`, `09-deploiement.md` ;
(e) **les absences volontaires** : signaler ici les conteneurs volontairement non documentés en détail (ex. `SYS-020`) pour qu'aucune absence ne soit prise pour un oubli.
Cette table remplace tout « sommaire des conteneurs » séparé (pas de table-sommaire doublon).
Format de renvoi : voir la skill `architecture-solution-gabarits`, « Renvois vers l'architecture détaillée (format Structurizr) » — slug d'ancre, URL-encodage du nom de système, libellé = nom de section.
-->

| ID | Nom du conteneur / système | Description | Architecture détaillée |
| ------- | -------------------------- | ----------- | ---------------------- |
| SYS-001 | [Application 1](documentation/Software%20System%201#vue-ensemble-des-composants) | Système logiciel permettant | Oui — nom = lien (ancre Structurizr) |
| SYS-002 | [Application 2](documentation/Software%20System%202#vue-ensemble-des-composants) | Système logiciel | Oui — nom = lien (ancre Structurizr) |
| SYS-003 | Active Directory - Alithya | Gestionnaire d'identités et d'accès | — (système externe, pas de détail) |

<!--
**Composants C4 sous leur conteneur.** Lorsqu'un conteneur de 1er rang est composite, lister ses composants C4 **sous** sa ligne (sous-liste ou lignes indentées), jamais comme lignes de 1er rang de la table. Exemple de forme :
- SYS-001 — Application 1
  - SYS-005 — Composant A (composant C4 de SYS-001)
  - SYS-006 — Composant B (composant C4 de SYS-001)
Vérifier la **complétude** : chaque conteneur de 1er rang présent ; aucun composant promu en ligne de 1er rang.
-->

**Tableau 23. Liste des systèmes / conteneurs logiques**

#### Architecture détaillée — renvois

<!--
Section **compacte** de renvois vers l'architecture détaillée **logicielle**, placée **directement sous la table des conteneurs**. Elle complète les liens de nom de la table pour les **sujets transverses de l'architecture détaillée logicielle sans conteneur dédié** (ex. externalisation d'un gateway, routeur IA local, registre d'interfaces/API, mémoire par couple).

**Périmètre (règle d'or 17).** Cette section ne liste **que** le volet **logiciel** (celui que porte l'architecture de solution désirée). Les autres volets **ne figurent pas ici** : l'architecture détaillée **de données** s'atteint via `10-cycle_vie_donnees.md`, la **sécurité** via `11-securite.md`, l'**infrastructure** via `09-deploiement.md` — chacun renvoyant ensuite vers son propre dossier détaillé (`architecture-detaillee/<software_system>/architecture-donnees|securite|infra/`).

**Format (règle d'or 17 + « Renvois vers l'architecture détaillée (format Structurizr) »).** Chaque renvoi est un **lien Markdown par ancre Structurizr** `documentation/<Software System>#<ancre>` dont le **libellé est le nom de la section** visée — **jamais** un nom ni un chemin de fichier, et **pas** de colonne « Fichier ». Aucun document d'architecture détaillée logicielle ne doit être **orphelin** de la navigation : il est atteignable soit par un lien de nom dans la table (conteneurs), soit par un renvoi ici (sujets transverses). Lorsque des paragraphes de renvoi des sections migrées subsistaient dans ce fichier, les **retirer** : la navigation vers le détail passe exclusivement par la table (liens de nom) et cette section de renvois.

- [Sujet transverse logiciel 1](documentation/Software%20System%201#sujet-transverse-1) — <description courte du sujet transverse>
- [Sujet transverse logiciel 2](documentation/Software%20System%201#sujet-transverse-2) — <description courte du sujet transverse>
-->

### Software System 1 (SYS-001) — Diagramme de contexte (DIA-002)

#### Description — Software System 1 (SYS-001)

<!-- Décrire le contexte du système logiciel 1 et ses entités en interactions directes (niveau élevé). -->

#### Diagramme — Software System 1 (SYS-001)

![Diagramme de contexte](embed:Context_1)

#### Architecture détaillée — Software System 1 (SYS-001)

<!-- 
**Renvoi uniquement (règle d'or 5-bis).** Cette sous-section du `06` (vue solution haut niveau, C4 N1/N2) ne contient **que le renvoi** vers l'architecture détaillée logicielle du Software System 1 — **ni description détaillée, ni image embarquée**. Le contenu de niveau composant (C4 N3/N4) vit sous `architecture-detaillee/software_system_1/architecture-logicielle/` (page d'entrée `00-architecture-detaillee.md`), et dans les trois autres volets `architecture-infra/`, `architecture-donnees/`, `architecture-securite/`. Le **nom** du conteneur dans la table « Liste des systèmes / conteneurs logiques » (Tab. 23) est le **lien de nom** (ancre Structurizr) vers la doc logicielle détaillée. Les diagrammes détaillés sont ajoutés à la demande dans ces documents et indexés dans le `001`. Rappel : l'architecture détaillée est portée dans le modèle C4/Structurizr (`models/`, `views/`), source de vérité.

- [Architecture logicielle détaillée](documentation/Software%20System%201#architecture-logicielle-detaillee) — composants, séquences au niveau composant, défauts logiciels
-->

### Software System 2 (SYS-002) — Diagramme de contexte (DIA-003)

#### Description — Software System 2 (SYS-002)

<!-- Décrire le contexte du système logiciel 2 et ses entités en interactions directes (niveau élevé). -->

#### Diagramme — Software System 2 (SYS-002)

![Diagramme de contexte](embed:Context_2)

#### Architecture détaillée — Software System 2 (SYS-002)

<!-- 
**Renvoi uniquement (règle d'or 5-bis).** Cette sous-section du `06` (vue solution haut niveau, C4 N1/N2) ne contient **que le renvoi** vers l'architecture détaillée logicielle du Software System 2 — **ni description détaillée, ni image embarquée**. Le contenu de niveau composant (C4 N3/N4) vit sous `architecture-detaillee/software_system_2/architecture-logicielle/` (page d'entrée `00-architecture-detaillee.md`), et dans les trois autres volets `architecture-infra/`, `architecture-donnees/`, `architecture-securite/`. Le **nom** du conteneur dans la table « Liste des systèmes / conteneurs logiques » (Tab. 23) est le **lien de nom** (ancre Structurizr) vers la doc logicielle détaillée. Les diagrammes détaillés sont ajoutés à la demande dans ces documents et indexés dans le `001`. Rappel : l'architecture détaillée est portée dans le modèle C4/Structurizr (`models/`, `views/`), source de vérité.

- [Architecture logicielle détaillée](documentation/Software%20System%202#architecture-logicielle-detaillee) — composants, séquences au niveau composant, défauts logiciels
-->

### Scénarios d'exécution (Runtime View)

<!-- 
**Renvoi uniquement pour le niveau composant (règle d'or 5-bis).** Au niveau **solution** (`06`), énumérer les scénarios d'exécution critiques (`SC-xxx`) par un **libellé + une phrase** d'intention — acteurs et systèmes de 1er rang impliqués, résultat attendu. Les **séquences détaillées au niveau composant** (diagrammes de séquence, enchaînements internes) **ne sont pas** décrites ni embarquées ici : elles vivent en architecture détaillée logicielle (`architecture-detaillee/<software_system>/architecture-logicielle/`) et sont atteintes par **renvoi** (ancre Structurizr). Le `06` **pointe**, il ne duplique pas.

- SC-001 — <Nom du scénario 1> : <une phrase d'intention — acteurs et systèmes de 1er rang, résultat attendu>. Séquence détaillée → [Scénario d'exécution SC-001](documentation/Software%20System%201#scenario-dexecution-sc-001)
- SC-002 — <Nom du scénario 2> : <une phrase d'intention — acteurs et systèmes de 1er rang, résultat attendu>. Séquence détaillée → [Scénario d'exécution SC-002](documentation/Software%20System%201#scenario-dexecution-sc-002)
-->

<!-- Lier chaque scénario aux **patrons d'intégration** utilisés (ex. Transactional Outbox/Inbox pour les événements d'intégration, publish/subscribe) et à la **matrice de suivi** du `02-objectifs.md` (patron retenu ↔ exigence/pilier). Le détail de l'enchaînement et le diagramme de séquence restent en architecture détaillée (renvoi ci-dessus) ; ne pas embarquer `embed:sequence_SC-xxx` dans le `06`. -->

### Défauts d'architecture

<!-- Faire la liste des **défauts d'architecture de la solution** (niveau solution). Les défauts logiciels (détaillés) sont documentés sous `architecture-detaillee/<software_system>/architecture-logicielle/`. -->

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
Cette section établit la **matrice de satisfaction** des exigences par l'architecture : pour chaque exigence fonctionnelle (`UC-xxx` du `03-besoins_affaires_exigences.md`) et non-fonctionnelle (`NFR-xxx` du `02-objectifs.md`), identifier le ou les **composants** (`SYS-xxx` du `06` et composants d'`architecture-detaillee/<software_system>/architecture-logicielle/`) et les **vues** où elle est traitée, avec un **statut de couverture**. Elle complète la matrice de suivi du `02-objectifs.md` (patrons ↔ exigences), la traçabilité exigences/UC → tests du `13-plan-qualite.md` et le mappage préoccupations → vues du `001`. La traçabilité est **bidirectionnelle** (exigence → composant/vue, et composant → exigences satisfaites).
-->

#### Matrice de satisfaction exigences → composants/vues

<!-- 
Une ligne par exigence. Le **composant** est référencé par son système (`SYS-xxx`) et/ou son composant détaillé (`architecture-detaillee/<software_system>/architecture-logicielle/`). La **vue** précise où l'exigence est traitée (vue contexte `DIA-xxx`, vue composants d'`architecture-logicielle/`, vue exécution `SC-xxx`, vue sécurité `architecture-securite/` ou `11-securite.md`, vue données `architecture-donnees/` ou `10-cycle_vie_donnees.md`, vue infrastructure `architecture-infra/` ou `09-deploiement.md`). Statut : **Couvert / Partiel / Non couvert**.
-->
| Exigence | Composant(s) satisfaisant(s) | Vue(s) où traitée | Statut de couverture |
| ---------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------- |
| UC-001 | SYS-001 — Application 1 (composants détaillés sous `architecture-detaillee/software_system_1/architecture-logicielle/`) | Vue contexte (DIA-002) ; vue composants (`architecture-logicielle/`) | Couvert |
| NFR-001 | SYS-001 — `09-deploiement.md` (INF-001) ; `11-securite.md` | Vue infrastructure (`architecture-detaillee/software_system_1/architecture-infra/`) ; vue sécurité (`architecture-securite/`, `11-securite.md`) | Partiel |
| ... | ... | ... | ... |

**Tableau 73. Matrice de satisfaction exigences → composants/vues**

#### Traçabilité inverse — composant → exigences satisfaites

<!-- 
Vue inversée : pour chaque composant (`SYS-xxx` / composant d'`architecture-detaillee/<software_system>/architecture-logicielle/`), lister les exigences (`UC-xxx` / `NFR-xxx`) qu'il satisfait. Toute exigence en statut **Non couvert** (aucun composant, aucune vue) constitue un **écart** à traiter dans l'évaluation de l'architecture (`06`) et le plan de qualité (`13-plan-qualite.md`).
-->

| Composant                                              | Exigences satisfaites | Statut de couverture |
| ------------------------------------------------------ | --------------------- | -------------------- |
| SYS-001 — Application 1 (composants détaillés sous `architecture-detaillee/software_system_1/architecture-logicielle/`) | UC-001, NFR-001       | Couvert              |
| ...                                                    | ...                   | ...                  |

**Tableau 74. Traçabilité inverse — composant → exigences satisfaites**

<!-- 
Maintenir cette matrice à chaque évolution des exigences (`02`, `03`), de l'architecture (`06`, `architecture-detaillee/<software_system>/`) ou du plan de qualité (`13`). Référencer les écarts de couverture dans les critères d'évaluation (`EVAL-xxx` du `06`) et les ADR concernés.
-->