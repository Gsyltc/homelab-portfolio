---
name: architecture-securite-gabarits
description: Gabarits de documentation d'architecture de sécurité (approfondissement du dossier documentation/architecture-securite/ d'un projet), découpés en fichiers Markdown à préfixe numérique à conserver. Porte deux jeux de gabarits — production (00→06), produit par l'Architecte cybersécurité, et revue (revue/revue-securite.md), produit par le Reviewer de sécurité (review-only). Utiliser pour créer ou mettre à jour le chapitre de sécurité détaillé d'un projet, en modifiant toujours les mêmes fichiers.
---

# Gabarits de documentation d'architecture de sécurité

Gabarits communs pour le **dossier de sécurité détaillé** d'un projet, placé dans `documentation/architecture-securite/`. La documentation est **découpée en plusieurs fichiers Markdown à préfixe numérique, un par thème** ; **conserver ce découpage, ces noms de fichiers et la structure des sections**. Ce dossier est l'**approfondissement** de la synthèse portée par `11-securite.md` de la DAS (skill `architecture-solution-gabarits`) — il ne la duplique pas.

Cette skill porte **deux jeux de gabarits** :

| Jeu | Répertoire | Produit par | Nature |
|---|---|---|---|
| **A — Production** | `gabarits/` (`00`→`06`) | **Architecte cybersécurité** | Documentation d'architecture de sécurité |
| **B — Revue** | `revue/` (`revue-securite.md`) | **Reviewer de sécurité** | Verdict de revue (review-only, aucune architecture produite) |

## Contenu des gabarits — Jeu A (production, `gabarits/`)

