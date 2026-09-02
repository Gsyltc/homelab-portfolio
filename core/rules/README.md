# Règles persistantes — mémoire du workflow

Ce répertoire contient la **mémoire de règles multi-couches** alimentée par la **boucle d'apprentissage** décrite dans la section « Règles & boucle d'apprentissage » de [`docs/core-workflow.md`](../../docs/core-workflow.md). Décision structurante tracée dans [ADR-0004](../../decisions/0004-boucle-apprentissage-et-regles-persistantes.md).

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
- l'**ADR** sur chaque décision structurante ;
- la **piste d'audit** sur l'issue ;
- le **contrôle sécurité minimal** (OWASP / STRIDE) ;
- les **garde-fous sécurité des scopes** (plancher de vérification, Depth non abaissable sur `security-patch` / `enterprise`, re-scoping tracé — voir « Scopes et axes d'exécution »).

Un candidat qui contredit l'un de ces invariants est **rejeté d'office**.
