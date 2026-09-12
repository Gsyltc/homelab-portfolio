# Sensor `equivalence-mifi` — traçabilité de l'équivalence MIFI collaborateur

Manifeste déclaratif du sensor qui contrôle la présence et la cohérence de l'objet **`mifi`** (équivalence des diplômes — contexte gouvernemental Québec, MIFI) dans chaque profil CV structuré (`cv-profils`). **Advisory** : produit un rapport, ne bloque jamais le gate humain.

## Objet

Chaque collaborateur du JSON `cv-profils` (produit par le stage `extraction-cv`, Gestionnaire CV) **doit** porter un objet `mifi` documentant si son niveau d'études nécessite une **équivalence MIFI** (Ministère de l'Immigration, de la Francisation et de l'Intégration). Le champ pivot `equivalence_requise` porte **4 états** :

- `non_requise` — **diplôme canadien** : aucune équivalence nécessaire ; `niveau_equivalent_qc` = le niveau tel quel.
- `oui` — le collaborateur **possède le MIFI** : `niveau_equivalent_qc` reconnu (DEC, BAC, etc.).
- `non` — **études à l'étranger sans MIFI** : pas d'équivalence disponible.
- `a_verifier` — le CV **ne permet pas de trancher** : à confirmer par l'humain (**ne rien inventer**).

L'objet `mifi` est **mandatory**. Un profil sans objet `mifi`, ou dont `equivalence_requise` est absent/hors énumération, est **non conforme**. Lorsque `equivalence_requise` vaut `oui` ou `non_requise`, `niveau_equivalent_qc` doit être **non vide** (le niveau reconnu au Québec est requis pour statuer la conformité au matching).

## Frontière et déclenchement

```yaml
type: sensor
id: equivalence-mifi
nature: advisory
frontiere: "Analyse → Matching"
artefact_controle: cv-profils
regles:
  - id: mifi-present
    champ: mifi
    controle: "objet présent"
  - id: equivalence-requise-valide
    champ: mifi.equivalence_requise
    controle: "présent, valeur ∈ {non_requise, oui, non, a_verifier}"
  - id: niveau-equivalent-qc-present-si-oui-ou-non-requise
    champ: mifi.niveau_equivalent_qc
    controle: "non vide lorsque mifi.equivalence_requise ∈ {oui, non_requise}"
  - id: a-verifier-signale
    champ: mifi.equivalence_requise
    controle: "si valeur = a_verifier → signaler (MIFI non tranché, réponse humaine attendue) sans bloquer"
portee: "chaque objet de la liste collaborateurs"
```

## En cas d'écart (advisory)

- Le sensor **ne bloque pas** : il **signale** dans le « Rapport d'équivalence MIFI » sur l'issue chaque collaborateur dont l'objet `mifi` est absent, incohérent (état hors énumération, `niveau_equivalent_qc` manquant alors que `equivalence_requise` = `oui`/`non_requise`), ou en état **`a_verifier`** (MIFI non tranché — réponse humaine attendue), et **propose de revenir compléter** le CV avant de présenter le contenu à l'humain.
- Les collaborateurs en `a_verifier` sont **listés explicitement** pour que l'humain tranche (passage à `oui` avec niveau, ou `non`) — le sensor ne présume rien.
- **Rappel de portée** : ce sensor est advisory et ne décide **pas** de l'éligibilité. La décision revient au filtre d'éligibilité (Gestionnaire CV) : une équivalence **tranchée `non`** face à un AO exigeant un niveau d'études rend l'axe **Études strict non atteint** ⇒ collaborateur `exclu` ; une équivalence **non tranchée** (`a_verifier`) laisse le collaborateur `a_verifier` (mention humaine — ne rien inventer).
- L'humain reste seul décideur : demander la correction, ou valider en connaissance de cause en actant l'écart sur l'issue.

## Rapport de sensor (piste d'audit)

Posté en commentaire sur l'issue, à la frontière Analyse → Matching, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart / à vérifier · `⛔` indisponible.

```
Rapport d'équivalence MIFI — Analyse → Matching   (source : matching-cv-ao/sensors/equivalence-mifi.md)
- <collaborateur> :
  - mifi-present : ✅ | ⚠️ <objet mifi manquant> | ⛔ <indisponible>
  - equivalence-requise-valide : ✅ | ⚠️ <absente/hors énumération> | ⛔ <indisponible>
  - niveau-equivalent-qc-present-si-oui-ou-non-requise : ✅ | ⚠️ <niveau manquant> | ⛔ <indisponible>
  - a-verifier-signale : ✅ (tranché) | ⚠️ <a_verifier — réponse humaine attendue> | ⛔ <indisponible>
```
