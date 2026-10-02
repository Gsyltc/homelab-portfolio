---
slug: presentation-resultats
phase: validation
execution: ALWAYS
condition: "Always executes"
lead_agent: Coordinateur Matching
support_agents: []
mode: inline
summary_confirmation: none
reviewer: null
review_class: none
review_artifact: ""
human_gate: granular
produces: [resultats-valides]
consumes: [{artifact: classement-final, required: true}]
requires_stage: [classement-profils]
sensors: []
scopes: [standard, complex, express]
inputs: "Classement final"
outputs: "Profils validés par l'humain"
---

# Présentation des résultats

## Objectif
Présenter chaque profil à l'humain pour validation granulaire (Keep/Modify/Redo par profil). **Gate humaine granulaire** : la présentation Markdown reste **DÉTAILLÉE, profil par profil** — l'humain lit le détail complet de chaque profil pour décider, pas un simple pointeur vers le JSON. Le YAML joint `classement-final` reste la source/piste d'audit.

> **Présentation détaillée (exigence humaine).** La réduction de prose vaut pour les échanges A2A (YAML joint), **pas** pour la présentation à l'humain aux gates. Le détail par critère, la recommandation et la justification sont **repris en clair** pour chaque profil.

> **Multi-profils (exigence humaine).** Lorsqu'un AO comporte **plusieurs profils recherchés** (≥ 2 profils dans `ao-profils-recherches`), le scoring final est **toujours détaillé par profil** : une **section par profil recherché** (adéquation candidat par candidat) + un **tableau de rappel des scores globaux avec une colonne par profil portant le verdict**, et une **colonne « Type »** (pigiste / interne / offre conditionnelle). Voir Steps 1bis / 1ter. Le score global reste **unique par candidat** (pondération immuable définie dans la compétence `matching-scoring`) ; le score chiffré par profil n'est **pas** introduit ici (option différée). La colonne « Type » est **informative** et n'entre pas dans le score.

