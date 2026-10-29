# Checklist d'architecture en pourcentage d'avancement (barème 80/10/10, suivi par section) — révision du modèle de statut discret

---
auteurs: Architecture Solution & Intégration (agent)
accepté par : ""
accepté le : ""
supersedes: "0042-checklist-architecture-processus-protocole-gabarit.md"
superseded_by: ""

---

## Status

Proposed

## Date de création

2026-10-29

## Contexte

La checklist d'architecture du workflow `core` suit l'avancement de l'architecture le long des 5 phases (`Initialization → Ideation → Inception → Construction → Operation`). Son modèle actuel attribue à chaque élément un **statut discret** (`validé` · `en cours` · `refusé` · `non débuté`) et calcule un pourcentage binaire : seul `validé` compte, tout le reste vaut 0.

Ce modèle binaire a deux limites :

- **Granularité insuffisante** : un livrable d'architecture réel (ex. la DAS) regroupe plusieurs sections mandatory. Tant que l'ensemble n'est pas accepté, l'élément reste à 0 % — un livrable à 17 sections conformes sur 18 est indiscernable d'un livrable vide.
- **Avancement non mesurable** : le statut ne reflète ni la part de conformité documentaire atteinte, ni les étapes de qualité (revue, acceptation humaine) franchies.

L'humain demandeur (sylvain.rodgers) a cadré un **pourcentage d'avancement par élément**, un **suivi par section mandatory** et un **barème homogène 80/10/10**. Le contrat des sections mandatory a sa source unique dans le sensor [`required-sections`](../core/sensors/sensors/required-sections.md) (DAS : 18 sections réparties sur 7 fichiers) : le modèle en % s'y adosse sans le redéfinir. Faire évoluer le modèle introduit par [`0042`](0042-checklist-architecture-processus-protocole-gabarit.md) modifie une surface de gouvernance (calcul de l'avancement + critère de gate) ; le garde-fou « ADR d'abord » impose de tracer la décision par ADR. Précédents : [`0025`](0025-durcissement-required-sections-das.md) et [`0040`](0040-aucune-note-de-generation-dans-les-livrables.md).

## Décision

**Remplacer le statut discret par un pourcentage d'avancement par élément (barème homogène 80/10/10), avec un décompte à la section mandatory adossé au sensor `required-sections`, et un gate de conformité par élément (conformité complète + revue de sécurité) rattaché à deux frontières de phase (`Inception → Construction` et `Construction → Operation`).**

