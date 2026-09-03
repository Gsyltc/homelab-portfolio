# Alignement des définitions d'agents Homelab sur le contrat AI-DLC « Adding an Agent »

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : 2026-09-03
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — validation humaine explicite obtenue (multica.gaston, 2026-09-03, issue ALI-209) : les trois points soumis ont été confirmés — (1) non-création de personas review-only dédiés côté Homelab (QA Docker reviewer technique correcteur + Architecte de sécurité), (2) classement des `tier`, (3) acceptation de l'ADR. L'invariant est respecté (aucun ADR accepté sans validation humaine granulaire). Cet ADR ne modifie **aucune posture de sécurité** ni **aucune surface d'exécution** : les définitions d'agents Homelab portaient déjà le front-matter conforme (voir § Contexte) ; il **trace** l'alignement, les divergences assumées et la distinction domaine / review.

## Contexte

Les définitions d'agents du workflow **Homelab** vivent sous [`homelab/agents/`](../homelab/agents/) (7 fichiers `.md` : Tech Lead, Spécialiste Docker, QA Docker, Spécialiste Terraform, Expert n8n, Expert Home Assistant, Architecte de sécurité Homelab). Le **Stage 1** de l'alignement AI-DLC du harness Homelab (issue **ALI-209**, parente ALI-208) porte ces fichiers sur le contrat **« Adding an Agent »** du *Harness Engineer Guide* (`awslabs/aidlc-workflows`). C'est l'**équivalent Homelab** du travail fait pour le harness `core` (issue ALI-194, tracée en [ADR-0008](0008-alignement-definitions-agents-sur-ai-dlc.md)).

Le contrat amont fixe un front-matter d'agent minimal :

- `name` — **doit égaler le stem du fichier** ;
- `display_name` — libellé humain ;
- `description` — résumé du rôle ;
- `disallowedTools` — **doit inclure `Task`** ; interdiction non optionnelle de l'auto-délégation (un agent ne peut pas engendrer ses propres sous-agents) ;
- `tier` — `judgment` / `balanced` / `templated` ; nomme la **nature du travail**, projeté ensuite en clés `model` / `effort` par harness (jamais de `model:` brut en source).

Point clé du contrat : **`allowedTools` ne fait pas partie du schéma AI-DLC**. Un agent hérite par défaut de tout le *toolset* de session ; pour le **restreindre**, on utilise une *allowlist* optionnelle `tools:` (et non `allowedTools`).

**Constat d'entrée (particularité de ce stage)** : contrairement au harness `core` (où les 9 fichiers portaient un `allowedTools: Multica` non conforme à retirer), les 7 fichiers `homelab/agents/*.md` ont été **créés directement conformes** lors de la refonte du workflow Homelab (ALI-200, PR #74 puis #80), l'Architecte de sécurité Homelab ayant été ajouté via ALI-203. À l'ouverture d'ALI-209, la vérification montre que **les 7 fichiers portent déjà** `name`=stem, `display_name`, `description`, `skills:`, `disallowedTools: Task` et un `tier` valide, **sans aucun `allowedTools` résiduel**. Le travail de ce stage est donc principalement de **vérifier**, **formaliser la distinction domaine / review** et **tracer les divergences assumées** — pas de corriger un front-matter non conforme.

Trois axes du contrat sont à traiter (issue ALI-209) :

1. **Front-matter** : confirmer `disallowedTools: Task` (obligatoire) + `tier` par agent, sans `allowedTools`.
2. **Reviewers** : distinguer les agents « domaine » des agents « review-only » (le QA Docker joue un rôle de reviewer technique — le formaliser).
3. **Connaissances par agent** : documenter les skills rattachées par persona (ou la raison pour laquelle les skills Multica en tiennent lieu).

Contrainte de cadrage (ALI-208 / ADR-0013) : adapter au moteur A2A **Multica**, sans importer le tooling amont non applicable (`bun`, hooks `.ts`, `dist/<harness>/`) ; toute divergence assumée est tracée ; aucune régression sur l'exécution A2A ni sur les garde-fous absolus du Homelab.

## Décision

### 1. Front-matter — contrat adopté, conformité confirmée (aucune correction requise)

