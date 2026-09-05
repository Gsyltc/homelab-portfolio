## Description des solutions étudiées

<!-- 
Cette section documente la **solution retenue** et les **solutions potentielles** étudiées. Il est possible de décrire plusieurs solutions (cas d'une prévente par exemple) ; dans ce cas, distinguer la **solution préférentielle** des **solutions alternatives**. Cette section doit permettre la compréhension des raisons du choix proposé.
Chaque choix de solution fait l'objet d'un **ADR** (skill `create-architectural-decision-record`) référencé ici, et vérifie la **couverture d'un patron** du répertoire `patron-architecture/` de la skill `architecture-solution-gabarits`.
-->

### État des lieux / Solution actuelle

<!-- Décrire la solution actuelle et les éléments nécessitant un changement ou une amélioration. Accompagner cette section d'un diagramme de contexte de la solution actuelle. -->

### Récapitulatif des solutions étudiées

<!-- Dans le cas où plusieurs solutions sont envisagées, faire un récapitulatif par rapport à : la solution actuelle, la solution préférentielle et les solutions envisagées. Accompagner cette section de diagrammes de contexte au besoin. -->

| Solution recommandée (SOL-001)                        | Solution alternative 1 (SOL-002)                     | Solution alternative 2 (SOL-003)                     |
| ----------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| Nom et description de la solution préférentielle      | Nom et description de la solution alternative 1      | Nom et description de la solution alternative 2      |
| Éléments de comparaison de la solution préférentielle | Éléments de comparaison de la solution alternative 1 | Éléments de comparaison de la solution alternative 2 |

**Tableau 27. Récapitulatif des solutions recommandées**

### Matrice de décision pondérée

<!-- 
Matrice de décision rendant le choix **auditable** : chaque **critère de décision** reçoit un **poids** (la somme des poids = 100 %), chaque solution reçoit un **score** (ex. échelle de 1 à 5) et le **total pondéré** est calculé. Définir les critères et le barème de score, et les documenter dans l'ADR.
-->

| Critère de décision                         |   Poids   | SOL-001 (recommandée) | SOL-002 (alternative 1) | SOL-003 (alternative 2) |
| ------------------------------------------- | :-------: | :-------------------: | :---------------------: | :---------------------: |
| Exemple : adéquation aux besoins d'affaires |   25 %    |           4           |            3            |            2            |
| Exemple : coût total de possession          |   25 %    |           3           |            4            |            3            |
| Exemple : faisabilité / délais              |   20 %    |           5           |            3            |            4            |
| Exemple : risques                           |   15 %    |           4           |            3            |            2            |
| Exemple : évolutivité                       |   15 %    |           4           |            4            |            3            |
| **Total pondéré**                           | **100 %** |                       |                         |                         |

**Tableau 28. Matrice de décision pondérée**

### Comparaison des coûts

<!-- Tableau comparatif unique des coûts par solution (**coût initial** et **coût récurrent** estimés). Le détail des coûts récurrents (licences, hébergement) est documenté dans `09-deploiement.md`. -->

| Solution                | Coût initial estimé | Coût récurrent estimé | Référence détail    |
| ----------------------- | ------------------: | --------------------: | ------------------- |
| SOL-001 (recommandée)   |                     |                       | `09-deploiement.md` |
| SOL-002 (alternative 1) |                     |                       | `09-deploiement.md` |
| SOL-003 (alternative 2) |                     |                       | `09-deploiement.md` |

**Tableau 29. Comparaison des coûts**

### Décision formelle

<!-- Consigner la décision formelle de choix de la solution. **C'est exactement le cas d'usage d'un ADR** : la décision formelle (date, décideurs, justification, alternatives rejetées) doit être enregistrée dans un ADR et le lien référencé ici. -->

| Élément                                             | Contenu    |
| --------------------------------------------------- | ---------- |
| Date de la décision                                 | YYYY-MM-DD |
| Décideurs                                           |            |
| Solution retenue                                    | SOL-001    |
| Justification                                       |            |
| Alternatives rejetées et raisons (SOL-002, SOL-003) |            |
| **Lien ADR**                                        |            |

**Tableau 30. Décision formelle**

### Solution recommandée (SOL-001)

<!-- Description précise de la solution, des points saillants, des raisons du choix (tracées dans un ADR). -->

#### Diagramme de contexte (SOL-001)

<!-- Ajouter un diagramme de contexte de la solution. -->

#### Avantages et limitations de la solution recommandée (SOL-001)

| Avantages  | Limitations  |
| ---------- | ------------ |
| AVANTAGE 1 | LIMITATION 1 |

**Tableau 31. Avantages et limitations (SOL-001)**

#### Analyse de faisabilité (SOL-001)

<!-- Analyse de faisabilité **brève** : technique, organisationnelle, budgétaire et calendaire (en arrimage avec `05-planification.md`). -->

#### Risques (SOL-001)

<!-- Risques associés à la solution, tracés dans `04-risques.md` (codes `RISQ-XXX`) et dans les ADR. -->

### Solution alternative 1 (SOL-002)

#### Diagramme de contexte (SOL-002)

<!-- Ajouter un diagramme de contexte de la solution. -->

#### Avantages et limitations de la solution alternative 1 (SOL-002)

| Avantages  | Limitations  |
| ---------- | ------------ |
| AVANTAGE 1 | LIMITATION 1 |

**Tableau 32. Avantages et limitations (SOL-002)**

#### Analyse de faisabilité (SOL-002)

<!-- Analyse de faisabilité **brève** : technique, organisationnelle, budgétaire et calendaire (en arrimage avec `05-planification.md`). -->

#### Risques (SOL-002)

<!-- Risques associés à la solution, tracés dans `04-risques.md` (codes `RISQ-XXX`) et dans les ADR. -->

### Solution alternative 2 (SOL-003)

#### Diagramme de contexte (SOL-003)

<!-- Ajouter un diagramme de contexte de la solution. -->

#### Avantages et limitations de la solution alternative 2 (SOL-003)

| Avantages  | Limitations  |
| ---------- | ------------ |
| AVANTAGE 1 | LIMITATION 1 |

**Tableau 33. Avantages et limitations (SOL-003)**

#### Analyse de faisabilité (SOL-003)

<!-- Analyse de faisabilité **brève** : technique, organisationnelle, budgétaire et calendaire (en arrimage avec `05-planification.md`). -->

#### Risques (SOL-003)

<!-- Risques associés à la solution, tracés dans `04-risques.md` (codes `RISQ-XXX`) et dans les ADR. -->
