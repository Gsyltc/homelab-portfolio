---
slug: consolidation-handoff
phase: construction
execution: ALWAYS
condition: "Always executes"
lead_agent: Architecture Solution & Intégration
support_agents: [Experte d'archivage, OpenSpec Expert]
mode: inline
summary_confirmation: required
reviewer: null
review_class: none
human_gate: granular
produces: [livrables_valides_mis_a_disposition]
consumes: [{artifact: controle_securite_coherence, required: true}]
requires_stage: [security-consistency-check]
sensors: [required-sections]
scopes: [standard, feature, infra, security-patch, mvp, poc, express, enterprise]
inputs: "Livrables contrôlés"
outputs: "Livrables validés granulairement + mis à disposition (Experte d'archivage) ; archivage OpenSpec si activé"
---

# Consolidation, validation humaine et mise à disposition

## Objectif

Valider les livrables restants et les mettre à disposition.

## Steps

### Step 1 — Validation granulaire humaine

De chaque livrable / choix restant à approuver (boucle Keep / Modify / Redo). Le `human_gate: granular` porte la force du gate ; aucune revue indépendante n'est déclarée à ce stade (`review_class: none`) — le contrôle sécurité a eu lieu au stage précédent.

### Step 2 — Mise à disposition

Confier à l'**Experte d'archivage** le téléversement, la visualisation, le téléchargement et l'archivage des documents validés dans le répertoire du projet ; fournir à l'humain un récapitulatif accessible.

### Step 3 — Archivage OpenSpec

L'**OpenSpec Expert** archive le changement après approbation : fusion des deltas dans les specs vivantes (`openspec/specs/<capability>/spec.md`) et déplacement du change vers `openspec/changes/archive/`. Il **ne crée pas de sous-issue** et **ne produit pas** les mises à jour d'architecture.

### Step 4 — Description des travaux de passation

L'**Expert OpenSpec** recense, dans le `design.md` et les specs, les éléments d'architecture et de documentation **susceptibles d'être impactés** (DAS, décision structurante, diagrammes, et au-delà). Pour chacun, il rédige une **description de passation auto-portante** : objet (ce que la spécification approuvée introduit / change), **nature pressentie du travail** (solution / logicielle, infrastructure, sécurité, données, AWS, etc. — indicatif), **renvoi vers les fichiers pertinents** (chemins relatifs : `proposal.md`, `design.md`, `specs/<capability>/spec.md`, ADR concernés) plutôt qu'une recopie exhaustive, et les décisions / contraintes amont héritées. Il **n'indique que ce que lui a réalisé** (la spécification, le change) et **transmet les informations** ; il **ne prescrit pas** les mises à jour à effectuer. Chaque description **précise explicitement** que le spécialiste / architecte destinataire doit **analyser les informations reçues et réaliser lui-même les mises à jour adéquates** (ajouts / modifications / suppressions d'éléments d'architecture et/ou documentaires) : l'**analyse et sa réalisation sont de la responsabilité du spécialiste / architecte**, pas de l'Expert OpenSpec. Ces descriptions constituent les **intrants** de cette analyse.

### Step 5 — Remontée au coordinateur

L'**Expert OpenSpec** passe l'issue en `done` et **remonte au coordinateur** par lien de mention actif, en lui transmettant les descriptions de passation du Step 4 (checklist de sortie de stage — [`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md)). Il ne poursuit pas lui-même le flux de production.

> **L'issue OpenSpec est un livrable terminal, pas une parente.** Une fois sa spécification approuvée, archivée et sa passation remontée, l'issue OpenSpec **reste `done`** : la remontée des descriptions de passation **ne la rouvre pas** et **n'en fait pas l'issue parente** des travaux d'architecture aval. Les sous-issues que le coordinateur crée au Step 6 ne sont **jamais** rattachées à l'issue OpenSpec (voir Step 6 pour le parent correct).

### Step 6 — Délégation des travaux par le coordinateur

Le **coordinateur** reçoit les descriptions de passation, **identifie la nature de chaque travail** et **délègue** aux spécialistes adéquats (solution / logicielle, infrastructure, sécurité, données, AWS, etc.) selon le « Cycle de livrable d'un spécialiste » ([`../../protocols/stage-protocol.md`](../../protocols/stage-protocol.md)) et le découpage de [`../inception/deliverables-breakdown.md`](../inception/deliverables-breakdown.md). Un même lot peut relever de **plusieurs natures** et donc de **plusieurs délégations**. Le coordinateur **ne produit pas** lui-même les livrables.

> **Rattachement correct des sous-issues de livrable.** Les sous-issues créées à partir de la passation sont des **livrables d'architecture aval**, au **même niveau** que l'issue OpenSpec dans la hiérarchie : elles se rattachent à l'**issue parente du découpage** — l'**issue ADR** sur impact structurant (`--parent <id-ADR>`), sinon l'**issue d'origine** —, **jamais à l'issue OpenSpec** (qui est elle-même une sous-issue de livrable, terminale et `done`). Prendre l'issue OpenSpec comme parent est une faute de flux : elle crée une hiérarchie livrable-sous-livrable incorrecte et peut rouvrir indûment l'issue OpenSpec via le garde-fou « issue parente bloquée ». Le coordinateur résout le bon parent (ADR / origine) avant de créer les sous-issues.

## Sensors

Outputs: livrables validés et mis à disposition. Frontière **Construction → Operation** : gate `artefacts-presents` + `liaison-tracabilite` + `absence-orphelin`.
Imports: `required-sections`.

## Learn

Boucle d'apprentissage maison (voir [`core/rules/`](../../../rules/README.md)) : ce stage **porte un gate humain granulaire** — le coordinateur y remonte les candidats-règles capturés en Construction, formulés en règles courtes ; l'humain garde ✅ / rejette ❌ / reformule 💬 chaque candidat séparément ; persistance des apprentissages **confirmés** dans `core/rules/` (application au prochain workflow).
