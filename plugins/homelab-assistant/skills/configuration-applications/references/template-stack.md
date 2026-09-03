# Template de configuration d'une stack

Fichier de référence de la skill `configuration-applications`. **Le template ci-dessous est le format de sortie officiel de toute configuration de stack** : il alimente les playbooks Terraform (`cloudflare`, `swarm`, `updatime_kuma`, configuration Authentik). Toute création ou modification d'un fichier de configuration respecte strictement ce template : toutes les variables des blocs Général, Cloudflare et Kuma sont présentes ; les sections d'authentification suivent la règle des blocs non vides ci-dessous.

## Règle des blocs d'authentification (blocs non vides)

Le fichier de sortie ne contient que des blocs d'authentification réellement utilisés par la stack :

- Si aucun service n'utilise un mode d'authentification, ses propriétés ne sont pas écrites du tout : jamais de tableau vide ni de scalaire orphelin pour un mode non utilisé.
- La section « Authentik - configuration commune » (`main_group`, `publisher`) accompagne toute utilisation de l'un des trois modes ; si aucun service n'utilise Authentik, aucune section Authentik n'apparaît dans le fichier.
- Le template ci-dessous documente l'intégralité des variables possibles à titre de référence ; il ne doit pas être recopié tel quel.

## Template

```hcl
name                    = "nom de la stack"
domain                  = "domaine de la stack"
secrets                 = false        # true si la stack docker compose contient des secrets, sinon false
description             = [ "description des services de la stack" ]   # tableau contenant les descriptions de tous les services de la stack
service_url             = [ "url des services de la stack" ]           # tableau contenant les urls de tous les services de la stack
icons                   = "icone de la stack"    # icone representant la stack ; disponible sur https://github.com/homarr-labs/dashboard-icons

## Cloudflare
cloudflare_dns_nb       = 1            # nombre de CNAME a creer dans Cloudflare

## Kuma
kuma_http_name          = ["nom des services"]   # tableau contenant les noms de tous les services de la stack devant etre monitores par Uptime Kuma
kuma_interval           = [ 30 ]       # tableau contenant les intervalles du healthcheck Uptime Kuma
kuma_max_retries        = [ 1 ]        # tableau contenant le nombre maximum de tentatives du healthcheck Uptime Kuma
kuma_retry_interval     = [ 20 ]       # tableau contenant l'intervalle entre 2 tentatives en cas d'echec du healthcheck Uptime Kuma
kuma_timeout            = [ 8 ]        # tableau contenant les timeouts du healthcheck Uptime Kuma
kuma_resend_interval    = [ 30 ]       # tableau contenant le nombre de tentatives avant une nouvelle notification en cas d'echec du healthcheck Uptime Kuma
kuma_level              = "FATAL"      # criticite du healthcheck Uptime Kuma
kuma_delai              = "1m"         # optionnel : delai d'attente apres deploiement avant creation des moniteurs Uptime Kuma ; defaut playbook "1m", ne renseigner que si la stack requiert une autre valeur

## Authentik - configuration commune   <-- section incluse uniquement si au moins un service utilise Authentik
main_group              = "Canada"     # groupe de securite Authentik
publisher               = ["Publisher de l'application"]   # tableau indiquant, pour chaque application OAuth/SAML, le nom de la societe qui a publie le logiciel

## Authentik - OAuth   <-- section incluse uniquement si au moins un service utilise OAuth
oauth                   = ["nom des services"]   # tableau contenant les services de la stack necessitant une authentification OAuth
allowed_redirect_uris   = [
    [
        {
            matching_mode   = "strict",
            url             = "uri de redirection Oauth",
        }
    ]
]
oauth_email_verified    = true
oauth_additionnal_mapping = "Groupes de securite additionnels Authentik"

## Authentik - SAML   <-- section incluse uniquement si au moins un service utilise SAML
saml                    = ["nom des services"]   # tableau contenant les services de la stack necessitant une authentification SAML
saml_description        = [ "Controlleur Reseaux Omada" ]   # tableau contenant les descriptions des services necessitant une authentification SAML
acs_url                 = ["url de configuration SAML"]

## Authentik - ForwardAuth   <-- section incluse uniquement si au moins un service utilise ForwardAuth
forwardauth             = ["nom des services"]   # tableau contenant les services de la stack necessitant une authentification ForwardAuth
skip_path_regex         = [ "/api(/.*)?$" ]      # tableau contenant les exceptions pour les services necessitant une authentification ForwardAuth
```

## Documentation des variables

Types utilisés : scalaire (`string`, `bool`, `number`) ou tableau (`string[]`, `number[]`). « Une entrée par service » signifie que la longueur du tableau suit le nombre de services concernés.

### Bloc Général

