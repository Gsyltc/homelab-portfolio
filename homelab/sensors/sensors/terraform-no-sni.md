---
id: terraform-no-sni
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
description: "Vérifie l'absence de la variable ${SNI} dans les fichiers Terraform livrés (domaines/URLs en clair attendus)."
category: security
fire_on: write
matches: "{**/*.tf,**/*.tfvars}"
origine: ALI-204
---

# Sensor `terraform-no-sni` — absence de `${SNI}` en Terraform *(prioritaire, sécurité)*

Check déterministe déclenché **à l'écriture** (`fire_on: write`) d'un fichier Terraform : vérifie l'**absence de la variable `${SNI}`** dans les fichiers `.tf` / `.tfvars` livrés. Le workflow impose d'y écrire les domaines/URLs **en clair** (ex. `https://<service>.<domaine-homelab>`), pas `${SNI}` (§ langue, format et sécurité). **Advisory** (`default_severity: advisory` — passage à `blocking` = décision structurante, SG-1).

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

Advisory par défaut : signale l'usage de `${SNI}`, ne bloque pas. **Ne remplace pas** l'audit du QA Docker (niveau `renforcé`, qui inclut « absence de `${SNI}` en Terraform ») ni la validation humaine (SG-3). L'interdiction **ne concerne que** les fichiers Terraform livrés : les espaces réservés du workflow (`${stack_name}`, etc.) restent autorisés. **Parsing statique uniquement** (SG-4).
