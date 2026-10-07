---
doc_id: secu-02-menaces-stride
theme: Menaces (STRIDE) par surface — matrice de synthèse et analyse détaillée
domaine: [securite]
sujets:
  - Menaces (STRIDE) par surface
  - Matrice de synthèse STRIDE par surface
  - Analyse détaillée par surface
types_presentation: [securite]
sensibilite: restreint
togaf_layer: technology
ordre_presentation: 2
---
## Menaces (STRIDE) par surface

<!--
Fichier `02` : modélisation des menaces **STRIDE** appliquée à chaque **surface d'attaque** (`S1…Sn`) définie dans `01-surfaces-et-actifs.md`.
STRIDE fait partie du **socle toujours actif** (voir `cybersecurite`) : Spoofing (S), Tampering (T), Repudiation (R), Information disclosure (I), Denial of service (D), Elevation of privilege (E).
Conventions (cf. ADR-0026, [`../../decisions/0026-matrice-tracabilite-stride-gabarit-securite.md`](../../decisions/0026-matrice-tracabilite-stride-gabarit-securite.md)) :
  - **Une ligne par couple (surface × catégorie STRIDE applicable)**. Une catégorie non applicable est indiquée `N/A` **avec justification** plutôt qu'omise, pour démontrer la couverture complète.
  - **Vraisemblance** et **Niveau de risques** : échelle commune `Faible` / `Moyen` / `Élevé` / `Critique`, harmonisée avec le `04-risques.md` de la DAS.
  - **Lien vulnérabilité** `VUL-xxx` et **Lien registre des risques** `RISQ-xxx` : renvois vers le `11-securite.md` / `04-risques.md` de la DAS, **sans duplication** du détail.
  - **ID `STR-xxx`** : identifiant stable de la ligne de traçabilité.
-->

### Matrice de synthèse STRIDE par surface

<!--
Vue de synthèse : couverture STRIDE de chaque surface. Une ligne par couple (surface × catégorie). Reporter l'ID de surface `S1…Sn` du `01`. Les N/A justifiés restent présents.
-->

| ID (`STR-xxx`) | Surface (`S1…Sn`) | Catégorie STRIDE | Propriété compromise | Menace identifiée | Vecteur / Scénario | Contre-mesure(s) | Vraisemblance | Niveau de risques | Lien vulnérabilité (`VUL-xxx`) | Lien registre des risques (`04`) | Statut |
| -------------- | ----------------- | ---------------- | -------------------- | ----------------- | ------------------ | ---------------- | ------------- | ----------------- | ------------------------------ | -------------------------------- | ------ |
| STR-001 | S1 | S (Spoofing)          | Authenticité     |  |  |  | Faible/Moyen/Élevé/Critique | Faible/Moyen/Élevé/Critique | - VUL-xxx | - RISQ-xxx | |
| STR-002 | S1 | T (Tampering)         | Intégrité        |  |  |  | Faible/Moyen/Élevé/Critique | Faible/Moyen/Élevé/Critique | - VUL-xxx | - RISQ-xxx | |
| STR-003 | S1 | R (Repudiation)       | Traçabilité      |  |  |  | Faible/Moyen/Élevé/Critique | Faible/Moyen/Élevé/Critique | - VUL-xxx | - RISQ-xxx | |
| STR-004 | S1 | I (Info. disclosure)  | Confidentialité  |  |  |  | Faible/Moyen/Élevé/Critique | Faible/Moyen/Élevé/Critique | - VUL-xxx | - RISQ-xxx | |
| STR-005 | S1 | D (Denial of service) | Disponibilité    |  |  |  | Faible/Moyen/Élevé/Critique | Faible/Moyen/Élevé/Critique | - VUL-xxx | - RISQ-xxx | |
| STR-006 | S1 | E (Elev. of privilege)| Autorisation     |  |  |  | Faible/Moyen/Élevé/Critique | Faible/Moyen/Élevé/Critique | - VUL-xxx | - RISQ-xxx | |

**Tableau. Matrice de synthèse STRIDE par surface**

### Analyse détaillée par surface

<!--
Pour chaque surface `S1…Sn`, dérouler l'analyse. Dupliquer le bloc `#### Surface Sn — <nom>` autant de fois qu'il y a de surfaces. Reprendre l'ID et le nom exacts du `01`.
-->

#### Surface S1 — <nom de la surface>

<!--
Décrire la surface (rappel bref depuis `01`, sans la redéfinir), puis l'analyse STRIDE détaillée des menaces retenues pour cette surface.
Pour chaque catégorie STRIDE applicable :
  - **Menace** et **scénario d'exploitation** (vecteur) ;
  - **Propriété compromise** (CIA + authenticité / traçabilité / autorisation) ;
  - **Contre-mesure(s)** retenue(s) et **risque résiduel** `P × I` (après contre-mesures) sur l'échelle `Faible…Critique` ;
  - renvois `STR-xxx` (matrice ci-dessus), `VUL-xxx` / `RISQ-xxx` (DAS), et croisement OWASP (`A0x` du `03-risques-owasp.md`).
Indiquer explicitement les catégories `N/A` et leur justification.
-->

| Catégorie STRIDE | Applicable | Menace / Scénario | Contre-mesure(s) | Risque résiduel (`P × I`) | Renvois (`STR` / `VUL` / `RISQ` / OWASP) |
| ---------------- | ---------- | ----------------- | ---------------- | ------------------------- | ---------------------------------------- |
| S (Spoofing)           | Oui / N/A |  |  | Faible/Moyen/Élevé/Critique |  |
| T (Tampering)          | Oui / N/A |  |  | Faible/Moyen/Élevé/Critique |  |
| R (Repudiation)        | Oui / N/A |  |  | Faible/Moyen/Élevé/Critique |  |
| I (Info. disclosure)   | Oui / N/A |  |  | Faible/Moyen/Élevé/Critique |  |
| D (Denial of service)  | Oui / N/A |  |  | Faible/Moyen/Élevé/Critique |  |
| E (Elev. of privilege) | Oui / N/A |  |  | Faible/Moyen/Élevé/Critique |  |

**Tableau. Analyse STRIDE détaillée — Surface S1**

<!-- Répéter le bloc `#### Surface Sn — <nom>` ci-dessus pour chaque surface S2, S3, … Sn du `01`. -->
