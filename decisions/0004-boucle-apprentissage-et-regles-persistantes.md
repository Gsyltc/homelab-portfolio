# Boucle d'apprentissage et règles persistantes multi-couches

---
auteurs: Sylvain G.
accepté par : Sylvain G.
accepté le : 2026-09-02
supersedes: ""
superseded_by: ""

---

## Status

Accepted

## Contexte

Le workflow `docs/core-workflow.md` capitalisait ses décisions structurantes en ADR, mais **ne capitalisait pas les corrections humaines récurrentes** : une correction apportée sur un projet pouvait devoir être répétée sur le suivant. L'analyse comparative avec AI-DLC 2.0 (issue parente ALI-184, cadrage ALI-185, [ADR-0001](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)) a identifié cet écart (mécanisme **D**) : AI-DLC dispose d'une **mémoire de règles en couches** (`org → team → project → phase → stage`, dépôt `awslabs/aidlc-workflows/core/memory`) alimentée par une **boucle d'apprentissage** aux gates.

Le Stage 3 (ALI-187) formalise ce mécanisme, en cohérence avec la gouvernance A2A du workspace (validation humaine granulaire, piste d'audit sur l'issue, contrôle sécurité systématique) et avec les scopes / axes du Stage 2 ([ADR-0003](0003-scopes-et-axes-depth-verification.md)). Les arbitrages ont été soumis à l'humain (Q-A à Q-F) et tranchés sur l'issue ALI-187.

## Décision

**Introduire une mémoire de règles multi-couches et une boucle d'apprentissage** capitalisant les corrections humaines validées en règles persistantes, dans le respect des invariants de gouvernance.

**Emplacement** (arbitrage Q-A) : fichiers Markdown versionnés dans le repo `homelab-portfolio`, répertoire **`core/rules/`**. La *capture* (candidats, décision humaine) reste tracée **sur l'issue** ; seule la **règle acceptée** est écrite sur disque.

**Couches** (arbitrage Q-B = version adaptée, couche `scope` incluse dès maintenant) — quatre couches, précédence `workspace` > `project` > `phase` > `scope` :

