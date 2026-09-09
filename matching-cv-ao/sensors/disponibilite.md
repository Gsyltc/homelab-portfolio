# Sensor `disponibilite-complete` — traçabilité de la disponibilité collaborateur

Manifeste déclaratif du sensor qui contrôle la présence **obligatoire** de l'information de disponibilité dans chaque profil CV structuré (`cv-profils`). **Advisory** : produit un rapport, ne bloque jamais le gate humain.

## Objet

Chaque collaborateur du JSON `cv-profils` (produit par le stage `extraction-cv`, Gestionnaire CV) **doit** porter une disponibilité complète, structurée en objet :

- `disponibilite.date_disponibilite` — date ISO `AAAA-MM-JJ` à partir de laquelle le collaborateur est disponible ;
- `disponibilite.taux_utilisation` — taux d'utilisation actuel, nombre entre `0` et `100` (en %).

Ces deux champs sont **mandatory**. Un profil dont l'un des deux manque, est vide, ou hors bornes est **non conforme**.

## Frontière et déclenchement

```yaml
type: sensor
id: disponibilite-complete
nature: advisory
frontiere: "Analyse → Matching"
artefact_controle: cv-profils
regles:
  - id: date-disponibilite-presente
    champ: disponibilite.date_disponibilite
    controle: "présent, non vide, date ISO AAAA-MM-JJ valide"
  - id: taux-utilisation-present
    champ: disponibilite.taux_utilisation
    controle: "présent, numérique, compris entre 0 et 100 inclus"
portee: "chaque objet de la liste collaborateurs"
```

## En cas d'écart (advisory)

- Le sensor **ne bloque pas** : il **signale** dans le « Rapport de disponibilité » sur l'issue chaque collaborateur dont la disponibilité est incomplète ou hors bornes, et **propose de revenir compléter** le CV avant de présenter le contenu à l'humain.
- L'humain reste seul décideur : demander la correction, ou valider en connaissance de cause en actant l'écart sur l'issue.

## Rapport de sensor (piste d'audit)

Posté en commentaire sur l'issue, à la frontière Analyse → Matching, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible.

```
Rapport de disponibilité — Analyse → Matching   (source : matching-cv-ao/sensors/disponibilite.md)
- <collaborateur> :
  - date-disponibilite-presente : ✅ | ⚠️ <manquante/invalide> | ⛔ <indisponible>
  - taux-utilisation-present : ✅ | ⚠️ <manquant/hors bornes> | ⛔ <indisponible>
```
