## Revue de sécurité

<!--
Gabarit de **revue de sécurité** (jeu B), produit par le **Reviewer de sécurité** (`security-reviewer-agent`). **Review-only** : ce document ne produit **aucune** architecture ; il **structure un verdict** motivé sur un livrable de sécurité existant (en règle générale le dossier `documentation/architecture-securite/` produit avec le jeu A, ou toute surface de sécurité produite / modifiée).
Il n'y a **pas** de front-matter de ciblage sur ce fichier : ce n'est pas un livrable d'architecture présentable, c'est un contrôle.
Rappel du socle (skill `cybersecurite`) : **OWASP Top 10 et STRIDE toujours actifs** ; COBIT / NIST si l'analyse documente les risques ; PCI DSS / GDPR / Loi 25 / LPRPDE **uniquement si explicitement demandés**. Ne jamais activer seul une norme non demandée.
-->

### Livrable revu

<!--
Identifier précisément ce qui est revu, pour que la revue soit rejouable et traçable.
-->

| Attribut | Valeur |
| -------- | ------ |
| Livrable revu (chemin) |  |
| Version / `digest` |  |
| Date de la revue |  |
| Reviewer |  |
| Demandeur / coordinateur |  |
| Socle normatif activé | OWASP + STRIDE (toujours) ; autres : préciser si explicitement demandés |

**Tableau. Identification du livrable revu**

### Grille de revue STRIDE / OWASP

<!--
Évaluer la **couverture** du livrable, par surface (`S1…Sn`) et par risque, selon trois états : **couvert** / **partiel** / **manquant**. Une ligne par (surface × axe d'analyse) pertinent. Renvoyer aux éléments du livrable (`STR-xxx`, `A0x`).
-->

| Surface (`S1…Sn`) | Axe (STRIDE catégorie / OWASP `A0x`) | Couverture (couvert / partiel / manquant) | Constat | Renvoi livrable (`STR-xxx` / `A0x`) |
| ----------------- | ------------------------------------ | ----------------------------------------- | ------- | ----------------------------------- |
| S1 | S (Spoofing) |  |  |  |
| S1 | A01 (Broken Access Control) |  |  |  |

**Tableau. Grille de revue STRIDE / OWASP**

### Constats à sévérité

<!--
Lister les constats de la revue, chacun avec une **sévérité** sur l'échelle commune `Faible` / `Moyen` / `Élevé` / `Critique`, et son caractère **bloquant** ou **non-bloquant** pour le verdict. ID stable `CST-xxx`.
-->

| ID (`CST-xxx`) | Constat | Sévérité (Faible/Moyen/Élevé/Critique) | Bloquant (oui / non) | Élément concerné (surface / risque / contrôle) | Correction attendue |
| -------------- | ------- | -------------------------------------- | -------------------- | ---------------------------------------------- | ------------------- |
| CST-001 |  | Faible/Moyen/Élevé/Critique | oui / non |  |  |

**Tableau. Constats de revue à sévérité**

### Verdict motivé

<!--
Rendre un **verdict** parmi : **FAVORABLE** / **FAVORABLE sous réserve** / **DÉFAVORABLE**, et le **motiver** explicitement par renvoi aux constats (`CST-xxx`).
  - **FAVORABLE** — aucun constat bloquant ; la couverture STRIDE / OWASP est jugée suffisante.
  - **FAVORABLE sous réserve** — constats non-bloquants à traiter ; lister les réserves non-bloquantes.
  - **DÉFAVORABLE** — au moins un constat bloquant ; la revue ne peut conclure favorablement en l'état.
Séparer clairement **réserves bloquantes** et **réserves non-bloquantes**.
-->

| Verdict | FAVORABLE / FAVORABLE sous réserve / DÉFAVORABLE |
| ------- | ------------------------------------------------ |
| Motivation (renvoi `CST-xxx`) |  |
| Réserves **bloquantes** |  |
| Réserves **non-bloquantes** |  |

**Tableau. Verdict de revue**

### Invariants du plancher SG-3

<!--
Rappeler explicitement, à chaque revue, les invariants non contournables (fiche `security-reviewer-agent`). Ne pas les reformuler à la baisse.
-->

- **Revue non substituable** : aucune revue de cohérence, aucun gate / sensor advisory ne peut porter, remplacer, conditionner ni court-circuiter la revue de sécurité. Un « vert » de gate ne dispense jamais de cette revue.
- **Antériorité sur la validation humaine** : la revue de sécurité **précède toujours** la validation humaine granulaire sur toute modification d'architecture ou de surface de sécurité.
- **Aucun abaissement sans validation humaine tracée** : un niveau de contrôle lié à la sécurité **ne peut jamais être abaissé** sans **validation humaine explicite et tracée**.
- **Review-only** : cette revue ne produit aucune architecture ; elle structure uniquement le verdict.
