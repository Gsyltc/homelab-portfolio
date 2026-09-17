---
name: matching-scoring
description: >
    Croisement et scoring des profils du workflow Matching : calcul du score pondéré IMMUABLE (Compétences 50 % / Expérience 35 % / Études 10 % / Disponibilité 5 %) sur les seuls collaborateurs retenus par le filtre d'éligibilité amont, règle de fraîcheur des compétences (> 10 ans ignorée), double check de conformité du niveau d'études (AO gouvernemental / équivalence MIFI / compensation), classement, schéma JSON de sortie et garde-fous. Charger avant tout croisement ou calcul de score.
keywords: [matching, scoring pondere, ponderation immuable, fraicheur competences, conformite etudes, mifi, equivalence diplomes, classement profils, forces ecarts, exclusion gouvernemental, certifications requises, prerequis certification]
---

# Croisement et scoring des profils

Cette compétence porte tout le détail opératoire du **croisement exigences AO ↔ profils CV** et du **calcul du score pondéré** pour le workflow Matching. Elle est chargée par l'agent **Matcher Profils** et alimente les stages de **croisement-profils** et **classement-profils** (phase Matching) du workflow Matching.

Le Matcher **ne score que les collaborateurs retenus** par le filtre d'éligibilité amont du Gestionnaire CV : le Coordinateur ne transmet que la **liste des retenus** (`eligibilite.collaborateurs_possibles`). Les collaborateurs `exclu` et `a_verifier` du filtre d'éligibilité **ne sont pas scorés** — ils sont propagés tels quels (avec leurs raisons) au classement et à la livraison. Cela inclut les exclusions de **localisation** (collaborateur hors du rayon de proximité — 70 km par défaut — d'un AO `sur_site`/`hybride`), les exclusions de **certifications requises** (collaborateur ne détenant pas une certification marquée `obligatoire` dans l'AO — ex. AWS Certified Solutions Architect – Associate) et les `a_verifier` correspondants (ville manquante, détention de certification non confirmée) : ces décisions sont prises **en amont** par le Gestionnaire CV et **n'entrent pas dans le scoring pondéré immuable**.

> **Certifications requises = éligibilité amont, pas scoring.** Une certification exigée par l'AO (`profils_recherches[].certifications_requises` avec `criticite: "obligatoire"`) est un **prérequis éliminatoire tranché en amont** (axe `certifications` du filtre d'éligibilité). Le Matcher **ne re-score pas** ce prérequis et **ne réintègre jamais** un collaborateur exclu pour certification manquante. À l'intérieur du scoring, les certifications (comme les certifications `souhaitee`/`nice-to-have`) alimentent uniquement la **couverture Compétences (50 %)** ; elles **n'ajoutent ni critère, ni pondération** et ne modifient pas les poids immuables 50/35/10/5.

## Entrées

