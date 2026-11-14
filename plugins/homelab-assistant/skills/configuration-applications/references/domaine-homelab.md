# Domaine DNS du homelab

Fichier de référence de la skill `configuration-applications`. **Source unique** du domaine DNS du homelab, utilisé pour proposer le FQDN par défaut d'une stack (`${fqdn}`).

## Valeur

| Clé | Valeur |
|---|---|
| `homelab_domain` | `jeedom-gaston.ovh` |

Ne pas confondre avec la variable Terraform `domain` (segment fonctionnel de la stack — voir [`domaines-stack.md`](domaines-stack.md)).

## Règles

- FQDN par défaut : `<stack_name>.<homelab_domain>` (ex. `grafana.jeedom-gaston.ovh`).
- Le FQDN est écrit **en clair** dans le Terraform, jamais via `${SNI}`.
- Toute autre mention du domaine dans le dépôt doit renvoyer à ce fichier plutôt que redéfinir la valeur.
