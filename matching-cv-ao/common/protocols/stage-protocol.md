# Protocole — exécution générique d'un stage

Cycle standard qu'un stage suit, quel que soit sa phase. Il ne se substitue jamais aux instructions propres de la fiche de stage ; il en fixe l'ossature commune, adaptée au moteur A2A Multica (mentions UUID, statut d'issue, piste d'audit sur l'issue).

## Cycle en 6 temps

```mermaid
flowchart LR
    E[1 Entree] --> D[2 Delegation A2A]
    D --> P[3 Production]
    P --> S[4 Sensors a l ecriture]
    S --> G[5 Verification gate a la frontiere]
    G --> V[6 Validation humaine granulaire]
    V -.->|Redo / Modify| P
```

### 1. Entrée — pré-requis et contexte
- Vérifier que les `requires_stage` sont satisfaits et que les artefacts `consumes` (marqués `required: true`) existent. Sinon : **halt-and-ask** (ne jamais deviner).
- Charger, **à la demande**, uniquement le contexte nécessaire au stage.

### 2. Délégation A2A (si `mode: subagent`)
- Le coordinateur poste un commentaire sur l'issue avec une **mention valide** `[@Label](mention://agent/<uuid>)` et une **mission claire** : objectif, périmètre, critères d'acceptation.
- **Ne jamais deviner un UUID** : le résoudre via `multica agent list --output json` (champ `id`). Vérifier `trigger_outcomes` après chaque mention.
- Si `mode: inline`, le coordinateur exécute directement.
- Si `for_each` est déclaré, le cycle 3→6 s'exécute **une fois par instance** de l'artefact nommé.

### 3. Production
- La fonction `lead_agent` produit les artefacts `produces`, dans la langue de l'humain.
- **Agent ↔ Agent** : JSON uniquement. **Agent ↔ Humain** : Markdown uniquement.
- Chaque décision structurante est tracée sur l'issue.
- L'agent trace son avancement sur l'issue (piste d'audit au fil de l'eau).

> ⛔ **UN STAGE DÉLÉGUÉ N'EST JAMAIS TERMINÉ SANS LIEN DE RETOUR ACTIF.** Produire le livrable
> ne suffit pas : tant que le lien de mention actif vers l'assigneur n'est pas posé ET que ses
> `trigger_outcomes` ne sont pas vérifiés, la tâche est **incomplète** et la chaîne A2A reste
> bloquée (incident EXPE-58 : un « à toi pour la suite » en texte clair n'a réveillé personne).

- **Retour de délégation (obligatoire, à la charge de l'agent délégataire)** : en fin de production, l'agent lead **construit lui-même** le lien de mention actif `[@Assigneur](mention://agent/<uuid-assigneur>)` vers **l'agent qui l'a délégué** dans son commentaire de livrable — UUID **résolu à chaque fois** via `multica agent list --output json` (à partir du **nom** de l'assigneur donné en texte clair dans la mission), **jamais copié depuis la consigne de délégation ni codé en dur**. C'est **ce lien, posé par l'agent qui termine, qui enqueue le run de reprise de l'assigneur**. Une mention en texte clair ou une simple réponse dans le fil **n'enqueue aucun run** et ne réveille pas l'assigneur. Réciproquement, **aucun agent ne se mentionne lui-même** avec un lien actif dans sa propre consigne de délégation (règle générale — voir `governance-security` « Règle A2A ») : il désigne l'agent de retour **par son nom**, en texte clair.
- **Vérification `trigger_outcomes`** : après le post, l'agent lead vérifie les `trigger_outcomes` de son commentaire (statuts `blocked` / `coalesced` / `deferred`). Si la mention n'a pas déclenché le run attendu, il le signale sur l'issue (halt-and-ask) plutôt que de considérer la tâche terminée.

### 4. Sensors à l'écriture
- À l'écriture d'un artefact, les `sensors` déclarés se déclenchent et leur verdict est consigné en commentaire. **Advisory** — n'autorise aucun raccourci.

### 5. Verification gate à la frontière de phase
- À la sortie de la phase, le coordinateur exécute le gate de traçabilité et poste le **« Rapport de vérification »** *avant* la validation humaine. Un écart est signalé, jamais bloquant.

### 6. Validation humaine granulaire
- Selon `human_gate` : `none` (aucune — Initialisation), `light` (approbation extraction — Analyse), `granular` (choix par choix — Validation), `explicit` (validation explicite — Clôture).
- Boucle **Keep / Modify / Redo** par élément (voir `conductor.md`). Sur `Modify` / `Redo`, retour au temps 3 pour l'élément concerné uniquement.

## Contrôle — non contournable
Le coordinateur valide chaque livrable avant validation humaine. La grille d'évaluation ne sera **jamais inventée** — elle sera demandée à l'humain si absente.

## Checklist de sortie de stage (`mode: subagent`) — non contournable
Un stage délégué (`mode: subagent`) n'est considéré **terminé** QUE lorsque les trois cases sont cochées, **dans cet ordre** :

1. ☑ **Livrable produit et vérifié** — artefacts `produces` écrits sous `${ROOT_DIRECTORY}` absolu, contrôle du livrable (Step « Contrôle ») passé, piste d'audit posée sur l'issue.
2. ☑ **Lien de retour ACTIF posé** — le commentaire de livrable se termine par `[@<Nom assigneur>](mention://agent/<uuid>)`, UUID résolu via `multica agent list --output json` (jamais copié/codé en dur), jamais une auto-mention. C'est ce lien qui enqueue le run de reprise.
3. ☑ **`trigger_outcomes` vérifié** — la mention a bien déclenché le run attendu ; sinon (`blocked`/`coalesced`/`deferred`) → **halt-and-ask** sur l'issue, ne pas conclure.

Tant que 2 ou 3 manque, la tâche est **incomplète** : ne jamais rendre la main comme si le stage était clos.

## Halt-and-ask
Le cycle s'arrête et interroge l'humain dès : échec / impossibilité d'un livrable ; écart ou contrôle requis ; gate / sensor en écart ; décision structurante nouvelle non cadrée ; action à impact / destructive (jamais autonome).
