---
id: swarm-deploy-section
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
description: "Vérifie la présence d'une section deploy compatible Docker Swarm sur chaque service du compose livré."
category: compose-shape
fire_on: gate
matches: "{**/*.yml,**/*.yaml}"
origine: ALI-204
---

# Sensor `swarm-deploy-section` — section `deploy` Swarm *(prioritaire)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie que chaque service du docker-compose livré porte une section **`deploy`** compatible **Docker Swarm** (le Homelab déploie en Swarm — voir label `Docker Swarm`). **Advisory** (`default_severity: advisory`). Recoupe le contrôle « compatibilité Swarm » du QA Docker (§2.2) et le niveau `standard` de l'axe de vérification.

## Contrat de vérification (`checks`)

```yaml
checks:
  services:
    section_deploy_presente: true          # chaque service porte une clé deploy:
    placement_recommande: "deploy.placement.constraints présent (advisory)"
    directives_non_swarm_signalees:         # incompatibles / ignorées en mode Swarm (signalées, non bloquantes)
      - restart          # remplacé par deploy.restart_policy en Swarm
      - depends_on       # non honoré par Swarm au démarrage
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor swarm-deploy-section — <fichier>   (source : homelab/sensors/sensors/swarm-deploy-section.md @ <commit>)
- verdict : ✅ section deploy présente (tous services) | ⚠️ service(s) sans deploy / directive non-Swarm : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : signale l'absence de `deploy` ou une directive non-Swarm, ne bloque pas. **Ne remplace pas** l'analyse de compatibilité Swarm du QA Docker (§2.2), qui reste l'autorité technique. **Parsing statique uniquement** (SG-4).
