# Protocole — format de retour d'un agent (prose réduite, 3 sections)

**Source unique** du format des **retours d'agent** du workflow `core` : comment un agent rédige son **compte rendu** et son **commentaire de retour A2A** sur l'issue. Ce protocole fixe la **forme** (concision + structure) ; il ne redéfinit **ni** les mécanismes de clôture de la boucle A2A — statut d'issue, lien de mention actif, `trigger_outcomes`, anti-wake parasite — qui ont leur source unique dans la « Checklist de sortie de stage » de [`stage-protocol.md`](stage-protocol.md) et la « Règle A2A » de [`governance-security.md`](governance-security.md), **ni** les invariants de gouvernance et de gating, dont la source unique reste [`governance-security.md`](governance-security.md) et [`conductor.md`](../conductor.md).

> **Qui est concerné.** **Tout agent** du workflow `core` qui poste un compte rendu ou un retour sur l'issue : coordinateur, architectes et experts (production), experts de méthodologie, Experte d'archivage, Agent de notifications. Les **reviewers** (cohérence, sécurité) appliquent déjà cette discipline via [`reviewer.md`](reviewer.md), § « Forme de la revue — prose réduite » : le présent protocole **généralise cette même exigence** à l'ensemble des agents, sans la dupliquer — la forme de la revue reste décrite dans `reviewer.md`, qui s'y réfère.

## 1. Prose réduite (obligatoire, tout retour)

- **Phrases courtes, une idée par puce, aucun remplissage** ni reformulation de ce qui est déjà tracé sur l'issue ou dans le livrable.
- **Réduction sans perte de contexte** : chaque écart, décision, risque ou action reste **intégralement compréhensible et actionnable de façon autonome** par le destinataire, sans reconstituer l'implicite. La concision ne justifie **jamais** d'omettre un écart, une référence de norme (OWASP / STRIDE…), une décision structurante ou une condition de levée d'un blocage.
- **Tableaux réduits au maximum** : un tableau n'est conservé que pour une structure réellement comparative ; sinon, préférer une liste à puces. Les tableaux retenus gardent le **minimum de colonnes** utiles, des **cellules télégraphiques** (pas de phrases), aucune colonne redondante avec le texte voisin.
- Objectif : un retour **dense et sans ambiguïté**.

## 2. Structure en 3 sections (obligatoire, tout retour)

Tout compte rendu / retour d'agent se structure en **trois sections markdown**, dans cet ordre. Les sections **1** et **3** suivent des règles d'apparition ; la section **1** est **toujours** présente.

### `## Résumé`

Synthèse **concise** des tâches effectuées, en **puces**. Une puce = un résultat ou un livrable, formulé en clair (quoi + où : artefact `produces`, décision tracée, chemin du fichier en code inline). Aucun récit du déroulé, aucune reprise de la piste d'audit déjà posée.

### `## Points bloquants`

**N'apparaît que s'il existe des points bloquants.** Chaque point en **puce** : l'objet du blocage, bref et autonome. Un point bloquant qui **requiert une décision ou une action humaine** (halt / gate) est **développé** dans la section 3 — ici, il est seulement listé et renvoyé à la section 3. **En l'absence de point bloquant, omettre entièrement cette section** (ne pas écrire « aucun »).

### `## Action humaine requise`

**Conditionnelle, et biconditionnelle — elle apparaît SI ET SEULEMENT SI une action humaine est effectivement nécessaire, et alors TOUJOURS avec un lien de mention actif de l'humain.** Deux déclencheurs, l'un suffit :

- un **point bloquant** (de la section 2) qui **requiert un arbitrage humain** pour être levé (halt-and-ask) ; **et / ou**
- un **gate de validation humaine** à franchir pour continuer le workflow.

> ⛔ **Un retour A2A n'est PAS une action humaine requise.** Rendre la main à un **agent** (retour de délégation vers le coordinateur, retour d'un reviewer vers le spécialiste, passation entre agents) est un échange **agent ↔ agent** : il **n'appelle aucune** section « Action humaine requise » et **aucune** mention de l'humain. N'inscris cette section **que** lorsque c'est bien l'**humain** — et pas un agent — qui doit intervenir. Mettre « Action humaine requise » alors que la main revient à un agent est un **écart de gouvernance** (il sollicite l'humain à tort et déclenche une notification injustifiée). Cas typique : un spécialiste qui termine son livrable **rend la main au coordinateur par retour A2A** (clôture par le lien `mention://agent/<uuid>`, **sans** cette section) ; c'est **ensuite le coordinateur**, porteur de la validation humaine granulaire, qui pose la section « Action humaine requise » **avec** la mention humaine s'il faut faire trancher l'humain.

**Mention humaine obligatoire dans la section (non contournable).** Dès que cette section apparaît, elle **doit** porter un **lien de mention actif de l'humain demandeur** `[@Nom](mention://member/<user_id>)` (UUID résolu via `multica workspace member list --output json`, jamais deviné ni remplacé par un placeholder comme `@<humain>`). Une section « Action humaine requise » **sans** mention active de l'humain ne satisfait **pas** l'invariant 6 de [`governance-security.md`](governance-security.md) (« Mention humaine obligatoire dès qu'une action humaine est requise ») et déclenche aussi l'invariant 7 (notification). Réciproquement, **aucune** mention de l'humain hors d'une action humaine réellement attendue.

Sans point bloquant à arbitrer **ni** gate à franchir — et **a fortiori sur un simple retour A2A** —, **omettre entièrement cette section** (ne rien écrire de superflu, ne mentionner aucun humain). Cette section **n'affaiblit aucune norme de gating** : elle en est la **mise en forme**, pas une dérogation. Pour **chaque** action requise, détailler :

- **Problème** — ce qui bloque ou ce qui doit être tranché.
- **Cause** — l'origine factuelle.
- **Solutions possibles + recommandation** — les options, et **ta recommandation** explicitement désignée parmi elles.
- **Mention humaine active + Gate / norme applicable** — le lien `[@Nom](mention://member/<user_id>)` de l'humain à solliciter, le gate concerné (`light` / `granular` / `explicit`) et le rappel que l'avancée reste conditionnée à l'arbitrage humain ; sur blocage, la **mention humaine obligatoire** et le passage en `blocked` s'appliquent (source unique : [`governance-security.md`](governance-security.md) et la « Checklist de sortie de stage » / « Halt-and-ask » de [`stage-protocol.md`](stage-protocol.md)).

## 3. Ce que ce protocole ne change pas (garde-fous)

- **Normes de gating préservées** — validation humaine granulaire, boucle Keep / Modify / Redo, gates de phase, contrôle sécurité systématique, mention humaine obligatoire sur blocage : **inchangés**. La section 3 ci-dessus **présente** l'action attendue ; elle ne remplace ni ne relâche aucun gate (invariants : [`conductor.md`](../conductor.md), [`governance-security.md`](governance-security.md)).
- **Clôture de la boucle A2A inchangée** — le commentaire de retour se termine toujours par le lien de mention actif prescrit (source unique : « Checklist de sortie de stage » de [`stage-protocol.md`](stage-protocol.md)). Le format en 3 sections est le **corps** de ce commentaire ; le lien de retour en reste la **clôture**.
- **Langue** — français par défaut (humain), termes OpenSpec / EARS en anglais si activés (source unique : [`conductor.md`](../conductor.md), « OBLIGATOIRE : langue et format »).
