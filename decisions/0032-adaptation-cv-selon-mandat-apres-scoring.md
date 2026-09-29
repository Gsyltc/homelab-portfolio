# Adaptation du CV des collaborateurs selon le mandat (AO) après scoring, sur décision humaine

---
auteurs: Mika (agent)
accepté par :
accepté le :
supersedes: ""
superseded_by: ""

---

## Status

Proposed

## Contexte

Le workflow `matching-cv-ao` s'arrête aujourd'hui, côté production de CV, sur une **mise à jour générique** du CV livrable (stage `mise-a-jour-cv`, phase Clôture) : mise à jour des données validées lors du matching + production d'un CV livrable DOCX à partir d'un gabarit fourni. Cette étape **n'adapte pas le CV aux termes d'un AO précis** : elle ne réordonne ni ne met en avant les éléments les plus corrélés au mandat, et ne produit pas de **copie dédiée à l'AO** distincte du CV « catalogue ».

L'humain qui pilote un matching a exprimé un besoin nouveau, en aval du scoring :

1. Lorsqu'un collaborateur obtient un **score global supérieur à 75**, le **leader de l'équipe** (Coordinateur Matching) doit **demander à l'humain si une adaptation du CV au mandat est nécessaire** — c'est une **étape supplémentaire** du workflow, qui intervient **après le scoring**.
2. Si l'humain souhaite des versions adaptées, **seuls les CV des collaborateurs ayant un score > 75 sont éligibles** ; l'humain choisit **quels CV éligibles adapter** (sélection granulaire, pas un traitement en masse).
3. Une fois la demande **reçue et validée** par l'humain, le Coordinateur **délègue l'adaptation au Gestionnaire CV** :
   - l'adaptation doit **s'aligner sur les termes de l'AO** (vocabulaire, exigences, profils recherchés) ;
   - elle doit **faire ressortir les éléments à la plus forte correspondance** avec le mandat.
4. L'humain doit pouvoir **voir les différences apportées** dans le CV afin de **valider les ajouts** (diff avant/après clair).
5. Le **CV original n'est jamais modifié** : l'adaptation produit une **copie spécifique** nommée `<date>-<collaborateur>-<titre-ao>`, au **format DOCX récent**.

Ce besoin n'est couvert par aucun stage existant. Il touche trois surfaces du triptyque : le **workflow** (nouveau stage + wiring des phases), une **compétence** (`cv-generation`, qui porte la production de CV) et deux **agents** (Coordinateur Matching pour l'orchestration de la nouvelle gate, Gestionnaire CV pour l'exécution de l'adaptation).

Contraintes de cohérence avec l'existant à respecter :

- **Pondération de scoring immuable** (50/35/10/5) : l'adaptation ne touche **pas** au scoring ; le seuil `> 75` est un **critère d'éligibilité à l'adaptation**, pas une modification du score.
- **Gouvernance A2A** (`governance-security`) : délégation = JSON de mission joint + commentaire minimal à mention active ; présentation humaine = Markdown détaillé aux gates.
- **Invariants non contournables** : validation humaine granulaire, piste d'audit sur l'issue, aucune action à impact sans validation humaine explicite, ne rien inventer.
- **Enracinement `${ROOT_DIRECTORY}`** et **format DOCX depuis un gabarit fourni** (jamais inventé ; gabarit absent ⇒ halt-and-ask) — règles portées par `conductor.md` et `cv-generation`.

## Décision

Introduire une **étape d'adaptation du CV au mandat**, conditionnelle et pilotée par l'humain, en aval du scoring, sans altérer le scoring ni la mise à jour générique existante.

- **DEC-001 — Nouveau stage `adaptation-cv` (phase Clôture, conditionnel).** Ajouter la fiche `matching-cv-ao/common/stages/cloture/adaptation-cv.md`.
  - `phase: cloture`, `execution: CONDITIONAL`, `condition: "Adaptation de CV au mandat demandée par l'humain pour un ou des collaborateurs éligibles (score > 75)"`.
  - `lead_agent: Gestionnaire CV`, `mode: subagent`, `human_gate: explicit`.
  - `for_each: cv-adaptation-demande` — **une exécution par CV adapté** retenu par l'humain (validation granulaire par CV).
  - `produces: [cv-adapte]`, `consumes: [{artifact: resultats-valides, required: true}, {artifact: resume-ao, required: true}]`, `requires_stage: [presentation-resultats]`.
  - `scopes: [standard, complex, express]` (hors `format-cv` : pas d'AO, donc pas d'adaptation au mandat).

