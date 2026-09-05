## Volumétrie

<!-- 
Cette section détaille l'ensemble des données de volumétries connues et futures.
Types de volumétrie :
  - **Affaires** (usagers, clients, etc.) ;
  - **Données** (volumes de données, transferts de données, archivages, etc.) ;
  - **Infrastructure** (charges réseaux, balancement de charges, etc.) ;
  - **Applications** (nb d'instances, etc.).
Chaque volume est identifié (`VOL-001`, …), relié au **composant** concerné du `06-architecture-solutions.md` (ex. `SYS-001`) et aux **types de données** du `10-cycle_vie_donnees.md` (ex. `DON-001`). 
Les volumétries **alimentent le dimensionnement** (`09-deploiement.md`) et les **tests de charge** (`13-plan-qualite.md`). Les seuils de **monitoring/alertes** sont des seuils d'alerte concrets (même provisoires) à confirmer en conception détaillée.
-->
### Volumétrie d'affaires

| ID      | Métriques             | Données actuelles | Données futures | Tendance / croissance % | Pic vs moyenne                | Niveau de criticité | Composant (`06`) | Type de données (`10`) | Source & hypothèses de projection         | Date de mesure | Propriétaire         | Confiance (mesuré/estimé) | Monitoring (seuil)  | Alertes (seuil)     | Description |
| ------- | --------------------- | ----------------- | --------------- | ----------------------- | ----------------------------- | ------------------- | ---------------- | ---------------------- | ----------------------------------------- | -------------- | -------------------- | ------------------------- | ------------------- | ------------------- | ----------- |
| VOL-001 | Nombre d'utilisateurs | 70 000            | à projeter      | +10 %/an (hypothèse)    | Pic : 8 000 / moyenne : 1 200 | Élevé               | SYS-001          | DON-001                | Chiffres d'affaires fournis par le client | 2026-01-01     | Responsable affaires | Mesuré                    | 75 % de la capacité | 85 % de la capacité |             |

**Tableau 59. Volumétrie d'affaires**

### Volumétrie des données

| ID      | Métriques               | Données actuelles | Données futures | Tendance / croissance % | Pic vs moyenne | Niveau de criticité | Composant (`06`) | Type de données (`10`) | Source & hypothèses de projection       | Date de mesure | Propriétaire                | Confiance (mesuré/estimé) | Monitoring (seuil)           | Alertes (seuil)              | Description     |
| ------- | ----------------------- | ----------------- | --------------- | ----------------------- | -------------- | ------------------- | ---------------- | ---------------------- | --------------------------------------- | -------------- | --------------------------- | ------------------------- | ---------------------------- | ---------------------------- | --------------- |
| VOL-002 | Volumes                 | 308,21 Go         | à projeter      | +15 %/an (hypothèse)    | —              | Élevé               | SYS-001          | DON-001                | Volume mesuré sur la base de production | 2026-01-01     | DBA / Architecte de données | Mesuré                    | 80 % de l'espace provisionné | 90 % de l'espace provisionné | Données métiers |
| VOL-003 | Nbre de schémas OIQ_PRD | 1                 | à projeter      | —                       | —              | Moyen               | SYS-001          | DON-001                | Base de production actuelle             | 2026-01-01     | DBA                         | Mesuré                    | —                            | Ajout non planifié           | Données métiers |

**Tableau 60. Volumétrie des données**

### Volumétrie infrastructure

| ID      | Métriques             | Données actuelles | Données futures | Tendance / croissance % | Pic vs moyenne | Niveau de criticité | Composant (`06`) | Type de données (`10`) | Source & hypothèses de projection          | Date de mesure | Propriétaire              | Confiance (mesuré/estimé) | Monitoring (seuil)    | Alertes (seuil)       | Description                                            |
| ------- | --------------------- | ----------------- | --------------- | ----------------------- | -------------- | ------------------- | ---------------- | ---------------------- | ------------------------------------------ | -------------- | ------------------------- | ------------------------- | --------------------- | --------------------- | ------------------------------------------------------ |
| VOL-004 | Nb de serveurs        | à définir         | à projeter      | —                       | —              | Élevé               | SYS-001          | —                      | À définir avec l'architecte infrastructure | 2026-01-01     | Architecte infrastructure | Estimé                    | 75 % CPU/RAM          | 85 % CPU/RAM          | Serveur On-Prem                                        |
| VOL-005 | Balancement de charge | à définir         | à projeter      | —                       | —              | Critique            | SYS-001          | —                      | À définir avec l'architecte infrastructure | 2026-01-01     | Architecte infrastructure | Estimé                    | 70 % du débit nominal | 80 % du débit nominal | Assure la stabilité du point d'entrée de l'application |

**Tableau 61. Volumétrie infrastructure**

### Volumétries applicatives

| ID      | Métriques                        | Données actuelles | Données futures | Tendance / croissance % | Pic vs moyenne              | Niveau de criticité | Composant (`06`) | Type de données (`10`) | Source & hypothèses de projection    | Date de mesure | Propriétaire          | Confiance (mesuré/estimé) | Monitoring (seuil)         | Alertes (seuil)            | Description |
| ------- | -------------------------------- | ----------------- | --------------- | ----------------------- | --------------------------- | ------------------- | ---------------- | ---------------------- | ------------------------------------ | -------------- | --------------------- | ------------------------- | -------------------------- | -------------------------- | ----------- |
| VOL-006 | Applications principale          | ? instances       | ? instances     | —                       | —                           | Critique            | SYS-001          | —                      | À définir en conception détaillée    | 2026-01-01     | Architecte applicatif | Estimé                    | 80 % du pool               | 90 % du pool               |             |
| VOL-007 | Nombre d'utilisateurs par jour   | 220 en moyenne    | Futur : ?       | —                       | —                           | Élevé               | SYS-001          | DON-001                | Métriques actuelles de la plateforme | 2026-01-01     | Responsable affaires  | Mesuré                    | 1 500 req/jour             | 2 000 req/jour             |             |
| VOL-008 | Nombre d'utilisateurs simultanés | 2000              | Futur : ?       | —                       | Pic : 2 000 / moyenne : 350 | Élevé               | SYS-001          | DON-001                | Métriques actuelles de la plateforme | 2026-01-01     | Architecte applicatif | Mesuré                    | 80 % du pool de connexions | 90 % du pool de connexions |             |

**Tableau 62. Volumétrie applicatives**
