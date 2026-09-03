## Implantation et déploiement

> Cette section décrit la façon dont la solution sera **implantée dans son écosystème**, ainsi que son **déploiement** et sa **surveillance**. Elle est rédigée en collaboration avec les architectes infrastructure, cloud, sécurité et DevOps.

### Implantation de la solution

> Décrire l'écosystème de la solution. Il est possible d'ajouter des schémas d'implantation et de répartition afin de décrire l'environnement. Les décisions d'implantation sont tracées dans des ADR et vérifient la couverture d'un patron du répertoire `patron-architecture/`.

![Exemple de diagramme d'implantation](embed:implantation)

### Description de l'environnement

#### Implantation du système

> Décrire l'environnement de la solution. Il est également possible d'utiliser Structurizr et ses vues/perspectives orientées infrastructure.

| ID | Services | Description | Commentaires |
|----|----------|-------------|--------------|
| INF-001 | Amazon AWS | Service de stockage Objet | Utilisé pour ... |

**Tableau 45. Liste des systèmes infrastructure**

#### Coûts récurrents (licences et hébergement)

> Tableau **consolidé** des coûts récurrents (licences + hébergement) : c'est ici la **source de vérité** des coûts récurrents. `05-planification.md` et `07-choix-des-solutions.md` y référencent. **Aucun secret** (clés, mots de passe, identifiants) ne doit figurer dans ce tableau.

| ID | Type | Description | Coût |
|----|------|-------------|------|
| LIC-001 | Licence | Licence A (3 ans) | $ 00.00 |
| HEB-001 | Hébergement | Ex. Networking — Application Gateway, Canada East : Basic V1 tier, Small Instance size : 1 Gateway hours instance(s) × 730 Hours, 50 GB Data processed unit(s), 5 GB Zone unit(s) | $ 20,84 / mois |

**Tableau 46. Coûts récurrents (licences et hébergement) — source de vérité**

#### Environnements

> Un tableau par environnement (développement, QA, recette/staging, production) : finalité, infrastructure en code (IaC), stratégie de sauvegarde. **Aucun secret** (URLs internes sensibles, identifiants, clés) ne doit figurer dans cette documentation.

| ID | Environnement | Finalité | Infrastructure (IaC) | Stratégie de sauvegarde |
|----|---------------|----------|----------------------|-------------------------|
| ENV-001 | Développement | | | |
| ENV-002 | Assurance qualité (QA) | | | |
| ENV-003 | Recette / staging | | | |
| ENV-004 | Production | | | |

**Tableau 47. Environnements**

#### Répartition des zones réseaux

> Décrire l'environnement de répartition des zones réseaux et les flux entre zones.

![exemple_network](embed:network)

### Plan de déploiement de la solution

> Décrire le plan de déploiement : mise en production, stratégie de déploiement, stratégie de validation et de **rollback** (en arrimage avec `14-preventions-et-resilience.md`).

#### Planification et mise en production

> Planifier la mise en production de l'application (jalons reliés à la feuille de route du `05-planification.md`).

#### Création de version

> Décrire le processus de création d'une version de l'application (versionnement sémantique, branches, artefacts).

#### Critères d'acceptation

> Décrire l'ensemble des critères d'acceptation définis par le client, cohérents avec les critères d'acceptation du `03-besoins_affaires_exigences.md` et le plan de qualité (`13-plan-qualite.md`).

#### Stratégie de déploiement

> Décrire la stratégie de déploiement retenue (ex. **blue/green**, **canary**, **rolling**) et les raisons du choix (tracées dans un ADR).

#### Procédure de rollback

> Décrire la procédure de retour arrière en cas d'échec de déploiement (en arrimage avec `14-preventions-et-resilience.md`).

#### Fenêtre de maintenance

> Décrire les fenêtres de maintenance prévues (fréquence, créneaux, préavis, impacts sur la disponibilité).

#### Validation post-déploiement (smoke tests)

> Décrire les validations post-déploiement : smoke tests, vérifications fonctionnelles et de surveillance après mise en production.

#### Préparation du déploiement

> Décrire les étapes préalables au déploiement de toute version en production (prérequis, validations, gel).

#### Runbook

> Décrire les procédures d'exploitation (runbooks) : démarrage/arrêt, incidents courants, escalade.

#### Transfert de responsabilités

> Checklist des responsabilités et des connaissances nécessaires à la maintenance de l'application :
> - [ ] Dossier de maintenance — support à la production ;
> - [ ] Runbooks (procédures d'exploitation) ;
> - [ ] Manuels utilisateurs / administrateurs ;
> - [ ] Formations (équipe de maintenance, utilisateurs) ;
> - [ ] Contacts support (escalade, disponibilité, canaux).

### Approche DevSecOps

> Définir l'ensemble des processus, méthodologies et outils DevSecOps utilisés ou en arrimage avec la solution. Cette section peut être :
> - un résumé de l'existant, afin de s'assurer que les éléments pertinents pour la solution ont été pris en compte ;
> - des recommandations/décisions d'architecture pour la mise en place de processus, méthodes et outils pour bonifier la solution.
> Elle doit être remplie avec l'aide des spécialistes DevSecOps.

#### Planification

> Décrire les processus, méthodes et moyens de planification du projet (outils : Jira, etc.).

#### Code and Build

> Décrire les outils et référentiels nécessaires au développement, par exemple :
> - gestionnaire de code source ;
> - moyens de gérer le versionnement des fichiers (Git/Gitflow, GitLab/GitLab Flow) ;
> - gestion des artefacts.

#### Sécurité de la chaîne d'approvisionnement

> Décrire les mesures de sécurité de la chaîne d'approvisionnement logicielle :
> - **SBOM** (Software Bill of Materials) généré et vérifié pour chaque version ;
> - **scan des vulnérabilités** des dépendances (OWASP, CVE) ;
> - **scan IaC** (Terraform, CloudFormation, etc.) des configurations ;
> - **secret scanning** (détection de secrets dans le code et la chaîne CI/CD).

#### Chaîne CI/CD

> Définir la chaîne CI/CD (intégration continue, déploiement continu) et ses **portes de validation (gates)**.

| Étape | Outil | Responsabilité | Porte de validation (gate) |
|-------|-------|----------------|----------------------------|
| Planification | | | |
| Code / Build | | | |
| Scan & tests (qualité, sécurité) | | | |
| Construction de l'artefact | | | |
| Déploiement | | | |
| Surveillance / observabilité | | | |

**Tableau 48. Chaîne CI/CD – portes de validation (gates)**

#### Observabilité

> Décrire les moyens de monitoring, tracing et alerting de la solution.

#### Amélioration continue

> Décrire les moyens permettant de mesurer l'existant et d'améliorer continuellement les processus. Exemple : métriques (chaîne CI/CD, monitoring, alerting, etc.).
