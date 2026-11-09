# Message A2A du workflow `core` porté par un fichier YAML joint (réduction de prose dans le fil) avec transmission des sensors

---
auteurs: Mika (agent)
accepté par : ""
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

## Date de création

2026-11-09

## Contexte

La communication **agent↔agent (A2A)** du workflow `core` transite aujourd'hui **en prose dans le fil de commentaires de l'issue** : la « Règle A2A » de `core/common/protocols/governance-security.md` et les temps 2-3 de `core/common/protocols/stage-protocol.md` prescrivent une délégation = « commentaire avec mission claire (objectif, périmètre, critères d'acceptation) » et un retour = « commentaire de retour avec résumé du livrable ». Les **résultats de sensors** sont eux aussi postés en prose (section `## Sensors` de `output-format.md`, « Rapport de vérification » de `sensors/gates.md`).

Conséquence observée (ORIG-421) : chaque handoff produit une prose d'orchestration que l'humain doit parcourir alors qu'elle ne lui est pas destinée. L'humain demande que **seuls les éléments décisionnels** restent visibles dans la tâche, les instructions inter-agents étant transmises par fichier.

Le workflow `matching-cv-ao` résout déjà ce problème : mission et livrable voyagent dans un **fichier YAML joint** (« message A2A »), le commentaire étant réduit à la mention active + le nom du fichier ([ADR-0033](0033-format-yaml-compact-message-a2a.md)). Ce modèle n'a jamais été transposé sur `core`. De plus, les agents `core` s'appuient sur des **sensors** dont la liste (à exécuter) et les verdicts (produits) doivent circuler entre agents pour que les contrôles soient effectués — un besoin propre à `core` absent du modèle `matching-cv-ao`.

## Décision

Transposer sur le **seul workflow `core`** le modèle A2A « fichier YAML joint + commentaire minimal » de `matching-cv-ao`, **enrichi de la transmission des sensors**.

- **Deux formes de commentaire, jamais confondues** : handoff A2A pur = mention active + nom du fichier YAML joint, aucune prose ; gate humaine = présentation Markdown détaillée en clair (inchangée).
- **Présentation des sensors au gate humain (obligatoire, non réductible)** : à tout gate de validation humaine, les verdicts de sensors du stage sont **présentés à l'humain en clair** (section `## Sensors`) ; le YAML joint ne s'y substitue jamais. La réduction de prose A2A ne retire rien de ce que l'humain voit au gate. Un gate humain présenté sans les sensors du stage est un écart (SG-2).
- **Enveloppe = YAML compact**, alignée sur le front-matter des fiches de stage et les manifestes de sensors (déjà en YAML).
- **Deux champs sensors ajoutés au schéma** du message A2A :
  - `sensors_a_executer` (délégation) — liste des sensors que l'agent délégataire doit lancer, reprise du champ `sensors:` de la fiche de stage / de la frontière de `gates.md` ;
  - `sensors_resultats` (retour / `rapport-verification`) — verdicts rendus par `sensor.py` (`conforme | ecart | indisponible` + ligne factuelle + source `manifeste @ commit`).
- **Source unique** du schéma : `core/common/protocols/governance-security.md`, § « Schéma du message A2A ». Les fiches de stage, `sensors/gates.md`, `reviewer.md` et les fiches d'agent s'y réfèrent par le nom `message A2A`, sans le redéfinir.
- **Garde-fous reconduits à l'identique** : le lien de mention actif reste le seul vecteur de déclenchement ; mention humaine obligatoire dès qu'une action humaine est requise ; piste d'audit sur l'issue (le YAML joint **est** l'audit) ; verdict de sensor = celui de `sensor.py`, jamais réinterprété ; `indisponible ≠ conforme` ; sensor déclaré mais absent des résultats = écart (silence interdit) ; message A2A **advisory** (ne remplace ni la validation humaine granulaire ni le contrôle sécurité).

## Conséquences

### Positives

- **POS-001** : le fil de la tâche ne porte plus que le décisionnel et les livrables destinés à l'humain — visibilité conforme à la demande (ORIG-423).
- **POS-002** : alignement de `core` sur `matching-cv-ao` — un seul paradigme A2A à maintenir dans le dépôt.
- **POS-003** : économie de tokens par handoff (enveloppe YAML compacte vs prose Markdown reformulée), effet cumulé sur les chaînes longues.
- **POS-004** : les sensors deviennent **transmissibles et exploitables** entre agents — la liste attendue et les verdicts circulent dans l'enveloppe, sans re-dérivation ni perte de traçabilité.
- **POS-005** : invariants de gouvernance et garde-fous sensors (SG-1..6) intacts.

### Négatives

- **NEG-001** : discipline de quoting YAML en notation *flow* (valeurs contenant `${...}`, `:` ou virgule) ; mitigée par « au moindre doute, guillemeter », inscrite dans le schéma source unique.
- **NEG-002** : un agent doit désormais produire un fichier joint à chaque handoff (téléversement `multica attachment`) plutôt qu'un simple commentaire ; coût opératoire marginal, compensé par la lisibilité du fil.
- **NEG-003** : frontière enveloppe ↔ données à tenir — l'enveloppe A2A est YAML ; les artefacts de données qu'elle référence gardent leur format propre.

## Alternatives étudiées

### ALT-001 - Conserver la prose dans le fil et filtrer à l'affichage

Masquer la prose inter-agents côté présentation plutôt que de la déplacer.

**Raison du rejet** : aucun mécanisme de filtrage d'affichage par rôle dans Multica ; la prose resterait dans la piste d'audit et continuerait de coûter des tokens au relecteur suivant.

### ALT-002 - Nouveau format d'enveloppe propre à `core` (JSON ou format maison)

Définir un schéma A2A distinct de celui de `matching-cv-ao`.

**Raison du rejet** : introduirait un second paradigme A2A à maintenir ; le YAML compact est déjà éprouvé (ADR-0033) et aligné sur l'existant du dépôt. Décision humaine explicite : « oui » au YAML compact (ORIG-423).

### ALT-003 - Transmettre les sensors hors de l'enveloppe A2A (fichier séparé)

Un artefact de sensors distinct du message A2A.

**Raison du rejet** : multiplierait les pièces jointes et dissocierait verdicts et mission ; les loger dans l'enveloppe (`sensors_a_executer` / `sensors_resultats`) garde un seul contrat de handoff, auditable d'un bloc.

## Notes d'implémentation

- **IMP-001** : schéma de l'enveloppe A2A (avec `sensors_a_executer` / `sensors_resultats`) défini **une seule fois** dans `core/common/protocols/governance-security.md` (§ « Règle A2A » réécrite + « Deux formes de commentaire » + « Schéma du message A2A »).
- **IMP-002** : fichiers couplés alignés — `core/common/protocols/stage-protocol.md` (temps 2 délégation, temps 3 retour, temps 4 sensors à l'écriture), `core/common/protocols/output-format.md` (§ `## Sensors` réservée au gate humain), `core/sensors/gates.md` (rapport de gate ↔ `rapport-verification`), `core/common/protocols/reviewer.md` (fin de revue ↔ message A2A).
- **IMP-003** : périmètre strictement limité à `core` ; les workflows `homelab` et `matching-cv-ao` ne sont pas touchés par cette décision.
- **IMP-004** : aucun secret dans le YAML ; validité YAML vérifiée (règle de quoting en notation *flow*).
- **IMP-005** : entrée `CHANGELOG.md` (`[Non publié] → Changed`).

## Références

- **REF-001** : [ADR-0033 - Format YAML compact pour l'enveloppe du message A2A](0033-format-yaml-compact-message-a2a.md) — modèle transposé.
- **REF-002** : [ADR-0038 - Workflow core agnostique du harnais](0038-workflow-core-agnostique-du-harnais.md) — no-op tracé si aucun outil de notification.
- **REF-003** : [ADR-0049 - Durcissement exécution sensors, hook par défaut et contrôle compte rendu au gate](0049-durcissement-execution-sensors-hook-par-defaut-et-controle-compte-rendu-au-gate.md) — garde-fous sensors (SG-1..6) reconduits.
- **REF-004** : [Spécification YAML 1.2](https://yaml.org/spec/1.2.2/) — règles de validité de la notation *flow*.
