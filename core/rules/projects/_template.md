# Règles — couche `project` : `<projet>`

Gabarit de règles **spécifiques à un projet**. Copier ce fichier en `projects/<slug-du-projet>.md` au démarrage d'un projet qui a ses propres règles. Chargé au démarrage, uniquement pour le **projet courant**.

Précédence : sous `workspace`, au-dessus de `phase` et `scope`. Une règle projet ne peut pas contredire une règle `workspace` sans arbitrage humain.

> **Convention** (alignée sur le contrat amont) : ranger les règles sous des **rubriques topicales** en prose (voir exemples ci-dessous — à créer / renommer selon le projet). Chaque règle garde un identifiant `RULE-PROJ-NNN`, sa portée, son origine et sa date (traçabilité, clause SEC-5). N'ouvrir une couche `project` que pour un **écart durable** de ce projet vis-à-vis des pratiques du workspace ; sinon la règle relève de `workspace`.

## Manière de travailler

- **RULE-PROJ-001** — _(exemple)_ Ce projet applique GDPR + Loi 25 ; toute donnée personnelle est classifiée en `1.3`.
  - _portée_ : project · _origine_ : ALI-000 · _ajoutée le_ : AAAA-MM-JJ

## Posture de vérification

_(rubrique indicative — règles de vérification / test propres au projet)_

## Sécurité

_(rubrique indicative — contraintes de sécurité propres au projet ; toute règle visant un scope à garde-fous ou un contrôle de sécurité passe par le contrôle sécurité, cf. SEC-2)_

> Aucune règle réelle tant qu'un projet n'en a pas fait valider. Supprimer les rubriques inutilisées et les exemples au moment de créer le fichier réel.
