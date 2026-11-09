# Protocole — fin de mission producteur (Homelab)

Source unique du **geste de fin de mission** d'un agent **producteur** (stages `review_class: none`) : **message A2A `retour` joint en YAML** + corps minimal, zéro prose d'orchestration dans le fil. Les fiches de stage et d'agent producteur **référencent** ce protocole, elles ne le redupliquent pas (source unique — SG-1 / SEC-5).

Même paradigme que le compte-rendu structuré des **reviewers** ([`report-format.md`](report-format.md) / [`report-format.schema.yaml`](report-format.schema.yaml), rapport **YAML** `review-<agent>-<stack>.yaml`), mais pour un **producteur** : le retour du producteur est l'instance **`retour`** du **message A2A** ([`governance-security.md`](governance-security.md) § « Schéma du message A2A »). Le producteur ne produit **pas** un rapport de revue (il ne classe pas de points `critical/warning/info`) ; il porte son **résultat** et ses **`sensors_resultats`** dans un YAML `retour` joint, aux côtés de son livrable.

> **Sensors portés par le YAML de retour, jamais par la prose du fil.** Les verdicts par sensor déclaré (exécutés à l'écriture — [`stage-protocol.md`](stage-protocol.md) § 4) voyagent dans le champ `sensors_resultats` du message A2A `retour`, **pas** en prose dans le thread. Aucun sensor déclaré ne reste silencieux : un sensor de `sensors_a_executer` absent de `sensors_resultats` est un écart (SG-2 : `indisponible ≠ conforme`).

## Geste de fin de mission (obligatoire)

En toute dernière action (livré, ou bloqué), le producteur :

- **joint deux fichiers** : son **livrable** (le fichier produit) **et** un **message A2A `retour` en YAML** (`retour-<agent>-<stack>.yaml`) conforme au schéma de [`governance-security.md`](governance-security.md), portant `resultat` (`ok` / `ecart` / `halt`), `sensors_resultats` (un élément par sensor déclaré, verdict rendu par `sensor.py`, jamais réinterprété) et `artefacts` (le livrable produit) ;
- réduit le corps du commentaire au **strict minimum** : mention valide du Tech Lead + **une** ligne de statut (`livré` / `proposé` / `appliqué` / `bloqué : <raison en une phrase>`) + le **nom du fichier YAML `retour` joint** ;
- **aucune prose, aucun relevé fin, aucune liste de points, aucun bloc technique, aucun rapport de sensor en prose** dans le **thread de fin de mission** : le détail (résultat, verdicts de sensors) vit exclusivement dans le YAML `retour` attaché ;
- publie **en réponse dans le thread** de la mission ; après publication, **lire
  obligatoirement `trigger_outcomes`** dans la réponse de la CLI. La tâche n'est
  **PAS terminée** tant que `trigger_outcomes` ne confirme pas un run enfilé pour le
  Tech Lead :
  - statut `blocked` / `coalesced` / `deferred`, **ou** absence de mention active du
    Tech Lead dans le corps → **corriger la mention et retenter UNE seule fois** ;
  - si la reprise échoue → **passer l'issue en `blocked`** et **escalader à l'humain**
    (ne jamais laisser le flux s'arrêter silencieusement) ;
  - un compte-rendu dont `trigger_outcomes` ne confirme aucun run de reprise est
    **réputé non rendu** — l'agent le signale explicitement plutôt que de clore ;
- **ne jamais régénérer ni relivrer le livrable pour corriger une mention manquante** :
  le livrable est **idempotent** une fois produit — republier / compléter **uniquement**
  la mention et le YAML `retour` (retente unique), puis escalade si la reprise échoue.
  Régénérer un livrable pour un problème de mention est un **défaut** (risque de perte de
  paramètres, double livraison), pas une correction.

Pour les branches **n8n / Home Assistant** : le livrable est appliqué via MCP ; ne joindre le fichier de livrable **que s'il existe** (p. ex. export de flux) — le message A2A `retour` (résultat + `sensors_resultats`), lui, est **toujours** joint.

> Invariant conservé : sans **mention valide** du Leader, le compte-rendu est réputé **non rendu** et le flux s'arrête. Toujours au Leader, jamais à l'agent de notifications. Aucun secret ni `${SNI}` dans le YAML.
