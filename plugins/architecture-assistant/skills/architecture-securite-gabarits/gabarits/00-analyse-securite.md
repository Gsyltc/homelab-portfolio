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
  - Synthèse exécutive
types_presentation: [securite]
sensibilite: restreint
togaf_layer: technology
ordre_presentation: 0
---
## Analyse de sécurité

<!--
Fichier d'entrée (`00`) du dossier d'architecture de sécurité détaillée (`documentation/architecture-securite/`). Il cadre la portée de l'analyse, rappelle le socle normatif activé, pose le triangle CIA, donne la table du chapitre (les fichiers `01`→`06`) et une synthèse exécutive.
Ce dossier est l'**approfondissement** du `11-securite.md` de la DAS (synthèse courte). Renvoyer vers lui, ne pas le dupliquer. Les échelles de risque et les codes `VUL-xxx` / `RISQ-xxx` restent harmonisés avec le `04-risques.md` et le `11-securite.md`.
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
Donner la table de navigation du dossier `architecture-securite/`. Conserver l'ordre et les noms de fichiers.
-->

| Fichier | Contenu |
| ------- | ------- |
| `00-analyse-securite.md` | Portée, socle normatif, triangle CIA, table du chapitre, synthèse exécutive |
| `01-surfaces-et-actifs.md` | Acteurs / identités, actifs classés CIA, frontières de confiance, surfaces `S1…Sn` |
| `02-menaces-stride.md` | Matrice de synthèse STRIDE par surface + analyse détaillée par surface |
| `03-risques-owasp.md` | Table OWASP Top 10 + fiche par risque `A01…A10` croisée avec les surfaces |
| `04-identites-humaines-vs-agents.md` | Invariant de séparation des identités humaines / charges d'agents |
| `05-gates-guardrails-escalade.md` | Analyse de la gouvernance (gates / guardrails / escalade) sous l'angle STRIDE / OWASP |
| `06-recommandations-priorisees.md` | Recommandations consolidées, priorisées `P1`/`P2`/`P3`, à ID stable, sourcées |

**Tableau. Table du chapitre d'architecture de sécurité**

### Synthèse exécutive

<!--
Résumer, en quelques paragraphes et sans jargon superflu :
  - la **posture de sécurité** globale constatée (points forts, points de vigilance) ;
  - les **surfaces** les plus exposées (renvoi `S1…Sn` du `01`) ;
  - les **risques majeurs** (renvoi aux lignes `R01…` du `03` / registre `RISQ-xxx` du `04`) ;
  - les **recommandations prioritaires** `P1` (renvoi au `06`).
Cette synthèse est destinée à la lecture rapide ; le détail est dans les fichiers `01`→`06`.
-->
