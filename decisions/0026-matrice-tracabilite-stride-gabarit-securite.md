# Matrice de traçabilité STRIDE dans le gabarit de sécurité de la DAS

---
auteurs: multica.gaston  
accepté par : ""  
accepté le : ""  
supersedes: ""  
superseded_by: ""  

---

## Status

Proposed

> Statut **Proposed** — la modification de gabarit a été validée par l'humain (multica.gaston, 2026-09-10) et publiée en PR. Le passage à **Accepted** reste subordonné à la validation humaine granulaire explicite de cet ADR et au contrôle sécurité (Architecte cybersécurité / Reviewer de sécurité), conformément à l'invariant de gouvernance A2A (« aucun ADR accepté sans validation humaine », cf. [ADR-0025](0025-durcissement-required-sections-das.md)). Aucune posture de sécurité n'est modifiée ici : l'ajout est une **rubrique de gabarit** (advisory par nature), les clauses SG-1 à SG-6 ([ADR-0005](0005-verification-gates-et-sensors.md)) sont préservées à l'identique.

## Contexte

Les architectes rédigent la documentation d'architecture de solution (DAS) à partir des gabarits de la skill `architecture-solution-gabarits` (`plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/`). Le gabarit [`11-securite.md`](../plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/11-securite.md) — fichier **mandatory** de la DAS au titre de l'[ADR-0025](0025-durcissement-required-sections-das.md) — porte la sous-section **« Modélisation des menaces (STRIDE) »** que le workflow `core` réalise en phase de conception, pour chaque composant / flux identifié dans `06-architecture-solutions.md`.

Jusqu'ici, ce gabarit décrivait *l'obligation* de mener l'analyse STRIDE et alimentait deux tableaux de vulnérabilités (`Sécurité applicative` — VUL-0xx, `Sécurité Infrastructure` — VUL-1xx), eux-mêmes liés au registre des risques (`RISQ-xxx` du `04-risques.md`). Mais **aucune structure ne matérialisait la traçabilité de bout en bout** entre :

- chaque **composant / flux** (`06-architecture-solutions.md`),
- les **6 catégories STRIDE** (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege),
- la **contre-mesure**, la **vulnérabilité** (`VUL-xxx`) et le **risque** (`RISQ-xxx`) correspondants.

L'humain (multica.gaston) demande d'ajouter au gabarit une **matrice de traçabilité STRIDE** afin que, lorsque l'analyse STRIDE est faite dans le workflow `core`, la couverture (composant × catégorie) et la traçabilité menace → mitigation → vulnérabilité → risque soient documentées de façon explicite et vérifiable.

## Décision

**Ajouter au gabarit [`11-securite.md`](../plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/11-securite.md) une sous-section `#### Matrice de traçabilité STRIDE`**, insérée immédiatement après « Modélisation des menaces (STRIDE) » et avant « Sécurité applicative ».

**Contenu de la matrice** (`Tableau 55`) — une ligne par couple **(composant/flux × catégorie STRIDE applicable)**, avec les colonnes :

| Colonne | Rôle |
| --- | --- |
| ID (`STR-xxx`) | Identifiant stable de la ligne de traçabilité |
| Composant / Flux (`06`) | Renvoi vers `06-architecture-solutions.md` |
| Catégorie STRIDE | `S` / `T` / `R` / `I` / `D` / `E` |
| Propriété compromise | Authenticité / Intégrité / Traçabilité / Confidentialité / Disponibilité / Autorisation |
| Menace identifiée | Description de la menace |
| Vecteur / Scénario | Scénario d'exploitation |
| Contre-mesure(s) | Mitigation retenue |
| Vraisemblance | Échelle **harmonisée** avec `04-risques.md` |
| Niveau de risques | Échelle **harmonisée** avec `04-risques.md` |
| Lien vulnérabilité (`VUL-xxx`) | Renvoi vers `Sécurité applicative` / `Sécurité Infrastructure` (sans duplication) |
| Lien registre des risques (`04`) | Renvoi `RISQ-xxx` |
| Statut | Aligné sur les statuts du `04-risques.md` |

**Règle de couverture** — chaque composant/flux est décliné sur les 6 catégories STRIDE ; une catégorie non applicable est indiquée `N/A` avec justification plutôt qu'omise, afin de démontrer la couverture complète.

**Harmonisation** — les échelles de *Vraisemblance* / *Niveau de risques* et les *statuts* renvoient au `04-risques.md` (mêmes échelles), et les liens `VUL-xxx` / `RISQ-xxx` évitent toute duplication du détail des vulnérabilités et des risques.

**Numérotation des tableaux** — la matrice devient `Tableau 55`, s'enchaînant proprement avec les tableaux existants 56 (Vulnérabilités applicatives), 57 (Infrastructure) et 58 (GIA).

**Caractère advisory / non structurant** — cet ajout est une **rubrique de gabarit** (asset de skill, outil de travail de l'architecte, règle d'or n°3) ; il n'introduit **aucun couplage `core → plugin`**, ne modifie **aucun sensor** ni aucune posture de sécurité (SG-1 à SG-6 inchangées).

## Conséquences

### Positives

