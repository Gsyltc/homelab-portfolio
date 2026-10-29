# Protocole — checklist d'architecture (cycle lecture / écriture)

**Source unique** du **processus de checklist d'architecture** du workflow `core` : comment l'**état d'avancement de l'architecture** est tenu, lu et mis à jour tout au long des **5 phases** (`Initialization → Ideation → Inception → Construction → Operation`). La checklist est un **processus à part** — ni un stage, ni un livrable d'architecture : elle **suit** l'avancement des livrables sans les produire. Ce protocole fixe la **mécanique** (structure, calcul du %, règles d'écriture, vérification de conformité) ; il ne redéfinit **ni** les gates de phase et la validation humaine granulaire — source unique [`../conductor.md`](../conductor.md) et [`governance-security.md`](governance-security.md) — **ni** les sections mandatory des livrables — source unique [`../../sensors/sensors/required-sections.md`](../../sensors/sensors/required-sections.md).

> **Qui est concerné.** Le **coordinateur** (Architecture Solution & Intégration) tient la checklist : il la lit sur demande humaine et ne met un élément à jour que sur **approbation humaine explicite**, après **vérification de conformité**. Les agents spécialisés produisent les livrables ; ils ne valident **jamais** eux-mêmes un élément de la checklist.

## 1. État de la checklist (où il vit)

- L'**état** est un **livrable versionné** du projet : `documentation/00-checklist-architecture.md`, copié depuis le gabarit [`gabarits/00-checklist-architecture.md`](gabarits/00-checklist-architecture.md) à l'initialisation du répertoire projet (Phase 0, [`../stages/initialization/directory-check.md`](../stages/initialization/directory-check.md)).
- Chaque **changement de statut** est **aussi tracé sur l'issue** (piste d'audit — source unique [`../conductor.md`](../conductor.md), « OBLIGATOIRE : piste d'audit sur l'issue ») : objet, ancien statut → nouveau statut, référence du ou des documents, verdict de conformité.
- Le fichier d'état est un **livrable** : il est soumis à l'invariant **« aucune note de génération / méta-production »** (réf. décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)). La traçabilité (qui a validé, quand, via quelle issue) vit **sur l'issue**, pas dans le fichier.

## 2. Structure imposée (sections et éléments)

Quatre sections, éléments **fixes** ; aucun ajout / retrait sans décision tracée (ADR). Statut par défaut `non débuté`.

- **Cadrage**
- **Besoins (MoSCoW)** — Entreprises et affaires · Solutions · Technologique · Sécurité
- **Livrables** — Architecture de solution (DAS) · Architecture Logicielle détaillée · Architecture de données détaillée · Architecture de sécurité détaillée · Architecture infrastructure détaillée
- **Projets** — Planification · Coûts · Risques · Exploitation · Arrimages

Statuts possibles par élément : `validé` · `en cours` · `refusé` · `non débuté`.

## 3. Calcul du pourcentage

- **Par section** : `% section = (nombre d'éléments validé) / (nombre total d'éléments de la section)`, arrondi à l'entier.
- **Global** : `% global = (nombre total d'éléments validé) / (nombre total d'éléments, toutes sections)`, arrondi à l'entier.
- Seul le statut `validé` compte. `en cours`, `refusé`, `non débuté` **ne comptent pas** comme validés.
- Une section à élément unique (Cadrage) vaut `0 %` ou `100 %`.

## 4. Mise à jour (écriture) — uniquement sur approbation humaine

Un élément ne passe à `validé` **que** si **les deux** conditions sont réunies :

1. **Annonce explicite de l'humain** que l'élément est accepté (gate de validation humaine granulaire — source unique [`../conductor.md`](../conductor.md), « La boucle aux gates : Keep / Modify / Redo »). Une validation d'agent ne suffit jamais.
2. **Vérification de conformité** réussie (section 6).

Autres transitions :

- `en cours` — travail engagé, pas encore accepté (information, sans gate).
- `refusé` — l'humain a rejeté (❌ Redo) l'élément ou son livrable ; tracer le motif sur l'issue.
- `non débuté` — défaut ; aucun travail engagé.

