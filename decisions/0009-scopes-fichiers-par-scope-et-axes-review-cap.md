# Scopes : un fichier par scope + axe « vérification » mappé sur `review_cap`

---
auteurs: Mika (agent, sur validation humaine granulaire — multica.gaston)
accepté par : (en attente de validation humaine)
accepté le : (en attente)
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** tant que la validation humaine granulaire n'est pas obtenue. Passera à **Accepted** après validation humaine explicite (invariant : aucun ADR accepté sans validation humaine). Aucune modification de la posture de sécurité n'est actée ici : les garde-fous des scopes ([ADR-0003](0003-scopes-et-axes-depth-verification.md)) sont préservés à l'identique.

## Contexte

Le mécanisme de scopes a été formalisé en [ADR-0003](0003-scopes-et-axes-depth-verification.md) : 8 scopes (`standard` défaut, `feature`, `infra`, `security-patch`, `mvp`, `poc`, `express`, `enterprise`), deux axes indépendants (Depth / vérification), auto-détection par mots-clés, matrice stage × scope. À ce stade, cette identité vivait **en prose** dans un tableau partagé ([`core/common/protocols/scopes-and-axes.md`](../core/common/protocols/scopes-and-axes.md)) et les mots-clés d'auto-détection n'étaient **pas déclarés en données**.

Le Stage 3 de l'alignement AI-DLC (issue ALI-196, parente ALI-193) porte les scopes sur le contrat **« Scopes »** du *Harness Engineer Guide* (`awslabs/aidlc-workflows`, [chapitre Scopes](https://awslabs.github.io/aidlc-workflows/harness-engineering/04-scopes/)). Ce contrat pose deux principes :

1. **Un fichier par scope** — l'identité (`name`, `depth`, `keywords`, `description`, et selon pertinence `testStrategy` / `review_cap` / `skeleton`) vit dans `core/scopes/<name>.md`, à l'image de `core/sensors/`.
2. **Appartenance transposée** — quels stages tournent sous un scope se déclare sur le champ `scopes:` de chaque fiche de stage, pas dans le fichier de scope. Ce point était **déjà en place** dans le dépôt (les fiches de stage portent leur liste `scopes:`), y compris les 3 stages d'Initialization qui nomment tous les scopes.

Deux écarts assumés doivent être **tracés en décision** plutôt que corrigés aveuglément (cadrage [ADR-0001](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)) :

- **Axe « vérification » vs `testStrategy`** — AI-DLC porte un axe « test strategy » (volume de tests). Le workspace produit majoritairement de la **documentation d'architecture**, ce qui rend cet axe peu pertinent tel quel ([ADR-0003](0003-scopes-et-axes-depth-verification.md), arbitrage Q-E : axe « niveau de vérification des livrables »).
- **Tooling non applicable** — pas de compilation `scope-grid.json`, pas de moteur TypeScript ni de champs `runner` / `freeform_default` : l'exécution passe par **Multica**.

## Décision

**Adopter la forme déclarative « un fichier par scope » d'AI-DLC**, sans importer le tooling non applicable.

**FIC-001 — Un fichier de données par scope.** Créer [`core/scopes/<name>.md`](../core/scopes/) pour les 8 scopes existants, avec front-matter : `name` (= stem du fichier), `depth` (`minimal` / `standard` / `comprehensive`), `verification` (`advisory` / `standard` / `renforcé`, champ maison), `keywords` (déclencheurs FR / EN en liste plate), `description` (une ligne), et selon pertinence `review_cap` / `skeleton`. Le corps porte l'intention en prose. Ces fichiers deviennent la **source d'identité** des scopes.

**FIC-002 — Appartenance conservée sur les stages.** Aucun changement : le champ `scopes:` des fiches de stage reste la déclaration d'appartenance. Contrôle : les 3 stages d'Initialization (`directory-check`, `brownfield-greenfield-detection`, `audit-trail-init`) nomment bien les 8 scopes.

**FIC-003 — Tableau conservé comme vue lisible.** [`scopes-and-axes.md`](../core/common/protocols/scopes-and-axes.md) reste la vue lisible consolidée (table des scopes liée aux fichiers, axes, ordre de désambiguïsation, matrice stage × scope, garde-fous). Une note de préséance y précise qu'**en cas d'écart d'identité, le fichier `core/scopes/<name>.md` fait foi**.

