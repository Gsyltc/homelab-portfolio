# Sensor `disponibilite-complete` — traçabilité de la disponibilité collaborateur

Manifeste déclaratif du sensor qui contrôle la présence **obligatoire** de l'information de disponibilité et du **type de collaborateur** (`alithya` | `recrutement` | `offre_conditionnelle` | `non_disponible`) dans chaque profil CV structuré (`cv-profils`), ainsi que le respect des **transitions STRICTES** de la machine à états du `type_collaborateur`. **Advisory** : produit un rapport, ne bloque jamais le gate humain.

## Objet

Chaque collaborateur du YAML `cv-profils` (produit par le stage `extraction-cv`, Gestionnaire CV) **doit** porter une disponibilité complète, structurée en objet, ainsi qu'un **type de collaborateur** :

- `type_collaborateur` — statut du collaborateur qui **qualifie sa disponibilité**, l'une des **4 valeurs** (`enum`) : `alithya` (interne, disponible selon `disponibilite`) · `recrutement` (candidat en cours de recrutement, disponible conditionnellement à l'embauche) · `offre_conditionnelle` (disponible seulement si l'AO est remporté) · `non_disponible` (ne peut pas être positionné — **écarté du matching**). Ce champ suit une **machine à états à transitions STRICTES** (seul l'**état courant** est porté, **aucun historique**) : transitions autorisées `recrutement → offre_conditionnelle`, `recrutement → alithya`, `offre_conditionnelle → alithya`, et depuis tout état `→ non_disponible` (se retire / démission) ; **toute autre transition est interdite** et **signalée** à l'humain (voir § Frontière, règle `transition-stricte`) ;
- `disponibilite.date_disponibilite` — date ISO `AAAA-MM-JJ` à partir de laquelle le collaborateur est disponible ;
- `disponibilite.taux_utilisation` — taux d'utilisation actuel, nombre entre `0` et `100` (en %).

Ces trois champs sont **mandatory**. Un profil dont l'un d'eux manque, est vide, hors bornes, ou (pour `type_collaborateur`) hors des 4 valeurs autorisées est **non conforme**. Un collaborateur `type_collaborateur = non_disponible` est **conforme** mais **signalé comme indisponible** (le filtre d'éligibilité le classe `exclu`, axe `disponibilite`).

## Frontière et déclenchement

```yaml
type: sensor
id: disponibilite-complete
nature: advisory
frontiere: "Analyse → Matching"
artefact_controle: cv-profils
regles:
  - id: type-collaborateur-present
    champ: type_collaborateur
    controle: "présent, non vide, l'une des valeurs alithya|recrutement|offre_conditionnelle|non_disponible ; non_disponible signalé comme indisponible (exclu du matching)"
  - id: transition-stricte
    champ: type_collaborateur
    controle: "si l'état change par rapport à la version précédente, la transition doit appartenir au graphe autorisé (recrutement→offre_conditionnelle, recrutement→alithya, offre_conditionnelle→alithya, *→non_disponible) ; toute transition hors graphe est SIGNALÉE à l'humain (advisory, non bloquant), jamais appliquée silencieusement"
  - id: date-disponibilite-presente
    champ: disponibilite.date_disponibilite
    controle: "présent, non vide, date ISO AAAA-MM-JJ valide"
  - id: taux-utilisation-present
    champ: disponibilite.taux_utilisation
    controle: "présent, numérique, compris entre 0 et 100 inclus"
portee: "chaque objet de la liste collaborateurs"
```

## En cas d'écart (advisory)

- Le sensor **ne bloque pas** : il **signale** dans le « Rapport de disponibilité » sur l'issue chaque collaborateur dont la disponibilité est incomplète ou hors bornes, ou dont le `type_collaborateur` est manquant / hors des 4 valeurs autorisées, et **propose de revenir compléter** le CV avant de présenter le contenu à l'humain.
- Un collaborateur `type_collaborateur = non_disponible` est **conforme** au sensor (donnée présente et valide) mais **signalé comme indisponible** (`⛔`) : il est écarté du matching (le filtre d'éligibilité le classe `exclu`, axe `disponibilite`). Un `type_collaborateur` **absent ou invalide** est un **écart** (`⚠️`), pas une indisponibilité.
- Une **transition d'état hors graphe** (changement de `type_collaborateur` ne respectant pas les transitions autorisées — ex. `non_disponible → *`, `offre_conditionnelle → recrutement`, `alithya → offre_conditionnelle`) est **signalée** (`⚠️`, règle `transition-stricte`) et **n'est pas appliquée** : l'humain tranche. Le sensor ne réécrit jamais un état de sa propre initiative.
- L'humain reste seul décideur : demander la correction, ou valider en connaissance de cause en actant l'écart sur l'issue.

## Rapport de sensor (piste d'audit)

Posté en commentaire sur l'issue, à la frontière Analyse → Matching, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible.

```
Rapport de disponibilité — Analyse → Matching   (source : matching-cv-ao/sensors/disponibilite.md)
- <collaborateur> :
  - type-collaborateur-present : ✅ <alithya/recrutement/offre_conditionnelle> | ⛔ non_disponible | ⚠️ <manquant/invalide>
  - transition-stricte : ✅ <pas de changement / transition autorisée> | ⚠️ <transition hors graphe signalée — non appliquée>
  - date-disponibilite-presente : ✅ | ⚠️ <manquante/invalide> | ⛔ <indisponible>
  - taux-utilisation-present : ✅ | ⚠️ <manquant/hors bornes> | ⛔ <indisponible>
```