| Variable | Type | Rôle | Exemple |
|---|---|---|---|
| `name` | `string` (scalaire) | Nom de la stack ; identifiant repris dans les playbooks Terraform. | `"portainer"` |
| `domain` | `string` (scalaire) | Domaine fonctionnel de la stack (segment d'URL), déduit de l'application principale. Valeurs autorisées : voir [references/domaines-stack.md](references/domaines-stack.md). | `"administration"` |
| `secrets` | `bool` (scalaire) | `true` si le docker compose de la stack contient des secrets, sinon `false`. Ne jamais écrire la valeur d'un secret dans ce fichier. | `false` |
| `description` | `string[]` (tableau) | Descriptions de tous les services de la stack ; une entrée par service. | `[ "Interface web Portainer" ]` |
| `service_url` | `string[]` (tableau) | URLs de tous les services de la stack ; une entrée par service. | `[ "https://portainer.mondomaine.tld" ]` |
| `icons` | `string` (scalaire) | Icône représentant la stack, choisie parmi https://github.com/homarr-labs/dashboard-icons. | `"portainer"` |

### Cloudflare

| Variable | Type | Rôle | Exemple |
|---|---|---|---|
| `cloudflare_dns_nb` | `number` (scalaire) | Nombre de CNAME à créer dans Cloudflare pour la stack (= nombre de services exposés, déduit des labels Traefik). | `1` |

### Uptime Kuma

Les tableaux `kuma_interval`, `kuma_max_retries`, `kuma_retry_interval`, `kuma_timeout` et `kuma_resend_interval` ont une entrée par service monitoré (même ordre que `kuma_http_name`). Leurs valeurs ne sont pas choisies librement : elles découlent du niveau `kuma_level` défini dans [references/criticites-kuma.md](references/criticites-kuma.md).

| Variable | Type | Rôle | Exemple |
|---|---|---|---|
| `kuma_http_name` | `string[]` (tableau) | Noms des services de la stack devant être monitorés par Uptime Kuma. | `["portainer"]` |
| `kuma_interval` | `number[]` (tableau) | Intervalles du healthcheck Uptime Kuma. | `[ 30 ]` |
| `kuma_max_retries` | `number[]` (tableau) | Nombre maximum de tentatives du healthcheck avant passage en échec. | `[ 1 ]` |
| `kuma_retry_interval` | `number[]` (tableau) | Intervalle entre 2 tentatives en cas d'échec du healthcheck. | `[ 20 ]` |
| `kuma_timeout` | `number[]` (tableau) | Timeouts du healthcheck. | `[ 8 ]` |
| `kuma_resend_interval` | `number[]` (tableau) | Nombre de tentatives avant qu'une nouvelle notification soit renvoyée en cas d'échec du healthcheck. | `[ 30 ]` |
| `kuma_level` | `string` (scalaire) | Criticité du healthcheck Uptime Kuma : `FATAL`, `ERROR`, `WARN` ou `INFO` (choix validé avec l'humain en cas de doute). Pilote les valeurs des tableaux `kuma_*`. | `"FATAL"` |
| `kuma_delai` | `string` (scalaire, optionnel) | Délai d'attente après le déploiement de la stack avant la création des moniteurs Uptime Kuma (`time_sleep` du playbook swarm). Défaut du playbook : `"1m"` ; à renseigner uniquement si la stack nécessite une valeur différente (ex. `"2m"` pour fireflyiii). Ne pas l'écrire si le défaut suffit. | `"2m"` |

### Authentik — configuration commune

Section écrite uniquement si au moins un service de la stack utilise l'un des trois modes Authentik.

| Variable | Type | Rôle | Exemple |
|---|---|---|---|
| `main_group` | `string` (scalaire) | Groupe de sécurité Authentik principal associé à la stack. | `"Canada"` |
| `publisher` | `string[]` (tableau) | Nom de la société qui a publié le logiciel ; **une entrée par application Authentik créée dans les modes OAuth et SAML** — le playbook ne consomme `publisher` que dans ces deux boucles (`meta_publisher`). Sans application OAuth/SAML, la variable reste sans effet : conserver une entrée par application concernée uniquement. | `["Portainer.io"]` |

### Authentik — mode OAuth

Section écrite uniquement si au moins un service de la stack utilise OAuth.

| Variable | Type | Rôle | Exemple |
|---|---|---|---|
| `oauth` | `string[]` (tableau) | Noms des services de la stack nécessitant une authentification OAuth. | `["portainer"]` |
| `allowed_redirect_uris` | tableau de tableaux d'objets | Pour chaque service OAuth, liste des URIs de redirection autorisées. Chaque entrée externe correspond à un service de `oauth` (même ordre) ; chaque objet porte `matching_mode` (mode de comparaison de l'URI, ex. `strict`) et `url` (URI de redirection OAuth). | voir template |
| `oauth_email_verified` | `bool` (scalaire) | Exige que l'e-mail de l'utilisateur soit vérifié par Authentik. | `true` |
| `oauth_additionnal_mapping` | `string` (scalaire) | Groupes de sécurité Authentik additionnels attribués via le mapping. Orthographe historique « additionnal » à conserver telle quelle (compatibilité avec le code existant). | `"Groupes de sécurité additionnels Authentik"` |

### Authentik — mode SAML

Section écrite uniquement si au moins un service de la stack utilise SAML.

| Variable | Type | Rôle | Exemple |
|---|---|---|---|
| `saml` | `string[]` (tableau) | Noms des services de la stack nécessitant une authentification SAML. | `["omada-controller"]` |
| `saml_description` | `string[]` (tableau) | Descriptions des services nécessitant une authentification SAML ; une entrée par service de `saml` (même ordre). | `[ "Contrôleur Réseaux Omada" ]` |
| `acs_url` | `string[]` (tableau) | URL de configuration SAML (Assertion Consumer Service) de chaque service SAML ; même ordre que `saml`. | `["https://omada.mondomaine.tld:8043/saml"]` |

### Authentik — mode ForwardAuth

Section écrite uniquement si au moins un service de la stack utilise ForwardAuth.

| Variable | Type | Rôle | Exemple |
|---|---|---|---|
| `forwardauth` | `string[]` (tableau) | Noms des services de la stack nécessitant une authentification ForwardAuth. | `["portainer"]` |
| `skip_path_regex` | `string[]` (tableau) | Exceptions (chemins exclus de l'authentification, expressions régulières) pour les services nécessitant une authentification ForwardAuth. | `[ "/api(/.*)?$" ]` |
