# Durcissement du sensor required-sections (volet DAS)

---
auteurs: multica.gaston  
accepté par : multica.gaston  
accepté le : 2026-09-05  
supersedes: ""  
superseded_by: ""  

---

## Status

Accepted

> Statut **Accepted** — validation humaine granulaire explicite obtenue (multica.gaston, 2026-09-05) et contrôle sécurité sur la surface du manifeste `required-sections` satisfait (invariant de gouvernance A2A respecté : aucun ADR accepté sans validation humaine). Aucune posture de sécurité n'est modifiée ici ; les clauses SG-1 à SG-6 ([ADR-0005](0005-verification-gates-et-sensors.md)) sont préservées à l'identique et le caractère advisory est reconduit.

## Contexte

Les architectes rédigent la documentation d'architecture de solution (DAS) à partir des gabarits de la skill `architecture-solution-gabarits` (`plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/`, 16 fichiers `001`, `01`–`15`). Jusqu'ici, le volet `das:` du sensor [`required-sections`](../core/sensors/sensors/required-sections.md) (advisory, `fire_on: gate`, introduit en [ADR-0005](0005-verification-gates-et-sensors.md), aligné AI-DLC en [ADR-0012](0012-alignement-sensors-sur-ai-dlc.md)) ne vérifiait que **5 rubriques minimales** génériques (`titre`, `contexte / objectif`, `vues (fonctionnelle / technique)`, `décisions liées (ADR)`, `risques`), portées en propre dans le manifeste — sans refléter le découpage réel de la DAS ni les fichiers les plus structurants.

L'humain (multica.gaston, issue ALI-218) souhaite un sensor **adapté** qui signale une documentation d'architecture **incomplète**, en s'assurant que les **fichiers et sections les plus importants (mandatory)** de la DAS sont **présents et non vides** au gate de phase.

Deux options avaient été posées pour la source de vérité des sections mandatory :

- **Option A — Sensor autonome.** Le manifeste `required-sections` porte lui-même la liste étendue des fichiers/sections DAS mandatory. Aucun couplage `core → plugin`. Coût : cohérence à maintenir à deux endroits (gabarit + manifeste), soit le [NEG-004](0012-alignement-sensors-sur-ai-dlc.md) déjà anticipé en ADR-0012.
- **Option B — Gabarits = source de vérité machine-lisible.** Marquer les sections mandatory dans les gabarits eux-mêmes (front-matter `mandatory: true`) ; le manifeste **dérive** ses attentes des gabarits. Plus proche du contrat AI-DLC (« the `required-sections` sensor derives its expectations from templates »). Coût : dépendance documentée `core → skill` à assumer et tracer comme divergence.

Dans les deux cas, **les gabarits restent dans la skill** : la décision ne portait que sur la manière dont le sensor connaît les sections mandatory. Le déplacement des gabarits hors de la skill était explicitement **hors périmètre** (les gabarits sont un asset de skill — outil de travail de l'architecte, règle d'or n°3 — atteint par le workflow via `skills:` des agents `solution-architect-agent` / `architecture-solution-integration-agent`).

## Décision

**Retenir l'Option A** (choix humain, multica.gaston, ALI-218) : le manifeste `required-sections` porte **en propre** la liste des fichiers et sections DAS mandatory, sans couplage `core → plugin`, dans la continuité de la trajectoire d'[ADR-0012](0012-alignement-sensors-sur-ai-dlc.md).

