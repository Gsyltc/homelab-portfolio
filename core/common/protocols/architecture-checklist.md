# Protocole — checklist d'architecture (cycle lecture / écriture)

**Source unique** du **processus de checklist d'architecture** du workflow `core` : comment l'**état d'avancement de l'architecture** est tenu, lu et mis à jour tout au long des **5 phases** (`Initialization → Ideation → Inception → Construction → Operation`). La checklist est un **processus à part** — ni un stage, ni un livrable d'architecture : elle **suit** l'avancement des livrables sans les produire.

Ce protocole fixe la **mécanique** : structure, unité de décompte, calcul du %, barème, règles d'écriture, vérification de conformité, et le **critère de son propre gate de conformité** (section 7). Il **ne redéfinit pas** les **gates de phase** ni la **validation humaine granulaire** — source unique [`../conductor.md`](../conductor.md) et [`governance-security.md`](governance-security.md) : le gate de conformité de la checklist (section 7) **alimente** le gate humain existant à **deux transitions de phase nommées** (`Inception → Construction` et `Construction → Operation`), sans s'y substituer. Les **sections mandatory** des livrables ont pour source unique [`../../sensors/sensors/required-sections.md`](../../sensors/sensors/required-sections.md) ; ce protocole ne les redéfinit pas.

> **Qui est concerné.** Le **coordinateur** (Architecture Solution & Intégration) tient la checklist : il la lit sur demande humaine et ne met à jour l'avancement d'un élément que sur **vérification de conformité objective** et, pour l'acceptation, sur **approbation humaine explicite**. Les agents spécialisés produisent les livrables ; ils ne s'auto-valident **jamais**.

## 1. État de la checklist (où il vit)

