---
name: configuration-applications
description: "Configuration des applications (stacks) du Homelab pour André - Spécialiste Terraform : processus à suivre, déduction automatique des 4 informations obligatoires d'une stack depuis le docker compose (type d'authentification via middlewares Traefik, cloudflare_dns_nb, domaine, criticité Kuma), et template obligatoire du fichier de configuration (Général, Cloudflare, Uptime Kuma, Authentik OAuth/ForwardAuth). Le template est le format de sortie officiel d'une configuration de stack."
---
Skill « Configuration des applications » pour André (Spécialiste Terraform). Elle définit le processus à suivre et le format de sortie obligatoire du fichier de configuration d'une stack du Homelab.

## Objectif

Permettre à André de configurer les services d'une stack Docker Swarm côté Terraform :

- savoir quelles informations réunir avant d'écrire une configuration, et où les trouver ;
- produire un fichier de configuration au format standard du Homelab : **le template défini dans [references/template-stack.md](references/template-stack.md) est le format de sortie officiel de toute configuration de stack**. Ce fichier alimente ensuite les playbooks Terraform (`cloudflare`, `swarm`, `updatime_kuma`, configuration Authentik).
- **le template défini dans [references/template-stack.md](references/template-stack.md) est la seule source de vérité du format des fichiers pour la création, la modification et la vérification d'un fichier de configuration**

## Quand utiliser cette skill

- Création d'une nouvelle stack : générer son fichier de configuration complet.
- Modification d'une stack existante : mettre à jour les variables concernées en conservant la structure du template ([references/template-stack.md](references/template-stack.md)).
- Relecture ou validation d'un fichier de configuration produit par l'humain ou par un autre agent.

## Processus à suivre

1. Lire la demande sur l'issue et le docker compose de l'application concernée.
2. Déterminer les informations obligatoires (règles de déduction détaillées : voir la section « Déduction des informations obligatoires » ci-dessous) :
   - **Type d'authentification** (aucune / ForwardAuth / OAuth) : déduit des middlewares Traefik configurés pour le service dans le docker compose ; règles détaillées dans [references/authentification.md](references/authentification.md).
   - **Nombre de services DNS à exposer** (= `cloudflare_dns_nb`) : déduit des labels Traefik configurés pour les services dans le docker compose.
   - **Domaine de la stack** : déduit de l'application principale ; valeur à choisir dans le fichier de référence [references/domaines-stack.md](references/domaines-stack.md). En cas d'ambiguïté, demander à l'humain.
   - **Criticité de la stack** (`FATAL` / `ERROR` / `WARN` / `INFO`) : pilote directement les valeurs `kuma_*` via le fichier de référence [references/criticites-kuma.md](references/criticites-kuma.md). En cas de doute, demander systématiquement à l'humain.
3. Rassembler les autres valeurs (nom, descriptions, URLs, icône, éditeur, groupe Authentik, URIs OAuth…) depuis le docker compose et la demande ; toute donnée manquante se demande à l'humain — ne jamais inventer une valeur.
4. Rédiger le fichier de configuration en respectant strictement le template défini dans [references/template-stack.md](references/template-stack.md) : toutes les variables des blocs Général, Cloudflare et Kuma sont présentes ; les sections d'authentification (commune, OAuth, ForwardAuth) ne sont écrites que si au moins un service utilise le mode concerné — jamais de bloc vide pour un mode non utilisé.
5. Relire : une entrée de tableau par service concerné (longueurs cohérentes), domaine conforme au fichier des domaines, valeurs `kuma_*` conformes au niveau de criticité choisi, aucune section d'authentification vide (blocs non utilisés omis), aucun secret en clair.
6. Soumettre le fichier sur l'issue pour validation (Stuart puis validation humaine explicite) avant toute application Terraform.

## Déduction des informations obligatoires (analyse du docker compose)

Pour chacune des 4 informations obligatoires : règle de décision, indices concrets à chercher dans le docker compose, exemples et cas limites — soit ci-dessous, soit dans le fichier de référence dédié.

**Règle transversale** : en cas de doute ou d'ambiguïté, poser la question à l'humain — ne jamais inventer une valeur ni choisir arbitrairement.

### 1. Type d'authentification

