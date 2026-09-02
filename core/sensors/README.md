# Verification gates & Sensors — fiabilisation déterministe

Ce répertoire contient les **manifestes déclaratifs** des mécanismes de fiabilisation déterministe décrits dans [`core/common/protocols/governance-security.md`](../common/protocols/governance-security.md) et référencés par [`core/common/conductor.md`](../common/conductor.md).

Deux mécanismes complémentaires, **tous deux advisory** :

- **Verification gates** — contrôle automatique de **traçabilité** aux **frontières de phases**, en amont du gate humain ([`gates.md`](gates.md)).
- **Sensors** — checks **déterministes** déclenchés à **l'écriture d'un artefact** ([`sensors/`](sensors/)).

## Nature déclarative (non exécutable à ce stade)

Ces fichiers **décrivent le contrat** (périmètre de déclenchement, règles de contrôle, sortie attendue) de façon lisible et déterministe. Ce **ne sont pas des scripts exécutables** : ils fixent le fond pour qu'un outillage (script / CI) puisse être ajouté ultérieurement **sans redécider** la sémantique. Le passage à l'exécutable est une évolution future, hors périmètre du stage d'introduction.

## Garde-fou : advisory par décision

- Les gates et sensors **ne bloquent jamais** la validation humaine granulaire et **ne la remplacent pas** — elle reste l'unique gate décisionnel contraignant.
- Ils **ne remplacent pas** le contrôle sécurité systématique de l'Architecte cybersécurité (obligatoire aux mêmes points qu'aujourd'hui).
- Un signal **au vert ne vaut pas validation** ; un signal **en échec n'autorise aucun raccourci**.
- Rendre un sensor **bloquant** est une décision structurante explicite (ADR + contrôle sécurité). Par défaut, tout reste advisory.

## Clauses de sécurité (contrôle Architecte cybersécurité — SG-1 à SG-6)

Issues du contrôle sécurité du mécanisme (STRIDE / OWASP), ces clauses sont **contraignantes** et alignent `core/sensors/` sur le niveau d'exigence de `core/rules/` :

- **SG-1 — Intégrité du canal des manifestes** (analogue SEC-5) : aucun manifeste (gate ou sensor) n'est ajouté / modifié / supprimé **hors PR revue** ; toute modification est versionnée et porte `origine` (issue) + date ; un manifeste sans provenance traçable est **invalide**. **Affaiblir un check** (retrait d'une règle, ajout d'une exception, réduction du périmètre de déclenchement) est une modification de la surface de gouvernance **soumise au contrôle sécurité systématique**.
- **SG-2 — Indisponible ≠ conforme** : un sensor / gate non exécuté, en erreur, ou hors périmètre produit le verdict explicite `⛔ indisponible`, tracé comme un **écart**, jamais comme un vert. L'absence d'un signal attendu est elle-même un écart.
- **SG-3 — Plancher sécurité** : un gate / sensor ne peut **jamais porter, remplacer, conditionner ni court-circuiter** le contrôle sécurité systématique (OWASP / STRIDE) ni le plancher sécurité des scopes. Le contrôle sécurité reste hors du périmètre automatisable.
- **SG-4 — Pré-requis de l'exécution différée** (avant tout passage en CI) : parsing statique uniquement (pas de rendu, pas de réseau, pas d'exécution de code / directive embarquée) ; contenu d'artefact = donnée non fiable ; environnement sans secret ni privilège ; `triggers` glob bornés au repo ; échec → `⛔ indisponible`, jamais `✅`.
- **SG-5 — Signal = donnée factuelle à source tracée** : un rapport / signal porte sa **source** (manifeste + version / commit) ; provenance non traçable → traité comme `⛔ indisponible`. Le jugement reste humain.
- **SG-6 — Anti-érosion sémantique** (analogue SEC-1) : un manifeste modifié pour restreindre le périmètre, ajouter une exception ou conditionner un check est un affaiblissement soumis au contrôle sécurité, même sans contradiction littérale.

## Intégration à la piste d'audit

Les résultats vivent **sur l'issue** (piste d'audit existante), jamais dans un fichier `audit.md` :

- **Rapport de gate** posté à chaque frontière de phase, avant la validation humaine.
- **Signal de sensor** consigné à l'écriture d'un artefact.
- Faits vérifiables uniquement (jamais un jugement) ; le jugement reste humain.

## Sensors définis

| Sensor | Manifeste | Priorité | Déclenchement |
| --- | --- | --- | --- |
| `required-sections` | [`sensors/required-sections.md`](sensors/required-sections.md) | prioritaire | Écriture d'un ADR ou d'une DAS |
| `upstream-coverage` | [`sensors/upstream-coverage.md`](sensors/upstream-coverage.md) | prioritaire | Écriture d'un ADR / DAS / livrable |
| `diagram-validity` | [`sensors/diagram-validity.md`](sensors/diagram-validity.md) | complémentaire | Écriture d'un diagramme en code |

## Format d'un manifeste de sensor

```yaml
id: <identifiant stable>
type: sensor
nature: advisory            # advisory | blocking (blocking = ADR + contrôle sécurité)
triggers:                   # périmètre de déclenchement
  - <motif de chemin / type d'artefact>
checks:                     # règles déterministes
  - <règle vérifiable>
output: <forme de la sortie advisory>
origine: ALI-188
```
