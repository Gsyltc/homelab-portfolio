---
name: traefik-manager-read
description: "Skill permettant d'accéder au information de Traefik Manager"
user-invocable: false
allowed-tools: Bash(multica *)
---

# Skill: Traefik Manager — Lecture seule

Accès en lecture seule à l'API Traefik Manager (`https://${TRAEFIK_MANAGER_URL}`).
Aucune modification n'est acceptée. Toute opération d'écriture est interdite sans accord explicite de l'humain.

## Authentification

Clé API via la variable d'environnement `TRAEFIK_MANAGER_API_KEY`.

```
curl -H "X-Api-Key: $TRAEFIK_MANAGER_API_KEY" https://${TRAEFIK_MANAGER_URL}/api/...
```

## Endpoints de lecture

### Vue d'ensemble Traefik

```bash
GET /api/traefik/overview
# Retourne les compteurs de routers, services, middlewares + flags features

GET /api/traefik/version
# Version et nom de code Traefik

GET /api/traefik/ping
# Latence de l'API Traefik (ok, latency_ms)
```

### Services déployés (via Traefik)

```bash
GET /api/traefik/services
# Tous les services HTTP, TCP, UDP connus de Traefik
# Response: { "http": [...], "tcp": [...], "udp": [...], "reachable": true }
# reachable=false → Traefik injoignable
```

### Middlewares configurés (via Traefik)

```bash
GET /api/traefik/middlewares
# Tous les middlewares HTTP et TCP
# Response: { "http": [...], "tcp": [...] }
```

### Routes (Traefik Manager — config files gérées)

```bash
GET /api/routes
# Routes + middlewares des config files gérées par Traefik Manager
# Response: { "apps": [...], "middlewares": [...], "configErrors": [...], "services": {...} }

GET /api/routes/all
# Idem mais inclut les routes de TOUS les providers (Docker, K8s, etc.) + @internal
# Response: même forme, sans configErrors

GET /api/routes/{route_id}
# Détail d'une route spécifique

GET /api/routes/{route_id}/raw
# YAML brut de la route et son service
```

### Routes d'un agent (multi-server)

```bash
GET /api/agents/{id}/routes
# Routes et middlewares d'un agent spécifique
```

### Entrypoints

```bash
GET /api/traefik/entrypoints
# [{ "name": "websecure", "address": ":443" }]
```

### Certificats TLS

```bash
GET /api/traefik/certs
# Certificats ACME + file-provider avec expiry
```

### Plugins

```bash
GET /api/traefik/plugins
# Plugins définis dans la config statique
```

## Endpoints de lecture (config Traefik Manager)

```bash
GET /api/configs
# Liste des fichiers de config dynamic chargés

GET /api/tls-options
# Profils TLS configurés

GET /api/settings
# Paramètres TM (secrets masqués)
```

## Format de réponse

Tous les endpoints retournent du JSON.
- Succès : `{ "ok": true }` ou `{ "success": true }`
- Erreur : `{ "ok": false, "message": "..." }` ou `{ "error": "..."}`
- 401 = non authentifié / session expirée
- 502 = Traefik injoignable

## Cas d'usage typiques

### Vérifier la cohérence d'une stack Docker Swarm

1. `GET /api/traefik/services` → liste des services déployés dans Traefik
2. `GET /api/routes` ou `GET /api/routes/all` → routes pointant vers ces services
3. `GET /api/traefik/middlewares` → middlewares effectivement appliqués
4. Comparer avec le docker-compose : chaque service référencé dans une route doit exister, chaque middleware utilisé par une route doit être défini

### Vérifier qu'un service est bien routé

1. `GET /api/traefik/routers` → chercher le router par nom
2. Vérifier `service_name`, `middlewares[]`, `entryPoints[]`, `rule`
3. `GET /api/traefik/services` → vérifier que le service cible existe et a des backends sains
