# homelab-portfolio

Sylvain Goubaud | Director of Expertise in Architecture | Montréal, QC | [LinkedIn](https://www.linkedin.com/in/sylvain-goubaud-47891b5b)

Monorepo de **plugins d'agents** ([Agent Plugins](https://agent-plugins.org), spécification v1.0.0) et de **workflows d'orchestration multi-agents (A2A)** pour la conception d'architecture de solution et l'exploitation d'un homelab de niveau production.

---

## À propos

Ce dépôt documente et outille une infrastructure réelle, prête pour la production — ce n'est pas un tutoriel. Il rassemble :

- des **plugins d'agents** portables (manifestes conformes au schéma v1.0.0) ;
- une **bibliothèque de skills** portées par les plugins, sous [`plugins/<nom>/skills/`](plugins/) ;
- deux **workflows A2A cloisonnés** qui pilotent la façon dont les agents collaborent, tracent leurs décisions et sollicitent une validation humaine.

## Les deux workflows

Le dépôt porte **deux workflows d'orchestration totalement indépendants**. Une demande relève de **l'un ou de l'autre**, jamais des deux ; il n'existe aucune passerelle entre eux (règle de routage complète dans [`AGENTS.md`](AGENTS.md)).

| Workflow | Périmètre | Coordinateur | Source |
| --- | --- | --- | --- |
| **Architecture de solution** | Documentation d'architecture, décisions structurantes, diagrammes (C4 / Archimate / PlantUML / CALM), choix technologiques, intégration, cybersécurité, AWS, cycle spec-driven (OpenSpec) | Architecture Solution & Intégration | [`core/common/conductor.md`](core/common/conductor.md) |
| **Homelab** | Stacks Docker Swarm / Proxmox, `docker-compose`, Terraform, flux n8n, Home Assistant, secrets Vault, routes Traefik | Tech Lead | [`core/workflows/homelab/homelab-workflow.md`](core/workflows/homelab/homelab-workflow.md) |

Le workflow d'architecture est structuré selon le modèle **conductor / stages / protocols** :

- [`core/common/conductor.md`](core/common/conductor.md) — instructions du coordinateur (le *comment*).
- [`core/common/stages/`](core/common/stages/) — une fiche par stage des 5 phases (`Initialization → Ideation → Inception → Construction → Operation`), le *quoi*.
- [`core/common/protocols/`](core/common/protocols/) — mécanismes transverses (définition de stage, protocole d'exécution, gouvernance & sécurité, revue, scopes & axes).
- [`core/rules/`](core/rules/) — mémoire de règles multi-couches (boucle d'apprentissage).
- [`core/sensors/`](core/sensors/) — manifestes des verification gates & sensors.
- [`core/agents/`](core/agents/) — définitions versionnées des agents du workflow (coordinateur, architectes, cybersécurité, reviewers de cohérence et de sécurité, OpenSpec, archivage, notifications, vente).

## Structure du dépôt

```
homelab-portfolio/
├── AGENTS.md                 # Standards du dépôt + règle de routage entre les deux workflows
├── README.md
├── CONTRIBUTING.md           # Comment contribuer
├── CODE_OF_CONDUCT.md        # Code de conduite de la communauté
├── LICENCE                   # MIT
├── core/                     # Workflow d'architecture + ressources partagées
│   ├── common/               #   conductor.md + stages/ + protocols/
│   ├── rules/                #   Règles persistantes multi-couches
│   ├── sensors/              #   Verification gates & sensors (advisory)
│   ├── agents/               #   Définitions des agents du workflow (11 fichiers .md)
│   └── workflows/homelab/    #   Workflow Homelab narratif (+ VERSION)
├── decisions/                # Registre des décisions structurantes (0001…0008)
├── docs/                     # Stub de redirection core-workflow + doc générale
└── plugins/                  # Packages de plugins d'agents (spec v1.0.0) — portent les skills
    ├── architecture-assistant/    #   OpenSpec, décision, gabarits, cybersécurité, AWS, Windows, supports de vente
    ├── general-purpose-assistant/ #   workflow de stack, notifications
    ├── homelab-assistant/         #   docker-composer, traefik
    ├── investment-assistant/      #   analyse, data provider, liste de titres
    └── medical-assistant/         #   dossiers médicaux
```

## Skills

Les skills sont **portées par les plugins**, à l'emplacement canonique [`plugins/<nom>/skills/<skill>/SKILL.md`](plugins/) (conforme à la spécification Agent Plugins v1.0.0). Chaque skill est un répertoire contenant un `SKILL.md` avec un front-matter YAML (`name` + `description`).

> **Important** — sur Multica, un `SKILL.md` présent dans le dépôt n'est **pas** utilisé automatiquement. Une skill devient utilisable après avoir été **importée** dans le workspace (`multica skill import`) puis **assignée** à un agent (`multica agent skills add|set`). Voir [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Plugins

Chaque sous-répertoire de [`plugins/`](plugins/) est un plugin auto-contenu, avec un manifeste `plugin.json` conforme au [schéma Agent Plugins v1.0.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) et ses skills sous `skills/`.

| Plugin | Rôle |
| --- | --- |
| `architecture-assistant` | Architecture de solution : OpenSpec, décision, gabarits DAS, cybersécurité, AWS, Windows, supports de vente |
| `general-purpose-assistant` | Skills transverses (workflow de stack, notifications) |
| `homelab-assistant` | Homelab : `docker-compose`, Traefik |
| `investment-assistant` | Domaine investissement |
| `medical-assistant` | Domaine médical |

## Décisions structurantes

Les décisions d'architecture sont tracées dans [`decisions/`](decisions/) (format court, numéroté). Toute décision structurante fait l'objet d'un enregistrement, conformément aux invariants des workflows.

## Contribuer

Lire [`CONTRIBUTING.md`](CONTRIBUTING.md) avant d'ouvrir une *pull request*, et respecter le [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Licence

Distribué sous licence **MIT** — voir [`LICENCE`](LICENCE).
