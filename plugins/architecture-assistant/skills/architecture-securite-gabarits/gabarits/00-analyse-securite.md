---
doc_id: secu-00-analyse-securite
theme: Analyse de sécurité — portée, socle normatif, triangle CIA, synthèse
domaine: [securite]
sujets:
  - Analyse de sécurité
  - Portée et objectifs
  - Socle normatif
  - Triangle CIA (Confidentialité, Intégrité, Disponibilité)
  - Table du chapitre
types_presentation: [securite]
sensibilite: restreint
togaf_layer: technology
ordre_presentation: 0
---
## Analyse de sécurité

<!--
Fichier d'entrée (`00`) du dossier d'architecture de sécurité détaillée (`documentation/architecture-securite/`). Il cadre la portée de l'analyse, rappelle le socle normatif activé, pose le triangle CIA et donne la table du chapitre (les fichiers `01`→`06`). **Pas de section « Synthèse exécutive »** (règle d'or 11 de la skill `architecture-securite-gabarits`) : la posture et les priorités sont portées par `06-recommandations-priorisees.md` et la synthèse de `11-securite.md`, atteints par renvoi.
Ce dossier est l'**approfondissement** du `11-securite.md` de la DAS (synthèse courte). Renvoyer vers lui par **ancre Structurizr** (`documentation/<Software System>#<ancre>`, libellé = nom de section), ne pas le dupliquer. Les échelles de risque et les codes `VUL-xxx` / `RISQ-xxx` restent harmonisés avec le `04-risques.md` et le `11-securite.md`.
-->

### Portée et objectifs

<!--
Décrire :
  - le **périmètre** couvert par l'analyse de sécurité (systèmes, flux, environnements concernés), en renvoi vers `06-architecture-solutions.md` et `09-deploiement.md` de la DAS ;
  - les **objectifs** de l'analyse (identifier menaces et risques, définir contre-mesures, démontrer la couverture) ;
  - ce qui est **hors périmètre** (explicite), pour éviter toute ambiguïté de couverture.
-->

### Socle normatif

<!--
Rappeler le socle normatif **effectivement activé** pour cette analyse, selon les règles d'activation de la skill `cybersecurite` :
  - **Toujours actifs** : OWASP Top 10 (`03-risques-owasp.md`) et STRIDE (`02-menaces-stride.md`).
  - **Conditionnels (si l'analyse documente les risques)** : COBIT, NIST — à indiquer seulement s'ils sont activés.
  - **Sur demande explicite** : PCI DSS, GDPR, Loi 25, LPRPDE — à n'inscrire que s'ils ont été **explicitement demandés** par l'humain ou le coordinateur.
Lister ici uniquement les normes réellement activées, avec la source de l'activation (demande humaine / coordinateur). Ne jamais activer seul une norme « sur demande ».
-->

| Norme / modèle | Statut d'activation | Source de l'activation | Portée dans l'analyse |
| -------------- | ------------------- | ---------------------- | --------------------- |
| OWASP Top 10   | Actif (par défaut)  | Socle                  |                       |
| STRIDE         | Actif (par défaut)  | Socle                  |                       |
| COBIT          | Inactif / Actif     |                        |                       |
| NIST           | Inactif / Actif     |                        |                       |
| PCI DSS        | Inactif / Actif     |                        |                       |
| GDPR           | Inactif / Actif     |                        |                       |
| Loi 25 (Québec)| Inactif / Actif     |                        |                       |
| LPRPDE         | Inactif / Actif     |                        |                       |

**Tableau. Socle normatif activé**

### Triangle CIA (Confidentialité, Intégrité, Disponibilité)

<!--
Poser le triangle CIA comme grille de lecture de l'ensemble du dossier. Pour chaque propriété, préciser les enjeux propres au projet et l'exigence attendue :
  - **Confidentialité** — protection contre la divulgation non autorisée.
  - **Intégrité** — protection contre l'altération non autorisée.
  - **Disponibilité** — maintien du service et de l'accès légitime.
Relier ces propriétés aux catégories STRIDE (`02`) et aux actifs classés (`01`).
-->

| Propriété       | Enjeu pour le projet | Exigence attendue | Catégories STRIDE associées |
| --------------- | -------------------- | ----------------- | --------------------------- |
| Confidentialité |                      |                   | I (Information disclosure)  |
| Intégrité       |                      |                   | T (Tampering)               |
| Disponibilité   |                      |                   | D (Denial of service)       |

**Tableau. Triangle CIA**

### Table du chapitre

<!--
Table de navigation du dossier `architecture-securite/`. Conserver l'ordre et les noms de fichiers du dossier.
**Renvois au format Structurizr (règles d'or 10 et 11)** : le **Sujet** est un **lien par ancre Structurizr** `documentation/<Software System>#<ancre>` dont le **libellé est le nom de la section** visée (jamais un nom de fichier) ; **aucune** colonne « Fichier ». Remplacer `<Software System>` par le nom réel du système (URL-encodé) et l'ancre par le slug du titre visé (voir la règle de slug d'ancre).
-->

| Sujet | Contenu |
| ----- | ------- |
| [Surfaces et actifs](documentation/Software%20System#surfaces-et-actifs) | Acteurs / identités, actifs classés CIA, frontières de confiance, surfaces `S1…Sn` |
| [Menaces (STRIDE) par surface](documentation/Software%20System#menaces-stride-par-surface) | Matrice de synthèse STRIDE par surface + analyse détaillée par surface |
| [Risques OWASP Top 10](documentation/Software%20System#risques-owasp-top-10) | Table OWASP Top 10 + fiche par risque `A01…A10` croisée avec les surfaces |
| [Identités humaines vs agents](documentation/Software%20System#identites-humaines-vs-agents) | Invariant de séparation des identités humaines / charges d'agents |
| [Gates, guardrails et escalade](documentation/Software%20System#gates-guardrails-et-escalade) | Analyse de la gouvernance (gates / guardrails / escalade) sous l'angle STRIDE / OWASP |
| [Recommandations priorisées](documentation/Software%20System#recommandations-priorisees) | Recommandations consolidées, priorisées `P1`/`P2`/`P3`, à ID stable, sourcées |

**Tableau. Table du chapitre d'architecture de sécurité**
