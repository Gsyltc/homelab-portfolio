---
slug: consolidation-handoff
phase: construction
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecture Solution & Intégration
support_agents: [OpenSpec Expert]
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: granular
produces: [livrables_valides]
consumes: [{artifact: controle_securite_coherence, required: true}]
requires_stage: [security-consistency-check]
sensors: [required-sections]
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Livrables contrôlés"
outputs: "Livrables validés granulairement par l'humain ; attestation OpenSpec (specs relues/validées, fichiers présents et conformes) si activé — l'archivage OpenSpec est découplé de l'approbation et relève de l'après-déploiement (operation/deployment-under-validation). La mise à disposition (archivage par dossier / commit + PR) est portée par le stage suivant delivery-handoff."
---

# Consolidation et validation humaine

## Objectif

Valider granulairement les livrables restants ; la mise à disposition est portée par le stage suivant [`delivery-handoff`](delivery-handoff.md).

## Steps

### Step 1 — Validation granulaire humaine

De chaque livrable / choix restant à approuver (boucle Keep / Modify / Redo). Le `human_gate: granular` porte la force du gate ; aucune revue indépendante n'est déclarée à ce stade (`review_class: none`) — le contrôle sécurité a eu lieu au stage précédent. Une fois les livrables validés, la **mise à disposition** (archivage par dossier ou commit + PR) et la **notification de fin de réalisation** sont portées par le stage suivant [`delivery-handoff`](delivery-handoff.md).

### Step 2 — Attestation OpenSpec (approbation = validation, pas archivage)

> **L'approbation d'une spécification = achèvement de la Phase 2 (revue et validation), pas archivage.** À ce stade, l'**OpenSpec Expert n'archive pas** le changement.

L'**OpenSpec Expert** **atteste** que les specs sont **relues et validées** et que les **fichiers du change sont présents et conformes** (structure OpenSpec : `proposal.md` + `design.md` + `tasks.md` + `specs/<capability>/spec.md` ; EARS en MAJUSCULES ; `#### Scenario:`). Il **ne crée pas de sous-issue**, **ne produit pas** les mises à jour d'architecture et **n'archive pas**. L'**archivage OpenSpec est découplé de l'approbation** : fusion des deltas dans les specs vivantes (`openspec/specs/<capability>/spec.md`) et déplacement vers `openspec/changes/archive/`, il n'intervient qu'**après implémentation ET déploiement effectifs**, en phase Operation ([`../operation/deployment-under-validation.md`](../operation/deployment-under-validation.md)).

### Step 3 — Description des travaux de passation

L'**Expert OpenSpec** recense, dans le `design.md` et les specs, les éléments d'architecture et de documentation **susceptibles d'être impactés** (DAS, décision structurante, diagrammes, et au-delà). Pour chacun, il rédige une **description de passation auto-portante** : objet (ce que la spécification approuvée introduit / change), **nature pressentie du travail** (solution / logicielle, infrastructure, sécurité, données, AWS, etc. — indicatif), **renvoi vers les fichiers pertinents** (chemins relatifs : `proposal.md`, `design.md`, `specs/<capability>/spec.md`, ADR concernés) plutôt qu'une recopie exhaustive, et les décisions / contraintes amont héritées. Il **n'indique que ce que lui a réalisé** (la spécification, le change) et **transmet les informations** ; il **ne prescrit pas** les mises à jour à effectuer. Chaque description **précise explicitement** que le spécialiste / architecte destinataire doit **analyser les informations reçues et réaliser lui-même les mises à jour adéquates** (ajouts / modifications / suppressions d'éléments d'architecture et/ou documentaires) : l'**analyse et sa réalisation sont de la responsabilité du spécialiste / architecte**, pas de l'Expert OpenSpec. Ces descriptions constituent les **intrants** de cette analyse.

### Step 4 — Remontée au coordinateur

L'**Expert OpenSpec** passe l'issue en `done` et **remonte au coordinateur** par lien de mention actif, en lui transmettant les descriptions de passation du Step 3 (checklist de sortie de stage — [`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md)). Il ne poursuit pas lui-même le flux de production.

> **L'issue OpenSpec est un livrable terminal, pas une parente.** Une fois sa spécification approuvée (Phase 2 achevée : specs relues/validées, fichiers présents et conformes) et sa passation remontée, l'issue OpenSpec **reste `done`** : la remontée des descriptions de passation **ne la rouvre pas** et **n'en fait pas l'issue parente** des travaux d'architecture aval. L'**archivage OpenSpec n'a pas lieu ici** — il est découplé de l'approbation et relève de l'après-déploiement ([`../operation/deployment-under-validation.md`](../operation/deployment-under-validation.md)). Les sous-issues que le coordinateur crée au Step 5 ne sont **jamais** rattachées à l'issue OpenSpec (voir Step 5 pour le parent correct).

### Step 5 — Délégation des travaux par le coordinateur

Le **coordinateur** reçoit les descriptions de passation, **identifie la nature de chaque travail** et **délègue** aux spécialistes adéquats (solution / logicielle, infrastructure, sécurité, données, AWS, etc.) selon le « Cycle de livrable d'un spécialiste » ([`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md)) et le découpage de [`../inception/deliverables-breakdown.md`](../inception/deliverables-breakdown.md). Un même lot peut relever de **plusieurs natures** et donc de **plusieurs délégations**. Le coordinateur **ne produit pas** lui-même les livrables.

> **Rattachement correct des sous-issues de livrable.** Les sous-issues créées à partir de la passation sont des **livrables d'architecture aval**, au **même niveau** que l'issue OpenSpec dans la hiérarchie : elles se rattachent à l'**issue parente du découpage** — l'**issue ADR** sur impact structurant (`--parent <id-ADR>`), sinon l'**issue d'origine** —, **jamais à l'issue OpenSpec** (qui est elle-même une sous-issue de livrable, terminale et `done`). Prendre l'issue OpenSpec comme parent est une faute de flux : elle crée une hiérarchie livrable-sous-livrable incorrecte et peut rouvrir indûment l'issue OpenSpec via le garde-fou « issue parente bloquée ». Le coordinateur résout le bon parent (ADR / origine) avant de créer les sous-issues.

## Sensors

Outputs: livrables validés granulairement par l'humain (mise à disposition portée par le stage suivant [`delivery-handoff`](delivery-handoff.md)). Gate humain granulaire.
Imports: `required-sections`.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : ce stage **porte un gate humain granulaire** — le coordinateur y remonte les candidats-règles capturés en Construction, formulés en règles courtes ; l'humain garde ✅ / rejette ❌ / reformule 💬 chaque candidat séparément ; persistance des apprentissages **confirmés** dans `core/rules/` (application au prochain workflow).
