# PRIORITÉ : Ce workflow est PRIORITAIRE sur tous les autres workflows intégrés

# Lorsqu'un humain ou un agent demande la création, la modification ou l'évolution d'une architecture, d'une solution ou d'un système, TOUJOURS suivre ce workflow EN PREMIER

Ce workflow est le contrat commun d'orchestration **multi-agents (A2A)** des travaux d'architecture du workspace. Il est coordonnée par **l'Architecture Solution & Intégration**.

Le workflow est **agnostique de la méthodologie**. Aucune méthode n'est imposée par défaut. Au besoin, il peut être **activé avec une méthodologie particulière** — par exemple **OpenSpec** (spec-driven), **BMAD**, ou **toute autre méthodologie** — **en fonction du contexte du projet**. La méthodologie retenue est déclarée au niveau du projet ou de l'issue (voir « Activation conditionnelle d'une méthodologie »). En l'absence de méthodologie déclarée, le workflow suit le parcours d'architecture standard.

---

## Principe fondateur : le workflow s'adapte au travail

**Le workflow s'adapte au travail, et non l'inverse.** Le coordinateur et chaque agent évaluent quelles étapes apportent de la valeur, en fonction de :

1. L'intention déclarée (par l'humain ou l'agent appelant) et sa clarté
2. L'état existant du système (documentation d'architecture, ADR, code, infrastructure)
3. La complexité et la portée du changement
4. L'évaluation des risques et de l'impact (dont sécurité)

Une modification simple reste efficace (traitement minimal) ; une modification complexe ou à risque reçoit un traitement complet.

Ce principe est **outillé** par le mécanisme de **scopes** (quelles étapes s'exécutent) et par deux **axes d'exécution indépendants** — **Depth** (détail des artefacts) et **niveau de vérification des livrables** (rigueur du contrôle) — décrits ci-dessous.

---

## Scopes et axes d'exécution

Le routage du travail n'est plus laissé au seul jugement subjectif : il repose sur un **scope** nommé (parcours d'étapes déterministe et auditable) et sur deux **axes indépendants** qui règlent, séparément, le détail des artefacts et la rigueur de leur vérification.

> Adaptation d'AI-DLC 2.0 (`awslabs/aidlc-workflows/core/scopes`) au contexte du workspace : architecture de solution, AWS, infrastructure Windows, livrables majoritairement documentaires. Décision structurante tracée dans [ADR-0003](../decisions/0003-scopes-et-axes-depth-verification.md).

### Table des scopes

| Scope | Intention type | Traitement |
| --- | --- | --- |
| `standard` *(défaut)* | Évolution ou conception d'architecture « normale » | Parcours d'architecture standard complet |
| `feature` | Ajout / évolution fonctionnelle d'une solution | Inception ciblée + Construction, sécurité systématique |
| `infra` | Infra / plateforme (AWS, réseau, Windows, migration) | Accent Architecte AWS / Admin Infrastructure Windows, rollback obligatoire |
| `security-patch` | Correction / durcissement de sécurité | **Architecte cybersécurité pilote**, périmètre resserré, traçabilité renforcée |
| `mvp` | Produit minimum viable — première version fonctionnelle à faire évoluer | Parcours ciblé sur le cœur de valeur, Depth standard, dette technique tracée |
| `poc` | Preuve de concept / exploration jetable | Allégé, Depth minimale, pas d'exigence de complétude documentaire |
| `express` | Petit changement clair et à faible risque | Chemin court : cadrage + décision + validation, étapes lourdes ignorées |
| `enterprise` | Chantier structurant, fort impact / conformité | Parcours complet + Depth comprehensive + normes conditionnelles activables |

Le scope par **défaut**, en l'absence de mot-clé détecté, est **`standard`** (parcours d'architecture actuel — aucune régression, compatibilité ascendante).

**Invariants non négociables, quel que soit le scope** — aucun scope ne peut les désactiver, y compris `poc` et `express` :

- Validation humaine granulaire (chaque choix validé / rejeté séparément).
- ADR sur chaque décision structurante.
- Piste d'audit sur l'issue.
- Contrôle sécurité minimal toujours actif (OWASP / STRIDE).

### Matrice stage × scope

Adossée à la structure actuelle du workflow (phases Inception / Construction / Operation ; le passage structurel aux 5 phases AI-DLC est traité ultérieurement). Légende : ✅ activé · ➖ allégé / optionnel · ❌ ignoré · 🔒 renforcé · *cond.* conditionnel.

| Étape | `standard` | `feature` | `infra` | `security-patch` | `mvp` | `poc` | `express` | `enterprise` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.1 Cadrage | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 1.2 Contexte existant | ➖ | ✅ | ✅ | ✅ | ➖ | ❌ | ➖ | ✅ |
| 1.3 Analyse besoins | ✅ | ✅ | ✅ | ✅ 🔒 [^sp13] | ✅ | ➖ | ➖ [^ex] | ✅ 🔒 [^ent13] |
| 1.4 Découpage livrables | ✅ | ✅ | ✅ | ➖ | ✅ | ➖ | ➖ | ✅ |
| 1.5 Conception + ADR | ✅ | ✅ | ✅ | ✅ 🔒 | ✅ | ➖ | ➖ | ✅ 🔒 |
| Contrôle sécurité (Architecte cybersécurité) | ✅ | ✅ | ✅ | 🔒 pilote | ✅ | ➖ | ➖ | ✅ 🔒 |
| 2.1 Livrables détaillés | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ✅ |
| 2.2 Sécurité + cohérence | ✅ | ✅ | ✅ | 🔒 | ✅ | ➖ | ➖ [^ex] | ✅ 🔒 |
| 2.3 Consolidation + mise à disposition | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ✅ | ✅ |
| 3.x Operation / déploiement | *cond.* | *cond.* | ✅ | *cond.* | *cond.* | ❌ | *cond.* [^ex] | ✅ |
| Validation humaine granulaire | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

