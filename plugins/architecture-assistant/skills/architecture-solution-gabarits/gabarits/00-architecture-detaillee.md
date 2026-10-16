---
doc_id: das-00-architecture-detaillee
theme: Page d'entrée d'un dossier d'architecture détaillée — portée, socle de conception, table du chapitre
domaine: [logiciel]
sujets:
  - Architecture détaillée
  - Portée et objectifs
  - Socle de conception
  - Table du chapitre
types_presentation: [technique]
sensibilite: interne
togaf_layer: application
ordre_presentation: 0
---
<!--
**Gabarit réutilisable — page d'entrée `00` d'un dossier d'architecture détaillée.**
Copier ce gabarit dans **chaque** sous-répertoire d'architecture détaillée d'un système :
`architecture-detaillee/<software_system>/architecture-logicielle/00-…`, `…/architecture-infra/00-…`,
`…/architecture-donnees/00-…`, `…/architecture-securite/00-…` (ordre NON NÉGOCIABLE des sous-répertoires, règle d'or 16).
Il est **calqué** sur `00-analyse-securite.md` de la skill `architecture-securite-gabarits`, mais **sans** section « Synthèse exécutive » (règle d'or 16).

**Conventions de titres (règle d'or 16) — à respecter sans exception :**
  - Titre de cette page `00` au niveau **`h2` (`##`)** ; adapter le libellé au volet du dossier
    (ex. `## Architecture logicielle détaillée`, `## Architecture infrastructure détaillée`,
    `## Architecture de données détaillée`). Les sous-sections démarrent en `###`.
  - **Pas de préfixe** `Architecture … détaillée — …` dans les titres des **fichiers de contenu** (`01`, `02`, …) du dossier : le titre porte le **sujet** (ex. `## Vue d'ensemble des composants`).
  - **Pas de suffixe** de nom de système dans les titres (proscrire `… (SYS-001 Talent Match)`) : l'appartenance au système est portée par l'arborescence et le modèle.

**Renvois (règle d'or 17 + « Renvois vers l'architecture détaillée (format Structurizr) ») :** la table du chapitre renvoie par **ancre Structurizr** `documentation/<Software System>#<ancre>`, **libellé = nom de la section**, **sans** colonne « Fichier ». Les **tableaux de cette page `00` ne sont pas numérotés** (navigation locale, hors index global Tab. 8 du `001`).

Ce dossier est l'**approfondissement** de la vue solution haut niveau (`06-architecture-solutions.md`) ; renvoyer vers elle, ne pas la dupliquer. Les identifiants (`SYS-xxx`, `DEF-xxx`, `SC-xxx`, `API-xxx`) restent harmonisés avec le `06` et le reste de la DAS.
-->
## Architecture détaillée

<!-- Adapter le libellé du titre `h2` au volet du dossier (logicielle / infrastructure / données / sécurité). -->

### Portée et objectifs

<!--
Décrire :
  - le **périmètre** couvert par ce dossier d'architecture détaillée (quel système / conteneur, quel volet), en renvoi vers la vue solution (`06-architecture-solutions.md`) et, selon le volet, vers `09-deploiement.md` / `10-cycle_vie_donnees.md` / `11-securite.md` ;
  - les **objectifs** de ce niveau de détail (descendre au niveau composant C4 N3/N4 : composants, contrats internes, séquences au niveau composant, défauts détaillés) ;
  - ce qui est **hors périmètre** (explicite), notamment ce qui reste au niveau solution dans le `06`.
-->

### Socle de conception

<!--
Rappeler le **socle de conception** qui borne ce dossier : invariants hérités et décisions socle applicables (ADR acceptés, `16-questions-decisions.md` § « Invariants hérités »), patrons d'architecture retenus (`patron-architecture/`, matrice de suivi du `02-objectifs.md`), contraintes technologiques pertinentes (`08-contraintes.md`), et la **source de vérité** : le modèle C4/Structurizr (`models/`, `views/`). Ne lister ici que ce qui **encadre effectivement** la conception détaillée de ce volet ; ne pas redécrire les décisions, y renvoyer.
-->

### Table du chapitre

<!--
Table de navigation du dossier. Conserver l'ordre et les noms de fichiers du dossier.
Le **Sujet** est un **lien par ancre Structurizr** dont le **libellé est le nom de la section** visée (jamais un nom de fichier) ; **aucune** colonne « Fichier ». Tableau **non numéroté**.
-->

| Sujet | Contenu |
| ----- | ------- |
| [Vue d'ensemble des composants](documentation/Software%20System%201#vue-ensemble-des-composants) | Composants C4 (N3) du conteneur, responsabilités, contrats internes |
| [Scénarios d'exécution détaillés](documentation/Software%20System%201#scenarios-dexecution-detailles) | Séquences au niveau composant (SC-xxx), enchaînements internes |
| [Défauts détaillés](documentation/Software%20System%201#defauts-detailles) | Défauts de ce volet, impacts, recommandations |

**Tableau. Table du chapitre d'architecture détaillée**
