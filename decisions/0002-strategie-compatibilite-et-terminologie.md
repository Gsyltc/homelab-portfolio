# Stratégie de compatibilité et terminologie

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

La refonte de `docs/core-workflow.md` vers AI-DLC 2.0 (voir [ADR-0001](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)) modifie la structure des phases et introduit de nouveaux mécanismes. Deux risques doivent être arbitrés avant l'exécution :

1. **Rupture de compatibilité** avec les issues et projets en cours qui référencent le workflow actuel (3 phases : Inception / Construction / Operations).
2. **Divergence de vocabulaire** entre les libellés historiques du workspace et la nomenclature AI-DLC 2.0.

Ces points ont été soumis à l'humain (arbitrages Q2 et Q3) et tranchés.

## Décision

**Compatibilité ascendante préservée** (arbitrage Q2 = Oui). La refonte n'invalide pas les références existantes :

- Les 3 phases actuelles se **mappent** sur les phases AI-DLC : Inception → Inception, Construction → Construction, Operations → Operation.
- Les phases **Initialization** et **Ideation** s'**ajoutent en amont** sans casser les parcours existants.
- Les nouveaux mécanismes (scopes, sensors, gates, learning loop) sont introduits en mode **advisory / opt-in** au départ, donc non bloquants pour les travaux déjà lancés.

**Adoption de la nomenclature AI-DLC 5 phases** (arbitrage Q3) : le document adopte les cinq noms de phases AI-DLC (`Initialization`, `Ideation`, `Inception`, `Construction`, `Operation`). Un **tableau de correspondance** conserve les libellés historiques comme alias, pour ne pas invalider la documentation et les habitudes existantes.

**Correction terminologique immédiate** : le libellé de la phase finale est corrigé de `Operations` (pluriel) vers `Operation` (singulier), conformément à la nomenclature AI-DLC et à l'instruction humaine explicite. Cette correction ponctuelle est appliquée dès le cadrage sur les occurrences du libellé de phase dans `core-workflow.md` ; le passage structurel complet à 5 phases reste réalisé au Stage 5.

## Conséquences

### Positives

- **POS-001** : Aucune rupture pour les issues/projets en cours référençant le workflow.
- **POS-002** : Vocabulaire aligné sur AI-DLC 2.0, cohérent avec la documentation AWS de référence.
- **POS-003** : Transition douce grâce aux alias et à l'introduction opt-in des nouveaux mécanismes.

### Négatives

- **NEG-001** : Maintien d'un tableau de correspondance (alias) à tenir à jour tant que les anciens libellés circulent.
- **NEG-002** : Coexistence temporaire de deux vocabulaires possible pendant la transition.

## Alternatives étudiées

### ALT-001 - Rupture nette (renommer sans alias, casser les références)

Adopter la nomenclature AI-DLC sans conserver les libellés historiques.

**Raison du rejet** : invaliderait la documentation et les références des travaux en cours (contraire à Q2 = Oui).

### ALT-002 - Statu quo terminologique (conserver Inception/Construction/Operations)

Garder le vocabulaire actuel sans adopter les noms AI-DLC.

**Raison du rejet** : maintient la divergence de vocabulaire avec la méthodologie cible (contraire à Q3).

## Notes d'implémentation

- **IMP-001** : Le tableau de correspondance des phases est intégré à `core-workflow.md` lors du passage aux 5 phases (Stage 5).
- **IMP-002** : La correction `Operations` → `Operation` porte sur les libellés de phase (vue d'ensemble, titre de phase, diagrammes Mermaid) sans altérer la sémantique de la phase.
- **IMP-003** : Critère de suivi : aucune référence existante cassée après la refonte ; alias documentés et traçables.

## Références

- **REF-001** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [AI-DLC workflows (awslabs)](https://github.com/awslabs/aidlc-workflows)
