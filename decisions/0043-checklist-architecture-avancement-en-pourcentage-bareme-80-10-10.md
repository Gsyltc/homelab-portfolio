# Checklist d'architecture — avancement en pourcentage par élément (barème 80/10/10, suivi par section)

---
auteurs: Architecture Solution & Intégration (agent)
accepté par : "multica.gaston"
accepté le : "2026-10-30"
supersedes: "0042-checklist-architecture-processus-protocole-gabarit.md"
superseded_by: ""

---

## Status

Accepted

## Date de création

2026-10-30

## Contexte

La décision [`0042`](0042-checklist-architecture-processus-protocole-gabarit.md) a introduit la checklist d'architecture comme **processus à part** (protocole dédié + gabarit d'état), avec un **statut discret** par élément (`validé` · `en cours` · `refusé` · `non débuté`) et un **calcul du %** où seul `validé` compte (binaire 0 / 100 par élément).

Ce modèle binaire masque l'avancement réel : un livrable d'architecture dont la moitié des sections obligatoires sont présentes et conformes reste compté `0 %` tant qu'il n'est pas globalement `validé`. L'humain demandeur veut une **lecture de l'avancement par degré de complétude**, pas par tout-ou-rien, et un **gate de planification / réalisation** adossé à un seuil mesurable.

Les décisions de forme sont cadrées :

1. **Pourcentage par élément** remplace le statut discret.
2. Pour chaque **livrable**, barème : **80 %** = proportion des **sections mandatory présentes et conformes** ; **+10 %** = **revue par un pair** réalisée ; **+10 %** = **acceptation humaine** explicite.
3. Le **même barème 80/10/10** s'applique à **tous** les livrables (DAS + architectures détaillées Logicielle / Données / Sécurité / Infrastructure).
4. Le **même barème 80/10/10** s'applique aussi aux autres sections (Cadrage, Besoins MoSCoW, Projets) : chaque élément listé est traité comme une **unité suivie**, pour une lecture tout-en-% homogène.
5. **Gate de planification / réalisation** : `< 80 %` ⇒ **bloqué** ; `≥ 80 %` ⇒ **déblocage possible** (lancement soumis à décision humaine ; revue pair et acceptation peuvent se faire en parallèle).

Faire évoluer le **modèle de scoring** d'un processus transverse de gouvernance **modifie la surface de gouvernance du workflow** : le garde-fou « ADR d'abord » impose de tracer la décision par ADR, qui **révise** et **supersede** l'ADR-0042.

## Décision

**Remplacer le statut discret de la checklist d'architecture par un pourcentage d'avancement par élément, avec un barème 80/10/10 par livrable, un recalcul dynamique du dénominateur des sections, et un gate de planification / réalisation à ≥ 80 %. Le protocole [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) reste la source unique du processus.**

- **% par élément** — chaque élément de la checklist porte un **pourcentage** (0–100), plus un statut discret par élément.
- **Barème 80/10/10 par livrable** :
  `% livrable = 80 × (sections conformes / total sections mandatory) + 10 × (revue pair) + 10 × (acceptation humaine)`,
  où `revue pair` et `acceptation humaine` valent `0` ou `1`. Arrondi à l'entier.
- **Dénominateur dynamique** — le `total sections mandatory` d'un livrable est celui du contrat **`required-sections`** au moment du calcul ; toute section / fichier mandatory ajouté au fil de l'eau **s'ajoute au dénominateur**, et la part 80 % se recalcule sur le nouveau total. La checklist ne redéfinit aucun contrat de sections : `required-sections` reste la **source unique**.
- **Barème homogène hors Livrables** — Cadrage, Besoins (MoSCoW) et Projets appliquent le même 80/10/10, chaque élément listé étant une unité suivie : `80 %` = élément présent et conforme (0 ou 80, l'élément n'ayant pas de sous-sections mandatory décomptées), `+10 %` revue pair, `+10 %` acceptation humaine.
- **Arrimages décomposé par rôles mandatory** — l'élément **Arrimages** (section Projets) fait exception au binaire : sa part 80 % se décompte par **rôle mandatory** présent et nommé dans la matrice RACI du DAS `001`. Rôles mandatory : Architecte de solution **ou** intégrateur (l'un ou l'autre = 1 rôle), Chef de projet, Responsable produit, Responsable Affaires, Lead Assurance Qualité, et **Responsable Légal uniquement si la Loi 25 est activée**. Dénominateur **5** (ou **6** sous Loi 25), relevant du dénominateur dynamique.
- **% section** = moyenne des % de ses éléments ; **% global** = moyenne des % de tous les éléments, toutes sections. Arrondi à l'entier.
- **Gate planification / réalisation** — `< 80 %` bloque le lancement ; `≥ 80 %` autorise le déblocage, qui **reste soumis à décision humaine**. Le seuil est une condition **nécessaire**, non suffisante : il ne remplace ni la validation humaine ni le contrôle sécurité.
- **Conformité objective uniquement** — un % de section ne résulte que d'une **vérification de conformité** (section présente + non vide + conforme), jamais d'une estimation (« ne jamais deviner »).

### Périmètre

