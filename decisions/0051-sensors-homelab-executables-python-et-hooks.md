# Sensors Homelab exécutables — scripts Python déterministes, sévérité par scope et hooks d'écriture

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

Les sensors du workflow Homelab étaient jusqu'ici des **manifestes déclaratifs** : `command: "non-exécutable (advisory documentaire)"`, aucun script ne les exécutait. Le README `homelab/sensors/` l'assumait (« Ce ne sont pas des scripts exécutables … le passage à l'exécutable est une évolution future »). Les agents devaient donc « simuler » les sensors en prose ou poster `⛔ indisponible` — ni déterministe ni reproductible.

Le workflow `core` a franchi ce pas avec [ADR-0046](0046-sensors-executables-python-et-hooks-agnostiques.md) : dispatcher Python unique, un script par sensor, hook d'écriture agnostique du harnais, gate de phase, le tout **advisory** (code 0). L'humain (HOM-292) demande de **reprendre ce mécanisme pour Homelab**, sur le modèle `core`.

Deux spécificités Homelab doivent être prises en compte, absentes de `core` :

- **Sévérité conditionnelle par scope** (ALI-204, arbitrage 2) : `plaintext-secret` et `terraform-no-sni` sont bloquants sur `security-patch` / `new-stack` (front-matter `severity_overrides`), advisory ailleurs.
- **Gates enrichis** : `homelab/sensors/gates.md` porte des clés absentes de `core` (`blocking_on_scope`, `conditional_on_scope`, `prerequis_40`).

## Décision

**Rendre les six sensors de Homelab exécutables par un dispatcher Python unique, branché sur un hook d'écriture et sur le verification gate, sans changer leur caractère advisory, et en portant nativement la sévérité conditionnelle par scope.**

1. **Dispatcher** `homelab/scripts/sensor.py` (Python standard, aucune dépendance) : `list`, `describe`, `fire <id>`, `gate <frontière>`, `hook`. Chemins ancrés sur `homelab/sensors`.
2. **Un script par sensor** : `homelab/scripts/sensors/<id avec _>.py` (`yaml_validity`, `swarm_deploy_section`, `plaintext_secret`, `terraform_no_sni`, `traefik_coherence`, `vault_secret_exists`), exposant `ID` et `run(ctx)`, appliquant le bloc `checks` du manifeste. Le code partagé vit dans `homelab/scripts/sensorlib/`, dont un **mini-analyseur YAML statique** (`yamlmini.py`) pour `yaml-validity` (pas de dépendance PyYAML — sans équivalent dans `core`). Le champ `command` des manifestes pointe désormais vers `python3 homelab/scripts/sensor.py fire <id>`.
3. **Sévérité conditionnelle par scope** : le dispatcher lit `severity_overrides` des manifestes et résout la sévérité effective via `--scope <scope>` (ou `SENSORS_SCOPE`). La sévérité bloquante est portée par le **rapport et le workflow**, jamais par le code retour (toujours 0 en mode advisory). Les gates enrichis (`blocking_on_scope`, `conditional_on_scope`, `prerequis_40`) sont interprétés par `parse_boundaries()`.
4. **Hook d'écriture** `homelab/sensors/hooks/post_write.py` : lit le JSON du harnais sur stdin, lance les sensors `fire_on: write` dont `matches` correspond, sort **toujours en 0**. Branché par défaut (`hooks.postToolUse`, matcher `fs_write`) sur les **agents producteurs** : Spécialiste Docker (compose) et Spécialiste Terraform (`.tf`/`.tfvars`).
5. **Gate** `sensor.py gate <frontière> [--scope]` : exécute les sensors de la frontière déclarés dans `gates.md` et produit le « Rapport de vérification ». Les artefacts non vérifiables par fichier restent `⛔` tant que le coordinateur ne les atteste pas (`--attest`).
6. **Garde-fous SG-1 à SG-6 appliqués par le code** : manifeste sans `origine` ou `kind` invalide ⇒ `⛔` (SG-1) ; sensor inconnu / périmètre vide / hors périmètre / erreur ⇒ `⛔`, jamais `✅` (SG-2) ; parsing statique seul (SG-4) ; `manifeste @ commit`, commit non traçable ⇒ `⛔` (SG-5). **Aucun sensor n'expose jamais la valeur d'un secret** (`plaintext-secret` : emplacement + clé + type ; `vault-secret-exists` : existence/forme seule).
7. **Advisory inchangé.** Code retour 0 même en écart. `--strict` (code 1) réservé CI. Le passage à bloquant « dur » resterait une décision ADR + contrôle sécurité distincte ; ici le bloquant par scope est déjà décidé (ALI-204) et porté par le rapport.

### Périmètre

- Ajoute `homelab/scripts/` (dispatcher, `sensorlib/`, six sensors, tests) et `homelab/sensors/hooks/` ; met à jour les manifestes (`command`), `homelab/sensors/README.md`, et enregistre le hook sur les fiches des agents producteurs (Spécialiste Docker, Spécialiste Terraform).
- **Hors périmètre** : les workflows `core` et `matching-cv-ao`, la modification des règles / seuils des sensors, le passage à bloquant « dur » hors `severity_overrides` déjà décidés.

## Conséquences

### Positives

- **POS-001** — **Déterminisme** : le même livrable (compose, `.tf`/`.tfvars`) donne le même verdict, sans interprétation d'un agent.
- **POS-002** — **Portabilité** : hook et dispatcher tournent sous Multica comme sous un autre harnais (chemin ancré `$CORE_HOME`).
- **POS-003** — **Pas de faux vert** : une défaillance du sensor est visible (`⛔`), jamais silencieuse (SG-2).
- **POS-004** — **Testable** : `python3 -m unittest discover -s homelab/scripts/tests` (38 tests).
- **POS-005** — **Sévérité par scope native** : le bloquant `security-patch` / `new-stack` est résolu par le code, plus seulement documentaire.

### Négatives / points d'attention

- **NEG-001** — **Contrôles structurels, pas sémantiques** : `yaml-validity` repose sur un analyseur statique **partiel** (sous-ensemble compose), pas un parseur YAML conforme ; `traefik-coherence` fait un contrôle de **surface** (l'autorité reste `traefik-manager-read`) ; `vault-secret-exists` vérifie la **forme** des références (l'existence réelle relève de `homelab-vault-access`, présence seule). Faits de forme.
- **NEG-002** — **Dépendance à Python 3.9+** sur le runtime de l'agent.
- **NEG-003** — **Maintenance double** : toute évolution d'un `checks` de manifeste doit être répercutée dans le script du sensor dans la même PR (SG-1 / SG-6).

## Alternatives étudiées

### ALT-001 — Garder les manifestes déclaratifs

**Non retenue** : c'est l'écart constaté (HOM-292). Les sensors n'étaient ni déterministes ni reproductibles.

### ALT-002 — Dépendre de PyYAML pour `yaml-validity`

**Non retenue** : `core` impose la bibliothèque standard seule (aucune dépendance, SG-4 : environnement minimal) ; un mini-analyseur statique interne suffit au contrôle de forme sans exécuter ni rendre le contenu.

### ALT-003 — Porter l'exécution côté CI uniquement

**Non retenue** : le feedback incrémental à l'écriture (hook) est l'intérêt principal ; `--strict` reste disponible pour un usage CI ultérieur.

## Notes d'implémentation

- Utilisation : `python3 homelab/scripts/sensor.py --root <projet> fire <id> [--path <fichier>...] [--scope <scope>]`.
- Gate : `python3 homelab/scripts/sensor.py --root <projet> gate phase3-phase4 --scope new-stack`.
- Tests : `python3 -m unittest discover -s homelab/scripts/tests`.
- Enregistrement du hook : voir `homelab/sensors/README.md`, section Hooks.
- Exécution d'un sensor seul : `python3 homelab/scripts/sensors/<id>.py --root <projet> [--path <fichier>...]`.

## Références

- Demande d'origine : HOM-292.
- Modèle `core` : [`0046`](0046-sensors-executables-python-et-hooks-agnostiques.md).
- Sensors Homelab : [`0016`](0016-verification-gates-et-sensors-homelab.md), [`0023`](0023-alignement-sensors-homelab-sur-ai-dlc.md) ; agnosticité du harnais : [`0038`](0038-workflow-core-agnostique-du-harnais.md).
- [`homelab/sensors/README.md`](../homelab/sensors/README.md), [`homelab/sensors/gates.md`](../homelab/sensors/gates.md).