[^sp13]: `security-patch` — l'étape `1.3` couvre a minima l'**analyse d'impact du correctif** : surface affectée, effets de bord, non-régression de sécurité. Exigence, pas option (un correctif sans analyse d'impact peut rouvrir ou déplacer la vulnérabilité).
[^ex]: `express` — l'allègement est réservé aux changements **sans impact runtime / production**. **Dès qu'un `express` implique un déploiement ou une action à impact** (`3.x` ≠ ❌), l'étape `2.2 Sécurité + cohérence` repasse à **✅** (non ➖) et la vérification à **`standard`** minimum.
[^ent13]: `enterprise` — l'étape `1.3` inclut deux pré-requis obligatoires : (a) une **classification des données traitées** (publiques / internes / sensibles / réglementées), et (b) un **point de contrôle « applicabilité des normes »** (voir « Renforcements sécurité par scope »).

#### Renforcements sécurité par scope

Ces clauses, issues du contrôle sécurité (Architecte cybersécurité), sont **contraignantes** — elles ferment les vecteurs d'abaissement de la posture de sécurité par le routage lui-même :

- **`security-patch` — analyse d'impact obligatoire** : l'étape `1.3` couvre l'impact du correctif (surface affectée, effets de bord, non-régression), même en traitement resserré. *(voir [^sp13])*
- **`enterprise` — applicabilité des normes tracée** : point de contrôle obligatoire où l'Architecte cybersécurité et l'humain **statuent explicitement** sur l'applicabilité de chaque norme candidate (PCI DSS / GDPR / Loi 25 / LPRPDE). La décision — **y compris « aucune norme spécifique requise »** — est **tracée en ADR** (sinon la conformité repose sur un oubli possible).
- **`enterprise` — classification des données** : pré-requis en `1.3` ; c'est elle qui conditionne l'activation des normes et le niveau `renforcé`. *(voir [^ent13])*
- **`express` — pas d'allègement sur action à impact** : réservé au sans-impact runtime/production ; sur déploiement ou action à impact, `2.2` = ✅ et vérification ≥ `standard`. *(voir [^ex])*
- **`poc` — non promouvable directement** : un PoC est **jetable par construction**. Il ne peut **jamais** être promu tel quel ; toute reprise en `feature` / `mvp` / `enterprise` **re-déclenche le contrôle sécurité complet du scope cible**.


**Affectation des agents par scope** (déclencheurs A2A) :

- `feature`, `standard`, `mvp`, `enterprise` → Architecte de solution (+ Architecte AWS si cloud) ; Architecte cybersécurité systématique.
- `infra` → Architecte AWS et/ou Admin Infrastructure Windows au premier plan ; plan de rollback validé avant toute action destructive.
- `security-patch` → **Architecte cybersécurité pilote l'analyse** ; Architecte de solution en appui documentaire.
- `poc`, `express` → Architecte de solution seul ; contrôle sécurité allégé mais toujours présent.
- La mise à disposition des livrables validés est confiée au **Gestionnaire de document**.
- OpenSpec (Fabien) reste **conditionnel** à tous les scopes, jamais imposé.

### Auto-détection du scope

Le scope est **auto-détecté** par mots-clés dans l'intention exprimée en langage libre (français / anglais), puis **confirmé explicitement avant démarrage** — jamais de démarrage silencieux sur un scope simplement déduit.

| Scope | Mots-clés FR | Mots-clés EN |
| --- | --- | --- |
| `standard` *(défaut)* | *(aucun mot-clé — scope retenu par défaut si aucun autre ne correspond)* | *(no keyword — default fallback)* |
| `feature` | fonctionnalité, évolution, ajouter, nouvelle capacité | feature, capability, add |
| `infra` | infrastructure, réseau, AWS, VM, migration, Windows, Intune, golden image | infra, network, deploy, migration, platform |
| `security-patch` | sécurité, faille, vulnérabilité, correctif, durcissement, CVE | security, vulnerability, patch, hardening, CVE |
| `mvp` | mvp, produit minimum viable, première version, version initiale, socle | mvp, minimum viable product, first version, initial release |
| `poc` | poc, preuve de concept, prototype, explorer, maquette | poc, proof of concept, prototype, spike |
| `express` | rapide, petit, mineur, trivial, urgent | express, quick, small, minor |
| `enterprise` | conformité, PCI, GDPR, Loi 25, audit, critique, entreprise | enterprise, compliance, audit, critical |

**Règle de désambiguïsation** — en cas de plusieurs correspondances, l'ordre de priorité est :

`security-patch` > `enterprise` > `infra` > `feature` > `mvp` > `poc` > `express` > `standard`

La sécurité et la conformité priment ; à défaut de tout mot-clé, le scope retenu est `standard`. En cas d'ambiguïté résiduelle ou de conflit fort, le coordinateur **propose le scope détecté et demande confirmation** plutôt que de trancher seul.

### Axe 1 — Depth (détail des artefacts)

Règle le niveau de détail des artefacts produits, **indépendamment** du scope et de l'axe de vérification :

