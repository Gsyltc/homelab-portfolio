# Protocole — format de retour vers l'humain (Homelab)

**Source unique** du format des commentaires **destinés à l'humain** du workflow `homelab` : proposition initiale, demande de paramètres, présentation de gate, arbitrage, clôture. Il est l'équivalent Homelab du protocole [`core/common/protocols/output-format.md`](../../../core/common/protocols/output-format.md), adapté au Homelab : pré-sélections, FQDN, Vault, NFS, Traefik, sensors et gates de phase.

Ce protocole fixe la **forme** (structure, concision, proposition par défaut). Il ne change **ni** la boucle Keep / Modify / Redo ([`conductor.md`](../conductor.md)), **ni** la mention humaine et la gate ([`governance-security.md`](governance-security.md) § « Règle A2A »), **ni** la clôture de la boucle A2A ([`stage-protocol.md`](stage-protocol.md)).

> **Le destinataire fixe la forme.**
> - **Destinataire = l'humain** : ce protocole (prose réduite, sections fixes, une proposition par défaut par question).
> - **Destinataire = un agent** : YAML joint (message A2A) et commentaire réduit à la mention active et au nom du fichier. Voir [`producer-report.md`](producer-report.md) et [`report-format.md`](report-format.md). Aucune des sections ci-dessous n'y figure.
>
> Seul le Tech Lead Homelab s'adresse à l'humain. Un spécialiste ou un reviewer ne rédige jamais ce format.

## 1. Prose réduite

- Phrases courtes, une idée par puce. Aucune reformulation de ce que l'issue ou le livrable contient déjà.
- Rien d'implicite : chaque question, risque ou action reste compréhensible seul. La concision ne justifie jamais d'omettre un écart, une source ou une condition de levée d'un blocage.
- Les valeurs sont écrites en clair (FQDN complet, chemin, nom de clé Vault), jamais sous forme de gabarit (`<stack>.<domaine>`).
- Tableaux seulement pour une comparaison réelle. Cellules télégraphiques.
- Aucun secret, aucune valeur Vault, jamais `${SNI}`.

## 2. Structure : quatre sections, dans cet ordre

### `## Résumé`

Toujours présente. Une puce par résultat : quoi + où (artefact, chemin en code inline, décision tracée). Aucun récit du déroulé. Elle rappelle en une ligne le **service** (stack), la **phase** courante et le **gate** attendu.

### `## Sensors`

Présente seulement si le stage ou le gate déclare au moins un sensor. Une puce par sensor, sans phrase :

```markdown
- `<sensor-id>` (`fire_on: write|gate`) — <artefact> : ✅ conforme | ⚠️ écart — <une ligne> | ⛔ indisponible — <motif du script>
```

Aucun sensor déclaré n'est omis (SG-2). `⛔ indisponible` n'est jamais lu comme conforme. La section est advisory : elle ne vaut pas validation.

### `## Points bloquants`

Présente seulement s'il en existe. Une puce par point, avec son renvoi vers la décision correspondante. Sinon, la section est omise (ne pas écrire « aucun »).

### `## Décisions à prendre`

Présente si et seulement si l'**humain** doit intervenir. Elle contient **une fiche par question**, numérotée, avec ces champs dans cet ordre :

```markdown
### D<n>. <intitulé court de la question>
- **Contexte** : <pourquoi la question se pose, source : doc officielle, règle, rapport QA>
- **Proposition par défaut** : ✅ <valeur ou choix concret> — <justification en une ligne>
- **Alternatives** : <option B> ; <option C> (<compromis en une ligne chacune>)
- **Impact** : <ce qui change selon le choix : fichiers, clés Vault, actions humaines>
- **Réponse attendue** : Keep | Modify (<valeur>) | Redo
```

Règles :
- **Chaque question porte une proposition par défaut**, formulée comme une valeur concrète et prête à être retenue. Répondre « Keep » suffit à la valider.
- **Pas de proposition possible** (information que seul l'humain détient, ex. nom d'un groupe, choix de goût) : écrire `**Proposition par défaut** : aucune — <motif>` et lister les options. Ne jamais inventer une valeur.
- **Une valeur manquante bloque la question qui en dépend** : la question est posée avec cette valeur (`**À fournir** : <valeur attendue>` dans la fiche), jamais validée sans elle (ex. un scope `groups` ne se valide pas sans le nom du mapping). Voir [`conductor.md`](../conductor.md), « Élément dépendant d'une valeur manquante ».
- Les questions sont regroupées en **un seul message par gate**. Toute valeur manquante connue au moment du gate y figure. Pas de questions posées au fil de l'eau.
- Les décisions sont indépendantes les unes des autres. L'humain répond par élément (`D1 Keep, D2 Modify : …`).
- **Livrables à relire** : si le gate porte sur des fichiers, ajouter avant les décisions `### Livrables à relire`, une puce par fichier (chemin en code inline, sous `.a-valider/<id-tâche>/<stack>/` avant dépôt).
- **Mention humaine** : le message se clôt par `[@Nom](mention://member/<user_id>)` suivi de l'action attendue. L'UUID vient de `multica workspace member list --output json`, jamais deviné. Aucune mention humaine hors d'une action réellement attendue.
- Gate `light`, `granular` ou `explicit` : indiquer laquelle et ce qui avance après la réponse. Sur blocage : mention humaine et issue `blocked`.

## 3. Gabarit de la proposition initiale (phase Idéation, gate léger)

Les sept points de [`intent-scope-approval`](../stages/ideation/intent-scope-approval.md) suivent le format des fiches ci-dessus. Pour chacun, la proposition par défaut est le résultat de la pré-sélection (cible, FQDN, auth, base, réseau). Quand une pré-sélection retient une seule option, elle est la proposition par défaut. Quand elle en laisse deux, le Tech Lead désigne l'option recommandée et la justifie, l'autre devient l'alternative.

## 4. Gabarit de la demande de paramètres (phase Cadrage, gate granulaire)

Les blocs de [`required-parameters-collection`](../stages/cadrage/required-parameters-collection.md) (OIDC, stockage, Valkey, clés Vault, mode d'exécution) sont des questions D<n> avec la valeur déduite comme proposition par défaut et sa source. Les clés Vault sont listées par nom seulement, avec leur `besoin`. Les actions humaines hors workflow (création des clés, secrets, dossiers NFS) sont rappelées en fin de message.

## 5. Ce que ce protocole ne change pas

- Validation humaine granulaire, Keep / Modify / Redo, gates de phase, contrôle sécurité, mention humaine sur blocage.
- Clôture A2A : un commentaire destiné à l'humain se termine par la mention de l'humain ; un handoff agent se termine par la mention de l'agent.
- Langue : français.
