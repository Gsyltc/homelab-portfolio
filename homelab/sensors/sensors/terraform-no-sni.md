---
id: terraform-no-sni
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
severity_overrides:
  # décision humaine (ALI-204, arbitrage 2 « Oui ») + contrôle sécurité QA Docker : bloquant sur les scopes sécuritaires
  - scopes: [security-patch, new-stack]
    severity: blocking
description: "Vérifie l'absence de la variable ${SNI} dans les fichiers Terraform livrés (domaines/URLs en clair attendus)."
category: security
fire_on: write
matches: "{**/*.tf,**/*.tfvars}"
origine: ALI-204
---

# Sensor `terraform-no-sni` — absence de `${SNI}` en Terraform *(prioritaire, sécurité)*

Check déterministe déclenché **à l'écriture** (`fire_on: write`) d'un fichier Terraform : vérifie l'**absence de la variable `${SNI}`** dans les fichiers `.tf` / `.tfvars` livrés. Le workflow impose d'y écrire les domaines/URLs **en clair** (ex. `https://<service>.<domaine-homelab>`), pas `${SNI}` (§ langue, format et sécurité). **Advisory par défaut**, **bloquant sur `security-patch` / `new-stack`** (décision humaine ALI-204, arbitrage 2 « Oui » + contrôle sécurité QA Docker, cf. `severity_overrides` ; SG-1).

## Contrat de vérification (`checks`)

```yaml
checks:
  interdit:
    motif: "\\$\\{?SNI\\}?"          # ${SNI} ou $SNI dans un fichier Terraform livré
    portee: "fichiers .tf / .tfvars uniquement"
  hors_perimetre:
    # l'interdiction ne vise QUE les fichiers Terraform livrés ;
    # les paramètres du workflow (${stack_name}, ${auth_type}, …) restent autorisés ailleurs
    - "docker-compose (*.yml)"
    - "paramètres de workflow (${stack_name}, ${auth_type}, ${traefik_network}, …)"
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` `${SNI}` détecté · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor terraform-no-sni — <fichier>   (source : homelab/sensors/sensors/terraform-no-sni.md @ <commit>)
- verdict : ✅ aucun ${SNI} | ⚠️ ${SNI} présent : <fichier:ligne> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory par défaut : signale l'usage de `${SNI}`, ne bloque pas hors scope sécuritaire. **Bloquant sur `security-patch` / `new-stack`** (décision humaine ALI-204 + contrôle sécurité QA Docker) : sur ces scopes, un `${SNI}` détecté dans un livrable Terraform **arrête l'avancée** jusqu'à correction ou levée humaine explicite tracée. Même bloquant, le sensor **ne remplace pas** l'audit du QA Docker (niveau `renforcé`, qui inclut « absence de `${SNI}` en Terraform ») ni la validation humaine (SG-3). L'interdiction **ne concerne que** les fichiers Terraform livrés : les espaces réservés du workflow (`${stack_name}`, etc.) restent autorisés. **Parsing statique uniquement** (SG-4). La bascule en bloquant est actée par l'[ADR-0016](../../../decisions/0016-verification-gates-et-sensors-homelab.md) (SG-1).
