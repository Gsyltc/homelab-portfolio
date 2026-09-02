# Règles — couche `project` : `<projet>`

Gabarit de règles **spécifiques à un projet**. Copier ce fichier en `projects/<slug-du-projet>.md` au démarrage d'un projet qui a ses propres règles. Chargé au démarrage, uniquement pour le **projet courant**.

Précédence : sous `workspace`, au-dessus de `phase` et `scope`. Une règle projet ne peut pas contredire une règle `workspace` sans arbitrage humain.

Exemple (à remplacer) :

- **RULE-PROJ-001** — _(exemple)_ Ce projet applique GDPR + Loi 25 ; toute donnée personnelle est classifiée en `1.3`.
  - _portée_ : project · _origine_ : ALI-000 · _ajoutée le_ : AAAA-MM-JJ

> Aucune règle réelle tant qu'un projet n'en a pas fait valider.
