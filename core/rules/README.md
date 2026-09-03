# Règles persistantes — mémoire du workflow

Ce répertoire contient la **mémoire de règles multi-couches** alimentée par la **boucle d'apprentissage** décrite dans [`core/common/protocols/governance-security.md`](../common/protocols/governance-security.md)
Les règles capitalisent les **corrections humaines validées** afin qu'un agent ne répète pas la même erreur d'un projet à l'autre. Elles sont des **fichiers Markdown versionnés**, lisibles au démarrage de chaque workflow (chargement paresseux — voir plus bas).

## Alignement AI-DLC (« Rules and the Learning Loop »)

Cette mémoire de règles est alignée sur le contrat AI-DLC **« Rules and the Learning Loop »** (*Harness Engineer Guide*), avec des **divergences assumées et tracées** dans [`decisions/0011`](../../decisions/0011-alignement-memoire-de-regles-sur-ai-dlc.md) (voir aussi [`decisions/0004`](../../decisions/0004-boucle-apprentissage-et-regles-persistantes.md)) :

- **Chaîne à 5 couches amont `org → team → project → phase → stage`** → ici **4 couches** `workspace > project > phase > scope` :
  - `org` + `team` sont **fusionnés dans `workspace`** (le workspace Multica *est* l'organisation et l'équipe — pas de frontière distincte à modéliser).
  - La couche **`stage`** amont (`aidlc-stage-<slug>.md`) est **réservée pour une future version** chez l'amont (non écrivable) : nous **restons alignés** et **ne la créons pas** (différée).
  - La couche **`scope`** est une **couche maison** (pont avec le mécanisme de scopes, [`decisions/0003`](../../decisions/0003-scopes-et-axes-depth-verification.md)) absente d'AI-DLC — conservée et documentée.
- **Emplacement** : l'amont place les règles sous `core/memory/` ; nous conservons **`core/rules/`** (cohérent avec `core/sensors/` / `core/common/`, agnostique de méthodologie). La **portée reste dérivable du chemin** (répertoire + nom de fichier), dans l'esprit amont « pas de champ `scope:` ».
- **Phases** : comme l'amont, la couche `phase` a **quatre fichiers** (`ideation`, `inception`, `construction`, `operation`) ; l'`initialization` est bootstrap-only et **ne porte pas** de fichier de règles.
- **Précédence explicite vs strict-additif** : l'amont est *strict-additif* (toutes les règles coexistent, rien n'écrase au runtime, conflit réglé **à l'admission**). Nous énonçons en plus une **précédence de couches** *et* appliquons le **contrôle de conflit à l'admission** : les deux modèles convergent — **le conflit se règle à l'écriture, jamais silencieusement au runtime** — et notre précédence explicite est un **sur-ensemble conservateur** du strict-additif.

## Couches (de la plus forte à la plus faible précédence)

| Couche | Fichier | Portée | Chargement | Correspondance AI-DLC |
| --- | --- | --- | --- | --- |
| `workspace` | [`workspace.md`](workspace.md) | Invariants et conventions valables partout | Au démarrage (toujours actif) | `org` + `team` fusionnés |
| `project` | `projects/<projet>.md` | Spécifique à un projet | Au démarrage, uniquement le projet courant | `project` |
| `phase` | `phases/<phase>.md` (`ideation`, `inception`, `construction`, `operation`) | Par phase du workflow | À la demande, quand la phase est déclenchée | `phase` (4 fichiers ; `initialization` sans règles) |
| `scope` | `scopes/<scope>.md` (`standard`, `feature`, `infra`, `security-patch`, `mvp`, `poc`, `express`, `enterprise`) | Par scope (voir « Scopes et axes d'exécution ») | À la demande, quand le scope est confirmé | couche maison (absente d'AI-DLC) |

