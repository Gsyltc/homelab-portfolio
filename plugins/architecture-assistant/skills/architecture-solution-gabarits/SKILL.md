---
name: architecture-solution-gabarits
description: Gabarits communs de documentation d'architecture de solution et d'intégration (DAS découpée en fichiers Markdown par thème) et catalogue de 45 patrons d'architecture cloud (patron-architecture/). Utiliser pour créer ou mettre à jour la documentation d'architecture d'un projet, en modifiant toujours les mêmes fichiers. Les gabarits sont dans le répertoire gabarits/ et les patrons dans patron-architecture/.
---

# Gabarits de documentation d'architecture de solution et d'intégration

Gabarit commun pour la documentation d'architecture de solution (DAS) et d'intégration. La documentation est **découpée en plusieurs fichiers Markdown, un par thème**. Les gabarits se trouvent dans le répertoire `gabarits/` de cette skill. Conserver ce découpage.

Cette skill inclut aussi un **catalogue de patrons d'architecture cloud** dans le répertoire `patron-architecture/` : 43 patrons du catalogue de l'Azure Architecture Center plus 2 patrons complémentaires **hors Well-Architected Framework** (Transactional Inbox et Transactional Outbox, d'après l'article de SoftwareMill). Tous sont agnostiques à la technologie : Azure, AWS, sur site, hybride. Chaque fiche décrit l'objectif du patron, quand l'envisager ou non, les prérequis, les avantages/inconvénients et les piliers du Well-Architected Framework couverts.

## Contenu des gabarits