- `minimal` : intention documentée, décision essentielle, pas de vues exhaustives.
- `standard` : besoins fonctionnels / non fonctionnels, ADR, diagrammes principaux.
- `comprehensive` : traçabilité complète, alternatives détaillées, vues multiples, registre de dette technique.

### Axe 2 — Niveau de vérification des livrables

Règle la rigueur du contrôle des livrables, **indépendamment** de Depth. Cet axe remplace, pour un workspace produisant majoritairement de la documentation d'architecture, l'axe « test strategy » d'AI-DLC :

- `advisory` : contrôle de cohérence par jugement d'agent.
- `standard` : cohérence documentation ↔ ADR + contrôle sécurité OWASP / STRIDE + validation humaine.
- `renforcé` : + traçabilité exigence ↔ ADR ↔ livrable, syntaxe des diagrammes validée, normes conditionnelles si demandées. *(Préfigure les Verification gates et Sensors introduits ultérieurement.)*
- **Cas code / IaC** : dès qu'un livrable comporte du code ou de l'IaC (ex. OpenSpec activé), cet axe **inclut une stratégie de tests** — le niveau `renforcé` exige alors des tests. L'axe reste ainsi compatible avec le sens AI-DLC quand du code existe, sans l'imposer à la documentation pure.

### Valeurs par défaut des axes, par scope

Les valeurs ci-dessous sont les **défauts** ; elles sont overridables (voir « Points d'override »).

| Scope | Depth par défaut | Vérification par défaut |
| --- | --- | --- |
| `standard` | standard | standard |
| `feature` | standard | standard |
| `infra` | standard | renforcé |
| `security-patch` | standard | renforcé |
| `mvp` | standard | standard |
| `poc` | minimal | advisory |
| `express` | minimal | standard |
| `enterprise` | comprehensive | renforcé |

### Points d'override

Les deux axes peuvent être ajustés à trois moments, du plus tôt au plus tard :

1. **À l'invocation** : l'humain ou l'agent appelant fixe `depth=` et `verification=` dans la demande.
2. **À la confirmation de scope** : lors de la confirmation du scope auto-détecté, le coordinateur propose les défauts et l'humain peut les ajuster.
3. **À un gate** : à une frontière de phase, l'humain peut **relever** le niveau (jamais l'abaisser sous les invariants).

**Garde-fou sécurité** : tout niveau lié à la sécurité **ne peut jamais être abaissé** par un override. Le plancher couvre trois leviers, pas seulement l'axe de vérification :

1. **Axe de vérification** : le contrôle sécurité minimal (OWASP / STRIDE) et, pour les scopes `security-patch` et `enterprise`, le niveau de vérification `renforcé` constituent un plancher ; un override ne peut que les maintenir ou les renforcer.
2. **Axe Depth** : sur `security-patch` et `enterprise`, la Depth **ne peut pas descendre sous `standard`** (préserve la traçabilité exigence ↔ ADR ↔ livrable, qui est un contrôle d'intégrité).
3. **Re-scoping** : tout changement de scope qui **abaisse le niveau de contrôle** d'un travail déjà détecté comme sécuritaire (mots-clés `security-patch`, ou scope courant `security-patch` / `enterprise`) **exige une validation humaine explicite tracée** sur l'issue. La reclassification en `express` / `poc` pour esquiver les contrôles est un contournement (STRIDE : Elevation of Privilege / Tampering sur la décision de routage) et n'est jamais silencieuse.

**Auto-détection = plancher, jamais plafond** : lorsqu'un scope est proposé par détection, la confirmation humaine peut le **maintenir ou monter** vers un scope à contrôle plus strict (ex. `security-patch` → `enterprise`) ; elle ne peut **descendre** vers un scope à contrôle allégé qu'avec la validation tracée du re-scoping (point 3).

---

## Règles & boucle d'apprentissage

Le workspace **capitalise les corrections humaines en règles persistantes** pour qu'un agent ne répète pas la même erreur d'un projet à l'autre. Le mécanisme combine une **mémoire de règles multi-couches** (fichiers Markdown versionnés) et une **boucle d'apprentissage** déclenchée aux points de validation humaine.

> Adaptation d'AI-DLC 2.0 (`awslabs/aidlc-workflows/core/memory`) au contexte du workspace (gouvernance A2A, livrables majoritairement documentaires, piste d'audit sur l'issue). Décision structurante tracée dans [ADR-0004](../decisions/0004-boucle-apprentissage-et-regles-persistantes.md). Les règles vivent dans [`core/rules/`](../core/rules/README.md).

### Système de règles en couches

Quatre couches, de la plus forte à la plus faible **précédence** :

| Couche | Fichier | Portée | Chargement |
| --- | --- | --- | --- |
| `workspace` | `core/rules/workspace.md` | Invariants et conventions valables partout | Au démarrage (toujours actif) |
| `project` | `core/rules/projects/<projet>.md` | Spécifique à un projet | Au démarrage, uniquement le projet courant |
| `phase` | `core/rules/phases/<phase>.md` (`inception` / `construction` / `operation`) | Par phase du workflow | À la demande, quand la phase est déclenchée |
| `scope` | `core/rules/scopes/<scope>.md` (les 8 scopes de la section précédente) | Par scope | À la demande, quand le scope est confirmé |

**Précédence** : `workspace` > `project` > `phase` > `scope`. Une règle d'une couche **ne peut pas contredire** une règle d'une couche supérieure sans arbitrage humain (voir « Contrôle de conflit à l'admission »).

Chaque règle porte un identifiant stable `RULE-<COUCHE>-NNN`, sa portée, l'issue d'origine et sa date d'ajout.

### Chargement des règles (paresseux)

Conformément au chargement optimisé pour le contexte : au démarrage, ne charger que les couches **toujours actives** — `workspace` et le `project` courant — ainsi que l'**index (titres) des règles** des autres couches. Les règles `phase` et `scope` ne sont chargées **en intégralité qu'à la demande**, lorsque la phase ou le scope concerné est effectivement déclenché. Documenter sur l'issue les règles chargées à la demande.

### La boucle d'apprentissage

La boucle capitalise les corrections humaines **sans jamais modifier l'exécution en cours** :

1. **Journal d'observations** *(pendant l'étape)* — chaque correction / rejet ❌ / reformulation 💬 humaine sur un choix est consignée en commentaire sur l'issue (piste d'audit existante) comme **candidat-règle** potentiel.
2. **Remontée des candidats** *(au point de validation humaine)* — le coordinateur formule les candidats détectés en règles courtes (« à l'avenir, faire X plutôt que Y »), en proposant pour chacun une **couche** et une **portée**. La détection est systématique (déclencheur **C1**) mais ne fait qu'alimenter la proposition.
3. **Confirmation humaine** — l'humain garde ✅ / rejette ❌ / reformule 💬 **chaque candidat séparément**. **Aucune règle n'est écrite sans validation humaine explicite** (garde-fou).
4. **Contrôle de conflit à l'admission** — avant écriture, chaque règle confirmée passe le contrôle ci-dessous.
5. **Écriture sur disque** — la règle admise est ajoutée au fichier de sa couche dans `core/rules/`, avec identifiant, portée, issue d'origine et date.
6. **Application au prochain workflow** — une règle nouvellement écrite **ne s'applique jamais en cours de route** ; elle est chargée au démarrage du **prochain** workflow.

**Portée par défaut** d'une règle apprise, en l'absence de précision : `project`. La promotion `project → workspace` est une décision structurante explicite (tracée en ADR si structurante) et **soumise dans tous les cas au contrôle sécurité systématique de l'Architecte cybersécurité** — qu'elle « touche la sécurité » ou non, au même titre qu'une écriture native en couche `workspace` (voir « Contrôle de conflit à l'admission », SEC-4). La qualification « touche la sécurité » ne conditionne jamais le déclenchement de ce contrôle.

