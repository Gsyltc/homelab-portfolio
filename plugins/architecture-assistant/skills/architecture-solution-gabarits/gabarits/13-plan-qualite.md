## Plan de qualité

> Cette section décrit le plan de test de la solution.
> Cela inclut l'ensemble des tests effectués par les développeurs, l'assurance qualité et le client.
> Les plans de tests sont généralement écrits par le leader Assurance Qualité.
> Les critères d'acceptation sont généralement définis par le client.
> Cette section n'a pas pour objectif de décrire l'ensemble des tests mais d'y adosser les références documentaires des parties prenantes.

### Pyramide de tests

> Pyramide de tests de la solution (unitaire → intégration → système → UAT) avec la **couverture attendue**, les **outils** et les **portes de validation (gates CI)**. Les volumétries du `12-volumetries.md` alimentent les jeux de tests de charge.

| Niveau | Description | Couverture attendue | Outils | Gates CI |
|--------|-------------|---------------------|--------|----------|
| Tests unitaires | Isoler chaque module du système et le tester séparément | ≥ 80 % du code | À définir (ex. JUnit, xUnit) | Validation de la MR |
| Tests d'intégration | Vérifier l'intégration des composants entre eux (API, bases de données, files) | Interfaces et flux critiques | À définir (ex. Postman, Testcontainers) | Validation de la MR |
| Tests système | Valider le système complet dans un environnement représentatif | Scénarios de bout en bout | À définir | Avant promotion d'environnement |
| Tests d'acceptation (UAT) | Validation par le client (critères d'acceptation du `03`) | Critères d'acceptation des UC | À définir avec le client | Porte de mise en production |

**Tableau 63. Pyramide de tests**

### Test à la charge du développeur

> L'architecte logiciel et/ou le Tech Lead doit s'assurer que les tests unitaires sont codés selon les bonnes pratiques.
> Pour chacun des tests, il est nécessaire de définir des critères d'acceptation ; garde-fous qui permettront de s'assurer de la stabilité de la chaîne d'intégration et déploiement.

| Type de test | Description | Référence documentaire |
|--------------|-------------|------------------------|
| Tests unitaires | Le but de ces tests de niveau unitaire est d'isoler chaque module du système et de les tester séparément. | A définir en conception détaillée |

**Tableau 64. Test de développement**

### Plan assurance qualité

> **L'architecte de solution n'est pas responsable du plan d'assurance qualité.** Cependant, il doit s'assurer de la cohérence du plan avec la solution (bonne pratique conservée) : assurer les arrimages nécessaires et s'assurer que les plans de tests répondent aux besoins.

| Référence du document | Description du document | Liens du document |
|------------------------|-------------------------|-------------------|
| TEST01 | Tests d'intégration | A définir en conception détaillée |
| TEST02 | Tests système | A définir en conception détaillée |

**Tableau 65. Plan d'assurance qualité**

### Tests non-fonctionnels

> Tests non-fonctionnels de la solution, en arrimage avec les autres sections du dossier.

| Type de test | Description | Références | Critères (exemples provisoires) |
|--------------|-------------|------------|----------------------------------|
| Performance / charge | Valider les volumétries et seuils d'alerte du `12-volumetries.md` (charge, pic, montée en charge) | `12-volumetries.md`, `02-objectifs.md` | Temps de réponse, débit cibles du `02` |
| Sécurité | Valider les contrôles du `11-securite.md` (OWASP/ASVS, STRIDE, chiffrement, GIA) | `11-securite.md`, `08-contraintes.md` | Aucune vulnérabilité critique ; conformité `NOR-001` |
| Résilience | Valider la reprise et la résilience du `14-preventions-et-resilience.md` (failover, reprise) | `14-preventions-et-resilience.md` | Respect des RTO/RPO |

**Tableau 66. Tests non-fonctionnels**

### Environnements et données de test

> Décrire les environnements de test (en lien avec `09-deploiement.md`) et les **données de test**, y compris le **masquage / anonymisation** des données personnelles (Loi 25, `08-contraintes.md`).

| Environnement | Finalité | Jeu de données | Masquage / anonymisation |
|---------------|----------|----------------|--------------------------|
| A définir (dev / QA / staging) | | | À définir (données personnelles masquées) |

**Tableau 67. Environnements et données de test**

### Traçabilité exigences / cas d'utilisation → tests

> Chaque **exigence / cas d'utilisation** du `03-besoins_affaires_exigences.md` doit être tracé vers son ou ses tests (règle d'or de la couverture des exigences).

| Exigence / UC (`03`) | Test associé | Niveau de test | Résultat attendu |
|----------------------|--------------|----------------|------------------|
| UC-001 / EXI-xxx | A définir | A définir | A définir |

**Tableau 68. Traçabilité exigences / cas d'utilisation → tests**
