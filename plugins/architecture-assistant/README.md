# architecture-assistant

Plugin conforme à **Agent Plugins v1.0.0** regroupant les skills d'**architecture
de solution** et d'**architecture de données** de l'espace de travail : cycle
spec-driven OpenSpec (SDD), décisions d'architecture (ADR), cybersécurité,
architectures cloud (AWS, Azure), infrastructure Windows, modélisation et
exploitation d'entrepôt de données, ingénierie analytique, ainsi que la
production de présentations client et de supports de vente.

## Structure (Agent Plugins v1.0.0)

```text
plugins/architecture-assistant/
├── plugin.json          # manifeste racine ($schema + name, schéma fermé)
├── mcp.json             # config MCP (mcpServers vide — voir « MCP » ci-dessous)
├── CHANGELOG.md
├── README.md
└── skills/
    ├── analytics-engineer/                    # SKILL.md + references/
    ├── architecture-securite-gabarits/        # SKILL.md + gabarits/ + revue/
    ├── architecture-solution-gabarits/        # SKILL.md + gabarits/ + patron-architecture/
    ├── aws-solution-architect/                # SKILL.md + assets/ + references/ + scripts/
    ├── azure-solution-architect/              # SKILL.md + assets/ + references/ + scripts/
    ├── cdae-ai-eligibilite/                   # SKILL.md
    ├── client-presentation-generation/        # SKILL.md + gabarits/ + instructions/ + references/
    ├── create-architecture-decision-record/   # SKILL.md
    ├── cybersecurite/                         # SKILL.md + principles/
    ├── data-warehouse-ops/                    # SKILL.md + assets/ + references/ + scripts/
    ├── git-delivery/                          # SKILL.md
    ├── openspec-archiving/                     # SKILL.md
    ├── openspec-context-loading/               # SKILL.md
    ├── openspec-implementation/                # SKILL.md
    ├── openspec-proposal-creation/             # SKILL.md + references/ + templates/
    ├── openspec-workflow/                      # SKILL.md
    ├── presentation-targeting/                 # SKILL.md
    ├── project-defaults/                       # SKILL.md + references/ + scripts/
    ├── sales-deck-generation/                  # SKILL.md
    └── windows-infrastructure-administration/  # SKILL.md
```

Chaque dossier immédiat sous `skills/` contient un `SKILL.md` conforme à la
spécification [Agent Skills](https://agentskills.io/specification) (frontmatter
`name` + `description`, puis corps Markdown). Le champ `name` du frontmatter
correspond au nom du dossier. La conformité est vérifiée par le validateur
officiel `skills-ref` — `scripts/validate_skills.sh` à la racine du dépôt,
également exécuté par le hook `pre-commit` et la CI GitHub Actions.

## Skills exportés (mapping)

### Architecture de solution

| Skill | Fonction (rôle utilisateur) | Contenu annexe |
|---|---|---|
| `architecture-solution-gabarits` | Architecte de solution — gabarits de DAS (découpée par thème) + catalogue de 45 patrons d'architecture cloud | `gabarits/`, `patron-architecture/` |
| `create-architecture-decision-record` | Architecte de solution — rédaction d'un ADR (décision optimisée pour l'IA) | — |
| `aws-solution-architect` | Architecte AWS — conception d'architectures serverless, templates CloudFormation, optimisation des coûts, CI/CD, migration | `assets/`, `references/`, `scripts/` |
| `azure-solution-architect` | Architecte Azure — conception serverless, templates Bicep/ARM, optimisation des coûts, CI/CD, migration | `assets/`, `references/`, `scripts/` |
| `windows-infrastructure-administration` | Admin infrastructure Windows — migration Win10→11, Intune, VMs/golden image, Autopilot, SCCM (MECM) | — |
| `project-defaults` | Architecte de solution — structure de projet standard, conventions, `${ROOT_DIRECTORY}`, correspondance des agents, création de projet | `references/`, `scripts/` |

### Cycle spec-driven OpenSpec (SDD)