### Contrôle de conflit à l'admission

Une règle apprise **ne peut pas contredire — ni éroder — une règle de niveau supérieur ou un garde-fou sans arbitrage humain**. Avant écriture :

1. **Précédence des couches** — `workspace` > `project` > `phase` > `scope`. Un candidat qui contredit une règle d'une couche supérieure n'est pas écrit tel quel : le coordinateur **remonte le conflit à l'humain** (et à l'Architecte cybersécurité si la règle touche la sécurité) ; l'arbitrage humain décide (rejet, reformulation, ou modification explicite de la règle supérieure via son canal propre — ADR si structurant). **Le coordinateur ne tranche jamais seul un conflit.**
2. **Invariants non contournables** — aucune règle apprise, à aucune couche, ne peut affaiblir les invariants non négociables (validation humaine granulaire, ADR sur décision structurante, piste d'audit sur l'issue, contrôle sécurité minimal OWASP / STRIDE) ni les garde-fous sécurité des scopes (plancher de vérification, Depth non abaissable sur `security-patch` / `enterprise`, re-scoping tracé). Un candidat qui les contredit est **rejeté d'office**.
3. **SEC-1 — Contrôle d'érosion sémantique** — le contrôle ne se limite pas à la contradiction littérale : un candidat qui **restreint la portée, ajoute une exception, ou conditionne l'application** d'un invariant non contournable ou d'un garde-fou de scope est traité comme un affaiblissement et **rejeté d'office**, même s'il n'entre pas en contradiction directe. L'idempotence n'exonère jamais de ce contrôle.
4. **SEC-2 — Contrôle sécurité systématique, à périmètre fondé sur le risque** — le contrôle sécurité de l'Architecte cybersécurité, avant écriture, s'applique à **toute** règle de couche `workspace`, **et** à toute règle de couche `project`, `phase` ou `scope` dès lors qu'elle vise ou modifie le comportement d'un scope à garde-fous (`security-patch`, `enterprise`), d'une phase de vérification, ou d'un contrôle de sécurité existant. Le critère de déclenchement est le **risque**, pas seulement la couche.
5. **SEC-3 — Pas d'exploitation d'un candidat dans le run courant** — un candidat-règle capturé pendant une étape **n'a aucune valeur normative tant qu'il n'est pas confirmé, contrôlé et écrit**. Il ne peut être ni appliqué, ni invoqué comme justification d'un autre choix dans le run courant. Seules les règles déjà écrites au démarrage du workflow font autorité ; l'application reste différée au **prochain** workflow, sans exception.
6. **SEC-5 — Intégrité du canal d'écriture** — aucune règle n'est ajoutée, modifiée ou supprimée dans `core/rules/` en dehors de la boucle d'apprentissage (capture → confirmation humaine → contrôle de conflit à l'admission). Toute modification de `core/rules/` est versionnée, revue en PR et porte l'`origine` (issue) et la date ; une entrée sans provenance traçable est invalide et retirée.
7. **Idempotence** — un candidat déjà couvert par une règle existante n'est pas ré-écrit (évite la dérive de `core/rules/`) — sans jamais court-circuiter SEC-1.

