---
id: version-livrables
kind: deterministic
command: "python3 homelab/scripts/sensor.py fire version-livrables"
default_severity: advisory
severity_overrides:
  - scopes: [new-stack, infra-terraform]
    severity: blocking
description: "Vérifie que chaque livrable (compose, .tfvars) a le sha256 de la version validée et que chaque verdict de sensor requis existe pour ce sha256."
category: governance
fire_on: gate
matches: "**/.a-valider/*/*/versions.json"
origine: HOM-320
---

# Sensor `version-livrables` — livrables identiques à la version validée

Check déterministe exécuté **au gate `phase3-phase4`** et **avant le déplacement** du stage [`file-deposit`](../../common/stages/validation/file-deposit.md). Il remplace la relance des sensors : un verdict reste valable tant que le `sha256` du livrable est inchangé ([`governance-security.md`](../../common/protocols/governance-security.md) § « Un contrôle, un propriétaire »). **Bloquant** sur `new-stack` / `infra-terraform`, advisory ailleurs.

## Fichier de référence

Fichier : `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/versions.json`.

- **Généré** à chaque version validée par la QA et la revue sécurité : `python3 "$CORE_HOME/homelab/scripts/versions.py" record --dir <répertoire> <retour.yaml>...`.
- Entrées : YAML joints téléchargés (`sensors_resultats[]` d'un retour A2A, `sensors[]` d'un rapport reviewer), chacun avec le `sha256` du livrable contrôlé.
- Le script ignore et signale tout verdict sans `sha256` ou d'une autre version, et retient le verdict le plus défavorable en cas de doublon.
- Il requiert PyYAML (code 2 sans écriture sinon).
- Le fichier ne contient ni secret ni valeur de configuration.

```json
{
  "livrables": {
    "sync-in.yml": {
      "sha256": "<empreinte du fichier livré>",
      "verdicts": {
        "yaml-validity": {"verdict": "conforme", "sha256": "<empreinte contrôlée>"},
        "plaintext-secret": {"verdict": "conforme", "sha256": "<empreinte contrôlée>"},
        "swarm-deploy-section": {"verdict": "conforme", "sha256": "<empreinte contrôlée>"},
        "traefik-coherence": {"verdict": "conforme", "sha256": "<empreinte contrôlée>"}
      }
    },
    "config.tfvars": {
      "sha256": "<empreinte du fichier livré>",
      "verdicts": {
        "terraform-no-sni": {"verdict": "conforme", "sha256": "<empreinte contrôlée>"},
        "plaintext-secret": {"verdict": "conforme", "sha256": "<empreinte contrôlée>"}
      }
    }
  }
}
```

## Contrat de vérification

| Contrôle | Règle |
| --- | --- |
| Présence | Chaque livrable de `versions.json` existe dans le même répertoire. |
| Version | Le `sha256` du fichier présent est celui de `versions.json`. |
| Livrables non enregistrés | Un compose (`*.yml`, `*.yaml`) ou un `.tfvars` du répertoire absent de `versions.json` est un écart. |
| Verdicts requis | Compose : `yaml-validity`, `plaintext-secret`, `swarm-deploy-section`, `traefik-coherence`. `.tfvars` : `terraform-no-sni`, `plaintext-secret`. Chacun doit exister avec `verdict` ∈ `conforme` / `ecart` / `indisponible`. |
| Verdict périmé | Le `sha256` d'un verdict diffère de celui du livrable : verdict absent (SG-2). |

Le sensor ne juge pas le **contenu** des verdicts : un `ecart` ou un `indisponible` y reste visible et se traite chez le propriétaire du sensor. Il garantit que les verdicts portent sur la version qui sera déposée. `parametres.json`, `preselection.json` et `versions.json` ne sont pas des livrables.

## Sortie (piste d'audit)

```
Sensor version-livrables — <fichier>   (source : homelab/sensors/sensors/version-livrables.md @ <commit>)
- verdict : ✅ livrables identiques à la version validée | ⚠️ <livrable> : <écart> | ⛔ indisponible : <motif>
```

## Garde-fou

Lecture seule, parsing statique (SG-4). Aucune valeur de configuration n'est lue : seules les empreintes sont calculées. Il ne remplace ni la QA, ni la revue sécurité, ni la validation humaine (SG-3).
