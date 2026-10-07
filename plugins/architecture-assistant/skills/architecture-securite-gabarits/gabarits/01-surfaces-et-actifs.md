---
doc_id: secu-01-surfaces-et-actifs
theme: Surfaces d'attaque et actifs — acteurs, actifs CIA, frontières de confiance
domaine: [securite]
sujets:
  - Surfaces d'attaque et actifs
  - Acteurs et identités
  - Actifs classés (CIA)
  - Frontières de confiance
  - Surfaces d'attaque
types_presentation: [securite]
sensibilite: restreint
togaf_layer: technology
ordre_presentation: 1
---
## Surfaces d'attaque et actifs

<!--
Fichier `01` : inventaire des **acteurs / identités**, des **actifs** classés selon le triangle CIA, des **frontières de confiance** et des **surfaces d'attaque** (`S1…Sn`). Ces surfaces servent d'ancrage à toute la suite du chapitre : la matrice STRIDE (`02`) et les fiches OWASP (`03`) y renvoient par leur identifiant `S1…Sn`.
Les IDs de surface (`S1…Sn`) sont **stables** : ne pas les renuméroter une fois attribués.
-->

### Acteurs et identités

<!--
Lister les acteurs qui interagissent avec le système et les identités qu'ils portent. Distinguer explicitement :
  - **identités humaines** (utilisateurs, administrateurs, opérateurs) ;
  - **charges / identités d'agents** (services, agents automatisés, comptes applicatifs).
La séparation humaines / agents est approfondie dans `04-identites-humaines-vs-agents.md` — y renvoyer, ne pas la dupliquer ici.
-->

| ID       | Acteur / identité | Type (humain / agent / service) | Rôle | Niveau de privilège | Renvoi |
| -------- | ----------------- | ------------------------------- | ---- | ------------------- | ------ |
| ACT-001  |                   |                                 |      |                     | voir `04` |

**Tableau. Acteurs et identités**

### Actifs classés (CIA)

<!--
Inventorier les **actifs** à protéger (données, services, secrets, composants) et leur **classification CIA** (sensibilité en Confidentialité, Intégrité, Disponibilité). Utiliser l'échelle commune `Faible` / `Moyen` / `Élevé` / `Critique`. Rester cohérent avec la classification des données du `10-cycle_vie_donnees.md` de la DAS.
-->

| ID       | Actif | Description | Confidentialité | Intégrité | Disponibilité | Propriétaire |
| -------- | ----- | ----------- | --------------- | --------- | ------------- | ------------ |
| ACTIF-001 |      |             | Faible/Moyen/Élevé/Critique | Faible/Moyen/Élevé/Critique | Faible/Moyen/Élevé/Critique | |

**Tableau. Actifs classés (CIA)**

### Frontières de confiance

<!--
Décrire les **frontières de confiance** (trust boundaries) : zones de confiance distinctes et points de franchissement (entrée / sortie de zone, changement de niveau de privilège, passage réseau). Chaque franchissement est un candidat de surface d'attaque. Relier aux zones de déploiement du `09-deploiement.md`.
Un diagramme (PlantUML / Mermaid / C4) illustrant les zones et les franchissements est référencé ici et dans l'index des diagrammes de la DAS.
-->

| ID       | Frontière | Zones séparées | Point de franchissement | Mécanisme de contrôle |
| -------- | --------- | -------------- | ----------------------- | --------------------- |
| FR-001   |           |                |                         |                       |

**Tableau. Frontières de confiance**

### Surfaces d'attaque

<!--
Recenser les **surfaces d'attaque** (`S1…Sn`) : chaque surface est un point ou un flux par lequel le système peut être attaqué (API exposée, interface d'administration, flux inter-services, canal de délégation d'agent, dépôt de secrets, etc.).
  - Chaque surface a un **ID stable** `S1…Sn` réutilisé dans `02` (matrice STRIDE) et `03` (fiches OWASP).
  - Relier chaque surface aux **actifs** exposés (`ACTIF-xxx`) et à la **frontière de confiance** franchie (`FR-xxx`).
  - Indiquer le **niveau d'exposition** sur l'échelle commune `Faible…Critique`.
-->

| ID  | Surface d'attaque | Description | Frontière franchie (`FR-xxx`) | Actifs exposés (`ACTIF-xxx`) | Niveau d'exposition |
| --- | ----------------- | ----------- | ----------------------------- | ---------------------------- | ------------------- |
| S1  |                   |             |                               |                              | Faible/Moyen/Élevé/Critique |
| S2  |                   |             |                               |                              | Faible/Moyen/Élevé/Critique |

**Tableau. Surfaces d'attaque (`S1…Sn`)**
