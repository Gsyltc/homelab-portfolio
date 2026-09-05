# Règles — couche `phase` : Production et Contrôle

Règles propres à la phase **Production et Contrôle** (Phase 2 : création docker-compose, vérification QA Docker, configuration Terraform, branches n8n/HA, contrôle qualité central). Chargées **à la demande** quand la phase Production est déclenchée.

Précédence : sous `global` et `stack`, au-dessus de `scope`.

## Manière de travailler

- **RULE-PH-001** — Les agents sont appelés **un après l'autre, dans l'ordre du workflow** (jamais lancés en parallèle) : le Tech Lead sérialise les délégations de phase Production et n'enchaîne le suivant qu'après le retour contrôlé du précédent.
  - _portée_ : phase Production · _origine_ : homelab-workflow.md §« Concurrence » + arbitrage humain (HOM-149, erreur de lancement simultané en début de phase 3) · _ajoutée le_ : 2026-09-04
