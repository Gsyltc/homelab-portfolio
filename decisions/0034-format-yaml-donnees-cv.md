# Format YAML pour les données CV du workflow Matching (économie de tokens)

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : "2026-09-29"
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — changement de **format de sérialisation** des **données CV** du workflow `matching-cv-ao`, demandé et validé explicitement par multica.gaston (EXPE-81, 2026-09-29 : « Les CV doivent désormais être au format YAML et non JSON pour réduire la consommation de token. Trace la décision avec une ADR. »). La décision **ne touche que les données CV** (profils extraits, verdict d'éligibilité, fichier d'analyse versionné) ; les autres artefacts de données (référentiel clients, résumé AO, classement, résultats de matching, livraison) **restent en JSON**, et les présentations Markdown aux gates humaines sont **inchangées**. Aucune posture de sécurité n'est modifiée, tous les invariants de gouvernance (validation humaine granulaire, piste d'audit, non-transmission des CV) sont **préservés**.

## Contexte

Le workflow `matching-cv-ao` extrait chaque CV source (PDF/DOCX fourni en pièce jointe) vers des **données CV structurées** : un **fichier d'analyse versionné** à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/`, portant les profils (`cv-profils` : compétences, expériences + projets, agrégats technos/méthodos, études, certifications, MIFI, disponibilité, localisation, langues) et le **verdict d'éligibilité** (`cv-eligibilite`). Ce **schéma est défini une seule fois** dans la compétence `cv-analyse` (plugin `rh-assistant`) — **source unique** — et référencé **par son nom** par les fiches de stage, les sensors, le conductor, la compétence `cv-generation` (qui lit ces données pour produire le CV livrable) et la compétence `matching-scoring` (le Matcher lit lui-même la dernière version pour scorer).

Ces données étaient portées par un **fichier JSON** (`<nom>-<prenom>-<AAAA-MM-JJ>.json`). multica.gaston a demandé (EXPE-81) que **les CV soient désormais au format YAML et non JSON pour réduire la consommation de token**.

Le coût token du JSON des données CV est **structurel** et non informationnel : accolades, guillemets sur **chaque** clé et **chaque** valeur, virgules, crochets. Les données CV sont **volumineuses et re-lues intégralement** à chaque exécution — par le Gestionnaire CV à l'extraction, puis par le Matcher qui lit la dernière version de chaque retenu pour le scoring, et par `cv-generation` pour produire le CV livrable. Le gain se cumule donc sur toute la chaîne, à chaque profil traité.

Cette décision **prolonge** [ADR-0033](0033-format-yaml-compact-message-a2a.md) (EXPE-79), qui avait converti la **seule enveloppe du message A2A** en YAML et avait **explicitement exclu de son périmètre** les schémas de données des skills (dont `cv-analyse`), en conservant les données CV en JSON. EXPE-81 lève cette frontière **pour les seules données CV** : c'est la décision dédiée annoncée par la note NEG-003 de l'ADR-0033 (« toute évolution future doit maintenir cette frontière — ne pas “yamliser” par ricochet un schéma de données de skill sans décision dédiée »).

### Mesure réelle (préalable à la décision)

Mesure BPE sur un **échantillon représentatif** de données CV (`cv-profils` + verdict `eligibilite` pour 2 collaborateurs, avec expériences, projets, agrégats technos/méthodos, études, certifications, MIFI, disponibilité, localisation), même information dans les deux formats, YAML valide vérifié par parse (round-trip PyYAML identique) :

| Format | tokens cl100k | tokens o200k | caractères | Δ cl100k | Δ o200k | Δ caractères |
| --- | --- | --- | --- | --- | --- | --- |
| JSON (indenté 2 espaces) | 2464 | 2404 | 9065 | référence | référence | référence |
| **YAML (bloc)** | **1865** | **1790** | **5865** | **−24,3 %** | **−25,5 %** | **−35,3 %** |
| JSON minifié (référence) | 1646 | 1616 | 5590 | −33,2 % | −32,8 % | −38,3 % |

- Tokeniseur `cl100k_base` (famille GPT-3.5/4) : **−24,3 %**. Contre-mesure `o200k_base` (famille GPT-4o) : **−25,5 %**. Économie de caractères : **−35,3 %**.
- Le gain provient de la **structure** (suppression des guillemets de clés, accolades, virgules ; indentation à la place des délimiteurs). La part **variable** (valeurs libres : noms, descriptions, responsabilités…) est identique d'un format à l'autre — le pourcentage réel sur un CV donné varie autour de ~25 % selon la proportion de contenu libre.
- Le **JSON minifié** économiserait un peu plus (~33 %) mais au prix de la **lisibilité de la piste d'audit** (une seule ligne dense) — écarté pour la même raison qu'à l'ADR-0033 (ALT-003).
- **Validité** : l'échantillon YAML a été **parsé sans erreur** et **round-trip identique** (PyYAML). Cinq règles de validité ont été identifiées et intégrées au schéma (voir Décision).