- **Barème par élément** : `% = 80 × (sections conformes / total sections) + 10·(revue) + 10·(acceptation humaine)`. Le `%` est un **indicateur d'avancement** (arrondi réservé à l'affichage), pas le critère du gate.
- **Unité = la section mandatory** : le `80 %` est proportionnel aux **sections mandatory présentes et non vides**, décomptées **à la section** selon `required-sections` (source unique, non dupliqué). Au contrat actuel : DAS = **18 sections** (7 fichiers), Architecture de sécurité détaillée = **2 sections** (`11-securite.md`).
- **Total dynamique** : le total est lu dans `required-sections` au moment du calcul ; toute évolution du contrat recalcule le `80 %` sans modifier la checklist. Le fichier d'état est un **instantané recalculé** à chaque mise à jour.
- **Éléments sans contrat de sections mandatory** (Cadrage, Besoins hors Sécurité, Projets, Architecture Logicielle / Données / Infrastructure détaillées) : `total = 1` **par convention** ; leur conformité est jugée par la **revue de cohérence**, faute de base objective (« ne jamais deviner »). **Exception : Besoins → Sécurité**, dont la conformité **et** le `(revue)` relèvent du **Reviewer de sécurité**.
- **Gate de conformité par élément, par frontière** : le gate s'applique **par élément** (jamais sur une moyenne). Un élément est conforme seulement si **toutes** ses sections mandatory sont conformes (conformité complète) et, pour les **éléments d'architecture** (cf. ci-dessous), si le **verdict de sécurité est favorable**. Chaque élément est jugé à la **frontière qui le produit** : **`Inception → Construction`** = Cadrage, Besoins (4), DAS ; **`Construction → Operation`** = architectures détaillées (Logicielle, Données, Sécurité, Infrastructure) et Projets (5).
- **Portée bloquante — décision humaine à acter** : conformément à la demande initiale (`< seuil ⇒ bloqué`) et à SG-3, le gate est **bloquant** (tant que la conformité complète, et le verdict de sécurité favorable pour les éléments d'architecture, manquent, le passage de frontière n'est pas présenté comme possible ; la décision humaine reste libre ensuite). **Le choix bloquant vs advisory et l'ancrage aux frontières sont un point de décision explicite pour l'humain demandeur** (`DEC-HUM-001` ci-dessous) ; tant qu'il n'est pas acté, `Proposed` vaut **proposition, non acquis**.
- **Revue de sécurité non substituable (SG-3)** : on appelle **élément d'architecture** tout élément soumis à la revue de sécurité — les **cinq éléments de la section Livrables** (DAS + architectures détaillées) **et** **Besoins → Sécurité** (marqués 🔒, un seul sens). Pour eux, le terme `(revue)` **et** la conformité (80 %) sont jugés par le **Reviewer de sécurité** ; son **verdict favorable** (version courante) **précède** le gate **et** l'acceptation humaine (jamais en parallèle). Les autres éléments relèvent de la **cohérence**.
- **Revue et acceptation versionnées (anti-falsification, OWASP A08)** : les deux `+10 %` ne valent que sur **verdict favorable sans point bloquant** et **acceptation d'un membre humain** (auteur `member`), **rattachés à une version** du **support** de l'élément — document(s) attendu(s), ou, pour les éléments sans document (Cadrage, Besoins, Projets), le **commentaire d'issue** (ou paragraphe du DAS) qui les porte. **Tout changement de ce support remet les deux termes à zéro**, tracé sur l'issue.
- **Garde-fous préservés** (détail en source unique protocole §4/§8) : aucun agent ne s'auto-valide ; les sensors restent **advisory** (« présent et non vide » = plancher de forme, jamais un niveau de sécurité) ; un abaissement d'une section mandatory de sécurité exige une validation humaine tracée (SG-3) ; fichier d'état sans note de méta-production (décision [`0040`](0040-aucune-note-de-generation-dans-les-livrables.md)).

### Périmètre

- Refonte du modèle de suivi : protocole `architecture-checklist.md`, gabarit d'état `00-checklist-architecture.md` (colonnes `%` + sous-tableau DAS fichier → sections), renvois du `conductor.md`, et correction du résidu de statut discret dans `directory-check.md`.
- **Hors périmètre** : aucun changement des 5 phases, des scopes, du contrat de `required-sections`, des gabarits DAS. La présente ADR **renforce** la posture de sécurité (revue de sécurité sur toute architecture, anti-abaissement, remise à zéro versionnée) et ne l'**abaisse** en aucun point ; aucun sensor ne passe d'advisory à bloquant (décision séparée).

### Point de décision humaine

