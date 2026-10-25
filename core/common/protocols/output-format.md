# Protocole — format de retour d'un agent (prose réduite, 4 sections)

**Source unique** du format des **retours d'agent** du workflow `core` : comment un agent rédige son **compte rendu** et son **commentaire de retour A2A** sur l'issue. Ce protocole fixe la **forme** (concision + structure) ; il ne redéfinit **ni** les mécanismes de clôture de la boucle A2A — statut d'issue, lien de mention actif, `trigger_outcomes`, anti-wake parasite — qui ont leur source unique dans la « Checklist de sortie de stage » de [`stage-protocol.md`](stage-protocol.md) et la « Règle A2A » de [`governance-security.md`](governance-security.md), **ni** les invariants de gouvernance et de gating, dont la source unique reste [`governance-security.md`](governance-security.md) et [`conductor.md`](../conductor.md).

> **Qui est concerné.** **Tout agent** du workflow `core` qui poste un compte rendu ou un retour sur l'issue : coordinateur, architectes et experts (production), experts de méthodologie, Experte d'archivage, Agent de notifications. Les **reviewers** (cohérence, sécurité) appliquent déjà cette discipline via [`reviewer.md`](reviewer.md), § « Forme de la revue — prose réduite » : le présent protocole **généralise cette même exigence** à l'ensemble des agents, sans la dupliquer — la forme de la revue reste décrite dans `reviewer.md`, qui s'y réfère.

## 1. Prose réduite (obligatoire, tout retour)

- **Phrases courtes, une idée par puce, aucun remplissage** ni reformulation de ce qui est déjà tracé sur l'issue ou dans le livrable.
- **Réduction sans perte de contexte** : chaque écart, décision, risque ou action reste **intégralement compréhensible et actionnable de façon autonome** par le destinataire, sans reconstituer l'implicite. La concision ne justifie **jamais** d'omettre un écart, une référence de norme (OWASP / STRIDE…), une décision structurante ou une condition de levée d'un blocage.
- **Tableaux réduits au maximum** : un tableau n'est conservé que pour une structure réellement comparative ; sinon, préférer une liste à puces. Les tableaux retenus gardent le **minimum de colonnes** utiles, des **cellules télégraphiques** (pas de phrases), aucune colonne redondante avec le texte voisin.
- Objectif : un retour **dense et sans ambiguïté**.

## 2. Structure en 4 sections (obligatoire, tout retour)

Tout compte rendu / retour d'agent se structure en **quatre sections markdown**, dans cet ordre. Les sections **2**, **3** et **4** suivent des règles d'apparition ; la section **1** est **toujours** présente.

### `## Résumé`

Synthèse **concise** des tâches effectuées, en **puces**. Une puce = un résultat ou un livrable, formulé en clair (quoi + où : artefact `produces`, décision tracée, chemin du fichier en code inline). Aucun récit du déroulé, aucune reprise de la piste d'audit déjà posée.

### `## Sensors`

**N'apparaît que si le stage déclare au moins un sensor** (`sensors:` non vide dans la fiche de stage). Aucune prose — **liste à puces uniquement**, une puce par sensor invoqué :

```markdown
## Sensors

- `<sensor-id>` (`fire_on: write|gate`) — <artefact concerné> : ✅ conforme | ⚠️ écart mineur — <une ligne> | ⛔ indisponible — <motif>
```

Règles :
- **Chaque sensor déclaré figure dans la liste** — aucune omission (SG-2 : silence = écart).
- **Pas de phrase, pas de tableau** — verdict + une ligne factuelle suffisent.
- **`⛔ indisponible`** quand le sensor n'est pas encore exécutable (mécanisme déclaratif) : indiquer le motif en une ligne, **jamais omettre l'entrée**.
- La section est **advisory** — ne vaut pas validation, n'autorise aucun raccourci (SG-1..6).
- **En l'absence de sensor déclaré, omettre entièrement cette section.**

### `## Points bloquants`

