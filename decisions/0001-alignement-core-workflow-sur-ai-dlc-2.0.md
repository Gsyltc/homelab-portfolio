# Alignement de core-workflow.md sur AI-DLC 2.0

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

Le document `docs/core-workflow.md` du dépôt `homelab-portfolio` est le contrat commun d'orchestration multi-agents (A2A) des travaux d'architecture du workspace. Il est aujourd'hui structuré en 3 phases (Inception / Construction / Operations), présentées comme une réinterprétation d'AI-DLC.

L'analyse comparative (issue parente ALI-184) et la lecture directe du dépôt de référence `awslabs/aidlc-workflows/core` (dossiers `scopes/`, `sensors/`, `memory/`, `knowledge/`, `hooks/`, `templates/`) mettent en évidence des écarts avec la méthodologie AI-DLC 2.0 d'AWS :

- **A** — 5 phases (Initialization → Ideation → Inception → Construction → Operation) vs 3 phases actuelles ; Initialization et Ideation manquent.
- **B** — 11 scopes nommés + auto-détection + matrice stage×scope ; chez nous le principe « le workflow s'adapte au travail » est énoncé mais non outillé.
- **C** — Depth et Test strategy comme deux axes indépendants ; chez nous ils sont mélangés.
- **D** — Learning loop alimentant des règles persistantes 5 couches (`org → team → project → phase → stage`) ; absent.
- **E** — Sensors : checks déterministes advisory ; nos contrôles reposent sur le jugement d'un agent.
- **F** — Verification gates : contrôle automatique de traçabilité aux frontières de phases ; absent.
- **G** — Mode d'autonomie en Construction (question posée une fois après le walking-skeleton, halt-and-ask sur échec) ; absent.

Points déjà conformes à conserver : validation humaine granulaire, contrôle sécurité systématique (Architecte cybersécurité), piste d'audit sur l'issue + ADR obligatoires, chargement optimisé du contexte (lazy loading), gouvernance A2A par mention avec UUID résolus, agnosticité méthodologique (OpenSpec/BMAD conditionnels).

## Décision

Faire évoluer `docs/core-workflow.md` pour l'aligner sur les mécanismes clés d'AI-DLC 2.0, **tout en conservant la gouvernance A2A propre au workspace**.

L'alignement est mené selon une **approche incrémentale** (arbitrage Q1 = Option B), et non en une refonte complète unique :

1. **Stage 2** — Scopes nommés + auto-détection + séparation des axes Depth / Test strategy (mécanismes B et C).
2. **Stage 3** — Learning loop + règles persistantes (mécanisme D).
3. **Stage 4** — Verification gates + Sensors déterministes advisory (mécanismes E et F).
4. **Stage 5** — Passage à 5 phases + mode d'autonomie Construction (mécanismes A et G).
5. **Stage 6** — Consolidation, validation humaine finale et mise à disposition.

**Périmètre des artefacts** (arbitrage Q4 = périmètre étendu mais progressif) : `core-workflow.md` reste le document contractuel de référence ; les artefacts annexes (répertoires de scopes, de mémoire de règles, manifestes de sensors) sont créés **au stage qui les introduit**, pas tous d'avance. Emplacement pressenti sous `docs/workflow/` (`scopes/`, `sensors/`, `memory/`), à confirmer au stage concerné.

**Format de diagramme** (arbitrage Q5) : les schémas du workflow restent en **Mermaid**.

**Contrôle sécurité** (arbitrage Q6) : la sollicitation de l'Architecte cybersécurité intervient aux stages où des mécanismes touchant la posture de sécurité sont réellement conçus — Stage 4 (sensors/gates) et Stage 5 (mode d'autonomie Construction). Aucune modification de posture n'est actée au stade du cadrage.

Le workflow **reste agnostique de la méthodologie** : OpenSpec/BMAD restent conditionnels, déclarés au niveau du projet ou de l'issue.

Le workflow Homelab (`docs/homelab-workflow.md`) est hors périmètre.

## Conséquences

### Positives

- **POS-001** : Adaptativité réellement outillée (scopes + axes Depth/Test), au lieu d'un principe non appliqué.
- **POS-002** : Capitalisation des corrections humaines en règles persistantes (learning loop), réduisant la répétition des mêmes erreurs.
- **POS-003** : Fiabilisation déterministe (sensors, gates) sans alourdir la charge humaine, la validation granulaire restant souveraine.
- **POS-004** : Vocabulaire aligné sur AI-DLC 2.0, facilitant la reprise des pratiques et de la documentation AWS.
- **POS-005** : Livraison de valeur par étapes, workflow utilisable entre chaque stage.

### Négatives

- **NEG-001** : Complexité documentaire accrue (nouveaux mécanismes et artefacts annexes à maintenir).
- **NEG-002** : Effort de conception réparti sur plusieurs stages, avec coordination et validations humaines multiples.
- **NEG-003** : Risque d'incohérence transitoire tant que les 5 phases ne sont pas encore en place (mitigé par la compatibilité ascendante — voir ADR-0002).

## Alternatives étudiées

### ALT-001 - Refonte complète en une seule passe (Q1 Option A)

Réécrire d'emblée `core-workflow.md` en 5 phases avec tous les mécanismes A→G.

**Raison du rejet** : risque de reprise élevé, workflow inutilisable pendant la refonte, et validation humaine massive en un seul point. L'approche incrémentale livre le plus gros gain (scopes) d'abord.

### ALT-002 - Statu quo (conserver 3 phases sans outillage)

Ne pas aligner sur AI-DLC 2.0 et conserver le workflow actuel.

**Raison du rejet** : les écarts B, D, E, F privent le workspace des gains d'adaptativité, de capitalisation et de fiabilisation identifiés dans l'analyse comparative.

## Notes d'implémentation

- **IMP-001** : Chaque mécanisme fait l'objet de son propre ADR au stage qui l'introduit (scopes, learning loop, sensors/gates, autonomie).
- **IMP-002** : La compatibilité ascendante et la terminologie sont traitées dans [ADR-0002 - Stratégie de compatibilité et terminologie](0002-strategie-compatibilite-et-terminologie.md).
- **IMP-003** : Critère de réussite : `core-workflow.md` révisé et validé par l'humain, ADR correspondants tracés, aucune régression de la gouvernance A2A ni de la validation humaine granulaire.

## Références

- **REF-001** : [ADR-0002 - Stratégie de compatibilité et terminologie](0002-strategie-compatibilite-et-terminologie.md)
- **REF-002** : [AI-DLC workflows (awslabs)](https://github.com/awslabs/aidlc-workflows)
- **REF-003** : [ADR Template de Michael Nygard / joelparkerhenderson](https://github.com/joelparkerhenderson/architecture-decision-record)
