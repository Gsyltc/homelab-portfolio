# Protocole — checklist d'architecture (cycle lecture / écriture)

**Source unique** du **processus de checklist d'architecture** du workflow `core` : comment l'**état d'avancement de l'architecture** est tenu, lu et mis à jour tout au long des **5 phases** (`Initialization → Ideation → Inception → Construction → Operation`). La checklist est un **processus à part** — ni un stage, ni un livrable d'architecture : elle **suit** l'avancement des livrables sans les produire. Ce protocole fixe la **mécanique** (structure, calcul du %, règles d'écriture, vérification de conformité) ; il ne redéfinit **ni** les gates de phase et la validation humaine granulaire — source unique [`../conductor.md`](../conductor.md) et [`governance-security.md`](governance-security.md) — **ni** les sections mandatory des livrables — source unique [`../../sensors/sensors/required-sections.md`](../../sensors/sensors/required-sections.md).

> **Qui est concerné.** Le **coordinateur** (Architecture Solution & Intégration) tient la checklist : il la lit sur demande humaine et ne fait **progresser le % d'un élément** que sur des faits **vérifiés** — conformité des sections, revue par un pair, et **acceptation humaine explicite** pour la part finale. Les agents spécialisés produisent les livrables ; ils ne s'**auto-acceptent jamais** un élément de la checklist.

## 1. État de la checklist (où il vit)

- L'**état** est un **livrable versionné** du projet : `documentation/00-checklist-architecture.md`, copié depuis le gabarit [`gabarits/00-checklist-architecture.md`](gabarits/00-checklist-architecture.md) à l'initialisation du répertoire projet (Phase 0, [`../stages/initialization/directory-check.md`](../stages/initialization/directory-check.md)).
- Chaque **changement de %** (et la composante qui l'a produit : sections conformes, revue pair, acceptation humaine) est **aussi tracé sur l'issue** (piste d'audit — source unique [`../conductor.md`](../conductor.md), « OBLIGATOIRE : piste d'audit sur l'issue ») : objet, ancien % → nouveau %, composante modifiée, référence du ou des documents, verdict de conformité.
- Le fichier d'état est un **livrable** : il est soumis à l'invariant **« aucune note de génération / méta-production »** (réf. décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)). La traçabilité (qui a accepté, quand, via quelle issue) vit **sur l'issue**, pas dans le fichier.

## 2. Structure imposée (sections et éléments)

Quatre sections, éléments **fixes** ; aucun ajout / retrait sans décision tracée (ADR). Chaque élément porte un **pourcentage d'avancement** (0–100, défaut `0 %`).

- **Cadrage**
- **Besoins (MoSCoW)** — Entreprises et affaires · Solutions · Technologique · Sécurité
- **Livrables** — Architecture de solution (DAS) · Architecture Logicielle détaillée · Architecture de données détaillée · Architecture de sécurité détaillée · Architecture infrastructure détaillée
- **Projets** — Planification · Coûts · Risques · Exploitation · Arrimages

Chaque élément est suivi **en pourcentage** selon le **barème 80/10/10** de la section 3. Un élément n'atteint **100 %** que lorsque sa part « sections conformes » est complète **et** que sa **revue par un pair** et son **acceptation humaine** sont réalisées.

## 3. Calcul du pourcentage (barème 80/10/10)

Chaque élément est noté **en pourcentage** selon un barème **homogène** à toutes les sections :

```
% élément = 80 × (sections conformes / total sections mandatory)
          + 10 × (revue pair réalisée)
          + 10 × (acceptation humaine)
```

où `revue pair réalisée` et `acceptation humaine` valent `0` ou `1`. Résultat arrondi à l'entier.

- **Part 80 % — conformité des sections.** Pour un **livrable** (section Livrables), `sections conformes / total sections mandatory` est la proportion des **sections mandatory** du ou des documents attendus qui sont **présentes et conformes** (section 6), d'après le contrat **source unique** [`required-sections`](../../sensors/sensors/required-sections.md). Pour les éléments **sans sous-sections mandatory décomptées** (Cadrage, Besoins MoSCoW, Projets), la part 80 % est **binaire** : `0` tant que l'élément n'est pas présent et conforme, `80` dès qu'il l'est — l'élément est traité comme une **unité suivie**.
- **Part +10 % — revue par un pair.** Ajoutée **une fois** qu'une **revue par un pair** (peer review) de l'élément a été réalisée et tracée sur l'issue.
- **Part +10 % — acceptation humaine.** Ajoutée **une fois** que l'humain a **explicitement accepté** l'élément (gate de validation humaine granulaire — source unique [`../conductor.md`](../conductor.md), « La boucle aux gates : Keep / Modify / Redo »). Aucun agent ne s'auto-accepte.

Les trois parts sont **indépendantes** : la revue pair et l'acceptation peuvent se faire **en parallèle** du travail sur les sections. Un élément à **100 %** a toutes ses sections conformes **et** sa revue pair **et** son acceptation humaine.

### Dénominateur dynamique

Le `total sections mandatory` d'un livrable est celui du contrat `required-sections` **au moment du calcul**. Toute **section ou fichier mandatory ajouté au fil de l'eau** s'ajoute au **dénominateur total** ; la part 80 % se **recalcule** sur le nouveau total (une section nouvellement requise non encore produite **abaisse** mécaniquement le %). La checklist ne redéfinit **aucun** contrat de sections : `required-sections` fait foi.

### Agrégation (section et global)

- **% section** = **moyenne** des % de ses éléments, arrondie à l'entier.
- **% global** = **moyenne** des % de **tous** les éléments, toutes sections confondues, arrondie à l'entier.

### Gate de planification / réalisation

Le % sert de **gate** au lancement de la planification / réalisation :

- **`< 80 %` ⇒ bloqué** : le lancement n'est pas autorisé.
- **`≥ 80 %` ⇒ déblocage possible** : le lancement devient autorisable, **soumis à décision humaine**. Le seuil est une condition **nécessaire, non suffisante** — il ne remplace **ni** la validation humaine **ni** le contrôle sécurité. La revue pair (+10 %) et l'acceptation (+10 %) peuvent se poursuivre **en parallèle** après déblocage.

## 4. Mise à jour (écriture) — composantes du %

Le % d'un élément n'évolue que par la mise à jour de ses **trois composantes**, chacune sur un fait **vérifié** :

1. **Part 80 % (sections conformes)** — recalculée après **vérification de conformité** (section 6) du ou des documents attendus. Une section ne compte comme conforme que si elle est **présente et non vide** ; en cas de doute, elle **ne compte pas** (« ne jamais deviner »).
2. **Part +10 % (revue pair)** — ajoutée lorsqu'une **revue par un pair** a été réalisée et tracée sur l'issue.
3. **Part +10 % (acceptation humaine)** — ajoutée **uniquement** sur **annonce explicite de l'humain** que l'élément est accepté (gate de validation humaine granulaire — source unique [`../conductor.md`](../conductor.md), « La boucle aux gates : Keep / Modify / Redo »). Une validation d'agent ne suffit **jamais**.

L'acceptation humaine (+10 %) est le **seul** chemin vers **100 %** : aucun scope, aucune règle apprise, aucun sensor advisory ne s'y substitue. Si l'humain **rejette** (❌ Redo) un élément ou son livrable, le motif est tracé sur l'issue et la part acceptation **reste à 0** jusqu'à reprise.

En **cas de doute** sur la conformité d'une section ou sur l'intention humaine : **ne jamais deviner, ne pas compter la part concernée** ; informer l'humain et attendre (garde-fou « ne jamais deviner » + validation humaine granulaire — [`governance-security.md`](governance-security.md)). Chaque changement de % (et de la composante qui l'a produit) est tracé sur l'issue **avant** d'être reporté dans le fichier d'état : objet, ancien % → nouveau %, composante modifiée, verdict de conformité, référence du ou des documents.

## 5. Lecture — sur demande humaine

Sur demande, le coordinateur affiche, en **prose réduite** (source unique [`output-format.md`](output-format.md)) :

- **chaque section** avec son **% d'avancement** ;
- pour **chaque élément**, son **% d'avancement** et, pour les Livrables, le **détail des trois composantes** (sections conformes / total, revue pair, acceptation) le cas échéant ;
- le **% global** ;
- pour les éléments soumis au **gate** planification / réalisation, l'indication **bloqué (`< 80 %`)** ou **déblocable (`≥ 80 %`)**.

La lecture est une **restitution d'état** : elle ne modifie aucun % et ne vaut ni revue pair ni acceptation.

## 6. Vérification de conformité (décompte de la part 80 %)

Pour établir la **part 80 %** d'un élément (proportion `sections conformes / total sections mandatory`), le coordinateur vérifie que :

- le ou les **documents attendus existent** et sont **au bon format** ;
- ils sont **clairs**, **sans note de génération d'agent** (réf. décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)), **sans doublon**, **sans incohérence** ;
- pour la section **Livrables**, **chaque section mandatory** attendue du document est comptée **conforme** uniquement si elle est **présente et non vide**, selon le sensor [`required-sections`](../../sensors/sensors/required-sections.md) (**source unique** du contrat et du **total** servant de dénominateur — ne pas le redupliquer ici ; le sensor reste **advisory** et **n'autorise jamais** à se passer de la validation humaine).

Le **total** de sections mandatory (dénominateur) est celui du contrat `required-sections` **au moment du calcul** (dénominateur dynamique, section 3). Toute section en échec de vérification ou ambiguë **ne compte pas** comme conforme ⇒ elle **abaisse** la part 80 %. En cas de doute, **ne pas compter**, informer l'humain (section 4).

Les parts **+10 % (revue pair)** et **+10 % (acceptation humaine)** sont **indépendantes** de ce décompte : elles s'ajoutent sur réalisation effective (revue tracée) et sur annonce humaine explicite, sans attendre que les sections soient toutes conformes.

### Mapping élément Livrables → document(s) attendu(s)

| Élément de la section **Livrables** | Document(s) attendu(s) dans `documentation/` | Contrat de sections |
| --- | --- | --- |
| Architecture de solution (DAS) | fichiers mandatory du DAS (`001`, `01`, `02`, `06`, `08`, `10`, `11`) | sensor [`required-sections`](../../sensors/sensors/required-sections.md), volet `das:` |
| Architecture Logicielle détaillée | `documentation/00-architecture-detaillee.md` (volet logiciel) | gabarit DAS `00-architecture-detaillee` |
| Architecture de données détaillée | `documentation/10-cycle_vie_donnees.md` + modèles de données | sensor [`data-lifecycle`](../../sensors/sensors/data-lifecycle.md) |
| Architecture de sécurité détaillée | `documentation/11-securite.md` (STRIDE / OWASP) | sensor [`required-sections`](../../sensors/sensors/required-sections.md), fichier `11-securite.md` |
| Architecture infrastructure détaillée | `documentation/09-deploiement.md` + diagrammes d'infrastructure | gabarit DAS `09-deploiement` |

> Le mapping s'appuie sur les sources uniques existantes (`required-sections`, `data-lifecycle`, gabarits DAS). Le **total de sections mandatory** de chaque livrable — dénominateur de la part 80 % — provient de ces sources (volet `das:` de `required-sections` pour le DAS). En cas d'écart de nommage ou de découpage, **ces sources font foi** ; la checklist ne redéfinit aucun contrat de sections.

## 7. Ce que ce protocole ne change pas (garde-fous)

- **Validation humaine granulaire** — la part **+10 % acceptation** d'un élément n'est ajoutée que sur annonce humaine explicite, et reste le **seul** chemin vers **100 %** ; aucun scope, aucune règle apprise, aucun sensor advisory ne peut l'y substituer (invariants [`../conductor.md`](../conductor.md), [`governance-security.md`](governance-security.md)).
- **Piste d'audit sur l'issue** — chaque changement de % (et la composante qui l'a produit) y est tracé ; le fichier d'état ne porte aucune méta-production (décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)).
- **Sensors advisory** — `required-sections` et `data-lifecycle` **assistent** le décompte de la part 80 % sans jamais bloquer ni remplacer la validation humaine (SG-1..6).
- **Gate ≥ 80 % non suffisant** — le seuil de déblocage planification / réalisation est une condition nécessaire, jamais une validation automatique : le lancement reste une décision humaine.
- **Ne jamais deviner** — doute sur la conformité d'une section ou l'intention humaine ⇒ informer l'humain, ne pas compter la part concernée.
- **Langue** — français par défaut (humain) ; voir [`../conductor.md`](../conductor.md), « OBLIGATOIRE : langue et format ».
