---
doc_id: das-05-planification
theme: Planification, CAPEX/OPEX
domaine: [affaires]
sujets:
  - Planification
  - Planification des tâches
  - Récapitulatif des efforts
  - Efforts de développement
  - Feuille de route
  - Estimation des coûts
  - Analyse CAPEX / OPEX
types_presentation: [executive, entreprise]
sensibilite: interne
togaf_layer: business
ordre_presentation: 5
---
## Planification

<!-- Cette section présente la planification du projet : découpage des livrables selon la **Work Breakdown Structure (WBS)**, récapitulatif des efforts, feuille de route et estimation des coûts. Les efforts et coûts sont alignés avec l'estimé de projet (WBS, `REF-01` du `001`), les rôles de l'arrimage RACI (`001`) et les volumétries (`12-volumetries.md`). -->

- **Date de début estimée** : YYYY-MM-DD <!-- À défaut de date fournie, J + 7 jours à compter de la date du jour. -->
- **Date de fin estimée** : YYYY-MM-DD <!-- Calculer lorsque c'est possible : date de début + durée estimée dérivée de la WBS et du récapitulatif des efforts (en tenant compte du nombre de collaborateurs et du calendrier ouvré). À défaut de données suffisantes, laisser le placeholder et le signaler. -->

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

<!-- Représenter les **jalons et livraisons** du projet sur une timeline. Chaque jalon est relié aux critères de qualification du `02-objectifs.md` et aux livrables de la WBS. **Si aucune date n'est fournie**, considérer le début de la feuille de route à **J + 7 jours à compter de la date du jour**, puis dérouler les jalons à partir de ce point. -->

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

### Analyse CAPEX / OPEX

<!--
AIDE À LA RÉDACTION — Analyse CAPEX / OPEX

But : distinguer et estimer les **coûts d'investissement (CAPEX)** et les **coûts d'exploitation (OPEX)** du projet, pour éclairer la décision d'affaires (choix de solution, modèle d'acquisition, horizon de retour sur investissement).

- **CAPEX (Capital Expenditure)** — dépenses d'investissement **capitalisées puis amorties** : matériel, licences perpétuelles, développement initial / mise en place (build), migration, achats réservés payés d'avance (ex. Reserved Instances / Savings Plans AWS avec engagement). Dépense ponctuelle qui crée un actif.
- **OPEX (Operating Expenditure)** — dépenses d'exploitation **récurrentes** : abonnements SaaS, hébergement et consommation cloud à l'usage (On-Demand), support, maintenance, main-d'œuvre d'exploitation. Dépense courante consommée au fil de l'eau.

Règles de rédaction :
1. **Ne jamais deviner un chiffre.** Si une information manque, la demander à l'humain : horizon d'analyse (nb d'années), devise, modèle d'acquisition (achat / location / abonnement), règle et durée d'amortissement, main-d'œuvre interne vs. externe, périmètre inclus (dev initial, migration, formation).
2. **Cohérence** : les montants doivent rester cohérents avec le « Récapitulatif des efforts » et « Estimation des coûts » ci-dessus, les volumétries (`12-volumetries.md`), le choix de solution (`07-choix-des-solutions.md`) et surtout la **source de vérité des coûts récurrents** du `09-deploiement.md` (Tableau 46) — ne pas recopier ces coûts, les **référencer**.
3. **Volet cloud / AWS** : les estimations cloud sont **sourcées des tarifs officiels** par l'Architecte AWS (date de consultation + région) et intégrées ici ; classer les engagements payés d'avance en CAPEX et la consommation à l'usage en OPEX.
4. **Montants indicatifs et non contractuels** ; expliciter les **hypothèses**. **Aucun secret** (clés, identifiants) dans ce tableau.
5. Maintenir la **numérotation globale** des tableaux et l'index du `001` (règles d'or 6 et 13). Le tableau ci-dessous est un **exemple** : remplacer les valeurs par celles du projet.

EXEMPLE (texte + tableau) — à remplacer par le contenu réel du projet :

Sur un horizon de 3 ans et en dollars canadiens (CAD), le projet « Portail client » retient un modèle majoritairement OPEX (hébergement cloud à l'usage). Le CAPEX se concentre sur le développement initial et une licence perpétuelle de l'outil de reporting ; l'OPEX couvre l'hébergement AWS (référence : Tableau 46 du `09`), le support et la maintenance évolutive. Hypothèses : amortissement linéaire du CAPEX sur 3 ans, main-d'œuvre d'exploitation estimée à 0,2 ETP, aucun engagement Reserved Instance la 1re année.
-->

| ID       | Poste de coût                                   | Type  | Modèle d'acquisition | Année 1   | Année 2   | Année 3   | Total 3 ans | Hypothèses / Source                                  |
| -------- | ----------------------------------------------- | ----- | -------------------- | --------- | --------- | --------- | ----------- | ---------------------------------------------------- |
| CAP-001  | Développement initial (build)                   | CAPEX | Interne (projet)     | $ 120 000 | $ 0       | $ 0       | $ 120 000   | Récapitulatif des efforts (Tableau 18)               |
| CAP-002  | Licence perpétuelle outil de reporting          | CAPEX | Achat                | $ 15 000  | $ 0       | $ 0       | $ 15 000    | Devis fournisseur (REF-xx du `001`)                  |
| OPX-001  | Hébergement cloud AWS (On-Demand)               | OPEX  | Abonnement / usage   | $ 24 000  | $ 24 000  | $ 24 000  | $ 72 000    | Source de vérité : Tableau 46 du `09` (Architecte AWS) |
| OPX-002  | Support et maintenance évolutive                | OPEX  | Abonnement           | $ 18 000  | $ 18 000  | $ 18 000  | $ 54 000    | 0,2 ETP exploitation                                 |
| **CAPEX** | **Sous-total investissement**                  | —     | —                    | $ 135 000 | $ 0       | $ 0       | $ 135 000   | —                                                    |
| **OPEX**  | **Sous-total exploitation**                    | —     | —                    | $ 42 000  | $ 42 000  | $ 42 000  | $ 126 000   | —                                                    |
| **Total** | **Coût total de possession (TCO)**             | —     | —                    | $ 177 000 | $ 42 000  | $ 42 000  | $ 261 000   | CAPEX amorti + OPEX                                  |

**Tableau 75. Analyse CAPEX / OPEX**
