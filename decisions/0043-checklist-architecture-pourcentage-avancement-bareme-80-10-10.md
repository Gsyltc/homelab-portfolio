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

- **Granularité insuffisante** : un livrable d'architecture réel (ex. la DAS) regroupe plusieurs fichiers et sections mandatory. Tant que l'ensemble n'est pas accepté, l'élément reste à 0 % — un livrable à 6 sections conformes sur 7 est indiscernable d'un livrable vide.
- **Avancement non mesurable** : le statut ne reflète ni la part de conformité documentaire déjà atteinte, ni les étapes de qualité (revue par un pair, acceptation humaine) franchies.

L'humain demandeur (sylvain.rodgers) a cadré une évolution vers un **pourcentage d'avancement par élément**, avec un **suivi par section mandatory** des livrables et un **barème homogène 80/10/10**. Le contrat des sections mandatory a déjà sa source unique dans le sensor [`required-sections`](../core/sensors/sensors/required-sections.md) (7 fichiers mandatory du DAS + sous-sections) : le modèle en % doit s'y adosser sans le redéfinir.

Faire évoluer le modèle de suivi introduit par [`0042`](0042-checklist-architecture-processus-protocole-gabarit.md) modifie une surface de gouvernance du workflow (mode de calcul de l'avancement + gate de déblocage). Le garde-fou « ADR d'abord » impose de tracer la décision par ADR avant toute modification documentaire. Le précédent existe : [`0025`](0025-durcissement-required-sections-das.md) (évolution d'une surface de gouvernance) et [`0040`](0040-aucune-note-de-generation-dans-les-livrables.md) (invariant en source unique + ADR).

## Décision

**Remplacer le statut discret par un pourcentage d'avancement par élément, calculé selon un barème homogène 80/10/10, avec un décompte par section mandatory adossé au sensor `required-sections` et un gate de déblocage à ≥ 80 %.**

- **Barème par élément** : `% = 80 × (sections conformes / total sections) + 10·(revue pair) + 10·(acceptation humaine)`, arrondi à l'entier. Les termes `(revue pair)` et `(acceptation humaine)` valent `1` si franchis, `0` sinon.
- **Suivi par section mandatory** pour les livrables : le `80 %` est proportionnel aux sections mandatory **présentes et non vides**, selon le contrat de `required-sections` (source unique, non dupliqué).
- **Dénominateur dynamique** : toute nouvelle section/fichier mandatory ajouté au contrat `required-sections` s'ajoute au total ; le `80 %` se recalcule sur le nouveau total, sans modifier la checklist.
- **Barème homogène** sur toutes les sections (Cadrage, Besoins MoSCoW, Livrables, Projets) : chaque élément listé est une unité suivie ; pour les éléments sans sous-sections mandatory, le terme `80 %` est atteint dès que le livrable attendu est présent et conforme (`sections conformes / total sections = 1`).
- **Gate par élément, conditionné à la conformité complète** : le gate s'applique **par élément** (jamais sur une moyenne : un `% global` ou `% section` élevé ne compense jamais un élément faible). Un élément n'est débloquable que si **toutes** ses sections mandatory sont conformes (`sections conformes / total = 1`), pas seulement si le total atteint `≥ 80 %`. Le **pourcentage reste un indicateur d'avancement**, pas le seul critère de gate. Les éléments de **surface de sécurité** (Besoins → Sécurité, Architecture de sécurité détaillée) sont requis individuellement et ne se compensent jamais. Le lancement reste soumis à **décision humaine**.
- **Revue de sécurité non substituable (SG-3)** : pour toute surface de sécurité ou d'architecture, le **gate ne remplace pas la revue de sécurité** et ne conditionne pas son déclenchement ; le verdict **favorable** du Reviewer de sécurité précède le déblocage. Le terme `(revue)` d'un élément de surface de sécurité n'est crédité que sur verdict du Reviewer de sécurité (la revue de cohérence s'ajoute, jamais à la place). L'état de la revue de sécurité (✓/✗) est affiché au moment du gate.
- **Revue et acceptation rattachées à une version (anti-falsification, OWASP A08)** : les deux `+10 %` ne sont crédités que sur **verdict favorable sans point bloquant ouvert** (revue) et **acceptation d'un membre humain** (auteur `member`, cité par identifiant), **rattachés à une référence de version** du livrable ; tout changement d'un contenu mandatory **remet les deux termes à zéro**, tracé sur l'issue.
- **Garde-fous préservés** : l'acceptation humaine (`+10 %`) ne provient que d'une annonce explicite d'un membre humain ; aucun agent ne s'auto-valide ni ne voit son acceptation comptée même relayée par un humain. Les sensors (`required-sections`, `data-lifecycle`) restent **advisory** ; « présent et non vide » est un plancher de forme, **jamais** un niveau de sécurité atteint. Un retrait/assouplissement d'une section mandatory de sécurité exige une validation humaine explicite tracée (SG-3). Un % de section ne résulte que d'une vérification de conformité objective (présent + non vide), jamais d'une estimation. La comparaison au seuil se fait sur la valeur non arrondie. Le fichier d'état reste un livrable sans note de méta-production (décision [`0040`](0040-aucune-note-de-generation-dans-les-livrables.md)).

### Périmètre

- Refonte du modèle de suivi : protocole `architecture-checklist.md` (sections structure, calcul, écriture, vérification), gabarit d'état `00-checklist-architecture.md` (colonnes `%` + sous-tableaux par section mandatory), et renvoi du `conductor.md` vers le modèle en %.
- **Hors périmètre** : aucun changement des 5 phases, des scopes, du contrat de `required-sections` (qui reste la source unique des sections mandatory), des gabarits DAS, ni de la posture de sécurité. Le passage d'un sensor advisory à bloquant resterait une décision séparée.

## Conséquences

### Positives

- **POS-001** : avancement mesurable et granulaire — un livrable partiellement conforme reflète sa part réelle (ex. 6/7 sections = ~69 %) au lieu de 0 %.
- **POS-002** : barème homogène 80/10/10 lisible d'un coup d'œil sur toutes les sections ; la qualité (revue pair, acceptation) est explicitement valorisée.
- **POS-003** : adossement au contrat unique `required-sections` — le décompte des sections conformes ne duplique aucun contrat et suit automatiquement ses évolutions (dénominateur dynamique).
- **POS-004** : gate par élément objectivable — le déblocage est conditionné par la **conformité complète** de l'élément (toutes sections mandatory) et, pour les surfaces de sécurité, par la revue de sécurité ; la moyenne ne compense jamais un élément faible, la décision de lancement restant humaine.
- **POS-005** : intégrité dans le temps — revue et acceptation sont rattachées à une version et remises à zéro à tout changement de contenu mandatory ; un livrable modifié ne conserve pas un crédit obtenu sur une version antérieure.

### Négatives

- **NEG-001** : cohérence à maintenir à deux endroits — le décompte s'appuie sur `required-sections` et les gabarits DAS ; toute évolution de nommage/découpage doit rester cohérente avec le mapping du protocole (les sources existantes font foi).
- **NEG-002** : tenue plus fine — le coordinateur doit décompter les sections conformes par livrable (assisté par le sensor advisory), au lieu d'un simple statut ; charge de tenue accrue, compensée par la granularité gagnée.
- **NEG-003** : lecture d'un % non entier possible — l'arrondi à l'entier sert à l'affichage ; la comparaison au seuil se fait sur la valeur non arrondie (ex. 79,5 % reste bloqué). Choix assumé, le détail par section restant consultable.
- **NEG-004** : double comptage assumé — `11-securite.md` alimente le DAS et « Architecture de sécurité détaillée », `10-cycle_vie_donnees.md` le DAS et « Architecture de données détaillée » ; les éléments restent jugés séparément (complétude d'ensemble vs profondeur du volet).
- **NEG-005** : remise à zéro des `+10 %` à chaque changement de contenu mandatory — protège l'intégrité mais impose de re-solliciter revue et acceptation après modification ; charge assumée, tracée sur l'issue.

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

## Notes d'implémentation

- **IMP-001** : refonte de [`core/common/protocols/architecture-checklist.md`](../core/common/protocols/architecture-checklist.md) — sections 2 à 6 : % par élément, barème 80/10/10, décompte par section mandatory (renvoi à `required-sections` comme source unique), dénominateur dynamique, gate ≥ 80 %.
- **IMP-002** : refonte du gabarit [`core/common/protocols/gabarits/00-checklist-architecture.md`](../core/common/protocols/gabarits/00-checklist-architecture.md) — colonnes `%` au lieu de `Statut`, sous-tableaux par section mandatory pour les Livrables, lignes revue pair / acceptation humaine, `% global` recalculé, front-matter YAML conservé.
- **IMP-003** : mise à jour du renvoi dans [`core/common/conductor.md`](../core/common/conductor.md) (section « Checklist d'architecture ») vers le modèle en %, sans dupliquer la logique du protocole.
- **IMP-004** : cohérence vérifiée avec [`required-sections`](../core/sensors/sensors/required-sections.md) (7 fichiers mandatory du DAS + sous-sections) sans redéfinir son contrat.
- **IMP-005** : liens relatifs vérifiés (résolution `realpath`) ; front-matter du gabarit validé (YAML). `superseded_by` de l'ADR-0042 renseigné vers la présente ADR.

## Références

- **REF-001** : [ADR-0042 - Checklist d'architecture comme processus à part](0042-checklist-architecture-processus-protocole-gabarit.md) — décision révisée (lien `supersedes`/`superseded_by` bidirectionnel).
- **REF-002** : [Sensor required-sections](../core/sensors/sensors/required-sections.md) — contrat unique des sections mandatory (décompte du 80 %).
- **REF-003** : [ADR-0025 - Durcissement du sensor required-sections](0025-durcissement-required-sections-das.md) — précédent d'évolution d'une surface de gouvernance.
- **REF-004** : [ADR-0040 - Aucune note de génération dans les livrables](0040-aucune-note-de-generation-dans-les-livrables.md) — invariant appliqué au fichier d'état.
- **REF-005** : [Protocole architecture-checklist](../core/common/protocols/architecture-checklist.md) — source unique du cycle lecture/écriture.
- **REF-006** : [Gabarit d'état 00-checklist-architecture](../core/common/protocols/gabarits/00-checklist-architecture.md) — gabarit d'état versionné.