> **SEC-4 — Contrôle sécurité systématique sur promotion vers `workspace`** : toute promotion d'une règle de `project` (ou couche inférieure) vers `workspace` est soumise au contrôle sécurité systématique de l'Architecte cybersécurité, qu'elle « touche la sécurité » ou non, au même titre qu'une écriture native en couche `workspace` (voir « Portée par défaut »).

### Articulation avec l'audit et OpenSpec

- **Piste d'audit** : la *capture* (candidats, décision humaine, conflit éventuel) vit **sur l'issue** ; seule la **règle acceptée** est écrite dans `core/rules/`. Pas de fichier `audit.md`.
- **OpenSpec (conditionnel)** : lorsqu'OpenSpec est activé, les règles apprises pertinentes pour l'Inception peuvent enrichir la formulation des propositions (Fabien), sans jamais imposer OpenSpec.

---

## Modèle de collaboration A2A

Le workflow n'est pas exécuté par un seul agent. **l'Architecture Solution & Intégration est le coordinateur** : il analyse la demande, découpe en livrables, délègue aux agents spécialisés via des mentions sur les issues, contrôle les livrables, sollicite la sécurité, puis demande la validation humaine granulaire. **l'Architecture Solution & Intégration ne produit pas lui-même les livrables** (sauf vérification).

### Acteurs et responsabilités

| Acteur                                  | Rôle dans le workflow                                                                                                                                                                                |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Humain (demandeur / valideur)**       | Exprime le besoin, arbitre les choix, valide **chaque** décision architecturale (validation granulaire) et autorise les actions à impact.                                                            |
| **Architecture Solution & Intégration** | **Coordinateur**. Lance et supervise les travaux, contrôle la cohérence avec les ADR, sollicite Architecte cybersécurité pour la sécurité, demande les validations humaines, orchestre la livraison. |
| **Architecte de solution**              | Documentation d'architecture (DAS), ADR, diagrammes C4 / Archimate / PlantUML / CALM. Ne traite pas la cybersécurité.                                                                                |
| **Architecte cybersécurité**            | Analyse des risques (OWASP, STRIDE, NIST, COBIT ; PCI DSS / GDPR / Loi 25 / LPRPDE sur demande explicite). **Sollicité par Sylvain à chaque modification d'architecture.**                           |
| **Architecte AWS**                      | Services AWS, diagrammes AWS, estimation et optimisation des coûts (tarifs officiels sourcés). Intervient quand AWS est requis.                                                                      |
| **Admin — Infrastructure Windows**      | Administration Windows : migrations Win10→Win11, Intune, VM, golden images, Autopilot, SCCM. Plan de rollback validé avant toute action destructive.                                                 |
| **OpenSpec Expert**                     | Cycle spec-driven (proposition, implémentation, archivage). **Sollicité uniquement si OpenSpec est activé** pour le projet.                                                                          |
| **Expert d'archivage**                  | Import / export de fichiers, archives, mise à disposition et téléchargement des livrables validés.                                                                                                   |
| **Agent de Notifications**              | Notification (ntfy) de fin de tâche, sur demande de Sylvain.                                                                                                                                         |

### Règle A2A

Un agent est déclenché par un **commentaire sur l'issue avec une mention valide** `[@Label](mention://agent/<uuid>)` et une **mission claire** : objectif, périmètre, critères d'acceptation. **Ne jamais deviner un UUID** : le résoudre via `multica agent list --output json` (champ `id`). L'agent appelé, en fin de tâche, mentionne en retour l'agent assigneur pour la vérification. Le coordinateur contrôle chaque livrable avant validation humaine.

---

## OBLIGATOIRE : Chargement du contexte au démarrage

Avant toute exécution, le coordinateur :

1. **Vérifie le répertoire officiel du projet** : S'il n'existe pas ou en cas de doute, demander confirmation à l'humain. Ne pas lancer les travaux sans cette confirmation.
2. **Charge le contexte existant** : documentation d'architecture, ADR, diagrammes, contraintes déjà tracées.
3. **Applique les paramètres par défaut d'architecture** (structure de répertoire, conventions de nommage, emplacements des ADR et diagrammes).
4. **Détermine si une méthodologie s'applique** (OpenSpec, BMAD, ou autre — voir ci-dessous).

### OBLIGATOIRE : Chargement optimisé pour le contexte

**Ne charger au démarrage que les éléments légers, et différer le chargement complet jusqu'au moment où il est réellement nécessaire** — afin de préserver la fenêtre de contexte.

**Au démarrage (chargement léger uniquement)** :

- Charger seulement les **métadonnées légères** nécessaires au cadrage et au routage : la **liste des livrables**, la **liste des agents disponibles et leurs descriptions** (via `multica agent list --output json` — champ `description`, **pas** les `instructions` complètes), la **liste des skills et leurs descriptions**, l'**index / titres des ADR** et le **sommaire de la documentation d'architecture**.
- **NE PAS** charger au démarrage : les instructions détaillées d'un agent, les fichiers de règles ou gabarits complets, les specs vivantes intégrales, ou le corps complet des ADR et documents.

