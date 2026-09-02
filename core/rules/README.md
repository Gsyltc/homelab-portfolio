# Règles persistantes — mémoire du workflow

Ce répertoire contient la **mémoire de règles multi-couches** alimentée par la **boucle d'apprentissage** décrite dans [`core/common/protocols/governance-security.md`](../common/protocols/governance-security.md) (source unique du workflow depuis le Stage 7 ; l'ancien `docs/core-workflow.md` est désormais un stub de redirection). Ce mécanisme fait l'objet d'une décision structurante dédiée.

Les règles capitalisent les **corrections humaines validées** afin qu'un agent ne répète pas la même erreur d'un projet à l'autre. Elles sont des **fichiers Markdown versionnés**, lisibles au démarrage de chaque workflow (chargement paresseux — voir plus bas).

## Couches (de la plus forte à la plus faible précédence)

| Couche | Fichier | Portée | Chargement |
| --- | --- | --- | --- |
| `workspace` | [`workspace.md`](workspace.md) | Invariants et conventions valables partout | Au démarrage (toujours actif) |
| `project` | `projects/<projet>.md` | Spécifique à un projet | Au démarrage, uniquement le projet courant |
| `phase` | `phases/<phase>.md` (`inception`, `construction`, `operation`) | Par phase du workflow | À la demande, quand la phase est déclenchée |
| `scope` | `scopes/<scope>.md` (`standard`, `feature`, `infra`, `security-patch`, `mvp`, `poc`, `express`, `enterprise`) | Par scope (voir « Scopes et axes d'exécution ») | À la demande, quand le scope est confirmé |

**Précédence** : `workspace` > `project` > `phase` > `scope`. Une règle d'une couche **ne peut pas contredire** une règle d'une couche supérieure sans arbitrage humain (contrôle de conflit à l'admission — voir le workflow).

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

## Invariants non contournables

Aucune règle apprise, à aucune couche, ne peut affaiblir :

- la **validation humaine granulaire** ;
- la **traçabilité** de chaque décision structurante ;
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