- L'**état** est un **livrable versionné** du projet : `documentation/00-checklist-architecture.md`, copié depuis le gabarit [`gabarits/00-checklist-architecture.md`](gabarits/00-checklist-architecture.md) à l'initialisation du répertoire projet (Phase 0, [`../stages/initialization/directory-check.md`](../stages/initialization/directory-check.md)).
- Chaque **changement d'avancement** est **aussi tracé sur l'issue** (piste d'audit — source unique [`../conductor.md`](../conductor.md), « OBLIGATOIRE : piste d'audit sur l'issue ») : objet, ancien % → nouveau %, ce qui l'a fait évoluer (section conforme, revue, acceptation humaine), **référence de version** du livrable (commit / révision d'issue), identité de l'auteur du verdict ou de l'acceptation, verdict de conformité.
- Le fichier d'état est un **livrable** : il est soumis à l'invariant **« aucune note de génération / méta-production »** (réf. décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)). La traçabilité (qui a validé, quand, via quelle issue, sur quelle version) vit **sur l'issue**, pas dans le fichier.

## 2. Structure imposée (sections et éléments)

Quatre sections, éléments **fixes** ; aucun ajout / retrait d'élément sans décision tracée (ADR). Avancement par défaut `0 %`.

- **Cadrage**
- **Besoins (MoSCoW)** — Entreprises et affaires · Solutions · Technologique · **Sécurité**
- **Livrables** — Architecture de solution (DAS) · Architecture Logicielle détaillée · Architecture de données détaillée · **Architecture de sécurité détaillée** · Architecture infrastructure détaillée
- **Projets** — Planification · Coûts · Risques · Exploitation · Arrimages

Chaque élément listé est une **unité suivie** et porte un **pourcentage d'avancement** (0 à 100 %), calculé selon le barème de la section 3.

**Éléments d'architecture (revue de sécurité SG-3).** On appelle **élément d'architecture** tout élément **soumis à la revue de sécurité** : les **cinq éléments de la section Livrables** (architecture de solution et architectures détaillées) **et** **Besoins → Sécurité**. Pour eux, le terme `(revue)` exige le **verdict du Reviewer de sécurité**, qui **précède** le gate et l'acceptation (sections 3, 7). Le marquage **🔒** (gabarit et tableaux de ce protocole) signale **exactement** ces éléments d'architecture — un seul sens. Les autres éléments (Cadrage, autres Besoins, Projets) relèvent de la revue de **cohérence**.

## 3. Calcul du pourcentage (barème 80/10/10)

Chaque élément est noté selon le **même barème homogène**. Le **pourcentage est un indicateur d'avancement**, pas le critère du gate (section 7) :

```
% élément = 80 × (sections conformes / total sections) + 10·(revue) + 10·(acceptation humaine)
```

### Unité de décompte = la **section mandatory**

Le décompte du terme 80 % se fait **à la section mandatory**, pas au fichier. Le `total sections` d'un élément est le **nombre de sections mandatory** de son ou ses documents attendus, lu dans le contrat `required-sections`. Exemples au contrat actuel :

- **Architecture de solution (DAS)** : **18 sections** réparties sur 7 fichiers mandatory (`001` : 4 · `01` : 3 · `02` : 3 · `06` : 2 · `08` : 2 · `10` : 2 · `11` : 2).
- **Architecture de sécurité détaillée** : **2 sections** du fichier `11-securite.md` (« Modélisation des menaces (STRIDE) », « Sécurité applicative »).

Les trois termes :

- **80 % — conformité documentaire** : proportion des **sections mandatory présentes et non vides**. `sections conformes` et `total sections` se lisent dans `required-sections` (**source unique**, non dupliqué ici). Pour un élément **sans contrat de sections mandatory** (section 6), `total sections = 1` **par convention** et le terme vaut `80 %` dès que le livrable attendu est jugé présent et conforme. **« Présent et non vide » est un plancher de forme, pas un niveau de sécurité ou de qualité atteint** : le fond est contrôlé par la revue (ci-dessous) ; un `80 %` ne vaut jamais « sécurisé ».
- **+10 % — revue** : le terme `(revue)` vaut `1` uniquement si le **verdict de revue** du reviewer dédié est **posté ET favorable, sans point bloquant ouvert**, et **rattaché à la version courante** du livrable (section 4). Pour **tout élément de la section Livrables** (architecture de solution et architectures détaillées — logicielle, données, sécurité, infrastructure) et pour l'élément **Besoins → Sécurité**, `(revue)` exige le **verdict du Reviewer de sécurité** (SG-3, « revue de sécurité avant la validation humaine sur toute modification d'architecture ») ; la revue de cohérence **s'ajoute** mais ne s'y substitue jamais. Pour les autres éléments (Cadrage, autres Besoins, Projets), le reviewer dédié est la **cohérence**.
- **+10 % — acceptation humaine** : le terme vaut `1` si un **membre humain** de l'espace (auteur de type `member`) a **explicitement accepté** l'élément (gate granulaire « Keep / Modify / Redo » — source unique [`../conductor.md`](../conductor.md)), rattaché à la version courante (section 4). Un commentaire d'agent, **même cité par un humain**, ne compte pas ; aucun agent ne s'auto-accepte. **Pour les éléments de la section Livrables et pour Besoins → Sécurité, l'acceptation humaine ne se crédite qu'après le verdict de sécurité favorable sur la même version** (jamais en parallèle — SG-3).

- **% section** : moyenne arithmétique des `% élément` de la section ; **% global** : moyenne de **tous** les `% élément`. Les deux sont arrondis à l'entier **pour l'affichage uniquement**.
- **Arrondi** : l'arrondi est **un affichage**. Le gate ne compare **aucun pourcentage** : il teste `sections conformes / total = 1` (section 7).

### Total dynamique, anti-abaissement, double comptage

- **Total dynamique** : le `total sections` est **toujours lu dans `required-sections` au moment du calcul** ; le fichier d'état n'est qu'un **instantané recalculé** à chaque mise à jour, jamais une source concurrente.
- **Anti-abaissement (SG-3)** : retirer ou assouplir une section mandatory **de sécurité** fait monter les % ; recevable **uniquement sur validation humaine tracée** (décision relevant de `required-sections` + contrôle sécurité, pas de la checklist).
- **Double comptage** : les sections de `11-securite.md` et `10-cycle_vie_donnees.md` comptent à la fois dans le DAS et dans l'élément détaillé correspondant (assumé ; cf. NEG-004 de l'ADR).

