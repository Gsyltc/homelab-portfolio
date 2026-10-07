---
doc_id: secu-04-identites-humaines-vs-agents
theme: Séparation des identités humaines et des charges d'agents
domaine: [securite]
sujets:
  - Séparation des identités humaines et des charges d'agents
  - Invariant de séparation
  - Inventaire des identités
  - Frontières de délégation
  - Contrôles de non-confusion
types_presentation: [securite]
sensibilite: restreint
togaf_layer: application
ordre_presentation: 4
---
## Séparation des identités humaines et des charges d'agents

<!--
Fichier `04` : pose et documente l'**invariant de séparation** entre les **identités humaines** (personnes, comptes nominatifs) et les **charges / identités d'agents** (services, agents automatisés, comptes applicatifs, charges d'exécution). Cet invariant est une **surface de sécurité** à part entière : toute confusion entre une identité humaine et une charge d'agent est un défaut de sécurité (usurpation — STRIDE `S`, élévation de privilège — STRIDE `E`).
Relier aux acteurs / identités du `01-surfaces-et-actifs.md` (`ACT-xxx`) et aux frontières de délégation analysées en gouvernance (`05-gates-guardrails-escalade.md`).
-->

### Invariant de séparation

<!--
Énoncer l'invariant de façon non ambiguë, par exemple :
  - une **identité humaine** ne porte jamais directement une charge d'agent, et réciproquement ;
  - une **charge d'agent** agit sous une identité de service distincte, traçable, à privilèges dédiés et minimaux ;
  - toute **délégation** d'une identité humaine vers un agent est explicite, bornée (portée, durée), révocable et tracée ;
  - aucun contrôle de sécurité lié à cette séparation ne peut être abaissé sans **validation humaine explicite tracée** (plancher SG-3, voir `05` et le gabarit de revue).
Préciser les conséquences attendues sur l'authentification, l'autorisation et la journalisation.
-->

### Inventaire des identités

<!--
Lister les identités, en qualifiant clairement leur nature (humaine / agent / service) et leur mode d'authentification. Reprendre les `ACT-xxx` du `01`.
-->

| ID (`ACT-xxx`) | Identité | Nature (humaine / agent / service) | Mode d'authentification | Privilèges | Source de vérité (IdP / annuaire) |
| -------------- | -------- | ---------------------------------- | ----------------------- | ---------- | --------------------------------- |
| ACT-001 |  |  |  |  |  |

**Tableau. Inventaire des identités (humaines vs agents)**

### Frontières de délégation

<!--
Décrire les **délégations** autorisées entre identités (humaine → agent, agent → agent). Pour chacune : déclencheur, portée, durée, mécanisme de révocation, trace produite. Toute délégation est une frontière de confiance à relier au `01` (`FR-xxx`) et aux menaces STRIDE du `02`.
-->

| ID       | Délégation (de → vers) | Déclencheur | Portée | Durée / révocation | Trace produite | Frontière (`FR-xxx`) |
| -------- | ---------------------- | ----------- | ------ | ------------------ | -------------- | -------------------- |
| DEL-001  |                        |             |        |                    |                |                      |

**Tableau. Frontières de délégation**

### Contrôles de non-confusion

<!--
Lister les **contrôles** garantissant que l'invariant de séparation n'est pas violé : séparation des espaces de secrets, nommage distinct, segmentation des rôles (RBAC/ABAC), interdiction d'exécution d'instructions issues de données, journalisation distinguant acteur humain et charge d'agent, alertes sur confusion d'identité.
Pour chaque contrôle : objectif, menace STRIDE couverte (`STR-xxx` / catégorie), risque OWASP lié (`A0x`), état (en place / à mettre en place), renvoi recommandation (`06`).
-->

| ID       | Contrôle de non-confusion | Objectif | Menace STRIDE couverte | Risque OWASP lié (`A0x`) | État | Recommandation (`06`) |
| -------- | ------------------------- | -------- | ---------------------- | ------------------------ | ---- | --------------------- |
| CTL-001  |                           |          |                        |                          |      |                       |

**Tableau. Contrôles de non-confusion des identités**
