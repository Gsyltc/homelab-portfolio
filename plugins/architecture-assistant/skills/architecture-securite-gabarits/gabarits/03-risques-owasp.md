---
doc_id: secu-03-risques-owasp
theme: Risques OWASP Top 10 — table de couverture et fiches par risque
domaine: [securite]
sujets:
  - Risques OWASP Top 10
  - Table de couverture OWASP Top 10
  - Fiches de risque (A01…A10)
types_presentation: [securite]
sensibilite: restreint
togaf_layer: application
ordre_presentation: 3
---
## Risques OWASP Top 10

<!--
Fichier `03` : application du référentiel **OWASP Top 10** (socle toujours actif, voir `cybersecurite`) aux surfaces d'attaque (`S1…Sn` du `01`) et aux menaces STRIDE (`02`).
  - La **table de couverture** donne, pour chacun des 10 risques, son applicabilité au projet et son renvoi vers les surfaces concernées.
  - Chaque risque applicable fait l'objet d'une **fiche** `A01…A10`.
  - Échelle commune `Faible` / `Moyen` / `Élevé` / `Critique` ; risque **résiduel** `P × I` après contre-mesures ; renvois `VUL-xxx` / `RISQ-xxx` vers la DAS sans duplication.
Les identifiants `A01…A10` sont **stables** (édition OWASP 2021). Un risque non applicable est conservé dans la table avec la mention `N/A` justifiée (couverture complète).
-->

### Table de couverture OWASP Top 10

<!--
Vue de synthèse des 10 risques. Pour chaque risque : applicabilité (Oui / N/A justifié), surfaces concernées (`S1…Sn`), niveau de risque résiduel, renvoi vers la fiche et le registre des risques.
-->

| ID  | Risque OWASP (2021)                               | Applicable | Surfaces (`S1…Sn`) | Niveau de risque résiduel | Lien registre des risques (`04`) |
| --- | ------------------------------------------------- | ---------- | ------------------ | ------------------------- | -------------------------------- |
| A01 | Broken Access Control                             | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |
| A02 | Cryptographic Failures                            | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |
| A03 | Injection                                         | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |
| A04 | Insecure Design                                   | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |
| A05 | Security Misconfiguration                         | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |
| A06 | Vulnerable and Outdated Components                | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |
| A07 | Identification and Authentication Failures        | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |
| A08 | Software and Data Integrity Failures              | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |
| A09 | Security Logging and Monitoring Failures          | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |
| A10 | Server-Side Request Forgery (SSRF)                | Oui / N/A  |                    | Faible/Moyen/Élevé/Critique | - RISQ-xxx |

**Tableau. Couverture OWASP Top 10**

### Fiches de risque (A01…A10)

<!--
Une fiche par risque **applicable**. Dupliquer le bloc `#### A0x — <nom>` pour chaque risque retenu. Pour un risque `N/A`, conserver une fiche courte justifiant la non-applicabilité.
Chaque fiche :
  - **Description contextualisée** du risque pour le projet ;
  - **Surfaces concernées** (`S1…Sn`) et **menaces STRIDE** liées (`STR-xxx` du `02`) ;
  - **Vulnérabilités** associées (`VUL-xxx`, renvoi DAS, sans duplication) ;
  - **Contre-mesures** et **risque résiduel** `P × I` sur l'échelle `Faible…Critique` ;
  - **Recommandation(s)** liée(s) (`R-11A-*` / `R-11B-*` du `06`).
-->

#### A01 — Broken Access Control

<!-- Description contextualisée. -->

| Attribut | Valeur |
| -------- | ------ |
| Surfaces concernées (`S1…Sn`) |  |
| Menaces STRIDE liées (`STR-xxx`) |  |
| Vulnérabilités (`VUL-xxx`) |  |
| Contre-mesure(s) |  |
| Risque résiduel (`P × I`) | Faible/Moyen/Élevé/Critique |
| Recommandation(s) liée(s) (`06`) |  |
| Lien registre des risques (`04`) | - RISQ-xxx |

**Tableau. Fiche de risque OWASP A01**

<!-- Répéter le bloc `#### A0x — <nom>` ci-dessus pour A02…A10, selon applicabilité. -->