## 4. Mise à jour (écriture) — conformité objective, revue favorable versionnée, acceptation humaine

L'avancement d'un élément évolue uniquement par **faits vérifiables**, jamais par estimation :

1. **Terme 80 %** — recalculé à chaque vérification de conformité (section 6) : sections mandatory présentes et non vides / total (contrat `required-sections`). Un doute sur la conformité d'une section ⇒ elle **ne compte pas** (« ne jamais deviner »).
2. **Terme +10 % revue** — passe à `1` uniquement quand le **verdict du reviewer dédié** (le **Reviewer de sécurité** pour les **éléments d'architecture**, section 2) est **posté, favorable et sans point bloquant ouvert**, **et** rattaché à la **version courante**. Un verdict « demande de corrections » ou portant un point bloquant **ne crédite pas** le terme.
3. **Terme +10 % acceptation humaine** — passe à `1` **uniquement** sur **annonce explicite d'un membre humain** (auteur `member`, cité par identifiant), rattachée à la **version courante**.

**Rattachement à une version (anti-falsification, OWASP A08).** Les deux `+10 %` sont crédités **pour une version précise** du **support** de l'élément (commit / révision d'issue tracée). Le support est : pour les éléments **avec document(s) attendu(s)**, ce ou ces documents ; pour les éléments **sans document** (Cadrage, Besoins, Projets), le **support versionné qui les porte** — le **commentaire d'issue** décrivant l'élément (identifiant + révision) ou, s'il y figure, le **paragraphe du DAS** qui le consigne. **Dès que ce support change — quelle qu'en soit la partie, mandatory ou non : nouvelle référence de version**, les **deux** termes **retombent à `0`** ; la remise à zéro est **tracée sur l'issue** et le crédit ne se rétablit que par une nouvelle revue favorable et une nouvelle acceptation sur la version modifiée.

Doute sur la conformité, le sens d'un verdict ou l'intention humaine ⇒ **ne jamais deviner** ; ne pas créditer ; informer l'humain (garde-fou « ne jamais deviner » + validation humaine granulaire — [`governance-security.md`](governance-security.md)). Chaque évolution de % est tracée sur l'issue **avant** report dans le fichier d'état, avec sa **preuve** et la **version** concernée.

## 5. Lecture — sur demande humaine

Sur demande, le coordinateur affiche, en **prose réduite** (source unique [`output-format.md`](output-format.md)) : chaque **section** avec son **%** ; chaque **élément** avec son **%** et, pour les Livrables, le **détail** (sections conformes / total, revue ✓/✗ et sa nature, acceptation ✓/✗, version évaluée) ; au **gate** (section 7), l'**état de conformité complète (✓/✗)** et de **revue de sécurité (✓/✗)** ; le **% global**. Le % affiché est un **instantané recalculé** à chaque mise à jour. La lecture ne modifie aucun % et ne vaut ni revue ni acceptation.

## 6. Vérification de conformité (préalable au terme 80 %)