- Révise le **modèle de scoring** du processus checklist : protocole, gabarit d'état, raccordements conductor.
- **Hors périmètre** : aucun changement des 5 phases, des scopes, du contrat `required-sections` lui-même, des gabarits DAS, ni d'aucune posture de sécurité. Les sensors restent **advisory** ; le passage à bloquant resterait une décision séparée. Le fichier d'état reste un livrable sans note de méta-production (décision [`0040`](0040-aucune-note-de-generation-dans-les-livrables.md)).

## Conséquences

### Positives

- **POS-001** : avancement **lisible par degré** — un livrable à moitié conforme se lit `~40 %` au lieu de `0 %`, l'état consolidé reflète le travail réel.
- **POS-002** : barème **explicite et reproductible** (80/10/10) — tout lecteur recalcule le % d'un livrable à partir du décompte des sections, de la revue pair et de l'acceptation.
- **POS-003** : gate **mesurable** (≥ 80 %) pour planification / réalisation, adossé à un seuil objectif plutôt qu'à un jugement global.
- **POS-004** : **dénominateur dynamique** — l'ajout de sections mandatory au fil de l'eau est pris en compte sans réécrire le barème.
- **POS-005** : garde-fous préservés — l'acceptation humaine (+10 %) reste le seul chemin vers 100 %, aucun agent ne s'auto-valide.

### Négatives

- **NEG-001** : **tenue plus fine** — le coordinateur décompte désormais les sections conformes par livrable, non plus un statut global ; charge de mise à jour accrue.
- **NEG-002** : **cohérence à maintenir** entre le décompte des sections et le contrat `required-sections` (source unique) ; une évolution du manifeste change les dénominateurs.
- **NEG-003** : **seuil à ne pas sur-interpréter** — `≥ 80 %` autorise sans obliger ; le risque est de lire le seuil comme une validation automatique. Le protocole rappelle que le déblocage reste une décision humaine.

## Alternatives étudiées

### ALT-001 - Conserver le statut discret de l'ADR-0042

Garder `validé` / `en cours` / `refusé` / `non débuté` et le % binaire.

**Raison du rejet** : ne donne pas la lecture par degré de complétude demandée ; un livrable partiellement conforme reste à `0 %`.

### ALT-002 - Pourcentage libre saisi à la main par élément

Laisser le coordinateur estimer un % d'avancement par élément sans barème.

**Raison du rejet** : viole « ne jamais deviner » (estimation subjective) et n'est pas reproductible ; le barème 80/10/10 ancre le % sur des faits vérifiables.

### ALT-003 - Barème 80/10/10 réservé aux Livrables, statut discret ailleurs

Appliquer le % par sections aux seuls livrables, garder un statut discret pour Cadrage / Besoins / Projets.

**Raison du rejet** : lecture hétérogène (deux échelles). Option retenue : barème homogène sur toutes les sections, chaque élément traité en unité suivie, pour un affichage tout-en-% cohérent.

## Notes d'implémentation

- **IMP-001** : révision de [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) — sections 2 à 6 : % par élément, barème 80/10/10, décompte par section mandatory des Livrables, recalcul dynamique du dénominateur, gate ≥ 80 %, lecture en %.
- **IMP-002** : révision de [`core/common/protocols/gabarits/00-checklist-architecture.md`](../core/common/protocols/gabarits/00-checklist-architecture.md) — colonnes `%` au lieu de `Statut`, sous-tableaux par section mandatory pour les Livrables, lignes `revue pair` / `acceptation humaine`, `% global` recalculé.
- **IMP-003** : mise à jour de [`core/common/conductor.md`](../core/common/conductor.md) — section « Checklist d'architecture » et point de gate planification / réalisation pointant vers le modèle en %.
- **IMP-004** : cohérence vérifiée avec [`required-sections`](../core/sensors/sensors/required-sections.md) (7 fichiers mandatory DAS + sous-sections) sans redéfinir son contrat.
- **IMP-004b** : l'élément **Arrimages** se décompte par rôles mandatory dont la **source** est la matrice RACI « Arrimage des rôles » du fichier DAS `001-document-architecture-solution.md` ; la checklist ne redéfinit pas cette matrice, elle décompte les rôles présents et nommés (dénominateur 5, ou 6 sous Loi 25).
- **IMP-005** : liens relatifs vérifiés ; front-matter YAML du gabarit valide ; `superseded_by` de l'ADR-0042 renseigné vers la présente ADR.
- **IMP-006** : aucun changement des phases, scopes, contrat `required-sections`, gabarits DAS ni de posture de sécurité ; révision documentaire du modèle de scoring uniquement.

## Références

- **REF-001** : [ADR-0042 - Checklist d'architecture comme processus à part](0042-checklist-architecture-processus-protocole-gabarit.md), révisée par la présente décision.
- **REF-002** : [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) — source unique du processus.
- **REF-003** : [`core/common/protocols/gabarits/00-checklist-architecture.md`](../core/common/protocols/gabarits/00-checklist-architecture.md) — gabarit d'état.
- **REF-004** : [`core/common/conductor.md`](../core/common/conductor.md) — raccordement (section checklist + gate planification / réalisation).
- **REF-005** : [`core/sensors/sensors/required-sections.md`](../core/sensors/sensors/required-sections.md) — contrat de sections réutilisé (dénominateur du décompte des Livrables).
- **REF-006** : [ADR-0040 - Aucune note de génération dans les livrables](0040-aucune-note-de-generation-dans-les-livrables.md) — invariant appliqué au fichier d'état.
