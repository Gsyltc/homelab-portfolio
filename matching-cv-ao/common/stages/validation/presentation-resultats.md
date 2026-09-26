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
Présenter chaque profil à l'humain pour validation granulaire (Keep/Modify/Redo par profil). **Gate humaine granulaire** : la présentation Markdown reste **DÉTAILLÉE, profil par profil** — l'humain lit le détail complet de chaque profil pour décider, pas un simple pointeur vers le JSON. Le JSON joint `classement-final` reste la source/piste d'audit.

> **Présentation détaillée (exigence humaine).** La réduction de prose vaut pour les échanges A2A (JSON joint), **pas** pour la présentation à l'humain aux gates. Le détail par critère, la recommandation et la justification sont **repris en clair** pour chaque profil.

> **Multi-profils (exigence humaine — [ADR-0029](../../../../decisions/0029-scoring-multi-profils-colonne-verdict-par-profil.md)).** Lorsqu'un AO comporte **plusieurs profils recherchés** (≥ 2 profils dans `ao-profils-recherches`), le scoring final est **toujours détaillé par profil** : une **section par profil recherché** (adéquation candidat par candidat) + un **tableau de rappel des scores globaux avec une colonne par profil portant le verdict** (recommandé, possible, etc.). Voir Steps 1bis / 1ter. Le score global reste **unique par candidat** (pondération immuable 50/35/10/5) ; le score chiffré par profil est une option **différée** ([ADR-0030](../../../../decisions/0030-scoring-chiffre-par-profil-recherche.md)).

## Steps
### Step 1 — Présentation profil par profil (DÉTAILLÉE)
Ouvrir la présentation par un **tableau de synthèse** (repris de l'ancien rapport de la Phase 2, désormais porté ici, à la seule gate de décision humaine) donnant en un coup d'œil :

- le **top des profils retenus** (score + recommandation) ;
- les profils **exclus** (`recommandation = "exclu"` — non-conformité études sur AO gouvernemental, avec motif) ;
- les profils **à vérifier** (`conformite_etudes.conforme = "a_verifier"`, MIFI non tranché) ;
- le rappel des **non-retenus d'éligibilité amont** (Gestionnaire CV — `exclu`/`a_verifier` avec raisons par axe : `localisation` > 70 km / ville manquante, `certifications` obligatoires non détenues, etc.).

Puis, pour chaque profil (dans l'ordre du classement `classement-final`), présenter en Markdown, **en clair**, le détail utile à la décision : **nom**, **score total**, **détail par critère** (compétences, expérience, études, disponibilité), **recommandation**, **justification**, et — pour un AO gouvernemental — le **statut de conformité des études** (et le motif si `exclu`). Terminer chaque profil par la **décision demandée** : ✅ Keep / 💬 Modify / ❌ Redo. Le JSON joint `classement-final` reste la source ; la présentation à l'humain le **reprend en clair**, elle ne se limite pas à le pointer.

### Step 1bis — Détail du scoring par profil recherché (OBLIGATOIRE si l'AO comporte ≥ 2 profils)
Lorsque l'AO comporte **plusieurs profils recherchés** (≥ 2 profils dans `ao-profils-recherches`), le scoring final est **toujours** détaillé par profil (exigence humaine — [ADR-0029](../../../../decisions/0029-scoring-multi-profils-colonne-verdict-par-profil.md)). Pour **chaque** profil recherché de l'AO (PR-001, PR-002, …), présenter en clair :

- le **rappel des exigences** du profil (exigences minimales + atouts) ;
- un **tableau d'adéquation candidat par candidat** — `Candidat | Adéquation | Couvert | Manquant` — où `Adéquation` reprend le **verdict du candidat pour CE profil** (`recommandé` / `possible` / `déconseillé`, avec nuance `fort` / `pertinent` / `partiel` si utile) ;
- le **classement du profil** (meilleur candidat pour ce poste).

Clore par le **tableau de rappel des scores globaux** au format « une colonne par profil = verdict » (Step 1ter). *(AO mono-profil : Step 1bis non applicable — la présentation par candidat du Step 1 suffit.)*

### Step 1ter — Tableau « Rappel — scores globaux » (une colonne par profil = verdict)
Le tableau de rappel des scores globaux comporte **une colonne par profil recherché de l'AO**, chaque cellule portant le **verdict du candidat pour ce profil** (`recommandé` / `possible` / `déconseillé` / `exclu`) — et non un verdict global unique. Conserver le **score global /100** et le **détail par critère** (pondération immuable 50/35/10/5) dans les premières colonnes ; ne pas altérer la pondération ni introduire de score chiffré par profil (option différée — [ADR-0030](../../../../decisions/0030-scoring-chiffre-par-profil-recherche.md)). Format :

```markdown
| Rang | Candidat | Score /100 | Comp. 50% | Exp. 35% | Études 10% | Dispo 5% | PR-001 <intitulé> | PR-002 <intitulé> | … |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **<nom>** | 77,2 | 67 | 92 | 80 | 70 | ✅ Recommandé | 🟡 Possible | … |
```

Une colonne est ajoutée **par profil recherché** de l'AO (intitulé abrégé `PR-00x <intitulé court>`) ; le verdict de chaque cellule est celui du candidat **pour ce profil**. Le verdict par profil est **dérivé de l'adéquation par profil** (Step 1bis) tant qu'aucun score chiffré par profil n'existe.

### Step 2 — Traitement des Modify/Redo
Sur Modify : ajuster et re-présenter **cet élément uniquement** (avec le même niveau de détail).
Sur Redo : proposer une alternative et relancer **cet élément uniquement** (présentation détaillée).
Ne jamais avancer sur un profil non validé.

### Step 3 — Synthèse des validations (piste d'audit)
Consigner sur l'issue l'artefact **JSON joint** `resultats-valides` (profils validés / rejetés / modifiés) et poster un commentaire **minimal** le référençant.

## Sensors
Outputs: `resultats-valides` → Phase Validation (gate: granular).
Imports: none.

## Learn
Documenter sur l'issue chaque validation/rejet par profil. Consigner les candidats-règles.
