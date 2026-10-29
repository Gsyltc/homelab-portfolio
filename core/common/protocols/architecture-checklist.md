# Protocole — checklist d'architecture (cycle lecture / écriture)

**Source unique** du **processus de checklist d'architecture** du workflow `core` : comment l'**état d'avancement de l'architecture** est tenu, lu et mis à jour tout au long des **5 phases** (`Initialization → Ideation → Inception → Construction → Operation`). La checklist est un **processus à part** — ni un stage, ni un livrable d'architecture : elle **suit** l'avancement des livrables sans les produire. Ce protocole fixe la **mécanique** (structure, calcul du %, barème, règles d'écriture, vérification de conformité) ; il ne redéfinit **ni** les gates de phase et la validation humaine granulaire — source unique [`../conductor.md`](../conductor.md) et [`governance-security.md`](governance-security.md) — **ni** les sections mandatory des livrables — source unique [`../../sensors/sensors/required-sections.md`](../../sensors/sensors/required-sections.md).

> **Qui est concerné.** Le **coordinateur** (Architecture Solution & Intégration) tient la checklist : il la lit sur demande humaine et ne met à jour l'avancement d'un élément que sur **vérification de conformité objective** et, pour l'acceptation, sur **approbation humaine explicite**. Les agents spécialisés produisent les livrables ; ils ne s'auto-valident **jamais**.

## 1. État de la checklist (où il vit)

- L'**état** est un **livrable versionné** du projet : `documentation/00-checklist-architecture.md`, copié depuis le gabarit [`gabarits/00-checklist-architecture.md`](gabarits/00-checklist-architecture.md) à l'initialisation du répertoire projet (Phase 0, [`../stages/initialization/directory-check.md`](../stages/initialization/directory-check.md)).
- Chaque **changement d'avancement** est **aussi tracé sur l'issue** (piste d'audit — source unique [`../conductor.md`](../conductor.md), « OBLIGATOIRE : piste d'audit sur l'issue ») : objet, ancien % → nouveau %, ce qui l'a fait évoluer (section conforme, revue pair, acceptation humaine), référence du ou des documents, verdict de conformité.
- Le fichier d'état est un **livrable** : il est soumis à l'invariant **« aucune note de génération / méta-production »** (réf. décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)). La traçabilité (qui a validé, quand, via quelle issue) vit **sur l'issue**, pas dans le fichier.

## 2. Structure imposée (sections et éléments)

Quatre sections, éléments **fixes** ; aucun ajout / retrait d'élément sans décision tracée (ADR). Avancement par défaut `0 %`.

- **Cadrage**
- **Besoins (MoSCoW)** — Entreprises et affaires · Solutions · Technologique · Sécurité
- **Livrables** — Architecture de solution (DAS) · Architecture Logicielle détaillée · Architecture de données détaillée · Architecture de sécurité détaillée · Architecture infrastructure détaillée
- **Projets** — Planification · Coûts · Risques · Exploitation · Arrimages

Chaque élément listé est une **unité suivie** et porte un **pourcentage d'avancement** (0 à 100 %), calculé selon le barème de la section 3.

## 3. Calcul du pourcentage (barème 80/10/10)

Chaque élément est noté selon le **même barème homogène** :

```
% élément = 80 × (sections conformes / total sections) + 10·(revue pair) + 10·(acceptation humaine)
```

arrondi à l'entier. Les trois termes :

- **80 % — conformité documentaire** : proportion des **sections mandatory présentes et non vides** du ou des documents attendus pour l'élément. `sections conformes` et `total sections` se lisent dans le contrat du sensor [`required-sections`](../../sensors/sensors/required-sections.md) (**source unique**, non dupliqué ici). Pour un élément **sans sous-sections mandatory** (le livrable attendu est suivi comme une unité), ce terme vaut `80 %` dès que le livrable attendu est **présent et conforme** (`sections conformes / total sections = 1`) et `0 %` sinon.
- **+10 % — revue par un pair** : le terme `(revue pair)` vaut `1` si une **revue par un pair** (reviewer dédié) a été réalisée et postée, `0` sinon.
- **+10 % — acceptation humaine** : le terme `(acceptation humaine)` vaut `1` si l'humain a **explicitement accepté** l'élément (gate granulaire « Keep / Modify / Redo » — source unique [`../conductor.md`](../conductor.md)), `0` sinon. Aucun agent ne s'auto-accepte.

- **% section** : moyenne arithmétique des `% élément` de la section, arrondie à l'entier.
- **% global** : moyenne arithmétique des `% élément` de **tous** les éléments, toutes sections, arrondie à l'entier.

### Dénominateur dynamique

Le `total sections` d'un élément Livrables est lu **au moment du calcul** dans le contrat `required-sections`. Toute **nouvelle section/fichier mandatory** ajouté à ce contrat **s'ajoute automatiquement au total** : le terme `80 %` se recalcule sur le nouveau total, **sans** modifier la checklist ni ce protocole. La checklist ne fige jamais une copie du total ; elle renvoie à la source.

## 4. Mise à jour (écriture) — conformité objective + acceptation humaine

L'avancement d'un élément évolue uniquement par **faits vérifiables**, jamais par estimation :

1. **Terme 80 %** — recalculé à chaque vérification de conformité (section 6) : nombre de sections mandatory présentes et non vides / total (contrat `required-sections`). Un doute sur la conformité d'une section ⇒ elle **ne compte pas** (garde-fou « ne jamais deviner »).
2. **Terme +10 % revue pair** — passe à `1` uniquement quand le **verdict de revue** du reviewer dédié est **posté** (il n'est jamais rédigé ni supposé par le producteur).
3. **Terme +10 % acceptation humaine** — passe à `1` **uniquement** sur **annonce humaine explicite** d'acceptation (gate de validation humaine granulaire — source unique [`../conductor.md`](../conductor.md)). Une validation d'agent ne suffit jamais.

En **cas de doute** sur la conformité, sur la tenue d'une revue ou sur l'intention humaine : **ne jamais deviner** ; ne pas créditer le terme concerné ; informer l'humain et attendre (garde-fou « ne jamais deviner » + validation humaine granulaire — [`governance-security.md`](governance-security.md)). Chaque évolution de % est tracée sur l'issue **avant** d'être reportée dans le fichier d'état.

## 5. Lecture — sur demande humaine

Sur demande, le coordinateur affiche, en **prose réduite** (source unique [`output-format.md`](output-format.md)) :

- **chaque section** avec son **% d'avancement** ;
- pour **chaque élément**, son **% d'avancement** et, pour les Livrables, le **détail du décompte** (sections conformes / total, revue pair ✓/✗, acceptation humaine ✓/✗) ;
- le **% global**.

La lecture est une **restitution d'état** : elle ne modifie aucun % et ne vaut ni revue ni acceptation.

## 6. Vérification de conformité (préalable au terme 80 %)

Avant de créditer les sections conformes d'un élément, le coordinateur vérifie que :

- le ou les **documents attendus existent** et sont **au bon format** ;
- ils sont **clairs**, **sans note de génération d'agent** (réf. décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)), **sans doublon**, **sans incohérence** ;
- pour la section **Livrables**, les **sections mandatory** attendues du document sont **présentes et non vides**, selon le sensor [`required-sections`](../../sensors/sensors/required-sections.md) (**source unique** du contrat — ne pas le redupliquer ici ; le sensor reste **advisory** et **n'autorise jamais** à se passer de la validation humaine). Le décompte `sections conformes / total sections` en découle directement.

Toute vérification en échec ou toute ambiguïté ⇒ **la section ne compte pas** ; informer l'humain (section 4).

### Mapping élément Livrables → document(s) attendu(s)

| Élément de la section **Livrables** | Document(s) attendu(s) dans `documentation/` | Contrat de sections (décompte du 80 %) |
| --- | --- | --- |
| Architecture de solution (DAS) | fichiers mandatory du DAS (`001`, `01`, `02`, `06`, `08`, `10`, `11`) | sensor [`required-sections`](../../sensors/sensors/required-sections.md), volet `das:` |
| Architecture Logicielle détaillée | `documentation/00-architecture-detaillee.md` (volet logiciel) | gabarit DAS `00-architecture-detaillee` |
| Architecture de données détaillée | `documentation/10-cycle_vie_donnees.md` + modèles de données | sensor [`data-lifecycle`](../../sensors/sensors/data-lifecycle.md) |
| Architecture de sécurité détaillée | `documentation/11-securite.md` (STRIDE / OWASP) | sensor [`required-sections`](../../sensors/sensors/required-sections.md), fichier `11-securite.md` |
| Architecture infrastructure détaillée | `documentation/09-deploiement.md` + diagrammes d'infrastructure | gabarit DAS `09-deploiement` |

> Le mapping s'appuie sur les sources uniques existantes (`required-sections`, `data-lifecycle`, gabarits DAS). En cas d'écart de nommage ou de découpage, **ces sources font foi** ; la checklist ne redéfinit aucun contrat de sections. Le **total sections** utilisé au dénominateur du 80 % est toujours lu dans ces sources (dénominateur dynamique, section 3).

## 7. Gate de planification / réalisation (seuil ≥ 80 %)

Le % d'avancement conditionne un **gate** de déblocage de la planification / réalisation :

- **`< 80 %` ⇒ bloqué** : la planification / réalisation ne peut pas être lancée.
- **`≥ 80 %` ⇒ déblocage possible** : le lancement devient envisageable, mais reste **soumis à la décision humaine**. La **revue par un pair** et l'**acceptation humaine** (les deux `+10 %`) peuvent se faire **en parallèle** du déblocage.

Le gate **n'automatise aucun lancement** : il informe la décision humaine, sans la remplacer. Les gates de phase et la validation humaine granulaire restent définis en source unique dans [`../conductor.md`](../conductor.md) et [`governance-security.md`](governance-security.md) ; ce seuil s'y raccorde sans les redéfinir.

## 8. Ce que ce protocole ne change pas (garde-fous)

- **Validation humaine granulaire** — le terme `+10 %` d'acceptation n'est crédité que sur annonce humaine explicite ; aucun scope, aucune règle apprise, aucun sensor advisory, aucun seuil de % ne peut s'y substituer (invariants [`../conductor.md`](../conductor.md), [`governance-security.md`](governance-security.md)).
- **Piste d'audit sur l'issue** — chaque évolution de % y est tracée ; le fichier d'état ne porte aucune méta-production (décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)).
- **Sensors advisory** — `required-sections` et `data-lifecycle` **assistent** le décompte des sections conformes sans jamais bloquer ni remplacer la validation humaine (SG-1..6).
- **Ne jamais deviner** — un % ne résulte que d'une vérification objective (présent + non vide, revue postée, acceptation annoncée) ; doute ⇒ ne pas créditer, informer l'humain.
- **Langue** — français par défaut (humain) ; voir [`../conductor.md`](../conductor.md), « OBLIGATOIRE : langue et format ».
