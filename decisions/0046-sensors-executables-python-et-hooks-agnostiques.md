# Sensors exécutables — scripts Python déterministes, hooks d'écriture et gate agnostiques du harnais

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

2026-11-06

## Contexte

Les sensors du workflow `core` sont aujourd'hui des **manifestes déclaratifs** : `command: "non-exécutable (advisory documentaire)"`. Aucun script ne les exécute. Les agents doivent donc les « simuler » en prose, ou poster `⛔ indisponible`. Le résultat n'est ni déterministe ni reproductible.

Le workflow amont AWS AI-DLC (`awslabs/aidlc-workflows`, `core/sensors/`, `core/hooks/`, `scripts/`) fonctionne autrement. Chaque sensor a un manifeste (`command`, `fire_on`, `matches`) **et** un exécutable. Un hook `PostToolUse` sur `Write|Edit` lance les sensors `fire_on: write`. Le gate de phase lance les sensors `fire_on: gate`. Un sensor défaillant produit un état distinct (`COULD_NOT_RUN`), jamais un vert. Le tout est advisory : le dispatcher sort en 0.

L'humain (HOM-283) demande de reprendre ce mécanisme pour `core`, avec des scripts **Python** (pas TypeScript).

## Décision

**Rendre les huit sensors de `core` exécutables par un dispatcher Python unique, branché sur un hook d'écriture et sur le verification gate, sans changer leur caractère advisory.**

1. **Dispatcher** `core/scripts/sensor.py` (Python standard, aucune dépendance) : `list`, `describe`, `fire <id>`, `gate <frontière>`, `hook`.
2. **Un script par sensor** : `core/scripts/sensors/<id avec _>.py` (ex. `required_sections.py`), qui expose `ID` et `run(ctx)` et applique le bloc `checks` du manifeste. Chaque script s'exécute seul. Le code partagé vit dans `core/scripts/sensorlib/`. Un manifeste sans script, ou un script sans manifeste, est une erreur (test dédié) ; à l'exécution, un script absent donne `⛔`. Le champ `command` des manifestes pointe désormais vers `python3 core/scripts/sensor.py fire <id>`.
3. **Hook d'écriture** `core/sensors/hooks/post_write.py` : lit le JSON du harnais sur stdin, lance les sensors `fire_on: write` dont `matches` correspond, sort **toujours en 0**. Il s'enregistre sur Claude Code, Kiro CLI ou tout harnais fournissant `tool_input.file_path`.
4. **Gate** `sensor.py gate <frontière>` : exécute les sensors de la frontière déclarés dans `gates.md` et produit le « Rapport de vérification ». Les artefacts non vérifiables par fichier restent `⛔` tant que le coordinateur ne les atteste pas (`--attest`).
5. **Garde-fous SG-1 à SG-6 appliqués par le code** :
   - manifeste sans `origine` ou `kind` invalide ⇒ `⛔` (SG-1) ;
   - sensor inconnu, périmètre vide, hors périmètre, erreur d'exécution ⇒ `⛔`, jamais `✅` (SG-2) ;
   - parsing statique seul : aucun rendu, aucun réseau, aucune exécution de directive ; une inclusion distante est signalée, pas suivie (SG-4) ;
   - chaque rapport porte `manifeste @ commit` ; commit non traçable ⇒ `⛔` (SG-5).
6. **Advisory inchangé.** Le code retour est 0 même en écart. `--strict` (code 1) est réservé à un usage CI ; le rendre bloquant dans le workflow reste une décision ADR + contrôle sécurité.

### Périmètre

- Ajoute `core/scripts/` (dispatcher et contrôles) et `core/sensors/hooks/`, met à jour les manifestes (`command`), `README.md` et `gates.md` de `core/sensors/`, ainsi que les temps 4 et 5 de `stage-protocol` et la section Sensors de `output-format`.
- **Hors périmètre** : les sensors `linter` et `type-check` de l'amont (pas de code produit par `core`), la modification des seuils ou des règles des sensors, le passage à bloquant, les workflows `homelab` et `matching-cv-ao`.

## Conséquences

### Positives

- **POS-001** — **Déterminisme** : le même artefact donne le même verdict, sans interprétation d'un agent.
- **POS-002** — **Portabilité** : le hook et le dispatcher tournent sous Multica comme sous un autre harnais (ADR-0038).
- **POS-003** — **Pas de faux vert** : une défaillance du sensor est visible (`⛔`), pas silencieuse.
- **POS-004** — **Testable** : tests unitaires `unittest` sous `core/scripts/tests/`.

### Négatives / points d'attention

- **NEG-001** — **Contrôles structurels, pas sémantiques** : `diagram-validity` vérifie la structure (type, délimiteurs, parenthésage), pas un rendu réel. `claim-sources` et `traceability` reposent sur des motifs (`BA-…`, `FR-…`, `ALI-…`). Les résultats restent des faits de forme.
- **NEG-002** — **Écarts hérités révélés** : les ADR antérieurs à `Date de création` ressortent en `⚠️`. C'est un constat, pas une régression.
- **NEG-003** — **Dépendance à Python 3.9+** sur le poste ou le runtime de l'agent.
- **NEG-004** — **Maintenance double** : toute évolution d'un `checks` de manifeste doit être répercutée dans le script du sensor dans la même PR (SG-1 / SG-6).

## Alternatives étudiées

### ALT-001 — Porter les scripts TypeScript de l'amont

**Non retenue** : l'humain demande Python, et `core` n'embarque pas de runtime Bun.

### ALT-002 — Garder les manifestes déclaratifs

**Non retenue** : c'est l'écart constaté. Les sensors ne sont ni déterministes ni reproductibles.

### ALT-003 — Rendre les sensors bloquants

**Non retenue** : décision structurante distincte (ADR + contrôle sécurité). Le gate humain reste le seul bloquant.

## Notes d'implémentation

- Utilisation : `python3 core/scripts/sensor.py --root <projet> fire <id> [--path <fichier>...]`.
- Gate : `python3 core/scripts/sensor.py --root <projet> gate construction-operation --attest coherence_doc_adr`.
- Tests : `python3 -m unittest discover -s core/scripts/tests`.
- Enregistrement du hook : voir `core/sensors/README.md`, section Hooks.
- Exécution d'un sensor seul : `python3 core/scripts/sensors/<id>.py --root <projet> [--path <fichier>...]`.

## Références

- Demande d'origine : HOM-283.
- Amont : `awslabs/aidlc-workflows` (`core/sensors/`, `core/hooks/aidlc-run-sensors.ts`, `core/tools/aidlc-sensor.ts`).
- [`0005`](0005-verification-gates-et-sensors.md), [`0012`](0012-alignement-sensors-sur-ai-dlc.md), [`0038`](0038-workflow-core-agnostique-du-harnais.md), [`0045`](0045-checklist-architecture-sections-requises-securite.md).
- [`core/sensors/README.md`](../core/sensors/README.md), [`core/sensors/gates.md`](../core/sensors/gates.md).
