---
title: Scopes — un fichier par scope (source d'identité)
contract: Contrat amont « Scopes » (Harness Engineer Guide)
---

# Scopes — un fichier de données par scope

Cette couche porte l'**identité** de chaque scope, en données déclaratives, alignée sur
le contrat amont « Scopes » (*Harness Engineer Guide*).

## Le contrat en deux moitiés

Un scope se déclare en **deux endroits**, et cette séparation est l'idée maîtresse :

1. **L'identité** vit dans son propre fichier — `core/scopes/<name>.md` (un fichier par scope,
   à l'image de `core/sensors/`). Il porte le nom du scope, ses métadonnées de routage
   (`keywords`) et ses **valeurs par défaut** d'axes (`depth`, niveau de vérification →
   `review_cap`).
2. **L'appartenance** (quels stages s'exécutent sous ce scope) vit **transposée sur les
   stages** : chaque fiche de stage (`core/common/stages/<phase>/<slug>.md`) nomme dans son
   front-matter `scopes:` les scopes sous lesquels elle s'exécute. Un stage qui ne nomme pas un
   scope est ignoré (`SKIP`) sous ce scope ; les **3 stages d'Initialization** nomment **tous**
   les scopes (ils s'exécutent toujours).

La liaison entre les deux est le **nom du scope**. L'appartenance est ainsi déclarée **une seule
fois, sur le stage**, jamais redéclarée dans huit blocs de scope séparés.

> **Source d'identité.** Ces fichiers sont désormais la **source d'identité** des scopes. Le
> tableau de [`../common/protocols/scopes-and-axes.md`](../common/protocols/scopes-and-axes.md)
> reste une **vue lisible** (matrice stage × scope, ordre de désambiguïsation, garde-fous) ;
> en cas d'écart sur l'identité d'un scope (nom, depth, mots-clés, vérification), **le fichier de
> scope fait foi**.

## Schéma du front-matter

```yaml
name: <scope>                 # requis — nom du scope (= stem du fichier)
depth: minimal|standard|comprehensive   # requis — détail des artefacts par défaut
verification: advisory|standard|renforcé # requis (maison) — niveau de vérification par défaut
review_cap: advisory|none               # optionnel — plafond de classe de revue (voir divergence)
keywords: [ ... ]             # optionnel — déclencheurs d'auto-détection FR / EN (liste plate)
description: "<une ligne>"    # optionnel — libellé court (vue d'aide / lisible)
skeleton: on|off              # optionnel — cérémonie walking-skeleton en Construction
```

Le corps Markdown qui suit le front-matter porte l'**intention en prose** : pourquoi ces stages,
pourquoi ceux-là sont allégés ou ignorés.

## Divergence assumée : axe « vérification » vs `testStrategy` amont

Le contrat amont sépare deux axes indépendants du scope : **Depth** (détail des artefacts) et
**Test strategy** (volume de tests). Ce workspace produit **majoritairement de la documentation
d'architecture** (DAS, ADR, diagrammes) plutôt que du code applicatif. L'axe « test strategy »
amont y est donc peu pertinent tel quel.

Décision (tracée en [ADR-0003](../../decisions/0003-scopes-et-axes-depth-verification.md), affinée
en [ADR-0010](../../decisions/0010-scopes-fichiers-par-scope-et-axes-review-cap.md)) :

- Champ maison **`verification`** — `advisory` / `standard` / `renforcé` (rigueur du contrôle des
  livrables) — **remplace** le `testStrategy` amont pour la documentation, **avec repli sur une
  stratégie de tests dès qu'un livrable comporte du code ou de l'IaC**.
- **Mapping vers `review_cap`** (champ du contrat amont — plafond de classe de revue,
  `adversarial` / `advisory` / `none`) : un scope à vérification **allégée** porte un `review_cap`
  pour matérialiser le plafond de revue en donnée conforme au contrat. Absence de `review_cap` =
  aucun abaissement au niveau du scope.

  | `verification` (maison) | `review_cap` (contrat amont) |
  | --- | --- |
  | `advisory` | `advisory` |
  | `standard` | *(absent — pas d'abaissement)* |
  | `renforcé` | *(absent — jamais abaissé)* |

  Un `review_cap` **abaisse** la `review_class` d'un stage mais ne la **relève jamais**
  (cohérent avec le garde-fou sécurité : plancher non abaissable).

## Garde-fous (non désactivables par un scope)

Rappel des invariants (détail : [`../common/protocols/governance-security.md`](../common/protocols/governance-security.md)) :

- Validation humaine granulaire, ADR sur décision structurante, piste d'audit, contrôle sécurité
  minimal (OWASP / STRIDE) — **aucun scope ne les désactive**.
- Sur `security-patch` / `enterprise` : `depth` ≥ `standard` et `verification` ≥ `renforcé` ;
  aucun `review_cap` abaissant.
- Auto-détection = **plancher** : la confirmation humaine peut monter le contrôle, jamais le
  descendre sans validation tracée.

## Non applicable ici (tooling amont)

Pas de compilation `scope-grid.json`, pas de moteur TypeScript, pas de champs `runner` /
`freeform_default` : l'exécution passe par **Multica**, pas par le harness amont. On adopte la
**forme déclarative** (un fichier par scope, front-matter, appartenance transposée) sans importer
le tooling non applicable (cadrage : [ADR-0001](../../decisions/0001-alignement-core-workflow-sur-ai-dlc-2.0.md)).

## Ordre de désambiguïsation

En cas de correspondances multiples de mots-clés (voir la vue lisible pour le détail) :

`security-patch` > `enterprise` > `infra` > `feature` > `mvp` > `poc` > `express` > `standard`

Défaut : **`standard`** en l'absence de mot-clé détecté.
