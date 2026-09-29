# Format YAML compact pour l'enveloppe du message A2A (économie de tokens)

---
auteurs: Mika (agent)
accepté par : multica.gaston
accepté le : "2026-09-29"
supersedes: ""
superseded_by: ""

---

## Status

Accepted

> Statut **Accepted** — changement de **format d'échange** de l'enveloppe du message A2A du workflow `matching-cv-ao`, demandé et validé explicitement par multica.gaston (EXPE-79, 2026-09-29 : « oui / B / oui »). La décision **ne touche que l'enveloppe A2A** (les schémas de données des skills et les présentations Markdown aux gates humaines restent inchangés) et **préserve tous les invariants de gouvernance A2A**. Aucune posture de sécurité n'est modifiée.

## Contexte

La communication **agent↔agent (A2A)** du workflow `matching-cv-ao` repose sur un **message A2A** joint à l'issue : trois types (`delegation`, `retour`, `rapport-verification`), dont le **schéma est défini une seule fois** dans `matching-cv-ao/common/protocols/governance-security.md` et référencé **par son nom** (« message A2A ») dans les fiches de stage, les sensors, le conductor et les fiches d'agent.

Ce message était porté par un **fichier JSON**. multica.gaston a signalé (EXPE-79) que « le JSON pour la communication A2A est coûteux » et demandé un **format plus léger économisant des tokens**, avec la consigne explicite **« pas de modification sans approbation humaine »**.

Le coût token de l'enveloppe A2A est **structurel** et non informationnel : accolades, guillemets sur **chaque** clé et **chaque** valeur, virgules, crochets, et **noms de clés répétés à chaque message**. Le fil de commentaires est, lui, **déjà minimal** (mention active + nom du fichier joint — invariants EXPE-54/EXPE-58) ; le gain doit donc venir de la **seule enveloppe**, re-lue intégralement par l'agent suivant à chaque handoff.

### Mesure réelle (préalable à la décision — demandée par l'humain)

Mesure BPE sur un **échantillon représentatif** des trois types de message (enveloppe équivalente JSON vs YAML compact, même information, YAML valide vérifié par parse) :

| Type de message | JSON (tokens) | YAML compact (tokens) | Économie |
| --- | --- | --- | --- |
| `delegation` | 325 | 258 | **−20,6 %** |
| `retour` | 184 | 138 | **−25,0 %** |
| `rapport-verification` | 284 | 202 | **−28,9 %** |
| **TOTAL** | **793** | **598** | **−24,6 %** |

- Tokeniseur `cl100k_base` (famille GPT-3.5/4) : **−24,6 %**. Contre-mesure `o200k_base` (famille GPT-4o) : **−26,9 %** (761 → 556). Économie de caractères : −18,5 %.
- Le gain provient de la **structure** (suppression des guillemets de clés, accolades, virgules ; listes en notation *flow* courte). La part **variable** (valeurs libres : `objet`, `perimetre`, `detail`…) est identique d'un format à l'autre — le pourcentage réel sur un message donné varie donc autour de ~25 % selon la proportion de contenu libre.
- **Validité** : tous les échantillons YAML ont été **parsés sans erreur** (PyYAML). Deux règles de validité ont été identifiées et intégrées au schéma (voir Décision).

## Décision

**Adopter le YAML compact comme format de l'enveloppe du message A2A** (`delegation`, `retour`, `rapport-verification`), en remplacement du JSON, pour le **seul** workflow `matching-cv-ao`.

Schéma de référence (source unique — `governance-security.md`) :

```yaml
type: delegation | retour | rapport-verification
de: <nom de l'agent émetteur>
vers: <nom de l'agent destinataire ou 'humain'>
stage: <slug du stage concerné>
objet: <phrase courte — ce qui est demandé ou livré>
perimetre: [<élément de périmètre>, ...]
criteres_acceptation: [<critère>, ...]
artefacts:
  - {role: produit | consomme, nom: <fichier>.yaml, chemin: "${ROOT_DIRECTORY}/..."}
resultat: {statut: ok | ecart | halt, detail: <optionnel>}
gate_humaine: aucune | legere | granulaire | explicite
reference_audit: <id de commentaire ou d'artefact>
```