Avant de créditer les sections conformes d'un élément, le coordinateur vérifie que le ou les **documents attendus existent**, sont **au bon format**, **clairs**, **sans note de génération d'agent** (décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)), **sans doublon ni incohérence** ; et que, pour la section **Livrables**, les **sections mandatory** sont **présentes et non vides** selon `required-sections` (**source unique** — advisory, n'autorise jamais à se passer de la validation humaine ni de la revue). « Présent et non vide » est un **critère de forme** ; le **fond** relève de la **revue** (section 3-4) — pour les **éléments d'architecture**, la **revue de sécurité** (SG-3). Échec ou ambiguïté ⇒ **la section ne compte pas** ; informer l'humain.

### Mapping élément → document(s) attendu(s) et contrat de sections

| Élément | Document(s) attendu(s) dans `documentation/` | Contrat de sections (décompte du 80 %) | Total sections |
| --- | --- | --- | --- |
| Cadrage | jugé sur l'issue (pas de document mandatory propre) | **aucun contrat** — convention `total = 1` | 1 |
| Besoins → Entreprises et affaires · Solutions · Technologique | jugés sur l'issue (pas de document mandatory propre) | **aucun contrat** — convention `total = 1` ; jugé par la **cohérence** | 1 |
| 🔒 Besoins → Sécurité | jugé sur l'issue | **aucun contrat** — convention `total = 1` ; jugé par le **Reviewer de sécurité** | 1 |
| 🔒 Architecture de solution (DAS) | fichiers mandatory du DAS (`001`,`01`,`02`,`06`,`08`,`10`,`11`) | `required-sections`, volet `das:` ; conformité par **cohérence**, `(revue)` par **sécurité** | **18** |
| 🔒 Architecture Logicielle détaillée | `00-architecture-detaillee.md` (volet logiciel) | gabarit DAS `00-architecture-detaillee` (**non mandatory** → `total = 1`) ; conformité par **cohérence**, `(revue)` par **sécurité** | 1 |
| 🔒 Architecture de données détaillée | `10-cycle_vie_donnees.md` + modèles | sensor `data-lifecycle` (**advisory, non mandatory** → `total = 1`) ; conformité par **cohérence** (Architecte de données en appui), `(revue)` par **sécurité** | 1 |
| 🔒 Architecture de sécurité détaillée | `11-securite.md` (STRIDE / OWASP) | `required-sections`, fichier `11-securite.md` ; conformité **et** `(revue)` par **sécurité** | **2** |
| 🔒 Architecture infrastructure détaillée | `09-deploiement.md` + diagrammes | gabarit DAS `09-deploiement` (**non mandatory** → `total = 1`) ; conformité par **cohérence**, `(revue)` par **sécurité** | 1 |
| Projets → Planification · Coûts · Risques · Exploitation · Arrimages | jugés sur l'issue (pas de document mandatory propre) | **aucun contrat** — convention `total = 1` par élément | 1 |

> **Éléments sans contrat de sections mandatory.** Pour tout élément dont « Total sections » vaut `1` **par convention** (Cadrage, les quatre Besoins, Logiciel, Données, Infrastructure, les cinq Projets), il n'existe **pas de base objective** de décompte section par section. Leur **conformité** (terme 80 %) est jugée par la revue de la nature de l'élément — **cohérence** pour la plupart, **Reviewer de sécurité** pour **Besoins → Sécurité** (comme son terme `(revue)`). En l'absence de base objective, le coordinateur **ne devine pas** et informe l'humain.
>
> **Combien de verdicts créditent conformité + `(revue)` ?** Cela dépend du reviewer :
> - **Un seul verdict** (0 → 90 %) pour les éléments dont **le même reviewer** juge la conformité (80 %) **et** `(revue)` : **Cadrage, Besoins hors Sécurité, Projets** (cohérence) et **Besoins → Sécurité** (Reviewer de sécurité).
> - **Deux verdicts, de deux reviewers**, pour **Architecture Logicielle / Données / Infrastructure détaillées** : la **conformité (80 %)** est jugée par la **cohérence**, mais `(revue)` (+10 %) exige le **verdict du Reviewer de sécurité** (élément d'architecture). Ces éléments ne sautent pas à 90 % sur un seul verdict : 80 % sur le verdict de conformité (cohérence), +10 % sur le verdict de sécurité favorable, +10 % sur acceptation humaine.
>
> Le détail (document attendu, reviewer de conformité, reviewer de `(revue)`, version) reste tracé sur l'issue.
>
> Seuls le **DAS** (18) et l'**Architecture de sécurité détaillée** (2) ont un contrat de sections lu dans `required-sections` ; en cas d'écart de nommage/découpage, **ces sources font foi**. La **remise à zéro** (section 4) s'applique à ces éléments comme aux autres, sur tout changement de leur **support versionné** — document(s) attendu(s), ou, pour les éléments sans document, le **commentaire d'issue** (ou paragraphe du DAS) qui les porte.

## 7. Gate de conformité de la checklist

Le gate s'applique **par élément**, jamais sur une moyenne. Un élément est **conforme au gate** uniquement si **toutes** ces conditions sont réunies :

1. **Conformité complète** — **toutes** les sections mandatory de l'élément sont conformes (`sections conformes / total = 1`, ex. DAS 18/18). Une seule section manquante ⇒ non conforme, quel que soit le %.
2. **Revue de sécurité (SG-3)** — pour tout **élément d'architecture** (les cinq Livrables et Besoins → Sécurité, section 2), le **verdict favorable du Reviewer de sécurité** (version courante) **précède** la conformité au gate **et** l'acceptation humaine.

### Deux frontières de phase (chaque élément est jugé où il est produit)

Le gate ne peut exiger un élément avant la phase qui le produit. Les éléments sont donc rattachés à la **frontière** qu'ils conditionnent (🔒 = élément d'architecture soumis à la revue de sécurité) :

| Frontière | Éléments exigés conformes | Produits en |
| --- | --- | --- |
| **`Inception → Construction`** | Cadrage · Besoins (🔒 Sécurité + 3 autres) · 🔒 Architecture de solution (DAS) | Inception |
| **`Construction → Operation`** | 🔒 Architectures détaillées (Logicielle · Données · Sécurité · Infrastructure) · Projets (les 5) | Construction |

### Portée du gate — **proposé bloquant, cf. ADR-0043 `DEC-HUM-001`**

Conformément à la demande initiale (`< seuil ⇒ bloqué`) et à SG-3, le gate est **proposé bloquant**. **« Bloquant » signifie que le coordinateur n'ouvre pas la sollicitation de validation humaine de la frontière** tant que la **conformité complète** d'un élément et, pour les **éléments d'architecture**, le **verdict de sécurité favorable** ne sont pas réunis. Ce n'est pas un verrou technique : l'humain **peut déroger** et franchir la frontière malgré un écart, mais par une **décision explicite tracée sur l'issue, mentionnant l'écart** (élément non conforme / verdict de sécurité manquant) — jamais un contournement silencieux. Au gate, le coordinateur **affiche** la conformité complète (✓/✗) et la revue de sécurité (✓/✗) de chaque élément (section 5).

> **Arbitrage `DEC-HUM-001` (ADR-0043).** Le caractère **bloquant** (vs advisory) et l'**ancrage aux deux frontières** sont soumis à l'humain demandeur ; `Proposed` vaut proposition. Un gate bloquant **s'écarte** de la règle « les gates de frontière sont advisory » du [`../conductor.md`](../conductor.md) (« Verification gates aux frontières de phases ») : l'exception (ou le rebascule en advisory) est à **acter dans `DEC-HUM-001`**.

## 8. Ce que ce protocole ne change pas (garde-fous)

- **Validation humaine granulaire** — le `+10 %` d'acceptation n'est crédité que sur annonce explicite d'un **membre humain** ; aucun scope, aucune règle apprise, aucun sensor advisory, aucun seuil de % ni gate ne peut s'y substituer (invariants [`../conductor.md`](../conductor.md), [`governance-security.md`](governance-security.md)).
- **Revue de sécurité non substituable (SG-3)** — sur tout **élément d'architecture** (section 2), la **revue de sécurité précède** la validation humaine ; **ni le gate ni le pourcentage ne la remplacent** ni ne conditionnent son déclenchement. Un contrôle lié à la sécurité ne s'abaisse jamais sans validation humaine tracée.
- **Piste d'audit sur l'issue** — chaque évolution de % y est tracée avec preuve et version ; le fichier d'état ne porte aucune méta-production (décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)).
- **Sensors advisory** — `required-sections` et `data-lifecycle` **assistent** le décompte sans jamais bloquer ni remplacer la validation humaine ni la revue (SG-1..6).
- **Ne jamais deviner** — un % ne résulte que d'une vérification objective ; doute ⇒ ne pas créditer, informer l'humain.
- **Langue** — français par défaut ; voir [`../conductor.md`](../conductor.md), « OBLIGATOIRE : langue et format ».
