# Sensor `disponibilite-complete` — disponibilité collaborateur obligatoire

Manifeste déclaratif du sensor `disponibilite-complete`. **Advisory** : produit un rapport, ne bloque jamais le gate humain.

Contrôle déterministe, à la **frontière Analyse → Matching**, que chaque profil CV structuré (`cv-profils`, produit par le Gestionnaire CV) porte une disponibilité **complète** : une **date de disponibilité** ISO et un **taux d'utilisation** courant.

## Contrat

```yaml
type: sensor
id: disponibilite-complete
nature: advisory
frontiere: "Analyse → Matching"
artefact_controle: cv-profils
rapport: issue
regles:
  - id: date-disponibilite-presente
    objet: "Chaque collaborateur porte disponibilite.date_disponibilite au format AAAA-MM-JJ."
  - id: taux-utilisation-present
    objet: "Chaque collaborateur porte disponibilite.taux_utilisation (entier 0–100)."
```

## Champ contrôlé

Le champ `disponibilite` de chaque entrée `collaborateurs` est un **objet obligatoire** :

```json
"disponibilite": {
  "date_disponibilite": "<AAAA-MM-JJ>",
  "taux_utilisation": <0–100>
}
```

- `date_disponibilite` — date ISO `AAAA-MM-JJ` à partir de laquelle le collaborateur est disponible ; **obligatoire**.
- `taux_utilisation` — taux d'utilisation actuel en pourcentage, entier `0–100` ; **obligatoire**.

## En cas d'écart (advisory)

- Le coordinateur **ne bloque pas** : il **signale l'écart** dans le « Rapport de vérification » sur l'issue et **propose de revenir corriger** avant de présenter le contenu à l'humain.
- L'humain reste seul décideur : demander la correction (compléter la disponibilité), ou valider en connaissance de cause en actant l'écart sur l'issue.

## Rapport de sensor (piste d'audit)

Posté en commentaire sur l'issue, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible.

```
Rapport de vérification — disponibilite-complete   (source : matching-cv-ao/sensors/disponibilite.md)
- date-disponibilite-presente : ✅ | ⚠️ <collaborateur sans date_disponibilite> | ⛔ <indisponible>
- taux-utilisation-present : ✅ | ⚠️ <collaborateur sans taux_utilisation> | ⛔ <indisponible>
```
