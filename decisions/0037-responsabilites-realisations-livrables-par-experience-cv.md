# Champ unique « Responsabilités, réalisations et biens livrables » au niveau expérience dans les données CV

---
auteurs: Gestionnaire CV (agent)
accepté par : multica.gaston
accepté le : "2026-10-01"
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — validé explicitement par multica.gaston au gate EXPE-95 (2026-10-01 :
> « A: Ok ; B: Confirmé ; C: garder ; D: oui »). Ajout d'**un champ liste unique**
> `responsabilites_realisations_livrables` au
> **niveau de l'expérience** (`experience[]`) du schéma des données CV du workflow `matching-cv-ao`, pour
> consigner la rubrique source **« Responsabilités, réalisations et biens livrables »** aujourd'hui
> partiellement perdue à l'extraction. **Conception arbitrée par l'humain (multica.gaston, gate EXPE-95,
> arbitrage Modify)** : « responsabilités, réalisations et livrables sont un seul et même champ (tableau) ;
> ils sont sous l'`experience` et non le `projet` ». La relocalisation de `responsabilites` du niveau projet
> vers le champ unique de l'expérience est **confirmée** (décision B). Évolution **documentaire** du workflow
> (schéma source-unique + fiches couplées), **sans** modification des poids de scoring ni d'aucune posture de
> sécurité. Tous les invariants de gouvernance (validation humaine granulaire, piste d'audit,
> non-transmission des CV, « ne rien inventer ») sont **préservés**.

## Contexte

Lors de l'extraction d'un CV source par le workflow `matching-cv-ao` (agent **Gestionnaire CV**, stage
`extraction-cv`, compétence `cv-analyse`), les CV originaux regroupent fréquemment, pour chaque mandat, une
rubrique **« Responsabilités, réalisations et biens livrables »**. Le schéma des données CV ne portait, au
niveau `experience[].projets[]`, qu'un champ `responsabilites` : les **réalisations** (ce qui a été
effectivement accompli) et les **biens livrables** (artefacts/produits remis) n'avaient aucun emplacement et
étaient **perdus** — absents du YAML des données CV, de la fiche d'analyse Markdown et du CV livrable
généré. Cas relevé par l'humain : CV de Sylvain Goubaud (EXPE-94).

