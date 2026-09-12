# Sensor `localisation-complete` — traçabilité de la localisation collaborateur

Manifeste déclaratif du sensor qui contrôle la présence **obligatoire** de l'information de localisation (ville du candidat) dans chaque profil CV structuré (`cv-profils`). **Advisory** : produit un rapport, ne bloque jamais le gate humain.

## Objet

Chaque collaborateur du JSON `cv-profils` (produit par le stage `extraction-cv`, Gestionnaire CV) **doit** porter une localisation, structurée en objet :

- `localisation.ville` — **ville de résidence/rattachement du collaborateur** (obligatoire) ;
- `localisation.region` — province/région si disponible (optionnel) ;
- `localisation.pays` — pays si disponible (optionnel) ;
- `localisation.source` — `cv` (ville extraite du CV) ou `humain` (ville obtenue par mention humaine).

Le champ `localisation.ville` est **mandatory** : le CV du candidat **doit** contenir sa ville. Un profil dont `ville` manque ou est vide est **non conforme** — le Gestionnaire CV doit alors **poser une mention humaine** pour l'obtenir (**ne rien inventer**).

Cette localisation est la base du **critère de proximité géographique** : lorsque l'AO impose un travail `sur_site` ou `hybride` (`ao.localisation_travail.mode`), un collaborateur situé à **plus de `rayon_km` (70 km par défaut)** de la `ville_site` de l'AO est **exclu** au filtre d'éligibilité (voir [`../agents/gestionnaire-cv-agent.md`](../agents/gestionnaire-cv-agent.md)). Ce sensor ne calcule pas la distance : il garantit seulement que la donnée d'entrée (ville du candidat) est **présente** pour permettre ce calcul.

## Frontière et déclenchement

```yaml
type: sensor
id: localisation-complete
nature: advisory
frontiere: "Analyse → Matching"
artefact_controle: cv-profils
regles:
  - id: ville-presente
    champ: localisation.ville
    controle: "présent, non vide (ville du candidat)"
  - id: source-valide
    champ: localisation.source
    controle: "présent, valeur ∈ {cv, humain}"
portee: "chaque objet de la liste collaborateurs"
```

## En cas d'écart (advisory)

- Le sensor **ne bloque pas** : il **signale** dans le « Rapport de localisation » sur l'issue chaque collaborateur dont la ville est manquante ou vide, et **propose de revenir compléter** le CV (mention humaine pour obtenir la ville) avant de présenter le contenu à l'humain.
- Une ville manquante conduit le Gestionnaire CV à classer le collaborateur `a_verifier` (jamais `exclu` de force) avec **mention humaine** — le sensor ne présume rien.
- L'humain reste seul décideur : demander la correction, ou valider en connaissance de cause en actant l'écart sur l'issue.

## Rapport de sensor (piste d'audit)

Posté en commentaire sur l'issue, à la frontière Analyse → Matching, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible.

```
Rapport de localisation — Analyse → Matching   (source : matching-cv-ao/sensors/localisation.md)
- <collaborateur> :
  - ville-presente : ✅ | ⚠️ <ville manquante — mention humaine attendue> | ⛔ <indisponible>
  - source-valide : ✅ | ⚠️ <source absente/hors énumération> | ⛔ <indisponible>
```