## Steps
### Step 1 — Présentation profil par profil (DÉTAILLÉE)
Ouvrir la présentation par un **tableau de synthèse** (repris de l'ancien rapport de la Phase 2, désormais porté ici, à la seule gate de décision humaine) donnant en un coup d'œil :

- le **top des profils retenus** (score + recommandation), avec une **colonne « Type »** identifiant le statut de chaque collaborateur — **pigiste / interne / offre conditionnelle** (dérivée de `type_collaborateur`) : cette colonne figure **dans tous les cas**, y compris pour un AO mono-profil où le Step 1ter ne s'applique pas ;
- les profils **exclus** (`recommandation = "exclu"` — non-conformité études sur AO gouvernemental, avec motif) ;
- les profils **à vérifier** (`conformite_etudes.conforme = "a_verifier"`, MIFI non tranché) ;
- le rappel des **non-retenus d'éligibilité amont** (Gestionnaire CV — `exclu`/`a_verifier` avec raisons par axe : `localisation` > 70 km / ville manquante, `certifications` obligatoires non détenues, etc.).

Puis, pour chaque profil (dans l'ordre du classement `classement-final`), présenter en Markdown, **en clair**, le détail utile à la décision : **nom**, **type de collaborateur** (pigiste / interne / offre conditionnelle / recrutement) et **rémunération** (taux horaire $CAD/h pour un pigiste, salaire annuel $CAD/an pour un interne / une offre conditionnelle, lorsque connue), **score total**, **détail par critère** (expérience, compétences, études, certifications, langues, disponibilité), **recommandation**, **justification**, et — pour un AO gouvernemental — le **statut de conformité des études** (et le motif si `exclu`). Terminer chaque profil par la **décision demandée** : ✅ Keep / 💬 Modify / ❌ Redo. Le YAML joint `classement-final` reste la source ; la présentation à l'humain le **reprend en clair**, elle ne se limite pas à le pointer.

### Step 1bis — Détail du scoring par profil recherché (OBLIGATOIRE si l'AO comporte ≥ 2 profils)
Lorsque l'AO comporte **plusieurs profils recherchés** (≥ 2 profils dans `ao-profils-recherches`), le scoring final est **toujours** détaillé par profil (exigence humaine). Pour **chaque** profil recherché de l'AO (PR-001, PR-002, …), présenter en clair :

- le **rappel des exigences** du profil (exigences minimales + atouts) ;
- un **tableau d'adéquation candidat par candidat** — `Candidat | Adéquation | Couvert | Manquant` — où `Adéquation` reprend le **verdict du candidat pour CE profil** (`recommandé` / `possible` / `déconseillé`, avec nuance `fort` / `pertinent` / `partiel` si utile) ;
- le **classement du profil** (meilleur candidat pour ce poste).

Clore par le **tableau de rappel des scores globaux** au format « une colonne par profil = verdict » (Step 1ter). *(AO mono-profil : Step 1bis non applicable — la présentation par candidat du Step 1 suffit.)*

### Step 1ter — Tableau « Rappel — scores globaux » (une colonne par profil = verdict)
Le tableau de rappel des scores globaux comporte une **colonne « Type »** (statut du collaborateur : **pigiste / interne / offre conditionnelle** — dérivée de `type_collaborateur` : `pigiste` → « Pigiste », `alithya` → « Interne », `offre_conditionnelle` → « Offre conditionnelle », `recrutement` → « Recrutement ») et **une colonne par profil recherché de l'AO**, chaque cellule de profil portant le **verdict du candidat pour ce profil** (`recommandé` / `possible` / `déconseillé` / `exclu`) — et non un verdict global unique. Conserver le **score global /100** et le **détail par critère** (pondération immuable définie dans `matching-scoring`) dans les premières colonnes ; ne pas altérer la pondération ni introduire de score chiffré par profil (option différée). La colonne « Type » est **informative** (identification pigiste/interne/offre conditionnelle), elle n'entre **pas** dans le score. Le tableau ci-dessous illustre le format de restitution (colonne Type + une colonne par critère + une colonne par profil recherché) :

```markdown
| Rang | Candidat | Type | Score /100 | Exp. 45% | Comp. 30% | Études 10% | Cert. 5% | Langues 5% | Dispo 5% | PR-001 <intitulé> | PR-002 <intitulé> | … |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **<nom>** | Pigiste | 77,2 | 92 | 67 | 80 | 60 | 90 | 100 | ✅ Recommandé | 🟡 Possible | … |
```

Une colonne est ajoutée **par profil recherché** de l'AO (intitulé abrégé `PR-00x <intitulé court>`) ; le verdict de chaque cellule est celui du candidat **pour ce profil**. Le verdict par profil est **dérivé de l'adéquation par profil** (Step 1bis) tant qu'aucun score chiffré par profil n'existe. La **colonne « Type »** reprend `type_collaborateur` du candidat (pigiste / interne / offre conditionnelle / recrutement), propagé depuis le CV via `matching-resultats` → `classement-final`.

### Step 2 — Traitement des Modify/Redo (boucle bornée)
Avant de traiter le premier Modify/Redo d'un profil, **fixer et annoncer sa condition de sortie** (aucun profil n'entre en boucle sans condition de terminaison explicite définie en tête de boucle).

- Sur Modify : ajuster et re-présenter **cet élément uniquement** (avec le même niveau de détail).
- Sur Redo : proposer une alternative et relancer **cet élément uniquement** (présentation détaillée).
- **`max_iterations` par profil = 3** tours Modify/Redo (compteur unique Modify+Redo, tenu et **tracé sur l'issue** à chaque tour).
- **Condition de sortie (un profil est *terminé* quand)** : **Keep**, **OU** exclusion actée, **OU** `max_iterations` atteint → **arbitrage humain**.
- **Au-delà du cap : halt-and-ask, pas de relance.** À `max_iterations` atteint sans validation, **cesser toute relance** et interroger explicitement l'humain (mention active) pour trancher : **garder le profil en l'état / l'exclure / consigne précise**. Ne jamais relancer un tour de plus de soi-même après le cap.

Ne jamais avancer sur un profil non validé. Ce bornage ne modifie **jamais** la pondération immuable (`matching-scoring`). Définition transverse complète : `conductor.md` § « Bornage de la boucle ».

### Step 3 — Synthèse des validations (piste d'audit)
Consigner sur l'issue l'artefact **YAML joint** `resultats-valides` (profils validés / rejetés / modifiés) et poster un commentaire **minimal** le référençant.

## Sensors
Outputs: `resultats-valides` → Phase Validation (gate: granular).
Imports: none.

## Learn
Documenter sur l'issue chaque validation/rejet par profil. Consigner les candidats-règles.
