# Liste des réseaux Traefik

## Réseaux ayant un connection avec internet

- traefik_frontend : Ce réseau est utilisée pour les applications communes. C'est le réseaux par défaut.
- traefik_auth : C'est le réseau pour toutes les applications de sécurité et d'authentification
- traefik_admin : Réseau pour toutes les applications d'administration (réseaux, système, technos, etc.)
- traefik_telemetry : Réseau pour toutes les communications télémétriques.

## Réseaux sans connexion internet

Ces réseaux sont utilisé uniquement pour la communication entre les stacks, lorsque nécessaire

- internal_monitoring : Réseau pour toutes les applications de monitoring, alerting, tracing.

## Configuration des middlewares de type d'authentification

Si requis, détermine le type d'authentification grace à ${auth_type}

| ${auth_type} | ${auth_label}               | description                                 |
| ------------ | --------------------------- | ------------------------------------------- |
| none         | securedNoAuth@file          | Pas d'authentification nécessaire           |
| local        | securedLocalAuth@file       | Authentification locale                     |
| oidc         | securedWithOIDC@file        | Authentification avec Authentik OpenID      |
| forwardauth  | securedWithForwardAuth@file | Authentification avec Authentik ForwardAuth |

## Configuration des labels Traefik

```yaml
- traefik.enable=true
- traefik.swarm.network=${nom du reseaux traefik à utiliser}
## Routeur
- traefik.http.routers.${input:stack}-router.rule=Host(`${input:stack}.${SNI}[nom-de-domaine]`)
- traefik.http.routers.${input:stack}-router.entrypoints=https
- traefik.http.routers.${input:stack}-router.middlewares=${auth_label}
- traefik.http.routers.${input:stack}-router.tls=true
- traefik.http.routers.${input:stack}-router.tls.certresolver=gaston-resolver_${ENVIRONMENT}
- traefik.http.routers.${input:stack}-router.service=${input:stack}-service
## Service
- traefik.http.services.${input:stack}-service.loadbalancer.server.port=${port_number}
```
