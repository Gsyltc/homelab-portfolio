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
| Verification gates | [`gates.md`](gates.md) | Contrôle de traçabilité aux frontières de phases |
| Sensor `disponibilite-complete` | [`disponibilite.md`](disponibilite.md) | Disponibilité collaborateur obligatoire (`date_disponibilite` + `taux_utilisation`) à la frontière Analyse → Matching |
