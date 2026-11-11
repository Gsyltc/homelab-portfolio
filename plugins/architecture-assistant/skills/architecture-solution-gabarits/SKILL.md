---
name: architecture-solution-gabarits
description: Gabarits de documentation d'architecture de solution et d'intégration (DAS découpée en fichiers Markdown par thème, répertoire gabarits/) et catalogue de 45 patrons d'architecture cloud agnostiques (patron-architecture/). Utiliser pour créer ou mettre à jour la documentation d'architecture d'un projet, en modifiant toujours les mêmes fichiers.
---

# Gabarits de documentation d'architecture de solution et d'intégration

- **DAS découpée par thème** : un fichier Markdown par thème, dans `gabarits/`. Conserver ce découpage.
- **Catalogue de patrons** : `patron-architecture/`, 45 fiches agnostiques (Azure, AWS, sur site, hybride) — objectif, quand l'envisager ou non, prérequis, avantages/inconvénients, piliers Well-Architected couverts.

## Quand utiliser

- Créer la documentation d'architecture de solution et d'intégration d'un nouveau projet.
- Mettre à jour celle d'un projet existant suite à de nouvelles exigences.

## Contenu des gabarits

| Fichier (`gabarits/`) | Thème |
|---|---|
| `001-document-architecture-solution.md` | Page de garde : métadonnées, historique, arrimages (RACI), lexique, références, index des tableaux et diagrammes |
| `01-introduction.md` | Contexte, vision, périmètre, parties prenantes, hypothèses |
| `02-objectifs.md` | Objectifs, piliers Well-Architected (Azure, AWS), matrice de suivi (patrons ↔ piliers ↔ exigences), critères de qualification |
| `03-besoins_affaires_exigences.md` | Processus d'affaires, cas d'utilisation, critères d'acceptation |
| `04-risques.md` | Analyse des risques |
| `05-planification.md` | Planification, efforts, coûts |
| `06-architecture-solutions.md` | Architecture de solution haut niveau (C4 N1/N2), diagrammes, acteurs, table des conteneurs (pont vers le détaillé), renvois, défauts |
| `07-choix-des-solutions.md` | Solutions étudiées et choix |
| `08-contraintes.md` | Lois, conformités, contraintes technologiques |
| `09-deploiement.md` | Implantation, environnement, déploiement, DevSecOps |
| `10-cycle_vie_donnees.md` | Cycle de vie des données |
| `11-securite.md` | Sécurité |
| `12-volumetries.md` | Volumétrie |
| `13-plan-qualite.md` | Plan de qualité |
| `14-preventions-et-resilience.md` | Prévention, reprise après sinistre, résilience |
| `15-concepts-transverses.md` | Concepts transverses (communication, erreurs, transactions, cache, persistance, observabilité, configuration, accessibilité) |
| `16-questions-decisions.md` | Invariants hérités, questions en attente, décisions attendues (par domaine). Toujours le **numéro le plus élevé** de la DAS (règle 17) |
| `00-architecture-detaillee.md` | Page d'entrée réutilisable d'un dossier détaillé : Portée et objectifs, Socle de conception, Table du chapitre. Sans « Synthèse exécutive » ; tableaux non numérotés ; titre `h2` (règle 13) |
| `00-checklist-architecture.md` | **Fichier d'état de processus (pas DAS)** : checklist d'architecture suivant l'avancement sur 5 phases. Initialisation et règles de tenue : règle 3 |

## Front-matter de ciblage

Chaque gabarit DAS (`001`, `01`–`16`) porte en tête un front-matter YAML (délimité par `---`, ignoré au rendu), consommé par la skill `presentation-targeting` pour localiser l'information sans lecture exhaustive. Copié à l'initialisation puis maintenu à jour.

```yaml
---
doc_id: <id-stable>                      # ex. das-03-besoins-affaires
theme: <thème principal>
domaine: [<domaines>]                    # affaires, solution, logiciel, data, infrastructure, ia, securite, transverse
sujets: [<titres H2 et H3>]              # dans l'ordre du document
types_presentation: [<types>]            # executive, entreprise, technique, securite
sensibilite: <public|interne|restreint>
togaf_layer: <business|data|application|technology|null>
ordre_presentation: <n|null>
---
```