Règles de conception associées, validées par l'humain (EXPE-79) :

1. **Périmètre = enveloppe A2A uniquement.** Le changement porte sur le **message A2A** (le fichier joint qui transporte la mission / le retour / le rapport de vérification). Les **schémas de données** portés par les skills du plugin `rh-assistant` (`cv-analyse`, `contexte-client`, `matching-scoring`) et les **fichiers de données** correspondants (`resume-ao.json`, `cv-eligibilite.json`, `classement-final`, `matching-resultats.json`, `clients/<nom-client>.json`, `livraison-finale`, `resultats-valides`, `cv-available`, `ao-pdf-received`) **restent en JSON** — hors périmètre, explicitement exclus.
2. **Mêmes champs, même sémantique.** Aucun champ n'est ajouté, retiré ni renommé ; l'auditabilité est intégralement préservée (le YAML joint **est** la piste d'audit, comme l'était le JSON).
3. **Deux règles de validité YAML (intégrées au schéma).** En notation *flow* (`[...]` / `{...}`), **mettre entre guillemets** toute valeur contenant `${...}`, `{`, `}`, `:` suivi d'un espace, ou une **virgule** (ex. `chemin: "${ROOT_DIRECTORY}/..."`, `detail: "5 profils, 1 exclu"`). Les champs non pertinents (dont `detail` vide) sont **omis**. Un doute sur la validité ⇒ passer la valeur en guillemets.
4. **Aucun secret** dans le YAML (invariant reconduit à l'identique).

## Conséquences

### Positives

- **POS-001** : **~25 % de tokens en moins par handoff A2A** (mesure réelle : −24,6 % cl100k / −26,9 % o200k), sur un flux qui enchaîne plusieurs délégations/retours par exécution → économie cumulée sur toute la chaîne.
- **POS-002** : **alignement avec l'existant du dépôt** — le front-matter des fiches de stage et les manifestes de sensors sont **déjà en YAML** ([ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md), [ADR-0009](0009-alignement-fiches-de-stage-sur-ai-dlc.md), [ADR-0012](0012-alignement-sensors-sur-ai-dlc.md)). Aucun nouveau paradigme introduit.
- **POS-003** : **auditabilité conservée** — YAML reste lisible à l'œil, la piste d'audit reste exploitable ; le gain n'est pas obtenu au prix de clés cryptiques (l'option « clés courtes » a été écartée pour cette raison).
- **POS-004** : **invariants intacts** — le lien de mention actif (seul vecteur de déclenchement), la validation humaine granulaire, la présentation Markdown détaillée aux gates, l'absence de secret et la piste d'audit sont **inchangés**.

### Négatives / points d'attention

- **NEG-001** : **règle de quoting à respecter** — en notation *flow*, les valeurs contenant `${...}`, une virgule ou `:` doivent être guillemetées, sinon le YAML est invalide. La règle est **inscrite dans le schéma source-unique** et dans `sensors/gates.md`, mais reste une discipline d'écriture (mitigée par : « au moindre doute, guillemeter »).
- **NEG-002** : **transition de format** — les messages A2A émis **avant** ce changement restent en JSON (pièces jointes éphémères, non re-parsées comme contrat de long terme) ; les runs postérieurs émettent du YAML. Aucune migration d'historique nécessaire.
- **NEG-003** : **frontière enveloppe ↔ données à tenir** — l'enveloppe est YAML, mais les artefacts de données qu'elle référence restent JSON (skills). Toute évolution future doit maintenir cette frontière (ne pas « yamliser » par ricochet un schéma de données de skill sans décision dédiée).

## Alternatives étudiées

### ALT-001 — TOML compact

Économie estimée proche du YAML (~30–40 % sur la structure), bonne lisibilité. **Non retenue** : introduirait un **troisième langage de sérialisation** dans un dépôt déjà standardisé sur YAML (front-matter, sensors) + JSON (données) ; coût cognitif sans bénéfice décisif sur YAML.

