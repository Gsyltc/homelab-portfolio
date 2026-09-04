# Alignement des fiches de stage Homelab sur le contrat AI-DLC « Anatomy of a Stage »

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : 2026-09-03
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — validation humaine explicite obtenue (multica.gaston, 2026-09-03, issue ALI-210) : les trois points soumis ont été confirmés — (1) **conserver la revue advisory** de `central-quality-control` (fix `reviewer: Tech Lead Homelab`, `review_class: advisory` inchangé), (2) ne pas utiliser `for_each` pour le verrou de concurrence (verrou inter-runs via `concurrency-lock-read`), (3) acceptation de l'ADR. L'invariant est respecté (aucun ADR accepté sans validation humaine granulaire). Cet ADR **ne modifie aucune posture de sécurité** ni **aucune surface d'exécution** : les 26 fiches de stage Homelab portaient déjà, dès leur production en ALI-207 (Stage 7 d'ALI-200), le corps en trois compartiments et le vocabulaire de front-matter normalisé. Ce stage **vérifie** la conformité, **corrige une seule incohérence** (`central-quality-control`, voir § Décision 5) et **trace** les divergences assumées.

## Contexte

Les fiches de stage du workflow **Homelab** vivent sous [`homelab/common/stages/<phase>/<slug>.md`](../homelab/common/stages/) (26 fichiers, 5 phases : `initialisation`, `ideation`, `cadrage`, `production`, `validation`). Elles ont été **produites directement conformes** lors de la refonte du workflow Homelab au modèle conductor/stages/protocols (ALI-200 Stage 7, issue **ALI-207**, tracée en [ADR-0018](0018-adaptation-modele-conductor-stages-protocols-homelab.md)), sur le contrat de [`homelab/common/protocols/stage-definition.md`](../homelab/common/protocols/stage-definition.md).

Le **Stage 2** de l'alignement AI-DLC du harness Homelab (issue **ALI-210**, parente ALI-208) porte ces fiches sur le contrat **« Anatomy of a Stage »** du *Harness Engineer Guide* (`awslabs/aidlc-workflows`, `harness-engineering/01-anatomy-of-a-stage`). C'est l'**équivalent Homelab** du travail fait pour le harness `core` (issue ALI-195, tracée en [ADR-0009](0009-alignement-fiches-de-stage-sur-ai-dlc.md)).