**Ensemble mandatory retenu** — au gate, chacun de ces **7 fichiers** doit être **présent** dans le répertoire `documentation/` du projet (les fichiers `.md` y sont déposés directement) et **non vide** (contenu propre ; commentaires HTML et cellules d'exemple ne comptent pas comme contenu) :

| Fichier | Thème |
| --- | --- |
| `001-document-architecture-solution.md` | Page de garde, historique, arrimages, structure |
| `01-introduction.md` | Contexte, périmètre, parties prenantes |
| `02-objectifs.md` | Objectifs, NFRs, matrice de suivi patrons ↔ piliers |
| `06-architecture-solutions.md` | Architecture de solution, diagrammes |
| `08-contraintes.md` | Lois, conformités, contraintes technologiques |
| `10-cycle_vie_donnees.md` | Cycle de vie et classification des données |
| `11-securite.md` | Modélisation des menaces (STRIDE), sécurité applicative |

Les fichiers `03`, `04`, `05`, `07`, `09`, `12`–`15` restent **recommandés** mais **hors périmètre mandatory** de ce check.

**Caractère advisory reconduit** ([ADR-0005](0005-verification-gates-et-sensors.md)) — le sensor **signale** l'incomplétude ; il ne bloque pas l'écriture, ne remplace ni la validation humaine granulaire ni le contrôle sécurité systématique. Tout passage à `blocking` resterait une décision structurante distincte (ADR + contrôle sécurité) — **hors périmètre** ici.

**Règle de cohérence gabarit ↔ manifeste (matérialisation NEG-004)** — la liste étant portée en propre par le manifeste, toute évolution du découpage ou du titre d'une section dans un gabarit mandatory (`gabarits/001`, `01`, `02`, `06`, `08`, `10`, `11`) **doit être répercutée dans le manifeste dans la même PR**. Cette synchronisation relève de SG-1 / SG-6 (versionnée, tracée, contrôle sécurité si affaiblissement).

## Conséquences

### Positives

- **POS-001** : Le sensor signale désormais une DAS **incomplète** de façon adaptée au découpage réel (7 fichiers structurants), là où il ne portait que 5 rubriques génériques.
- **POS-002** : Aucun couplage `core → plugin` introduit ; le manifeste reste autonome et directement lisible (Option A), cohérent avec la trajectoire d'ADR-0012.
- **POS-003** : Posture de sécurité (SG-1 à SG-6) et caractère advisory **inchangés** ; l'incomplétude est un signal factuel, la validation reste humaine.
- **POS-004** : La règle de cohérence gabarit ↔ manifeste (NEG-004) est **explicitée et outillable** par la revue de PR, au lieu de rester implicite.

### Négatives

- **NEG-001** : Cohérence à maintenir **à deux endroits** (gabarit + manifeste) — c'est le coût assumé de l'Option A (NEG-004 d'ADR-0012), atténué par la règle de synchronisation en PR.
- **NEG-002** : Un durcissement du périmètre d'un check advisory peut générer davantage de signaux `⚠️` sur des DAS partielles en cours de rédaction ; atténué par le caractère advisory (aucun blocage) et par le fait que le check est évalué **au gate**, pas à chaque écriture.
- **NEG-003** : Le manifeste n'étant pas exécutable ([DIV-command](0012-alignement-sensors-sur-ai-dlc.md)), la vérification reste portée par l'application disciplinée du coordinateur tant qu'aucun outillage n'est ajouté.

## Alternatives étudiées

### ALT-001 — Option B (gabarits = source de vérité machine-lisible)

Marquer les sections mandatory dans le front-matter des gabarits (`mandatory: true`) et faire **dériver** le manifeste de ces marquages, au plus près du contrat AI-DLC (« the `required-sections` sensor derives its expectations from templates »).

**Raison du rejet** : introduit une dépendance `core → skill` à tracer comme divergence supplémentaire, alors que la trajectoire retenue depuis ADR-0012 est celle du manifeste autonome sans couplage `core → plugin`. Choix humain explicite en faveur de l'Option A (multica.gaston, ALI-218). L'Option B reste réévaluable si un dispatcher exécutable dérivant des gabarits est un jour importé.

### ALT-002 — Conserver les 5 rubriques génériques

Ne rien changer au volet `das:`.

**Raison du rejet** : les 5 rubriques génériques ne reflètent pas le découpage réel de la DAS et ne détectent pas l'absence des fichiers structurants ; elles ne répondent pas au besoin exprimé (signaler une documentation incomplète).

### ALT-003 — Rendre le check bloquant

Enforcer la présence des 7 fichiers au gate.

**Raison du rejet** : contredirait la décision de gouvernance advisory ([ADR-0005](0005-verification-gates-et-sensors.md)) et déplacerait le pouvoir de décision vers un automate non outillé. Retenu : advisory ; passage à `blocking` = décision structurante distincte (ADR + contrôle sécurité).

## Notes d'implémentation

- **IMP-001** : [`core/sensors/sensors/required-sections.md`](../core/sensors/sensors/required-sections.md) — bloc `das:` réécrit (`fichiers_mandatory` : 7 fichiers + sections, `non_vide: true`) ; corps enrichi (tableau des fichiers mandatory + justification, règle de cohérence gabarit ↔ manifeste) ; `description` et `origine` du front-matter mis à jour (`ALI-188 (durcissement volet DAS : ALI-218)`) ; section Sortie complétée (fichier mandatory absent = écart, SG-2).
- **IMP-002** : [`core/sensors/README.md`](../core/sensors/README.md) — ligne `required-sections` de la table « Sensors définis » précisée (fichiers/sections mandatory de la DAS, renvoi vers cet ADR).
- **IMP-003** : `matches` corrigé pour le volet DAS — les documents de la DAS vivent directement dans le répertoire `documentation/` du projet (chemin racine configuré dans Multica) ; le glob passe de `documentations/**/*.md` à `documentation/*.md` (ALI-218, commentaire multica.gaston). `fire_on: gate`, `kind`, `command` (placeholder non exécutable, DIV-command) et l'invariant `id` = stem du fichier sont préservés.
- **IMP-006** : Cohérence de chemin propagée aux sensors frères — sur confirmation humaine (multica.gaston, ALI-218), le glob des sensors `upstream-coverage`, `claim-sources` et `traceability` est harmonisé de `documentations/**/*.md` vers `documentation/*.md` dans la même PR (les segments `decisions/` et `livrables/` restent inchangés). Modification de leur surface de gouvernance tracée au titre de SG-1 / SG-6, sans autre changement sémantique.
- **IMP-004** : Contrôle sécurité (Architecte cybersécurité / Reviewer de sécurité) sur la surface du manifeste **avant** validation humaine et passage à *Accepted* ; clauses SG-1 à SG-6 reconduites sans changement.
- **IMP-005** : Cohérence gabarit ↔ manifeste (NEG-004) à vérifier en revue à chaque évolution d'un gabarit mandatory (`gabarits/001`, `01`, `02`, `06`, `08`, `10`, `11`).

## Références

- **REF-001** : [ADR-0005 — Verification gates et Sensors déterministes advisory](0005-verification-gates-et-sensors.md)
- **REF-002** : [ADR-0012 — Alignement des manifestes de sensors sur le contrat AI-DLC « Sensors »](0012-alignement-sensors-sur-ai-dlc.md)
- **REF-003** : [ADR-0003 — Scopes et axes Depth / vérification des livrables](0003-scopes-et-axes-depth-verification.md)
- **REF-004** : [`core/sensors/sensors/required-sections.md`](../core/sensors/sensors/required-sections.md) ; [`core/sensors/README.md`](../core/sensors/README.md)
- **REF-005** : [AI-DLC Harness Engineer Guide — Sensors](https://awslabs.github.io/aidlc-workflows/harness-engineering/06-sensors/)