- **DEC-002 — Gate d'éligibilité et de choix humain, portée par le Coordinateur.** Le déclenchement de l'adaptation est une **gate humaine explicite** tenue par le Coordinateur Matching (le « leader de l'équipe »), placée **après la présentation des résultats / le scoring** :
  1. le Coordinateur calcule l'ensemble **éligible** = collaborateurs dont le **score global > 75** (seuil strict) ;
  2. s'il est **vide**, l'étape est **sautée** (pas de question inutile) ;
  3. sinon, le Coordinateur **présente la liste éligible** (nom, score, meilleure correspondance) et **demande à l'humain** : (a) une adaptation est-elle souhaitée ? (b) si oui, **quels CV éligibles adapter** (sélection par collaborateur, Keep/Modify/Redo) ;
  4. seuls les CV **explicitement choisis** par l'humain donnent lieu à une instance de `cv-adaptation-demande` transmise au Gestionnaire CV. **Aucune adaptation autonome.**

- **DEC-003 — Nouveau type d'opération dans la compétence `cv-generation` : « Adaptation d'un CV au mandat ».** Étendre `plugins/rh-assistant/skills/cv-generation/SKILL.md` avec une opération d'adaptation qui :
  - part de la **dernière analyse JSON** du collaborateur et du **résumé JSON de l'AO** (`resume-ao`, exigences + profils recherchés + vocabulaire) ;
  - **aligne le CV sur les termes de l'AO** (terminologie, intitulés d'exigences, profils recherchés) et **fait ressortir les éléments à plus forte correspondance** (réordonnancement, mise en avant des compétences/expériences couvrant les exigences) — **sans inventer** de compétence, d'expérience ou de durée absente des données (donnée manquante ⇒ mention humaine) ;
  - produit un **diff avant/après lisible** (éléments mis en avant, réordonnés, reformulés au vocabulaire de l'AO) présenté à l'humain **avant écriture**, pour validation des ajouts (invariant : aucune écriture avant accord explicite) ;
  - écrit une **copie spécifique dédiée à l'AO**, **jamais** en écrasant le CV catalogue ni les données d'analyse.

- **DEC-004 — Nommage et format de la copie adaptée.** La copie adaptée est un **DOCX** produit depuis un **gabarit fourni** (par défaut le format client `format-client-<client>.docx` si l'AO l'impose, sinon CV long ; gabarit absent ⇒ halt-and-ask, pas de repli Markdown automatique), nommée :

  `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/<AAAA-MM-JJ>-<nom-prenom>-<titre-ao-slug>.docx`

  où `<titre-ao-slug>` est le titre de l'AO normalisé (minuscules, tirets). Le **CV original / catalogue et les données d'analyse JSON ne sont pas modifiés** par l'adaptation (la copie adaptée est un livrable **dérivé et daté**, versionné sans écrasement de l'historique).

- **DEC-005 — Orchestration dans le `conductor.md` et wiring des phases.** Insérer `adaptation-cv` dans la phase **Clôture**, **après** `presentation-resultats` (donc après scoring et validation des profils) et **en amont ou en parallèle** de `livraison` selon l'ordre retenu à l'implémentation ; documenter la nouvelle gate dans la séquence A2A du conductor (le Coordinateur porte la question d'éligibilité/choix ; le Gestionnaire CV exécute l'adaptation par CV retenu). Mettre à jour les tableaux de phases/stages (README workflow + conductor) et le guide d'utilisation (`docs/guide-utilisation-workflow-matching.md`).