- **DEC-HUM-001** : l'humain demandeur (**sylvain.rodgers**) arbitre la **portée du gate** — **bloquant** (recommandé, retenu par défaut ci-dessus, aligné sur la demande initiale `< seuil ⇒ bloqué` et sur SG-3) **ou advisory** — et confirme l'**ancrage aux deux frontières** (`Inception → Construction` : Cadrage/Besoins/DAS ; `Construction → Operation` : architectures détaillées/Projets). Tant que cet arbitrage n'est pas tracé, le statut `Proposed` vaut **proposition, non acquis** ; la clause bloquante n'est pas écrite comme un fait établi. Éléments d'arbitrage :
  - **Conflit à lever avec les « Verification gates » du conductor.** La section « Verification gates aux frontières de phases » du `conductor.md` pose que les gates de frontière sont **advisory** et « ne bloquent jamais ». Un gate de checklist **bloquant** s'en écarte : si l'option bloquante est retenue, `DEC-HUM-001` doit **acter l'exception** (le gate de conformité de la checklist est un contrôle bloquant distinct des vérifications de traçabilité advisory) **et** la refléter dans cette section du conductor ; si l'option advisory est retenue, le protocole §7, l'ADR, le conductor et le gabarit rebasculent en advisory.
  - **Définition opérationnelle de « bloquant ».** « Bloquant » signifie que le coordinateur **n'ouvre pas la sollicitation de validation humaine de la frontière** tant que la conformité complète (et le verdict de sécurité favorable pour un élément d'architecture) manque. Ce n'est pas un verrou technique : l'humain **peut décider de passer outre**, mais c'est alors une **dérogation explicite, tracée sur l'issue avec l'écart constaté** (élément non conforme / verdict de sécurité manquant) — jamais un contournement silencieux.
  - **Rattachement de Projets à `Construction → Operation`.** Planification, Coûts et Risques **s'affinent** pendant la Construction (coûts et risques de réalisation, planning d'exécution) et ne sont **stabilisés** qu'en fin de Construction ; les exiger conformes dès `Inception → Construction` figerait des estimations encore ouvertes. Ils sont donc rattachés à `Construction → Operation`. Le **cadrage initial** (ébauche de planification issue des stages d'Inception `deliverables-breakdown` / `design-and-decisions`) reste couvert par l'élément **Cadrage** à la frontière `Inception → Construction`. À confirmer par l'humain si une partie de Projets doit être exigée plus tôt.

## Conséquences

### Positives

- **POS-001** : avancement mesurable et granulaire — un livrable partiellement conforme reflète sa part réelle (ex. DAS 17/18 sections ≈ 76 %) au lieu de 0 %.
- **POS-002** : barème homogène 80/10/10 lisible d'un coup d'œil sur toutes les sections ; la qualité (revue, acceptation) est explicitement valorisée.
- **POS-003** : adossement au contrat unique `required-sections` — le décompte des sections conformes ne duplique aucun contrat et suit automatiquement ses évolutions (dénominateur dynamique).
- **POS-004** : gate par élément objectivable — le déblocage est conditionné par la **conformité complète** de l'élément (toutes sections mandatory) et, pour les **éléments d'architecture**, par la revue de sécurité ; la moyenne ne compense jamais un élément faible, la décision de lancement restant humaine.
- **POS-005** : intégrité dans le temps — revue et acceptation sont rattachées à une version et remises à zéro à **tout changement du ou des documents attendus** (mandatory ou non) ; un livrable modifié ne conserve pas un crédit obtenu sur une version antérieure.

### Négatives