**DIV-001 — Divergence « vérification » vs `testStrategy` (assumée et tracée).** Le champ maison **`verification`** remplace le `testStrategy` d'AI-DLC pour la documentation d'architecture, **avec repli sur une stratégie de tests dès qu'un livrable comporte du code ou de l'IaC** (reconduit de [ADR-0003](0003-scopes-et-axes-depth-verification.md), arbitrage Q-E). On ne réintroduit pas `testStrategy` : le sens AI-DLC est préservé par le repli code / IaC.

**MAP-001 — Mapping `verification` → `review_cap`.** Le champ `review_cap` du contrat AI-DLC (plafond de classe de revue) matérialise en **donnée conforme** l'allègement de contrôle des scopes à vérification allégée :

| `verification` (maison) | `review_cap` (AI-DLC) |
| --- | --- |
| `advisory` | `advisory` |
| `standard` | *(absent — pas d'abaissement)* |
| `renforcé` | *(absent — jamais abaissé)* |

Concrètement : `poc` (vérification `advisory`) et `express` (chemin court) portent `review_cap: advisory` ; les autres scopes n'en portent pas. Un `review_cap` **abaisse** la `review_class` d'un stage mais ne la **relève jamais** — cohérent avec le garde-fou sécurité (plancher non abaissable).

**GAR-001 — Garde-fous préservés.** Les invariants et garde-fous de [ADR-0003](0003-scopes-et-axes-depth-verification.md) (R1→R8) sont reconduits sans changement : plancher OWASP / STRIDE non désactivable, `depth` ≥ `standard` et `verification` ≥ `renforcé` sur `security-patch` / `enterprise`, aucun `review_cap` abaissant sur les scopes sécuritaires, auto-détection = plancher.

## Conséquences

### Positives

- **POS-001** : Identité des scopes en **données** (front-matter), auto-détection par `keywords` déclarés plutôt qu'en prose — alignée sur le contrat AI-DLC « Scopes ».
- **POS-002** : Source d'identité unique par scope ; le tableau reste lisible mais cesse d'être la source de vérité, réduisant le risque de dérive.
- **POS-003** : `review_cap` rend l'allègement de revue explicite et conforme, sans abandonner l'axe « vérification » adapté au documentaire.
- **POS-004** : Appartenance transposée déjà conforme — aucun re-travail sur les fiches de stage.

### Négatives

- **NEG-001** : Deux surfaces à garder cohérentes (fichiers de scope ↔ vue lisible) ; atténué par la note de préséance et une vérification à chaque évolution.
- **NEG-002** : Champ maison `verification` en plus de `review_cap` — un lecteur habitué à AI-DLC doit lire la règle de mapping.

## Alternatives étudiées

### ALT-001 — Conserver uniquement le tableau en prose

Ne rien extraire en fichiers de scope, garder l'identité dans `scopes-and-axes.md`.

**Raison du rejet** : ne respecte pas le contrat AI-DLC « un fichier par scope » ; l'auto-détection reste en prose, non déclarée en données.

### ALT-002 — Réintroduire `testStrategy` d'AI-DLC tel quel

Remplacer l'axe « vérification » par `testStrategy`.

**Raison du rejet** : le workspace est majoritairement documentaire ; l'axe « vérification » couvre le cas documentaire et se replie sur une stratégie de tests dès qu'il y a du code / IaC (reconduit de [ADR-0003](0003-scopes-et-axes-depth-verification.md)).

### ALT-003 — Compiler un `scope-grid.json`

Reproduire la transposition compilée d'AI-DLC.

**Raison du rejet** : non applicable — pas de moteur AI-DLC, exécution via Multica. La matrice lisible et le champ `scopes:` des stages suffisent.

## Notes d'implémentation

- **IMP-001** : Fichiers créés sous [`core/scopes/`](../core/scopes/) — un `README.md` (contrat + divergence + mapping) et 8 fichiers de scope.
- **IMP-002** : [`scopes-and-axes.md`](../core/common/protocols/scopes-and-axes.md) mis à jour : note de préséance, liens vers les fichiers de scope, colonne `review_cap`, renvoi vers cet ADR.
- **IMP-003** : Champs `runner` / `freeform_default` d'AI-DLC volontairement omis (non applicables Multica).

## Références

- **REF-001** : [ADR-0001 — Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [ADR-0003 — Scopes et axes Depth / vérification des livrables](0003-scopes-et-axes-depth-verification.md)
- **REF-003** : [AI-DLC Harness Engineer Guide — Scopes](https://awslabs.github.io/aidlc-workflows/harness-engineering/04-scopes/)
- **REF-004** : [`core/scopes/README.md`](../core/scopes/README.md)
