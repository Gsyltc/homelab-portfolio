---
id: traefik-coherence
kind: deterministic
command: "non-exécutable (advisory documentaire — référence le check traefik-manager-read)"
default_severity: advisory
description: "Vérifie la cohérence Traefik du compose livré (labels, entrypoints, réseau) en s'appuyant sur le check traefik-manager-read existant."
category: traefik
fire_on: gate
matches: "{**/*.yml,**/*.yaml}"
origine: ALI-204
---

# Sensor `traefik-coherence` — cohérence Traefik *(complémentaire)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie la **cohérence Traefik** du docker-compose livré (labels de routage, entrypoints, appartenance au réseau Traefik). Ce sensor **ne réimplémente pas** l'analyse Traefik : il **référence le check `traefik-manager-read` existant** (skill du QA Docker, §2.2) et se limite à consigner un signal factuel advisory. **Advisory** (`default_severity: advisory`).

## Contrat de vérification (`checks`)

```yaml
checks:
  reference_check_existant:
    check: traefik-manager-read              # autorité : skill du QA Docker (§2.2)
    role_du_sensor: "consigne le verdict factuel, sans réanalyser"
  coherence_de_surface:                      # contrôle statique de surface uniquement
    reseau_traefik_present: "le service exposé rejoint ${traefik_network} (défaut traefik_frontend)"
    labels_routage_presents: "traefik.enable + router rule + entrypoint cohérents"
    aucun_config_errors: "aucune configErrors rapportée par traefik-manager-read"
```

## Sortie (piste d'audit)

Verdicts : `✅` cohérent · `⚠️` incohérence · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor traefik-coherence — <fichier>   (source : homelab/sensors/sensors/traefik-coherence.md @ <commit>)
- verdict : ✅ cohérent (traefik-manager-read) | ⚠️ incohérence : <labels / entrypoint / réseau / configErrors> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : consigne le signal Traefik, ne bloque pas. **L'autorité technique reste `traefik-manager-read`** exécuté par le QA Docker (§2.2) ; ce sensor ne fait que tracer le verdict et un contrôle de surface, il **ne remplace pas** la vérification du QA Docker ni la validation humaine (SG-3). **Parsing statique / lecture seule** (SG-4) : jamais d'écriture sur la configuration Traefik.