- **DEC-006 — Mise à jour des fiches d'agents (slim).** Compléter :
  - **Coordinateur Matching** — responsabilité d'ouvrir la **gate d'adaptation** (éligibilité `> 75`, question à l'humain, collecte du choix granulaire) et de déléguer `adaptation-cv` par CV retenu ;
  - **Gestionnaire CV** — responsabilité d'**exécuter l'adaptation au mandat** via la compétence `cv-generation` (nouvelle opération), en produisant la copie dédiée à l'AO et le diff de validation.

  Les fiches restent **slim** ; le détail opératoire vit dans la compétence `cv-generation` (source unique) et la fiche de stage.

- **DEC-007 — Séparation stricte adaptation ↔ mise à jour générique.** L'adaptation au mandat (`adaptation-cv`) est **distincte** de la mise à jour générique du CV (`mise-a-jour-cv`) : la première produit une **copie datée liée à un AO** mettant en avant la correspondance au mandat ; la seconde met à jour le **CV catalogue** avec les données validées. Les deux ne se confondent jamais et peuvent coexister dans la phase Clôture.

## Conséquences

### Positives

- **POS-001** : le besoin humain est couvert de bout en bout — question d'adaptation après scoring, éligibilité `> 75`, choix granulaire, adaptation au mandat, diff de validation, copie DOCX dédiée non destructive.
- **POS-002** : **aucune régression** sur le scoring (pondération immuable préservée) ni sur la mise à jour générique existante (`mise-a-jour-cv` inchangé dans son rôle).
- **POS-003** : **non destructif et auditable** — copie datée dédiée à l'AO, original/catalogue et JSON d'analyse intacts, diff présenté et validé, piste d'audit sur l'issue.
- **POS-004** : cohérent avec la gouvernance existante — gate humaine explicite, délégation A2A par JSON joint, format DOCX depuis gabarit fourni, enracinement `${ROOT_DIRECTORY}`, « ne rien inventer ».
- **POS-005** : détail opératoire centralisé dans `cv-generation` (source unique), fiches d'agents restant slim — pas de duplication.

### Négatives

- **NEG-001** : une **gate humaine supplémentaire** en Clôture allonge le parcours. Atténuation : la gate est **sautée** si aucun collaborateur n'a un score `> 75`, et le choix est granulaire (l'humain n'adapte que ce qu'il veut).
- **NEG-002** : dépendance renforcée aux **gabarits fournis** (une copie liée à un AO utilise souvent le format client). Atténuation : règle inchangée — gabarit absent ⇒ halt-and-ask, jamais de gabarit inventé.
- **NEG-003** : risque de **confusion copie adaptée ↔ CV catalogue**. Atténuation : nommage explicite `<date>-<collaborateur>-<titre-ao>`, DEC-007 posant la séparation stricte des deux stages.

## Alternatives étudiées

### ALT-001 — Étendre le stage existant `mise-a-jour-cv` au lieu de créer `adaptation-cv`

Ajouter la logique d'adaptation au mandat directement dans `mise-a-jour-cv`.

**Raison du rejet** : `mise-a-jour-cv` a une sémantique différente (mise à jour du **CV catalogue** avec les données validées, sans notion de mandat ni de copie datée). Y greffer l'adaptation mélangerait deux intentions, brouillerait la condition d'exécution (générique vs conditionnelle au score `> 75` + choix humain) et le nommage des livrables. Un stage dédié garde chaque intention lisible (DEC-007).

### ALT-002 — Placer la gate d'éligibilité/adaptation en phase Matching (juste après le scoring)

Déclencher la question dès la fin du scoring, en phase Matching.

**Raison du rejet** : la phase Matching est désormais `human_gate: none` (le rapport de scores et la décision humaine sur les profils sont portés en phase Validation — voir README workflow). Introduire une gate humaine en Matching contredirait ce choix. La question d'adaptation s'appuie sur des **profils déjà validés** (score consolidé, exclusions traitées) : sa place naturelle est **après** `presentation-resultats`, en Clôture.

### ALT-003 — Adapter automatiquement tous les CV avec score > 75, sans demander à l'humain

Produire les copies adaptées pour tous les éligibles sans gate.

**Raison du rejet** : viole l'invariant « aucune action à impact sans validation humaine explicite » et le besoin exprimé (« il faut demander à l'humain quels sont les CV éligibles à adapter »). L'adaptation reste **sur décision et choix granulaire de l'humain**.
