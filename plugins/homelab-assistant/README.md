# homelab-assistant

Plugin conforme à **Agent Plugins v1.0.0** regroupant les skills DevOps/Homelab
de l'espace de travail. Il permet à un agent d'accompagner les tâches courantes
du homelab : configuration de stacks (Terraform), génération de
`docker-compose.yml`, validation de Dockerfile (stacks *build-from-source*),
accès aux secrets Vault et lecture de l'état Traefik.

La skill de notifications `ntfy-notifications` est **mutualisée** et n'appartient
pas à ce plugin : elle est conservée dans le plugin `general-purpose-assistant`
(voir CHANGELOG).

## Structure (Agent Plugins v1.0.0)

```text
plugins/homelab-assistant/
├── plugin.json          # manifeste racine ($schema + name, schéma fermé)
├── mcp.json             # config MCP (mcpServers vide — voir « MCP » ci-dessous)
├── CHANGELOG.md
├── README.md
└── skills/
    ├── configuration-applications/   # SKILL.md + references/
    ├── docker-composer/              # SKILL.md + references/
    ├── dockerfile-validator/         # SKILL.md + scripts/ + references/ + examples/ + tests/
    ├── homelab-vault-access/         # SKILL.md
    └── traefik-manager-read/         # SKILL.md
```

Chaque dossier immédiat sous `skills/` contient un `SKILL.md` conforme à la
spécification [Agent Skills](https://agentskills.io/specification) (frontmatter
`name` + `description`, puis corps Markdown). Le champ `name` du frontmatter
correspond au nom du dossier.

## Skills exportés (mapping)

| Skill | Fonction (rôle utilisateur) | Contenu annexe |
|---|---|---|
| `configuration-applications` | Spécialiste Terraform — configuration des stacks (`.tf`/`.tfvars`) | `references/` (authentification, criticités Kuma, domaines, template) |
| `docker-composer` | Spécialiste Docker / QA Docker — génération de `docker-compose.yml` | `references/` (network, template) |
| `dockerfile-validator` | QA Docker — lint/audit/scan de Dockerfile (stacks *build-from-source* uniquement) | `scripts/`, `references/`, `examples/`, `tests/` |
| `homelab-vault-access` | Spécialiste Docker / QA Docker / Spécialiste Terraform — accès Vault (AppRole) | — |
| `traefik-manager-read` | Spécialiste Docker / QA Docker / Architecte sécurité — lecture Traefik Manager | — |

La skill de notifications (`ntfy-notifications`) est **mutualisée** : son porteur
est l'Agent de notifications, dont la définition est partagée (`core/`). Elle
reste dans le plugin `general-purpose-assistant` et n'est **pas** dupliquée ici.

Les skills non-homelab de l'espace de travail (les 4 skills `investissement-*`
de l'équipe finance et les skills `kestra-*` externes) sont **exclus** de ce
plugin ; les skills `investissement-*` disposent de leur propre plugin
`investment-assistant`.

## MCP

`mcp.json` déclare un objet `mcpServers` **vide** (`{}`), ce qui est valide
selon la spec v1.0.0 (§7.2.1). Aucun serveur MCP spécifique au homelab n'a pu
être confirmé au moment de l'export :

- Les agents Homelab (Tech Lead, Expert Home Assistant, Expert n8n) ont un
  `mcp_config` `null` et aucun serveur MCP d'espace de travail assigné
  (`multica agent mcp list <id>` renvoie une liste vide).
- Aucune configuration MCP non-redacted n'était donc disponible à traduire.

Si des serveurs MCP homelab sont confirmés ultérieurement, ils devront être
ajoutés à `mcp.json` au format v1.0.0 (`stdio` / `streamable-http` / `sse`), en
**externalisant tout secret** (aucun token ni credential dans `headers`/`env`,
la spec l'interdit — §7.2.1 / §9.2).

## Sécurité (dépôt public)

- Aucun secret en clair n'est committé. Tous les identifiants sont référencés
  via des variables d'environnement documentées, jamais leurs valeurs :
  - `homelab-vault-access` : `VAULT_ADDR`, `VAULT_APPROLE_ROLE_ID`,
    `VAULT_APPROLE_SECRET_ID` (jamais de `role_id`/`secret_id` en clair).
  - `traefik-manager-read` : `TRAEFIK_MANAGER_URL`, `TRAEFIK_MANAGER_API_KEY`.
- Les occurrences de `password` / `secret` présentes dans
  `dockerfile-validator` sont des **exemples pédagogiques** (Dockerfiles
  volontairement mauvais) et la logique du script de détection de secrets ;
  ce ne sont pas de vrais secrets.
- Le domaine `jeedom-gaston.ovh` est le domaine public du propriétaire, déjà
  présent ailleurs dans ce dépôt ; il n'est pas traité comme un secret.
