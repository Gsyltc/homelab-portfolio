# Format YAML exclusif pour tous les artefacts de données du workflow Matching

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : "2026-10-01"
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — généralisation du **format de sérialisation** à **tous** les artefacts de données du workflow `matching-cv-ao`, demandée explicitement par multica.gaston (EXPE-84, 2026-10-01 : « Il y a encore des échanges qui se font avec JSON. Je veux **exclusivement du YAML**. »). La décision **lève la frontière** laissée par [ADR-0033](0033-format-yaml-compact-message-a2a.md) (enveloppe A2A) et [ADR-0034](0034-format-yaml-donnees-cv.md) (données CV), qui avaient volontairement conservé en JSON tous les **autres** artefacts. Elle **ne touche pas** les présentations Markdown aux gates humaines, ni les flags CLI `--output json`, ni le CV livrable DOCX/Markdown. Tous les invariants de gouvernance (validation humaine granulaire, piste d'audit, non-transmission des CV, mention active A2A) sont **préservés**. Aucune posture de sécurité n'est modifiée.

## Contexte

Le workflow `matching-cv-ao` échange et persiste plusieurs **artefacts de données structurées**, chacun défini par une **source unique** (compétence du plugin `rh-assistant` ou fiche de stage) et référencé **par son nom** dans les fiches de stage, les sensors, le conductor et les fiches d'agent.

Deux ADR ont déjà basculé une partie du flux en YAML :

- **[ADR-0033](0033-format-yaml-compact-message-a2a.md)** (EXPE-79) : l'**enveloppe du message A2A** (`delegation`, `retour`, `rapport-verification`) → YAML compact. Elle a **explicitement exclu** de son périmètre les schémas de données des skills, et laissé en JSON tous les artefacts de données.
- **[ADR-0034](0034-format-yaml-donnees-cv.md)** (EXPE-81) : les **données CV** (`cv-profils`, `cv-eligibilite`, fichier d'analyse versionné) → YAML. Elle a **explicitement conservé en JSON** le référentiel des contextes clients, le résumé AO, le classement, les résultats de matching, la livraison, l'inventaire CV, la réception AO et la grille remplie.

Ces deux ADR portaient la même note (NEG-003) : « toute évolution future doit maintenir cette frontière — ne pas “yamliser” par ricochet un autre schéma de données sans **décision dédiée** ».

Sur l'issue EXPE-84 (exécution réelle de l'AO NBCJP00007962), multica.gaston a constaté que des artefacts circulaient **encore en JSON** (`ao-pdf-received.json`, `cv-available.json`, `resume-ao.json`, `matching-resultats.json`, `classement-final.json`, `livraison-finale.json`) et a donné la consigne : **« Je veux exclusivement du YAML. »** Cette instruction **lève la frontière** laissée par 0033 et 0034 : c'est la **décision dédiée** annoncée par leur note NEG-003, étendue cette fois à **tous** les artefacts de données restants.

Le coût token du JSON est **structurel** (accolades, guillemets sur chaque clé/valeur, virgules, crochets) et non informationnel ; le gain de la bascule est le même que celui mesuré dans 0033 (−24,6 % cl100k sur l'enveloppe A2A) et 0034 (−24,3 % cl100k sur les données CV). L'alignement de **tous** les artefacts sur YAML supprime en outre la **double discipline** JSON+YAML (deux conventions de validité à tenir) et les **wordings d'invariant incohérents** restés formulés « JSON↔Markdown » depuis 0033 alors que l'A2A est déjà YAML.

## Décision

**Adopter le YAML comme format exclusif de tous les artefacts de données** du workflow `matching-cv-ao`, en remplacement du JSON résiduel.

### A. Artefacts de données basculés JSON → YAML

| # | Artefact | Source unique / stage producteur | Extension |
| --- | --- | --- | --- |
| A1 | `resume-ao` (résumé AO) | compétence `rfp-analyse` + stage `parse-ao` | `.yaml` |
| A2 | `matching-resultats` (scores) | compétence `matching-scoring` + stage `croisement-profils` | `.yaml` |
| A3 | `classement-final` | stages `classement-profils` + `presentation-resultats` | `.yaml` |
| A4 | `livraison-finale` | stage `cloture/livraison` | `.yaml` |
| A5 | `resultats-valides` | stage `presentation-resultats` | `.yaml` |
| A6 | `grille-remplie` | stage `remplissage-grille` | `.yaml` |
| A7 | `cv-available` (inventaire) | stage `chargement-cv` | `.yaml` |
| A8 | `ao-pdf-received` | stage `reception-ao` | `.yaml` |
| A9 | Référentiel des contextes clients `clients/<nom-client>` | compétence `contexte-client` (source unique) + consommateurs | `.yaml` |

**Mêmes champs, même sémantique.** Aucun champ n'est ajouté, retiré ni renommé ; seules changent l'**extension** (`.json` → `.yaml`) et les **pointeurs de fichiers**. Le seul renommage de champ est `clients_json` → **`clients_yaml`** (preuves d'expertise de firme dans `rfp-analyse`, qui **pointe** vers un fichier `clients/` désormais YAML) ; `cv_analyse_json` était déjà `cv_analyse_yaml` (ADR-0034).

### A9 — Référentiel `clients/<nom-client>` (décision cadrée avec l'humain)

Le référentiel des contextes clients `${ROOT_DIRECTORY}/clients/<nom-client>.json` n'est **pas un « échange »** mais un **état persistant** qu'[ADR-0034](0034-format-yaml-donnees-cv.md) avait explicitement gardé en JSON (seul le champ `sources[].cv_analyse_json` y avait été renommé `cv_analyse_yaml`). La consigne **« exclusivement du YAML »** tranche en faveur de son **inclusion dans la bascule** : le référentiel passe en `${ROOT_DIRECTORY}/clients/<nom-client>.yaml`. Son schéma source-unique (compétence `contexte-client`) est converti en YAML, et toutes les références consommatrices (`rfp-analyse`, `cv-analyse`, `cv-generation`, `parse-ao`, `extraction-cv`, `conductor`, `README`, `docs`, sensor `expertise-firme`) pointent désormais sur `.yaml`.

**Stratégie de migration des fichiers runtime** (identique à la logique NEG-002 d'ADR-0034) : cette ADR modifie **la documentation du workflow** (schéma, conventions, wording). Les fichiers `clients/*.json` déjà écrits sous `${ROOT_DIRECTORY}` relèvent des **données de runtime** (hors de ce dépôt). En pratique, la prochaine maintenance d'un client (CV long contenant un contexte client) écrit directement un `.yaml` ; un référentiel existant uniquement en `.json` doit être **converti côté runtime** (round-trip JSON→YAML, mêmes champs) ou reconstruit à la prochaine capitalisation. Un référentiel **vide ou absent** reste **normal et non bloquant** (premier run → `couverture` `non_couvert` / `verdict` `indeterminable`).

### B. Textes d'invariant alignés (A2A = YAML)

Depuis ADR-0033 l'A2A est en YAML, mais plusieurs fichiers décrivaient encore la communication agent↔agent comme « JSON ». Ils sont corrigés en **« YAML » (A2A)** tout en gardant **« Markdown » (agent↔humain)** : invariants « communication YAML↔Markdown » (`scopes-and-axes`, `scopes/README`, `scopes/format-cv`), « livrables YAML » (`reviewer`), « Format de sortie (YAML → Agent) » et « Agent↔Agent en YAML » (`rfp-analyse`, `matching-scoring`), diagramme et rôles du `conductor`, guide d'utilisation (`docs`).

### Règles de validité YAML (réutilisées de 0033 / 0034)

Les schémas introduits réutilisent **sans les redéfinir** les règles de validité déjà actées :

1. **Notation *flow* (`[...]` / `{...}`)** : mettre entre guillemets toute valeur contenant `${...}`, `:` suivi d'un espace, une virgule, `{` ou `}` (règle ADR-0033 / NEG-001).
2. **Dates ISO complètes `AAAA-MM-JJ` et dates partielles `AAAA-MM` / `present` entre guillemets** ; valeurs numériques-chaînes guillemetées, vrais nombres non quotés ; booléens réservés `yes/no/on/off` jamais employés comme valeur libre (règles ADR-0034).
3. **Au moindre doute, guillemeter.** Contrôle de **parse sans erreur** avant remise de tout livrable.
4. **Aucun secret** dans les artefacts (invariant reconduit).

## Conséquences

### Positives

- **POS-001** : **réduction de tokens généralisée** à tous les artefacts (ordre de grandeur mesuré : −24 à −27 % selon le tokeniseur, voir 0033/0034), sur un flux qui enchaîne réception AO, inventaire, résumé AO, scoring, classement, résultats validés, grille et livraison à chaque exécution.
- **POS-002** : **un seul format de données** dans tout le workflow (YAML) — plus de double discipline JSON+YAML, une seule convention de validité à tenir, cohérence totale avec le front-matter, les sensors et l'enveloppe A2A déjà en YAML.
- **POS-003** : **wordings d'invariant cohérents** — « communication YAML↔Markdown » reflète enfin la réalité depuis ADR-0033 (fin de l'incohérence « JSON↔Markdown »).
- **POS-004** : **auditabilité conservée** — YAML reste lisible à l'œil et diffable ; la piste d'audit (artefacts joints) et la mémoire persistante (référentiel clients) restent exploitables.
- **POS-005** : **invariants intacts** — validation humaine granulaire, présentation Markdown détaillée aux gates, non-transmission des CV, absence de secret, mention active A2A (anti-wake EXPE-54 / `trigger_outcomes` EXPE-58).

### Négatives / points d'attention

- **NEG-001** : **discipline de quoting YAML** à respecter sur l'ensemble des schémas (dates, numériques-chaînes, notation flow) — mitigée par « au moindre doute, guillemeter » + contrôle de parse. Les règles sont inscrites dans les schémas source-unique.
- **NEG-002** : **transition de format** — les artefacts et le référentiel `clients/` écrits **avant** ce changement restent en `.json` côté runtime (données hors dépôt) ; les artefacts éphémères (joints à l'issue) ne sont pas re-parsés comme contrat de long terme et sont réémis en YAML au run suivant ; le référentiel `clients/` persistant migre à la prochaine écriture ou par conversion côté runtime (voir A9).
- **NEG-003** : **frontière désormais fermée** — il n'existe plus de frontière « enveloppe/données CV YAML vs reste JSON » : **tous** les artefacts de données sont YAML. La seule frontière subsistante est **données (YAML) ↔ présentations humaines (Markdown)** et **flags CLI `--output json`** (syntaxe de commande, hors sujet).

## Hors périmètre (inchangé)

- **Présentations Markdown aux gates humaines** (récaps détaillés profil par profil, rapport final de livraison) — restent Markdown.
- **Flags CLI `--output json`** (`multica ... --output json`) — syntaxe de commande, sans rapport avec le format d'échange.
- **CV livrable DOCX / Markdown** (compétence `cv-generation`) — inchangé.
- **`plugin.json`** (manifeste Agent Plugins, schéma externe) — inchangé.

## Alternatives étudiées

### ALT-001 — Conserver le JSON pour les artefacts restants (statu quo 0033/0034)

**Non retenue** : contraire à la consigne explicite « exclusivement du YAML » (EXPE-84) et maintient une double discipline de format + des wordings d'invariant incohérents.

### ALT-002 — Exclure le référentiel `clients/` de la bascule (le laisser en JSON)

Option par défaut d'ADR-0034 (état persistant, pas un « échange »). **Non retenue** : « exclusivement du YAML » ne souffre pas d'exception ; la migration runtime est documentée (A9 / NEG-002) et de faible impact (fichier reconstruit/converti à la prochaine capitalisation).

### ALT-003 — JSON minifié / TOML / format maison

**Non retenues** pour les mêmes raisons qu'aux ADR-0033 (ALT-001..004) et 0034 (ALT-002..004) : perte d'auditabilité (minifié), troisième langage (TOML), fragilité (format maison). YAML est déjà le standard du dépôt.

## Notes d'implémentation

- **IMP-001** : **sources uniques converties en YAML** — `plugins/rh-assistant/skills/rfp-analyse/SKILL.md` (schéma `resume-ao`), `plugins/rh-assistant/skills/matching-scoring/SKILL.md` (schéma `matching-resultats`), `plugins/rh-assistant/skills/contexte-client/SKILL.md` (schéma `clients/<nom-client>`). Les données CV (`cv-analyse`) étaient déjà YAML (ADR-0034).
- **IMP-002** : **fiches de stage et artefacts nommés mis à jour de concert** (extension + wording) — `parse-ao.md` (A1), `croisement-profils.md` (A2), `classement-profils.md` + `presentation-resultats.md` (A3, A5), `livraison.md` (A4), `remplissage-grille.md` (A6), `chargement-cv.md` (A7), `reception-ao.md` (A8). Référentiel clients (A9) propagé dans `extraction-cv.md`, `conductor.md`, `README.md`, `docs/guide-utilisation-workflow-matching.md`, `sensors/expertise-firme.md`, `sensors/gates.md`, `sensors/README.md`, et les fiches d'agent `analyste-rfp-agent.md` / `gestionnaire-cv-agent.md`.
- **IMP-003** : **invariants A2A réalignés (B)** — `common/protocols/scopes-and-axes.md`, `scopes/README.md`, `scopes/format-cv.md`, `common/protocols/reviewer.md`, `plugins/rh-assistant/skills/rfp-analyse/SKILL.md`, `plugins/rh-assistant/skills/matching-scoring/SKILL.md`, `plugins/rh-assistant/skills/cv-generation/SKILL.md`, `common/conductor.md`, `docs/guide-utilisation-workflow-matching.md` : « JSON↔Markdown » → « YAML↔Markdown », « Agent↔Agent en JSON » → « en YAML ».
- **IMP-004** : **notes ADR-0034 mises à jour** — `cv-analyse/SKILL.md` et `extraction-cv.md` ne décrivent plus le référentiel `clients/` comme « conservé en JSON (hors périmètre CV) » mais comme désormais YAML au titre de la présente ADR.
- **IMP-005** : **renommage `clients_json` → `clients_yaml`** (preuves `expertise_firme` dans `rfp-analyse`) ; `cv_analyse_json` déjà `cv_analyse_yaml` (ADR-0034).
- **IMP-006** : **validité vérifiée** — tous les blocs de schéma YAML introduits (`rfp-analyse`, `matching-scoring`, `contexte-client`) et toutes les fences YAML des fichiers modifiés ont été **parsés sans erreur** (PyYAML). Aucune référence `.json` résiduelle hors périmètre (grep de contrôle : seuls subsistent `--output json` et `plugin.json`).
- **IMP-007** : entrée `CHANGELOG.md` (`[Non publié] → Changed`).

## Références

- **REF-001** : EXPE-84 — constat et consigne « exclusivement du YAML » (multica.gaston, 2026-10-01) ; EXPE-85 — issue de correction (en charge : Mika).
- **REF-002** : [ADR-0033](0033-format-yaml-compact-message-a2a.md) — enveloppe A2A en YAML compact (EXPE-79) ; frontière NEG-003 levée par la présente ADR.
- **REF-003** : [ADR-0034](0034-format-yaml-donnees-cv.md) — données CV en YAML (EXPE-81) ; frontière NEG-003 et exclusion du référentiel `clients/` levées par la présente ADR (A9).
- **REF-004** : [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md), [ADR-0009](0009-alignement-fiches-de-stage-sur-ai-dlc.md), [ADR-0012](0012-alignement-sensors-sur-ai-dlc.md) — YAML déjà en place pour front-matter et sensors (cohérence de format).
- **REF-005** : sources uniques — `rfp-analyse` (`resume-ao`), `matching-scoring` (`matching-resultats`), `contexte-client` (`clients/<nom-client>`), `cv-analyse` (données CV, déjà YAML).
- **REF-006** : invariants préservés — validation humaine granulaire et piste d'audit (`governance-security` § Invariants non contournables), non-transmission des CV (`cv-analyse` § Garde-fou), anti-wake / mention active (EXPE-54), `trigger_outcomes` vérifiés (EXPE-58).