En **cas de doute** sur la conformité ou sur l'intention humaine : **ne jamais deviner, ne pas valider** ; informer l'humain et attendre (garde-fou « ne jamais deviner » + validation humaine granulaire — [`governance-security.md`](governance-security.md)). Chaque changement de statut est tracé sur l'issue **avant** d'être reporté dans le fichier d'état.

## 5. Lecture — sur demande humaine

Sur demande, le coordinateur affiche, en **prose réduite** (source unique [`output-format.md`](output-format.md)) :

- **chaque section** avec son **% d'avancement** ;
- pour **chaque élément**, son **statut** (`validé` / `en cours` / `refusé` / `non débuté`) ;
- le **% global**.

La lecture est une **restitution d'état** : elle ne modifie aucun statut et ne vaut pas validation.

## 6. Vérification de conformité (préalable à `validé`)

Avant de passer un élément à `validé`, le coordinateur vérifie que :

- le ou les **documents attendus existent** et sont **au bon format** ;
- ils sont **clairs**, **sans note de génération d'agent** (réf. décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)), **sans doublon**, **sans incohérence** ;
- pour la section **Livrables**, les **sections mandatory** attendues du document sont **présentes et non vides**, selon le sensor [`required-sections`](../../sensors/sensors/required-sections.md) (**source unique** du contrat — ne pas le redupliquer ici ; le sensor reste **advisory** et **n'autorise jamais** à se passer de la validation humaine).

Toute vérification en échec ou toute ambiguïté ⇒ **ne pas valider**, informer l'humain (section 4).

### Mapping élément Livrables → document(s) attendu(s)

| Élément de la section **Livrables** | Document(s) attendu(s) dans `documentation/` | Contrat de sections |
| --- | --- | --- |
| Architecture de solution (DAS) | fichiers mandatory du DAS (`001`, `01`, `02`, `06`, `08`, `10`, `11`) | sensor [`required-sections`](../../sensors/sensors/required-sections.md), volet `das:` |
| Architecture Logicielle détaillée | `documentation/00-architecture-detaillee.md` (volet logiciel) | gabarit DAS `00-architecture-detaillee` |
| Architecture de données détaillée | `documentation/10-cycle_vie_donnees.md` + modèles de données | sensor [`data-lifecycle`](../../sensors/sensors/data-lifecycle.md) |
| Architecture de sécurité détaillée | `documentation/11-securite.md` (STRIDE / OWASP) | sensor [`required-sections`](../../sensors/sensors/required-sections.md), fichier `11-securite.md` |
| Architecture infrastructure détaillée | `documentation/09-deploiement.md` + diagrammes d'infrastructure | gabarit DAS `09-deploiement` |

> Le mapping s'appuie sur les sources uniques existantes (`required-sections`, `data-lifecycle`, gabarits DAS). En cas d'écart de nommage ou de découpage, **ces sources font foi** ; la checklist ne redéfinit aucun contrat de sections.

## 7. Ce que ce protocole ne change pas (garde-fous)

- **Validation humaine granulaire** — un élément n'est `validé` que sur annonce humaine explicite ; aucun scope, aucune règle apprise, aucun sensor advisory ne peut l'y substituer (invariants [`../conductor.md`](../conductor.md), [`governance-security.md`](governance-security.md)).
- **Piste d'audit sur l'issue** — chaque changement de statut y est tracé ; le fichier d'état ne porte aucune méta-production (décision [`0040`](../../../decisions/0040-aucune-note-de-generation-dans-les-livrables.md)).
- **Sensors advisory** — `required-sections` et `data-lifecycle` **assistent** la vérification de conformité sans jamais bloquer ni remplacer la validation humaine (SG-1..6).
- **Ne jamais deviner** — doute sur la conformité ou l'intention ⇒ informer l'humain, ne pas valider.
- **Langue** — français par défaut (humain) ; voir [`../conductor.md`](../conductor.md), « OBLIGATOIRE : langue et format ».