**Chargement différé (à la demande, au moment de la délégation ou de l'utilisation)** :

- Charger le **contenu complet** d'un agent, d'une skill, d'une méthodologie, d'un gabarit, d'un ADR ou d'une spec **uniquement lorsque l'étape ou la délégation qui en a besoin est effectivement déclenchée**.
- Exemple : les règles complètes d'une méthodologie ne sont chargées **qu'après** que l'humain / le contexte projet l'a activée ; si aucune méthodologie n'est activée, ses règles ne sont jamais chargées.
- Exemple : les instructions détaillées d'un architecte (Architecte de solution, Architecte AWS, Architecte cybersécurité, Admin) ne sont pertinentes que pour l'agent lui-même au moment de sa tâche ; le coordinateur se contente de la description pour router.

**Règles conditionnelles** (ex. normes de sécurité PCI DSS / GDPR / Loi 25 / LPRPDE) : ne sont chargées et appliquées que si **explicitement demandées** ; par défaut, seules les règles toujours actives (OWASP / STRIDE) le sont. Les règles non applicables à l'étape en cours sont marquées **N/A** plutôt que chargées.

**Justification par étape** : à chaque étape, n'évaluer et ne charger que les règles et documents **pertinents pour l'objectif de l'étape et les artefacts produits**. Documenter sur l'issue ce qui a été chargé à la demande, pour garder la piste d'audit.

### Activation conditionnelle d'une méthodologie

**Aucune méthodologie n'est imposée par défaut.** Une méthodologie (OpenSpec, BMAD, ou autre) s'active uniquement si elle est déclarée en fonction du contexte projet :

- La **description du projet Multica** déclare la méthodologie (ex. `Méthodologie: OpenSpec`, `Méthodologie: BMAD` ; les variantes historiques `OpenSpec: Oui` / `OpenSpec: Non` restent reconnues), **ou**
- L'**issue porte un tag de méthodologie** (ex. `OpenSpec`, `BMAD`), **ou**
- L'humain le demande explicitement.

**Comportement** :

- **Méthodologie déclarée** → le coordinateur applique le cycle propre à cette méthodologie et **délègue à l'agent spécialiste** correspondant lorsqu'il existe. Les livrables des phases prennent la forme prescrite par la méthodologie retenue.
  - **OpenSpec** (spec-driven) → délégué à **Fabien** (`c2dbee8f-9ed4-4867-9b21-6cdd4a8840eb`). Les livrables d'Inception prennent la forme d'une proposition OpenSpec (proposal / design / tasks / deltas de specs au format EARS, termes en MAJUSCULES conservés en anglais : `## ADDED/MODIFIED/REMOVED Requirements`, `WHEN`, `THEN`, `SHALL`, `GIVEN`).
  - **BMAD** → appliquer le cycle BMAD ; le déléguer à l'agent spécialiste dédié s'il existe dans le workspace, sinon le piloter via le coordinateur et les architectes. Si aucun agent spécialiste n'est encore défini, le signaler à l'humain (un agent dédié pourra être créé ultérieurement).
  - **Autre méthodologie** → même logique : appliquer le cycle demandé, déléguer à l'agent spécialiste s'il existe, sinon le signaler à l'humain.
- **Méthodologie non déclarée / ambiguë** → si le contexte projet ne précise pas de méthodologie, demander à l'humain s'il faut en activer une (et laquelle), puis inscrire la réponse dans la description du projet.
- **Aucune méthodologie (ou explicitement aucune)** → suivre le **parcours d'architecture standard** décrit ci-dessous (documentation d'architecture + ADR + diagrammes produits par Architecte de solution / Architecte AWS / Admin, sans cycle méthodologique spécifique).

> Quelle que soit la méthodologie, la **gouvernance A2A reste identique** : coordination par Sylvain, contrôle sécurité systématique par Architecte cybersécurité, ADR obligatoires, validation humaine granulaire, mise à disposition via Nina, notification via l'Agent de Notifications.

---

## OBLIGATOIRE : Piste d'audit sur l'issue

La piste d'audit vit **sur l'issue Multica**, pas dans un fichier `audit.md`. Chaque agent :

- Documente **chaque étape franchie** en commentaire (analyse, décision, délégation, résultat, sollicitation sécurité, validation).
- Capture l'**entrée brute** des demandes et arbitrages humains lorsqu'elle conditionne une décision, sans la résumer.
- N'écrase jamais l'historique : on ajoute des commentaires.
- Trace chaque décision structurante dans un **ADR** ; les livrables détaillés vivent dans le répertoire du projet.

---

## OBLIGATOIRE : Langue et format

- Rédiger **tous les documents dans la langue de l'humain (français par défaut)**.
- **Conserver l'anglais** pour les termes non traduits des templates OpenSpec / EARS (uniquement si OpenSpec est activé).
- Générer les diagrammes **en code** (PlantUML, Mermaid, Structurizr DSL, CALM, Archimate) et en **valider la syntaxe** avant écriture. Toujours demander à l'humain le **format de diagramme souhaité** avant génération.
- Ne jamais inclure de secrets, mots de passe ou identifiants dans les livrables.

---

# Vue d'ensemble des phases

Trois phases AI-DLC, réinterprétées pour la gouvernance d'architecture :

```mermaid
flowchart TD
    A[Demande humain ou agent] --> B[PHASE 1 - INCEPTION]
    B --> C[PHASE 2 - CONSTRUCTION]
    C --> D[PHASE 3 - OPERATION]
    B -.->|securite Architecte cybersécurité + validation granulaire humaine| B
    C -.->|securite Architecte cybersécurité + validation granulaire humaine| C
```

- **INCEPTION** — Déterminer QUOI et POURQUOI → besoins, décisions d'architecture (ADR), conception cible validée.
- **CONSTRUCTION** — Déterminer COMMENT → produire les livrables détaillés (documentation, diagrammes, IaC ou implémentation), vérifier, faire valider.
- **OPERATION** — DÉPLOYER et EXPLOITER → déploiement / administration sous validation humaine explicite.

---

# PHASE 1 — INCEPTION

