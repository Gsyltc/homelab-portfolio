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
| `06-architecture-solutions.md`       | Architectures de solution, diagrammes, acteurs, systèmes, défauts d'architecture |
| `07-choix-des-solutions.md`          | Solutions étudiées et choix |
| `08-contraintes.md`                  | Lois, conformités, contraintes technologiques |
| `09-deploiement.md`                  | Implantation, environnement, déploiement, DevSecOps |
| `10-cycle_vie_donnees.md`            | Cycle de vie des données |
| `11-securite.md`                     | Sécurité |
| `12-volumetries.md`                  | Volumétrie |
| `13-plan-qualite.md`                 | Plan de qualité |
| `14-preventions-et-resilience.md`    | Prévention, reprise après sinistre, résilience |
| `15-concepts-transverses.md`         | Concepts transverses (communication, erreurs, transactions, cache, persistance, observabilité, configuration, accessibilité) |

## Front-matter de ciblage

Chaque gabarit de la DAS (`001`, `01`–`15`) porte en tête un **front-matter YAML** (délimité par `---`), non intrusif (ignoré au rendu Markdown) et placé **avant** le contenu. Il permet à la skill `presentation-targeting` de **localiser l'information à présenter sans lecture exhaustive** du corps. Le front-matter est copié avec le gabarit à l'initialisation (règle d'or 3) puis maintenu à jour (règles d'or 12 et 13).

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
6. Maintenir la **numérotation globale et continue** des tableaux ainsi que l'index du fichier `001` (liste des tableaux et des diagrammes) à chaque changement.
7. Mettre à jour l'**historique du document** (`001`) à chaque modification (version, date, statut, motif, auteur, approbateur). La **description / motif du changement** reste **concise** et limitée à l'essentiel (une à deux lignes factuelles, sans prose superflue).
8. Utiliser des **identifiants codés** cohérents pour les articles (ex. `RISQ-001`, `UC-001`, `CT-001`).
9. Les diagrammes sont générés en **code** (PlantUML, Mermaid, Structurizr, BPMN, C4) et référencés dans l'index du `001`. Ils **réutilisent le thème du projet** (répertoire `theme/`, p. ex. `theme/0000-default-styles.dsl`) **lorsqu'il est disponible** ; ne pas réinventer ni approximer un style quand le thème existe.
10. Les **décisions d'architecture** sont tracées dans des ADR (voir la skill `create-architectural-decision-record`) et référencées dans les fichiers concernés.
11. Ne jamais inclure de secrets, mots de passe ou identifiants dans la documentation.
12. **Front-matter de ciblage maintenu à jour.** Chaque fichier de la DAS (`001`, `01`–`15`) porte en tête un **front-matter YAML de ciblage** (voir « Front-matter de ciblage ») consommé par la skill `presentation-targeting`. Le maintenir cohérent avec le contenu : **jamais de secret** dans le front-matter, et une **sensibilité réelle** (`sensibilite`) reflétant la confidentialité effective des sections (`restreint` n'est jamais exposé au client).
13. **Maintenance du champ `sujets`.** Le champ `sujets` du front-matter reflète les **titres de niveau 2 (`##`) et niveau 3 (`###`)** du document, dans l'ordre du document. Dès qu'un titre H2/H3 est **ajouté, renommé ou supprimé**, mettre à jour `sujets` dans le même changement pour qu'il reste le reflet fidèle de la structure ciblable.
14. **Aucune information de génération dans la documentation.** Un document livré ne contient que ce qui concerne le projet (architecture, décisions, exigences, etc.). Proscrire toute mention de méta-génération — p. ex. « diagramme généré avec … », « document produit par … », notes d'outil ou horodatage de génération.
15. **Feuille de route sans date → J+7.** Pour toute feuille de route / timeline / roadmap, si aucune date n'est indiquée, considérer le début à **J + 7 jours à compter de la date du jour**.

## Arrimage avec les autres skills

- `create-architectural-decision-record` : chaque décision d'architecture (choix de solution, patron, technologie) fait l'objet d'un ADR référencé dans les fichiers concernés.
- `presentation-targeting` : consomme le **front-matter de ciblage** de chaque fichier de la DAS (`theme`, `domaine`, `types_presentation`, `sensibilite` et surtout `sujets` = titres H2/H3) pour localiser l'information à présenter sans lecture exhaustive. Garder ce front-matter à jour (règles d'or 12 et 13) pour que le ciblage reste fiable.
- Les fichiers `09`, `12`, `14` sont rédigés en collaboration avec les architectes infrastructure, cloud, sécurité et DevOps ; `13` en arrimage avec le leader Assurance Qualité.