- Les **exigences AO** (JSON produit par `parse-ao` : `exigences`, `profils_recherches`, `ao.client_gouvernemental`, `ao.equivalence_diplomes`, `ao.localisation_travail`), **y compris les technologies et méthodologies exigées** par l'AO (portées par `exigences` / `profils_recherches`).
- La **liste des retenus** transmise par le Coordinateur (`eligibilite.collaborateurs_possibles`) — pour chaque retenu, une référence `analyse_json`.
- Pour chaque retenu, **lire soi-même** la **dernière version JSON** référencée par `analyse_json` (`cv-profils`, `<nom>-<prenom>-<AAAA-MM-JJ>.json`) — les CV ne sont **pas** transmis par le Gestionnaire CV. En plus des `competences`, lire les **agrégats collaborateur `technologies` et `methodologies`** (`{ nom, mois_experience, derniere_utilisation }`, mois d'XP en union calendaire) pour évaluer la couverture des technos/méthodos exigées par l'AO et remplir les grilles. Les versions JSON antérieures et les sources supprimés ne sont **jamais** croisés.

## Scoring pondéré

> **IMMUABLE** — ce scoring ne peut être modifié qu'avec une validation humaine explicite tracée. Aucun scope, aucune règle apprise ne peut altérer ces poids.

| Critère | Poids | Méthode de calcul |
| --- | --- | --- |
| Compétences (compétences + technologies + méthodologies) | 50 % | **Couverture regroupée** : nombre d'éléments requis par l'AO (compétences **+ technologies + méthodologies**) couverts par le profil (compétence **éligible** / techno / méthodo présente dans les agrégats et **fraîche ≤ 10 ans**) / total des éléments requis par l'AO |
| Expérience en projets | 35 % | Pertinence clients similaires + durée projets similaires (jours/personnes, mois) |
| Études | 10 % | Niveau de formation correspondant — **niveau le plus élevé parmi `etudes[]`** (après équivalence MIFI). Les certifications relèvent du critère Compétences, pas de celui-ci |
| Disponibilité | 5 % | À partir de `disponibilite.date_disponibilite` (plus la disponibilité est proche, plus le score est élevé) et `disponibilite.taux_utilisation` (plus le taux d'utilisation est bas, plus le collaborateur est disponible) |

`score_total` = somme pondérée des quatre critères, sur 100.

> **Critère Compétences (50 %) — regroupement.** Le critère Compétences **regroupe compétences + technologies + méthodologies** dans **un seul et même critère à 50 %** — il n'y a **ni nouveau critère, ni nouvelle pondération** : le regroupement se fait **à l'intérieur** du critère Compétences. La couverture = (éléments requis par l'AO — compétences, technologies **et** méthodologies — effectivement couverts par le profil) / (total des éléments requis par l'AO). Un élément requis **non couvert**, ou couvert **uniquement** par un élément **périmé** (`derniere_utilisation` à plus de 10 ans), est traité comme **non couvert** → il alimente les `ecarts`. Les mois d'XP par techno/méthodo (agrégats `mois_experience`) sont **informatifs** (grilles) et ne modifient pas cette règle de couverture.

## Règle d'éligibilité des compétences (fraîcheur)

> **Compétences / technologies / méthodologies périmées ignorées** — un élément (compétence, technologie **ou** méthodologie) dont la **dernière utilisation remonte à plus de 10 ans** (par rapport à la date du jour) est **exclu** du calcul de compatibilité.

1. Pour chaque compétence du profil, lire `derniere_utilisation` (fournie par le Gestionnaire CV) ; de même pour chaque technologie/méthodologie via `derniere_utilisation` des **agrégats** `technologies` / `methodologies`.
2. Si `date_du_jour − derniere_utilisation > 10 ans`, l'élément est **inéligible** : il ne compte ni comme couverture d'une exigence, ni dans les forces.
3. Une exigence AO (compétence, technologie ou méthodologie) couverte uniquement par un élément inéligible est traitée comme **non couverte** (elle apparaît dans les `ecarts` et dans les listes `*_manquantes`).
4. Le champ `mois_experience` (compétences comme agrégats techno/méthodo) reste indicatif mais ne modifie pas cette règle binaire de fraîcheur.
5. Journaliser les éléments écartés pour péremption (> 10 ans) dans la justification, pour la piste d'audit.

## Règle de conformité du niveau d'études (client gouvernemental) — double check aval

> **Double contrôle en aval du filtre d'éligibilité amont** — le filtre d'éligibilité du Gestionnaire CV **ne supprime pas** ce contrôle : il est **conservé** comme double vérification sur les seuls retenus. Cette règle **n'altère pas** les poids du scoring immuable (50/35/10/5). Elle agit comme un critère de conformité qui peut conduire à l'**exclusion** d'un collaborateur, sans jamais modifier la pondération du score.

Cette règle s'applique **uniquement** lorsque `ao.client_gouvernemental = true`, sur les collaborateurs **retenus** par le filtre d'éligibilité amont. Elle évalue la conformité du niveau d'études du collaborateur au **niveau requis** de l'AO (`profils_recherches[].etudes_requises`), en tenant compte de l'équivalence MIFI et de la politique de compensation de l'AO.

1. **Niveau de référence du collaborateur** : utiliser `mifi.niveau_equivalent_qc` lorsque `mifi.equivalence_requise` = `oui` ou `non_requise` — sinon le **niveau le plus élevé parmi `etudes[]`**. C'est le niveau reconnu au Québec (diplôme canadien tel quel, ou équivalence MIFI obtenue). Les **certifications** (`certifications[]`) ne sont **pas** un niveau d'études et n'entrent pas dans ce calcul.
2. **`equivalence_requise = non`** (études à l'étranger **sans** équivalence) : le diplôme n'est **pas comparable** au niveau québécois → traiter comme un **écart de niveau** (le niveau requis n'est pas atteint), **sauf** si la compensation de l'AO s'applique et est satisfaite.
3. **Compensation de l'AO** (si `equivalence_diplomes.acceptee = "oui"` et `compensation_annees_par_annee_manquante` défini) : calculer le nombre d'**années d'études manquantes** entre le niveau requis et le niveau du collaborateur, puis exiger `compensation_annees_par_annee_manquante × années_manquantes` **années d'expérience pertinente**. Comparer à l'expérience pertinente du collaborateur. Exemple : BAC requis, collaborateur DEC (≈ 3 ans manquants), compensation 3 ans/année → ~9 ans d'xp pertinente requis pour être conforme.
4. **`equivalence_requise = a_verifier`** sur un AO gouvernemental : **ne pas conclure** la conformité → statut `conforme = "a_verifier"`, **signaler à l'humain** (le MIFI n'est pas tranché). **Pas d'exclusion automatique** tant que l'humain n'a pas tranché.
5. **Exclusion** : un collaborateur **non conforme** (`conforme = "non"`) sur un AO gouvernemental est **exclu du classement** : `recommandation = "exclu"`, `score_total` neutralisé/écarté du classement principal, `motif_exclusion` explicite. L'exclusion est **reportée dans le classement et le rapport final de livraison**.

## Procédure

1. **Recevoir** les exigences AO (JSON) et la **liste des retenus** (`eligibilite.collaborateurs_possibles`). Pour chaque retenu, **lire soi-même** la dernière version JSON via `analyse_json`. **Ne pas scorer** les `exclu` ni `a_verifier` du filtre d'éligibilité amont — les propager tels quels au classement.
2. **Croiser** chaque profil CV avec les exigences AO, en appliquant la règle de fraîcheur (compétences / technologies / méthodologies > 10 ans ignorées). Pour le critère **Compétences (50 %)**, évaluer la **couverture regroupée** des compétences, **technologies** et **méthodologies** exigées par l'AO (connues vs manquantes) à partir des `competences` et des agrégats `technologies` / `methodologies` du profil.
3. **Calculer le score pondéré** (50/35/10/5) pour chaque profil.
4. **Identifier les forces et écarts** de chaque profil par rapport aux exigences.
5. **Appliquer le double check de conformité des études** si `ao.client_gouvernemental = true`.
6. **Classer les profils** par score décroissant ; les exclus (conformité études) et les `exclu`/`a_verifier` amont apparaissent avec leurs raisons hors du classement principal.
7. **Produire le JSON structuré** avec les résultats, y compris justification, forces et écarts.

## Format de sortie (JSON → Agent)

```json
{
  "resultats": [
    {
      "collaborateur": "<prénom nom>",
      "score_total": <score sur 100>,
      "score_competences": {
        "score": <sur 100>,
        "poids": 0.50,
        "regroupe": ["competences", "technologies", "methodologies"],
        "details": ["<compétence couverte (éligible)>"],
        "competences_couvertes": ["<compétence requise par l'AO et couverte (éligible ≤ 10 ans)>"],
        "competences_manquantes": ["<compétence requise par l'AO non couverte (ou périmée > 10 ans)>"],
        "technologies_couvertes": ["<technologie requise par l'AO et couverte (agrégat, fraîche ≤ 10 ans)>"],
        "technologies_manquantes": ["<technologie requise par l'AO non couverte (ou périmée > 10 ans)>"],
        "methodologies_couvertes": ["<méthodologie requise par l'AO et couverte (agrégat, fraîche ≤ 10 ans)>"],
        "methodologies_manquantes": ["<méthodologie requise par l'AO non couverte (ou périmée > 10 ans)>"],
        "mois_experience_technologies": [ { "nom": "<technologie>", "mois_experience": 0, "derniere_utilisation": "<AAAA-MM>" } ],
        "mois_experience_methodologies": [ { "nom": "<méthodologie>", "mois_experience": 0, "derniere_utilisation": "<AAAA-MM>" } ],
        "competences_ignorees_peremption": ["<compétence/techno/méthodo exclue car > 10 ans sans utilisation>"]
      },
      "score_experience": {
        "score": <sur 100>,
        "poids": 0.35,
        "details": ["<pertinence>"]
      },
      "score_etudes": {
        "score": <sur 100>,
        "poids": 0.10,
        "details": ["<niveau>"]
      },
      "score_disponibilite": {
        "score": <sur 100>,
        "poids": 0.05,
        "details": ["<disponibilité>"]
      },
      "forces": ["<force du profil>"],
      "ecarts": ["<écart par rapport aux exigences>"],
      "conformite_etudes": {
        "requise": true,
        "niveau_requis": "<ex. Baccalauréat>",
        "niveau_collaborateur": "<ex. DEC (via MIFI) | BAC canadien | étranger non équivalé>",
        "equivalence_mifi": "non_requise | oui | non | a_verifier",
        "compensation_appliquee": "<ex. '3 ans/année manquante — 9 ans requis'>",
        "annees_xp_compensation": 0,
        "conforme": "oui | non | a_verifier",
        "motif_exclusion": "<renseigné si conforme = non>",
        "justification": "..."
      },
      "recommandation": "recommande|possible|deconseille|exclu",
      "justification": "<justification courte>"
    }
  ]
}
```

> **Bloc `conformite_etudes` et valeur `recommandation: "exclu"`** : renseignés uniquement pour un AO gouvernemental (`ao.client_gouvernemental = true` → `conformite_etudes.requise = true`). Ce bloc **n'altère pas** les poids du scoring immuable ; il agit comme critère de conformité/éligibilité pouvant conduire à l'exclusion. Quand `conforme = "non"`, le collaborateur est **exclu** : `recommandation = "exclu"`, `score_total` écarté du classement principal, `motif_exclusion` explicite ; l'exclusion doit apparaître dans le classement **et le rapport final de livraison**. Quand `conforme = "a_verifier"` (MIFI non tranché sur AO gouvernemental), **ne pas exclure automatiquement** : signaler à l'humain pour décision. Pour un AO **non** gouvernemental, `conformite_etudes.requise = false` et les études sont évaluées uniquement via le critère de scoring « Études » (10 %).

## Garde-fous

- **Scoring IMMUABLE** — les poids 50/35/10/5 ne changent qu'avec une validation humaine explicite tracée. Ni la fraîcheur, ni la conformité des études, ni aucun scope ne modifie ces poids. Le **regroupement compétences + technologies + méthodologies se fait à l'intérieur du critère Compétences (50 %)** — **aucun nouveau critère, aucune nouvelle pondération**.
- **Fraîcheur > 10 ans** — s'applique aux compétences **et** aux technologies/méthodologies (via `derniere_utilisation` des agrégats) : un élément périmé ne couvre aucune exigence et alimente les `ecarts` / listes `*_manquantes`.
- **Mois d'XP techno/méthodo informatifs** — les agrégats `mois_experience` (union calendaire) servent au remplissage des grilles et à la présentation humaine ; ils ne modifient pas la règle binaire de couverture/fraîcheur.
- **Ne scorer que les retenus** — jamais les `exclu` ni les `a_verifier` du filtre d'éligibilité amont (y compris les exclusions de **localisation** et de **certifications requises `obligatoire`**) ; les propager tels quels avec leurs raisons, sans jamais réintégrer un collaborateur exclu.
- **Lire soi-même la dernière version JSON** de chaque retenu — ne jamais croiser une version antérieure ni un source supprimé ; les CV ne circulent pas en A2A.
- **Ne rien inventer** — une donnée manquante (MIFI non tranché, niveau d'études indéterminé) reste `a_verifier` et se signale à l'humain ; jamais d'exclusion sur donnée inconnue.
- **Aucun secret** dans les livrables, justifications ou notifications.

## Communication

Invariant JSON↔Markdown (Agent↔Agent en JSON, Agent↔Humain en Markdown) — défini une seule fois dans le protocole `governance-security` et le conductor ; non redéfini ici.
