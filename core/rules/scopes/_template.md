# Règles — couche `scope` : `<scope>`

Gabarit de règles **rattachées à un scope** (voir « Scopes et axes d'exécution » : `standard`, `feature`, `infra`, `security-patch`, `mvp`, `poc`, `express`, `enterprise`). Copier ce fichier en `scopes/<scope>.md`. Chargé **à la demande** quand le scope est confirmé.

Précédence : couche la plus faible. Une règle `scope` ne peut pas contredire une règle `workspace` / `project` / `phase` sans arbitrage humain.

> **Convention** (alignée AI-DLC) : ranger les règles sous des **rubriques topicales** en prose (voir exemples ci-dessous — à créer / renommer selon le scope). Chaque règle garde un identifiant `RULE-SC-NNN`, sa portée, son origine et sa date (traçabilité, clause SEC-5). Une règle visant un scope à garde-fous (`security-patch`, `enterprise`) ou une phase de vérification passe par le **contrôle sécurité systématique** (clause SEC-2) ; elle ne peut jamais abaisser un garde-fou de scope (plancher de vérification, Depth non abaissable).

## Posture de vérification

- **RULE-SC-001** — _(exemple)_ `security-patch` : l'analyse d'impact du correctif (surface, effets de bord, non-régression) est produite avant toute recommandation.
  - _portée_ : scope security-patch · _origine_ : ALI-000 · _ajoutée le_ : AAAA-MM-JJ

## Manière de travailler

_(rubrique indicative — allègements / renforcements de méthode propres au scope)_

> Aucune règle réelle tant qu'un scope n'en a pas fait valider. Supprimer les rubriques inutilisées et les exemples au moment de créer le fichier réel.