- **POS-001** : Traçabilité STRIDE **de bout en bout** matérialisée (composant/flux → catégorie → menace → contre-mesure → `VUL-xxx` → `RISQ-xxx`), là où seule l'obligation d'analyse était décrite.
- **POS-002** : **Couverture explicite** des 6 catégories par composant (dont les `N/A` justifiés), facilitant la revue de complétude de la DAS et le contrôle sécurité.
- **POS-003** : Échelles et statuts **harmonisés** avec le `04-risques.md` et liens `VUL`/`RISQ` **sans duplication** — cohérence documentaire préservée.
- **POS-004** : Aucun couplage `core → plugin`, aucun sensor modifié, posture de sécurité (SG-1 à SG-6) et caractère advisory **inchangés**.

### Négatives

- **NEG-001** : Cohérence à maintenir entre la matrice STRIDE et les tableaux de vulnérabilités (`VUL-xxx`) ainsi que le registre des risques (`RISQ-xxx`) ; atténuée par les liens explicites et la revue de PR.
- **NEG-002** : Charge de rédaction accrue pour l'architecte (6 lignes par composant/flux) ; atténuée par la règle `N/A` justifié et par le caractère advisory (aucun blocage).
- **NEG-003** : Le gabarit `11-securite.md` étant **mandatory** ([ADR-0025](0025-durcissement-required-sections-das.md)), toute évolution de son découpage doit rester cohérente avec le manifeste `required-sections` — cf. règle de cohérence gabarit ↔ manifeste (NEG-004 d'[ADR-0012](0012-alignement-sensors-sur-ai-dlc.md)). L'ajout d'une **sous-section** n'affecte pas la liste des sections mandatory portée par le manifeste, mais la vérification de cohérence reste à confirmer en revue.

## Alternatives étudiées

### ALT-001 — Ne pas ajouter de matrice (statu quo)

Conserver la seule sous-section « Modélisation des menaces (STRIDE) » et les tableaux de vulnérabilités.

**Raison du rejet** : ne matérialise pas la traçabilité composant × catégorie STRIDE → mitigation → vulnérabilité → risque, et ne répond pas au besoin exprimé de tracer la couverture et la traçabilité de l'analyse STRIDE.

### ALT-002 — Placer la matrice dans un fichier de gabarit distinct

Créer un nouveau gabarit dédié à la traçabilité STRIDE.

**Raison du rejet** : fragmenterait la section Sécurité, multiplierait les fichiers mandatory à synchroniser et éloignerait la matrice de son contexte immédiat (modélisation des menaces, tableaux de vulnérabilités). Le regroupement dans `11-securite.md` préserve la cohérence de lecture.

### ALT-003 — Étendre les tableaux de vulnérabilités existants avec une colonne « catégorie STRIDE »

Ajouter les colonnes STRIDE aux tableaux `VUL-xxx` plutôt qu'une matrice dédiée.

**Raison du rejet** : les tableaux de vulnérabilités partent de la vulnérabilité constatée, pas de la couverture systématique composant × catégorie ; ils ne permettent pas d'exprimer les `N/A` justifiés ni la couverture des 6 catégories par composant. La matrice dédiée et les tableaux restent complémentaires, reliés par `VUL-xxx`.

## Notes d'implémentation

- **IMP-001** : [`plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/11-securite.md`](../plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/11-securite.md) — ajout de la sous-section `#### Matrice de traçabilité STRIDE` (bloc de consignes de remplissage + `Tableau 55`) entre « Modélisation des menaces (STRIDE) » et « Sécurité applicative ». Tableaux suivants renumérotés en 56/57/58 (enchaînement conservé).
- **IMP-002** : Cohérence gabarit ↔ manifeste (NEG-004, [ADR-0012](0012-alignement-sensors-sur-ai-dlc.md)) à vérifier en revue : l'ajout d'une sous-section n'altère pas la liste des sections mandatory portée par [`required-sections`](../core/sensors/sensors/required-sections.md) ; à confirmer par l'Architecte cybersécurité.
- **IMP-003** : Contrôle sécurité (Architecte cybersécurité / Reviewer de sécurité) requis **avant** passage à *Accepted* ; clauses SG-1 à SG-6 reconduites sans changement.
- **IMP-004** : PR portant la modification du gabarit : [homelab-portfolio#118](https://github.com/Gsyltc/homelab-portfolio/pull/118).

## Références

- **REF-001** : [ADR-0025 — Durcissement du sensor required-sections (volet DAS)](0025-durcissement-required-sections-das.md) — `11-securite.md` comme fichier mandatory de la DAS
- **REF-002** : [ADR-0005 — Verification gates et Sensors déterministes advisory](0005-verification-gates-et-sensors.md)
- **REF-003** : [ADR-0012 — Alignement des manifestes de sensors sur le contrat AI-DLC « Sensors »](0012-alignement-sensors-sur-ai-dlc.md)
- **REF-004** : [`plugins/architecture-assistant/skills/cybersecurite/principles/stride.md`](../plugins/architecture-assistant/skills/cybersecurite/principles/stride.md) — modèle STRIDE (6 catégories, propriétés, contre-mesures)
- **REF-005** : [`plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/04-risques.md`](../plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/04-risques.md) — registre des risques (échelles, statuts, `RISQ-xxx`)
