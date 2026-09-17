# Verification gates & Sensors — fiabilisation déterministe

Ce répertoire contient les **manifestes déclaratifs** des mécanismes de fiabilisation déterministe du workflow Matching AO ↔ CV.

## Nature déclarative (non exécutable à ce stade)

Ces fichiers **décrivent le contrat** (périmètre de déclenchement, règles de contrôle, sortie attendue) de façon lisible et déterministe. Ce **ne sont pas des scripts exécutables**.

## Garde-fou : advisory par décision

- Les gates **ne bloquent jamais** la validation humaine granulaire et **ne la remplacent pas**.
- Un signal **au vert ne vaut pas validation** ; un signal **en échec n'autorise aucun raccourci**.

## Gates définis

| Gate | Fichier | Objet |
| --- | --- | --- |
| Verification gates | `gates.md` | Contrôle de traçabilité aux frontières de phases |
| Sensor `disponibilite-complete` | `disponibilite.md` | Présence obligatoire de la disponibilité (date de disponibilité + taux d'utilisation en %) dans chaque profil CV, contrôlée à la frontière Analyse → Matching |
| Sensor `equivalence-mifi` | `equivalence-mifi.md` | Présence et cohérence de l'objet `mifi` (équivalence MIFI, 4 états d'`equivalence_requise`) dans chaque profil CV ; signale les collaborateurs en `a_verifier`, contrôlé à la frontière Analyse → Matching |
| Sensor `localisation-complete` | `localisation.md` | Présence obligatoire de la ville du candidat (`localisation.ville`) dans chaque profil CV ; signale les villes manquantes (mention humaine attendue), base du critère de proximité ≤ 70 km, contrôlé à la frontière Analyse → Matching |
| Sensor `expertise-firme` | `expertise-firme.md` | Lorsque l'AO exige une expertise de firme, contrôle l'objet `expertise_firme` et sa couverture appuyée sur le référentiel `${ROOT_DIRECTORY}/clients/*.json` ; un `verdict` ≠ `conforme` déclenche une **gate humaine légère non bloquante**, contrôlé à la frontière Analyse → Matching |