Déduit des middlewares Traefik configurés pour le service. La table de décision entre les trois cas (« Pas d'authentification » / ForwardAuth / OAuth), avec la correspondance officielle des middlewares nommés du Homelab, les indices Traefik concrets, les exemples et les cas limites sont détaillés dans le fichier de référence [references/authentification.md](references/authentification.md).

### 2. Nombre de services DNS à exposer (`cloudflare_dns_nb`)

Règle de décision : compter les **noms d'hôte publics distincts** exposés par les règles Traefik de la stack (`traefik.http.routers.<r>.rule=Host(…)`). Chaque nom d'hôte public = 1 CNAME à créer dans Cloudflare.

Exemples :

- Une seule interface web : `Host(`portainer.mondomaine.tld`)` → `cloudflare_dns_nb = 1`.
- Application plus API séparées : `Host(`app.mondomaine.tld`)` + `Host(`api.mondomaine.tld`)` → `cloudflare_dns_nb = 2`.

Cas limites :

- Plusieurs routeurs sur le même hôte (ex. routeur supplémentaire `PathPrefix(`/api`)` sur le même domaine) : compter les hôtes, pas les routeurs → toujours 1 CNAME.
- Service purement interne (pas de règle `Host` publique, exposition réseau interne uniquement) : non compté.
- Service exposé publiquement sans authentification centralisée (middleware `securedNoAuth`, `securedNoSSO`, `securedLocalAuth`) : validation obligatoire de l'humain avant de compter son CNAME — voir [references/authentification.md](references/authentification.md).
- Règle wildcard ou `HostRegexp` rendant le nombre d'hôtes incertain → demander à l'humain.

### 3. Domaine de la stack

Règle de décision : identifier l'application principale de la stack (le service qui justifie l'existence de la stack), déterminer sa fonction, puis choisir `domain` **strictement** dans le fichier de référence [references/domaines-stack.md](references/domaines-stack.md).

Exemples : Portainer → `administration` ; Grafana → `monitoring` ; Pi-hole → `networking` ; Vaultwarden → `securite`.

Cas limites :

- Stack couvrant plusieurs périmètres : retenir le domaine correspondant au service principal ; si deux domaines restent également plausibles après analyse → demander à l'humain.
- Fonction absente du fichier de référence (aucun domaine ne convient) : ne jamais créer un nouveau domaine ni une variante orthographique → demander à l'humain.

### 4. Criticité de la stack (`kuma_level`)

Règle de décision : proposer un niveau parmi `FATAL` / `ERROR` / `WARN` / `INFO` en s'appuyant sur le guide de choix du fichier de référence [references/criticites-kuma.md](references/criticites-kuma.md), puis faire valider le niveau par l'humain dès qu'un doute subsiste.

Repères de proposition : `FATAL` pour ce qui bloque le Homelab (authentification, reverse proxy, DNS) ; `ERROR` pour un service important dont la panne perturbe fortement l'usage ; `WARN` pour un service utile non bloquant ; `INFO` pour un service secondaire ou expérimental.

Cas limites :

- Doute sur l'impact réel d'une coupure (usage peu documenté, service récent) → demander systématiquement à l'humain, ne rien figer.
- Les tableaux `kuma_*` ne sont remplis qu'une fois le niveau confirmé : leurs valeurs découlent exclusivement de la ligne du niveau choisi dans le fichier de référence.

## Fichiers de référence

| Fichier | Contenu |
|---|---|
| [references/template-stack.md](references/template-stack.md) | Template de configuration d'une stack (format de sortie officiel) + documentation de chaque variable (type, tableau vs scalaire, rôle, exemple). Inclut la règle des blocs d'authentification non vides. |
| [references/authentification.md](references/authentification.md) | Type d'authentification : table de décision (aucune / ForwardAuth / OAuth) depuis les middlewares Traefik, avec la colonne de correspondance des middlewares nommés du Homelab, exemples, cas limites, correspondance avec les sections du template. |
| [references/domaines-stack.md](references/domaines-stack.md) | Domaines de stack autorisés pour `domain`. |
| [references/criticites-kuma.md](references/criticites-kuma.md) | Criticités Uptime Kuma (`FATAL`/`ERROR`/`WARN`/`INFO`) et paramètres `kuma_*` exacts associés. |

## Règles transverses

- Les deux modes d'authentification Authentik (OAuth, ForwardAuth) sont des sections distinctes du template : un service n'apparaît que dans la section correspondant à son mode d'authentification déterminé lors de l'analyse du docker compose (voir [references/authentification.md](references/authentification.md)). Les sections d'un mode non utilisé par aucun service sont omises du fichier de sortie (blocs non vides uniquement). SAML et LDAP ne sont **pas** supportés actuellement (retirés — voir ADR-0020) : une stack les requérant est remontée à l'humain.
- Conserver les noms de variables exactement tels qu'ils figurent dans le template (y compris `oauth_additionnal_mapping`) : ils correspondent aux variables attendues par les playbooks Terraform existants.
- Aucune donnée sensible (token, mot de passe, secret Vault, URL interne sensible) dans le fichier de configuration ni dans les commentaires : `secrets = true` signale leur existence, jamais leur contenu.
- Toute information non déductible avec certitude se demande à l'humain ; on ne devine jamais une valeur.