**N'apparaît que s'il existe des points bloquants.** Chaque point en **puce** : l'objet du blocage, bref et autonome. Un point bloquant qui **requiert une décision ou une action humaine** (halt / gate) est **développé** dans la section 3 — ici, il est seulement listé et renvoyé à la section 3. **En l'absence de point bloquant, omettre entièrement cette section** (ne pas écrire « aucun »).

### `## Action humaine requise`

**Biconditionnelle** : présente **si et seulement si** l'**humain** (pas un agent) doit intervenir, et alors **toujours** avec lien de mention actif de l'humain.

- **Déclencheurs** (l'un suffit) : point bloquant (section 2) requérant un arbitrage humain (halt-and-ask) ; **et / ou** gate de validation humaine à franchir.
- **Pas sur un retour A2A** : rendre la main à un **agent** (délégation → coordinateur, reviewer → spécialiste, passation) est un échange agent ↔ agent — **ni** cette section **ni** mention humaine ; l'y mettre est un écart de gouvernance (sollicitation + notification injustifiées). Cas type : un spécialiste clôt par le lien `mention://agent/<uuid>` **sans** cette section ; c'est **ensuite le coordinateur** qui la pose si l'humain doit trancher.
- **Mention humaine obligatoire** (non contournable) : lien actif `[@Nom](mention://member/<user_id>)` (UUID via `multica workspace member list --output json`, jamais deviné ni placeholder type `@<humain>`). Sans elle, invariant 6 de [`governance-security.md`](governance-security.md) non satisfait (+ déclenche l'invariant 7, notification). Réciproquement, **aucune** mention humaine hors action réellement attendue.
- **Sinon, omettre entièrement** la section (ni prose superflue, ni mention). Elle **met en forme** l'arbitrage, ne relâche **aucune** norme de gating.
- **Liste des fichiers modifiés obligatoire** : d'abord `### Liste des fichiers modifiés`, une **puce par fichier** créé / modifié / supprimé, chemin en code inline (`chemin/vers/fichier.ext`) ; une seule puce « Aucun fichier modifié » si rien. Puis `### Décision à prendre` (arbitrage + lien de mention actif).

Forme attendue :

```markdown
## Action humaine requise

### Liste des fichiers modifiés
- `chemin/vers/fichier-1.ext`
- `chemin/vers/fichier-2.ext`

### Décision à prendre
[@Nom](mention://member/<user_id>) <description des décisions à prendre, une par point si plusieurs>
```

Sous `### Décision à prendre`, pour **chaque** action : **Problème** (ce qui bloque / à trancher) · **Cause** (origine factuelle) · **Solutions + recommandation** (options, ta reco désignée) · **Mention humaine active + gate** (lien `[@Nom](mention://member/<user_id>)`, gate `light` / `granular` / `explicit`, avancée conditionnée à l'arbitrage ; sur blocage, mention humaine + passage en `blocked` — source unique [`governance-security.md`](governance-security.md) et « Checklist de sortie de stage » / « Halt-and-ask » de [`stage-protocol.md`](stage-protocol.md)).

## 3. Ce que ce protocole ne change pas (garde-fous)

- **Normes de gating préservées** — validation humaine granulaire, boucle Keep / Modify / Redo, gates de phase, contrôle sécurité systématique, mention humaine obligatoire sur blocage : **inchangés**. La section 3 ci-dessus **présente** l'action attendue ; elle ne remplace ni ne relâche aucun gate (invariants : [`conductor.md`](../conductor.md), [`governance-security.md`](governance-security.md)).
- **Clôture de la boucle A2A inchangée** — le commentaire de retour se termine toujours par le lien de mention actif prescrit (source unique : « Checklist de sortie de stage » de [`stage-protocol.md`](stage-protocol.md)). Le format en 4 sections est le **corps** de ce commentaire ; le lien de retour en reste la **clôture**.
- **Langue** — français par défaut (humain), termes OpenSpec / EARS en anglais si activés (source unique : [`conductor.md`](../conductor.md), « OBLIGATOIRE : langue et format »).
