## Objectifs

<!--
Cette section liste les objectifs d'affaires et d'architecture, les exigences non-fonctionnelles (NFRs), les patrons d'architecture selon les piliers du Well-Architected Framework, la matrice de traçabilité et les critères de qualification.
**Chaque section décrit les BESOINS, et non les solutions préconisées** (les solutions sont décrites dans `06-architecture-solutions.md` et tracées dans des ADR).
-->

### Objectifs de la solution

<!-- Objectifs tels qu'exprimés par le client (avant-vente, mandat) et objectifs d'architecture qui en découlent. Priorité : élevée / moyenne / faible. -->

| ID          | Type         | Objectif | Priorité | Critère de succès | Responsable |
| ----------- | ------------ | -------- | -------- | ----------------- | ----------- |
| OBJ-001     | Affaires     |          |          |                   |             |
| OBJ-ARC-001 | Architecture |          |          |                   |             |

**Tableau 11. Objectifs**

### Exigences non-fonctionnelles (NFRs)

<!-- 
Les NFRs doivent être **mesurables et testables** (sans métrique, elles ne sont pas vérifiables). 
Elles sont validées par les tests non-fonctionnels du plan de qualité (`13-plan-qualite.md`). 
-->

| ID      | Exigence non-fonctionnelle | Métrique / Cible | Criticité | Test de vérification | Statut |
| ------- | -------------------------- | ---------------- | --------- | -------------------- | ------ |
| NFR-001 |                            |                  |           |                      |        |

**Tableau 12. Exigences non-fonctionnelles**

### Framework d'architecture

<!--
Cette section identifie, pour chaque pilier du Well-Architected Framework, les **besoins** du projet et les **patrons d'architecture** recommandés pour y répondre.
**Le Well-Architected Framework se base sur les piliers Azure et AWS** : 
  - [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
  - [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/).
Chaque pilier est évalué selon les deux référentiels.
Chaque section n'est remplie que si le pilier est pertinent pour le projet. 
Chaque patron retenu fait l'objet d'une fiche dans le répertoire `patron-architecture/` de la skill `architecture-solution-gabarits`, est décrit dans `06-architecture-solutions.md` et tracé dans un ADR.
-->

#### Excellence opérationnelle

<!-- 
Cette section permet d'identifier et de décrire les besoins en termes d'excellence opérationnelle.
Exemple : **Patron** : besoin couvert, lien avec le pilier.
-->

#### Fiabilité

<!-- 
Cette section permet d'identifier et de décrire les besoins en termes de fiabilité.
Exemple : **Patron** : besoin couvert, lien avec le pilier.
-->

#### Efficacité des performances

<!-- 
Cette section permet d'identifier et de décrire les besoins en termes d'efficacité des performances.
Exemple : **Patron** : besoin couvert, lien avec le pilier.
-->

#### Sécurité

<!-- 
Exemples de besoins fréquents : l'application contient des données sensibles (affaires, renseignements personnels) → chiffrement au repos, en transit et en mémoire ; rotation des clés de chiffrement ; limitation des accès selon le **moindre privilège** ; classification des données.
Exemple : **Patron** : besoin couvert, lien avec le pilier.
-->

#### Optimisation des coûts

<!-- 
Cette section permet d'identifier et de décrire les besoins en termes d'optimisation des coûts.
Exemple : **Patron** : besoin couvert, lien avec le pilier.
-->

#### Développement durable

<!-- 
> Cette section permet d'identifier et de décrire les besoins en termes de développement durable.
Exemple : **Patron** : besoin couvert, lien avec le pilier.
-->

### Matrice de suivi

<!-- 
Matrice de **traçabilité** : lie chaque patron d'architecture aux piliers du Well-Architected Framework (Azure et AWS), aux exigences couvertes, aux ADR et aux tests de vérification. Une ligne par patron. Les fiches des patrons sont disponibles dans le répertoire `patron-architecture/` de la skill `architecture-solution-gabarits`.
-->

| Patron | Piliers (WAF) | Exigences / besoins couverts | ADR | Test de vérification |
| ------ | ------------- | ---------------------------- | --- | -------------------- |
|        |               |                              |     |                      |

**Tableau 13. Matrice de suivi (traçabilité patrons ↔ piliers ↔ exigences)**

### Critères de qualification

<!-- 
Les critères de qualification valident la réussite de l'initiative. **Les critères d'acceptation doivent être mesurés avec des métriques** (méthode de mesure et cible requises).
-->

| ID        | Nom | Description | Priorité | Métriques de l'existant | Métriques souhaitées (cible) | Méthode de mesure | Responsable affaires | Statut |
| --------- | --- | ----------- | -------- | ----------------------- | ---------------------------- | ----------------- | -------------------- | ------ |
| QUALIF_01 |     |             |          |                         |                              |                   |                      |        |

**Tableau 14. Critères de qualification**

### Non-objectifs

<!-- 
Ce que la solution ne doit **pas** faire (explicite les limites du mandat et évite la dérive du périmètre).
Expliciter les non-objectifs du projet.
-->