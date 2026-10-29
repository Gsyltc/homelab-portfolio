# Protocole — checklist d'architecture (cycle lecture / écriture)

**Source unique** du **processus de checklist d'architecture** du workflow `core` : comment l'**état d'avancement de l'architecture** est tenu, lu et mis à jour tout au long des **5 phases** (`Initialization → Ideation → Inception → Construction → Operation`). La checklist est un **processus à part** — ni un stage, ni un livrable d'architecture : elle **suit** l'avancement des livrables sans les produire. Ce protocole fixe la **mécanique** (structure, calcul du %, barème, règles d'écriture, vérification de conformité, gate) ; il ne redéfinit **ni** les gates de phase et la validation humaine granulaire — source unique [`../conductor.md`](../conductor.md) et [`governance-security.md`](governance-security.md) — **ni** les sections mandatory des livrables — source unique [`../../sensors/sensors/required-sections.md`](../../sensors/sensors/required-sections.md).

> **Qui est concerné.** Le **coordinateur** (Architecture Solution & Intégration) tient la checklist : il la lit sur demande humaine et ne met à jour l'avancement d'un élément que sur **vérification de conformité objective** et, pour l'acceptation, sur **approbation humaine explicite**. Les agents spécialisés produisent les livrables ; ils ne s'auto-valident **jamais**.

## 1. État de la checklist (où il vit)

- L'**état** est un **livrable versionné** du projet : `documentation/00-checklist-architecture.md`, copié depuis le gabarit [`gabarits/00-checklist-architecture.md`](gabarits/00-checklist-architecture.md) à l'initialisation du répertoire projet (Phase 0, [`../stages/initialization/directory-check.md`](../stages/initialization/directory-check.md)).
- Chaque **changement d'avancement** est **aussi tracé sur l'issue** (piste d'audit — source unique [`../conductor.md`](../conductor.md), « OBLIGATOIRE : piste d'audit sur l'issue ») : objet, ancien % → nouveau %, ce qui l'a fait évoluer (section conforme, revue, acceptation humaine), **référence de version** du livrable concerné (commit / révision d'issue), identité de l'auteur du verdict ou de l'acceptation, verdict de conformité.
- Le fichier d'état est un **livrable** : il est soumis à l'invariant **« aucune note de génération / méta-production »** (réf. décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)). La traçabilité (qui a validé, quand, via quelle issue, sur quelle version) vit **sur l'issue**, pas dans le fichier.

## 2. Structure imposée (sections et éléments)

Quatre sections, éléments **fixes** ; aucun ajout / retrait d'élément sans décision tracée (ADR). Avancement par défaut `0 %`.

- **Cadrage**
- **Besoins (MoSCoW)** — Entreprises et affaires · Solutions · Technologique · **Sécurité**
- **Livrables** — Architecture de solution (DAS) · Architecture Logicielle détaillée · Architecture de données détaillée · **Architecture de sécurité détaillée** · Architecture infrastructure détaillée
- **Projets** — Planification · Coûts · Risques · Exploitation · Arrimages

Chaque élément listé est une **unité suivie** et porte un **pourcentage d'avancement** (0 à 100 %), calculé selon le barème de la section 3.

Deux éléments sont des **éléments de surface de sécurité** : **Besoins → Sécurité** et **Livrables → Architecture de sécurité détaillée**. Ils reçoivent un traitement renforcé au gate (section 7) et pour la revue (sections 3-4).

## 3. Calcul du pourcentage (barème 80/10/10)

Chaque élément est noté selon le **même barème homogène**. Le **pourcentage est un indicateur d'avancement**, pas le seul critère du gate (section 7) :

```
% élément = 80 × (sections conformes / total sections) + 10·(revue) + 10·(acceptation humaine)
```

Les trois termes :

- **80 % — conformité documentaire** : proportion des **sections mandatory présentes et non vides** du ou des documents attendus pour l'élément. `sections conformes` et `total sections` se lisent dans le contrat du sensor [`required-sections`](../../sensors/sensors/required-sections.md) (**source unique**, non dupliqué ici). Pour un élément **sans sous-sections mandatory** (le livrable attendu est suivi comme une unité), ce terme vaut `80 %` dès que le livrable attendu est **présent et conforme** (`sections conformes / total sections = 1`) et `0 %` sinon. **« Présent et non vide » est un plancher de forme, pas un niveau de sécurité ou de qualité atteint** : le fond est contrôlé par la revue (ci-dessous) ; un `80 %` ne vaut jamais « sécurisé ».
- **+10 % — revue** : le terme `(revue)` vaut `1` uniquement si le **verdict de revue** du reviewer dédié est **posté ET favorable, sans point bloquant ouvert**, et **rattaché à la version courante** du livrable (section 4). Pour les **éléments de surface de sécurité** (section 2), le terme `(revue)` exige le **verdict du Reviewer de sécurité** (SG-3) — la revue de cohérence s'ajoute mais ne s'y substitue jamais. Pour les autres éléments, le reviewer dédié est celui de la nature du livrable (cohérence par défaut).
- **+10 % — acceptation humaine** : le terme `(acceptation humaine)` vaut `1` si un **membre humain** de l'espace (auteur de type `member`) a **explicitement accepté** l'élément (gate granulaire « Keep / Modify / Redo » — source unique [`../conductor.md`](../conductor.md)), rattaché à la version courante (section 4). Un commentaire d'agent, **même cité par un humain**, ne compte pas. Aucun agent ne s'auto-accepte.

- **% section** : moyenne arithmétique des `% élément` de la section, arrondie à l'entier **pour l'affichage uniquement**.
- **% global** : moyenne arithmétique des `% élément` de **tous** les éléments, toutes sections, arrondie à l'entier **pour l'affichage uniquement**.
- **Arrondi** : l'arrondi à l'entier sert **uniquement à l'affichage**. Toute **comparaison à un seuil** (gate, section 7) se fait sur la **valeur non arrondie** (ex. 79,5 % reste `< 80 %`).

### Dénominateur dynamique

Le `total sections` d'un élément Livrables est lu **au moment du calcul** dans le contrat `required-sections`. Toute **nouvelle section/fichier mandatory** ajouté à ce contrat **s'ajoute automatiquement au total** : le terme `80 %` se recalcule sur le nouveau total, **sans** modifier la checklist ni ce protocole. La checklist ne fige jamais une copie du total ; elle renvoie à la source.

> **Garde-fou anti-abaissement (SG-3).** Un **retrait** ou un **assouplissement** d'une section mandatory **de sécurité** du contrat `required-sections` ferait **monter** mécaniquement les pourcentages. Un tel changement n'est recevable que sur **validation humaine explicite et tracée** (un contrôle lié à la sécurité ne s'abaisse jamais sans validation humaine tracée). Cette décision relève de `required-sections` (source unique) et d'un contrôle sécurité, pas de la checklist.

> **Double comptage.** Un même fichier peut alimenter deux éléments : `11-securite.md` compte dans le DAS **et** dans « Architecture de sécurité détaillée » ; `10-cycle_vie_donnees.md` compte dans le DAS **et** dans « Architecture de données détaillée ». C'est **assumé** (le DAS mesure la complétude d'ensemble, l'élément détaillé mesure la profondeur du volet) ; les deux éléments restent suivis et jugés séparément.

## 4. Mise à jour (écriture) — conformité objective, revue favorable versionnée, acceptation humaine

L'avancement d'un élément évolue uniquement par **faits vérifiables**, jamais par estimation :

1. **Terme 80 %** — recalculé à chaque vérification de conformité (section 6) : nombre de sections mandatory présentes et non vides / total (contrat `required-sections`). Un doute sur la conformité d'une section ⇒ elle **ne compte pas** (garde-fou « ne jamais deviner »).
2. **Terme +10 % revue** — passe à `1` uniquement quand le **verdict du reviewer dédié** (Reviewer de sécurité pour les éléments de surface de sécurité) est **posté, favorable et sans point bloquant ouvert**, **et** rattaché à la **version courante** du livrable. Un verdict « demande de corrections » ou portant un point bloquant **ne crédite pas** le terme. Le verdict n'est jamais rédigé ni supposé par le producteur.
3. **Terme +10 % acceptation humaine** — passe à `1` **uniquement** sur **annonce explicite d'un membre humain** (auteur `member`, cité par son identifiant dans la trace), rattachée à la **version courante** du livrable. Une validation d'agent — même relayée par un humain — ne suffit jamais.

**Rattachement à une version (anti-falsification, OWASP A08).** Les termes `+10 % revue` et `+10 % acceptation` sont crédités **pour une version précise** du livrable (référence de commit / révision d'issue tracée). **Dès qu'un contenu mandatory du livrable change**, les **deux** termes **retombent à `0`** (la revue et l'acceptation ne valent que pour la version évaluée) ; la remise à zéro est **tracée sur l'issue** et le crédit ne peut être rétabli que par une nouvelle revue favorable et une nouvelle acceptation sur la version modifiée.

En **cas de doute** sur la conformité, sur le sens du verdict de revue ou sur l'intention humaine : **ne jamais deviner** ; ne pas créditer le terme concerné ; informer l'humain et attendre (garde-fou « ne jamais deviner » + validation humaine granulaire — [`governance-security.md`](governance-security.md)). Chaque évolution de % est tracée sur l'issue **avant** d'être reportée dans le fichier d'état, avec sa **preuve** (section/verdict/acceptation) et la **version** concernée.

## 5. Lecture — sur demande humaine

Sur demande, le coordinateur affiche, en **prose réduite** (source unique [`output-format.md`](output-format.md)) :

- **chaque section** avec son **% d'avancement** ;
- pour **chaque élément**, son **% d'avancement** et, pour les Livrables, le **détail du décompte** (sections conformes / total, **revue ✓/✗ avec nature — sécurité pour les surfaces de sécurité**, acceptation humaine ✓/✗, version évaluée) ;
- pour un élément présenté **au gate** (section 7) : l'**état de la conformité complète** (toutes sections mandatory ✓/✗) **et** l'**état de la revue de sécurité ✓/✗**, de sorte qu'un déblocage sans conformité complète ou sans revue de sécurité soit **visible** ;
- le **% global**.

La lecture est une **restitution d'état** : elle ne modifie aucun % et ne vaut ni revue ni acceptation.

## 6. Vérification de conformité (préalable au terme 80 %)

Avant de créditer les sections conformes d'un élément, le coordinateur vérifie que :

- le ou les **documents attendus existent** et sont **au bon format** ;
- ils sont **clairs**, **sans note de génération d'agent** (réf. décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)), **sans doublon**, **sans incohérence** ;
- pour la section **Livrables**, les **sections mandatory** attendues du document sont **présentes et non vides**, selon le sensor [`required-sections`](../../sensors/sensors/required-sections.md) (**source unique** du contrat — ne pas le redupliquer ici ; le sensor reste **advisory** et **n'autorise jamais** à se passer de la validation humaine ni de la revue). Le décompte `sections conformes / total sections` en découle directement.

« Présent et non vide » est un **critère de forme** : il **n'atteste pas** de la qualité ni de la sécurité du contenu. Le **contrôle de fond** relève de la **revue** (section 3-4) — pour les éléments de surface de sécurité, la **revue de sécurité** (SG-3). Toute vérification en échec ou toute ambiguïté ⇒ **la section ne compte pas** ; informer l'humain (section 4).

### Mapping élément Livrables → document(s) attendu(s)

| Élément de la section **Livrables** | Document(s) attendu(s) dans `documentation/` | Contrat de sections (décompte du 80 %) |
| --- | --- | --- |
| Architecture de solution (DAS) | fichiers mandatory du DAS (`001`, `01`, `02`, `06`, `08`, `10`, `11`) | sensor [`required-sections`](../../sensors/sensors/required-sections.md), volet `das:` |
| Architecture Logicielle détaillée | `documentation/00-architecture-detaillee.md` (volet logiciel) | gabarit DAS `00-architecture-detaillee` |
| Architecture de données détaillée | `documentation/10-cycle_vie_donnees.md` + modèles de données | sensor [`data-lifecycle`](../../sensors/sensors/data-lifecycle.md) |
| **Architecture de sécurité détaillée** *(surface de sécurité)* | `documentation/11-securite.md` (STRIDE / OWASP) | sensor [`required-sections`](../../sensors/sensors/required-sections.md), fichier `11-securite.md` |
| Architecture infrastructure détaillée | `documentation/09-deploiement.md` + diagrammes d'infrastructure | gabarit DAS `09-deploiement` |

> Le mapping s'appuie sur les sources uniques existantes (`required-sections`, `data-lifecycle`, gabarits DAS). En cas d'écart de nommage ou de découpage, **ces sources font foi** ; la checklist ne redéfinit aucun contrat de sections. Le **total sections** utilisé au dénominateur du 80 % est toujours lu dans ces sources (dénominateur dynamique, section 3). La **conformité du jugement** des éléments sans contrat de sections mandatory (Cadrage, Besoins, Projets) relève de la **revue de cohérence** (qui juge, sur quelle base) ; en l'absence de base objective, le coordinateur **ne devine pas** et informe l'humain.

## 7. Gate de planification / réalisation

Le gate de déblocage de la planification / réalisation s'applique **par élément**, jamais sur une moyenne. Un `% global` ou un `% section` élevé **ne débloque jamais** à lui seul : la moyenne ne compense pas un élément faible.

Un élément est **débloquable** uniquement si **toutes** les conditions suivantes sont réunies :

1. **Conformité complète** — **toutes** les sections mandatory de l'élément sont conformes (présentes et non vides), soit `sections conformes / total sections = 1` (ex. DAS : 7/7). Le pourcentage reste un **indicateur d'avancement** ; le critère de déblocage est la **conformité complète**, pas le seuil `≥ 80 %`. Une seule section mandatory manquante ⇒ **bloqué**, même si le total atteint 80 % ou plus grâce aux `+10 %`.
2. **Revue de sécurité pour les surfaces de sécurité** — pour les **éléments de surface de sécurité** (Besoins → Sécurité, Architecture de sécurité détaillée), le **verdict favorable du Reviewer de sécurité** (SG-3) sur la version courante est **requis avant le déblocage**. Le gate **ne remplace pas** cette revue et **ne conditionne pas** son déclenchement.
3. **Décision humaine** — même toutes conditions réunies, le lancement reste **soumis à la décision humaine** (gate granulaire). Le gate **n'automatise aucun lancement**.

L'**acceptation humaine** d'un élément et la **revue de cohérence** peuvent intervenir **en parallèle** du déblocage **des éléments hors surface de sécurité**. Pour les surfaces de sécurité, la revue de sécurité **précède** le déblocage (point 2 ci-dessus).

Au moment où un gate est présenté à l'humain, le coordinateur **affiche l'état de la conformité complète (✓/✗) et l'état de la revue de sécurité (✓/✗)** de l'élément (section 5), de sorte qu'aucun déblocage ne puisse se faire sans que l'écart soit visible.

Les gates de phase et la validation humaine granulaire restent définis en source unique dans [`../conductor.md`](../conductor.md) et [`governance-security.md`](governance-security.md) ; ce gate s'y raccorde sans les redéfinir.

## 8. Ce que ce protocole ne change pas (garde-fous)

- **Validation humaine granulaire** — le terme `+10 %` d'acceptation n'est crédité que sur annonce explicite d'un **membre humain** ; aucun scope, aucune règle apprise, aucun sensor advisory, aucun seuil de % ne peut s'y substituer (invariants [`../conductor.md`](../conductor.md), [`governance-security.md`](governance-security.md)).
- **Revue de sécurité non substituable (SG-3)** — sur toute architecture ou surface de sécurité, la **revue de sécurité précède** la validation humaine ; **ni le gate ni le pourcentage ne la remplacent** et ne conditionnent son déclenchement. Un contrôle lié à la sécurité ne s'abaisse jamais sans validation humaine tracée.
- **Piste d'audit sur l'issue** — chaque évolution de % y est tracée avec sa preuve et la version concernée ; le fichier d'état ne porte aucune méta-production (décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)).
- **Sensors advisory** — `required-sections` et `data-lifecycle` **assistent** le décompte des sections conformes sans jamais bloquer ni remplacer la validation humaine ni la revue (SG-1..6).
- **Ne jamais deviner** — un % ne résulte que d'une vérification objective (présent + non vide, verdict favorable posté, acceptation annoncée par un membre) ; doute ⇒ ne pas créditer, informer l'humain.
- **Langue** — français par défaut (humain) ; voir [`../conductor.md`](../conductor.md), « OBLIGATOIRE : langue et format ».
