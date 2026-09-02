# Verification gates & Sensors — fiabilisation déterministe

Ce répertoire contient les **manifestes déclaratifs** des mécanismes de fiabilisation déterministe décrits dans la section « Verification gates & Sensors » de [`docs/core-workflow.md`](../../docs/core-workflow.md). Décision structurante tracée dans [ADR-0005](../../decisions/0005-verification-gates-et-sensors.md).

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

## Intégration à la piste d'audit

Les résultats vivent **sur l'issue** (piste d'audit existante — [ADR-0004](../../decisions/0004-boucle-apprentissage-et-regles-persistantes.md)), jamais dans un fichier `audit.md` :

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
