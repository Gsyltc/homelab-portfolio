# Protocole — fin de mission producteur (Homelab)

Source unique du **geste de fin de mission** d'un agent **producteur** (stages `review_class: none`). Fiches de stage et d'agent producteur le **référencent** sans le redupliquer (SG-1 / SEC-5).

- **Instance du message A2A** : le retour du producteur est un message `retour` ([`governance-security.md`](governance-security.md) § « Schéma du message A2A »). Il porte `resultat` et `sensors_resultats`, pas de points `critical/warning/info`.
- **Reviewer** : même paradigme, voir [`report-format.md`](report-format.md).
- **Sensors** : les verdicts par sensor déclaré (exécutés à l'écriture, [`stage-protocol.md`](stage-protocol.md) § 4) voyagent dans `sensors_resultats`, jamais en prose dans le fil. Un sensor de `sensors_a_executer` absent de `sensors_resultats` est un écart (SG-2 : `indisponible ≠ conforme`).

## Geste de fin de mission (obligatoire)

Règles communes (réponse dans le thread, mention valide, `trigger_outcomes`, reprise unique puis `blocked` + escalade) : [`governance-security.md`](governance-security.md) § « Règle A2A », « Retour A2A ». Spécifique au producteur, en toute dernière action (livré ou bloqué) :

- **Joindre deux fichiers** :
  - le **livrable** ;
  - le message A2A `retour` (`retour-<agent>-<stack>.yaml`) avec `resultat` (`ok` / `ecart` / `halt`), `sensors_resultats` (un élément par sensor déclaré, verdict de `sensor.py` jamais réinterprété) et `artefacts`.
- **Corps du commentaire** : mention valide du Tech Lead + **une** ligne de statut (`livré` / `proposé` / `appliqué` / `bloqué : <raison en une phrase>`) + nom du YAML joint.
- **Aucune** prose, relevé, liste de points, bloc technique ni rapport de sensor dans le thread de fin de mission.
- **Mention manquante ou non enfilée** : republier uniquement la mention et le YAML `retour`. Ne jamais régénérer ni relivrer le livrable (idempotent une fois produit) : le faire est un défaut (perte de paramètres, double livraison).

Pour les branches **n8n / Home Assistant** : le livrable est appliqué via MCP ; ne joindre le fichier de livrable **que s'il existe** (p. ex. export de flux) — le message A2A `retour` (résultat + `sensors_resultats`), lui, est **toujours** joint.