### ALT-002 — Format maison « clé: valeur » minimaliste (le plus économe)

Économie la plus élevée (~45–55 %). **Non retenue** : imposerait un **parseur/convention maison** à cadrer et à maintenir, au détriment de la robustesse et de la lisibilité outillée ; risque supérieur pour un gain marginal face au YAML.

### ALT-003 — JSON minifié (sans espaces/retours)

**Non retenue** : gain faible (~10–15 %, la ponctuation JSON demeure) et **perte de lisibilité** de la piste d'audit.

### ALT-004 — JSON à clés courtes (`t`, `de`, `v`, `o`…)

**Non retenue** : gain modéré (~20–30 %) mais **enveloppe illisible à l'audit** et fragile (table de correspondance implicite) — contraire à l'exigence de piste d'audit exploitable.

## Notes d'implémentation

- **IMP-001** : **source unique** — schéma de l'enveloppe A2A converti en YAML compact dans `matching-cv-ao/common/protocols/governance-security.md` (§ « Schéma du message A2A »), avec la note de périmètre + les deux règles de validité YAML. Les fiches qui référencent « message A2A » **par leur nom** n'ont pas à redéfinir le schéma.
- **IMP-002** : **fichiers couplés mis à jour de concert** (wording d'enveloppe JSON → YAML uniquement) — `common/protocols/stage-protocol.md`, `sensors/gates.md` (bloc `verdicts` du `rapport-verification` en YAML), `README.md` (§ Communication), `common/conductor.md` (rôles, vecteurs, invariants, diagramme de séquence : `mission.yaml`), les fiches de délégation/retour (`stages/analyse/parse-ao.md`, `stages/analyse/extraction-cv.md`, `stages/matching/croisement-profils.md`, `stages/cloture/mise-a-jour-cv.md`), `common/protocols/reviewer.md`, et les fiches d'agent (`coordinateur-matching-agent.md`, `matcher-profils-agent.md`).
- **IMP-003** : **hors périmètre, conservé en JSON** — schémas et fichiers de données des skills (`cv-analyse`, `contexte-client`, `matching-scoring`) et artefacts de données nommés (`resume-ao.json`, `cv-eligibilite.json`, `classement-final`, `matching-resultats.json`, `clients/*.json`, `livraison-finale`, `resultats-valides`, `cv-available`, `ao-pdf-received`) ; ainsi que les **flags CLI `--output json`** (syntaxe de commande, sans rapport avec l'enveloppe).
- **IMP-004** : **validité vérifiée** — tous les blocs de schéma YAML introduits (`governance-security.md`, `sensors/gates.md`) et les échantillons de mesure ont été **parsés sans erreur** (PyYAML).
- **IMP-005** : entrée `CHANGELOG.md` (`[Non publié] → Changed`).

## Références

- **REF-001** : EXPE-79 — demande et validation du changement de format A2A (multica.gaston, 2026-09-29 : périmètre = enveloppe A2A seule ; format = B / YAML compact ; mesure réelle préalable = oui).
- **REF-002** : `matching-cv-ao/common/protocols/governance-security.md` (§ Schéma du message A2A) — source unique du schéma d'enveloppe A2A, désormais en YAML compact.
- **REF-003** : `matching-cv-ao/common/protocols/stage-protocol.md` — cycle A2A (délégation temps 2, retour temps 3, rapport de vérification gate).
- **REF-004** : `matching-cv-ao/sensors/gates.md` — sous-schéma `verdicts` du `rapport-verification` (YAML).
- **REF-005** : [ADR-0007](0007-adaptation-modele-conductor-stages-protocols.md), [ADR-0009](0009-alignement-fiches-de-stage-sur-ai-dlc.md), [ADR-0012](0012-alignement-sensors-sur-ai-dlc.md) — YAML déjà en place pour front-matter et sensors (cohérence de format).
- **REF-006** : invariants A2A préservés — anti-wake / mention active (EXPE-54), `trigger_outcomes` vérifiés (EXPE-58), validation humaine granulaire et piste d'audit (`governance-security` § Invariants non contournables).
