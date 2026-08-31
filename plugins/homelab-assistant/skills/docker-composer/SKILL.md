---
name: docker-composer
description: "Skill for composing and managing Docker Compose configurations"
user-invocable: true
allowed-tools: Bash(*)
---

# Skill: Docker Composer

Gestion et composition de fichiers Docker Compose pour les stacks homelab.

## Fonctionnalités

### Lecture et validation
- Parser des fichiers `docker-compose.yml` / `docker-compose.yaml`
- Valider la syntaxe YAML et la structure Docker Compose
- Vérifier les services, networks, volumes, secrets, configs

### Composition et génération
- Fusionner plusieurs fichiers compose (override, extension)
- Générer des fichiers compose à partir de templates
- Appliquer des profils (dev, prod, staging)

### Opérations courantes
- Lister les services définis
- Extraire la configuration d'un service spécifique
- Résoudre les variables d'environnement (.env)
- Vérifier les dépendances entre services (depends_on)

## Usage typique

### Valider un docker-compose
```bash
docker compose -f docker-compose.yml config
```

### Lister les services
```bash
docker compose -f docker-compose.yml config --services
```

### Afficher la config résolue (avec variables .env)
```bash
docker compose -f docker-compose.yml --env-file .env config
```

### Appliquer un profil
```bash
docker compose -f docker-compose.yml --profile monitoring config
```

## Structure attendue d'un projet homelab

```
homelab/
├── docker-compose.yml          # Base configuration
├── docker-compose.override.yml # Local overrides (gitignored)
├── .env                        # Variables d'environnement
├── .env.example                # Template des variables
└── stacks/
    ├── monitoring/
    │   ├── docker-compose.yml
    │   └── .env
    ├── media/
    │   ├── docker-compose.yml
    │   └── .env
    └── ...
```

## Bonnes pratiques

1. **Toujours utiliser un fichier .env** pour les secrets et config spécifique à l'environnement
2. **Séparer les stacks** par domaine fonctionnel (monitoring, media, networking, etc.)
3. **Utiliser des networks externes** pour la communication inter-stacks
4. **Définir les volumes nommés** explicitement pour la persistance
5. **Limiter les privilèges** : `security_opt`, `read_only`, `user`, `cap_drop`

## Exemple de composition multi-fichiers

```bash
# Composition de base + override local + profil spécifique
docker compose \
  -f docker-compose.yml \
  -f docker-compose.override.yml \
  -f stacks/monitoring/docker-compose.yml \
  --profile monitoring \
  config
```

## Variables d'environnement utiles

- `COMPOSE_PROJECT_NAME` : Nom du projet (prefixe conteneurs/volumes/networks)
- `COMPOSE_FILE` : Liste de fichiers compose séparés par `:`
- `COMPOSE_PROFILES` : Profils actifs séparés par `,`
- `DOCKER_HOST` : Endpoint Docker daemon (ex: `unix:///var/run/docker.sock`)