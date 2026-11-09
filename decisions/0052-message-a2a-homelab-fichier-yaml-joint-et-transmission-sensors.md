# Message A2A du workflow `homelab` porté par un fichier YAML joint (réduction de prose dans le fil) avec transmission des sensors

---
auteurs: Sylvain Goubaud
accepté par : Sylvain Goubaud
accepté le : "2026-11-09"
supersedes: ""
superseded_by: ""

---

## Status

Accepted

## Date de création

2026-11-09

## Contexte

La communication **agent↔agent (A2A)** du workflow `homelab` transite aujourd'hui **de façon hétérogène dans le fil de commentaires de l'issue** :

- le **message de délégation** du Tech Lead Homelab est encore de la **prose** — la « Règle A2A » de `homelab/common/protocols/governance-security.md` prescrit une mission = « commentaire avec mission claire (objectif, périmètre, critères d'acceptation) » ; depuis HOM-291, cette prose porte en plus `core_home` (racine du checkout du harnais) et la liste des fiches / protocoles à recharger ;
- le **compte-rendu reviewer** est déjà en **YAML joint** (`homelab/common/protocols/report-format.md` + `report-format.schema.yaml`, rapport `review-<agent>-<stack>.yaml`) ;
- le **producteur** ne joint que son livrable, aucun YAML (`homelab/common/protocols/producer-report.md`), et poste ses verdicts de sensors en prose sur l'issue.

Conséquence : chaque **délégation** produit une prose d'orchestration que l'humain doit parcourir alors qu'elle ne lui est pas destinée. L'humain demande que **seuls les éléments décisionnels** restent visibles dans la tâche, la mécanique inter-agents (mission, livrable, verdicts de sensors au retour) étant transmise par **fichier joint**.

Le workflow `matching-cv-ao` résout déjà ce problème : mission et livrable voyagent dans un **fichier YAML joint** (« message A2A »), le commentaire étant réduit à la mention active + le nom du fichier ([ADR-0033](0033-format-yaml-compact-message-a2a.md)). Le workflow `core` vient de transposer ce modèle, **enrichi de la transmission des sensors** propre aux workflows outillés ([ADR-0050](0050-message-a2a-core-fichier-yaml-joint-et-transmission-sensors.md), PR #319). Le workflow `homelab` partage avec `core` ce besoin : ses agents s'appuient sur des **sensors exécutables** (HOM-292 / HOM-293 : harnais Python, invocation ancrée `$CORE_HOME`) dont la liste (à exécuter) et les verdicts (produits) doivent circuler entre agents pour que les contrôles soient effectués et tracés. Ce modèle complet n'a jamais été transposé sur `homelab`.

## Décision

Transposer sur le **seul workflow `homelab`** le modèle A2A « fichier YAML joint + commentaire minimal » (de `matching-cv-ao` / `core`), **enrichi de la transmission des sensors**, sur le modèle de l'[ADR-0050](0050-message-a2a-core-fichier-yaml-joint-et-transmission-sensors.md).

- **Deux formes de commentaire, jamais confondues** : handoff A2A pur (délégation / retour sans gate humaine) = mention active + nom du fichier YAML joint, aucune prose ; gate humaine = présentation Markdown détaillée en clair (inchangée).
- **Présentation des sensors au gate humain (obligatoire, non réductible)** : à tout gate de validation humaine, les verdicts de sensors du stage sont **présentés à l'humain en clair** (section `## Sensors` de la présentation, ou ligne « Sensors de gate » du **Rapport de vérification** — [`gates.md`](../homelab/sensors/gates.md)) ; le YAML joint ne s'y substitue jamais. La réduction de prose A2A ne retire **rien** de ce que l'humain voit au gate. Un gate humain présenté sans les sensors du stage est un écart (SG-3 / SG-2).
- **Enveloppe = YAML compact**, alignée sur le front-matter des fiches de stage et les manifestes de sensors (déjà en YAML), et sur le rapport reviewer déjà en YAML.
- **Champs sensors au schéma** du message A2A :
  - `sensors_a_executer` (délégation) — liste des sensors que l'agent délégataire doit lancer, reprise du champ `sensors:` de la fiche de stage / de la frontière de [`gates.md`](../homelab/sensors/gates.md) ;
  - `sensors_resultats` (retour / `rapport-verification`) — verdicts rendus par `sensor.py` (`conforme | ecart | indisponible` + ligne factuelle + source `manifeste @ commit`).
- **Propagation `$CORE_HOME` conservée** : le champ `core_home` (racine du checkout `homelab-portfolio`) reste porté par le message `delegation`, pour que le délégataire lance sensors / gates / hook **sans re-chercher le harnais** (acquis HOM-291) ; il rejoint simplement l'enveloppe YAML au lieu de la prose.
- **Source unique** du schéma : `homelab/common/protocols/governance-security.md`, § « Schéma du message A2A ». Les fiches de stage, [`gates.md`](../homelab/sensors/gates.md), `reviewer.md`, `report-format.md`, `producer-report.md` et les fiches d'agent s'y réfèrent par le nom `message A2A`, sans le redéfinir.
- **Articulation avec le rapport reviewer existant** : le `review-<agent>-<stack>.yaml` conforme à [`report-format.schema.yaml`](../homelab/common/protocols/report-format.schema.yaml) **reste** la forme détaillée du retour d'un reviewer (points `critical/warning/info` + `sensors[]`). Il **est** l'instance `retour` / `rapport-verification` du message A2A pour un reviewer ; le schéma A2A généralise ce contrat aux **autres handoffs** (délégation Tech Lead → spécialiste, retour producteur), aujourd'hui en prose. Les deux ne se contredisent pas : `report-format` détaille le retour reviewer, le schéma A2A porte l'enveloppe commune à tous les handoffs.
- **Garde-fous reconduits à l'identique** : le lien de mention actif reste le **seul vecteur de déclenchement** ; pas d'auto-mention active (anti-wake parasite) ; mention humaine obligatoire dès qu'une action humaine est requise ; piste d'audit sur l'issue (le YAML joint **est** l'audit) ; verdict de sensor = celui de `sensor.py`, **jamais réinterprété** ; `indisponible ≠ conforme` ; sensor déclaré dans `sensors_a_executer` mais absent de `sensors_resultats` = écart (silence interdit) ; message A2A **advisory** (ne remplace ni la validation humaine granulaire ni le contrôle sécurité systématique porté par l'Analyste QA et l'Architecte de sécurité Homelab) ; exception bloquante `plaintext-secret` / `terraform-no-sni` sur `security-patch` / `new-stack` inchangée (ALI-204).

## Conséquences

### Positives

- **POS-001** : le fil de la tâche ne porte plus que le décisionnel et les livrables destinés à l'humain — visibilité conforme à la demande (constat HOM-293).
- **POS-002** : alignement de `homelab` sur `core` et `matching-cv-ao` — un seul paradigme A2A à maintenir dans le dépôt.
- **POS-003** : économie de tokens par handoff (enveloppe YAML compacte vs prose Markdown reformulée), effet cumulé sur les chaînes longues ; mesure de référence `matching-cv-ao` : ~−25 % ([ADR-0033](0033-format-yaml-compact-message-a2a.md)).
- **POS-004** : les sensors deviennent **transmissibles et exploitables** entre agents — la liste attendue et les verdicts circulent dans l'enveloppe, sans re-dérivation ni perte de traçabilité ; cohérent avec le harnais exécutable Homelab (HOM-292 / HOM-293).
- **POS-005** : invariants de gouvernance et garde-fous sensors (SG-1..6, SEC-1..5) intacts ; `core_home` (HOM-291) préservé dans l'enveloppe.

### Négatives

- **NEG-001** : discipline de quoting YAML en notation *flow* (valeurs contenant `${...}`, `:` ou virgule) ; mitigée par « au moindre doute, guillemeter », inscrite dans le schéma source unique.
- **NEG-002** : le Tech Lead et les producteurs doivent désormais produire un fichier joint à chaque handoff (téléversement `multica attachment`) plutôt qu'un simple commentaire ; coût opératoire marginal, compensé par la lisibilité du fil. Le reviewer, lui, joignait déjà son YAML.
- **NEG-003** : frontière enveloppe ↔ données à tenir — l'enveloppe A2A est YAML ; les artefacts de données qu'elle référence (docker-compose, `.tfvars`) gardent leur format propre.

## Alternatives étudiées

### ALT-001 - Conserver la prose de délégation et ne changer que le producteur

Ne joindre un YAML qu'au retour producteur, laisser la délégation en prose.

**Raison du rejet** : laisserait la prose d'orchestration la plus volumineuse (la délégation) dans le fil et le coût token au délégataire ; n'unifierait pas le paradigme A2A. La demande vise la **mécanique inter-agents entière**, pas une moitié.

### ALT-002 - Nouveau format d'enveloppe propre à `homelab` (JSON ou format maison)

Définir un schéma A2A distinct de celui de `core` / `matching-cv-ao`.

**Raison du rejet** : introduirait un troisième paradigme A2A à maintenir ; le YAML compact est déjà éprouvé ([ADR-0033](0033-format-yaml-compact-message-a2a.md)) et aligné sur l'existant du dépôt (front-matter, sensors, rapport reviewer déjà en YAML).

### ALT-003 - Transmettre les sensors hors de l'enveloppe A2A (fichier séparé)

Un artefact de sensors distinct du message A2A.

**Raison du rejet** : multiplierait les pièces jointes et dissocierait verdicts et mission ; les loger dans l'enveloppe (`sensors_a_executer` / `sensors_resultats`) garde un seul contrat de handoff, auditable d'un bloc — et préserve la cohérence avec le `sensors[]` déjà porté par le rapport reviewer.

## Notes d'implémentation

- **IMP-001** : schéma de l'enveloppe A2A (avec `sensors_a_executer` / `sensors_resultats` et `core_home`) défini **une seule fois** dans `homelab/common/protocols/governance-security.md` (§ « Règle A2A » réécrite + « Deux formes de commentaire » + « Schéma du message A2A »).
- **IMP-002** : fichiers couplés alignés — `homelab/common/protocols/stage-protocol.md` (temps 2 délégation, temps 3 retour, temps 4 sensors à l'écriture, référence au schéma), `homelab/common/protocols/producer-report.md` (retour producteur = instance `retour` du message A2A), `homelab/common/protocols/report-format.md` (le rapport reviewer **est** l'instance `retour` / `rapport-verification` du message A2A), `homelab/common/conductor.md` (règle A2A, propagation `core_home`, diagramme de séquence), `homelab/sensors/gates.md` (rapport de gate ↔ `rapport-verification`, sensors au gate humain).
- **IMP-003** : périmètre strictement limité à `homelab` ; les workflows `core` et `matching-cv-ao` ne sont **pas** touchés par cette décision.
- **IMP-004** : aucun secret dans le YAML ; aucun `${SNI}` ; validité YAML vérifiée (règle de quoting en notation *flow*).
- **IMP-005** : entrée `CHANGELOG.md` (`[Non publié] → Changed`).

## Références

- **REF-001** : [ADR-0050 - Message A2A du workflow `core` porté par un fichier YAML joint et transmission des sensors](0050-message-a2a-core-fichier-yaml-joint-et-transmission-sensors.md) — modèle directement transposé (PR #319).
- **REF-002** : [ADR-0033 - Format YAML compact pour l'enveloppe du message A2A](0033-format-yaml-compact-message-a2a.md) — origine du format YAML compact (`matching-cv-ao`) et mesure de l'économie de tokens.
- **REF-003** : [ADR-0051 - Sensors Homelab exécutables — scripts Python déterministes, sévérité par scope et hooks d'écriture](0051-sensors-homelab-executables-python-et-hooks.md) — harnais Homelab exécutable, prérequis à la transmission de verdicts de sensors réels.
- **REF-004** : HOM-291 (lazy loading Homelab aligné sur `core`, propagation `$CORE_HOME` / `core_home`) — acquis préservé dans l'enveloppe A2A.
- **REF-005** : [Spécification YAML 1.2](https://yaml.org/spec/1.2.2/) — règles de validité de la notation *flow*.