## Décision

**Adopter le YAML comme format des données CV** du workflow `matching-cv-ao`, en remplacement du JSON, pour le **seul** périmètre des données CV.

**Périmètre — données CV uniquement** :

- le **fichier d'analyse versionné** par collaborateur : `<nom>-<prenom>-<AAAA-MM-JJ>.json` → **`<nom>-<prenom>-<AAAA-MM-JJ>.yaml`** (à la racine de `${ROOT_DIRECTORY}/collaborateurs/<nom-prenom>/cv/`, jamais écrasé, historique conservé) ;
- l'artefact **`cv-profils`** (liste `collaborateurs`) et l'artefact **`cv-eligibilite`** (objet `eligibilite` à 3 états) ;
- le **champ de référence** `analyse_json` → **`analyse_yaml`** (dans `cv-profils`, dans `eligibilite.collaborateurs_possibles`, et dans l'entrée `sources[]` du référentiel clients : `cv_analyse_json` → `cv_analyse_yaml`).

Schéma de référence : **source unique dans `cv-analyse` (§ Format de sortie (YAML — données CV))** — **mêmes champs, même sémantique** que l'ancien JSON, rien n'est ajouté, retiré ni renommé hormis `analyse_json` → `analyse_yaml` et l'extension `.json` → `.yaml`.

Règles de conception associées, validées par l'humain (EXPE-81) :

1. **Périmètre = données CV uniquement.** Restent en JSON (hors périmètre, explicitement exclus) : le **référentiel des contextes clients** `${ROOT_DIRECTORY}/clients/<nom-client>.json` (schéma défini dans `contexte-client` — ce n'est pas un CV), le **résumé AO** (`resume-ao.json`), le **classement** (`classement-final`), les **résultats de matching** (`matching-resultats.json`), la **livraison** (`livraison-finale`), les **résultats validés** (`resultats-valides`), l'**inventaire CV** (`cv-available` — un listing d'audit, pas des données CV), la **réception AO** (`ao-pdf-received`) et la **grille remplie** (`grille-remplie`). L'**enveloppe du message A2A** est déjà en YAML (ADR-0033). Les **flags CLI `--output json`** (syntaxe de commande) sont sans rapport.
2. **Mêmes champs, même sémantique.** Aucun champ n'est ajouté, retiré ni renommé (hormis `analyse_json` → `analyse_yaml`) ; l'auditabilité est intégralement préservée (le YAML **est** la mémoire persistante et la piste d'audit, comme l'était le JSON).
3. **Cinq règles de validité YAML (intégrées au schéma source-unique `cv-analyse`).** Le YAML des données CV doit rester **parsable sans ambiguïté de type** :
   - **Dates ISO complètes `AAAA-MM-JJ` toujours entre guillemets** (`date_derniere_modification`, `disponibilite.date_disponibilite`) — non quotées, elles seraient interprétées comme des **objets date** par le parseur.
   - **Dates partielles `AAAA-MM` et `present` entre guillemets** (`date_debut`, `date_fin`, `derniere_utilisation`, `certifications[].date_expiration`) — par cohérence, pour éviter toute coercition.
   - **Valeurs numériques restant des chaînes entre guillemets** (`annee_obtention`, `certifications[].reference`) ; les vrais nombres (`mois_experience`, `duree_mois`, `jours_personnes`, `taux_utilisation`) restent **non quotés**.
   - **Booléens réservés** : `conserve: false` est un vrai booléen (correct) ; les énums `oui`/`non` de `mifi.equivalence_requise` restent des **chaînes** (sûres) ; **ne jamais** employer `yes/no/on/off` comme valeur libre.
   - **Notation *flow* (`[...]` / `{...}`)** : mettre entre guillemets toute valeur contenant `${...}`, `:` suivi d'un espace, une virgule, `{` ou `}`. Au moindre doute, guillemeter.
4. **Aucun secret** dans le YAML des données CV (invariant reconduit à l'identique).
5. **Non-transmission des CV inchangée** : seuls le verdict d'éligibilité et la référence `analyse_yaml` des retenus circulent en A2A ; ni les sources, ni les fiches Markdown, ni le YAML complet des données CV ne sont transmis (invariant `cv-analyse` § Garde-fou).

## Conséquences

### Positives

- **POS-001** : **~25 % de tokens en moins par lecture de données CV** (mesure réelle : −24,3 % cl100k / −25,5 % o200k), sur des données **volumineuses et re-lues plusieurs fois par exécution** (extraction, scoring de chaque retenu, génération du CV livrable) → économie cumulée sur toute la chaîne et à chaque profil.
- **POS-002** : **alignement avec l'existant du dépôt** — le front-matter des fiches de stage, les manifestes de sensors ([ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md), [ADR-0009](0009-alignement-fiches-de-stage-sur-ai-dlc.md), [ADR-0012](0012-alignement-sensors-sur-ai-dlc.md)) et l'enveloppe A2A ([ADR-0033](0033-format-yaml-compact-message-a2a.md)) sont **déjà en YAML**. Aucun nouveau paradigme introduit.
- **POS-003** : **auditabilité conservée** — le YAML reste lisible à l'œil, la mémoire CV et la piste d'audit restent exploitables ; le gain n'est pas obtenu au prix de clés cryptiques (l'option « clés courtes » a été écartée pour cette raison).
- **POS-004** : **invariants intacts** — validation humaine granulaire, présentation Markdown détaillée aux gates, non-transmission des CV, absence de secret et piste d'audit sont **inchangés**. Le versionnage (fichier daté du jour, jamais écrasé, dernière version seule croisée avec un AO) est **identique**, sur `.yaml` au lieu de `.json`.

### Négatives / points d'attention

- **NEG-001** : **règles de quoting à respecter** — dates ISO complètes, dates partielles et valeurs numériques-chaînes doivent être guillemetées, sinon le YAML est mal typé (date, entier) ou invalide. Les cinq règles sont **inscrites dans le schéma source-unique** `cv-analyse` (§ Règles de validité YAML) et référencées dans le stage `extraction-cv` (écriture + contrôle) ; elles restent une discipline d'écriture (mitigée par « au moindre doute, guillemeter » + contrôle de parse au Step 3).
- **NEG-002** : **transition de format** — les analyses CV écrites **avant** ce changement restent en `.json` sous `${ROOT_DIRECTORY}/collaborateurs/` (données de runtime, hors de ce dépôt). Cette ADR modifie **la documentation du workflow** (schéma, conventions, wording) ; la **migration des fichiers `.json` existants** vers `.yaml` relève des données de runtime et n'est pas portée par ce dépôt. En pratique, la prochaine extraction d'un collaborateur (nouvelle pièce jointe) produit directement un `.yaml` ; un collaborateur sans nouvelle pièce jointe mais avec une ancienne analyse `.json` doit être re-extrait ou son fichier converti côté runtime.
- **NEG-003** : **frontière données CV ↔ autres données à tenir** — les données CV sont YAML, mais les artefacts non-CV référencés (référentiel clients, résumé AO, classement, résultats de matching, livraison, inventaire) restent JSON. Toute évolution future doit maintenir cette frontière explicite (ne pas « yamliser » par ricochet un autre schéma de données sans décision dédiée). Le référentiel clients `clients/<nom-client>.json` reste **JSON** : seul le champ `sources[].cv_analyse_json` y a été renommé `cv_analyse_yaml` car il **pointe** vers un fichier CV désormais YAML.

## Alternatives étudiées

### ALT-001 — Conserver le JSON (statu quo)

**Non retenue** : ne répond pas à la demande explicite de réduction de tokens (EXPE-81). Le JSON indenté est le format le plus coûteux en tokens de structure sur des données CV volumineuses re-lues plusieurs fois par exécution.

### ALT-002 — JSON minifié (sans espaces/retours)

Économie la plus élevée mesurée (~33 % cl100k). **Non retenue** : **perte de lisibilité** de la mémoire CV et de la piste d'audit (une seule ligne très dense, difficilement relisible/diffable par l'humain). Même arbitrage qu'à l'ADR-0033 (ALT-003) : le gain marginal (~8 points) face au YAML ne justifie pas la perte d'auditabilité.

### ALT-003 — TOML

Lisible et compact, mais **introduirait un troisième langage de sérialisation** dans un dépôt déjà standardisé sur YAML (front-matter, sensors, enveloppe A2A) + JSON (autres données). Coût cognitif sans bénéfice décisif sur YAML. **Non retenue.**

### ALT-004 — YAML à clés courtes / format maison

Gain supérieur possible, mais **mémoire CV illisible à l'audit** et fragile (table de correspondance implicite) — contraire à l'exigence de piste d'audit exploitable et à la non-transmission bien tracée des CV. **Non retenue.**

## Notes d'implémentation

- **IMP-001** : **source unique** — schéma des données CV converti en YAML dans `plugins/rh-assistant/skills/cv-analyse/SKILL.md` (§ Format de sortie (YAML — données CV) + § Versionnage YAML), avec la note de périmètre (ADR-0034) et les **cinq règles de validité YAML** (§ Règles de validité YAML). Renommage `analyse_json` → `analyse_yaml` et `.json` → `.yaml` dans toute la compétence (règle de sélection de la source CV, structure `cv/`, garde-fou de non-transmission).
- **IMP-002** : **fichiers couplés mis à jour de concert** (wording de format des données CV JSON → YAML uniquement) — stage `common/stages/analyse/extraction-cv.md` (front-matter `outputs`, écriture du fichier `.yaml`, contrôle du livrable au Step 3 avec contrôle de parse, `cv-eligibilite.yaml`), `common/stages/initialisation/chargement-cv.md` (inventaire des analyses `.yaml`, réutilisation du cache YAML), `common/stages/matching/croisement-profils.md` (le Matcher lit la dernière version YAML via `analyse_yaml`), `common/stages/cloture/mise-a-jour-cv.md` (fiche + YAML = mémoire), `common/conductor.md` (tableau de stockage, note format du CV livrable, diagramme de séquence `cv-eligibilite.yaml`), `sensors/localisation.md` / `disponibilite.md` / `equivalence-mifi.md` (« du YAML `cv-profils` »), `scopes/standard.md` / `complex.md` / `express.md` / `format-cv.md` (flux YAML, § Versionnage YAML), `README.md` (tableau des compétences, schéma YAML, tableau de stockage, note de communication + frontière ADR-0034), la fiche d'agent `agents/gestionnaire-cv-agent.md`, les compétences `plugins/rh-assistant/skills/cv-generation/SKILL.md` (lit la dernière version YAML) et `plugins/rh-assistant/skills/matching-scoring/SKILL.md` (le Matcher lit la dernière version YAML), et `docs/guide-utilisation-workflow-matching.md`.
- **IMP-003** : **hors périmètre, conservé en JSON** — référentiel des contextes clients `clients/<nom-client>.json` (schéma `contexte-client`, seul le champ `sources[].cv_analyse_json` renommé `cv_analyse_yaml` car il pointe vers un fichier CV YAML), `resume-ao.json`, `classement-final`, `matching-resultats.json`, `livraison-finale`, `resultats-valides`, `cv-available` (inventaire d'audit), `ao-pdf-received`, `grille-remplie` ; l'**enveloppe A2A** (déjà YAML, ADR-0033) ; les **flags CLI `--output json`**.
- **IMP-004** : **validité vérifiée** — le bloc de schéma YAML introduit dans `cv-analyse` et l'échantillon de mesure ont été **parsés sans erreur** (PyYAML), l'échantillon en round-trip identique. Les cinq règles de validité ont été dérivées de tests de coercition de type réels (dates, numériques, booléens réservés).
- **IMP-005** : entrée `CHANGELOG.md` (`[Non publié] → Changed`).

## Références

- **REF-001** : EXPE-81 — demande et validation du changement de format des données CV (multica.gaston, 2026-09-29 : « Les CV doivent désormais être au format YAML et non JSON pour réduire la consommation de token. Trace la décision avec une ADR. »).
- **REF-002** : `plugins/rh-assistant/skills/cv-analyse/SKILL.md` (§ Format de sortie (YAML — données CV), § Versionnage YAML, § Règles de validité YAML) — source unique du schéma des données CV, désormais en YAML.
- **REF-003** : [ADR-0033](0033-format-yaml-compact-message-a2a.md) — format YAML compact de l'enveloppe A2A (EXPE-79) ; la présente ADR en prolonge la logique aux données CV, levant la frontière annoncée par sa note NEG-003.
- **REF-004** : [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md), [ADR-0009](0009-alignement-fiches-de-stage-sur-ai-dlc.md), [ADR-0012](0012-alignement-sensors-sur-ai-dlc.md) — YAML déjà en place pour front-matter et sensors (cohérence de format).
- **REF-005** : `matching-cv-ao/common/stages/analyse/extraction-cv.md` — producteur des données CV (`cv-profils`, `cv-eligibilite`) ; `plugins/rh-assistant/skills/matching-scoring/SKILL.md` et `plugins/rh-assistant/skills/cv-generation/SKILL.md` — consommateurs de la dernière version YAML.
- **REF-006** : invariants préservés — non-transmission des CV (`cv-analyse` § Garde-fou), validation humaine granulaire et piste d'audit (`governance-security` § Invariants non contournables), anti-wake / mention active (EXPE-54), `trigger_outcomes` vérifiés (EXPE-58).
