# Protocole — répertoire de relecture `.a-valider/` (Homelab)

Source unique du répertoire où sont déposés les fichiers générés en attente de validation humaine. Fiches de stage et de sensor le **référencent** sans le redéfinir.

## Chemin

- `${WORK_DIRECTORY}/.a-valider/<id-tâche>/<stack>/`
  - `<id-tâche>` : identifiant de l'issue (ex. `HOM-303`)
  - `${WORK_DIRECTORY}` vide ou introuvable : issue `blocked` ([`stack-detection.md`](../stages/initialisation/stack-detection.md))

## Contenu

- Livrables générés : fichiers Docker Compose, `.tf`, `.tfvars`. Aucun fichier hors de ce répertoire avant la validation humaine explicite
- Fichiers de travail : `parametres.json`, `preselection.json` (jamais déposés), `versions.json`
- Le commentaire de livraison consigne le chemin résolu

## Cycle de vie

- **Alimentation** : spécialistes, Production ([`docker-compose-creation.md`](../stages/production/docker-compose-creation.md), [`terraform-configuration.md`](../stages/production/terraform-configuration.md))
- **Déplacement** (non copie) vers les emplacements définitifs, puis suppression : [`file-deposit.md`](../stages/validation/file-deposit.md)
- **Échec de vérification** : conserver le répertoire et le signaler à l'humain

## Règles

- **Hors détection** : exclu de toute recherche de stack existante (un fichier présent n'est pas une preuve)
- **Hors git** : à exclure via le `.gitignore` du répertoire de travail ; le Tech Lead le vérifie et le signale à l'humain sinon