| Skill | Fonction (rôle utilisateur) | Contenu annexe |
|---|---|---|
| `openspec-workflow` | Architecte / OpenSpec — workflow complet SDD (templates, arborescence, specs GIVEN/WHEN/THEN, init/proposition/application/archivage) | — |
| `openspec-context-loading` | OpenSpec — chargement du contexte projet, liste des specs et changements, recherche de capacités | — |
| `openspec-proposal-creation` | OpenSpec — création de propositions de changement structurées (deltas de spec) | `references/`, `templates/` |
| `openspec-implementation` | OpenSpec — implémentation des propositions approuvées (tâches séquentielles + validation) | — |
| `openspec-archiving` | OpenSpec — archivage des changements terminés, fusion des deltas dans la doc vivante | — |

### Cybersécurité

| Skill | Fonction (rôle utilisateur) | Contenu annexe |
|---|---|---|
| `cybersecurite` | Architecte cybersécurité — analyse de sécurité (OWASP, PCI DSS, GDPR, Loi 25, LPRPDE, NIST, COBIT, STRIDE) | `principles/` |
| `architecture-securite-gabarits` | Architecte cybersécurité / Reviewer sécurité — gabarits de documentation d'architecture de sécurité (production 00→06 + revue) | `gabarits/`, `revue/` |

### Architecture de données

| Skill | Fonction (rôle utilisateur) | Contenu annexe |
|---|---|---|
| `data-warehouse-ops` | Architecte de données — cycle de vie d'un entrepôt de données (SSOT, ETL/ELT, modélisation dimensionnelle, qualité, gouvernance, lignage, SLA) | `assets/`, `references/`, `scripts/` |
| `analytics-engineer` | Ingénieur analytique — transformation/modélisation de données (dbt), BI, orchestration de pipelines, qualité | `references/` |

### Présentation & avant-vente

| Skill | Fonction (rôle utilisateur) | Contenu annexe |
|---|---|---|
| `presentation-targeting` | Présentation client — ciblage des sections utiles dans la doc d'architecture (réduction des coûts de lecture) | — |
| `client-presentation-generation` | Présentation client — gabarits par type (Executive, Entreprise/Affaires TOGAF, Technique, Sécurité) + mise en forme | `gabarits/`, `instructions/`, `references/` |
| `sales-deck-generation` | Avant-vente — supports de vente et réponses d'appels d'offres (Word/PDF/HTML) à partir de livrables d'architecture | — |
| `cdae-ai-eligibilite` | Conseil — analyse d'éligibilité et estimation du crédit d'impôt CDAE-IA (Québec) | — |

### Transverse

| Skill | Fonction (rôle utilisateur) | Contenu annexe |
|---|---|---|
| `git-delivery` | Capacité technique — commit + ouverture de PR vers une branche cible fournie (`gh`/`glab`), sans logique de workflow | — |

## MCP

`mcp.json` déclare un objet `mcpServers` **vide** (`{}`), ce qui est valide
selon la spec v1.0.0 (§7.2.1) : aucune de ces skills ne dépend d'un serveur MCP.
Si un serveur MCP est confirmé ultérieurement, il devra être ajouté à `mcp.json`
au format v1.0.0 (`stdio` / `streamable-http` / `sse`), en **externalisant tout
secret** (aucun token ni credential dans `headers`/`env`, la spec l'interdit —
§7.2.1 / §9.2).

## Sécurité (dépôt public)

- Aucun secret en clair n'est committé. Les skills cloud (`aws-solution-architect`,
  `azure-solution-architect`) et de données (`data-warehouse-ops`) décrivent des
  **patrons et des templates** : tout identifiant d'accès y est référencé via des
  variables d'environnement ou des paramètres, jamais en valeur.
- `git-delivery` n'embarque aucun credential : l'authentification Git/`gh` est
  fournie par l'environnement de l'agent.
- Les skills de documentation (gabarits, présentations) n'embarquent aucune
  donnée projet sensible : elles décrivent la **structure** des livrables, pas
  leur contenu.