Contrat visé (deux lecteurs disjoints — le **parseur** ne lit que le front-matter YAML, l'**agent exécutant** ne lit que le corps) :

1. **Corps en trois compartiments, ordre fixe** : `## Steps` → `## Sensors` → `## Learn`.
2. **Vocabulaire `mode`** (topologie de communication) : `inline | subagent | pipeline | mob`.
3. **`review_class` + `review_artifact`** : nature de la revue (`adversarial | advisory | none`) séparée de la force du gate humain (`human_gate`).
4. **`for_each`** : itération une-fois-par-instance (omis ⇒ exécution unique).
5. **Liaison de sensors** par id nu ; cohérence `produces` / `consumes` / `requires_stage`.

**Constat d'entrée (particularité de ce stage)** : contrairement au harness `core` (où les 20 fiches portaient un corps `## Objectif`/`## Steps`/`## Gate` à réécrire — ADR-0009), les 26 fiches Homelab portent **déjà** le corps `## Steps`/`## Sensors`/`## Learn` en ordre fixe et un front-matter au vocabulaire AI-DLC. Le travail de ce stage est donc principalement de **vérifier** la conformité de façon systématique, **corriger le résiduel** et **tracer les divergences assumées** — pas de réécrire un corps non conforme.

Contrainte de cadrage (ALI-208 / [ADR-0013](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md)) : adapter au moteur A2A **Multica**, sans importer le tooling amont non applicable (`bun`, compilation `stage-graph.json`, hooks `.ts`) ; le graphe reste conceptuel via `consumes` / `produces` / `requires_stage`. Aucune régression sur les garde-fous absolus du Homelab.

## Décision

**Vérifier et aligner les 26 fiches de stage Homelab sur le contrat « Anatomy of a Stage »** — corps trois compartiments, vocabulaire `mode`/`review_class`, `for_each`, liaison de sensors, cohérence `produces`/`consumes` — **en traçant les divergences maison assumées** plutôt qu'en important le tooling amont.

### 1. Corps en trois compartiments (ordre fixe) — conformité vérifiée

Les **26 fiches** portent, après le front-matter, exactement `## Steps` → `## Sensors` → `## Learn` (chacun présent une seule fois, dans l'ordre — vérifié programmatiquement). Aucune correction n'a été nécessaire.

- **`## Steps`** — prose impérative (le travail métier).
- **`## Sensors`** — résumé local compact : `Outputs:` (où atterrissent les sorties + type de gate humain), `Imports:` **reflétant** le front-matter `sensors:` (`none` si vide), `Upstream targets:` **reflétant** `consumes:` quand pertinent, et les exceptions propres au stage (`Review artifact:`). Le comportement partagé des sensors reste dans [`homelab/sensors/README.md`](../homelab/sensors/README.md).
- **`## Learn`** — contrat de boucle d'apprentissage (voir § Décision 4).

Le corps est un **artefact de framework immuable en forme** ; la seule édition sanctionnée en cours de workflow est l'ajout d'un id de sensor à `sensors:` (déclencheur `SENSOR_PROPOSED`).

### 2. Vocabulaire `mode` (topologie de communication) — conformité vérifiée

Toutes les valeurs `mode` des 26 fiches appartiennent à l'ensemble AI-DLC `inline | subagent | pipeline | mob` (vérifié) ; aucune valeur maison résiduelle (ex. `multi-agent`). Répartition observée :

- `inline` — majorité des stages courts (bootstrap Initialisation, cadrage, aiguillage Tech Lead, gates de Validation).
- `subagent` — délégations hub-and-spoke : `docker-compose-creation`, `docker-compose-qa`, `terraform-configuration`, `n8n-branch`, `home-assistant-branch`, `review-and-notification`.
- `pipeline` — `autonomy-mode` (Tech Lead → Spécialiste Docker → QA Docker, chaînage ordonné) ; `support_agents` non vide (contrainte AI-DLC respectée).
- `mob` — inutilisé côté Homelab (aucun stage ne fait travailler plusieurs supports en ronde d'objection parallèle) ; divergence D-1 ci-dessous.

### 3. `review_class` + `review_artifact` — conformité vérifiée + une correction

Vocabulaire AI-DLC `adversarial | advisory | none` respecté. Répartition :

- **`adversarial`** (revue indépendante non substituable, plancher SG-3) : `autonomy-mode` (reviewer QA Docker, artefact `walking-skeleton.md`), `docker-compose-qa` (reviewer QA Docker, artefact `rapport-qa-docker.md`).
- **`advisory`** (revue consultative préparant le gate humain) : `central-quality-control` (contrôle qualité central du Tech Lead, artefact `controle-qualite-central.md`).
- **`none`** : les 23 autres stages (aucune revue indépendante déclarée).

**Correction de cohérence appliquée** — voir § Décision 5.

### 4. `for_each` et compartiment `## Learn`

- **`for_each`** : **aucune fiche** ne porte `for_each` (toutes en exécution unique). Réponse à l'input de l'issue ci-dessous (§ Décision 6) : le `for_each` n'est **pas** le mécanisme du verrou de concurrence par stack.
- **`## Learn`** : chaque compartiment pointe vers la **boucle d'apprentissage Homelab** ([`homelab/rules/`](../homelab/rules/README.md)), alignée sur ALI-200 Stage 3 ([ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md)) : cycle capture → confirmation humaine → contrôle de conflit → écriture, avec les 4 couches `global > stack > phase > scope`. Les stages d'**Initialisation** tiennent le journal des candidats-règles mais **sautent** l'interaction liée au gate humain (bootstrap déterministe) — conforme au protocole.

### 5. Correction unique — `central-quality-control` : `reviewer: null` → `reviewer: Tech Lead Homelab`

La fiche `production/central-quality-control.md` portait `reviewer: null` **avec** `review_class: advisory` **et** `review_artifact: controle-qualite-central.md`. Cela **violait** la règle de cohérence du protocole (`reviewer: null ⇒ review_class: none` et pas de `review_artifact` ; `reviewer != null ⇒ review_class != none` **et** `review_artifact` renseigné).

**Résolution retenue** : renseigner `reviewer: Tech Lead Homelab` (au lieu d'abaisser `review_class` à `none`). Motif : le contrôle qualité central **est** une revue advisory réellement effectuée (aiguillage GO / RENVOI au niveau macro, produisant l'artefact `controle-qualite-central.md`) ; la porter par une fonction nommée **préserve la sémantique de revue** au lieu de la supprimer. Le Tech Lead étant à la fois `lead_agent` et porteur de cette revue advisory, c'est le **même patron déjà sanctionné** dans le harness Homelab : `docker-compose-qa` a `lead_agent: QA Docker` **et** `reviewer: QA Docker`. La note `Review artifact:` du corps a été mise à jour pour expliciter que la revue est portée par le Tech Lead lui-même.

**Divergence vs core** : sur `core` (ADR-0009, § Décision 3), le cas analogue (`consolidation-handoff`, `review_class: granular` + `reviewer: null`) avait été résolu en abaissant à `review_class: none` — car il n'y avait pas de revue réelle, seulement une confusion nature/gate. Ici la revue advisory du Tech Lead **existe** et produit un artefact ; on la **conserve** en nommant son porteur. Divergence assumée et cohérente avec le rôle « contrôleur qualité central » du Tech Lead (voir [ADR-0019](0019-alignement-definitions-agents-homelab-sur-ai-dlc.md), § Décision 3).

### 6. Réponses aux inputs requis de l'issue

- **Compartiment `Learn` ↔ learning loop (ALI-200 Stage 3)** : rattaché. Chaque `## Learn` référence [`homelab/rules/`](../homelab/rules/README.md) (learning loop [ADR-0015](0015-learning-loop-et-regles-persistantes-homelab.md)) ; les stages d'Initialisation journalisent sans interaction de gate (bootstrap).
- **`for_each` pour la sérialisation par stack (verrou de concurrence) ?** — **Non.** Le verrou « un seul traitement par stack » est un **verrou inter-runs** porté par le stage déterministe [`initialisation/concurrency-lock-read.md`](../homelab/common/stages/initialisation/concurrency-lock-read.md) (lecture de la clé de metadata `active_step`, mise en file si occupé). Le `for_each` du protocole nomme au contraire un **artefact dont les instances pilotent une itération une-fois-par-instance à l'intérieur d'un même run** (ex. un lot de livrables). Confondre les deux mécaniserait à tort le verrou de concurrence en boucle d'itération. Le `for_each` reste donc **volontairement inutilisé** ; divergence D-2 tracée.

### 7. Cohérence `produces` / `consumes` / `requires_stage` — vérifiée

Vérification programmatique (script `verify_stages.py`, § Notes d'implémentation) : **0 erreur, 0 avertissement** après correction. Contrôles passés sur les 26 fiches :

- `slug` = stem de fichier ; `phase` = répertoire ; valeurs d'énumération valides (`phase`, `execution`, `mode`, `summary_confirmation`, `review_class`, `human_gate`).
- `execution: CONDITIONAL` ⇒ `condition` non vide.
- `human_gate` cohérent avec la phase.
- `mode: pipeline|mob` ⇒ `support_agents` non vide.
- Cohérence `reviewer` / `review_class` / `review_artifact` (les deux sens de l'implication).
- `sensors:` ne référence que des manifestes existants (6 sensors définis : `plaintext-secret`, `swarm-deploy-section`, `terraform-no-sni`, `traefik-coherence`, `vault-secret-exists`, `yaml-validity`).
- `requires_stage` ne référence que des slugs existants (aucune dépendance orpheline).
- Traçabilité **`consumes` required ⇒ `produces` amont** : tout artefact consommé en `required: true` est produit par un stage amont (aucune arête arrière orpheline). Les entrées `required: false` externes (ex. `detection_stack_existante_vs_nouvelle` consommée en optionnel) restent tolérées.

## Conséquences

### Positives

- **POS-001** : Les 26 fiches de stage Homelab **confirmées conformes** au contrat « Anatomy of a Stage » (corps 3 compartiments, vocabulaire `mode`/`review_class`, liaison de sensors, cohérence du graphe), vérification **outillée et reproductible**.
- **POS-002** : Incohérence unique (`central-quality-control`) **corrigée sans perte de sémantique** : la revue advisory du Tech Lead est conservée et son porteur nommé.
- **POS-003** : Traçabilité `produces`/`consumes`/`requires_stage` **vérifiée sans orphelin** ; le graphe conceptuel est cohérent sans compilation.
- **POS-004** : Réponses explicites aux deux inputs de l'issue (`Learn` ↔ learning loop ; `for_each` ≠ verrou de concurrence), tracées comme décisions.
- **POS-005** : Divergences vs `core` (pas de `mob` ; `for_each` inutilisé ; revue advisory portée par le lead) **explicitement assumées et tracées**.

### Négatives

- **NEG-001** : La correction `central-quality-control` diverge de la résolution `core` du cas analogue (abaissement à `none`) : divergence assumée, justifiée par l'existence réelle de la revue advisory du Tech Lead. À re-confirmer si le rôle du Tech Lead évoluait.
- **NEG-002** : `mob` et `for_each` restent inutilisés côté Homelab : le vocabulaire est plus large que l'usage actuel, sans coût mais à documenter pour éviter une conclusion « champ manquant ».
- **NEG-003** : La vérification de cohérence du graphe reste **advisory** (conventions Markdown, pas de compilation `stage-graph.json` — non applicable Multica) ; elle dépend du script de vérification, non d'un moteur runtime.

## Alternatives étudiées

### ALT-001 — Abaisser `central-quality-control` à `review_class: none` (miroir strict de core)

**Raison du rejet** : supprimerait la trace d'une revue advisory qui **existe réellement** (le Tech Lead aiguille GO / RENVOI et produit `controle-qualite-central.md`). Nommer le porteur (`reviewer: Tech Lead Homelab`) satisfait le contrat **et** préserve la sémantique ; c'est le patron déjà utilisé pour `docker-compose-qa` (reviewer = lead).

### ALT-002 — Utiliser `for_each: stack` pour sérialiser le traitement par stack

**Raison du rejet** : le `for_each` est une itération **intra-run** (une passe par instance d'artefact), pas un **verrou inter-runs**. La sérialisation par stack est un contrôle de concurrence porté par `concurrency-lock-read` (metadata `active_step`). Mélanger les deux introduirait une sémantique erronée.

### ALT-003 — Réécrire les corps pour aligner le style sur `core`

**Raison du rejet** : les corps Homelab sont **déjà** conformes en forme (3 compartiments, ordre fixe) ; une réécriture cosmétique risquerait des régressions sans bénéfice de conformité.

## Notes d'implémentation

- **IMP-001** : **26 fiches** `homelab/common/stages/*/*.md` vérifiées — corps `## Steps`/`## Sensors`/`## Learn` en ordre fixe (present-une-fois, vérifié), vocabulaire `mode`/`review_class`/`human_gate`/`summary_confirmation`/`execution` dans les ensembles AI-DLC, `sensors:` sans id orphelin (6 manifestes définis), `requires_stage` sans slug orphelin, traçabilité `consumes(required)` ⇒ `produces` sans orphelin.
- **IMP-002** : **Une seule modification de fichier de stage** : `production/central-quality-control.md` — front-matter `reviewer: null` → `reviewer: Tech Lead Homelab` (les champs `review_class: advisory` et `review_artifact: controle-qualite-central.md` inchangés) et note `Review artifact:` du corps précisée (« revue portée par le **Tech Lead** lui-même »). Aucune autre fiche modifiée.
- **IMP-003** : Vérification **outillée et reproductible** via un script de contrôle (parsing front-matter + règles de cohérence du protocole + graphe `produces`/`consumes`/`requires_stage` + validation des ids de sensors). Résultat final : **0 erreur, 0 avertissement**. Le script est un outil de vérification local (non versionné dans le dépôt ; peut être reproduit à la vérification globale ALI-214).
- **IMP-004** : **Pointeur hors périmètre (à traiter en ALI-214)** — le fichier `decisions/0011-alignement-memoire-de-regles-sur-ai-dlc.md` porte encore **6 marqueurs de conflit Git résiduels** (`<<<<<<<` / `=======` / `>>>>>>>`), déjà signalés en ALI-209. Non traité ici (hors périmètre stages) ; à nettoyer à la vérification globale.
- **IMP-005** : Numérotation — le présent ADR est **0020** (suivant `0019`). Pointeurs `README.md` et `AGENTS.md` mis à jour vers `0001…0020`.
- **IMP-006** : Contrôle sécurité — cet ADR **ne déplace aucune fonction de verdict** ni surface d'exécution : les revues adversariales (QA Docker) et la posture sécurité (Architecte de sécurité, couche `global`) sont inchangées. La correction `central-quality-control` reste **advisory** (ne remplace ni le contrôle sécurité ni la validation humaine, plancher SG-3). Le passage à *Accepted* requiert la validation humaine granulaire (invariant).

## Références

- **REF-001** : Issue ALI-210 (Stage 2 — Stages Homelab : corps 3 compartiments, vocabulaire, `for_each`, sensors) ; issue parente ALI-208.
- **REF-002** : [ADR-0009 - Alignement des fiches de stage sur le contrat AI-DLC « Anatomy of a Stage »](0009-alignement-fiches-de-stage-sur-ai-dlc.md) (équivalent `core`, issue ALI-195).
- **REF-003** : [ADR-0018 - Adaptation du modèle conductor/stages/protocols au Homelab](0018-adaptation-modele-conductor-stages-protocols-homelab.md) (production des fiches, ALI-207).
- **REF-004** : [ADR-0015 - Learning loop et règles persistantes Homelab](0015-learning-loop-et-regles-persistantes-homelab.md) (compartiment `## Learn`).
- **REF-005** : [ADR-0019 - Alignement des définitions d'agents Homelab sur AI-DLC](0019-alignement-definitions-agents-homelab-sur-ai-dlc.md) (rôle Tech Lead / QA Docker / distinction domaine-review).
- **REF-006** : [`homelab/common/protocols/stage-definition.md`](../homelab/common/protocols/stage-definition.md) — schéma de front-matter et règles de cohérence.
- **REF-007** : [AI-DLC — Harness Engineer Guide, « Anatomy of a Stage »](https://awslabs.github.io/aidlc-workflows/harness-engineering/01-anatomy-of-a-stage/)
