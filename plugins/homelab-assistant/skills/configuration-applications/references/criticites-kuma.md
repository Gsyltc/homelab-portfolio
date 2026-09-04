# Criticités Uptime Kuma

Fichier de référence de la skill `configuration-applications`. Il définit les 4 niveaux de criticité d'une stack et les paramètres Uptime Kuma exacts associés à chacun.

## Utilisation

- Le niveau est choisi pour la variable `kuma_level` (`FATAL`, `ERROR`, `WARN` ou `INFO`) : c'est la criticité du healthcheck Uptime Kuma de la stack.
- **La criticité pilote directement les valeurs des tableaux `kuma_*` du template** : une fois le niveau choisi, chaque tableau prend exactement la valeur du niveau ci-dessous (répétée pour chaque service monitoré, même ordre que `kuma_http_name`). Aucune autre valeur n'est autorisée.
- En cas de doute sur le niveau, **demander systématiquement à l'humain** — ne jamais le deviner.
- À la relecture : vérifier que chaque valeur `kuma_interval`, `kuma_max_retries`, `kuma_retry_interval`, `kuma_timeout` et `kuma_resend_interval` correspond bien à la ligne du niveau choisi.

## Niveaux de criticité et paramètres Kuma exacts

| Criticité | interval | max_retries | retry_interval | timeout | resend_interval |
|---|---|---|---|---|---|
| `FATAL` | 20 | 1 | 20 | 8 | 30 |
| `ERROR` | 30 | 1 | 20 | 10 | 30 |
| `WARN` | 60 | 3 | 30 | 15 | 30 |
| `INFO` | 120 | 5 | 60 | 20 | 30 |

Correspondance avec les variables du template :

| Niveau | Variables du template |
|---|---|
| `interval` | `kuma_interval` |
| `max_retries` | `kuma_max_retries` |
| `retry_interval` | `kuma_retry_interval` |
| `timeout` | `kuma_timeout` |
| `resend_interval` | `kuma_resend_interval` |

## Guide de choix

| Niveau | Quand le choisir |
|---|---|
| `FATAL` | Service critique dont l'interruption bloque le Homelab ou les accès (authentification, reverse proxy, DNS). |
| `ERROR` | Service important dont l'indisponibilité perturbe fortement l'usage courant. |
| `WARN` | Service utile dont l'indisponibilité est gênante sans être bloquante. |
| `INFO` | Service secondaire ou expérimental, surveillé à titre informatif. |

Le tableau ci-dessus est un guide : le niveau reste un choix validé avec l'humain en cas de doute.

## Exemple

Stack `portainer`, criticité `FATAL`, deux services monitorés :

```hcl
kuma_http_name       = ["portainer", "portainer-agent"]
kuma_interval        = [ 20, 20 ]
kuma_max_retries     = [ 1, 1 ]
kuma_retry_interval  = [ 20, 20 ]
kuma_timeout         = [ 8, 8 ]
kuma_resend_interval = [ 30, 30 ]
kuma_level           = "FATAL"
```
