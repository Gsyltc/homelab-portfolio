# Contribuer à homelab-portfolio

Merci de votre intérêt pour ce dépôt. Il rassemble des **plugins d'agents** (spécification [Agent Plugins v1.0.0](https://agent-plugins.org)), une **bibliothèque de skills** et deux **workflows d'orchestration multi-agents (A2A)**. Ce guide décrit comment proposer une contribution cohérente avec ces standards.

Avant toute contribution, lisez également [`AGENTS.md`](AGENTS.md) (standards du dépôt et règle de routage) et le [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Prérequis

- **Git** et un compte GitHub.
- Un éditeur avec support Markdown et YAML.
- Pour valider un manifeste de plugin : un validateur JSON Schema (schéma de référence : [`plugin.schema.json` v1.0.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)).
- Pour les diagrammes : les rendre **en code** (Mermaid, PlantUML, Structurizr DSL, CALM, Archimate) et valider leur syntaxe avant de committer.

## Flux de contribution

1. **Forkez** le dépôt et créez une branche depuis `main` :
   `git checkout -b <type>/<description-courte>` (ex. `docs/mise-a-jour-readme`, `feat/skill-x`).
2. Faites des **commits atomiques** avec des messages clairs, au format [Conventional Commits](https://www.conventionalcommits.org/) : `type(scope): résumé` (types courants : `feat`, `fix`, `docs`, `refactor`, `chore`).
3. **Vérifiez** votre changement (voir « Checklist » plus bas).
4. Ouvrez une **pull request** vers `main` avec un titre concis (< 70 caractères) et une description qui explique le *quoi*, le *pourquoi* et ce qui a été testé.
5. La PR est **relue** ; un contrôle de cohérence (et un contrôle sécurité si l'architecture est touchée) peut être demandé avant fusion.

> Ne poussez jamais directement sur `main`. Toute modification passe par une pull request.

## Types de contributions

### Skills

Les skills sont **portées par les plugins**, à l'emplacement canonique [`plugins/<nom>/skills/<skill>/SKILL.md`](plugins/) (spécification Agent Plugins v1.0.0). Chaque skill :

- est un répertoire contenant un `SKILL.md` avec un **front-matter YAML** (`name` et `description` obligatoires) ;
- porte un `name` en minuscules alphanumériques avec tirets (cohérent avec le nom du répertoire) ;
- décrit une **seule préoccupation** — préférez plusieurs petits skills à un gros ;
- utilise l'**impératif** dans sa description (« Résume le document », pas « Résumé du document »).

> **Utilisation sur Multica** — déposer un `SKILL.md` dans le dépôt **ne suffit pas** : la plateforme ne le découvre pas automatiquement. Une skill devient utilisable seulement après avoir été **importée** dans le workspace, puis **assignée** à un agent :
>
> ```
> multica skill import <url-ou-archive>        # enregistre la skill dans le workspace
> multica skill list                            # vérifie l'enregistrement
> multica agent skills add <agent> <skill…>     # rend la skill utilisable par l'agent
> ```
>
> Après un changement de skill, réimportez/rafraîchissez (`multica skill refresh`) et vérifiez l'assignation ; les agents chargent leurs skills au démarrage de session.

### Plugins

- Chaque plugin est un sous-répertoire auto-contenu de [`plugins/`](plugins/) avec un `plugin.json` **conforme au schéma v1.0.0** (schéma fermé : seuls `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `extensions` sont autorisés au niveau racine).
- Le **nom du répertoire du plugin doit correspondre** au champ `name` de son `plugin.json`.
- Les noms de plugins utilisent des minuscules alphanumériques avec tirets et points (pas de `--` ni `..` consécutifs).
- La configuration d'un serveur MCP va dans un `mcp.json` racine par plugin, **jamais** dans `plugin.json`.
- Les extensions spécifiques à un client utilisent un namespace *reverse-domain* (ex. `com.vendor.client/`).

### Workflows A2A

Le dépôt porte **deux workflows cloisonnés** (voir la règle de routage dans [`AGENTS.md`](AGENTS.md)) :

- **Architecture de solution** → [`core/common/conductor.md`](core/common/conductor.md) + [`core/common/stages/`](core/common/stages/) + [`core/common/protocols/`](core/common/protocols/).
- **Homelab** → [`homelab/common/conductor.md`](homelab/common/conductor.md) + [`homelab/common/stages/`](homelab/common/stages/) + [`homelab/common/protocols/`](homelab/common/protocols/).

Toute évolution d'un workflow doit :

- respecter les **invariants** communs (coordination sur l'issue, délégation A2A par mention valide, validation humaine granulaire, chargement de contexte optimisé, aucun secret dans les livrables) ;
- rester **agnostique de la méthodologie** (OpenSpec/BMAD restent conditionnels) ;
- ne **jamais créer de passerelle** entre les deux workflows ;
- pour une fiche de stage, porter un **front-matter conforme** à [`core/common/protocols/stage-definition.md`](core/common/protocols/stage-definition.md).

### Décisions structurantes

Toute décision d'architecture significative est tracée dans [`decisions/`](decisions/) sous forme d'un enregistrement court et numéroté (`NNNN-titre-court.md`), en cohérence avec les enregistrements existants (`0001`…`0012`). Ne modifiez pas rétroactivement un enregistrement accepté : ajoutez-en un nouveau qui le supersède si besoin.

### Documentation

- Rédigez en **français par défaut**, sauf termes techniques non traduits.
- Vérifiez que les **liens relatifs** ne sont pas cassés.
- Ne committez **aucun secret** (mot de passe, jeton, identifiant) — ni dans le code, ni dans la documentation, ni dans les exemples.

## Checklist avant d'ouvrir une PR

- [ ] La branche part de `main` à jour ; la PR cible `main`.
- [ ] Commits au format Conventional Commits.
- [ ] `plugin.json` valide contre le schéma v1.0.0 (si un plugin est touché).
- [ ] Nom de répertoire de plugin = champ `name`.
- [ ] Skills : `SKILL.md` présent avec front-matter `name` + `description` valide.
- [ ] Diagrammes rendus en code et **syntaxe validée**.
- [ ] Aucun lien relatif cassé ; aucun secret introduit.
- [ ] Décision structurante ajoutée dans `decisions/` si le changement en est une.
- [ ] Description de PR : quoi / pourquoi / vérifications effectuées.

## Signaler un bug ou proposer une évolution

Ouvrez une **issue** décrivant le contexte, le comportement observé et le comportement attendu. Pour une faille de sécurité, ne l'exposez pas publiquement : contactez le mainteneur (**Sylvain Goubaud**, [LinkedIn](https://www.linkedin.com/in/sylvain-goubaud-47891b5b)) ou ouvrez une issue confidentielle.

## Licence

En contribuant, vous acceptez que vos contributions soient distribuées sous la licence **MIT** du dépôt (voir [`LICENCE`](LICENCE)).