Pour les 7 fichiers `homelab/agents/*.md`, l'état vérifié à l'ouverture d'ALI-209 est **déjà conforme** ; cet ADR l'entérine comme état cible :

- `name` = stem du fichier (vérifié sur les 7) ;
- `display_name` présent (vérifié) ;
- `description` présente (vérifiée) ;
- `disallowedTools: Task` présent sur **chaque** agent (vérifié sur les 7) ;
- `tier` présent et ∈ {`judgment`, `balanced`} (vérifié — voir § tiers) ;
- **aucun** champ `allowedTools` (vérifié : aucune occurrence sous `homelab/agents/`) ;
- **aucune** *allowlist* `tools:` ajoutée : les agents Multica reçoivent leurs capacités via l'**assignation de skills**, pas via une *allowlist* d'outils de session.

**Divergence assumée (tracée)** : le champ `disallowedTools` est un front-matter **Claude-only** dans l'amont ; sur **Multica** il n'existe pas d'outil `Task`, la valeur est donc **documentaire / déclarative** (intention explicite « aucune sous-délégation »), sans effet d'exécution mais cohérente avec le contrat et avec la gouvernance A2A par mention. Identique à la divergence tracée pour `core` en [ADR-0008](0008-alignement-definitions-agents-sur-ai-dlc.md), § Décision 1.

### 2. Tiers retenus

| Agent (stem) | `tier` | Justification |
| --- | --- | --- |
| `tech-lead-homelab-agent` | `judgment` | Coordinateur + contrôleur qualité central : arbitrage multi-contraintes, routage A2A, verrou de concurrence, décision de mise en revue humaine — raisonnement qui cascade en aval. |
| `security-architect-homelab-agent` | `judgment` | **Jugement sécurité** : analyse de risque (STRIDE / OWASP adaptés homelab), hardening, contrôleur sécurité de la couche `global` de la mémoire de règles — surface sécurité qui cascade. Garde-fou : « en cas de doute, `judgment` ». |
| `docker-specialist-agent` | `balanced` | Production de `docker-compose` Swarm sous mission cadrée (contexte, périmètre, critères fournis par le Leader). |
| `qa-docker-agent` | `balanced` | **Reviewer technique** : juge/corrige un livrable existant contre des critères explicites (YAML, Swarm, hardening technique, cohérence Traefik) — profil « reviewer-shaped ». |
| `terraform-specialist-agent` | `balanced` | Production de fichiers `.tf`/`.tfvars` sous mission cadrée ; ne déploie jamais. |
| `n8n-expert-agent` | `balanced` | Conception / diagnostic de flux n8n via MCP sous mission cadrée. |
| `home-assistant-expert-agent` | `balanced` | Pilotage Home Assistant via MCP officiel sous mission cadrée, double validation avant toute action réelle. |

