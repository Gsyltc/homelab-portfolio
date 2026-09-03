# Règles — couche `stack` : `<stack>`

Gabarit de règles **rattachées à une stack** (portainer, traefik, gitea, …). Copier ce fichier en `stacks/<stack>.md`. Chargé au démarrage, uniquement pour la **stack courante**.

Pendant Homelab de [`../../core/rules/projects/_template.md`](../../core/rules/projects/_template.md).

Précédence : sous `global`, au-dessus de `phase` et `scope`. Une règle stack ne peut pas contredire une règle `global` sans arbitrage humain.

> **Convention** (alignée sur le contrat amont et `core/rules/`) : ranger les règles sous des **rubriques topicales** en prose (voir exemples ci-dessous — à créer / renommer selon la stack). Chaque règle garde un identifiant `RULE-ST-NNN`, sa portée, son origine et sa date (traçabilité, clause SEC-5). N'ouvrir une couche `stack` que pour un **écart durable** de cette stack vis-à-vis des conventions globales ; sinon la règle relève de `global`.

## Conventions Docker/Swarm

- **RULE-ST-001** — _(exemple)_ Cette stack utilise un volume NFS partagé au lieu d'un volume local ; toujours déclarer le driver NFS.
  - _portée_ : stack `<stack>` · _origine_ : ALI-000 · _ajoutée le_ : AAAA-MM-JJ

## Conventions Traefik

_(rubrique indicative — règles de routage / labels Traefik propres à la stack)_

## Sécurité / Hardening

_(rubrique indicative — contraintes de sécurité propres à la stack ; toute règle visant un scope à garde-fous ou un contrôle de sécurité passe par le contrôle sécurité, cf. SEC-2)_

## Conventions Terraform

_(rubrique indicative — `.tfvars`, variables, conventions HCL propres à la stack)_

> Aucune règle réelle tant qu'une stack n'en a pas fait valider. Supprimer les rubriques inutilisées et les exemples au moment de créer le fichier réel.
