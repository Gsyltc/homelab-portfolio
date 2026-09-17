# Sensor `expertise-firme` — traçabilité de l'expertise de firme vis-à-vis de l'AO

Manifeste déclaratif du sensor qui contrôle l'objet **`expertise_firme`** produit par le stage `parse-ao` (Analyste RFP) lorsqu'un AO exige une **expérience/expertise de firme**, au regard du **référentiel des contextes clients** `${ROOT_DIRECTORY}/clients/*.json`. **Advisory et non bloquant** : produit un rapport et déclenche, le cas échéant, une **gate humaine légère** ; il ne bloque jamais le workflow ni le gate humain.

## Objet

Lorsque l'AO exige une expertise de firme (`expertise_firme.exigee = "oui"`), l'objet `expertise_firme` (artefact `ao-expertise-firme`) **doit** :

- décomposer l'exigence en `criteres_attendus[]` (secteur, technologie, contexte, mandat similaire, volume, avec `minimum` le cas échéant) ;
- fournir une `couverture[]` par critère (`couvert` / `partiel` / `non_couvert`) **appuyée sur des preuves factuelles** tirées du référentiel `clients/*.json` (client, chemin du fichier, mandats pertinents) — **jamais** une couverture supposée ;
- porter un `verdict` ∈ {`conforme`, `minimums_non_atteints`, `indeterminable`} et un `gate_humaine` ∈ {`aucune`, `legere`}.

Le référentiel `clients/<nom-client>.json` est **maintenu par le Gestionnaire CV** lors de l'analyse d'un CV long contenant un contexte client (voir la compétence `cv-analyse` du plugin `rh-assistant`). Un référentiel `clients/` **vide ou insuffisant** conduit à `non_couvert`/`indeterminable` (jamais à une expertise inventée).

## Frontière et déclenchement

```yaml
type: sensor
id: expertise-firme
nature: advisory
bloquant: false
frontiere: "Analyse → Matching"
artefact_controle: ao-expertise-firme
source_reference: "${ROOT_DIRECTORY}/clients/*.json"
regles:
  - id: expertise-objet-present
    champ: expertise_firme
    controle: "présent ; exigee ∈ {oui, non, non_precise}"
  - id: couverture-appuyee-referentiel
    champ: expertise_firme.couverture
    controle: "si exigee = oui : chaque critère porte un statut et, si couvert/partiel, au moins une preuve issue de clients/*.json (jamais inventée)"
  - id: verdict-coherent
    champ: expertise_firme.verdict
    controle: "∈ {conforme, minimums_non_atteints, indeterminable} ; gate_humaine = legere (+ detail_gate) dès que verdict ≠ conforme"
portee: "objet expertise_firme de l'AO (lorsque exigee = oui)"
```

## Gate humaine légère (non bloquante)

- Si `expertise_firme.exigee = "oui"` et `verdict` ∈ {`minimums_non_atteints`, `indeterminable`} (donc `gate_humaine: "legere"`), le sensor **signale** le point et le Coordinateur **demande une confirmation légère** à l'humain : poursuivre malgré le manque d'expertise de firme, ou compléter le référentiel `clients/` (analyser un CV long apportant le contexte/mandats manquants).
- **Non bloquant** : cette gate **n'arrête pas** le workflow. L'humain reste seul décideur — il peut acter le manque et poursuivre, ou demander à compléter le référentiel. Aucune exclusion ni arrêt automatique.
- Si `exigee = "non"`/`non_precise`, ou `verdict = conforme`, aucune gate n'est levée (`gate_humaine: "aucune"`).

## Rapport de sensor (piste d'audit)

Posté en commentaire sur l'issue, à la frontière Analyse → Matching, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart / minimums non atteints · `⛔` indisponible.

```
Rapport d'expertise de firme — Analyse → Matching   (source : matching-cv-ao/sensors/expertise-firme.md)
- expertise exigée par l'AO : oui | non | non_precise
- expertise-objet-present : ✅ | ⚠️ <objet manquant/incomplet> | ⛔ <indisponible>
- couverture-appuyee-referentiel : ✅ | ⚠️ <critère sans preuve dans clients/*.json> | ⛔ <référentiel clients/ vide>
- verdict-coherent : ✅ conforme | ⚠️ minimums_non_atteints (gate humaine légère) | ⚠️ indeterminable (gate humaine légère) | ⛔ <indisponible>
- gate humaine légère : aucune | légère → <detail_gate : critère non couvert / minimum non atteint>
```
