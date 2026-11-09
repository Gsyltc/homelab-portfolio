# Agents — workflow `core` (Architecture de solution & intégration)

Définitions conformes (front-matter YAML + corps Markdown) des agents du **workflow `core`** d'architecture de solution & intégration, coordonné par l'**Architecture Solution & Intégration**. Le workflow de référence est [`conductor.md`](../common/conductor.md) (source unique — instructions du coordinateur ; le QUOI de chaque étape vit dans [`stages/`](../common/stages/) et les mécanismes transverses dans [`protocols/`](../common/protocols/)). Règle de routage entre workflows : section « Architecture Flow » de [`AGENTS.md`](../../AGENTS.md).

## Rôles génériques → fichiers

| Rôle générique (workflow) | Fichier | Objet |
| --- | --- | --- |
| Architecture Solution & Intégration (**coordinateur**) | [architecture-solution-integration-agent.md](architecture-solution-integration-agent.md) | Coordonne, supervise et valide les travaux ; vérifie la cohérence avec les ADR, demande les validations humaines, met les documents à disposition. Ne produit pas les livrables. |
| Architecte de solution | [solution-architect-agent.md](solution-architect-agent.md) | Conçoit les solutions TI : documentation d'architecture (DAS), ADR, diagrammes C4 / Archimate / PlantUML / CALM. |
| Architecte AWS | [aws-architect-agent.md](aws-architect-agent.md) | Définit les services AWS requis, produit les diagrammes d'architecture et optimise les coûts. |
| Architecte Azure | [azure-architect-agent.md](azure-architect-agent.md) | Porte toutes les fonctions cloud Azure : services, diagrammes, coûts, et livrables d'infrastructure de déploiement Azure (IaC, plans de déploiement / rollback). |
| Architecte Cybersécurité | [cybersecurity-architect-agent.md](cybersecurity-architect-agent.md) | Sécurité : OWASP, STRIDE, ISO 27001, NIST, COBIT, ISO 42001/23894, PCI DSS. Périmètre sécurité (hors production des livrables non sécurité). |
| Architecte de données | [data-architect-agent.md](data-architect-agent.md) | Modélisation (dimensionnel, Data Vault), Data Warehouse / Lake / Lakehouse, virtualisation. Traduit les besoins de l'Architecte de solution en modèles de données. |
| OpenSpec Expert | [openspec-agent.md](openspec-agent.md) | Méthode OpenSpec (SDD) : initialise, propose, applique et archive les spécifications. |
| Experte d'archivage | [archiving-agent.md](archiving-agent.md) | Import / export de documents, création d'archives lors des exports multiples, et mise à disposition par Git (commit + PR) sur tâche cadrée par le coordinateur. |
| Vente & Appels d'Offres | [sales-proposals-agent.md](sales-proposals-agent.md) | Synthétise les architectures en supports de vente et réponses d'appels d'offres (Word / PDF / HTML / script). |
| Présentation client | [client-presentation-agent.md](client-presentation-agent.md) | Présentations client de projet ciblées (Executive / Entreprise-Affaires TOGAF / Technique-Fonctionnelle / Sécurité-Conformité) ; HTML dynamique (Archify) et PowerPoint ; à partir des documents d'architecture validés. |
| Reviewer de cohérence | [consistency-reviewer-agent.md](consistency-reviewer-agent.md) | Revue « review-only » de la cohérence (documentation ↔ décisions, absence de conflits, complétude, conventions). Ne produit aucun livrable. |
| Reviewer de sécurité | [security-reviewer-agent.md](security-reviewer-agent.md) | Revue « review-only » de la sécurité (OWASP / STRIDE toujours actifs ; autres cadres selon surface). Non substituable dès qu'une surface de sécurité est produite ou modifiée. |
| Infrastructure Windows | [windows-infrastructure-admin-agent.md](windows-infrastructure-admin-agent.md) | Administration Windows : migration Win10→Win11, Intune, VMs, golden image, Autopilot, SCCM. Périmètre strictement Windows (le cloud Azure relève de l'Architecte Azure). |
| Agent de notifications | [notification-agent.md](notification-agent.md) | Notifications de fin de tâches. Utilitaire de workspace partagé (source unique de vérité de sa définition). |

## Correspondance nom ↔ fonction (source unique)

Les fichiers ci-dessus définissent les acteurs par **rôle générique** (fonction). La correspondance concrète **nom ↔ fonction** — nécessaire pour recréer la liste des agents et router une délégation A2A — fait foi dans la skill **`project-defaults`** ([`SKILL.md`](../../plugins/architecture-assistant/skills/project-defaults/SKILL.md)), **source unique de vérité**. Aucun agent ne duplique cette table. Cette table ne fige **aucun UUID** : chaque workspace a ses propres UUID, à résoudre à la demande.

Les agents sont créés au format **`<nom> - <fonction>`** (ex. `Manuel - Architecte de solution`), la `<fonction>` reprenant le `display_name` du fichier de définition. Pour toute délégation, la mention prend la forme `[@Label](mention://agent/<uuid>)` : **résoudre l'UUID via `multica agent list --output json`** (champ `id`), ne jamais deviner ni inventer un UUID.

## Création / recréation des agents et création d'un nouveau projet

La procédure de **création d'un nouveau projet** (projet workspace, liaison du dépôt, description complète, structure disque, création des agents et skills `core` manquants) et la **recréation de la liste des agents** sont décrites dans la skill [`project-defaults`](../../plugins/architecture-assistant/skills/project-defaults/SKILL.md).

## Hook d'écriture des sensors — branché par défaut sur les agents de production

Les **agents de production de livrables** portent, dans leur front-matter, le **hook d'écriture** `core/sensors/hooks/post_write.py` (champ `hooks.postToolUse`, matcher `fs_write`), désigné par un **chemin ancré sur le checkout `core`** (`$CORE_HOME`) afin de se déclencher même quand le répertoire courant est le dépôt du projet vérifié — convention d'invocation : [`../sensors/README.md`](../sensors/README.md) (§ Nature et § Hooks). À chaque `fs_write`, les sensors `fire_on: write` (`style-concision`, `diagram-validity`, `detailed-arch-refs`) se déclenchent **automatiquement** et émettent un signal **advisory** (jamais bloquant, code 0), sans dépendre de la discipline manuelle au temps 4 du [`stage-protocol`](../common/protocols/stage-protocol.md). Le hook est **agnostique du harnais** ([ADR-0038](../../decisions/0038-workflow-core-agnostique-du-harnais.md), [ADR-0046](../../decisions/0046-sensors-executables-python-et-hooks-agnostiques.md)) : la forme Claude Code (`PostToolUse` / `Write|Edit`) est documentée dans [`../sensors/README.md`](../sensors/README.md) (§ Hooks). Il **ne remplace pas** le lancement explicite des sensors au temps 4 ni le compte rendu `## Sensors` — il en est le **filet déterministe**.

**Périmètre (choix documenté).** Le hook est branché sur les **sept agents qui produisent des livrables** matchés par les sensors `fire_on: write` (`matches: documentation/**/*.md`, `*.puml`, `*.dsl`) :

- Architecte de solution · Architecte AWS · Architecte Azure · Architecte de données · Infrastructure Windows · Architecte Cybersécurité · OpenSpec Expert.

**Hors périmètre (choix documenté).** Le hook n'est **pas** branché sur :

- le **coordinateur** (Architecture Solution & Intégration) — il coordonne, ne produit pas de livrable ;
- les **reviewers** (cohérence, sécurité) — « review-only », n'écrivent aucun livrable ;
- **Vente & Appels d'Offres** et **Présentation client** — produisent des supports (Word / PDF / HTML / PPTX) hors du périmètre `matches` des sensors d'écriture ;
- les **utilitaires** (Experte d'archivage, Agent de notifications).

Reste **advisory par décision** : rendre un sensor bloquant est une décision structurante distincte (ADR + contrôle sécurité, SG-3) — voir [`../sensors/README.md`](../sensors/README.md), « Garde-fou : advisory par décision ».

## Garde-fous (rappel)

Coordination par l'issue (piste d'audit sur l'issue Multica) · délégation A2A par mention valide `[@Label](mention://agent/<uuid>)` · le coordinateur coordonne, les spécialistes produisent · validation humaine granulaire · aucun secret dans les livrables · diagrammes générés en code. Ces règles sont définies une seule fois dans [`conductor.md`](../common/conductor.md) et [`protocols/`](../common/protocols/).