> **Couche `stage` différée** : AI-DLC réserve une cinquième couche « règles par stage » pour une version future (non écrivable aujourd'hui). Nous restons alignés en ne la créant pas ; la granularité fine reste couverte par la couche `scope` et par les fiches de stage (comportement). Réévaluable si l'amont ouvre la couche `stage` ou si un besoin réel émerge ([`decisions/0011`](../../decisions/0011-alignement-memoire-de-regles-sur-ai-dlc.md)).

**Précédence** : `workspace` > `project` > `phase` > `scope`. Une règle d'une couche **ne peut pas contredire** une règle d'une couche supérieure sans arbitrage humain (contrôle de conflit à l'admission — voir le workflow). Cette précédence explicite **préserve et renforce** l'invariant amont « conflit réglé à l'écriture, jamais au runtime » (elle n'est pas une résolution silencieuse au runtime : aucune couche n'écrase une autre sans arbitrage).

## Cycle de vie d'une règle

1. **Capture** : pendant une étape, chaque correction / rejet / reformulation humaine sur un choix est un *candidat-règle* potentiel (tracé sur l'issue).
2. **Remontée** : au point de validation humaine, le coordinateur propose les candidats formulés en règles courtes, avec couche et portée proposées.
3. **Confirmation humaine** : l'humain garde ✅ / rejette ❌ / reformule 💬 chaque candidat séparément. Rien n'est écrit sans validation explicite.
4. **Contrôle de conflit à l'admission** : précédence des couches + invariants non contournables + (pour toute règle `workspace`) contrôle sécurité systématique de l'Architecte cybersécurité.
5. **Écriture** : la règle acceptée est ajoutée au fichier de sa couche, avec un identifiant, la date et le lien vers l'issue d'origine.
6. **Application au prochain workflow** : une règle nouvellement écrite n'altère jamais l'exécution en cours ; elle prend effet au démarrage du **prochain** workflow.

## Format d'une règle

Chaque règle est une entrée de liste avec un identifiant stable `RULE-<COUCHE>-NNN` :

```md
- **RULE-WS-001** — Toute modification d'architecture passe par l'Architecte cybersécurité avant validation humaine.
  - _portée_ : workspace · _origine_ : ALI-000 · _ajoutée le_ : AAAA-MM-JJ
```

**Rubriques topicales** (convention alignée sur AI-DLC) : dans un fichier de couche, les règles se rangent sous des **rubriques topicales** en prose — par ex. `## Manière de travailler`, `## Posture de vérification`, `## Déploiement`, `## Style / conventions`, `## Sécurité` — une règle = une puce sous la rubrique idoine. Les rubriques sont **indicatives** (à créer selon le besoin) ; l'identifiant `RULE-*`, la portée, l'origine et la date restent **obligatoires** (traçabilité, clause SEC-5). Voir les gabarits [`projects/_template.md`](projects/_template.md) et [`scopes/_template.md`](scopes/_template.md).

## Invariants non contournables

Aucune règle apprise, à aucune couche, ne peut affaiblir :

- la **validation humaine granulaire** ;
- l'**ADR** sur chaque décision structurante ;
- la **piste d'audit** sur l'issue ;
- le **contrôle sécurité minimal** (OWASP / STRIDE) ;
- les **garde-fous sécurité des scopes** (plancher de vérification, Depth non abaissable sur `security-patch` / `enterprise`, re-scoping tracé — voir « Scopes et axes d'exécution »).

Un candidat qui contredit l'un de ces invariants est **rejeté d'office**.

## Clauses de sécurité (contrôle Architecte cybersécurité)

Issues du contrôle sécurité du mécanisme (STRIDE / OWASP), ces clauses sont **contraignantes** et ferment les vecteurs de dérive de gouvernance :

- **SEC-1 — érosion sémantique** : un candidat qui restreint la portée, ajoute une exception ou conditionne l'application d'un invariant ou d'un garde-fou est traité comme un affaiblissement et **rejeté d'office**, même sans contradiction littérale. L'idempotence n'exonère jamais de ce contrôle.
- **SEC-2 — périmètre fondé sur le risque** : le contrôle sécurité systématique s'applique à toute règle `workspace` **et** à toute règle `project` / `phase` / `scope` visant un scope à garde-fous (`security-patch`, `enterprise`), une phase de vérification, ou un contrôle de sécurité existant.
- **SEC-3 — pas d'exploitation d'un candidat dans le run courant** : un candidat capturé n'a aucune valeur normative tant qu'il n'est pas confirmé, contrôlé et écrit ; il ne peut être appliqué ni invoqué dans le run courant. L'application reste différée au prochain workflow.
- **SEC-4 — promotion vers `workspace`** : toute promotion d'une couche inférieure vers `workspace` est soumise au contrôle sécurité systématique, qu'elle « touche la sécurité » ou non.
- **SEC-5 — intégrité du canal d'écriture** : aucune règle n'est ajoutée / modifiée / supprimée dans `core/rules/` hors de la boucle (capture → confirmation humaine → contrôle de conflit). Toute modification est versionnée, revue en PR, et porte `origine` + date ; une entrée sans provenance traçable est invalide et retirée.