| Fichier | Thème |
|---|---|
| `00-analyse-securite.md` | Portée, socle normatif, triangle CIA, table du chapitre (renvois par ancre Structurizr). **Pas de « Synthèse exécutive »** (voir règle d'or 11) |
| `01-surfaces-et-actifs.md` | Acteurs / identités, actifs classés CIA, frontières de confiance, surfaces d'attaque (`S1…Sn`) |
| `02-menaces-stride.md` | Matrice de synthèse STRIDE par surface + analyse détaillée par surface |
| `03-risques-owasp.md` | Table OWASP Top 10 + fiche par risque (`A01…A10`) croisée avec les surfaces |
| `04-identites-humaines-vs-agents.md` | Invariant de séparation des identités humaines et des charges d'agents |
| `05-gates-guardrails-escalade.md` | Analyse de la gouvernance (gates / guardrails / escalade) sous l'angle STRIDE / OWASP |
| `06-recommandations-priorisees.md` | Recommandations consolidées, priorisées (`P1`/`P2`/`P3`), à ID stable, sourcées |

## Contenu des gabarits — Jeu B (revue, `revue/`)

| Fichier | Thème |
|---|---|
| `revue-securite.md` | Grille de revue STRIDE / OWASP, constats à sévérité, verdict motivé, rappel du plancher SG-3 |

## Front-matter de ciblage

Chaque gabarit de production (`00`–`06`) porte en tête un **front-matter YAML** (délimité par `---`), non intrusif (ignoré au rendu Markdown) et placé **avant** le contenu, homogène avec celui des gabarits de `architecture-solution-gabarits` (`11-securite.md`). Il permet à la skill `presentation-targeting` de **localiser l'information sans lecture exhaustive** du corps.

```yaml
---
doc_id: <id-stable>                       # ex. secu-02-menaces-stride
theme: <thème principal>                  # ex. Menaces (STRIDE) par surface
domaine: [securite]                       # toujours securite pour ce dossier
sujets: [<titres H2 et H3>]               # = titres ## et ### du document, dans l'ordre ; maj quand les titres changent
types_presentation: [securite]            # securite (compléter si une section vise un autre public)
sensibilite: restreint                    # dossier sécurité : restreint par défaut (jamais exposé au client)
togaf_layer: <business|data|application|technology|null>
ordre_presentation: <n|null>              # = préfixe numérique du fichier (0→6)
---
```

- **`sujets`** est le **sommaire ciblable** : la liste des intitulés H2 (`##`) et H3 (`###`), dans l'ordre du document. Le maintenir à jour à chaque ajout / renommage / suppression d'un titre H2/H3.
- **`domaine`** vaut `[securite]` pour tout le dossier.
- **`sensibilite`** vaut `restreint` par défaut (modélisation des menaces, surfaces, identités) et **n'est jamais exposé au client**.
- **Aucun secret** ne figure dans le front-matter.

> Le gabarit de **revue** (`revue/revue-securite.md`) ne porte **pas** de front-matter de ciblage : ce n'est pas un livrable d'architecture présentable, c'est un verdict de contrôle.

## Renvois vers l'architecture détaillée (format Structurizr)

> Reporté de la skill `architecture-solution-gabarits` (§ « Renvois vers l'architecture détaillée (format Structurizr) »), **adapté à la sécurité** — fichier de synthèse de référence : `11-securite.md` de la DAS.

La documentation est rendue par **Structurizr**. Les **liens Markdown par chemin de fichier** (`../architecture-securite/….md`, `../../documentation/….md`) **ne résolvent pas** dans ce rendu : ils sont **proscrits** comme renvois de navigation. Le format de renvoi **unique** vers une section est le **lien d'ancre Structurizr** :

```
documentation/<Software System>#<ancre-de-section>
```

- `<Software System>` = **nom** du `SoftwareSystem` dans le modèle (`models/`), **URL-encodé** (espace → `%20`). Ex. : `documentation/Talent%20Match`.
- `<ancre-de-section>` = **slug** du titre visé (voir « Règle de slug d'ancre »).
- Exemple attendu : `documentation/Talent%20Match#surfaces-dattaque`. Contre-exemple **proscrit** : `architecture-securite/01-surfaces-et-actifs.md`.

### Règle de slug d'ancre

Le slug dérive du **texte du titre**, de façon déterministe : (1) **minuscules** ; (2) **apostrophes / guillemets retirés** ; (3) tout caractère non alphanumérique → **tiret** `-`, tirets multiples réduits à un, tirets de début/fin retirés ; (4) **accents** : **translittération** par défaut (`é`→`e`, `à`→`a`, `ç`→`c`…), car plusieurs instances translittèrent avant de slugifier — si l'instance cible **conserve** les accents, aligner le slug sur son rendu réel. **En cas de doute, vérifier l'ancre effectivement générée** avant de figer le renvoi.

Exemples : « Surfaces d'attaque » → `surfaces-dattaque` ; « Menaces (STRIDE) par surface » → `menaces-stride-par-surface`.

### Libellé du lien = nom de la section

Dans **toute** table ou liste de renvoi (table du chapitre du `00`, renvois croisés entre fichiers, renvoi vers / depuis `11-securite.md`), le **libellé** du lien est le **nom de la section** visée (texte du titre), **jamais** un nom ni un chemin de fichier. Forme : `[Nom de la section](documentation/<Software System>#<ancre>)`. **Ne pas** ajouter de colonne « Fichier » : côté Structurizr, la donnée de navigation est l'**ancre**, pas le fichier.

### Séparation `11-securite.md` ↔ dossier détaillé (renvoi, pas duplication) — adaptation sécurité des points 3 & 4

- **`11-securite.md`** (DAS) est la **synthèse de sécurité de niveau solution** : posture, vulnérabilités de synthèse, GIA de haut niveau. Le **dossier `architecture-securite/`** (cette skill) en est l'**approfondissement** (surfaces, STRIDE, OWASP, identités, gouvernance, recommandations).
- Le contenu de **niveau détaillé** (matrices STRIDE par surface, fiches OWASP, analyse de gouvernance) vit **dans le dossier détaillé** ; `11-securite.md` porte la **synthèse** et **renvoie** par ancre Structurizr — **sans** dupliquer les matrices ni embarquer les tableaux détaillés. Réciproquement, le dossier détaillé renvoie vers `11-securite.md` pour la synthèse de niveau solution plutôt que de la recopier.
- **Périmètre d'une table de renvoi de ce dossier** : elle ne liste **que** les renvois de l'**architecture de sécurité détaillée** (le volet porté par `11-securite.md`). Les autres volets détaillés (logiciel, données, infrastructure) s'atteignent via leurs documents de niveau solution respectifs (`06-architecture-solutions.md`, `10-cycle_vie_donnees.md`, `09-deploiement.md`), pas depuis une table de ce dossier. Aucun fichier du dossier ne doit être **orphelin** de la navigation (atteignable par la table du chapitre du `00` ou un renvoi croisé).
- **Échelles et codes** (`VUL-xxx` / `RISQ-xxx`, échelle `Faible…Critique`) restent **harmonisés** avec `04-risques.md` et `11-securite.md` : harmoniser par **renvoi**, jamais par copie.

## Quand utiliser

- **Architecte cybersécurité** — pour **produire** le dossier de sécurité détaillé d'un projet : copier l'ensemble des fichiers de `gabarits/` dans `documentation/architecture-securite/` du projet (front-matter compris), puis remplir chaque section. L'analyse elle-même (STRIDE, OWASP, activation conditionnelle des normes) relève de la skill `cybersecurite`.
- **Reviewer de sécurité** — pour **structurer un verdict** de revue de sécurité à partir de `revue/revue-securite.md`. Ce gabarit ne produit **aucune** architecture : il structure uniquement le verdict (review-only), conformément au plancher SG-3.

## Conventions à figer (toute la skill)

- **IDs stables** : surfaces `S1…Sn` ; risques OWASP `A01…A10` ; lignes de risque consolidées `R01…` ; recommandations `R-11A-*` (applicatif) / `R-11B-*` (infrastructure) ou préfixe projet équivalent, **stables dans le temps** ; vulnérabilités `VUL-xxx` (en renvoi vers la DAS, sans duplication).
- **Échelle commune** : `Faible` / `Moyen` / `Élevé` / `Critique` pour la probabilité (vraisemblance) comme pour l'impact, **harmonisée** avec le `04-risques.md` de la DAS.
- **Risque résiduel** : exprimé comme `P × I` (probabilité × impact), après contre-mesures.
- **Liens ADR relatifs** : renvois vers les décisions sous la forme `../../decisions/NNNN-....md`.
- **Renvois croisés** entre fichiers du chapitre (ex. une surface `S3` du `01` citée dans la matrice STRIDE du `02`, un risque OWASP du `03` lié à une recommandation du `06`) : **lier, ne pas dupliquer**. Les renvois **de navigation** (table du chapitre du `00`, renvois vers / depuis `11-securite.md`) utilisent le **format d'ancre Structurizr** (`documentation/<Software System>#<ancre>`), libellé = nom de section, **pas** de chemin de fichier ni de colonne « Fichier » — voir « Renvois vers l'architecture détaillée (format Structurizr) ».

## Règles d'or

1. **Conserver le découpage, les noms de fichiers et la structure des sections.** Toute mise à jour se fait en **lisant, analysant puis modifiant les fichiers existants** — jamais en recréant ou en restructurant le découpage.
2. **Initialisation** : copier **l'ensemble** des fichiers de `gabarits/` dans `documentation/architecture-securite/` du projet, en conservant les noms de fichiers **et le front-matter YAML de ciblage**. Un thème non couvert pour l'instant est copié tel quel.
3. **Socle normatif — OWASP + STRIDE toujours actifs.** Toute analyse de sécurité s'appuie **par défaut** sur OWASP Top 10 et STRIDE. Les autres normes (COBIT, NIST, PCI DSS, GDPR, Loi 25, LPRPDE) ne sont activées **que sur activation humaine explicite** (ou du coordinateur) — voir les règles d'activation de la skill `cybersecurite`. **Ne jamais décider seul** d'appliquer une norme non demandée.
4. **IDs, échelles, liens figés** : respecter les conventions ci-dessus (IDs stables, échelle `Faible…Critique`, risque résiduel `P × I`, liens ADR relatifs, renvois croisés sans duplication).
5. **Front-matter de ciblage maintenu à jour.** Le champ `sujets` reflète les titres H2/H3 dans l'ordre ; le mettre à jour dans le même changement qu'un ajout / renommage / suppression de titre. Jamais de secret dans le front-matter ; `sensibilite` reflète la confidentialité réelle (`restreint` pour ce dossier).
6. **Aucun secret** (mot de passe, jeton, clé, identifiant) ne figure dans la documentation ni dans le front-matter.
7. **Décisions tracées en ADR** : chaque décision d'architecture de sécurité est tracée dans un ADR (skill `create-architectural-decision-record`) et référencée par un lien relatif `../../decisions/NNNN-....md`.
8. **La revue est review-only** : le gabarit `revue/revue-securite.md` ne produit aucune architecture ; il structure un verdict. Il respecte le plancher SG-3 (revue obligatoire et non substituable, précédant la validation humaine granulaire).
9. **Validation humaine** : toute production ou modification est soumise à la revue de sécurité puis à la validation humaine granulaire avant d'être considérée comme acceptée.
10. **Renvois au format Structurizr (report point 1 & 2).** Les renvois de navigation (table du chapitre du `00`, renvois croisés de navigation, renvois vers / depuis `11-securite.md`) utilisent le format d'**ancre Structurizr** `documentation/<Software System>#<ancre>` avec **libellé = nom de section** ; la forme « chemin de fichier » et toute colonne « Fichier » sont **proscrites** (voir « Renvois vers l'architecture détaillée (format Structurizr) » et sa règle de slug d'ancre). *Les liens ADR relatifs `../../decisions/NNNN-….md` ne sont pas des renvois de navigation d'architecture détaillée et restent inchangés.*
11. **Page d'entrée `00` sans « Synthèse exécutive » (report point 6).** Le `00-analyse-securite.md` est la **page d'entrée** du dossier : sections **Portée et objectifs**, **Socle normatif**, **Triangle CIA**, **Table du chapitre** — **sans** section « Synthèse exécutive » (la posture et les priorités sont portées par `06-recommandations-priorisees.md` et la synthèse de `11-securite.md`, atteints par renvoi). Titre de la page `00` en **`h2`** (`## Analyse de sécurité`).
12. **Historique consolidé — une ligne = un livrable accepté (report point 8).** Lorsque la livraison du dossier de sécurité est consignée dans l'historique du `001` de la DAS, appliquer la politique de consolidation de la skill `architecture-solution-gabarits` (règle d'or 7) : **une seule ligne de version par lot de travail** (ex. « production du dossier d'architecture de sécurité ») décrivant le **livrable**, pas une ligne par micro-correction ; les itérations de revue mettent à jour **la même ligne** (motif consolidé, date réactualisée) tant que le lot est `Revue en cours`. Toute histoire/journal interne au dossier suit la même granularité.
13. **Aucune information de génération dans la documentation (report de la règle d'or 14 de `architecture-solution-gabarits`).** Un document de sécurité livré ne contient **QUE** ce qui est pertinent pour le projet (surfaces, menaces, risques, recommandations, etc.). Il est **interdit** d'ajouter des notes liées à la **génération** ou à la **façon dont a été créé** un diagramme ou un élément du dossier. Proscrire notamment :
    - toute mention de **méta-génération** — p. ex. « diagramme généré avec … », « document produit par … », notes d'outil, d'agent ou horodatage de génération ;
    - toute note décrivant **comment** un diagramme, une matrice (STRIDE, OWASP) ou une section a été construit, modélisé ou dérivé (procédé de fabrication, outil employé, étapes de production) ;
    - tout commentaire de processus de rédaction ou de génération, qu'il soit dans le corps, en note de bas de page ou en commentaire masqué.
    Ces informations relèvent du **processus**, pas du contenu d'architecture : les retirer avant livraison. En cas de doute, appliquer le critère « **QUE des informations pertinentes au projet** ».

## Arrimage avec les autres skills (éviter tout chevauchement)

- **`cybersecurite`** — porte l'**analyse** : méthode STRIDE / OWASP, règles d'activation conditionnelle des normes, principes fondamentaux. `architecture-securite-gabarits` n'héberge **que le format** (découpage, sections, tableaux, front-matter) ; elle ne redéfinit pas la méthode d'analyse.
- **`architecture-solution-gabarits`** — `11-securite.md` reste la **synthèse courte** du corps de la DAS. Le dossier `architecture-securite/` produit avec la présente skill en est l'**approfondissement** : renvoi croisé entre les deux, **jamais de duplication**. Les échelles (vraisemblance / niveau de risque) et les codes `VUL-xxx` / `RISQ-xxx` restent harmonisés avec la DAS (`04-risques.md`, `11-securite.md`).
- **`create-architectural-decision-record`** — les décisions de sécurité sont tracées en ADR et référencées depuis les gabarits par liens relatifs vers `../../decisions/`.
- **`presentation-targeting`** — consomme le front-matter de ciblage (`theme`, `domaine`, `types_presentation`, `sensibilite`, `sujets`) des gabarits de production pour localiser l'information sans lecture exhaustive. Garder ce front-matter à jour (règle d'or 5).

Base directory for this skill: the workspace skills directory (managed by `multica skill`). Relative paths in this skill (e.g. `gabarits/`, `revue/`) are relative to this base directory. Les liens `../../decisions/` et `../architecture-solution-gabarits/...` sont relatifs à l'emplacement du dossier **produit** dans le projet (`documentation/architecture-securite/`).
