---
id: historique-repas-30j
kind: deterministic
command: "python3 plugins/medical-assistant/scripts/sensors/historique_repas_30j.py --data-dir /nfs/workspace/datas/repas"
default_severity: blocking
description: "Vérifie qu'aucun repas de repas-retenus.md n'est plus ancien que 30 jours glissants. Un repas au-delà de la fenêtre est un échec : l'historique doit être purgé avant clôture."
category: repas-historique
fire_on: gate
matches: "/nfs/workspace/datas/repas/repas-retenus.md"
origine: AUQU-153
---

# Sensor `historique-repas-30j` — historique dans la fenêtre de 30 jours *(clôture, bloquant)*

Check déterministe lancé **à la clôture** du chef cuisinier : `repas-retenus.md` est un historique
**glissant de 30 jours**. Toute entrée dont la date est antérieure à *date de référence − 30 jours*
est un **échec** : elle doit avoir été purgée, sinon le repas reste exclu des propositions au-delà
de la fenêtre et le décompte des 30 jours devient faux.

## Contrat de vérification (`checks`)

```yaml
checks:
  fichier: "/nfs/workspace/datas/repas/repas-retenus.md"
  fenetre_jours: 30
  chaque_entree:
    date_iso_lisible: true
    date >= (reference - 30 jours): true   # sinon FAILED
```

## Sortie (piste d'audit)

Verdicts : `✅` historique conforme · `⚠️` **FAILED** (au moins un repas plus ancien que 30 jours,
ou date illisible) · `⛔` indisponible (fichier absent, tableau illisible).

```
Sensor historique-repas-30j — repas-retenus.md
- verdict : ✅ historique conforme : <n> entrée(s) | ⚠️ FAILED : <n> repas au-delà de 30 jours | ⛔ indisponible : <motif>
```

## Garde-fou

**Bloquant** par décision humaine explicite (AUQU-153) : en cas d'échec, l'agent purge l'historique
(étape « Purge de l'historique glissant ») puis relance le sensor avant de clôturer. Le sensor
**ne modifie jamais la donnée** : il constate. Un `⛔` n'est jamais un vert (SG-2) et ne vaut pas
autorisation de clôturer.