| Fichier (dans `gabarits/`)           | Thème |
|--------------------------------------|-------|
| `001-document-architecture-solution.md` | Page de garde : métadonnées, historique, arrimages (RACI), lexique, références, index des tableaux et diagrammes |
| `01-introduction.md`                 | Contexte, vision, périmètre, parties prenantes, hypothèses |
| `02-objectifs.md`                    | Objectifs, piliers Well-Architected (Azure et AWS), matrice de suivi (traçabilité patrons ↔ piliers ↔ exigences), critères de qualification |
| `03-besoins_affaires_exigences.md`   | Processus d'affaires, cas d'utilisation, critères d'acceptation |
| `04-risques.md`                      | Analyse des risques |
| `05-planification.md`                | Planification, efforts, coûts |
| `06-architecture-solutions.md`       | Architectures de solution (haut niveau), diagrammes, acteurs, table des systèmes/conteneurs (pont vers l'architecture détaillée `architecture-detaillee/<software_system>/`), renvois, défauts d'architecture |
| `07-choix-des-solutions.md`          | Solutions étudiées et choix |
| `08-contraintes.md`                  | Lois, conformités, contraintes technologiques |
| `09-deploiement.md`                  | Implantation, environnement, déploiement, DevSecOps |
| `10-cycle_vie_donnees.md`            | Cycle de vie des données |
| `11-securite.md`                     | Sécurité |
| `12-volumetries.md`                  | Volumétrie |
| `13-plan-qualite.md`                 | Plan de qualité |
| `14-preventions-et-resilience.md`    | Prévention, reprise après sinistre, résilience |
| `15-concepts-transverses.md`         | Concepts transverses (communication, erreurs, transactions, cache, persistance, observabilité, configuration, accessibilité) |
| `16-questions-decisions.md`          | **Dernier fichier de la liste** : regroupe en un seul fichier les **invariants hérités** (section de cadrage), les **questions en attente** et les **décisions attendues** ; questions et décisions déclinées en sous-sections par domaine (logiciel, sécurité, données, infrastructure). Porte **toujours le numéro le plus élevé** de la DAS (voir règle d'or 20) |
| `00-architecture-detaillee.md`       | **Gabarit de page d'entrée réutilisable** pour chaque dossier d'architecture détaillée (`architecture-detaillee/<software_system>/<volet>/00-…`). Sections : Portée et objectifs, Socle de conception, Table du chapitre (renvois par ancre Structurizr). **Pas de « Synthèse exécutive »** ; tableaux non numérotés ; titre en `h2` (voir règle d'or 16) |

## Front-matter de ciblage

Chaque gabarit de la DAS (`001`, `01`–`16`) porte en tête un **front-matter YAML** (délimité par `---`), non intrusif (ignoré au rendu Markdown) et placé **avant** le contenu. Il permet à la skill `presentation-targeting` de **localiser l'information à présenter sans lecture exhaustive** du corps. Le front-matter est copié avec le gabarit à l'initialisation (règle d'or 3) puis maintenu à jour (règles d'or 12 et 13).

```yaml
---
doc_id: <id-stable>                       # ex. das-03-besoins-affaires
theme: <thème principal>                  # ex. Besoins d'affaires, BAE, cas d'usage
domaine: [<domaines>]                     # affaires, solution, logiciel, data, infrastructure, ia, securite, transverse
sujets: [<titres H2 et H3>]               # = titres ## et ### du document, dans l'ordre ; maj quand les titres changent
types_presentation: [<types>]            # executive, entreprise, technique, securite
sensibilite: <public|interne|restreint>   # confidentialité réelle (ne pas exposer 'restreint' au client)
togaf_layer: <business|data|application|technology|null>
ordre_presentation: <n|null>
---
```

- **`sujets`** est le **sommaire ciblable** : la liste des intitulés H2/H3 (texte du titre), dans l'ordre du document. Il permet de mapper un chapitre de présentation directement vers la ou les sections concernées. Le maintenir à jour à chaque ajout/renommage/suppression d'un titre H2/H3 (règle d'or 13).
- **`domaine`** classe le document par domaine d'architecture : `affaires`, `solution`, `logiciel`, `data`, `infrastructure`, `ia`, `securite`, `transverse`. Le domaine **`solution`** traite de l'**architecture de solution à haut niveau** (vue d'ensemble, cadrage, choix structurants de la solution), par opposition au détail logiciel/data/infra.
- **`sensibilite`** doit refléter la confidentialité **réelle** du contenu ; `restreint` (ex. modélisation des menaces, GIA) n'est jamais exposé au client.
- **Aucun secret** ne figure dans le front-matter (règle d'or 12).

## Renvois vers l'architecture détaillée (format Structurizr)

La documentation est rendue par **Structurizr** (vue `documentation` d'un `SoftwareSystem`). Les **liens Markdown par chemin de fichier** (`../architecture-detaillee/<ss>/…​.md`) **ne résolvent pas** dans ce rendu : ils sont **proscrits**. Le format de renvoi **unique** vers une section d'architecture détaillée est le **lien d'ancre Structurizr** :

```
documentation/<Software System>#<ancre-de-section>
```

- `<Software System>` est le **nom** du `SoftwareSystem` tel qu'il figure dans le modèle (`models/`), **URL-encodé** (espace → `%20`). Exemple : `documentation/Talent%20Match`.
- `<ancre-de-section>` est le **slug** du titre de section visé (voir « Règle de slug d'ancre »).
- Exemple complet attendu : `documentation/Talent%20Match#api-applicatives`.
- Contre-exemple **proscrit** : `architecture-detaillee/talent-match/architecture-logicielle/01-vue-ensemble-composants.md`.

### Règle de slug d'ancre

Le slug d'ancre dérive du **texte du titre** de la section visée, de façon déterministe :

1. passage en **minuscules** ;
2. **apostrophes** et guillemets **retirés** (`l'appariement` → `lappariement`) ;
3. tout caractère non alphanumérique (espaces, ponctuation) → **tiret** `-`, les tirets multiples étant réduits à un seul, et les tirets de début/fin retirés ;
4. **accents** : le comportement dépend de l'instance Structurizr. Par **défaut**, considérer une **translittération** (`é`→`e`, `à`→`a`, `ç`→`c`…), car plusieurs instances translittèrent avant de slugifier. Si l'instance cible **conserve** les accents dans l'ancre, aligner le slug sur son rendu réel. **En cas de doute, vérifier l'ancre effectivement générée** par l'instance avant de figer le renvoi — un renvoi qui ne résout pas est un défaut.

Exemples : « API applicatives » → `api-applicatives` ; « Cycle de vie des données » → `cycle-de-vie-des-donnees` (défaut translittéré) ; « Appariement mandats ↔ candidats » → `appariement-mandats-candidats`.

### Libellé du lien = nom de la section

Dans **toute** table ou liste de renvoi (table des conteneurs du `06`, section « Architecture détaillée — renvois », table du chapitre d'une page `00`), le **libellé** du lien Markdown est le **nom de la section** visée (texte du titre), **jamais** un nom ou un chemin de fichier. Forme : `[Nom de la section](documentation/<Software System>#<ancre>)`. **Ne pas** ajouter de colonne « Fichier » : le fichier n'est pas une donnée de navigation côté Structurizr, l'ancre l'est.

### Périmètre d'un renvoi (niveau de contenu)

Un renvoi vers l'architecture détaillée ne vise **que du contenu de niveau composant et en dessous** (C4 **Niveau 3 — Composants** et **Niveau 4 — Code**). Les sections du `06` dont le contenu vit en architecture détaillée (ex. diagramme de composants, scénarios d'exécution au niveau composant) ne portent **que le renvoi** — **ni description détaillée, ni image embarquée** ; le `06` reste la vue solution haut niveau (C4 N1 contexte / N2 conteneurs) et **pointe**. Voir règles d'or 4-bis et 17.

### Portée de la table « Architecture détaillée — renvois » du `06`

Cette table (sous la table des conteneurs, `06`) ne liste **que les renvois de l'architecture détaillée *logicielle* de la solution désirée** (volet porté par l'architecture de solution). Les autres volets ne s'y retrouvent **pas** directement : ils sont atteints via leur **document de niveau solution** respectif —

- **données** → `10-cycle_vie_donnees.md` (puis `architecture-detaillee/<ss>/architecture-donnees/`) ;
- **sécurité** → `11-securite.md` (puis `architecture-detaillee/<ss>/architecture-securite/` et sa page `00`) ;
- **infrastructure** → `09-deploiement.md` (puis `architecture-detaillee/<ss>/architecture-infra/`).

## Quand utiliser

- Créer la documentation d'architecture de solution et d'intégration d'un nouveau projet.
- Mettre à jour la documentation d'architecture d'un projet existant suite à de nouvelles exigences.

## Règles d'or

1. **Toujours modifier dans les mêmes fichiers.** La documentation d'architecture d'un projet est découpée dans des fichiers fixes. Toute modification se fait en **lisant, analysant puis modifiant les fichiers existants** — jamais en recréant ou en restructurant le découpage.
2. **Vérifier la couverture d'un patron.** Chaque décision d'architecture (choix de solution, de technologie, de structure d'intégration) doit **vérifier si elle couvre un patron** du répertoire `patron-architecture/` de cette skill. Si oui, référencer la fiche du patron (ex. `patron-architecture/circuit-breaker.md`) dans le fichier concerné et dans la matrice de suivi du `02` ; si aucun patron ne couvre la décision, l'expliciter.
3. **Initialisation** : copier **l'ensemble** des fichiers de `gabarits/` dans le répertoire `documentation/` du projet, en conservant les noms de fichiers **et le front-matter YAML de ciblage** en tête de chaque fichier (voir « Front-matter de ciblage »). Si un thème n'est pas couvert pour l'instant, le gabarit est simplement copié tel quel, front-matter compris.
4. **Modification** :
   - Lire et analyser les fichiers existants (contexte global, décisions déjà prises) avant toute modification.
   - Appliquer les modifications selon les nouvelles exigences, à la bonne section du bon fichier.
   - Effectuer une **relecture de cohérence** (autocontrôle) des modifications avant toute revue : cohérence entre fichiers, terminologie, numérotation des tableaux, références croisées, historique.
   - Toute modification doit être **approuvée par l'humain** lors de la phase de revue.
5. Conserver le découpage des fichiers, les noms de fichiers et la structure des sections.
5-bis. **Séparation solution ↔ détaillé (renvoi, pas duplication).** Le `06` est la **vue solution haut niveau** (C4 **Niveau 1 — Contexte** et **Niveau 2 — Conteneurs**). Tout contenu de **niveau composant et en dessous** (C4 **Niveau 3 — Composants**, **Niveau 4 — Code**) — diagramme de composants, scénarios d'exécution détaillés au niveau composant, défauts logiciels détaillés — vit **en architecture détaillée** : dans le `06`, les sections concernées portent **uniquement le renvoi** (ancre Structurizr, voir « Renvois vers l'architecture détaillée (format Structurizr) »), **sans** description détaillée **ni** image embarquée. On ne **duplique** jamais entre solution et détaillé : chaque fait vit à **un seul endroit** et l'autre niveau **pointe**.
6. Maintenir la **numérotation globale et continue** des tableaux ainsi que l'index du fichier `001` (liste des tableaux et des diagrammes) à chaque changement. **Index des diagrammes exhaustif** : l'index des diagrammes (Tab. 7 du `001`) doit couvrir **à la fois** les diagrammes de l'architecture de **solution** (`06`) **et** ceux des **architectures détaillées** (`architecture-detaillee/<software_system>/…`), la colonne « Fichier » pointant la bonne vue. *Cette colonne « Fichier » est propre à l'**index technique des diagrammes** (traçabilité vue ↔ source) ; elle ne s'applique **pas** aux **tables de renvoi** de navigation (table des conteneurs du `06`, section « Architecture détaillée — renvois », table du chapitre d'une page `00`), qui n'ont **jamais** de colonne « Fichier » et renvoient par **ancre Structurizr** avec un libellé = nom de section (voir « Renvois vers l'architecture détaillée (format Structurizr) »).*
7. Mettre à jour l'**historique du document** (`001`) à chaque modification (version, date, statut, motif, auteur, approbateur). La colonne **« Description / Motif du changement »** du Tableau 2 (Historique) tient en **une ligne factuelle** (style de référence V1.0–V1.6), jamais en paragraphes multi-phrases :
   - Conserver le **strict essentiel** : objet du changement + identifiant de traçabilité (`ORIG-xxx` / `ADR-xxxx`) + fichier(s) touché(s) quand c'est le cœur du changement.
   - Retirer la **prose explicative** et les **énumérations détaillées** (listes de composants/vues, justifications, « non-régression attestée », etc.) — elles vivent dans le corps du DAS et les ADR, pas dans l'historique.
   - **Zéro doublon** entre lignes d'historique ; la **traçabilité** (IDs) reste toujours préservée.
   - **Granularité d'une entrée = un livrable accepté, pas une correction intermédiaire** (politique de consolidation). Un **lot de travail** (ex. « production de l'architecture détaillée ») donne **une seule ligne de version** décrivant le **livrable**, et non une ligne par micro-correction issue des allers-retours de revue. Tant qu'un lot est **en cours de revue** (statut `Revue en cours`), les itérations successives **mettent à jour la même ligne** (motif consolidé, date réactualisée) au lieu d'en créer une nouvelle à chaque correction ; une **nouvelle ligne** n'est ouverte que pour un **nouveau lot** de travail distinct. À l'acceptation, la ligne reflète le livrable tel qu'approuvé. Objectif : un historique où **une ligne = un livrable**, lisible, sans la trace des `V1.1→V1.15` de micro-corrections.
   - **Colonne « Statut » — cycle de revue** : à chaque mise à jour, la **dernière version** (ligne la plus récente) passe à **`Revue en cours`** et **toutes les versions précédentes** passent à **`Revue`**. Le statut **`Approuvé`** n'est inscrit qu'**après validation humaine explicite**.
8. Utiliser des **identifiants codés** cohérents pour les articles (ex. `RISQ-001`, `UC-001`, `CT-001`).
9. Les diagrammes sont générés en **code** (PlantUML, Mermaid, Structurizr, BPMN, C4) et référencés dans l'index du `001` ; ils sont **embarqués via Structurizr** (vue `image` + kroki + `embed:`, voir règle d'or 19). **Le modèle C4/Structurizr est la source de vérité de l'architecture détaillée.** L'architecture détaillée d'un `SoftwareSystem` (ou conteneur de 1er rang) ne vit pas seulement en prose Markdown : chaque système ayant une architecture détaillée doit **la porter dans le modèle** (`models/`, `views/`), conteneurs et composants modélisés comme éléments de 1er ordre. La DAS (`architecture-detaillee/<software_system>/`, table des conteneurs du `06`, renvois) **reflète** ce modèle. Porter l'architecture détaillée dans le modèle est un **travail de modélisation à part entière** (évolution de `models/`/`views/`), distinct d'un simple déplacement de prose. **Ordre NON NÉGOCIABLE** des sous-répertoires d'architecture détaillée (au sein de chaque `architecture-detaillee/<software_system>/`) : `architecture-logicielle`, `architecture-infra`, `architecture-donnees`, `architecture-securite`.
10. Les **décisions d'architecture** sont tracées dans des ADR (voir la skill `create-architectural-decision-record`) et référencées dans les fichiers concernés.
11. Ne jamais inclure de secrets, mots de passe ou identifiants dans la documentation.
12. **Front-matter de ciblage maintenu à jour.** Chaque fichier de la DAS (`001`, `01`–`16`) porte en tête un **front-matter YAML de ciblage** (voir « Front-matter de ciblage ») consommé par la skill `presentation-targeting`. Le maintenir cohérent avec le contenu : **jamais de secret** dans le front-matter, et une **sensibilité réelle** (`sensibilite`) reflétant la confidentialité effective des sections (`restreint` n'est jamais exposé au client).
13. **Maintenance du champ `sujets`.** Le champ `sujets` du front-matter reflète les **titres de niveau 2 (`##`) et niveau 3 (`###`)** du document, dans l'ordre du document. Dès qu'un titre H2/H3 est **ajouté, renommé ou supprimé**, mettre à jour `sujets` dans le même changement pour qu'il reste le reflet fidèle de la structure ciblable.
14. **Aucune information de génération dans la documentation.** Un document livré ne contient **QUE** ce qui est pertinent pour le projet (architecture, décisions, exigences, etc.). Il est **interdit** d'ajouter des notes liées à la **génération** ou à la **façon dont a été créé** un diagramme ou un élément du DAS. Proscrire notamment :
    - toute mention de **méta-génération** — p. ex. « diagramme généré avec … », « document produit par … », notes d'outil, d'agent ou horodatage de génération ;
    - toute note décrivant **comment** un diagramme, un tableau ou une section a été construit, modélisé ou dérivé (procédé de fabrication, outil employé, étapes de production) ;
    - tout commentaire de processus de rédaction ou de génération, qu'il soit dans le corps, en note de bas de page ou en commentaire masqué.
    Ces informations relèvent du **processus**, pas du contenu d'architecture : les retirer avant livraison. En cas de doute, appliquer le critère « **QUE des informations pertinentes au projet** ».
15. **Feuille de route sans date → J+7.** Pour toute feuille de route / timeline / roadmap, si aucune date n'est indiquée, considérer le début à **J + 7 jours à compter de la date du jour**.
16. **Architecture détaillée sous `architecture-detaillee/<software_system>/`.** L'architecture détaillée de chaque système logiciel vit dans un répertoire `architecture-detaillee/<software_system>/` organisé en **quatre sous-répertoires**, dans cet **ordre NON NÉGOCIABLE** :
    - `architecture-logicielle/` — architecture logicielle détaillée (composants, séquences, défauts) ;
    - `architecture-infra/` — architecture infrastructure et DevOps détaillée ;
    - `architecture-donnees/` — architecture de données détaillée ;
    - `architecture-securite/` — architecture de sécurité détaillée.
    Les éléments `conteneurs / sous-systèmes` ayant une documentation détaillée relèvent de ce détail, **hors** de la vue solution haut niveau du `06`. Convention de numérotation : **séquentielle libre** par sous-répertoire (`architecture-detaillee/<software_system>/architecture-logicielle/NN-…`), l'index du `001` (Tab. 6/7/8) assurant la correspondance ; pas de renumérotage à fort blast radius.
    - **Page d'entrée `00` par dossier détaillé (obligatoire).** Chaque sous-répertoire d'architecture détaillée possède une **page d'entrée `00`** calquée sur le gabarit `gabarits/00-architecture-detaillee.md` de cette skill (lui-même aligné sur `00-analyse-securite.md`) : sections **Portée et objectifs**, **Socle de conception**, **Table du chapitre** ; **sans** « Synthèse exécutive ». Les tableaux de la page `00` **ne sont pas numérotés** (navigation locale, hors index global Tab. 8 du `001`). La **table du chapitre** renvoie aux sections du dossier par **ancre Structurizr** (libellé = nom de section), **sans** colonne « Fichier ».
    - **Conventions de titres de l'architecture détaillée** (sans ambiguïté) :
      - **Titre de la page `00`** : niveau **`h2` (`##`)** (ex. `## Architecture logicielle détaillée`), à l'image du `## Analyse de sécurité` du `00-analyse-securite.md` ; les sous-sections démarrent en `###`.
      - **Pas de préfixe** de type `Architecture logicielle détaillée — …` dans les titres des **fichiers de contenu** (`01`, `02`, …) : le titre porte le **sujet** (ex. `## Vue d'ensemble des composants`), le contexte « architecture détaillée logicielle » étant donné par le dossier et la page `00`.
      - **Pas de suffixe** de **nom de système** dans les titres (ex. proscrire `… (SYS-001 Talent Match)`) : l'appartenance au système est portée par l'arborescence `architecture-detaillee/<software_system>/` et le modèle, pas répétée dans chaque titre.
17. **Table des conteneurs = pont unique solution ↔ détaillé.** Dans le `06`, la table « Liste des systèmes / conteneurs logiques » (Tab. 23) est le pont unique vers l'architecture détaillée :
    - **Granularité conteneur** : une ligne par **conteneur de 1er rang** ; les **composants C4** d'un conteneur composite redescendent **sous** la ligne de leur conteneur (jamais de ligne de 1er rang), tout en restant référencés par identifiant (`SYS-xxx`). Vérifier la **complétude** de la table.
    - **Lien de nom = ancre Structurizr** : le **nom** d'un conteneur disposant d'une doc détaillée est un **lien Markdown** au format **`documentation/<Software System>#<ancre>`** (voir « Renvois vers l'architecture détaillée (format Structurizr) ») vers la section d'architecture détaillée logicielle correspondante ; granularité conteneur, composants non liés. **Jamais** de lien par chemin de fichier (`…/architecture-logicielle/…​.md`), **jamais** de colonne « Fichier ».
    - **Chapeau de lecture** : un **chapeau** précède la table (nature, granularité, comment trouver la doc détaillée = nom-lien par ancre, index des sujets non-conteneur, absences volontaires). **Pas de table-sommaire séparée** (ce serait un doublon de la table des conteneurs).
    - **Section « renvois » (périmètre logiciel)** : une section compacte « Architecture détaillée — renvois », **directement sous la table**, référence par **ancre Structurizr** (libellé = nom de section) les **sujets transverses de l'architecture détaillée *logicielle*** sans conteneur dédié. Elle **ne** liste **que** le volet **logiciel** (porté par l'architecture de solution) ; les volets **données / sécurité / infrastructure** sont atteints via leurs documents de niveau solution (`10-cycle_vie_donnees.md`, `11-securite.md`, `09-deploiement.md`), pas depuis cette table. Aucun document détaillé ne doit être **orphelin** de la navigation (atteignable par lien de nom OU par renvoi, selon son volet).
18. **Aucune référence de commit ni de tâche de suivi dans la documentation.** De façon **générale**, **aucun** document de la documentation d'architecture — DAS (`001`, `01`–`16`, `architecture-detaillee/…`) **comme ADR (`decisions/`)** — ne contient de **SHA de commit** ni d'**identifiant de tâche de suivi** (`ORIG-NNN`, liens `mention://issue`, numéros de tickets, etc.) : ce sont des références de **processus**, pas du contenu d'architecture. Règle de nettoyage : retirer SHA et identifiants de tâches, **neutraliser** les liens de tâches en texte simple, reformuler la ponctuation orpheline — **sans** changement sémantique. **Conservés** : les tags de **version** (`v2.10.0`, baselines) et les références **OpenSpec** (specs/changes, `REF-04`…), qui ne sont ni des commits ni des tâches. Cette règle s'aligne sur la skill `create-architecture-decision-record` (« Jamais de référence au workflow », « Pas d'issues en référence »).
20. **Fichier « Questions en attente / Décisions attendues » toujours en dernier.** Les **questions en attente** et les **décisions attendues** du projet sont regroupées dans **un seul et même fichier** (`16-questions-decisions.md`), structuré en **deux grandes sections** — *Questions en attente* puis *Décisions attendues* — chacune déclinée en **sous-sections par domaine** (dans l'ordre : *Logiciel*, *Sécurité*, *Données*, *Infrastructure* ; ajouter un domaine supplémentaire seulement si le projet le requiert). Une **section de cadrage « Invariants hérités »** précède ces deux sections : elle rappelle les **invariants non contournables hérités** des couches supérieures (gouvernance, plancher de sécurité, règles de niveau supérieur, ADR acceptés — source `core/common/protocols/governance-security.md` § « Invariants non contournables » et registre `decisions/`) qui **bornent** questions et décisions ; **aucune** question ni décision ne peut affaiblir un invariant hérité (en cas de tension, l'invariant **prime** et l'arbitrage humain est requis). Ce fichier porte **toujours le numéro le plus élevé** de la DAS afin de rester le **dernier de la liste** : si un nouveau fichier est ajouté au DAS, ce fichier de questions/décisions doit être **renommé** pour reprendre le numéro le plus élevé (ex. un ajout en `16-…` fait passer les questions/décisions en `17-questions-decisions.md`). Mettre alors à jour son `ordre_presentation` et toutes les références au fichier. Identifiants codés `INV-NNN` (invariants hérités), `Q-NNN` (questions) et `DEC-NNN` (décisions), continus et globaux au fichier par type ; une question tranchée est close avec renvoi, une décision tranchée devient un **ADR** (`decisions/`, skill `create-architectural-decision-record`) référencé dans le fichier.
19. **Diagrammes embarqués via Structurizr par défaut.** Par **défaut**, les diagrammes **Mermaid**, **PlantUML** et **BPMN** sont **embarqués pour Structurizr** : chacun est déclaré comme **vue `image`** Structurizr (`views/`), rendue par **kroki**, et intégré à la DAS **exclusivement** via une référence `embed:` — `![…](embed:<clé>)`. **Proscrire** l'inclusion directe d'un fichier image/source (`![](….svg)`, `![](….puml)`, `.mmd` brut) dans le Markdown. Le renderer kroki est choisi selon le type de source (`mermaid`, `plantuml`, `bpmn`) ; les diagrammes réutilisent le **thème du projet** (`theme/`) lorsqu'il existe. Chaque diagramme est **validé** (DSL Structurizr) et **indexé** dans le `001` (Tab. 7). *Les diagrammes C4 sont déjà des vues Structurizr natives ; cette règle étend l'embarquement par vue `image`+kroki aux sources non-C4 (Mermaid, PlantUML, BPMN).*

## Arrimage avec les autres skills

- `create-architectural-decision-record` : chaque décision d'architecture (choix de solution, patron, technologie) fait l'objet d'un ADR référencé dans les fichiers concernés.
- `presentation-targeting` : consomme le **front-matter de ciblage** de chaque fichier de la DAS (`theme`, `domaine`, `types_presentation`, `sensibilite` et surtout `sujets` = titres H2/H3) pour localiser l'information à présenter sans lecture exhaustive. Garder ce front-matter à jour (règles d'or 12 et 13) pour que le ciblage reste fiable.
- Les fichiers `09`, `12`, `14` sont rédigés en collaboration avec les architectes infrastructure, cloud, sécurité et DevOps ; `13` en arrimage avec le leader Assurance Qualité.