Une **première conception** (tour 1 d'EXPE-95) avait ajouté **deux listes séparées** `realisations[]` et
`livrables[]` **au niveau du projet** (`experience[].projets[]`), à côté du `responsabilites` existant. Au
**gate humain**, multica.gaston a tranché **Modify** avec une consigne explicite et sans ambiguïté :

> « responsabilités, réalisations et livrables sont un seul et même champ (tableau). Ils sont sous
> l'`experience` et non le `projet`. »

Cette décision **remplace** la conception par projet : un **champ liste unique** fusionnant les trois axes,
porté **au niveau de l'expérience**.

Le schéma des données CV est défini par une **source unique** — la compétence `cv-analyse`
(`plugins/rh-assistant/skills/cv-analyse/SKILL.md`) — portée en **YAML** depuis
[ADR-0034](0034-format-yaml-donnees-cv.md), format désormais **exclusif** pour tous les artefacts de données
([ADR-0036](0036-format-yaml-exclusif-workflow-matching.md)).

## Décision

**Ajouter au schéma des données CV un champ liste unique, au niveau de l'expérience** (`experience[]`) :

- **`responsabilites_realisations_livrables: []`** — **une seule liste** (tableau) regroupant, par
  expérience/mandat, l'ensemble des entrées de la rubrique source « Responsabilités, réalisations et biens
  livrables » (responsabilités tenues, réalisations accomplies et biens livrables produits **confondus**,
  une entrée par bullet, dans l'ordre du CV).

### Niveau de portage retenu — l'expérience (`experience[]`), champ unique

Conformément à l'arbitrage humain :

- **un seul champ** (et non trois listes distinctes) : les trois axes de la rubrique source ne sont **pas
  décomposés** — ils sont consignés tels quels dans une liste unique ;
- **au niveau `experience[]`** (racine de chaque expérience), **jamais** au niveau `experience[].projets[]` :
  la contribution est décrite **à la maille du mandat**, pas répartie par projet.

**Conséquence sur `experience[].projets[]`** : les projets ne portent **plus aucune** liste de
responsabilités/réalisations/livrables. Le champ `responsabilites` qui existait au niveau projet **avant**
EXPE-95 est **retiré du projet** et **absorbé** dans le champ unique de l'expérience (les responsabilités
rejoignent la liste fusionnée au niveau expérience). Les projets ne conservent que `nom`, `date_debut` et
`date_fin`. *(Point explicité au Coordinateur pour confirmation : la relocalisation de `responsabilites`
touche un champ pré-EXPE-95.)*

### Nommage du champ

`responsabilites_realisations_livrables` reprend **littéralement** les trois axes de la rubrique source du
CV, dans l'ordre du libellé. Nom proposé et retenu faute d'ambiguïté ; tout doute de nommage serait signalé
à l'humain plutôt que tranché arbitrairement.

### Règles associées (reconduisent les invariants existants)

1. **« Ne rien inventer » (garde-fou reconduit)** : rubrique absente du CV ⇒
   `responsabilites_realisations_livrables: []`, **jamais** de contenu fabriqué ; mention humaine si
   pertinent. Ne pas scinder un bullet ni déduire un axe non écrit.
2. **Pas de décomposition par axe** : la liste est **unique** ; on ne crée pas de sous-listes
   responsabilités/réalisations/livrables (c'est précisément ce que l'arbitrage Modify a écarté).
3. **Mêmes règles de validité YAML** que le reste du schéma (ADR-0034 / ADR-0036) : liste de chaînes libres,
   notation *flow* guillemetée au moindre doute, parse sans erreur avant remise. Aucune règle nouvelle.
4. **Aucun secret** dans cette liste (invariant reconduit).

### Propagation (fiches couplées)

- **`cv-analyse/SKILL.md`** (source unique) : bloc de schéma YAML d'exemple (`experience[]` porte le champ
  unique ; `projets[]` réduit à `nom`/dates), section « Champs obligatoires et règles » (nouvelle règle
  `experience[].responsabilites_realisations_livrables` + règle `experience[].projets` dépouillée), contenu
  de la fiche d'analyse Markdown.
- **`extraction-cv.md`** : consigne d'extraction du champ unique par expérience (Step 1) et contrôle du
  livrable (Step 3) vérifiant la présence du champ unique au niveau `experience[]` (et son absence au niveau
  projet).
- **`cv-generation/SKILL.md`** : opération « Mise à jour d'expérience » (champ unique au niveau expérience)
  et section **« Responsabilités, réalisations et biens livrables » par mandat** du CV livrable (DOCX par
  défaut, Markdown sur demande), avec garde-fou de **cohérence des gabarits** (`${ROOT_DIRECTORY}/gabarits/cv/` :
  si aucun emplacement adapté, signalement humain, aucune mise en page inventée).

## Conséquences

### Positives

- **POS-001** : la **contribution concrète** du collaborateur par mandat (responsabilités, réalisations,
  biens livrables) est **capturée et restituée** — fin de la perte d'information relevée en EXPE-94.
- **POS-002** : **conception conforme à l'arbitrage humain** — un champ unique, à la maille du mandat, fidèle
  au libellé et à la structure de la rubrique source (pas de sur-décomposition artificielle).
- **POS-003** : **source unique respectée** — schéma défini une seule fois dans `cv-analyse`, propagé aux
  fiches couplées ; aucune coexistence incohérente avec l'ancienne conception par projet (champs
  `realisations`/`livrables` du projet retirés).
- **POS-004** : **invariants intacts** — « ne rien inventer », validation humaine granulaire, piste d'audit,
  non-transmission des CV, absence de secret.

### Négatives / points d'attention

- **NEG-001** : **relocalisation d'un champ pré-EXPE-95** — `responsabilites`, auparavant au niveau projet,
  est absorbé dans le champ unique de l'expérience. C'est un changement de maille (projet → expérience) pour
  un champ existant ; explicité au Coordinateur / à l'humain pour confirmation.
- **NEG-002** : **transition de format des données runtime** — les analyses CV écrites **avant** ce
  changement portent l'ancienne structure (voire les champs du tour 1). Comme pour ADR-0034 (NEG-002), cette
  ADR modifie la **documentation du workflow** ; les fichiers CV déjà écrits sous `${ROOT_DIRECTORY}`
  (données runtime, hors dépôt) acquièrent le champ unique à la **prochaine extraction**. Une analyse
  réutilisée sans nouvelle extraction aura simplement le champ absent (traité comme `[]`).
