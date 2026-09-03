# Authentification d'une stack

Fichier de référence de la skill `configuration-applications`. Il regroupe tous les aspects liés à l'authentification d'une stack : déduction du type d'authentification depuis le docker compose (middlewares Traefik et variables d'environnement), indices concrets, exemples, cas limites, et correspondance avec les sections du template ([references/template-stack.md](references/template-stack.md)).

**Règle transversale** : en cas de doute ou d'ambiguïté, poser la question à l'humain — ne jamais inventer une valeur ni choisir arbitrairement.

## Type d'authentification : règle de décision

Règle de décision : examiner, pour chaque service exposé, ses labels Traefik et ses variables d'environnement / fichiers de configuration dans le docker compose, puis trancher entre les quatre cas.

Indices concrets permettant de trancher :

| Cas | Middleware(s) du Homelab | Indices dans le docker compose |
|---|---|---|
| **Pas d'authentification** | `securedNoAuth`, `securedNoSSO`, `securedLocalAuth` | Aucun middleware d'authentification sur le routeur Traefik du service, et aucune trace SAML / OAuth / ForwardAuth dans les variables d'environnement ou fichiers de config montés. Seuls des labels Traefik « standards » sont présents (`rule`, `entrypoints`, `tls.certresolver`, `service.port`). |
| **ForwardAuth** | `securedWithForwardAuth` | Un middleware `forwardAuth` est appliqué au routeur du service. Deux formes possibles : référence à un middleware Authentik existant (`traefik.http.routers.<r>.middlewares=<app>-outpost@authentik` ou `authentik@file`), ou définition locale (`traefik.http.middlewares.<m>.forwardauth.address=http://…/outpost.goauthentik.io/…`). Souvent accompagné d'un routeur dédié à l'outpost : `traefik.http.routers.<r>-outpost.rule=Path(`/outpost.goauthentik.io/`)`. → renseigner `forwardauth[]` (et `skip_path_regex[]` si nécessaire). |
| **SAML** | — (aucun à ce jour) | Pas de middleware `forwardAuth` ; l'application est elle-même fournisseur de service SAML : variables d'environnement ou fichiers de config contenant `SAML` (`SAML_METADATA_URL`, `SAML_ENTITY_ID`, chemin ACS…), URLs Authentik de la forme `/application/saml/<slug>/…`. → renseigner `saml[]`, `saml_description[]`, `acs_url[]`. |
| **OAuth** | `securedWithOIDC` | Pas de middleware `forwardAuth` ; l'application est cliente OAuth2/OIDC : variables contenant `OAUTH` ou `OIDC` (`OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `OIDC_ISSUER`…), URI de callback de type `/oauth2/callback` ou `/authorization-code/callback`, URLs Authentik de la forme `/application/o/<slug>/authorize` ou `/token`. → renseigner `oauth[]`, `allowed_redirect_uris[][]`. |

La colonne « Middleware(s) du Homelab » donne la correspondance officielle entre les middlewares nommés du provider fichier (`<nom>@file`) et le type d'authentification : c'est l'indice prioritaire dès qu'un middleware de cette liste est référencé sur le routeur du service.

**Pour `securedNoAuth`, `securedNoSSO` et `securedLocalAuth` (pas d'authentification) : validation obligatoire de l'humain pour décider si le DNS du service doit être exposé publiquement, le service n'étant protégé par aucune sécurité centralisée.**

Exemple ForwardAuth :

```yaml
labels:
  - "traefik.http.routers.portainer.rule=Host(`portainer.mondomaine.tld`)"
  - "traefik.http.routers.portainer.middlewares=portainer-outpost@authentik"
```

Exemple OAuth :

```yaml
environment:
  - OAUTH_CLIENT_ID=xxxxxxxx
  - OAUTH_REDIRECT_URI=https://grafana.mondomaine.tld/oauth2/callback
```

Cas limites :

- Service non exposé par Traefik (aucun label Traefik) : il n'a pas d'intégration Authentik → cas « Pas d'authentification », même si l'application possède son propre login interne (un login applicatif natif n'est pas une intégration Authentik et ne remplit aucune section OAuth/SAML/ForwardAuth).
- Middleware référencé mais défini hors du compose (provider fichier ou dynamique) : se baser sur la colonne « Middleware(s) du Homelab » de la table ci-dessus ; si le nom n'y figure pas et que sa nature reste incertaine → demander à l'humain.
- Un même service présentant à la fois un middleware `forwardAuth` ET des variables OAuth/SAML : ambiguïté → demander à l'humain.
- Stack multi-services avec des modes différents : classer chaque service indépendamment ; un service n'apparaît que dans la section du template correspondant à son propre mode.

## Correspondance avec le template

Un service n'apparaît que dans la section du template correspondant à son propre mode. Une section dont le tableau est vide n'est jamais écrite dans le fichier de sortie (blocs non vides uniquement — voir [references/template-stack.md](references/template-stack.md)) :

| Cas | Section / variables du template à remplir |
|---|---|
| **Pas d'authentification** | Aucune section Authentik pour ce service. Si aucun service de la stack n'utilise Authentik : aucune section Authentik du tout (ni commune, ni OAuth/SAML/ForwardAuth). |
| **ForwardAuth** | « Authentik - ForwardAuth » : `forwardauth[]` (+ `skip_path_regex[]` si nécessaire). |
| **SAML** | « Authentik - SAML » : `saml[]`, `saml_description[]`, `acs_url[]`. |
| **OAuth** | « Authentik - OAuth » : `oauth[]`, `allowed_redirect_uris[][]`, plus les scalaires `oauth_email_verified` et `oauth_additionnal_mapping`. |

La section « Authentik - configuration commune » (`main_group`, `publisher[]`) accompagne toute utilisation de l'un des trois modes Authentik.
