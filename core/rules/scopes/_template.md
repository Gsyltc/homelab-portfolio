# Règles — couche `scope` : `<scope>`

Gabarit de règles **rattachées à un scope** (voir « Scopes et axes d'exécution » : `standard`, `feature`, `infra`, `security-patch`, `mvp`, `poc`, `express`, `enterprise`). Copier ce fichier en `scopes/<scope>.md`. Chargé **à la demande** quand le scope est confirmé.

Précédence : couche la plus faible. Une règle `scope` ne peut pas contredire une règle `workspace` / `project` / `phase` sans arbitrage humain.

Exemple (à remplacer) :

- **RULE-SC-001** — _(exemple)_ `security-patch` : l'analyse d'impact du correctif (surface, effets de bord, non-régression) est produite avant toute recommandation.
  - _portée_ : scope security-patch · _origine_ : ALI-000 · _ajoutée le_ : AAAA-MM-JJ

> Aucune règle réelle tant qu'un scope n'en a pas fait valider.
