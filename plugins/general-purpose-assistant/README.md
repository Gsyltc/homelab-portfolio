# general-purpose-assistant

Plugin conforme à **Agent Plugins v1.0.0** regroupant les skills **transverses**
de l'espace de travail — celles qui ne sont rattachées à aucun domaine métier
précis et sont **mutualisées** entre les agents : notifications push, génération
des guides d'utilisation des workflows et création/validation d'Agent Skills.

## Structure (Agent Plugins v1.0.0)

```text
plugins/general-purpose-assistant/
├── plugin.json          # manifeste racine ($schema + name, schéma fermé)
├── mcp.json             # config MCP (mcpServers vide — voir « MCP » ci-dessous)
├── CHANGELOG.md
├── README.md
└── skills/
    ├── guide-utilisation-workflow-generation/   # SKILL.md + assets/
    ├── ntfy-notifications/                       # SKILL.md
    └── skill-authoring/                          # SKILL.md
```

Chaque dossier immédiat sous `skills/` contient un `SKILL.md` conforme à la
spécification [Agent Skills](https://agentskills.io/specification) (frontmatter
`name` + `description`, puis corps Markdown). Le champ `name` du frontmatter
correspond au nom du dossier. La conformité est vérifiée par le validateur
officiel `skills-ref` — `scripts/validate_skills.sh` à la racine du dépôt,
également exécuté par le hook `pre-commit` et la CI GitHub Actions.

## Skills exportés (mapping)

| Skill | Fonction (rôle utilisateur) | Contenu annexe |
|---|---|---|
| `ntfy-notifications` | Agent de notifications (partagé `core/`) — envoi de notifications push via ntfy pour tout évènement à partager avec l'humain | — |
| `guide-utilisation-workflow-generation` | Rédaction documentaire — production et mise à jour des guides d'utilisation des workflows (`core`, `homelab`, `matching-cv-ao`) au format PDF (trame éditoriale, conventions de diagrammes, charte graphique, gabarit HTML, régénération WeasyPrint) | `assets/` (gabarit HTML du guide) |
| `skill-authoring` | Auteur de skills — création, modification et validation d'une Agent Skill conforme à agentskills.io (frontmatter autorisé, contraintes de nom/description, organisation `scripts/`/`references/`/`assets/`, validation via le validateur officiel `skills-ref` ; mise à jour obligatoire du README et du CHANGELOG à chaque ajout/modification/retrait de skill) | — |

La skill de notifications `ntfy-notifications` est **mutualisée** : son porteur
est l'Agent de notifications, dont la définition est partagée (`core/`). C'est
ce plugin qui l'héberge ; elle n'est **pas** dupliquée dans les autres plugins
(voir le README et le CHANGELOG de `homelab-assistant`).

## MCP

`mcp.json` déclare un objet `mcpServers` **vide** (`{}`), ce qui est valide
selon la spec v1.0.0 (§7.2.1) : aucune de ces skills transverses ne dépend d'un
serveur MCP. Si un serveur MCP transverse est confirmé ultérieurement, il devra
être ajouté à `mcp.json` au format v1.0.0 (`stdio` / `streamable-http` / `sse`),
en **externalisant tout secret** (aucun token ni credential dans `headers`/`env`,
la spec l'interdit — §7.2.1 / §9.2).

## Sécurité (dépôt public)

- Aucun secret en clair n'est committé. La skill `ntfy-notifications` référence
  les paramètres d'accès ntfy via des variables d'environnement documentées
  (`NTFY_URL`, `NTFY_CHANNEL`, `NTFY_USER`, `NTFY_PASSWORD`), jamais leurs
  valeurs ; le mot de passe n'est jamais affiché ni loggé en clair.
- Les skills de ce plugin décrivent des **mécaniques** (envoi de notifications,
  génération de guides, création de skills) et n'embarquent aucune donnée
  sensible.
