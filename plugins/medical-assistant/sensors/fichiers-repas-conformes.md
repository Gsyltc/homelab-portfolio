---
id: fichiers-repas-conformes
kind: deterministic
command: "python3 plugins/medical-assistant/scripts/sensors/fichiers_repas_conformes.py --data-dir /nfs/workspace/datas/repas"
default_severity: advisory
description: "Vérifie que repas-retenus.md, repas-exclus.md et ingredients-refuses.md sont à jour et conformes : front matter cohérent (type, updated, count, oldest/newest), tableau à 4 colonnes, listes à puces sans doublon."
category: repas-donnees
fire_on: gate
matches: "/nfs/workspace/datas/repas/{repas-retenus.md,repas-exclus.md,ingredients-refuses.md}"
origine: AUQU-153
---

# Sensor `fichiers-repas-conformes` — données de repas à jour et conformes *(clôture)*

Check déterministe lancé **à la clôture** du chef cuisinier : contrôle les **trois fichiers de
données** du domaine repas, en écriture comme en lecture, contre le schéma de la skill
`recherche-repas`.

## Contrat de vérification (`checks`)

```yaml
checks:
  fichiers: [repas-retenus.md, repas-exclus.md, ingredients-refuses.md]
  front_matter:
    present_et_plat: true
    type_attendu: [repas-retenus, repas-exclus, ingredients-refuses]
    updated: "date ISO valide, non postérieure à la date de référence"
    count: "entier égal au nombre réel d'entrées du corps"
  repas_retenus:
    rolling_window_days: 30
    tableau: "en-tête Date | Repas | Appareil | Emplacement de la recette, 4 colonnes par ligne"
    dates: "ISO valides"
    oldest_newest: "égaux aux bornes réelles du tableau"
  repas_exclus / ingredients_refuses:
    liste: "puces « - élément », aucun doublon"
```

## Sortie (piste d'audit)

Un verdict **par fichier** : `✅` conforme · `⚠️` écart de format (détail des écarts) ·
`⛔` indisponible (fichier absent ou illisible).

```
Sensor fichiers-repas-conformes — <fichier>
- verdict : ✅ front matter et corps conformes | ⚠️ <n> écart(s) de format | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : le sensor constate la conformité, il **ne réécrit aucun fichier**. La correction
(front matter, `count`, bornes, doublons) revient à l'agent, qui relance le sensor ensuite.
`/nfs/workspace/datas/repas/` reste la source de vérité.
