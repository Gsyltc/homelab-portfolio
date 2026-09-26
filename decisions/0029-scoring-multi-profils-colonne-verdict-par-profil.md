# Scoring multi-profils : détail par profil + colonne « verdict par profil » dans la présentation des résultats

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : 2026-09-26
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — décision de traçage demandée explicitement par multica.gaston (EXPE-67, 2026-09-26) avec **PR immédiate, sans gate humaine**. La décision est **documentaire et de présentation** : elle ne touche que la restitution Markdown à l'humain au stage `presentation-resultats` (Phase 3 — Validation). Elle **n'altère aucune** posture de sécurité, aucun invariant A2A, et surtout **pas la pondération immuable du scoring** (Compétences 50 % · Expérience 35 % · Études 10 % · Disponibilité 5 %) ni le calcul du score global unique par candidat.

## Contexte

Sur **EXPE-67** (AO MEQ 256490-S4-AP, focus **Volet B — Intégration**, **2 profils recherchés** : PR-001 Intégrateur d'infrastructures réseau, PR-002 Conseiller en architecture d'intégration), l'humain a demandé un matching des candidats retenus. Le stage `presentation-resultats` produit aujourd'hui :

- un **tableau de synthèse** (top des retenus : score global + recommandation unique) ;
- puis un **bloc détaillé par candidat** (détail par critère, recommandation, justification).

En réponse à une demande finale (« donne-moi les résultats **par profil** pour le Volet B, uniquement le matching, candidats retenus »), le Coordinateur a produit une restitution **plus riche** que ce que la fiche de stage codifie : une **section par profil recherché de l'AO** (adéquation candidat par candidat : Couvert / Manquant, classement du poste) et un tableau de rappel `Rappel — scores globaux Volet B (retenus)`.

L'humain a validé ce format et demandé **un seul ajustement** : dans le tableau de rappel, remplacer la colonne globale unique (« Profils visés » / recommandation unique) par **une colonne par profil recherché**, chaque cellule portant le **verdict du candidat pour ce profil** (recommandé, possible, etc.). Il souhaite en outre que ce **détail par profil devienne le standard** dès qu'un AO comporte **plusieurs profils** à matcher.

Le problème traité : la fiche `presentation-resultats` ne codifie ni l'**éclatement par profil recherché** en cas de multi-profils, ni le **format « une colonne par profil = verdict »** du tableau de rappel. Le bon format existait donc en pratique mais n'était pas garanti par le contrat de workflow.

## Décision

**Amender la fiche de stage `matching-cv-ao/common/stages/validation/presentation-resultats.md`** pour rendre standard, **dès qu'un AO comporte ≥ 2 profils recherchés**, une présentation détaillée par profil, et fixer le format du tableau de rappel :

1. **Déclencheur multi-profils.** Lorsque l'AO comporte **plusieurs profils recherchés** (≥ 2 profils dans `ao-profils-recherches`), le scoring final est **toujours détaillé par profil** — c'est une exigence humaine tracée ici, pas une option de scope.