**Objectif** : planification, collecte des besoins, décisions architecturales.
**Focus** : QUOI et POURQUOI.
**Livrable de sortie** : conception cible et décisions (ADR) **validées par l'humain** de façon granulaire, après contrôle sécurité par Architecte cybersécurité.

**Étapes** :

- Réception et cadrage de la demande (TOUJOURS)
- Chargement du contexte existant (CONDITIONNEL — système existant)
- Analyse des besoins (TOUJOURS — profondeur adaptative)
- Planification et découpage en livrables (TOUJOURS)
- Conception d'architecture et ADR (TOUJOURS)

## 1.1 — Réception et cadrage (TOUJOURS)

1. Passer l'issue en `in_progress`.
2. Consigner la demande initiale (entrée brute) en commentaire.
3. Vérifier le répertoire du projet et l'activation éventuelle d'OpenSpec.
4. Clarifier le besoin d'affaires : objectifs, exigences fonctionnelles et non fonctionnelles, contraintes. **Ne poser que les questions qui changent réellement la conception.** Ne jamais deviner une information manquante.

## 1.2 — Chargement du contexte existant (CONDITIONNEL)

**Exécuter SI** : système / documentation existants et contexte insuffisant.
**Ignorer SI** : greenfield, ou contexte déjà suffisant.

Charger la documentation d'architecture, les ADR et diagrammes pertinents ; en produire une synthèse sur l'issue.

## 1.3 — Analyse des besoins (TOUJOURS — profondeur adaptative)

- **Minimale** : demande simple et claire — documenter l'analyse d'intention.
- **Standard** : recueillir besoins fonctionnels et non fonctionnels (performance, sécurité, scalabilité, portabilité, maintenabilité).
- **Complète** : haut risque — besoins détaillés avec traçabilité.

Documenter les besoins retenus sur l'issue.

## 1.4 — Planification et découpage en livrables (TOUJOURS)

1. Déterminer les phases et étapes à exécuter et leur profondeur.
2. **Découper le travail en livrables** et désigner l'agent responsable de chacun :
   - Documentation d'architecture / ADR / diagrammes → **Architecte de solution**.
   - Choix AWS, diagrammes AWS, coûts → **Architecte AWS** (si AWS requis).
   - Administration / infrastructure Windows → **Admin Infrastructure Windows** (si concerné).
   - Cycle spec-driven → **Fabien** (uniquement si OpenSpec activé).
3. Créer les issues nécessaires et déclencher chaque agent par mention avec mission claire.
4. Produire la visualisation du workflow retenu (diagramme validé) sur l'issue.

## 1.5 — Conception d'architecture, ADR et contrôle sécurité (TOUJOURS)

1. Les agents désignés produisent leurs livrables de conception (vues fonctionnelle/technique, choix, alternatives, risques) et **tracent chaque décision structurante dans un ADR**.
2. **Contrôle sécurité obligatoire (Architecte cybersécurité)** : à **chaque modification d'architecture** par un agent, Sylvain lit le résumé des modifications, poste un commentaire mentionnant **Architecte cybersécurité** (`694a1a6f-9659-48ea-b45f-43ae6dc01706`) avec le contexte, **attend son analyse** et intègre ses recommandations avant toute validation. Préciser explicitement toute norme spécifique à appliquer (PCI DSS, GDPR, Loi 25, LPRPDE) — sinon seules OWASP/STRIDE (+ NIST/COBIT si documentation des risques) sont actives.
3. **Contrôle de cohérence ADR** : vérifier la correspondance documentation ↔ ADR, l'absence de conflits entre ADR ; signaler les écarts et demander les corrections aux agents responsables.
4. **Validation granulaire humaine** (point de synchronisation) : présenter à l'humain **chaque choix / recommandation séparément** (choix, justification, alternative), demander une validation ✅ / rejet ❌ / 💬 par élément. Ne pas avancer sur un élément non validé ; sur rejet, proposer une alternative et relancer la validation de cet élément uniquement.
5. **Analyse de dette technique (Architecte de solution)** : pour chaque décision ou spécification produite, l'Architecte de solution évalue le potentiel de réduction de la dette technique et consigne ses **recommandations justifiées/prouvées** dans l'ADR ou la spécification. Si un document de dette technique est fourni sans décision ni demande de modification d'architecture, il produit à la place un **registre de dette technique en annexe** de la documentation (aucun ADR). Ces éléments entrent dans le contrôle de cohérence et la validation granulaire humaine.

> Si OpenSpec est activé, cette phase se matérialise par une **proposition OpenSpec** créée par Fabien, qui notifie Sylvain à la mise en revue (`in_review`) ; Sylvain analyse puis fait approuver l'humain. À spécification approuvée, Fabien crée les tâches de mise à jour des documents d'architecture (backlog, assignées à Sylvain, priorité qu'il détermine).

---

# 🟢 PHASE 2 — CONSTRUCTION

**Objectif** : conception détaillée et production des livrables.
**Focus** : COMMENT le construire.
**Entrée** : conception cible et ADR validés.

**Étapes** :

- Production des livrables détaillés (par livrable / agent)
- Contrôle sécurité et cohérence
- Consolidation, validation humaine et mise à disposition

## 2.1 — Production des livrables détaillés

Chaque agent exécute son livrable (documentation détaillée, diagrammes définitifs, estimation de coûts AWS, configuration/administration infra, ou — si OpenSpec activé — implémentation des tâches via Fabien avec tests). Chaque agent, en fin de travail, mentionne Sylvain pour vérification. Documenter sur l'issue.

## 2.2 — Contrôle sécurité et cohérence (TOUJOURS)

1. **Solliciter Architecte cybersécurité** pour tout livrable modifiant l'architecture (mêmes règles qu'en 1.5).
2. Vérifier structure, complétude, qualité, format des livrables, et cohérence avec les ADR.
3. Demander les corrections aux agents responsables le cas échéant.