- `workspace` — `core/rules/workspace.md` (invariants et conventions valables partout, toujours chargé).
- `project` — `core/rules/projects/<projet>.md` (spécifique à un projet, projet courant chargé au démarrage).
- `phase` — `core/rules/phases/<phase>.md` (`inception` / `construction` / `operation`, chargé à la demande).
- `scope` — `core/rules/scopes/<scope>.md` (les 8 scopes de l'ADR-0003, chargé à la demande) — pont explicite avec le mécanisme de scopes.

**Déclencheur de capture** (arbitrage Q-C = C1 avec garde-fous) : à chaque validation granulaire, le coordinateur **propose systématiquement** les candidats-règles détectés dans la piste d'audit ; l'**écriture reste subordonnée à une validation humaine explicite** (garde-fou). Une règle nouvellement écrite s'applique au **prochain** workflow, jamais en cours de route.

**Portée par défaut** (arbitrage Q-D) : `project`. La promotion vers `workspace` est une décision structurante explicite (ADR si structurante ; contrôle sécurité si elle touche la sécurité).

**Contrôle de conflit à l'admission** (arbitrage Q-E = oui + oui) :

- **Précédence des couches** : une règle ne peut pas contredire une règle d'une couche supérieure ; sur conflit, le coordinateur **remonte à l'humain** (et à l'Architecte cybersécurité si sécurité) et ne tranche jamais seul.
- **Invariants non contournables** : aucune règle ne peut affaiblir la validation humaine granulaire, les ADR, la piste d'audit, le contrôle sécurité minimal (OWASP / STRIDE) ni les garde-fous sécurité des scopes ; un tel candidat est rejeté d'office.
- **Contrôle sécurité systématique de la couche `workspace`** : toute règle admise en couche `workspace` passe par un contrôle de l'Architecte cybersécurité avant écriture, qu'elle « touche la sécurité » ou non.
- **Idempotence** : pas de ré-écriture d'un candidat déjà couvert.

**Articulation** (arbitrage Q-F) : capture sur l'issue / règle acceptée sur disque ; chargement paresseux des couches `phase` et `scope` ; articulation OpenSpec conditionnelle (les règles apprises peuvent enrichir les propositions OpenSpec sans jamais imposer la méthodologie).

## Conséquences

### Positives

- **POS-001** : Les corrections humaines récurrentes sont capitalisées ; un agent ne répète plus la même erreur d'un projet à l'autre.
- **POS-002** : Règles versionnées, diffables et revues comme tout artefact d'architecture (au même titre que les ADR).
- **POS-003** : Couche `scope` = pont direct avec l'ADR-0003 ; une règle peut cibler un scope précis.
- **POS-004** : Le chargement paresseux des couches `phase` / `scope` préserve la fenêtre de contexte.
- **POS-005** : Le contrôle de conflit et les invariants non contournables empêchent une règle apprise d'affaiblir la posture de sécurité ou la gouvernance.

### Négatives

- **NEG-001** : `core/rules/` est un nouvel artefact à maintenir et à tenir cohérent (risque de dérive atténué par l'idempotence et la revue).
- **NEG-002** : Effort supplémentaire au point de validation (proposition des candidats, choix de couche/portée).
- **NEG-003** : Le contrôle sécurité systématique de la couche `workspace` ajoute une sollicitation de l'Architecte cybersécurité à chaque règle globale.

## Alternatives étudiées

### ALT-001 - Règles en métadonnée d'issue / projet Multica

Stocker les règles dans la métadonnée Multica plutôt que dans le repo.

**Raison du rejet** : la métadonnée est par-issue, non versionnée, non partagée et déconseillée pour du contenu long ; elle ne permet ni la revue ni le chargement « au démarrage de chaque workflow ». Les règles sont un artefact contractuel qui appartient au repo (arbitrage Q-A).

### ALT-002 - Reprise littérale des 5 couches AI-DLC (`org/team/project/phase/stage`)

Adopter la nomenclature de référence telle quelle.

**Raison du rejet** : le workspace n'a pas d'équivalent « team » distinct (le workspace est l'équipe) ni de « stage » séparé de la phase. Adaptation à 4 couches, avec ajout d'une couche `scope` propre à notre mécanisme de scopes (arbitrage Q-B).

### ALT-003 - Capture sur demande explicite uniquement (C2)

N'enregistrer un candidat-règle que lorsque l'humain le demande explicitement.

**Raison du rejet** : risque de laisser filer des corrections récurrentes par oubli — exactement l'erreur que le mécanisme veut éviter. Retenu : C1 (proposition systématique) avec écriture subordonnée à validation humaine explicite (arbitrage Q-C).

## Notes d'implémentation

- **IMP-001** : Mécanisme documenté dans la section « Règles & boucle d'apprentissage » de [`docs/core-workflow.md`](../docs/core-workflow.md).
- **IMP-002** : Structure scaffoldée dans `core/rules/` — [`README.md`](../core/rules/README.md), `workspace.md` (seedé avec les invariants existants), `projects/_template.md`, `phases/{inception,construction,operation}.md`, `scopes/_template.md`.
- **IMP-003** : Une règle nouvellement écrite s'applique au **prochain** workflow ; l'exécution en cours n'est jamais altérée.
- **IMP-004** : Contrôle sécurité (Architecte cybersécurité) sollicité sur le mécanisme — notamment le contrôle de conflit à l'admission, les invariants non contournables et le contrôle systématique de la couche `workspace` — avant la validation finale.

## Références

- **REF-001** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [ADR-0002 - Stratégie de compatibilité et terminologie](0002-strategie-compatibilite-et-terminologie.md)
- **REF-003** : [ADR-0003 - Scopes et axes Depth / vérification des livrables](0003-scopes-et-axes-depth-verification.md)
- **REF-004** : [AI-DLC workflows (awslabs) — core/memory](https://github.com/awslabs/aidlc-workflows/tree/main/core/memory)
