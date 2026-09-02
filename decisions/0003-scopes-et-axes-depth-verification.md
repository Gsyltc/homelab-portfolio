# Scopes et axes Depth / vérification des livrables

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

Le principe fondateur de `docs/core-workflow.md` — « le workflow s'adapte au travail » — était énoncé mais **non outillé** : l'adaptativité reposait sur le jugement subjectif du coordinateur et des agents, sans routage déterministe ni traçabilité. L'analyse comparative avec AI-DLC 2.0 (issue parente ALI-184, cadrage ALI-185, [ADR-0001](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)) a identifié deux écarts à combler au Stage 2 :

- **B** — AI-DLC formalise des scopes nommés + auto-détection par mots-clés + matrice stage × scope ; chez nous ce mécanisme était absent.
- **C** — AI-DLC sépare **Depth** (détail des artefacts) et **Test strategy** (volume de tests) en deux axes indépendants ; chez nous ils étaient mélangés (ancienne section « profondeur adaptative »).

Le dépôt de référence `awslabs/aidlc-workflows/core/scopes` définit 11 scopes (`bugfix, classic, enterprise, express, feature, infra, mvp, poc, refactor, security-patch, workshop`). Le workspace produit **majoritairement de la documentation d'architecture** (DAS, ADR, diagrammes) plutôt que du code applicatif, ce qui rend l'axe « test strategy » d'AI-DLC peu pertinent tel quel.

Les arbitrages ont été soumis à l'humain (Q-A à Q-F) et tranchés sur l'issue ALI-186.

## Décision

**Formaliser un mécanisme de scopes et deux axes d'exécution indépendants** dans `core-workflow.md`, dans le respect des invariants de gouvernance A2A du workspace.

**Table de scopes** (arbitrage Q-A = noms anglais, `mvp` réintégré) — 8 scopes : `standard` (défaut), `feature`, `infra`, `security-patch`, `mvp`, `poc`, `express`, `enterprise`. Les scopes `bugfix`, `refactor`, `classic` et `workshop` d'AI-DLC sont écartés (peu pertinents pour un workspace d'architecture documentaire, couverts par `feature` / `express` / `standard`).

**Scope par défaut** (arbitrage Q-B) : `standard`, en l'absence de mot-clé détecté — parcours d'architecture actuel, aucune régression, compatibilité ascendante ([ADR-0002](0002-strategie-compatibilite-et-terminologie.md)).

**Matrice stage × scope** (arbitrage Q-C = matrice validée) : chaque scope active, allège, ignore ou renforce les étapes du workflow. **Affectation des agents corrigée** pour référencer les rôles plutôt que les prénoms : contrôle sécurité par l'**Architecte cybersécurité** (`security-patch` : pilote), mise à disposition des livrables par le **Gestionnaire de document**. OpenSpec (Fabien) reste conditionnel.

**Auto-détection** (arbitrage Q-D = table validée + ligne `mvp` ajoutée) : détection par mots-clés FR / EN, confirmation explicite avant démarrage, et règle de désambiguïsation par ordre de priorité : `security-patch` > `enterprise` > `infra` > `feature` > `mvp` > `poc` > `express` > `standard`.

**Deux axes indépendants** (arbitrage Q-E = validé) :

- **Depth** (détail des artefacts) : `minimal` / `standard` / `comprehensive`.
- **Niveau de vérification des livrables** (rigueur du contrôle) : `advisory` / `standard` / `renforcé`. Cet axe **remplace** l'axe « test strategy » d'AI-DLC pour la documentation d'architecture, avec **repli sur une stratégie de tests dès qu'un livrable comporte du code ou de l'IaC**.

Les deux axes sont indépendants du scope et l'un de l'autre ; chaque scope porte des **valeurs par défaut** overridables.

**Points d'override** (arbitrage Q-F = validé) : à l'invocation, à la confirmation de scope, et à un gate. **Garde-fou sécurité** : tout niveau lié à la sécurité ne peut jamais être abaissé par un override — le contrôle sécurité minimal (OWASP / STRIDE) et, pour `security-patch` / `enterprise`, le niveau de vérification `renforcé`, constituent un plancher.

**Invariants non négociables** préservés quel que soit le scope : validation humaine granulaire, ADR sur décision structurante, piste d'audit sur l'issue, contrôle sécurité minimal.

## Conséquences

### Positives

- **POS-001** : Adaptativité réellement outillée — routage déterministe et auditable par scope, à la place d'un principe non appliqué.
- **POS-002** : Depth et vérification pilotables séparément, sans qu'un axe ne contraigne l'autre.
- **POS-003** : Axe de vérification adapté à un workspace documentaire, tout en restant compatible avec le sens AI-DLC (stratégie de tests) dès qu'il y a du code / de l'IaC.
- **POS-004** : Garde-fou explicite empêchant l'abaissement des niveaux de sécurité par override.
- **POS-005** : Base pour les Verification gates et Sensors du stage suivant (le niveau `renforcé` les préfigure).

### Négatives

- **NEG-001** : Table de scopes, matrice et mots-clés à maintenir à jour à mesure que le workflow évolue.
- **NEG-002** : Effort de cadrage supplémentaire au démarrage (détection + confirmation du scope, choix des axes).

## Alternatives étudiées

### ALT-001 - Reprise littérale des 11 scopes AI-DLC

Adopter tels quels les 11 scopes du dépôt de référence.

**Raison du rejet** : plusieurs scopes (`bugfix`, `refactor`, `classic`, `workshop`) sont orientés développement logiciel et peu pertinents pour un workspace d'architecture documentaire ; ils alourdissent la détection sans valeur ajoutée. Sélection de 8 scopes adaptés (arbitrage Q-A).

### ALT-002 - Conserver l'axe « test strategy » d'AI-DLC tel quel

Garder un axe centré sur le volume de tests unitaires / intégration / e2e.

**Raison du rejet** : le workspace produit majoritairement de la documentation, pas du code ; l'axe « niveau de vérification des livrables » couvre le cas documentaire et se replie sur une stratégie de tests quand du code existe (arbitrage Q-E).

### ALT-003 - Overrides libres sans garde-fou sécurité

Permettre l'ajustement des deux axes dans les deux sens sans restriction.

**Raison du rejet** : un abaissement du niveau de vérification sur un scope sécuritaire (`security-patch`, `enterprise`) affaiblirait la posture de sécurité. Un plancher non abaissable est imposé (arbitrage Q-F).

## Notes d'implémentation

- **IMP-001** : Le mécanisme est documenté dans la section « Scopes et axes d'exécution » de `docs/core-workflow.md`.
- **IMP-002** : Les Verification gates et Sensors déterministes (mécanismes E / F d'AI-DLC) sont introduits à un stage ultérieur ; le niveau de vérification `renforcé` en pose le cadre advisory.
- **IMP-003** : Le passage structurel aux 5 phases AI-DLC est traité à un stage ultérieur ; la matrice s'adossera alors à la nouvelle ossature de phases.
- **IMP-004** : Contrôle sécurité (Architecte cybersécurité) sur l'impact des scopes touchant la sécurité (`security-patch`, `enterprise`) sollicité lors de la conception détaillée.

## Références

- **REF-001** : [ADR-0001 - Alignement de core-workflow.md sur AI-DLC 2.0](0001-alignement-core-workflow-sur-ai-dlc-2.0.md)
- **REF-002** : [ADR-0002 - Stratégie de compatibilité et terminologie](0002-strategie-compatibilite-et-terminologie.md)
- **REF-003** : [AI-DLC workflows (awslabs) — core/scopes](https://github.com/awslabs/aidlc-workflows/tree/main/core/scopes)
