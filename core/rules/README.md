# Règles persistantes — mémoire du workflow

Mémoire de règles **multi-couches**, alimentée par la **boucle d'apprentissage** ([`governance-security`](../common/protocols/governance-security.md)).

- Elle capitalise les **corrections humaines validées**, pour qu'un agent ne répète pas la même erreur d'un projet à l'autre.
- Les règles sont des **fichiers Markdown versionnés**, lus au démarrage de chaque workflow (chargement paresseux, voir « Couches »).

## Alignement sur le contrat amont (« Rules and the Learning Loop »)

Alignée sur le contrat amont (*Harness Engineer Guide*), avec des **divergences assumées** ([`decisions/0011`](../../decisions/0011-alignement-memoire-de-regles-sur-ai-dlc.md), [`decisions/0004`](../../decisions/0004-boucle-apprentissage-et-regles-persistantes.md)) :

- **Couches** : 4 (`workspace > project > phase > scope`) au lieu de 5 (`org → team → project → phase → stage`).
  - `org` + `team` fusionnés dans `workspace` (le workspace Multica est l'organisation et l'équipe).
  - `stage` : réservée par l'amont pour plus tard ; non créée ici.
  - `scope` : couche maison, pont avec les scopes ([`decisions/0003`](../../decisions/0003-scopes-et-axes-depth-verification.md)).
- **Emplacement** : `core/rules/` (et non `core/memory/`), cohérent avec `core/sensors/` et `core/common/`. La portée reste dérivable du chemin.
- **Phases** : 4 fichiers (`ideation`, `inception`, `construction`, `operation`) ; `initialization` n'a pas de règles.
- **Précédence** : explicite (voir « Couches »), là où l'amont est strict-additif. Les deux convergent : **le conflit se règle à l'écriture, jamais silencieusement au runtime**.

## Couches (de la plus forte à la plus faible précédence)

| Couche | Fichier | Portée | Chargement |
| --- | --- | --- | --- |
| `workspace` | [`workspace.md`](workspace.md) | Invariants et conventions valables partout | Au démarrage (toujours actif) |
| `project` | `projects/<projet>.md` | Un projet | Au démarrage, projet courant uniquement |
| `phase` | `phases/<phase>.md` | Une phase du workflow | À la demande, au déclenchement de la phase |
| `scope` | `scopes/<scope>.md` (`standard`, `feature`, `infra`, `security-patch`, `mvp`, `poc`, `express`, `enterprise`) | Un scope ([scopes et axes](../common/protocols/scopes-and-axes.md)) | À la demande, scope confirmé |

**Précédence** : `workspace` > `project` > `phase` > `scope`.

- Une règle ne peut pas contredire une règle d'une couche supérieure sans arbitrage humain (contrôle de conflit à l'admission).
- Aucune couche n'écrase une autre en silence au runtime.

> **Couche `stage` différée** : réévaluable si l'amont l'ouvre ou si un besoin réel émerge ([`decisions/0011`](../../decisions/0011-alignement-memoire-de-regles-sur-ai-dlc.md)). La granularité fine reste couverte par la couche `scope` et les fiches de stage.

## Cycle de vie d'une règle

1. **Capture** : toute correction, rejet ou reformulation humaine est un candidat-règle, tracé sur l'issue.
2. **Remontée** : au point de validation humaine, le coordinateur propose les candidats en règles courtes, avec couche et portée proposées.
3. **Confirmation humaine** : l'humain garde ✅ / rejette ❌ / reformule 💬 chaque candidat séparément. Rien n'est écrit sans validation explicite.
4. **Contrôle de conflit** : précédence des couches, invariants non contournables et, pour toute règle `workspace`, contrôle sécurité systématique de l'Architecte cybersécurité.
5. **Écriture** : ajout au fichier de la couche, avec identifiant, date et lien vers l'issue d'origine.
6. **Application** : au démarrage du **prochain** workflow ; jamais dans l'exécution en cours.

## Format d'une règle

Entrée de liste avec identifiant stable `RULE-<COUCHE>-NNN` :

```md
- **RULE-WS-001** — Toute modification d'architecture passe par l'Architecte cybersécurité avant validation humaine.
  - _portée_ : workspace · _origine_ : ALI-000 · _ajoutée le_ : AAAA-MM-JJ
```

**Rubriques topicales** (convention amont) :

- Les règles se rangent sous des rubriques en prose, créées au besoin : `## Manière de travailler`, `## Posture de vérification`, `## Déploiement`, `## Style / conventions`, `## Sécurité`…
- Une règle = une puce sous la rubrique idoine.
- Obligatoires : identifiant `RULE-*`, portée, origine, date (traçabilité, SEC-5).
- Gabarits : [`projects/_template.md`](projects/_template.md), [`scopes/_template.md`](scopes/_template.md).

## Invariants non contournables

Aucune règle apprise, à aucune couche, ne peut affaiblir :

- la **validation humaine granulaire** ;
- l'**ADR** sur chaque décision structurante ;
- la **piste d'audit** sur l'issue ;
- le **contrôle sécurité minimal** (OWASP / STRIDE) ;
- les **garde-fous sécurité des scopes** (plancher de vérification, Depth non abaissable sur `security-patch` / `enterprise`, re-scoping tracé).

Un candidat qui contredit l'un d'eux est **rejeté d'office**.

## Clauses de sécurité (contrôle Architecte cybersécurité)

Clauses **contraignantes**, issues du contrôle sécurité du mécanisme (STRIDE / OWASP) :

- **SEC-1 — érosion sémantique** : un candidat qui restreint la portée, ajoute une exception ou conditionne un invariant / garde-fou est **rejeté d'office**, même sans contradiction littérale. L'idempotence n'exonère jamais de ce contrôle.
- **SEC-2 — périmètre fondé sur le risque** : contrôle sécurité systématique sur toute règle `workspace` **et** sur toute règle `project` / `phase` / `scope` visant un scope à garde-fous (`security-patch`, `enterprise`), une phase de vérification ou un contrôle de sécurité existant.
- **SEC-3 — pas d'exploitation dans le run courant** : un candidat n'a aucune valeur normative avant confirmation, contrôle et écriture ; application au prochain workflow.
- **SEC-4 — promotion vers `workspace`** : contrôle sécurité systématique, qu'elle « touche la sécurité » ou non.
- **SEC-5 — intégrité du canal d'écriture** :
  - Aucune modification de `core/rules/` hors de la boucle (capture → confirmation humaine → contrôle de conflit).
  - Toute modification est versionnée, revue en PR, avec `origine` + date.
  - Entrée sans provenance traçable = invalide, retirée.
