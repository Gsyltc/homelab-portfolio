---
auteurs: Sylvain Goubaud
parties_prenantes: ""
accepte_par: Sylvain Goubaud
accepte_le: "2026-11-03"
supersedes: ""
superseded_by: ""
---

# Checklist d'architecture — sections requises par livrable et suivi de l'architecture de sécurité

## Status

Accepted

> Statut **Accepted** — validation humaine granulaire explicite obtenue (multica.gaston, ORIG-387, 2026-11-03) sur les quatre arbitrages : structure de la section « Frontières de confiance » du gabarit `11` (modèle Talent Match, diagramme embarqué), STRIDE portée par `02-menaces-stride`, checklist sans rappel de calcul, et sections requises portées par `required-sections` seul (pas de liste dans le protocole). Le changement est **documentaire** : il ajoute des sections requises et retire de la checklist le rappel des calculs ; il ne modifie aucune posture de sécurité, aucun gate de phase et ne rend aucun sensor bloquant. Les invariants SG-1 à SG-6 sont préservés (surface versionnée, tracée, advisory).

## Contexte

L'ADR [`0043`](0043-checklist-architecture-avancement-en-pourcentage-bareme-80-10-10.md) a fixé le barème 80/10/10 de la checklist d'architecture et laissé le **contrat des sections** au sensor [`required-sections`](../core/sensors/sensors/required-sections.md). Pour l'**architecture de sécurité détaillée**, ce contrat ne couvrait que deux rubriques du fichier `11-securite.md` (STRIDE, sécurité applicative) : le chapitre d'architecture de sécurité (`architecture-securite/`) — surfaces d'attaque, modélisation STRIDE par surface, risques OWASP — n'était **ni requis ni décompté**, et les frontières de confiance n'étaient suivies nulle part alors qu'elles conditionnent la lecture des menaces.

Sur le projet OAI-DLC, la revue de la checklist a montré deux écarts :

1. **Sections manquantes au contrat.** L'humain (multica.gaston, ORIG-387) demande de suivre sept sections : surfaces d'attaque, STRIDE, OWASP, sécurité applicative, frontières de confiance **avec diagramme**, sécurité infrastructure, gestion des identités et des accès. Trois vivent dans le chapitre `architecture-securite/`, quatre dans `11-securite.md`.
2. **Rappel des calculs dans la checklist.** Le fichier d'état reprenait la mécanique du barème (`Part 80 % = 80 × …`, tables de composantes) : un lecteur y lit une formule par élément au lieu de l'état d'avancement. L'humain ne veut plus de ce rappel dans la checklist.

Le premier point touche la **surface de gouvernance** `required-sections` (SG-1 / SG-6) et le second la **forme du livrable d'état**. Les deux relèvent du garde-fou « ADR d'abord » du [`conductor.md`](../core/common/conductor.md).

## Décision

**Faire porter les sept sections de l'architecture de sécurité par le workflow — contrat `required-sections` (volets `das:` et `securite:`) et gabarit d'état de la checklist — et retirer de la checklist tout rappel de calcul.**

