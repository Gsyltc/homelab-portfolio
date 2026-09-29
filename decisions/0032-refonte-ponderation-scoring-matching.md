# Refonte de la pondération du scoring matching (6 critères 45/30/10/5/5/5)

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : "2026-09-29"
supersedes: "0030-scoring-chiffre-par-profil-recherche"
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — changement **fonctionnel** de la pondération immuable du scoring, demandé et validé explicitement par multica.gaston (EXPE-71, 2026-09-29). La pondération du scoring est **immuable** : elle ne peut changer qu'avec une **validation humaine explicite tracée** — c'est précisément l'objet de cet ADR. Ce document **supersede** [ADR-0030](0030-scoring-chiffre-par-profil-recherche.md) : la pondération de référence à 4 critères (50/35/10/5) y est remplacée par une pondération à **6 critères (45/30/10/5/5/5)**.

## Contexte

La pondération immuable du scoring `matching-cv-ao` reposait jusqu'ici sur **4 critères** :

| Critère | Poids |
| --- | --- |
| Compétences (compétences + technologies + méthodologies) | 50 % |
| Expérience en projets | 35 % |
| Études | 10 % |
| Disponibilité | 5 % |

Cette répartition figeait la pondération dans la skill `matching-scoring` et dans plusieurs fichiers couplés du workflow (`conductor.md`, `README.md`, fiches d'agent et de stage, guide d'utilisation). Les **certifications** n'étaient pas un critère de scoring : les certifications `obligatoire` étaient (et restent) un **prérequis éliminatoire amont** (filtre d'éligibilité du Gestionnaire CV), et les certifications `souhaitée` alimentaient la couverture du critère Compétences. Les **langues** n'étaient pas évaluées comme critère.

multica.gaston a demandé (EXPE-71) une nouvelle répartition mettant davantage l'accent sur l'**expérience en projets** et introduisant deux critères dédiés (**Certifications**, **Langues**).

## Décision

**Adopter la pondération immuable à 6 critères suivante** (somme = 100 %) :

| Critère | Poids | Méthode |
| --- | --- | --- |
| Expérience en projets | **45 %** | Pertinence clients similaires + durée projets similaires |
| Compétences (compétences + technologies + méthodologies) | **30 %** | Couverture regroupée des compétences / technologies / méthodologies exigées par l'AO (fraîcheur ≤ 10 ans) |
| Études | **10 %** | Niveau de formation (après équivalence MIFI) |
| Certifications | **5 %** | Couverture des certifications `souhaitée` / nice-to-have de l'AO par les certifications détenues |
| Langues | **5 %** | Couverture des langues exigées ; **français exigé par défaut** si l'AO ne précise rien |
| Disponibilité | **5 %** | À partir de la date de disponibilité et du taux d'utilisation |

Règles de conception associées, validées par l'humain (EXPE-71) :

1. **Certifications `obligatoire` = éliminatoires en amont, non re-scorées.** Le critère Certifications (5 %) ne mesure que la couverture des certifications `souhaitée`. Un collaborateur exclu en amont pour certification `obligatoire` manquante n'est jamais réintégré ni re-scoré.
2. **Certifications sorties du critère Compétences.** Le critère Compétences (30 %) regroupe uniquement compétences + technologies + méthodologies ; les certifications relèvent désormais de leur critère dédié.
3. **Langues — français par défaut.** Si l'AO ne précise aucune exigence de langue, le critère Langues (5 %) considère le **français comme exigé par défaut**.
4. **Immutabilité préservée.** La nouvelle pondération reste **immuable** ; aucun scope, aucune règle apprise, ni la fraîcheur, ni la conformité des études ne la modifie. Seule une nouvelle validation humaine explicite tracée (nouvel ADR) pourrait la changer.

## Conséquences

### Positives

- **POS-001** : l'**expérience en projets** devient le critère prépondérant (45 %), conformément à la priorité métier exprimée.
- **POS-002** : les **certifications** et les **langues** sont désormais évaluées explicitement et de façon traçable, au lieu d'être noyées dans le critère Compétences (certifications) ou absentes (langues).
- **POS-003** : la traçabilité ADR est propre — le changement de pondération immuable est acté par une décision humaine, comme l'exigent les garde-fous de la skill.

### Négatives / points d'attention

- **NEG-001** : impact **transverse** — la pondération est répliquée dans plusieurs fichiers ; toute future évolution doit les mettre à jour de concert (voir Références).
- **NEG-002** : les scores calculés avec l'ancienne pondération (50/35/10/5) ne sont **pas comparables** aux nouveaux ; les livrables de matching antérieurs à ce changement gardent leur pondération d'origine (non recalculés).
- **NEG-003** : le critère Langues suppose que le profil porte un champ `langues[]` exploitable ; à défaut, le français par défaut s'applique côté exigence, mais l'absence de langue côté profil doit être traitée comme un écart.

## Alternatives étudiées

### ALT-001 — Conserver 4 critères et intégrer certifications/langues dans Compétences

Rejetée : ne répond pas à la demande d'un poids explicite pour l'expérience, les certifications et les langues, et masque ces dimensions dans un critère composite.

### ALT-002 — Faire des langues un critère éliminatoire plutôt qu'un poids

Non retenue : la demande porte sur une **pondération** (5 %), pas sur un filtre éliminatoire. Les langues restent donc un critère de scoring ; seule l'exigence gouvernementale d'études et les certifications `obligatoire` demeurent éliminatoires.

## Notes d'implémentation

- **IMP-001** : pondération et schéma JSON de sortie portés par la skill `plugins/rh-assistant/skills/matching-scoring/SKILL.md` (ajout des blocs `score_certifications` et `score_langues`, poids `0.45 / 0.30 / 0.10 / 0.05 / 0.05 / 0.05`).
- **IMP-002** : fichiers couplés mis à jour de concert — `matching-cv-ao/common/conductor.md`, `matching-cv-ao/README.md`, `matching-cv-ao/agents/matcher-profils-agent.md`, `matching-cv-ao/common/stages/matching/croisement-profils.md`, `matching-cv-ao/common/stages/validation/presentation-resultats.md`, `matching-cv-ao/common/stages/cloture/livraison.md`, `docs/guide-utilisation-workflow-matching.md`.
- **IMP-003** : entrée `CHANGELOG.md` (`[Non publié] → Changed`).
- **IMP-004** : l'option « score chiffré par profil recherché » d'[ADR-0030](0030-scoring-chiffre-par-profil-recherche.md) reste **différée** ; si elle est reprise, elle devra s'appuyer sur la pondération à 6 critères de cet ADR.

## Références

- **REF-001** : EXPE-71 — demande et validation du changement de pondération (multica.gaston, 2026-09-29).
- **REF-002** : [ADR-0030 — Score chiffré par profil recherché (option différée)](0030-scoring-chiffre-par-profil-recherche.md) — **superseded** par le présent ADR pour la pondération de référence.
- **REF-003** : [ADR-0029 — Scoring multi-profils : détail par profil + colonne verdict par profil](0029-scoring-multi-profils-colonne-verdict-par-profil.md) — présentation par profil ; invariant de pondération mis à jour vers 45/30/10/5/5/5.
- **REF-004** : `plugins/rh-assistant/skills/matching-scoring/SKILL.md` — source unique de la pondération immuable et du schéma JSON de scoring.
- **REF-005** : `matching-cv-ao/common/conductor.md` (§ Scoring pondéré) — pondération immuable 45/30/10/5/5/5.
