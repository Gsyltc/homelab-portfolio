---
id: vault-secret-exists
kind: deterministic
command: "non-exécutable (advisory documentaire — existence seule, jamais la valeur)"
default_severity: advisory
description: "Vérifie l'existence (jamais la valeur) des secrets Vault référencés par le livrable, via homelab-vault-access en lecture de présence."
category: security
fire_on: gate
matches: "{**/*.yml,**/*.yaml,**/*.tf,**/*.tfvars}"
origine: ALI-204
---

# Sensor `vault-secret-exists` — existence des secrets Vault référencés *(optionnel, sécurité)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : pour chaque **référence de secret Vault** présente dans le livrable, vérifie que le secret **existe** dans Vault. **Il ne lit, ne recopie et n'affiche JAMAIS la valeur du secret** — uniquement sa **présence** (chemin résolu ou non). **Advisory** (`default_severity: advisory`). Optionnel : n'est actif que si l'humain autorise cette vérification d'existence (question d'arbitrage de l'ADR).

## Contrat de vérification (`checks`)

```yaml
checks:
  references_vault:
    detection: "chemins de secrets Vault référencés (ex. vault:kv/<stack>/<clé>, *_FILE monté depuis Vault)"
    existence_seule: true            # présence du chemin, PAS la valeur
  interdiction_absolue:
    lecture_valeur: false            # ne JAMAIS récupérer / logger / transmettre la valeur
    portee: "métadonnée d'existence uniquement (skill homelab-vault-access en mode présence)"
```

> **Invariant de sécurité.** Ce sensor s'appuie sur `homelab-vault-access` **en lecture de présence uniquement**. Aucune valeur de secret n'est jamais récupérée, affichée, loggée, copiée ni transmise dans un commentaire, un livrable ou une notification (garde-fou « secrets » du chargement optimisé pour le contexte).

## Sortie (piste d'audit)

Verdicts : `✅` tous présents · `⚠️` référence manquante · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor vault-secret-exists — <fichier>   (source : homelab/sensors/sensors/vault-secret-exists.md @ <commit>)
- verdict : ✅ secrets référencés présents | ⚠️ référence(s) sans secret Vault : <chemin, jamais la valeur> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory et **existence seule** : signale un chemin de secret référencé mais absent, **sans jamais lire la valeur**, ne bloque pas. **Ne remplace pas** la validation humaine ni le contrôle sécurité (SG-3). **Parsing statique + lecture de présence uniquement** (SG-4) : environnement sans privilège d'exfiltration, jamais de récupération de valeur. Activation soumise à l'autorisation humaine explicite tracée sur l'issue.
