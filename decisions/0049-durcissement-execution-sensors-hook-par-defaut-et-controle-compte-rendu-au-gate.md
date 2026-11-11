---
auteurs: Sylvain Goubaud
parties_prenantes: ""
accepte_par: Sylvain Goubaud
accepte_le: ""
supersedes: ""
superseded_by: ""
---

# Durcissement de l'exécution des sensors — hook d'écriture par défaut et contrôle du compte rendu au gate

## Status

Proposed

<!-- Provenance (SG-1) : origine ORIG-418 (durcissement de l'exécution des sensors). -->

## Date de création

2026-11-08

## Contexte

Le mécanisme de sensors du workflow `core` ([ADR-0046](0046-sensors-executables-python-et-hooks-agnostiques.md)) repose, sous Multica, sur l'**auto-discipline de l'agent auteur** au temps 4 du `stage-protocol` : c'est lui qui lance `fire` et poste la section `## Sensors`. Deux fragilités d'exécution subsistent :

1. **Hook d'écriture non branché.** Le hook `core/sensors/hooks/post_write.py` existe et sort toujours en 0 (advisory), mais aucune fiche d'agent ne le déclare. Rien ne déclenche donc les sensors `fire_on: write` automatiquement : le signal dépend entièrement de la discipline manuelle.
2. **`⛔ indisponible` silencieux.** La clause SG-2 (« indisponible ≠ conforme », « silence = écart ») ne produit un verdict `⛔` **que** si quelqu'un exécute le sensor. Tant que le lancement dépend d'un agent qui peut l'omettre, l'écart reste invisible : un compte rendu « aucun sensor déclaré » passe le gate sans signal.

Un écart concret a révélé ces deux points : un livrable de production (documents de la DAS) a été rendu avec « aucun sensor déclaré » alors que le stage de production déclare un champ `sensors:` non vide ; l'exécution manuelle a ensuite fait ressortir plusieurs écarts advisory (style, hypothèses non confirmées, absence de référence amont). Le workflow **couvrait déjà** le cas (checklist de sortie de stage, SG-2) : il s'agit d'une **exécution défaillante**, pas d'un trou de conception.

## Décision

Ajouter **deux durcissements d'exécution**, qui transforment l'obligation « sur l'honneur » en garantie déterministe **sans rendre aucun sensor bloquant** :

1. **Hook d'écriture branché par défaut sur les agents de production.** Les fiches des **sept agents qui produisent des livrables** (Architecte de solution, Architecte AWS, Architecte Azure, Architecte de données, Infrastructure Windows, Architecte Cybersécurité, OpenSpec Expert) déclarent le hook `core/sensors/hooks/post_write.py` en front-matter (`hooks.postToolUse`, matcher `fs_write`). Les sensors `fire_on: write` se déclenchent alors à chaque écriture, indépendamment de la discipline manuelle au temps 4. Le hook reste **agnostique du harnais** (forme Claude Code `PostToolUse` / `Write|Edit` documentée dans `core/sensors/README.md`).
2. **Contrôle du compte rendu au gate (temps 5).** Une capacité `report-check` du dispatcher `core/scripts/sensor.py` constate l'**absence de section `## Sensors` renseignée** dans le compte rendu alors que la **fiche de stage active déclare un champ `sensors:` non vide**, et la signale comme **écart advisory** (`⚠️`). Le coordinateur l'exécute avant la validation humaine et propose de faire rejouer le temps 4. Une fiche à `sensors: []` (ou sans champ) rend l'absence de section légitime (`✅`) ; une fiche introuvable donne `⛔` (SG-2).

### Périmètre

- **Inclus** : champ `hooks:` sur les sept fiches de production ; sous-commande `report-check` (+ helpers `stage_sensors`, `report_has_sensors_section`, `check_report`) ; intégration au temps 5 du `stage-protocol` ; documentation de périmètre dans `core/agents/README.md` et `core/sensors/README.md` ; tests unitaires.
- **Hors périmètre** : le coordinateur, les reviewers (review-only), Vente & Appels d'Offres et Présentation client (supports hors périmètre `matches`), les utilitaires (archivage, notifications) — aucun ne reçoit le hook. Le passage d'un check en **bloquant** reste une décision structurante distincte.

## Conséquences

### Positives

- **POS-001** : les sensors `fire_on: write` se déclenchent automatiquement à l'écriture des livrables, sans dépendre d'un lancement manuel oubliable.
- **POS-002** : un compte rendu omettant la section `## Sensors` alors que le stage en déclare devient un écart **visible** au gate (SG-2 effectif même sans `fire` lancé).
- **POS-003** : le contrôle est déterministe, testé, à provenance tracée (`sensor.py report-check @ commit`).
- **POS-004** : périmètre explicitement documenté — aucune ambiguïté sur les agents concernés.

### Négatives

- **NEG-001** : le contrôle au gate constate la **présence de la section**, pas l'exactitude de son contenu ; un compte rendu renseigné à tort reste à la charge du jugement humain.
- **NEG-002** : la liaison hook ↔ harnais dépend de la lecture du champ `hooks:` par le runtime ; un harnais qui ne le lit pas ne bénéficie pas du filet (le lancement manuel au temps 4 reste la source de vérité).
- **NEG-003** : une évolution du champ `sensors:` d'une fiche de stage doit rester cohérente avec le contrôle `report-check` (couverture par les tests).

## Alternatives étudiées

### ALT-001 — Rendre un sensor ou le contrôle bloquant

Faire échouer le gate en l'absence de section `## Sensors`.

**Raison du rejet** : rendre un check bloquant est une décision structurante dédiée (ADR + contrôle sécurité, SG-3). Le gate humain reste le seul décideur contraignant ; tout reste advisory par défaut.

### ALT-002 — Brancher le hook sur tous les agents

Déclarer le hook sur l'ensemble des fiches, y compris coordinateur, reviewers et utilitaires.

**Raison du rejet** : ces agents n'écrivent pas de livrables matchés par les sensors `fire_on: write` ; le hook y serait du bruit sans valeur, et brouillerait la séparation des rôles (un reviewer ne produit pas).

### ALT-003 — S'en tenir à la discipline manuelle

Laisser le temps 4 reposer sur l'agent auteur, sans filet.

**Raison du rejet** : c'est précisément la fragilité constatée. Le silence restait un faux conforme.

## Notes d'implémentation

- **IMP-001** : contrôle de gate — `python3 core/scripts/sensor.py report-check --stage <fiche-de-stage> --report-file <compte-rendu>` (compte rendu sur stdin si `--report-file` absent) ; `--format json` pour une sortie exploitable ; `--strict` (code 1) réservé à la CI, le défaut reste code 0.
- **IMP-002** : hook — champ `hooks.postToolUse` `{ matcher: fs_write, command: "python3 core/sensors/hooks/post_write.py" }` ; équivalent Claude Code documenté dans `core/sensors/README.md` (§ Hooks).
- **IMP-003** : tests — `python3 -m unittest discover -s core/scripts/tests` (classe `ReportCheckTests`) ; advisory vérifié (code 0 même en écart), `--strict` vérifié (code 1).

## Références

- **REF-001** : [ADR-0046 - Sensors exécutables — scripts Python déterministes, hooks d'écriture et gate agnostiques du harnais](0046-sensors-executables-python-et-hooks-agnostiques.md)
- **REF-002** : [ADR-0038 - Workflow `core` agnostique du harnais](0038-workflow-core-agnostique-du-harnais.md)
- **REF-003** : [ADR-0005 - Verification gates et sensors](0005-verification-gates-et-sensors.md)
- **REF-004** : [core/sensors/README.md](../core/sensors/README.md)
- **REF-005** : [core/common/protocols/stage-protocol.md](../core/common/protocols/stage-protocol.md)