`balanced` / `templated` projettent aujourd'hui à l'identique sur les harness où le tier ne change rien (Kiro / Cursor / Copilot héritent du modèle et de l'effort de session) ; le tier reste néanmoins **sémantiquement correct** et exploitable par un harness qui l'honore.

### 3. Distinction domaine / review — modèle Homelab tracé (divergence assumée vs core)

Le contrat amont modélise la revue par des **personas review-only dédiés** ; le harness `core` a créé deux personas review-only distincts sur **arbitrage humain explicite** (Reviewer de cohérence, Reviewer de sécurité — [ADR-0008](0008-alignement-definitions-agents-sur-ai-dlc.md), § Décision 3). **Le Homelab ne reproduit pas cette scission** et **assume la divergence** : le rôle de revue reste **porté par des fonctions existantes**, pas par des personas review-only séparés.

Classification des 7 agents Homelab :

| Nature | Agent(s) | Rôle |
| --- | --- | --- |
| **Coordination** | Tech Lead Homelab | Coordonne, sollicite, applique le verrou par stack, demande la validation humaine. Contrôleur qualité central : rien ne va en revue humaine sans son contrôle. Ne produit pas de livrable. |
| **Domaine (production)** | Spécialiste Docker, Spécialiste Terraform, Expert n8n, Expert Home Assistant | Produisent les livrables (compose, `.tf`, flux n8n, config Home Assistant) sous mission cadrée. |
| **Review technique** | **QA Docker** | **Reviewer technique** (review-shaped) des `docker-compose` : vérifie et corrige après création (YAML, Swarm, hardening technique, cohérence Traefik). Intervient **après** le Spécialiste Docker. |
| **Jugement sécurité** | Architecte de sécurité Homelab | Porte le **jugement sécurité** (analyse de risque, durcissement, revue des choix d'exposition / authentification) et le **contrôle sécurité** de la couche `global` de la mémoire de règles. Distinct du QA Docker (conformité technique) et du Tech Lead (coordination). |

**Formalisation du QA Docker comme reviewer** : sa `description` et son corps l'énoncent déjà (« vérifie et corrige … Intervient après la création ») ; cet ADR l'**explicite** comme fonction de **review technique**, distincte de la production (Spécialiste Docker) et du jugement sécurité (Architecte de sécurité). Le `tier: balanced` du QA Docker reflète ce profil review-shaped, cohérent avec le classement des reviewers `core`.

**Divergence assumée (tracée) — pas de personas review-only dédiés côté Homelab** :

- Le QA Docker **corrige** les livrables (il n'est pas strictement « review-only » comme les reviewers `core` qui ne modifient rien) : c'est un **reviewer technique correcteur**, adapté à un pipeline Docker opérationnel où correction et vérification sont indissociables. Le garde-fou de séparation reste net : le **Spécialiste Docker produit**, le **QA Docker contrôle/corrige**, le **Tech Lead** ne présente à l'humain qu'un livrable contrôlé.
- La revue de sécurité est portée par l'**Architecte de sécurité Homelab** (jugement + contrôle d'admission des règles `global`), et non par un « Reviewer de sécurité » review-only distinct. Motif : le périmètre Homelab est volontairement limité à la **sécurité de base** (pas de conformité réglementaire — Loi 25, PCI DSS, GDPR/RGPD, LPRPDE explicitement hors périmètre) ; dédoubler analyse et verdict n'apporterait pas le bénéfice qui a justifié la scission côté `core`.
- **Invariants préservés** : validation humaine granulaire ; aucun livrable en revue humaine sans le contrôle du Tech Lead ; le contrôle sécurité de la couche `global` reste porté par l'Architecte de sécurité (clauses SEC-2 / SEC-4 de la mémoire de règles) ; garde-fous absolus intacts (règle absolue n8n, Terraform ne déploie jamais, aucun secret, jamais `${SNI}` en Terraform, un seul traitement par stack).

### 4. Connaissances par agent — les skills Multica tiennent lieu d'overlay

Comme pour `core` ([ADR-0008](0008-alignement-definitions-agents-sur-ai-dlc.md), § Décision 4), le Homelab **ne crée pas** d'arborescence `homelab/knowledge/<agent>/`. La connaissance par persona est portée par les **skills Multica**, déclarées dans le champ `skills:` de chaque agent et effectivement chargées après **import** (`multica skill import`) puis **assignation** (`multica agent skills add|set`). Skills rattachées, vérifiées dans le front-matter :

| Agent | `skills:` | Connaissances / accès |
| --- | --- | --- |
| Tech Lead Homelab | `[]` | Coordination pure ; savoir-faire dans le corps (verrou par stack, délégation A2A, gates). Pas de skill de production. |
| Spécialiste Docker | `docker-composer`, `homelab-vault-access`, `traefik-manager-read` | Génération compose Swarm ; lecture secrets Vault (AppRole) ; lecture Traefik Manager. |
| QA Docker | `docker-composer`, `dockerfile-validator`, `homelab-vault-access`, `traefik-manager-read` | Idem + validation Dockerfile ; lecture seule Traefik (aucune écriture). |
| Spécialiste Terraform | `configuration-applications`, `homelab-vault-access` | Écriture `.tf`/`.tfvars` ; lecture secrets Vault. |
| Expert n8n | `caveman`, `caveman-compress` | Compression de contexte ; **accès n8n via serveur MCP** (URL / jeton en variables d'environnement de l'agent), pas via une skill. |
| Expert Home Assistant | `[]` | **Accès Home Assistant via serveur MCP officiel**, pas via une skill — d'où `skills:` vide. |
| Architecte de sécurité Homelab | `cybersecurite`, `traefik-manager-read` | Analyse de risque / hardening ; lecture Traefik. |

**Divergence assumée (tracée)** : deux agents portent leur capacité principale par **serveur MCP** (n8n, Home Assistant) plutôt que par skill — d'où un `skills:` vide (Home Assistant) ou limité au support de contexte (n8n). C'est cohérent avec le modèle Multica (les MCP sont configurés au niveau de l'agent, cf. `multica agent mcp`), et documenté ici pour éviter de conclure à tort à une connaissance manquante.

### 5. Réponses aux inputs requis de l'issue

- **Existence des agents** : les 7 agents Homelab **existent** comme fonctions Multica (créés/provisionnés en ALI-200 ; Architecte de sécurité ajouté en ALI-203). Leur table d'UUID fait foi dans [`tech-lead-homelab-agent.md`](../homelab/agents/tech-lead-homelab-agent.md), à re-vérifier via `multica agent list --output json` (champ `id`) — ne jamais deviner un UUID. Ce stage **aligne la forme déclarative** de leurs définitions ; il n'en crée aucun.
- **Emplacement** des définitions : [`homelab/agents/`](../homelab/agents/) (miroir de `core/agents/`), avec un [`README.md`](../homelab/agents/README.md) qui documente rôles ↔ fichiers ↔ objet. L'Agent de notifications (Alfred) n'est **pas** dupliqué sous `homelab/agents/` : sa source unique reste [`core/agents/notification-agent.md`](../core/agents/notification-agent.md).

## Conséquences

### Positives

- **POS-001** : Front-matter d'agent Homelab **confirmé conforme** au contrat AI-DLC (`name`=stem, `display_name`, `description`, `disallowedTools: Task`, `tier`) sans `allowedTools`, sans importer le tooling amont.
- **POS-002** : Frontière « pas d'auto-délégation » **explicite dans la source**, cohérente avec la gouvernance A2A par mention.
- **POS-003** : `tier` rend lisible la nature du travail par agent et ouvre la voie à une projection modèle/effort par un harness qui l'honore, sans redécision.
- **POS-004** : Distinction **domaine / review / coordination / jugement sécurité** formalisée et tracée ; le QA Docker est reconnu comme **reviewer technique** ; l'Architecte de sécurité comme fonction de **jugement sécurité** distincte.
- **POS-005** : Divergences vs `core` (pas de personas review-only dédiés ; capacités MCP pour n8n / Home Assistant) **explicitement assumées et tracées**, cohérentes avec le périmètre « sécurité de base » du Homelab.

### Négatives

- **NEG-001** : `disallowedTools: Task` est **inerte à l'exécution sur Multica** (pas d'outil `Task`) : valeur documentaire ; atténué par la satisfaction du contrat pour tout futur portage de harness.
- **NEG-002** : La classification `tier` n'a **aucun effet** sur les harness qui héritent du modèle/effort de session ; elle reste néanmoins sémantiquement utile et sans coût.
- **NEG-003** : L'absence d'overlay `homelab/knowledge/<agent>/` impose de passer par l'import/assignation de skills (ou la config MCP) pour enrichir un persona ; c'est le mécanisme Multica attendu, mais il diffère de l'amont (documenté ici).
- **NEG-004** : Le modèle de revue Homelab **diverge** du modèle `core` (pas de reviewers review-only dédiés ; le QA Docker corrige en plus de vérifier) : divergence assumée, à re-confirmer si le périmètre Homelab venait à inclure de la conformité réglementaire (ce qui n'est pas le cas aujourd'hui).

## Alternatives étudiées

### ALT-001 — Créer des personas « review-only » dédiés côté Homelab (miroir strict de core)

**Raison du rejet** : le périmètre Homelab est limité à la **sécurité de base** (pas de conformité réglementaire) et le pipeline Docker rend la vérification et la correction indissociables. Dédoubler analyse et verdict n'apporterait pas le bénéfice qui a justifié la scission côté `core` (arbitrage humain ALI-194), au prix de deux fonctions supplémentaires à provisionner. Le QA Docker (reviewer technique correcteur) et l'Architecte de sécurité (jugement + contrôle d'admission) couvrent la revue avec les invariants préservés.

### ALT-002 — Ajouter une *allowlist* `tools:` restrictive par agent

**Raison du rejet** : sur Multica les capacités sont conférées par **assignation de skills** (et **configuration MCP**), pas par une *allowlist* d'outils de session. Une `tools:` restrictive n'aurait pas de correspondance runtime et risquerait de sur-contraindre à tort. Laisser hériter le toolset de session (recommandation amont).

### ALT-003 — Créer une arborescence `homelab/knowledge/<agent>/`

**Raison du rejet** : créerait une source de connaissance non chargée par le runtime Multica (découverte non automatique), concurrente des skills importées/assignées et des serveurs MCP — divergence sans bénéfice d'exécution.

### ALT-004 — Dupliquer l'Agent de notifications sous `homelab/agents/`

**Raison du rejet** : Alfred est un utilitaire partagé entre les deux workflows ; sa source unique reste `core/agents/notification-agent.md`. Une duplication créerait deux sources divergentes.

## Notes d'implémentation

- **IMP-001** : 7 fichiers `homelab/agents/*.md` **vérifiés** conformes (name=stem, `display_name`, `description`, `disallowedTools: Task`, `tier` ∈ {judgment, balanced}, `skills:` présent) ; **aucune** occurrence de `allowedTools`. Aucune modification de front-matter n'a été nécessaire : les fichiers étaient déjà conformes (créés en ALI-200 / ALI-203).
- **IMP-002** : Distinction domaine / review **tracée** dans le présent ADR (§ Décision 3) : QA Docker = reviewer technique (correcteur) ; Architecte de sécurité = jugement sécurité + contrôle d'admission `global` ; 4 spécialistes = production ; Tech Lead = coordination + contrôle qualité central. Le [`homelab/agents/README.md`](../homelab/agents/README.md) reflète déjà ces rôles.
- **IMP-003** : Connaissances — **aucune arborescence `homelab/knowledge/`** créée ; les skills Multica (import + assignation) et les serveurs MCP (n8n, Home Assistant) tiennent lieu d'overlay.
- **IMP-004** : Pointeurs — `README.md` et `AGENTS.md` mentionnent `decisions/ (0001…0012)` (plage en retard sur les ADR existants 0013…0017) ; mis à jour vers `0001…0018` pour inclure le présent ADR. La renumérotation fine de la plage intermédiaire relève de la vérification globale (ALI-214).
- **IMP-005** : Contrôle sécurité — cet ADR **ne modifie aucune surface de sécurité** (aucune fonction de verdict n'est déplacée : l'Architecte de sécurité reste l'analyste/contrôleur, le QA Docker reste le reviewer technique). Il **trace** l'existant. Le passage à *Accepted* requiert la validation humaine granulaire (invariant).
- **IMP-006** : Cohérence de stage — les définitions référencent `homelab/common/conductor.md` et `homelab/common/stages|protocols/`, non encore créés (ALI-200 stage 7). Divergence temporaire connue : les agents pointent vers un workflow de référence à produire ; la cohérence finale est vérifiée en ALI-214. Aucun blocage pour cet ADR (le front-matter et la classification ne dépendent pas de ces fichiers).

## Références

- **REF-001** : Issue ALI-209 (Stage 1 — Agents Homelab : front-matter AI-DLC, reviewers, connaissances) ; issue parente ALI-208.
- **REF-002** : [ADR-0008 - Alignement des définitions d'agents sur le contrat AI-DLC « Adding an Agent »](0008-alignement-definitions-agents-sur-ai-dlc.md) (équivalent `core`, issue ALI-194).
- **REF-003** : [ADR-0013 - Cadrage de la refonte de homelab-workflow.md sur AI-DLC 2.0](0013-cadrage-refonte-homelab-workflow-sur-ai-dlc.md).
- **REF-004** : [ADR-0015 - Learning loop et règles persistantes Homelab](0015-learning-loop-et-regles-persistantes-homelab.md) (couche `global`, contrôle sécurité SEC-2 / SEC-4).
- **REF-005** : [`homelab/agents/README.md`](../homelab/agents/README.md) — rôles ↔ fichiers ↔ objet.
- **REF-006** : [AI-DLC — Harness Engineer Guide, « Adding an Agent »](https://awslabs.github.io/aidlc-workflows/harness-engineering/03-adding-an-agent/)
- **REF-007** : [AI-DLC workflows (awslabs) — core/agents](https://github.com/awslabs/aidlc-workflows)
