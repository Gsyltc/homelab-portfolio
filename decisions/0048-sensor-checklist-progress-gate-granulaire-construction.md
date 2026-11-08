# Sensor `checklist-progress` de catégorie `progress` attaché au gate granulaire de Construction

---
auteurs: Sylvain Goubaud
accepté par : "Sylvain Goubaud"
accepté le : "2026-11-08"
supersedes: ""
superseded_by: ""

---

## Status

Accepted

## Date de création

2026-11-08

## Contexte

La **checklist d'architecture** est un processus de suivi du workflow `core` : un fichier d'état versionné `documentation/00-checklist-architecture.md` dont la logique (structure imposée, **barème 80/10/10**, agrégation % section / % global, écriture sur faits vérifiés) a sa **source unique** dans le protocole `core/common/protocols/architecture-checklist.md` (chaîne ADR-0042 → 0043 → 0045 ; gabarit d'état porté par la skill depuis ADR-0047).

L'humain demandeur (multica.gaston, HOM-273) veut, **avant chaque gate granulaire humaine durant la Construction**, un **retour d'avancement** restitué par un sensor attaché au workflow, à l'usage de l'**Architecte de solution intégrateur** (coordinateur). Le retour attendu : avancement **global de la solution**, avancement du **cadrage**, des **besoins (MoSCoW)** et des **livrables**.

Le workflow `core` porte déjà **huit sensors** déterministes (manifeste `core/sensors/sensors/<id>.md` + script `core/scripts/sensors/<id>.py`, exécutés par `core/scripts/sensor.py`, bijection verrouillée par `test_sensors.py`), tous **advisory**, de catégories `document-shape`, `provenance`, `traceability`. Aucun ne porte la restitution d'un **avancement** : c'est une **nouvelle catégorie** fonctionnelle (`progress`), et l'ajout d'un sensor modifie la **surface de gouvernance** du workflow (SG-1 / SG-6) ⇒ **ADR requis** (« ADR d'abord », `conductor.md`).

Point de conception : un sensor de progression ne doit **ni calculer** le barème (la mécanique 80/10/10 reste source unique du protocole), **ni décider**, **ni écrire** un avancement ou une acceptation. Il **lit** les % déjà portés dans le fichier d'état et les **restitue** — il constate, le jugement et l'acceptation restent humains.

## Décision

**Ajouter au workflow `core` un neuvième sensor, `checklist-progress`, de catégorie `progress`, `advisory`, déclenché au gate (`fire_on: gate`) sur `documentation/00-checklist-architecture.md`, attaché aux quatre stages de Construction à gate granulaire humain. Le sensor restitue l'avancement porté par le fichier d'état (global de la solution, cadrage, besoins MoSCoW, livrables) ; il ne calcule, ne décide ni n'écrit rien.**

1. **Manifeste** `core/sensors/sensors/checklist-progress.md` — `id: checklist-progress`, `kind: deterministic`, `category: progress`, `default_severity: advisory`, `fire_on: gate`, `matches: "documentation/00-checklist-architecture.md"`, `command: "python3 core/scripts/sensors/checklist_progress.py"`, `origine: HOM-273`. Le corps porte le contrat `checks` (lecture seule des quatre avancements), la forme de la sortie advisory et les garde-fous (SG-1..6 ; aucun auto-accept).

2. **Script** `core/scripts/sensors/checklist_progress.py` — bibliothèque standard, `ID = "checklist-progress"`, `run(ctx)`, réutilise `sensorlib`. Lit les % déjà portés dans le fichier d'état (`**% global :** <n> %` ; titres `## Cadrage — <n> %`, `## Besoins (MoSCoW) — <n> %`, `## Livrables — <n> %`). Fichier absent, illisible ou sans avancement lisible ⇒ `⛔ indisponible` (SG-2). Le sensor n'émet **jamais** `⚠️` : un avancement bas est un **fait restitué**, pas un écart de forme.

3. **Attachement aux stages** — `checklist-progress` est ajouté au champ `sensors:` (et à la ligne « ## Sensors » / Imports) des **quatre** stages de Construction portant `human_gate: granular` : `walking-skeleton`, `detailed-deliverables`, `consolidation-handoff`, `delivery-handoff`. Le stage `security-consistency-check` (`human_gate: none`) est **hors périmètre**.

4. **Mécanique inchangée** — le barème 80/10/10, le décompte des sections conformes, la revue pair, l'acceptation humaine et l'agrégation restent la **source unique** du protocole `architecture-checklist.md`. Le sensor **lit et restitue**, il ne recalcule rien.

### Périmètre

- Ajout d'un sensor (manifeste + script + test + documentation README) et son attachement aux quatre stages de Construction à gate granulaire.
- **Hors périmètre** : la logique du protocole (inchangée), les 5 phases, les scopes, les contrats `required-sections` / `data-lifecycle`, la posture de sécurité, la validation humaine granulaire. Le **passage de `advisory` à `blocking`** resterait une décision **séparée** (ADR + contrôle sécurité), comme pour les autres sensors.

## Conséquences

### Positives

- **POS-001** — **retour d'avancement déterministe** avant chaque gate granulaire humaine de Construction : l'Architecte de solution intégrateur dispose des quatre avancements (solution, cadrage, besoins, livrables) sans calcul manuel.
- **POS-002** — **séparation nette constat / décision** : le sensor restitue ce que le fichier d'état porte ; il ne calcule pas le barème (source unique = protocole) et n'écrit aucun %, préservant « aucun auto-accept ».
- **POS-003** — **nouvelle catégorie `progress`** ouverte proprement, sur le modèle exact des 8 sensors existants (manifeste + script + bijection testée).
- **POS-004** — **garde-fous préservés** : advisory, SG-1..6 respectés ; `⛔` sur fichier absent / illisible (jamais lu comme conforme) ; aucune substitution à la validation humaine ni au contrôle sécurité.

### Négatives / points d'attention

- **NEG-001** — **cohérence à maintenir** entre le format du gabarit d'état (titres portant le `%`) et le parsing du sensor : un changement de format du gabarit (porté par la skill, ADR-0047) doit être répercuté dans le script dans la même PR (SG-1 / SG-6).
- **NEG-002** — le sensor **dépend d'un fichier d'état renseigné par le coordinateur** : avant toute mise à jour des %, il restitue l'état initial (`0 %` partout), ce qui est le comportement attendu (il constate), non un écart.
- **NEG-003** — **bijection verrouillée à 9** : tout nouveau sensor devra mettre à jour `OneScriptPerSensorTests` (8 → 9 ici).

## Alternatives étudiées

### ALT-001 — Sensor qui calcule le barème 80/10/10

Faire calculer l'avancement par le sensor à partir des sections conformes.

**Raison du rejet** : dupliquerait la mécanique du protocole (perte de la source unique, dérive garantie) et ferait du sensor un décideur. Le protocole reste la source unique ; le sensor **constate** les % déjà portés.

### ALT-002 — Attacher le sensor au seul `detailed-deliverables`

Limiter l'attachement à un stage.

**Raison du rejet** : la demande vise **chaque** gate granulaire humaine de Construction ; les quatre stages `human_gate: granular` sont concernés. `security-consistency-check` (`human_gate: none`) reste hors périmètre.

### ALT-003 — Sensor `blocking` sur un seuil (≥ 80 %)

Rendre le sensor bloquant sous le seuil du gate planification / réalisation.

**Raison du rejet** : le gate ≥ 80 % relève du protocole et d'une **décision humaine** ; rendre un sensor bloquant est une décision structurante séparée (ADR + contrôle sécurité). Par défaut, tout reste advisory.

## Notes d'implémentation

- **IMP-001** — manifeste `core/sensors/sensors/checklist-progress.md` (front-matter + corps `checks` / sortie / garde-fous).
- **IMP-002** — script `core/scripts/sensors/checklist_progress.py` (`ID`, `run(ctx)`, `sensorlib`, lecture seule, `⛔` sur absence / illisibilité).
- **IMP-003** — attachement aux quatre stages Construction à gate granulaire (`sensors:` + ligne Imports) ; `security-consistency-check` exclu.
- **IMP-004** — tests `core/scripts/tests/test_sensors.py` : `OneScriptPerSensorTests` 8 → 9 (bijection préservée) ; cas `SensorTests` : checklist absente ⇒ `⛔`, checklist renseignée ⇒ `✅` avec les quatre avancements.
- **IMP-005** — ligne `checklist-progress` au tableau « Sensors définis » de `core/sensors/README.md` (catégorie `progress`) + « Huit sensors » → « Neuf sensors ».
- **IMP-006** — vérifications : `python3 core/scripts/sensor.py list` (9ᵉ sensor, script valide) ; `python3 -m unittest discover -s core/scripts/tests` (bijection 9, nouveau cas vert).

## Références

- **REF-001** — HOM-273 (mission d'origine) / HOM-287 (sous-issue B, ce travail) : multica.gaston, demande d'un sensor de restitution d'avancement avant chaque gate granulaire humaine de Construction.
- **REF-002** — [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) — source unique du processus et du barème 80/10/10 (inchangée).
- **REF-003** — [`0043-checklist-architecture-avancement-en-pourcentage-bareme-80-10-10.md`](0043-checklist-architecture-avancement-en-pourcentage-bareme-80-10-10.md) — barème 80/10/10 restitué par le sensor.
- **REF-004** — [`0047-checklist-gabarit-porte-par-la-skill-sans-couplage-core-plugin.md`](0047-checklist-gabarit-porte-par-la-skill-sans-couplage-core-plugin.md) — gabarit d'état porté par la skill (sous-issue A, HOM-286).
- **REF-005** — [`0046-sensors-executables-python-et-hooks-agnostiques.md`](0046-sensors-executables-python-et-hooks-agnostiques.md) — modèle manifeste + script Python des sensors, bijection testée.
- **REF-006** — [`core/sensors/README.md`](../core/sensors/README.md) — tableau « Sensors définis » (catégorie `progress`) et garde-fous SG-1..6.
- **REF-007** — stages de Construction à gate granulaire : [`walking-skeleton`](../core/common/stages/construction/walking-skeleton.md), [`detailed-deliverables`](../core/common/stages/construction/detailed-deliverables.md), [`consolidation-handoff`](../core/common/stages/construction/consolidation-handoff.md), [`delivery-handoff`](../core/common/stages/construction/delivery-handoff.md).