- **NEG-001** : cohérence à maintenir à deux endroits — le décompte s'appuie sur `required-sections` et les gabarits DAS ; toute évolution de nommage/découpage doit rester cohérente avec le mapping du protocole (les sources existantes font foi).
- **NEG-002** : tenue plus fine — le coordinateur doit décompter les sections conformes par livrable (assisté par le sensor advisory), au lieu d'un simple statut ; charge de tenue accrue, compensée par la granularité gagnée.
- **NEG-003** : le `%` affiché est **arrondi** (lisibilité) ; il reste un indicateur d'avancement. Le gate ne compare aucun pourcentage — il teste `sections conformes / total = 1` — donc l'arrondi n'influe pas sur le déblocage.
- **NEG-004** : double comptage assumé — `11-securite.md` alimente le DAS et « Architecture de sécurité détaillée », `10-cycle_vie_donnees.md` le DAS et « Architecture de données détaillée » ; les éléments restent jugés séparément (complétude d'ensemble vs profondeur du volet).
- **NEG-005** : remise à zéro des `+10 %` à **tout changement du ou des documents attendus** de l'élément — protège l'intégrité mais impose de re-solliciter revue et acceptation après modification ; charge assumée, tracée sur l'issue.
- **NEG-006** : revue de sécurité requise pour **tous** les éléments d'architecture (section Livrables) avant l'acceptation — allonge le circuit de ces éléments, mais aligne la checklist sur SG-3 (revue de sécurité avant la validation humaine sur toute architecture) ; compromis assumé en faveur de la sécurité.

## Alternatives étudiées

### ALT-001 - Conserver le statut discret (modèle 0042)

Garder `validé / en cours / refusé / non débuté` avec % binaire.

**Raison du rejet** : granularité insuffisante ; un livrable presque complet reste indiscernable d'un livrable vide. L'humain demande un avancement mesurable par section.

### ALT-002 - Pourcentage libre saisi par le coordinateur

Laisser le coordinateur estimer un % d'avancement par élément.

**Raison du rejet** : violerait le garde-fou « ne jamais deviner » ; un % doit résulter d'une vérification objective (présent + non vide), pas d'une estimation.

### ALT-003 - Barème pondéré variable selon l'élément

Pondérer différemment chaque section (ex. Livrables plus lourds que Cadrage).

**Raison du rejet** : complexité et arbitraire ; l'humain a cadré un barème **homogène** 80/10/10 pour une lecture tout-en-% cohérente (option : chaque élément listé = une unité suivie).

### ALT-004 - Gate au seuil `≥ 80 %` seul

Débloquer un élément dès que son pourcentage atteint `≥ 80 %`, sans autre condition.

**Raison du rejet** : la formule additive permet aux deux `+10 %` (revue, acceptation) de **compenser** une conformité documentaire incomplète. Un élément à 80 % peut avoir une section mandatory manquante (y compris de sécurité), ou atteindre 89 % avec une section manquante. Le gate retient donc la **conformité complète par élément** ; le pourcentage reste un indicateur d'avancement, jamais le critère de déblocage.

## Notes d'implémentation

- **IMP-001** : refonte du protocole [`architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) (% par élément, décompte à la section, total dynamique, gate de conformité **bloquant** rattaché à **deux frontières** `Inception → Construction` et `Construction → Operation`) et du gabarit [`00-checklist-architecture.md`](../core/common/protocols/gabarits/00-checklist-architecture.md) (colonnes `%`, sous-tableau DAS fichier → sections, front-matter YAML conservé).
- **IMP-002** : renvois mis à jour dans [`conductor.md`](../core/common/conductor.md) (section checklist + Références) et correction du résidu de statut discret dans [`directory-check.md`](../core/common/stages/initialization/directory-check.md) (Step 3 → « 0 % »), sans dupliquer la logique du protocole.
- **IMP-003** : cohérence vérifiée avec [`required-sections`](../core/sensors/sensors/required-sections.md) (DAS = 18 sections sur 7 fichiers ; `11-securite.md` = 2 sections) sans redéfinir son contrat ; liens relatifs vérifiés ; front-matter YAML du gabarit validé.
- **IMP-004** : lien `supersedes`/`superseded_by` bidirectionnel avec l'ADR-0042. **À l'acceptation de la présente ADR**, passer l'ADR-0042 (actuellement `Proposed`) au statut **`Superseded`**.

## Références

- **REF-001** : [ADR-0042 - Checklist d'architecture comme processus à part](0042-checklist-architecture-processus-protocole-gabarit.md) — décision révisée (lien `supersedes`/`superseded_by` bidirectionnel).
- **REF-002** : [Sensor required-sections](../core/sensors/sensors/required-sections.md) — contrat unique des sections mandatory (décompte du 80 %).
- **REF-003** : [ADR-0025 - Durcissement du sensor required-sections](0025-durcissement-required-sections-das.md) — précédent d'évolution d'une surface de gouvernance.
- **REF-004** : [ADR-0040 - Aucune note de génération dans les livrables](0040-aucune-note-de-generation-dans-les-livrables.md) — invariant appliqué au fichier d'état.
- **REF-005** : [Protocole architecture-checklist](../core/common/protocols/architecture-checklist.md) — source unique du cycle lecture/écriture.
- **REF-006** : [Gabarit d'état 00-checklist-architecture](../core/common/protocols/gabarits/00-checklist-architecture.md) — gabarit d'état versionné.
