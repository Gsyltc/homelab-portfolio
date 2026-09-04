---
id: plaintext-secret
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
severity_overrides:
  # décision humaine (ALI-204, arbitrage 2 « Oui ») + contrôle sécurité QA Docker : bloquant sur les scopes sécuritaires
  - scopes: [security-patch, new-stack]
    severity: blocking
description: "Détecte des motifs de secret en clair (mot de passe / token / clé API) dans les livrables compose et Terraform."
category: security
fire_on: write
matches: "{**/*.yml,**/*.yaml,**/*.tf,**/*.tfvars}"
origine: ALI-204
---

# Sensor `plaintext-secret` — détection de secret en clair *(prioritaire, sécurité)*

Check déterministe déclenché **à l'écriture** (`fire_on: write`) : détecte des **motifs de secret en clair** (mot de passe, token, clé API) dans un livrable compose ou Terraform. **Advisory par défaut**, **bloquant sur `security-patch` / `new-stack`** (décision humaine ALI-204, arbitrage 2 « Oui » + contrôle sécurité du QA Docker, cf. `severity_overrides` ; SG-1). Recoupe le garde-fou absolu « aucun secret en clair » du workflow (§ langue, format et sécurité) et le contrôle macro « un secret en clair saute-t-il aux yeux ? » du Tech Lead (§2.6).

## Contrat de vérification (`checks`)

```yaml
checks:
  motifs_interdits:
    # affectation directe d'un secret à une valeur littérale non-référencée
    - "(?i)(password|passwd|pwd)\\s*[:=]\\s*['\\\"]?[^\\s'\\\"$]{6,}"
    - "(?i)(token|api[_-]?key|secret|access[_-]?key)\\s*[:=]\\s*['\\\"]?[A-Za-z0-9/_+.-]{12,}"
    - "(?i)(-----BEGIN [A-Z ]*PRIVATE KEY-----)"
  exceptions_tolerees:
    # convention _FILE (secret monté depuis un fichier / Vault, jamais en clair)
    - "*_FILE"
    # référence Vault / variable d'environnement / secret Docker (pas une valeur en clair)
    - "${...}"
    - "vault:*"
    - "/run/secrets/*"
```

> **Ne lit ni ne recopie jamais la valeur détectée** : le signal indique **l'emplacement** (fichier + ligne + clé) et le **type de motif**, jamais le contenu du secret (garde-fou « aucun secret dans les commentaires / notifications »).

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` motif détecté · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor plaintext-secret — <fichier>   (source : homelab/sensors/sensors/plaintext-secret.md @ <commit>)
- verdict : ✅ aucun secret en clair détecté | ⚠️ motif suspect : <fichier:ligne clé + type, jamais la valeur> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory par défaut : signale un motif suspect **sans jamais divulguer la valeur**, ne bloque pas hors scope sécuritaire. **Bloquant sur `security-patch` / `new-stack`** (décision humaine ALI-204 + contrôle sécurité QA Docker) : sur ces scopes, un motif détecté **arrête l'avancée** jusqu'à correction ou levée humaine explicite tracée. Même bloquant, le sensor **ne remplace pas** l'audit de sécurité du QA Docker (niveau `renforcé`) ni la validation humaine (SG-3). **Parsing statique uniquement** (SG-4) : détection par motif, jamais de résolution / lecture de secret Vault.
