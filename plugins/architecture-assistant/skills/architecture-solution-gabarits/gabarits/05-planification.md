---
doc_id: das-05-planification
theme: Planification, CAPEX/OPEX, crédit CDAE-IA
domaine: [affaires]
sujets:
  - Planification
  - Planification des tâches
  - Récapitulatif des efforts
  - Efforts de développement
  - Feuille de route
  - Estimation des coûts
  - Crédit d'impôt CDAE-IA (estimation)
types_presentation: [executive, entreprise]
sensibilite: interne
togaf_layer: business
ordre_presentation: 5
---
## Planification

<!-- Cette section présente la planification du projet : découpage des livrables selon la **Work Breakdown Structure (WBS)**, récapitulatif des efforts, feuille de route et estimation des coûts. Les efforts et coûts sont alignés avec l'estimé de projet (WBS, `REF-01` du `001`), les rôles de l'arrimage RACI (`001`) et les volumétries (`12-volumetries.md`). -->

- **Date de début estimée** : YYYY-MM-DD
- **Date de fin estimée** : YYYY-MM-DD

### Planification des tâches

<!-- Découper le projet en livrables et en tâches selon la **Work Breakdown Structure (WBS)** (template `REF-01` du `001`). La WBS est la structure de référence du projet : chaque livrable est tracé dans les fichiers thématiques concernés et relié aux rôles (arrimage RACI du `001`). -->

![Image 1. Work Breakdown Structure](embed:wbs)

### Récapitulatif des efforts

<!-- Ce tableau récapitule l'ensemble des efforts estimés du projet **par rôle**, selon une estimation en trois points (basse / probable / haute). Préciser l'unité (jours ou jours-personnes) ; l'effort total doit être cohérent avec la WBS et les rôles de l'arrimage RACI (`001`). -->

| **Rôles**                     | **Nb de collaborateurs** | **Estimation basse** | **Estimation probable** | **Estimation haute** |
|-------------------------------|--------------------------|----------------------|-------------------------|----------------------|
| Architectes                   | 1                        | 0                    | 0                       | 0                    |
| Développeurs                  | 3                        | 0                    | 0                       | 0                    |
| UX/UI                         | 1                        | 0                    | 0                       | 0                    |
| Analystes                     | 2                        | 0                    | 0                       | 0                    |
| Intégration de tâche / DevOps | 1                        | 0                    | 0                       | 0                    |
| Assurance Qualité             | 1                        | 0                    | 0                       | 0                    |
| Gestion du changement         | 1                        | 0                    | 0                       | 0                    |
| Chargés de projet             | 1                        | 0                    | 0                       | 0                    |
| Support des pratiques         | 1                        | 0                    | 0                       | 0                    |
| **Total**                     | -                        | **0**                | **0**                   | **0**                |

**Tableau 18. Récapitulatif des efforts**

### Efforts de développement

<!-- Ce tableau récapitule les efforts de développement **uniquement** (il ne comprend pas les efforts annexes). L'écart type mesure la dispersion de l'estimation (delta entre le meilleur scénario et le scénario défavorable) ; il sert à qualifier le niveau de confiance de l'estimation. -->

| **Meilleur scénario** | **Scénario probable** | **Scénario défavorable** | **Déviation standard** |
|-----------------------|-----------------------|--------------------------|------------------------|
| 0                     | 0                     | 0                        | 0                      |

**Tableau 19. Efforts de développement**

### Feuille de route

<!-- Représenter les **jalons et livraisons** du projet sur une timeline. Chaque jalon est relié aux critères de qualification du `02-objectifs.md` et aux livrables de la WBS. -->

![Image 2. Feuille de route](embed:timeline)

### Estimation des coûts

<!-- 
Ce tableau est une estimation de l'ensemble des coûts du projet. Il est donné à titre informatif et n'est pas contractuel. Il ne prend pas en compte les différents ajustements pouvant être apportés par les directeurs de projets et directeurs de développement des affaires.
Les coûts doivent être cohérents avec le récapitulatif des efforts et les volumétries (`12-volumetries.md`).
-->

| Meilleur scénario | Scénario probable | Scénario défavorable |
|-------------------|-------------------|----------------------|
| $ 0               | $ 0               | $ 0                  |

**Tableau 20. Estimation des coûts**

### Crédit d'impôt CDAE-IA (estimation)

<!--
Sous-section CONDITIONNELLE — ne la renseigner (et ne conserver cette section) QUE si les trois conditions sont réunies :
1. l'humain a demandé explicitement l'estimation du crédit CDAE-IA ;
2. le projet est éligible — la description du projet porte `CDAE-AI: Oui` ;
3. l'ensemble des informations nécessaires au calcul sont disponibles.
Si une information manque, indiquer les éléments manquants à l'humain et NE PAS produire d'estimation partielle. Si le projet n'est pas éligible (`CDAE-AI: Non`) ou si aucune demande n'a été faite, laisser la section vide ou la retirer.
La méthode, les conditions d'éligibilité et les taux font autorité dans la skill `cdae-ai-eligibilite` (source unique) — ne pas les dupliquer ici, s'y référer.
Estimation INFORMATIVE, NON CONTRACTUELLE et SANS valeur de conseil fiscal : les attestations et le traitement fiscal relèvent d'Investissement Québec et de Revenu Québec.
-->

- **Éligibilité (description du projet)** : `CDAE-AI: Oui`
- **Taux appliqué** : 30 % des salaires admissibles (22 % remboursable + 8 % non remboursable) — **ou** taux réduit 15 % (11 % + 4 %) si ≥ 50 % des revenus proviennent de services rendus hors Québec à une société ayant un lien de dépendance.
- **Base de calcul** : salaires admissibles (revenu d'emploi selon la Loi sur les impôts du Québec ; plus de plafond salarial), proratisés selon les jours travaillés.

| **Employé / rôle** | **Salaires admissibles** | **Jours travaillés / jours exercice** | **Taux** | **Crédit remboursable** | **Crédit non remboursable** | **Crédit total** |
|--------------------|--------------------------|----------------------------------------|----------|-------------------------|-----------------------------|------------------|
| —                  | $ 0                      | 0 / 0                                   | 30 %     | $ 0                     | $ 0                         | $ 0              |
| **Total**          | **$ 0**                  | -                                      | -        | **$ 0**                 | **$ 0**                     | **$ 0**          |

**Tableau 21. Estimation du crédit d'impôt CDAE-IA**

> Estimation informative et non contractuelle, sans valeur de conseil fiscal. Conditions d'éligibilité et méthode de calcul : skill `cdae-ai-eligibilite` (source unique). Attestations et traitement fiscal : Investissement Québec / Revenu Québec.
