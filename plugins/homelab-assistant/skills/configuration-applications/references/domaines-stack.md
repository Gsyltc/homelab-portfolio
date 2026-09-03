# Domaines de stack

Fichier de référence de la skill `configuration-applications`. Il liste les domaines autorisés pour la variable `domain` du fichier de configuration d'une stack, avec leur périmètre.

## Utilisation

- `domain` est un scalaire `string` : le segment d'URL qui qualifie fonctionnellement la stack.
- La valeur est déduite de l'application principale de la stack (analyse du docker compose et de la demande).
- **La valeur doit être choisie strictement dans ce tableau** — aucun autre domaine n'est autorisé, aucune variante orthographique (pas d'accents ni de majuscules).
- En cas d'ambiguïté entre deux domaines, demander à l'humain ; ne jamais inventer une valeur.

## Domaines autorisés

| Domaine | Périmètre |
|---|---|
| `administration` | Logiciels dédiés à l'administration système. |
| `applications` | Autres types de logiciels, applications courantes. |
| `database` | Bases de données, administration de bases de données. |
| `developpement` | Développement d'applications, d'architectures. |
| `domotique` | Domotique, IoT, automatisation. |
| `ia` | Tout logiciel d'IA. |
| `monitoring` | Surveillance de systèmes informatiques. |
| `networking` | Gestion des réseaux informatiques. |
| `securite` | Sécurité : vault, password manager, authentification, analyse cyber. |
| `storage` | Gestion de fichiers, serveurs de fichiers. |

## Exemples de déduction

| Application principale | Domaine retenu | Raison |
|---|---|---|
| Portainer | `administration` | Administration de l'environnement Docker Swarm. |
| Vaultwarden | `securite` | Password manager. |
| Grafana | `monitoring` | Surveillance / visualisation de métriques. |
| Pi-hole | `networking` | Gestion DNS du réseau. |
| Nextcloud | `storage` | Gestion et partage de fichiers. |
