# Score chiffré par profil recherché (option différée)

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : ""
supersedes: ""
superseded_by: ""

---

## Status

Proposed

> Statut **Proposed** — décision **traçée** à la demande de multica.gaston (EXPE-67, 2026-09-26) pour être **arbitrée plus tard**. La PR qui porte cet ADR est **immédiate et sans gate humaine** (traçage de l'option), mais **l'implémentation n'est PAS engagée** : elle est portée par une **issue séparée placée en Backlog**, où l'humain décidera s'il applique. Ce document décrit le périmètre, l'impact et les alternatives — il ne modifie aucun fichier du workflow tant qu'il n'est pas passé `Accepted`.

## Contexte

Sur **EXPE-67** (AO MEQ 256490-S4-AP, Volet B, 2 profils recherchés), l'humain a validé une présentation **détaillée par profil** avec, dans le tableau de rappel, **une colonne verdict par profil** (recommandé, possible, etc.) — décision tracée dans [ADR-0029](0029-scoring-multi-profils-colonne-verdict-par-profil.md), à implémenter immédiatement.

Le modèle de scoring actuel produit **un score global unique par candidat**, calculé sur **l'union des exigences du volet** (pondération immuable Compétences 50 % · Expérience 35 % · Études 10 % · Disponibilité 5 %). La couverture par profil recherché est aujourd'hui exprimée **qualitativement** (fort / pertinent / partiel → verdict recommandé / possible / déconseillé), sans **score chiffré propre à chaque profil**.

Une évolution plus ambitieuse a été identifiée : produire un **score /100 distinct par profil recherché** de l'AO (PR-001, PR-002, …), calculé sur le **sous-ensemble d'exigences propre à ce profil**, en plus (ou à la place) du verdict qualitatif. Cette option est **plus lourde** et **différée** : l'humain veut d'abord **voir les changements qu'elle implique** avant de décider.

## Décision

**Décision proposée (non engagée)** : introduire un **score chiffré par profil recherché** dans le workflow de matching, en complément du score global par candidat.

Périmètre pressenti (à valider si passage `Accepted`) :

1. **Calcul par sous-ensemble d'exigences.** Pour chaque profil recherché, ne prendre en compte que **les exigences de ce profil** (exigences minimales + atouts propres au profil) au lieu de l'union du volet. La pondération des critères (50/35/10/5) resterait immuable **à l'intérieur** de chaque score par profil.
2. **Schéma JSON étendu.** L'artefact `matching-resultats` (produit par le Matcher) porterait, par candidat, un tableau `scores_par_profil` (`{profil_id, intitulé, score_total, détail par critère, recommandation}`) en plus du `score_total` global conservé pour compatibilité.
3. **Restitution.** Le tableau de rappel afficherait, par profil, **le score chiffré ET le verdict** (au lieu du seul verdict d'[ADR-0029](0029-scoring-multi-profils-colonne-verdict-par-profil.md)).

## Conséquences

### Positives

- **POS-001** : classement **par poste réellement chiffré** — pour un AO à N profils, on obtient le meilleur candidat de chaque poste sur une base quantitative, pas seulement qualitative.
- **POS-002** : lève la NEG-002 d'[ADR-0029](0029-scoring-multi-profils-colonne-verdict-par-profil.md) (verdict par profil aujourd'hui qualitatif) en l'appuyant sur un score.

### Négatives / coûts (raison du différé)

- **NEG-001** : impact **transverse** — modifie le Matcher (`matching-cv-ao/common/stages/matching/croisement-profils.md`), le skill `matching-scoring`, le schéma JSON de sortie, le stage `classement-profils` (agrégation par profil) et `presentation-resultats` (affichage). Beaucoup plus large que le changement présentationnel d'[ADR-0029](0029-scoring-multi-profils-colonne-verdict-par-profil.md).
- **NEG-002** : nécessite que l'Analyste RFP **rattache chaque exigence à un profil** (mapping exigence → profil) de façon fiable dans `ao-profils-recherches` ; les exigences transverses (communes à plusieurs profils) demandent une règle d'attribution.
- **NEG-003** : risque d'**incohérence** entre score global (union) et scores par profil (sous-ensembles) à expliquer à l'humain ; besoin de définir lequel fait foi pour l'affectation finale.
- **NEG-004** : nécessite un **re-test** du scoring sur des AO multi-profils existants (dont EXPE-67) pour vérifier la stabilité du classement.

## Alternatives étudiées

### ALT-001 — S'en tenir au verdict qualitatif par profil (ADR-0029 seul)

Conserver un score global unique + un verdict par profil dérivé de l'adéquation qualitative.

**Statut** : c'est l'**état retenu à court terme** ([ADR-0029](0029-scoring-multi-profils-colonne-verdict-par-profil.md), implémentée immédiatement). Le présent ADR-0030 n'est engagé que si l'humain décide d'aller plus loin.

### ALT-002 — Score par profil calculé par le Coordinateur à la présentation (sans toucher le Matcher)

Dériver un score par profil au moment de la présentation, sans modifier le Matcher ni le schéma JSON.

**Raison du rejet (pressenti)** : placerait un calcul de score **hors du Matcher**, en contradiction avec la séparation des rôles (le scoring appartient au Matcher, source unique). Non retenu, mais consigné.

## Notes d'implémentation

- **IMP-001** : **aucune modification de fichier** engagée par cet ADR tant qu'il est `Proposed`. Le détail des changements est porté par l'**issue B (Backlog)** créée à cet effet, pour que l'humain visualise l'ampleur avant de décider.
- **IMP-002** : si `Accepted`, séquence pressentie : (1) mapping exigence → profil dans `parse-ao` / `ao-profils-recherches` ; (2) calcul `scores_par_profil` dans le skill `matching-scoring` + stage `croisement-profils` ; (3) agrégation dans `classement-profils` ; (4) affichage chiffré dans `presentation-resultats` ; (5) re-test sur EXPE-67.
- **IMP-003** : passage `Proposed` → `Accepted` et renseignement de `accepté le` **uniquement** sur décision humaine explicite (issue B).

## Références

- **REF-001** : EXPE-67 — AO MEQ 256490-S4-AP, Volet B (2 profils) — contexte de la demande.
- **REF-002** : [ADR-0029 — Scoring multi-profils : détail par profil + colonne verdict par profil](0029-scoring-multi-profils-colonne-verdict-par-profil.md) — décision A, implémentée immédiatement ; ADR-0030 en est le prolongement optionnel.
- **REF-003** : `matching-cv-ao/common/stages/matching/croisement-profils.md` et le skill `matching-scoring` — points d'impact principaux si la décision est acceptée.
- **REF-004** : `matching-cv-ao/common/conductor.md` (§ Scoring pondéré) — pondération immuable 50/35/10/5, à préserver à l'intérieur de chaque score par profil.
