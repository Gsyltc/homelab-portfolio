# Nommage daté unifié `<YYYY-mm-dd>-<nom>` et archivage de la dernière analyse CV (YAML + Markdown conservés)

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : "2026-10-01"
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — évolution **documentaire** du workflow `matching-cv-ao` demandée et validée explicitement par multica.gaston (EXPE-88). Elle **prolonge** [ADR-0034](0034-format-yaml-donnees-cv.md) (format YAML des données CV) sans la modifier : elle n'altère ni le format de sérialisation (YAML des données CV, JSON hors périmètre), ni les champs, ni les poids du scoring (immuables, [ADR-0032](0032-refonte-ponderation-scoring-matching.md)), ni aucun invariant de gouvernance (validation humaine granulaire, piste d'audit, non-transmission des CV). Elle porte **deux décisions** : (1) un **nommage daté unifié** `<YYYY-mm-dd>-<nom>` pour les deux artefacts d'analyse et le CV livrable ; (2) **seule la dernière analyse à la racine de `cv/`**, les versions antérieures des **deux** formats (YAML **et** Markdown) étant déplacées dans `archives/`. Elle **acte explicitement la conservation des deux formats d'analyse** — YAML (données reparsables) et Markdown (fiche d'analyse humaine).

## Contexte

Le workflow `matching-cv-ao` produit, par collaborateur, deux artefacts d'analyse dans `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/` : une **fiche d'analyse Markdown** (lisible par l'humain) et un **YAML de données CV** (reparsable, lu par le Matcher, `cv-generation`, les sensors). Le **CV livrable** (DOCX par défaut, Markdown sur demande) est produit par `cv-generation`. Ce schéma est défini **une seule fois** dans la compétence `cv-analyse` (plugin `rh-assistant`) — **source unique** — et référencé par leur nom par les fiches de stage, le conductor, les sensors et les autres compétences.

Deux écarts et une clarification ont motivé cette décision :

1. **Nommage divergent entre documentation et runtime.** L'inspection des CV runtime (9 collaborateurs à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/`, `archives/` exclu) montre que les fichiers existants sont déjà nommés **`<YYYY-mm-dd>-<nom>.json`** + **`<YYYY-mm-dd>-<nom>.md`** : la **convention datée unifiée est déjà en place côté runtime**. La **documentation**, elle, décrivait un nommage **différent et désormais obsolète** : fiche Markdown `<AAAA-MM-JJ>-<nom>-<prenom>.md`, YAML `<nom>-<prenom>-<AAAA-MM-JJ>.yaml`, CV livrable `<nom>-<prenom>-<type-gabarit>-<AAAA-MM-JJ>.docx`. (Les **données** runtime sont encore en `.json` — la migration YAML d'[ADR-0034](0034-format-yaml-donnees-cv.md) n'y a pas été appliquée ; cela relève des données de runtime, hors de ce dépôt — cf. ADR-0034 NEG-002.)

2. **Règle de versionnage « toutes les versions à la racine ».** La documentation prévoyait que le YAML n'était **jamais écrasé** et que **toutes** les versions s'accumulaient à la racine de `cv/`, la « dernière version » étant départagée par tri sur la date du nom puis le mtime. Cela encombre la racine et complique l'inventaire.

3. **Rôle des deux formats à clarifier.** Il fallait **acter explicitement** que les deux formats d'analyse coexistent avec des rôles distincts (données reparsables vs fiche humaine), et **ne pas supprimer** la fiche Markdown.

### Analyse de tokens (justification de la conservation des deux formats)

Mesure réelle `tiktoken` (`cl100k_base` + `o200k_base`) sur les 9 CV runtime, à **information identique** (mêmes données sérialisées en 3 formats), YAML round-trip PyYAML vérifié :

| Format (même donnée) | cl100k | o200k | vs JSON | vs YAML |
| --- | --- | --- | --- | --- |
| JSON indenté | 67 428 | 64 912 | réf. | — |
| YAML bloc | 57 183 | 54 611 | −15 à −16 % | — |
| Markdown structuré | 38 963 | 36 331 | −42 à −44 % | −32 à −34 % |

- Le **Markdown** est le moins coûteux en tokens, mais **n'est pas reparsable** vers un schéma strict : le Matcher, `cv-generation` et les sensors relisent les données **par programme**. Il ne peut donc **pas** se substituer au YAML comme format de données.
- Le **YAML** reste le format des **données** (reparsable, −15 à −16 % vs JSON, cf. ADR-0034) ; le **Markdown** reste la **fiche d'analyse lisible par l'humain** (mémoire humaine, présentation à l'audit).
- Les deux formats ont donc des **rôles distincts et complémentaires** — ni l'un ni l'autre n'est redondant. La conservation des deux est **confirmée** (aucune suppression de la fiche Markdown).

## Décision

### Décision 1 — Nommage daté unifié `<YYYY-mm-dd>-<nom>`

Aligner la **documentation** du workflow sur la convention datée (déjà appliquée au runtime), pour **les deux** artefacts d'analyse **et** le CV livrable :

- **Fiche d'analyse Markdown** : `<AAAA-MM-JJ>-<nom>-<prenom>.md` → **`<YYYY-mm-dd>-<nom>.md`** ;
- **Données CV YAML** : `<nom>-<prenom>-<AAAA-MM-JJ>.yaml` → **`<YYYY-mm-dd>-<nom>.yaml`** ;
- **CV livrable DOCX** : `<nom>-<prenom>-<type-gabarit>-<AAAA-MM-JJ>.docx` → **`<YYYY-mm-dd>-<nom>-<type-gabarit>.docx`** ;
- **CV livrable Markdown** (sur demande explicite) : `<nom>-<prenom>-cv-<AAAA-MM-JJ>.md` → **`<YYYY-mm-dd>-<nom>-cv.md`**.

Règles de nommage :

- **Préfixe `<YYYY-mm-dd>`** = **toujours la date du jour** de l'analyse (ISO), cohérent avec `date_derniere_modification`.
- **`<nom>`** = **slug minuscule** cohérent avec le segment `<nom-prenom>` du répertoire du collaborateur (confirmé par multica.gaston).
- **Champs de référence inchangés** : `analyse_markdown` et `analyse_yaml` sont **conservés** (les deux formats restent) ; seule la valeur (le chemin/nom) suit le nouveau nommage.

### Décision 2 — Seule la dernière analyse à la racine ; les versions antérieures (YAML + Markdown) dans `archives/`

Seule la **dernière** analyse reste à la racine de `cv/`. **Avant** d'écrire la nouvelle analyse, **déplacer vers `archives/` toutes** les versions antérieures des **deux** artefacts (YAML **et** Markdown).

- Remplace la règle « YAML jamais écrasé, toutes versions à la racine ». L'historique est **conservé** mais **dans `archives/`** (YAML + MD).
- La règle « dernière version » devient **triviale** : à la racine, **un seul couple** `<YYYY-mm-dd>-<nom>.{yaml,md}` (fin des règles de tri par date/mtime pour départager plusieurs versions racine).
- Le stage `chargement-cv` scanne la **racine** (couple courant) **+ `archives/`** (historique) ; seul le YAML courant à la racine sert au matching.

### Décision 3 — Conservation explicite des deux formats d'analyse

Les deux formats d'analyse **coexistent**, avec des rôles distincts, et **aucun n'est supprimé** :

- **YAML** — format des **données CV** (reparsable par le Matcher, `cv-generation`, les sensors) ; conservé conformément à [ADR-0034](0034-format-yaml-donnees-cv.md).
- **Markdown** — **fiche d'analyse lisible par l'humain** (mémoire humaine) ; conservée.

Justification : analyse de tokens ci-dessus (le Markdown est le moins coûteux mais non reparsable ; le YAML reste nécessaire comme format de données). La distinction **fiche d'analyse (mémoire) ≠ CV livrable** reste inchangée.

Règles de conception associées, validées par l'humain (EXPE-88) :

1. **Périmètre = documentation du workflow.** Aucun changement de format de sérialisation (YAML des données CV / JSON hors périmètre, cf. ADR-0034), aucun champ ajouté/retiré/renommé, aucun poids de scoring modifié.
2. **Source unique = `cv-analyse`.** Le nommage, la structure de `cv/` et la règle d'archivage sont définis **une seule fois** dans `cv-analyse` ; les autres fichiers y renvoient par référence (pas de duplication de schéma).
3. **Invariants reconduits** : validation humaine granulaire, présentation Markdown détaillée aux gates, non-transmission des CV, aucun secret, piste d'audit sur l'issue — **inchangés**.

## Conséquences

### Positives

- **POS-001** : **documentation alignée sur le runtime** — le nommage daté unifié `<YYYY-mm-dd>-<nom>` décrit par la documentation correspond désormais aux fichiers réellement présents côté runtime, supprimant une source de confusion.
- **POS-002** : **racine de `cv/` lisible** — un seul couple `<YYYY-mm-dd>-<nom>.{yaml,md}` à la racine ; la « dernière version » est triviale (plus de tri par date/mtime). L'historique reste intégralement conservé dans `archives/`.
- **POS-003** : **nommage cohérent entre artefacts** — fiche d'analyse, données et CV livrable partagent le même préfixe `<YYYY-mm-dd>-<nom>`, facilitant le repérage et le tri chronologique.
- **POS-004** : **conservation actée des deux formats** — rôle de chaque format explicité et justifié par l'analyse de tokens ; aucune perte de la fiche Markdown humaine ni du YAML reparsable.
- **POS-005** : **invariants et scoring intacts** — aucun impact sur les poids immuables, la non-transmission des CV, la validation humaine ou la piste d'audit.

### Négatives / points d'attention

- **NEG-001** : **archivage à la charge du stage d'extraction** — l'ordre « archiver d'abord (les deux artefacts), écrire ensuite » doit être respecté pour garantir l'unicité du couple racine. Mitigation : règle inscrite dans la source unique `cv-analyse` (§ Versionnage) et contrôlée au Step 3 de `extraction-cv` (vérification « un seul couple à la racine + versions antérieures des deux artefacts archivées »).
- **NEG-002** : **fichiers runtime existants** — les analyses runtime sont déjà au nommage daté, mais leurs **données** sont encore en `.json` (migration YAML d'ADR-0034 non appliquée au runtime). Cette ADR modifie **la documentation** ; la **migration des fichiers runtime** (`.json` → `.yaml`, et toute normalisation de nommage résiduelle) relève des **données de runtime, hors de ce dépôt** (cf. ADR-0034 NEG-002).
- **NEG-003** : **cohérence du nommage à tenir** — tout nouvel emplacement documentaire citant un artefact CV doit utiliser `<YYYY-mm-dd>-<nom>` (et non l'ancien `<nom>-<prenom>-<AAAA-MM-JJ>`). Mitigation : source unique + référence par nom ; contrôle d'absence d'occurrence résiduelle au moment de la rédaction.

## Alternatives étudiées

### ALT-001 — Conserver le nommage documentaire existant (statu quo)

**Non retenue** : laisse la documentation divergente du runtime (deux conventions concurrentes), source d'erreurs. Ne répond pas à la demande d'alignement (EXPE-88).

### ALT-002 — Supprimer la fiche Markdown (ne garder que le YAML)

**Non retenue** : le Markdown est la **mémoire humaine** lisible à l'audit et le format le moins coûteux en tokens ; le supprimer dégraderait la relecture humaine sans gain, et l'humain a explicitement demandé de **conserver les deux formats**.

### ALT-003 — Supprimer le YAML (ne garder que le Markdown, le moins coûteux en tokens)

**Non retenue** : le Markdown **n'est pas reparsable** vers un schéma strict ; le Matcher, `cv-generation` et les sensors relisent les données par programme. Le YAML reste indispensable comme format de données (cf. ADR-0034).

### ALT-004 — Conserver toutes les versions à la racine (statu quo du versionnage)

**Non retenue** : encombre la racine et impose un tri par date/mtime pour départager les versions. L'archivage de la dernière seule rend la racine triviale tout en conservant l'historique dans `archives/`.

## Notes d'implémentation

- **IMP-001** : **source unique** — nommage `<YYYY-mm-dd>-<nom>`, structure de `cv/` et règle « dernière analyse seule à la racine, versions antérieures des deux artefacts dans `archives/` » définis dans `plugins/rh-assistant/skills/cv-analyse/SKILL.md` (bloc de structure `cv/`, § Analyse versionnée (Markdown), § Versionnage YAML, règle de sélection de la source CV, champs obligatoires, exemple YAML `analyse_markdown`/`analyse_yaml`).
- **IMP-002** : **fichiers couplés mis à jour par référence** — stage `common/stages/analyse/extraction-cv.md` (front-matter `outputs`, Step 1 archivage des **deux** artefacts + écriture `<YYYY-mm-dd>-<nom>.{md,yaml}`, Step 3 contrôle « un seul couple à la racine + versions antérieures archivées »), `common/stages/initialisation/chargement-cv.md` (inventaire racine couple courant + `archives/`), `common/stages/matching/croisement-profils.md` (dernière version YAML = seul YAML à la racine), `common/stages/cloture/mise-a-jour-cv.md` (mémoire YAML + MD, CV livrable daté), `common/conductor.md` (tableau de stockage : analyses + CV livrable), `README.md` (tableau de stockage), `scopes/format-cv.md` (organisation stricte de `cv/`), `plugins/rh-assistant/skills/cv-generation/SKILL.md` (table fiche d'analyse vs CV livrable, nommage du CV livrable DOCX/Markdown, procédure Step 5 + archivage des deux), `plugins/rh-assistant/skills/matching-scoring/SKILL.md` (le Matcher lit `<YYYY-mm-dd>-<nom>.yaml`), `docs/guide-utilisation-workflow-matching.md` (tableau de stockage + flux).
- **IMP-003** : **corrections de résidus** connexes repérées pendant l'alignement — `common/conductor.md` (rôle Gestionnaire CV : `analyse_json` → `analyse_yaml`) et `common/stages/cloture/mise-a-jour-cv.md` (« JSON d'analyse versionné » → YAML du jour) : résidus pré-ADR-0034 corrigés en cohérence.
- **IMP-004** : **hors périmètre, inchangé** — format de sérialisation (YAML des données CV / JSON pour référentiel clients `clients/<nom-client>.json`, `resume-ao`, `classement-final`, `matching-resultats`, `livraison-finale`, `resultats-valides`, `cv-available`, `ao-pdf-received`, `grille-remplie`, cf. ADR-0034) ; champs du schéma ; poids du scoring (ADR-0032) ; format de date **valeur** `AAAA-MM-JJ` des champs ISO (`date_derniere_modification`, `disponibilite.date_disponibilite`) — distinct du **préfixe de nommage** `<YYYY-mm-dd>`.
- **IMP-005** : **analyse de tokens** mesurée par `tiktoken` (`cl100k_base` + `o200k_base`) sur les 9 CV runtime à information identique, YAML round-trip PyYAML vérifié (JSON 67 428/64 912 ; YAML 57 183/54 611 ; Markdown 38 963/36 331).
- **IMP-006** : entrée `CHANGELOG.md` (`[Non publié] → Changed`).

## Références

- **REF-001** : EXPE-88 — demande et validation du nommage daté unifié, de l'archivage de la dernière analyse seule et de la conservation des deux formats (multica.gaston).
- **REF-002** : [ADR-0034](0034-format-yaml-donnees-cv.md) — format YAML des données CV (EXPE-81) ; la présente ADR la **prolonge** (nommage + archivage) sans la modifier.
- **REF-003** : [ADR-0032](0032-refonte-ponderation-scoring-matching.md) — pondération immuable du scoring (inchangée).
- **REF-004** : `plugins/rh-assistant/skills/cv-analyse/SKILL.md` — source unique du schéma, du nommage et de la règle d'archivage des analyses CV.
- **REF-005** : `matching-cv-ao/common/stages/analyse/extraction-cv.md` — producteur des analyses (archivage des deux artefacts + écriture du couple courant) ; `plugins/rh-assistant/skills/matching-scoring/SKILL.md` et `plugins/rh-assistant/skills/cv-generation/SKILL.md` — consommateurs de la dernière version YAML.
- **REF-006** : invariants préservés — non-transmission des CV (`cv-analyse` § Garde-fou), validation humaine granulaire et piste d'audit (`governance-security` § Invariants non contournables).
