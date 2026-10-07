---
doc_id: secu-06-recommandations-priorisees
theme: Recommandations de sécurité consolidées et priorisées (P1/P2/P3)
domaine: [securite]
sujets:
  - Recommandations de sécurité priorisées
  - Méthode de priorisation
  - Recommandations applicatives (R-11A-*)
  - Recommandations infrastructure (R-11B-*)
  - Feuille de route de remédiation
types_presentation: [securite]
sensibilite: restreint
togaf_layer: application
ordre_presentation: 6
---
## Recommandations de sécurité priorisées

<!--
Fichier `06` : consolidation des **recommandations** issues de l'ensemble du chapitre (menaces STRIDE `02`, risques OWASP `03`, identités `04`, gouvernance `05`). Chaque recommandation est **sourcée** (traçée vers la menace / le risque / le contrôle qui la motive), à **ID stable**, et **priorisée** `P1` / `P2` / `P3`.
Convention d'identifiants (stables, cohérents avec le `11-securite.md` de la DAS) :
  - **`R-11A-*`** : recommandations de **sécurité applicative** ;
  - **`R-11B-*`** : recommandations de **sécurité infrastructure** ;
  - adapter le préfixe au projet si nécessaire, mais le figer une fois attribué.
Échelle commune `Faible…Critique` ; renvois `S1…Sn`, `STR-xxx`, `A0x`, `VUL-xxx`, `RISQ-xxx`, ADR (`../../decisions/NNNN-....md`).
-->

### Méthode de priorisation

<!--
Expliciter la méthode de priorisation :
  - **P1** — critique / urgent : risque résiduel `Élevé`/`Critique`, à traiter en priorité ;
  - **P2** — important : risque résiduel `Moyen`, à planifier ;
  - **P3** — souhaitable : risque résiduel `Faible` ou amélioration de posture.
La priorité découle du **risque résiduel** `P × I` (après contre-mesures existantes) et de la faisabilité. Rester cohérent avec les échelles du `04-risques.md`.
-->

### Recommandations applicatives (R-11A-*)

<!--
Une ligne par recommandation applicative. Chaque recommandation est sourcée (origine) et priorisée.
-->

| ID (`R-11A-*`) | Recommandation | Priorité (P1/P2/P3) | Source (`STR-xxx` / `A0x` / `S1…Sn` / `VUL-xxx`) | Risque résiduel visé (`P × I`) | Propriétaire | Échéance | Statut | ADR lié |
| -------------- | -------------- | ------------------- | ------------------------------------------------ | ------------------------------ | ------------ | -------- | ------ | ------- |
| R-11A-001 |  | P1/P2/P3 |  | Faible/Moyen/Élevé/Critique |  |  |  | `../../decisions/NNNN-....md` |

**Tableau. Recommandations applicatives (`R-11A-*`)**

### Recommandations infrastructure (R-11B-*)

<!--
Une ligne par recommandation infrastructure. Mêmes règles que ci-dessus.
-->

| ID (`R-11B-*`) | Recommandation | Priorité (P1/P2/P3) | Source (`STR-xxx` / `A0x` / `S1…Sn` / `VUL-xxx`) | Risque résiduel visé (`P × I`) | Propriétaire | Échéance | Statut | ADR lié |
| -------------- | -------------- | ------------------- | ------------------------------------------------ | ------------------------------ | ------------ | -------- | ------ | ------- |
| R-11B-001 |  | P1/P2/P3 |  | Faible/Moyen/Élevé/Critique |  |  |  | `../../decisions/NNNN-....md` |

**Tableau. Recommandations infrastructure (`R-11B-*`)**

### Feuille de route de remédiation

<!--
Ordonnancer les recommandations dans le temps par vagues de priorité (P1 d'abord). Si aucune date n'est fournie, considérer le début à J+7 jours (cohérent avec la règle d'or de `architecture-solution-gabarits`). Relier aux jalons de `05-planification.md` de la DAS si pertinent.
-->

| Vague | Priorité | Recommandations incluses (`R-11A-*` / `R-11B-*`) | Fenêtre (début → fin) | Dépendances |
| ----- | -------- | ------------------------------------------------ | --------------------- | ----------- |
| V1    | P1       |                                                  |                       |             |
| V2    | P2       |                                                  |                       |             |
| V3    | P3       |                                                  |                       |             |

**Tableau. Feuille de route de remédiation**