1. **Contrat `required-sections` — fichier `11-securite.md`.** Les sections requises deviennent : « Sécurité applicative », « Frontières de confiance », « Sécurité Infrastructure », « Gestion des identités et des accès (GIA) ». La section « Modélisation des menaces (STRIDE) » n'est **pas supprimée** du gabarit `11` : elle est **déplacée** au contrat du chapitre sécurité, où vit la matrice STRIDE par surface (`02-menaces-stride.md`), afin d'éviter un décompte en double.
2. **Contrat `required-sections` — nouveau volet `securite:`.** Trois fichiers mandatory du chapitre `architecture-securite/` : `01-surfaces-et-actifs.md` (section « Surfaces d'attaque »), `02-menaces-stride.md` (section « Matrice de synthèse STRIDE par surface »), `03-risques-owasp.md` (section « Table de couverture OWASP Top 10 »). Le volet accepte le chapitre **où qu'il soit niché** sous `documentation/` (le contrat porte sur le nom du répertoire et du fichier, pas sur la profondeur) ; le glob `matches` couvre désormais `documentation/**/*.md` en plus de `documentation/*.md`.
3. **Gabarit d'état `00-checklist-architecture` — tables de sections requises par livrable.** Le gabarit déploie, livrable par livrable, la table de conformité (section requise, document, conforme ?) et son total ; pour l'architecture de sécurité détaillée, les **sept sections** y figurent, réparties sur le chapitre `architecture-securite/` et le fichier `11-securite.md`. La section « Frontières de confiance » n'est conforme que si son **diagramme** est présent et valide. Le gabarit n'est **pas** un contrat de sections : `required-sections` en reste la source unique, et le protocole `architecture-checklist` ne les reduplique pas.
4. **Gabarit `11-securite.md`.** Ajout d'une section « Frontières de confiance » structurée sur le modèle du `11-securite.md` de Talent Match : **description des frontières et des actifs protégés** (périmètre, actifs, hypothèse de confiance), **flux inter-frontières et points de contrôle**, puis **diagramme obligatoire** — généré en code et embarqué via Structurizr (`embed:`, règle d'or 19). Le détail par frontière (`FR-xxx`), les actifs (`ACTIF-xxx`) et les surfaces (`S1…Sn`) restent dans le chapitre `architecture-securite/` — pas de duplication ; la section n'est conforme que si le diagramme est présent et lisible.
5. **Checklist sans calcul.** Le protocole (section 5) et le gabarit d'état interdisent le rappel de formule ou d'opération dans la checklist : elle présente la conformité constatée (`n / total`), la revue pair, l'acceptation humaine et le %. La mécanique du barème reste dans le protocole, source unique.

### Périmètre

- Modifie la **surface `required-sections`** (fichier `11`, nouveau volet `securite:`), le **protocole checklist**, son **gabarit d'état**, le **gabarit `11-securite`** de la skill `architecture-solution-gabarits` et la ligne du sensor dans `core/sensors/README.md`.
- **Hors périmètre** : les 5 phases, les scopes, le barème 80/10/10 (inchangé), les autres livrables détaillés, la posture de sécurité, le caractère **advisory** des sensors. Aucun passage à bloquant.

## Conséquences

### Positives

- **POS-001** — **Couverture complète de la sécurité** : les sept sections demandées sont requises par le workflow et décomptées par la checklist ; le chapitre `architecture-securite/` n'est plus invisible au gate.
- **POS-002** — **Diagramme opposable** : les frontières de confiance ne sont conformes que si leur diagramme est présent, ce qui donne un point de contrôle objectif au lieu d'une intention.
- **POS-003** — **Checklist lisible** : l'état remplace le calcul ; un lecteur voit l'avancement sans reconstituer une multiplication par élément.
- **POS-004** — **Source unique préservée** : le contrat reste dans `required-sections` ; le gabarit d'état déploie les tables de suivi et renvoie au contrat, le protocole ne liste pas les sections.

### Négatives / points d'attention