- **`sujets`** : sommaire ciblable = titres `##`/`###` dans l'ordre ; à mettre à jour à chaque ajout/renommage/suppression d'un titre (règle 11).
- **`domaine`** : `solution` = architecture haut niveau (vue d'ensemble, cadrage, choix structurants), par opposition au détail logiciel/data/infra.
- **`sensibilite`** : confidentialité réelle ; `restreint` (menaces, GIA) jamais exposé au client.
- **Aucun secret** dans le front-matter.

### Lecture et écriture ciblées (lazy loading)

Cette skill est la **source unique** de la règle de ciblage pour les documents issus de ses gabarits : les agents qui lisent, modifient ou créent ces documents l'appliquent. Le workflow `core` reste agnostique ; si un gabarit futur porte d'autres métadonnées, **sa skill** redéfinit les champs de routage ci-dessous.

- **Champs de routage de ces gabarits** : `doc_id`, `theme`, `domaine`, `sujets` (H2/H3), `types_presentation`, `sensibilite`, `togaf_layer`.
- **Lecture / analyse.**
  1. Lister les fichiers visés et lire **uniquement leur front-matter** (jamais le corps à ce stade).
  2. Retenir les fichiers dont les champs de routage recoupent le besoin ; `sujets` désigne les sections (H2/H3) pertinentes.
  3. Ouvrir **seulement ces sections** (ou le fichier entier si le besoin couvre tout le thème). Ne jamais charger toute la documentation.
- **Modification.**
  1. Localiser le fichier et la section par le front-matter, comme pour la lecture.
  2. Ne modifier que les sections concernées.
  3. Si un titre H2/H3 est ajouté, renommé, supprimé ou déplacé, mettre à jour `sujets` **dans le même changement**.
- **Création.**
  1. Si aucun fichier ni section ne couvre le besoin, partir du gabarit correspondant (front-matter compris) ; ne pas dupliquer un thème déjà couvert.
  2. Renseigner les champs de routage (`doc_id` stable, `theme`, `domaine`, `sensibilite` réelle, `ordre_presentation`).
  3. Renseigner `sujets` avec les titres H2/H3 réellement présents, dans l'ordre.
- **Contrôle.** Le sensor `sujets-a-jour` (`core/sensors/sensors/sujets-a-jour.md`) signale à l'écriture tout `sujets` désynchronisé des titres. Il est advisory : la tenue à jour reste la responsabilité de l'agent qui écrit.

## Renvois vers l'architecture détaillée (format Structurizr)

Rendu par **Structurizr** (vue `documentation` d'un `SoftwareSystem`). Les liens Markdown par chemin de fichier **ne résolvent pas** : proscrits. Format de renvoi **unique** = lien d'ancre Structurizr :

```
documentation/<Software System>#<ancre-de-section>
```

- `<Software System>` : nom du `SoftwareSystem` du modèle (`models/`), URL-encodé (espace → `%20`).
- `<ancre-de-section>` : slug du titre visé (voir ci-dessous).
- Exemple : `documentation/Talent%20Match#api-applicatives`. Proscrit : `architecture-detaillee/talent-match/architecture-logicielle/01-....md`.

**Slug d'ancre** (déterministe, depuis le texte du titre) :

- minuscules ;
- apostrophes et guillemets retirés (`l'appariement` → `lappariement`) ;
- tout caractère non alphanumérique → `-`, tirets multiples réduits, tirets de bord retirés ;
- accents : par défaut translittérer (`é`→`e`, `à`→`a`, `ç`→`c`) ; si l'instance conserve les accents, s'aligner sur son rendu. En cas de doute, **vérifier l'ancre réellement générée** — un renvoi qui ne résout pas est un défaut.
- Exemples : « API applicatives » → `api-applicatives` ; « Cycle de vie des données » → `cycle-de-vie-des-donnees`.

**Libellé et périmètre** :

- Dans toute table/liste de renvoi, le **libellé** du lien = **nom de la section** visée, jamais un nom/chemin de fichier. Forme `[Nom de la section](documentation/<Software System>#<ancre>)`. Jamais de colonne « Fichier ».
- Un renvoi ne vise **que du contenu C4 N3 (Composants) et N4 (Code)**. Les sections du `06` dont le contenu vit en détaillé portent **le seul renvoi**, sans description ni image embarquée.
- Table « Architecture détaillée — renvois » du `06` : **volet logiciel uniquement**. Autres volets atteints via leur document de niveau solution :
  - données → `10-cycle_vie_donnees.md` ;
  - sécurité → `11-securite.md` ;
  - infrastructure → `09-deploiement.md`.

## Règles d'or

1. **Modifier dans les mêmes fichiers.** Lire, analyser, puis modifier les fichiers existants ; jamais recréer ni restructurer le découpage, les noms de fichiers ou la structure des sections.
2. **Cycle de modification.**
   - Lire et analyser les fichiers existants (contexte, décisions prises) avant toute modification.
   - Appliquer à la bonne section du bon fichier.
   - **Relecture de cohérence** (autocontrôle) avant revue : cohérence inter-fichiers, terminologie, numérotation des tableaux, références croisées, historique.
   - Toute modification est **approuvée par l'humain** en revue.
3. **Initialisation.**
   - Copier les fichiers **strictement nécessaires** de `gabarits/` dans `documentation/`, en conservant noms et front-matter. Un thème non couvert est copié tel quel.
   - **Exception — `00-checklist-architecture.md`** : fichier d'état de processus, **exclu** de la copie en lot. Copié **seulement s'il est absent** (idempotent, jamais d'écrasement), tous éléments à 0 %. Présence vérifiée par le workflow `core` en Initialization (`directory-check`) ; règles de tenue (barème 80/10/10, conformité, revue pair, acceptation) en **source unique** dans `core/common/protocols/architecture-checklist.md`.
4. **Couverture d'un patron.** Chaque décision d'architecture vérifie si elle couvre un patron de `patron-architecture/` : si oui, le référencer dans le fichier concerné et la matrice du `02` ; sinon, l'expliciter.
5. **Séparation solution ↔ détaillé (renvoi, pas duplication).** Le `06` est la vue solution (C4 N1/N2). Le contenu C4 N3/N4 (composants, séquences détaillées, défauts logiciels) vit en architecture détaillée ; le `06` porte **le seul renvoi** par ancre. Chaque fait vit à **un seul endroit**.
6. **Numérotation et index.**
   - Numérotation globale continue des tableaux + index du `001` à jour à chaque changement.
   - Index des diagrammes (`001`, Tab. 7) exhaustif : solution (`06`) **et** architectures détaillées, colonne « Fichier » pointant la vue.
   - Cette colonne « Fichier » est propre à l'index technique ; les tables de **renvoi** de navigation n'en ont jamais (renvoi par ancre, libellé = nom de section).
7. **Historique du document (`001`).** Mise à jour à chaque modification (version, date, statut, motif, auteur, approbateur). Colonne « Description / Motif » :
   - **une ligne factuelle** : objet + identifiant de traçabilité (`ORIG-xxx`/`ADR-xxxx`) + fichier(s) touché(s) ; pas de prose ni d'énumérations détaillées.
   - zéro doublon ; traçabilité (IDs) préservée.
   - **une ligne = un livrable accepté** : un lot en revue met à jour **la même ligne** (statut `Revue en cours`) ; nouvelle ligne seulement pour un nouveau lot.
   - Statut : à chaque mise à jour, la dernière version passe `Revue en cours`, les précédentes `Revue` ; `Approuvé` seulement après validation humaine explicite.
8. **Identifiants codés** cohérents (`RISQ-001`, `UC-001`, `CT-001`).
9. **Diagrammes.**
   - Générés **en code** (PlantUML, Mermaid, Structurizr, BPMN, C4), validés (DSL), indexés dans le `001` (Tab. 7).
   - Embarqués via Structurizr : vue `image` + kroki + référence `embed:` (`![…](embed:<clé>)`). Proscrire l'inclusion directe d'un fichier image/source. Renderer kroki selon le type ; réutiliser le thème projet (`theme/`) s'il existe.
   - **Le modèle C4/Structurizr est la source de vérité du détaillé** : conteneurs et composants modélisés comme éléments de 1er ordre dans `models/`/`views/` ; la DAS le reflète. C'est un travail de modélisation, pas un déplacement de prose.
10. **ADR.** Chaque décision d'architecture est tracée en ADR (skill `create-architecture-decision-record`) et référencée dans les fichiers concernés.
11. **Front-matter de ciblage maintenu à jour.** Cohérent avec le contenu ; `sujets` reflète les titres `##`/`###` dans l'ordre, mis à jour dans le même changement qu'un ajout/renommage/suppression ; jamais de secret ; `sensibilite` réelle. Contrôlé par le sensor `sujets-a-jour` ; protocole de lecture/écriture ciblées : section « Front-matter de ciblage ».
12. **Aucun secret** (mot de passe, identifiant) dans la documentation.
13. **Architecture détaillée sous `architecture-detaillee/<software_system>/`**, en quatre sous-répertoires dans cet **ordre non négociable** :
    - `architecture-logicielle/` · `architecture-infra/` · `architecture-donnees/` · `architecture-securite/`.
    - Numérotation séquentielle libre par sous-répertoire ; l'index du `001` assure la correspondance.
    - **Page d'entrée `00` obligatoire** par dossier (modèle `00-architecture-detaillee.md`) : Portée et objectifs, Socle de conception, Table du chapitre ; sans « Synthèse exécutive » ; tableaux non numérotés ; table du chapitre par ancre (libellé = nom de section, sans colonne « Fichier »).
    - Titres : page `00` en `h2` (`## Architecture logicielle détaillée`), sous-sections en `###` ; **pas de préfixe** de volet ni de **suffixe** de nom de système dans les titres des fichiers de contenu.
14. **Table des conteneurs = pont unique solution ↔ détaillé** (`06`, Tab. 23) :
    - une ligne par **conteneur de 1er rang** ; composants C4 sous la ligne de leur conteneur, référencés par `SYS-xxx` ; vérifier la complétude.
    - nom d'un conteneur avec doc détaillée = lien par **ancre Structurizr** ; jamais de chemin de fichier ni de colonne « Fichier ».
    - **chapeau de lecture** avant la table ; pas de table-sommaire séparée.
    - section compacte « Architecture détaillée — renvois » sous la table = **volet logiciel uniquement** ; données/sécurité/infrastructure atteints via `10`/`11`/`09`. Aucun document détaillé orphelin de navigation.
15. **Aucune note de génération dans la documentation.** Un livrable ne contient **que** du contenu pertinent au projet. Interdit : mentions de méta-génération (« généré avec… », outil, agent, horodatage), description du procédé de fabrication, commentaire de processus (corps, note, commentaire masqué). Les retirer avant livraison.
16. **Aucune référence de commit ni de tâche de suivi** (SHA, `ORIG-NNN`, `mention://issue`, numéros de tickets) dans la DAS **comme dans les ADR** : retirer et neutraliser les liens en texte simple, sans changement sémantique. **Conservés** : tags de version (`v2.10.0`) et références OpenSpec (`REF-04`…).
17. **`16-questions-decisions.md` toujours en dernier.** Un seul fichier, deux sections (*Questions en attente*, *Décisions attendues*), chacune par domaine (*Logiciel*, *Sécurité*, *Données*, *Infrastructure*). Précédé d'une section « Invariants hérités » rappelant les invariants non contournables (gouvernance, plancher sécurité, ADR acceptés — source `core/common/protocols/governance-security.md`) : aucune question ni décision ne peut les affaiblir ; en tension, l'invariant prime et l'humain arbitre. Porte toujours le numéro le plus élevé : un nouveau fichier DAS le fait renommer (ex. `17-…`), avec mise à jour de `ordre_presentation` et des références. Identifiants `INV-NNN`, `Q-NNN`, `DEC-NNN` ; une question tranchée est close avec renvoi, une décision tranchée devient un ADR référencé.
18. **Feuille de route sans date → J + 7 jours** à compter du jour.

## Arrimage avec les autres skills

- `create-architecture-decision-record` : chaque décision d'architecture donne un ADR référencé dans les fichiers concernés.
- `presentation-targeting` : consomme le front-matter de ciblage (`theme`, `domaine`, `types_presentation`, `sensibilite`, `sujets`) ; garder ce front-matter à jour (règle 11).
- `09`, `12`, `14` rédigés avec les architectes infrastructure, cloud, sécurité, DevOps ; `13` avec le leader Assurance Qualité.
