---
id: repas-calendrier-agenda
kind: deterministic
command: "python3 plugins/medical-assistant/scripts/sensors/repas_calendrier_agenda.py --data-dir /nfs/workspace/datas/repas"
default_severity: advisory
description: "Vérifie que chaque repas retenu à venir existe dans le calendrier Home Assistant `calendar.repas` avec ses ingrédients consignés, et que le créneau du lendemain 12h–13h existe sans description."
category: repas-agenda
fire_on: gate
matches: "/nfs/workspace/datas/repas/repas-retenus.md"
origine: AUQU-153
---

# Sensor `repas-calendrier-agenda` — repas et ingrédients dans l'agenda *(clôture)*

Check déterministe lancé **à la clôture** du chef cuisinier : confronte les repas retenus à venir
de `repas-retenus.md` aux évènements réellement présents dans le calendrier Home Assistant
(`calendar.repas` par défaut, surchargeable par `HOMEASSISTANT_CALENDAR_ENTITY`).

## Contrat de vérification (`checks`)

```yaml
checks:
  perimetre: "repas retenus dont la date >= date de référence (ou --jour)"
  evenement_repas:
    existe: true                    # même jour, 19h00–20h00
    summary_porte_le_plat: true     # libellé du repas (comparaison normalisée)
    ingredients_consignes: true     # description = liste de puces « - ingrédient », sans ligne hors format
  evenement_lendemain:
    existe: true                    # jour + 1, 12h00–13h00
    summary_porte_le_plat: true
    sans_description: true
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart (repas absent, ingrédients manquants ou hors format, créneau
12h–13h absent ou renseigné) · `⛔` indisponible (variables `HOMEASSISTANT_URL` /
`HOMEASSISTANT_TOKEN` absentes, calendrier injoignable, fichiers de données illisibles).
Source tracée : données `/nfs/workspace/datas/repas/` + calendrier HA.

```
Sensor repas-calendrier-agenda — <N> repas à venir
- verdict : ✅ repas et ingrédients présents au calendrier | ⚠️ <n> écart(s) calendrier | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : le signal factualise l'écart, il ne remplace pas la validation humaine. **Lecture seule**
sur le calendrier : le sensor ne crée, ne modifie ni ne supprime aucun évènement. Aucun secret
affiché : ni l'URL ni le jeton HA ne sortent du script (seul le code HTTP est cité en cas d'erreur).