- **NEG-001** — **Déplacement de STRIDE** : la modélisation STRIDE n'est plus vérifiée dans `11-securite.md` mais dans `02-menaces-stride.md`. La couverture est conservée, l'emplacement change ; le gabarit `11` garde une section STRIDE de synthèse non contrôlée par le sensor.
- **NEG-002** — **Dénominateur élargi** : la sécurité passe de 2 à 7 sections requises ; les projets dont le chapitre sécurité est incomplet voient leur % de sécurité **baisser mécaniquement** (dénominateur dynamique, ADR-0043). C'est l'effet recherché, mais il faut le lire comme un progrès de mesure, pas une régression.
- **NEG-003** — **Cohérence gabarit ↔ manifeste** élargie à trois gabarits supplémentaires (`architecture-securite-gabarits/01`, `02`, `03`) ; toute évolution de titres doit être répercutée dans la même PR (NEG-004 de l'ADR-0012).

## Alternatives étudiées

### ALT-001 — Règle de projet (`core/rules/projects/`) seulement

Consigner le besoin dans une règle de projet OAI-DLC sans toucher au workflow. **Non retenue** : l'humain demande explicitement la modification du workflow ; une règle de projet ne change ni le contrat des sections ni le comportement des autres projets.

### ALT-002 — Ajouter les sections dans le seul gabarit de checklist

Étendre la checklist sans toucher `required-sections`. **Non retenue** : la liste vivrait hors du contrat, donc hors du dénominateur contrôlé par le sensor ; `required-sections` reste la source unique.

### ALT-003 — Redupliquer la liste des sections dans le protocole `architecture-checklist`

Décrire dans le protocole les sections requises de chaque livrable (table livrable → sections, détail par livrable). **Non retenue** (arbitrage humain) : le contrat des sections est déjà porté par `required-sections`, une liste dans le protocole en fait un doublon susceptible de diverger. Le protocole renvoie au contrat ; seul le gabarit d'état déploie des tables de suivi, qui ne redéfinissent rien.

### ALT-004 — Un nouveau sensor dédié à l'architecture de sécurité

Créer un sensor `security-architecture-sections`. **Non retenue** : le contrôle est de même nature (présence et non-vacuité de sections) ; un volet supplémentaire du sensor existant suffit et évite de multiplier les manifestes.

## Notes d'implémentation

- **IMP-001** — [`core/sensors/sensors/required-sections.md`](../core/sensors/sensors/required-sections.md) : sections du fichier `11`, nouveau volet `securite:`, glob `documentation/**/*.md`, cohérence gabarits élargie.
- **IMP-002** — [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) : règle « la checklist présente l'état, jamais le calcul » (section 5), vérification de conformité et mapping mis à jour (section 6), **aucune liste de sections requises** (renvoi à la source unique `required-sections`).
- **IMP-003** — [`core/common/protocols/gabarits/00-checklist-architecture.md`](../core/common/protocols/gabarits/00-checklist-architecture.md) : gabarit réécrit sans formule, tables de conformité par livrable, sept sections de sécurité (suivi déployé depuis `required-sections`).
- **IMP-004** — [`plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/11-securite.md`](../plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/11-securite.md) : section « Frontières de confiance » sur le modèle de Talent Match (description des frontières et actifs, flux et points de contrôle, diagramme obligatoire embarqué via `embed:`).
- **IMP-005** — liens relatifs vérifiés, front-matter YAML du gabarit valide, aucun changement de posture de sécurité.

## Références

- **REF-001** — ORIG-387 : demande humaine (multica.gaston) de modifier le protocole `architecture-checklist` et les sections requises, sans rappel des calculs dans la checklist.
- **REF-002** — [ADR-0043 - Checklist d'architecture : avancement en pourcentage, barème 80/10/10](0043-checklist-architecture-avancement-en-pourcentage-bareme-80-10-10.md) : barème et dénominateur dynamique, inchangés.
- **REF-003** — [ADR-0025 - Durcissement du sensor required-sections (volet DAS)](0025-durcissement-required-sections-das.md) : Option A, manifeste autonome et règle de cohérence gabarit ↔ manifeste.
- **REF-004** — [`core/sensors/sensors/required-sections.md`](../core/sensors/sensors/required-sections.md) : contrat de sections.
- **REF-005** — [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) : protocole de la checklist (mécanique, sans contrat de sections).
- **REF-006** — [`core/common/protocols/gabarits/00-checklist-architecture.md`](../core/common/protocols/gabarits/00-checklist-architecture.md) : gabarit d'état.
- **REF-007** — [`plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/11-securite.md`](../plugins/architecture-assistant/skills/architecture-solution-gabarits/gabarits/11-securite.md) : gabarit du fichier `11`.
- **REF-008** — [ADR-0040 - Aucune note de génération dans les livrables](0040-aucune-note-de-generation-dans-les-livrables.md) : invariant appliqué au fichier d'état.