2. **Section par profil recherché.** Pour **chaque** profil recherché de l'AO (PR-001, PR-002, …) : rappel des exigences (minimales + atouts), **tableau d'adéquation candidat par candidat** (`Candidat | Adéquation | Couvert | Manquant`, l'`Adéquation` reprenant le verdict du candidat pour CE profil), puis **classement du poste**.

3. **Tableau « Rappel — scores globaux » — une colonne par profil = verdict.** Le tableau de rappel comporte **une colonne par profil recherché de l'AO**, chaque cellule portant le **verdict du candidat pour ce profil** (`recommandé` / `possible` / `déconseillé` / `exclu`). Le **score global /100** et le **détail par critère** (pondération immuable 50/35/10/5) restent dans les premières colonnes. La colonne globale unique « recommandation / profils visés » est remplacée par ces colonnes par profil.

4. **Invariants préservés.** La pondération du scoring reste **immuable** ; le **score global reste unique par candidat** (calculé sur l'union des exigences du volet) — cette décision **n'introduit pas** de score chiffré par profil (traité séparément dans [ADR-0030](0030-scoring-chiffre-par-profil-recherche.md)). Le JSON `classement-final` reste la source d'audit ; seule la **restitution Markdown à l'humain** évolue.

## Conséquences

### Positives

- **POS-001** : le détail par profil est **garanti par le contrat** dès qu'un AO comporte plusieurs profils — plus de dépendance à une demande finale ad hoc de l'humain.
- **POS-002** : le tableau de rappel devient **lisible poste par poste** : pour un AO à N profils, on lit d'un coup d'œil quel candidat est recommandé/possible **pour chaque poste**, ce qui facilite l'affectation (ex. PR-001 → candidat X, PR-002 → candidat Y).
- **POS-003** : aucune modification de la pondération ni du calcul de score ; changement **strictement présentationnel** → risque de régression fonctionnelle nul.

### Négatives

- **NEG-001** : le tableau de rappel **s'élargit** avec le nombre de profils (une colonne par profil) ; sur un AO à nombreux profils, le tableau peut devenir large. Atténuation : l'intitulé de colonne est abrégé (`PR-00x <intitulé court>`).
- **NEG-002** : le **verdict par profil** doit être dérivable des données de matching (adéquation par profil). Aujourd'hui le `recommandation` du JSON est global ; le Coordinateur dérive le verdict par profil à partir de l'adéquation par profil décrite dans la présentation. Tant qu'un score chiffré par profil n'existe pas ([ADR-0030](0030-scoring-chiffre-par-profil-recherche.md)), ce verdict par profil reste un **jugement qualitatif** (fort/pertinent/partiel → recommandé/possible/déconseillé), pas un seuil chiffré.

## Alternatives étudiées

### ALT-001 — Ne rien changer au contrat, laisser le Coordinateur improviser le format par profil à la demande

Conserver `presentation-resultats` tel quel et compter sur une demande finale de l'humain pour obtenir le détail par profil.

**Raison du rejet** : le bon format ne serait pas garanti ; il dépendrait à chaque AO d'une relance humaine, à rebours de l'exigence explicite « détail systématique quand plusieurs profils ».

### ALT-002 — Introduire directement un score chiffré par profil

Calculer et afficher un score /100 distinct par profil recherché, au lieu d'un verdict qualitatif par profil.

**Raison du rejet** : changement **plus lourd** touchant le Matcher (`croisement-profils`) et le skill `matching-scoring` (calcul, schéma JSON, pondération par sous-ensemble d'exigences). L'humain a demandé, pour l'immédiat, **une colonne verdict par profil** ; le score chiffré par profil est tracé **séparément** dans [ADR-0030](0030-scoring-chiffre-par-profil-recherche.md) pour décision ultérieure.

## Notes d'implémentation

- **IMP-001** : `matching-cv-ao/common/stages/validation/presentation-resultats.md` — ajout d'une note « Multi-profils (exigence humaine) » à l'Objectif ; refonte du **Step 1** (présentation détaillée par candidat conservée) ; ajout d'un **Step 1bis** (section par profil recherché si ≥ 2 profils) et d'un **Step 1ter** (format du tableau « Rappel — scores globaux » avec une colonne par profil portant le verdict).
- **IMP-002** : aucun autre fichier du triptyque n'est modifié par cette décision. Le calcul du score (skill `matching-scoring`, stage `croisement-profils`) et la pondération immuable restent **inchangés**.
- **IMP-003** : décision de traçage avec **PR immédiate sans gate humaine** (demande explicite multica.gaston, EXPE-67, 2026-09-26). L'implémentation A est portée par une **issue dédiée en TODO (démarrage immédiat)**.

## Références

- **REF-001** : EXPE-67 — AO MEQ 256490-S4-AP, focus Volet B (2 profils), demande de détail par profil et de la colonne verdict par profil dans le tableau de rappel.
- **REF-002** : `matching-cv-ao/common/stages/validation/presentation-resultats.md` — fiche de stage amendée par cette décision.
- **REF-003** : `matching-cv-ao/common/stages/matching/classement-profils.md` — produit `classement-final` (source JSON de la présentation), inchangé.
- **REF-004** : [ADR-0030 — Score chiffré par profil recherché (option différée)](0030-scoring-chiffre-par-profil-recherche.md) — décision B, traçée pour arbitrage ultérieur.
