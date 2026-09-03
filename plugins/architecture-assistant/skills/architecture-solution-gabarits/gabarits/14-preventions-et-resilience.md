## Prévention, reprise après sinistre et résilience

> Cette section décrit les moyens de **prévention**, de **reprise après sinistre (PRA)** et de **résilience** de la solution, en cohérence avec les risques du `04-risques.md` et la criticité des systèmes.

### Plan de continuité des activités (PCA)

> Le PCA ou plan de résilience doit décrire les moyens permettant de garantir une haute disponibilité au niveau de la production.
> Il comprend un ensemble de procédures, moyens, équipements et architectures requis afin de permettre la continuité de l'activité de la société quels que soient les sinistres qui pourraient survenir.
> Cette section devra être renseignée durant la phase de conception détaillée.

### Plan de reprise des activités (PRA)

> Le PRA est considéré comme un complément du PCA ou comme un palliatif en cas d'absence du PCA.
> Il se compose de processus à mettre en œuvre après la survenue d'un incident pour permettre à l'entreprise de reprendre son activité normale directement ou progressivement.

### Criticité par système / processus

> Tableau de **criticité par système / processus** (en lien avec le `03-besoins_affaires_exigences.md` : processus `PROC-xxx`, cas d'utilisation `UC-xxx` ; et le `06-architecture-solutions.md` : `SYS-xxx`). La criticité **détermine les RTO/RPO** de la section suivante.

| ID | Système / processus (`03` / `06`) | Criticité | Impacts si indisponible | Détermine RTO / RPO |
|----|-----------------------------------|-----------|-------------------------|---------------------|
| RES-001 | A définir (ex. PROC-001 / SYS-001) | Critique / Élevée / Moyenne / Basse | Perte de chiffre d'affaires, image de marque, impact juridique | RTO / RPO associés |

**Tableau 69. Criticité par système / processus**

### Indicateurs clés (RTO / RPO)

> RTO (Recovery Time Objective) : durée nécessaire pour pouvoir remettre la production en route, ou plus précisément l'intervalle de temps maximum pouvant être supporté entre le moment de la notification du sinistre et la reprise de l'activité. Il peut exister des RTO différents selon les équipements concernés.
>
> RPO (Recovery Point Objective) : période des données non récupérables, c'est-à-dire la quantité maximale de données que la société peut accepter de perdre, ou la « fraîcheur » des données.

| Fonctions ou système | Criticité | Scénarios de sinistre | Délai de récupération (RTO) | Point de récupération (RPO) | Stratégie de reprise (cold/warm/hot) | Sauvegardes (types, rétention, tests de restauration) | Tests DR périodiques | Responsable | Impacts |
|----------------------|-----------|-----------------------|-----------------------------|-----------------------------|--------------------------------------|--------------------------------------------------------|----------------------|-------------|---------|
| A définir | | Perte de DC, perte de région, cyberattaque | | | | | | | |

**Tableau 70. RTOs et RPOs**

### Niveau de services

> Définition des niveaux de services demandés par le client (SLA, SLO, SLI). Distinguer le **SLA contractuel** (promesse faite au client) du **SLO interne** (cible visée par l'exploitation).

#### Accords de niveau de service (SLA) — contractuel

> Le SLA définit la qualité de service, prestation prescrite entre un fournisseur de service et un client. C'est l'engagement **contractuel** envers le client.

#### Objectifs de niveau de service (SLO) — interne

> Le SLO est un moyen de mesurer la(les) performance(s) du fournisseur de service et de prévenir les litiges entre les deux parties, basés sur un malentendu.
> Un SLO peut être composé d'une ou plusieurs mesures de qualité de service (QoS). Exemple : un SLO de disponibilité.
> Les SLO doivent être **concrets** : cible, méthode de mesure, alerte et budget d'erreur associés.

| SLO | Cible | Méthode de mesure (SLI) | Alerte | Budget d'erreur | SLA contractuel associé |
|-----|-------|-------------------------|--------|-----------------|-------------------------|
| SLO-001 | Ex. disponibilité ≥ 99,95 % | Ex. sondes de santé sur le point d'entrée | Ex. sous 95 % sur 30 jours glissants | Ex. 4,4 h/mois | Ex. SLA 99,9 % |

**Tableau 71. SLO – objectifs de niveau de service**

#### Indicateurs de niveau de service (SLI)

> Un SLI (indicateur de niveau de service) mesure le respect d'un SLO (objectif de niveau de service).
> Ainsi, par exemple, si votre SLA spécifie que vos systèmes seront disponibles 99,95 % du temps, votre SLO est probablement de 99,95 % de disponibilité et vos SLI sont la mesure réelle de votre disponibilité. Peut-être 99,96 %, peut-être 99,99 %. Pour rester en conformité avec votre SLA, le SLI devra respecter ou dépasser les promesses faites dans ce document.