- **NEG-003** : **cohérence des gabarits** — un gabarit DOCX fourni peut ne pas offrir d'emplacement adapté ;
  traité par **halt-and-ask / signalement humain** (jamais de mise en page inventée).

## Alternatives étudiées

### ALT-001 — Conserver le seul champ `responsabilites` par projet (statu quo pré-EXPE-95)

**Non retenue** : cause de la perte d'information (réalisations et biens livrables non capturés).

### ALT-002 — Trois listes distinctes `responsabilites`/`realisations`/`livrables` au niveau projet (conception du tour 1)

Décomposait la rubrique source en trois axes à la maille du projet. **Non retenue** : écartée par l'arbitrage
humain **Modify** au gate EXPE-95 — l'humain veut **un seul champ** et **au niveau de l'expérience**, pas
trois listes par projet. Les champs `realisations`/`livrables` ajoutés au projet lors du tour 1 ont été
**retirés** pour éviter toute coexistence incohérente.

### ALT-003 — Champ unique mais au niveau projet (`experience[].projets[]`)

Garderait le champ fusionné mais à la maille du projet. **Non retenue** : l'arbitrage humain place
explicitement le champ **sous l'`experience` et non le projet** ; porter au projet désalignerait la
contribution par rapport à la maille voulue et poserait un problème de rattachement quand une expérience
couvre plusieurs projets.

## Notes d'implémentation

- **IMP-001** : **source unique** — ajout de `responsabilites_realisations_livrables: []` au niveau
  `experience[]` dans `plugins/rh-assistant/skills/cv-analyse/SKILL.md` (§ Format de sortie (YAML — données
  CV) + § Champs obligatoires et règles + contenu de la fiche Markdown) ; retrait des champs
  `realisations`/`livrables` et du champ `responsabilites` au niveau `experience[].projets[]`.
- **IMP-002** : **fiches couplées** — `common/stages/analyse/extraction-cv.md` (Step 1 extraction du champ
  unique par expérience, Step 3 contrôle de présence au niveau expérience / absence au niveau projet) ;
  `plugins/rh-assistant/skills/cv-generation/SKILL.md` (opération « Mise à jour d'expérience » + section
  « Responsabilités, réalisations et biens livrables » par mandat + garde-fou gabarits).
- **IMP-003** : **révision de conception** — cette ADR a d'abord été rédigée (tour 1) pour un portage par
  projet (fichier `0037-realisations-biens-livrables-par-projet-cv.md`) ; elle est **renommée**
  `0037-responsabilites-realisations-livrables-par-experience-cv.md` et réécrite après l'arbitrage humain
  **Modify** (champ unique, niveau expérience). Références croisées (CHANGELOG) mises à jour.
- **IMP-004** : **validité vérifiée** — le bloc de schéma YAML modifié dans `cv-analyse` (instance concrète
  avec le champ unique au niveau expérience) a été **parsé sans erreur** (PyYAML).
- **IMP-005** : entrée `CHANGELOG.md` (`[Non publié] → Changed`).

## Références

- **REF-001** : EXPE-95 — mission d'évolution du workflow ; **arbitrage humain Modify** au gate
  (multica.gaston, 2026-10-01 : « responsabilités, réalisations et livrables sont un seul et même champ ;
  ils sont sous l'`experience` et non le `projet` ») ; EXPE-94 — cas relevé (CV de Sylvain Goubaud).
- **REF-002** : `plugins/rh-assistant/skills/cv-analyse/SKILL.md` — source unique du schéma des données CV.
- **REF-003** : [ADR-0034](0034-format-yaml-donnees-cv.md) — données CV en YAML (schéma source-unique,
  logique de transition runtime NEG-002) ; [ADR-0036](0036-format-yaml-exclusif-workflow-matching.md) —
  format YAML exclusif de tous les artefacts de données.
- **REF-004** : invariants préservés — « ne rien inventer » et non-transmission des CV (`cv-analyse`
  § Garde-fou), validation humaine granulaire et piste d'audit (`governance-security`), anti-wake / mention
  active (EXPE-54), `trigger_outcomes` vérifiés (EXPE-58).
