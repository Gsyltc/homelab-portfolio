---
alwaysApply: true
---

This is a monorepo of [Agent Plugins](https://agent-plugins.org) maintained by Sylvain G., compliant with the Agent Plugins Specification v1.0.0.

## Key Directories

- `/plugins`: Agent Plugin packages — each subdirectory is a self-contained plugin
- `/plugins/<name>/plugin.json`: Required manifest (v1.0.0 schema)
- `/plugins/<name>/skills/`: Portable Agent Skills (each skill is an immediate child directory with a `SKILL.md`)
- `/architecture-rules`: Architecture Workflow

## Code Standards

- Plugin manifests (`plugin.json`) must conform to the [Agent Plugins v1.0.0 schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json). The schema is closed — only `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and `extensions` are allowed at the top level.
- Plugin directory names must match the `name` field in their `plugin.json`.
- Plugin names use lowercase alphanumeric characters with hyphens and dots (no consecutive `--` or `..`).
- Skills are immediate child directories of `skills/` and must contain a `SKILL.md` with YAML front matter (`name` and `description` fields).
- MCP server configuration goes in a root-level `mcp.json` per plugin, never inside `plugin.json`.
- Client-specific extensions use reverse-domain namespaces (e.g., `com.vendor.client/`).

## Writing Standards

- Skill instructions in `SKILL.md` should be concise and actionable.
- Use imperative mood in skill descriptions ("Summarize the document" not "Summarizes the document").
- One concern per skill — prefer multiple small skills over one large one.

## Architecture Flow

**TO DEFINE**

## Repository Structure

```
homelab-portfolio/
├── architecture-rules/              # Workflow Documentation (mkdocs/docusaurus compatible)
├── plugins/
│   ├── architecture-assistant/      # Main plugin: Solution architecture skills and agents
│   │   ├── plugin.json
│   │   └── skills/                  # 5 skills (4 openspec + 1 architecture)
│   ├── general-purpose-assistant/   # General purpose plugins
│   |   ├── plugin.json
│   |   └── skills/
│   ├── investment-assistant/        # Investments plugins
│   |   ├── plugin.json
│   |   └── skills/
│   └── medical-assistant/           # Medical plugins
│       ├── plugin.json
│       └── skills/
```
