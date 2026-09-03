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

## Quand utiliser

- Créer la documentation d'architecture de solution et d'intégration d'un nouveau projet.
- Mettre à jour la documentation d'architecture d'un projet existant suite à de nouvelles exigences.

## Règles d'or

1. **Toujours modifier dans les mêmes fichiers.** La documentation d'architecture d'un projet est découpée dans des fichiers fixes. Toute modification se fait en **lisant, analysant puis modifiant les fichiers existants** — jamais en recréant ou en restructurant le découpage.
2. **Vérifier la couverture d'un patron.** Chaque décision d'architecture (choix de solution, de technologie, de structure d'intégration) doit **vérifier si elle couvre un patron** du répertoire `patron-architecture/` de cette skill. Si oui, référencer la fiche du patron (ex. `patron-architecture/circuit-breaker.md`) dans le fichier concerné et dans la matrice de suivi du `02` ; si aucun patron ne couvre la décision, l'expliciter.
3. **Initialisation** : copier **l'ensemble** des fichiers de `gabarits/` dans le répertoire `documentation/` du projet, en conservant les noms de fichiers. Si un thème n'est pas couvert pour l'instant, le gabarit est simplement copié tel quel.
4. **Modification** :
   - Lire et analyser les fichiers existants (contexte global, décisions déjà prises) avant toute modification.
   - Appliquer les modifications selon les nouvelles exigences, à la bonne section du bon fichier.
   - Effectuer une **relecture de cohérence** (autocontrôle) des modifications avant toute revue : cohérence entre fichiers, terminologie, numérotation des tableaux, références croisées, historique.
   - Toute modification doit être **approuvée par l'humain** lors de la phase de revue.
5. Conserver le découpage des fichiers, les noms de fichiers et la structure des sections.
6. Maintenir la **numérotation globale et continue** des tableaux ainsi que l'index du fichier `001` (liste des tableaux et des diagrammes) à chaque changement.
7. Mettre à jour l'**historique du document** (`001`) à chaque modification (version, date, statut, motif, auteur, approbateur).
8. Utiliser des **identifiants codés** cohérents pour les articles (ex. `RISQ-001`, `UC-001`, `CT-001`).
9. Les diagrammes sont générés en **code** (PlantUML, Mermaid, Structurizr, BPMN, C4) et référencés dans l'index du `001`.
10. Les **décisions d'architecture** sont tracées dans des ADR (voir la skill `create-architectural-decision-record`) et référencées dans les fichiers concernés.
11. Ne jamais inclure de secrets, mots de passe ou identifiants dans la documentation.

## Arrimage avec les autres skills

- `create-architectural-decision-record` : chaque décision d'architecture (choix de solution, patron, technologie) fait l'objet d'un ADR référencé dans les fichiers concernés.
- Les fichiers `09`, `12`, `14` sont rédigés en collaboration avec les architectes infrastructure, cloud, sécurité et DevOps ; `13` en arrimage avec le leader Assurance Qualité.
