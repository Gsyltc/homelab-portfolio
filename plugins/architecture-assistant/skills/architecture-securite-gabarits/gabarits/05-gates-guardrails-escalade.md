---
doc_id: secu-05-gates-guardrails-escalade
theme: Gouvernance — gates, guardrails et escalade sous l'angle STRIDE / OWASP
domaine: [securite]
sujets:
  - Gouvernance — gates, guardrails et escalade
  - Dispositifs de gouvernance
  - Analyse STRIDE / OWASP de la gouvernance
  - Chemins d'escalade et de validation humaine
  - Plancher non contournable (SG-3)
types_presentation: [securite]
sensibilite: restreint
togaf_layer: application
ordre_presentation: 5
---
## Gouvernance — gates, guardrails et escalade

<!--
Fichier `05` : analyse de la **gouvernance de sécurité** — gates (points de contrôle), guardrails (garde-fous) et chemins d'escalade — **sous l'angle STRIDE / OWASP**. La gouvernance est elle-même une surface : un gate contournable, un guardrail désactivable sans trace ou une escalade mal bornée sont des défauts de sécurité.
Relier aux surfaces (`S1…Sn` du `01`), aux menaces (`STR-xxx` du `02`) et aux risques OWASP (`A0x` du `03`). Ne pas redéfinir le fonctionnement du workflow ; en **analyser la sécurité**.
-->

### Dispositifs de gouvernance

<!--
Recenser les dispositifs : gates (points de contrôle bloquants ou advisory), guardrails (garde-fous préventifs), mécanismes de validation humaine granulaire, revues obligatoires. Pour chacun : rôle, caractère (bloquant / advisory), portée, trace produite.
-->

| ID       | Dispositif | Type (gate / guardrail / revue / validation) | Caractère (bloquant / advisory) | Rôle | Trace produite |
| -------- | ---------- | -------------------------------------------- | ------------------------------- | ---- | -------------- |
| GOV-001  |            |                                              |                                 |      |                |

**Tableau. Dispositifs de gouvernance**

### Analyse STRIDE / OWASP de la gouvernance

<!--
Appliquer STRIDE et OWASP aux dispositifs de gouvernance eux-mêmes. Exemples de questions : un gate peut-il être usurpé (S) ou contourné (E) ? un guardrail peut-il être désactivé sans trace (R / T) ? une escalade peut-elle divulguer de l'information (I) ou être saturée (D) ? Mauvaise configuration des contrôles (OWASP A05), défaillance de journalisation / surveillance (A09), contrôle d'accès défaillant sur l'administration des gates (A01).
Une ligne par couple (dispositif × menace retenue). Risque résiduel `P × I` ; renvois `STR-xxx` / `A0x` / recommandation (`06`).
-->

| ID       | Dispositif (`GOV-xxx`) | Catégorie STRIDE | Risque OWASP (`A0x`) | Menace / Scénario | Contre-mesure(s) | Risque résiduel (`P × I`) | Renvois (`STR` / `06`) |
| -------- | ---------------------- | ---------------- | -------------------- | ----------------- | ---------------- | ------------------------- | ---------------------- |
| GSEC-001 |                        |                  |                      |                   |                  | Faible/Moyen/Élevé/Critique |                      |

**Tableau. Analyse STRIDE / OWASP de la gouvernance**

### Chemins d'escalade et de validation humaine

<!--
Décrire les **chemins d'escalade** vers une décision humaine et la **validation humaine granulaire** : déclencheur, destinataire, décision attendue, trace. Préciser quels changements exigent impérativement une validation humaine (notamment tout abaissement d'un contrôle de sécurité).
-->

| ID       | Chemin d'escalade | Déclencheur | Destinataire (humain) | Décision attendue | Trace produite |
| -------- | ----------------- | ----------- | --------------------- | ----------------- | -------------- |
| ESC-001  |                   |             |                       |                   |                |

**Tableau. Chemins d'escalade et de validation humaine**

### Plancher non contournable (SG-3)

<!--
Rappeler explicitement les invariants du plancher SG-3 (fiche agent `security-reviewer-agent`), que la gouvernance doit garantir :
  - la **revue de sécurité est obligatoire et non substituable** dès qu'une architecture ou une surface de sécurité est produite ou modifiée ; aucun gate / sensor advisory ni revue de cohérence ne peut la porter, la remplacer, la conditionner ou la court-circuiter ; un « vert » de gate ne dispense jamais de la revue de sécurité ;
  - la revue de sécurité **précède toujours** la validation humaine granulaire sur toute modification d'architecture ;
  - **aucun niveau de contrôle de sécurité ne peut être abaissé sans validation humaine explicite tracée**.
Indiquer comment les dispositifs ci-dessus concrétisent ce plancher et où les violations potentielles ont été analysées (lignes `GSEC-xxx`).
-->