## 2.3 — Consolidation, validation humaine et mise à disposition (TOUJOURS)

1. **Validation granulaire humaine** de chaque livrable / choix restant à approuver.
2. **Mise à disposition** : confier à **Nina** (`8f54de1e-9725-4c0a-9dc7-9bb32f160acb`) le téléversement, la visualisation, le téléchargement et l'archivage des documents validés dans le répertoire du projet ; fournir à l'humain un récapitulatif accessible.
3. Si OpenSpec activé : Fabien archive le changement (fusion des deltas dans les specs vivantes) et passe l'issue à Done après approbation.

---

# 🟡 PHASE 3 — OPERATION

**Objectif** : déployer et exploiter.
**Focus** : COMMENT DÉPLOYER et LANCER.

**Étapes** :

- Déploiement / administration sous validation humaine
- Notification de fin
- Maintenance et support (extension future)

## 3.1 — Déploiement / administration sous validation humaine

1. Soumettre la configuration / le plan complet à l'humain pour **validation explicite**.
2. Pour les actions d'infrastructure destructives ou de migration (Admin Windows), un **plan de rollback détaillé** doit être publié et **validé par l'humain avant exécution**.
3. **Aucune action à impact (déploiement, migration, orchestration) sans validation humaine explicite.**

## 3.2 — Notification de fin

Une fois la tâche réalisée et passée en revue, Sylvain demande à **l'Agent de Notifications** (`9b5a4076-7b9c-4db6-9d03-06ba49ae0f0f`) d'envoyer une notification (ntfy) : message court (« L'issue a été réalisée »), identifiant de l'issue et lien si possible.

## 3.3 — Maintenance et support (extension future)

Emplacement réservé : planification de déploiement, surveillance/observabilité, réponse aux incidents, préparation à la production.

---

# Fin de chantier

- Ne clôturer aucune issue comme « terminée » avant la **validation humaine**.
- Informer l'humain sur l'issue lorsque l'ensemble du travail est achevé, avec le récapitulatif des livrables et leur emplacement.

---

# Principes clés et garde-fous

- **Exécution adaptative** : n'exécuter que les étapes qui apportent de la valeur.
- **Méthode agnostique** : OpenSpec est conditionnel (déclaré au niveau du projet ou de l'issue) ; sinon, parcours d'architecture standard.
- **Chargement optimisé pour le contexte** : au démarrage, ne charger que les métadonnées légères (descriptions d'agents/skills, index des ADR, sommaire de la documentation) ; différer le chargement complet (instructions d'agent, règles de méthodologie, gabarits, specs, corps des ADR) jusqu'au moment où l'étape ou la délégation en a besoin.
- **Sylvain coordonne, les spécialistes produisent** : la production des livrables revient aux agents spécialisés.
- **Sécurité systématique** : toute modification d'architecture passe par Architecte cybersécurité avant validation humaine ; normes spécifiques appliquées uniquement si explicitement demandées.
- **Validation humaine granulaire** : chaque choix est validé/rejeté séparément ; rien n'avance sur un élément non validé.
- **ADR obligatoires** : chaque décision structurante est tracée, révisée, sans conflit ; aucune décision acceptée sans validation humaine.
- **Capitalisation des corrections (learning loop)** : les corrections humaines validées deviennent des règles persistantes multi-couches (`core/rules/`) ; l'écriture est subordonnée à une validation humaine explicite et à un contrôle de conflit à l'admission ; une règle apprise s'applique au **prochain** workflow, jamais en cours de route.
- **Jamais de supposition** : information requise manquante → demander à l'humain et attendre.
- **Coordination par l'issue** : chaque étape, décision et délégation documentée en commentaire ; délégations A2A par mention valide (UUID résolu, jamais deviné) avec mission claire.
- **Validation de contenu** : diagrammes en code, syntaxe validée ; format de diagramme confirmé par l'humain avant génération.
- **Séparation des responsabilités** : fichiers/exports via Nina ; notifications via l'Agent de Notifications ; Docker Compose hors périmètre (Stuart).
- **Aucun secret** dans les livrables ; **aucune action à impact** sans validation humaine explicite ; **rollback validé** avant action destructive.

---

# Points de synchronisation A2A (résumé)

```mermaid
sequenceDiagram
    participant H as Humain
    participant S as Sylvain
    participant A as Architecte de solution / Architecte AWS / Admin (ou Fabien si OpenSpec)
    participant X as Architecte cybersécurité
    participant N as Nina
    participant AL as l'Agent de Notifications

    H->>S: Demande (issue)
    S->>S: Cadrage + besoins + decoupage (INCEPTION)
    S->>A: Delegue livrables (mention + mission)
    A-->>S: Livrable + ADR
    S->>X: Sollicite controle securite
    X-->>S: Analyse + recommandations
    S->>H: Validation granulaire (choix par choix)
    H-->>S: Validation / rejet par element
    S->>A: Production detaillee (CONSTRUCTION)
    A-->>S: Livrables detailles
    S->>X: Controle securite
    S->>H: Validation granulaire
    S->>N: Mise a disposition des livrables valides
    S->>H: Validation deploiement (OPERATION)
    H-->>S: Validation explicite (+ rollback si destructif)
    S->>AL: Demande notification de fin
    AL-->>H: Notification ntfy
```
