# Règles — couche `scope` : `<scope>`

Gabarit de règles **rattachées à un scope Homelab** (voir `homelab/scopes/` : `stack-update`, `new-stack`, `config-change`, `security-patch`, `infra-terraform`, `n8n`, `home-assistant`). Copier ce fichier en `scopes/<scope>.md`. Chargé **à la demande** quand le scope est confirmé.

Pendant Homelab de [`../../core/rules/scopes/_template.md`](../../core/rules/scopes/_template.md).

Précédence : couche la plus faible. Une règle `scope` ne peut pas contredire une règle `global` / `stack` / `phase` sans arbitrage humain.

> **Convention** (alignée sur le contrat amont et `core/rules/`) : ranger les règles sous des **rubriques topicales** en prose (voir exemples ci-dessous — à créer / renommer selon le scope). Chaque règle garde un identifiant `RULE-SC-NNN`, sa portée, son origine et sa date (traçabilité, clause SEC-5). Une règle visant un scope à garde-fous (`security-patch`, `new-stack`) ou une phase de vérification passe par le **contrôle sécurité systématique** (clause SEC-2) ; elle ne peut jamais abaisser un garde-fou de scope (plancher de vérification, Depth non abaissable).

## Conventions Docker/Swarm

- **RULE-SC-001** — _(exemple)_ `new-stack` : le docker-compose inclut toujours un healthcheck applicatif (pas seulement TCP).
  - _portée_ : scope `new-stack` · _origine_ : ALI-000 · _ajoutée le_ : AAAA-MM-JJ

## Sécurité / Hardening

_(rubrique indicative — contraintes de sécurité propres au scope)_

## Manière de travailler

_(rubrique indicative — allègements / renforcements de méthode propres au scope)_

> Aucune règle réelle tant qu'un scope n'en a pas fait valider. Supprimer les rubriques inutilisées et les exemples au moment de créer le fichier réel.
