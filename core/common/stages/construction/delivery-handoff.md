---
slug: delivery-handoff
phase: construction
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecture Solution & Intégration
support_agents: [Experte d'archivage, Agent de notifications]
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: granular
produces: [livrables_valides_mis_a_disposition]
consumes: [{artifact: livrables_valides, required: true}]
requires_stage: [consolidation-handoff]
sensors: [required-sections]
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Livrables validés granulairement (consolidation-handoff)"
outputs: "Livrables mis à disposition : commit + PR si accord humain explicite, sinon archivage par dossier ; notification de fin de réalisation (fichiers / PR en attente) envoyée dès la mise à disposition"
---

# Mise à disposition et notification de fin de réalisation

## Objectif

Mettre à disposition les livrables validés — par archivage ou par Git (commit + PR) — puis notifier dès cette mise à disposition.

> **« Archivage par dossier » ≠ « archivage OpenSpec ».** L'archivage évoqué dans ce stage est le **fallback de mise à disposition** des livrables (zip + téléversement) quand il n'y a pas de commit/PR. Il ne faut pas le confondre avec l'**archivage OpenSpec** (fusion des deltas dans les specs vivantes + déplacement vers `openspec/changes/archive/`), qui est **découplé de l'approbation** et n'intervient qu'**après déploiement effectif**, en phase Operation ([`../operation/deployment-under-validation.md`](../operation/deployment-under-validation.md), Step 5). Aucun archivage OpenSpec n'a lieu dans ce stage.

## Steps

> **La logique de ce stage est portée par le workflow** : le **coordinateur** décide, pose la question de PR, résout la branche cible et déclenche la notification. L'**Experte d'archivage** ne porte **aucune** de ces décisions — elle **exécute** la tâche technique confiée (archivage par dossier, ou commit + PR). L'**Agent de notifications** porte seulement le canal, sur sollicitation du coordinateur.

> **Précondition de séquencement — mettre à disposition seulement après la réalisation ET la revue.** La mise à disposition n'intervient **jamais** avant que les livrables aient été **réalisés** (`detailed-deliverables`) **et revus** — revue de cohérence (`detailed-deliverables`, `review_class: advisory`) puis revue de sécurité (`security-consistency-check`, `review_class: adversarial`) — **et validés par l'humain** (gate granulaire de [`consolidation-handoff`](consolidation-handoff.md)). C'est un **acte de fin de cycle** : il ne porte que sur des livrables produits, revus et validés — pas sur un travail en cours ni non revu.

### Step 1 — Demande explicite de commit + PR (systématique)

Le **coordinateur pose toujours** à l'humain une **demande explicite et distincte** : « **commit + PR : oui ou non ?** ». La validation granulaire des livrables au stage précédent **ne vaut jamais** accord implicite pour le commit ou la PR : ce sont **deux gates séparés**. La demande est posée **que le projet soit Git ou non** ; si le projet n'est pas sous Git (`Git : Non` consigné en Initialization — [`../initialization/git-detection.md`](../initialization/git-detection.md)), le commit/PR est sans objet et seul le fallback archivage s'applique.

### Step 2 — Si OUI : mise à disposition par Git (commit + PR)

Le coordinateur confie à l'**Experte d'archivage** la tâche technique suivante, dont il a résolu lui-même les paramètres :

- **Commiter tous les fichiers liés à la tâche et à l'ensemble de ses sous-tâches** — pas seulement le dernier livrable validé, mais l'intégralité des fichiers produits par la tâche et ses sous-tâches.
- **Créer une Pull Request** depuis la branche d'issue (`feature/<id-issue>-<slug-court>` créée en Initialization) vers la **branche cible**.
- **Résolution de la branche cible par le coordinateur**, dans cet ordre de priorité :
  1. `branche GIT: <nom>` présent dans la **description du projet** (prioritaire) ;
  2. sinon `branche GIT: <nom>` présent dans le **README du projet** ;
  3. sinon **`integration`** par défaut.

Le coordinateur transmet à l'Experte d'archivage la branche cible déjà résolue ; l'Experte exécute le commit + la PR via sa capacité Git ([`../../../agents/archiving-agent.md`](../../../agents/archiving-agent.md)) et remonte le **lien de PR** et un récapitulatif sur l'issue.

### Step 3 — Si NON : fallback archivage par dossier

Pas de commit ni de PR. Le coordinateur confie à l'**Experte d'archivage** le téléversement, la visualisation, le téléchargement et l'archivage des documents validés dans le répertoire du projet (zip + `multica attachment upload`) ; fournir à l'humain un récapitulatif accessible.

### Step 4 — Notification de fin de réalisation (dès la mise à disposition)

**Dès que la mise à disposition est effectuée** (Step 2 ou Step 3), le coordinateur sollicite l'**Agent de notifications** (il **ne notifie pas lui-même** — le workflow porte le déclenchement, l'Agent porte le canal). Le message informe que **l'issue a été réalisée** et que des **fichiers (archive) ou une PR sont en attente** :

- **l'issue a été réalisée et revue** ;
- **ce qui est en attente** : une **PR** (fournir le lien si disponible) ou des **fichiers / une archive** mis à disposition ;
- identifiant de l'issue et lien si possible ; **aucun secret** dans la notification.

Cette notification est **avancée au moment de la mise à disposition** (fin de Construction), avant tout déploiement : elle est distincte de la notification post-déploiement d'Operation ([`../operation/completion-notification.md`](../operation/completion-notification.md)), qui reste conditionnelle au déploiement.

## Sensors

Outputs: livrables mis à disposition (archive par dossier ou commit + PR) + notification de fin de réalisation envoyée. Frontière **Construction → Operation** : gate `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin`.
Imports: `required-sections`.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : ce stage **porte un gate humain granulaire** — le coordinateur y remonte les candidats-règles capturés sur la mise à disposition (choix PR / archivage, résolution de branche cible, format de notification), formulés en règles courtes ; l'humain garde ✅ / rejette ❌ / reformule 💬 chaque candidat séparément ; persistance des apprentissages **confirmés** dans `core/rules/` (application au prochain workflow).
