# Protocole — fin de mission producteur (Homelab)

Source unique du **geste de fin de mission** d'un agent **producteur** (stages `review_class: none`) : livrable seul, corps minimal, zéro prose. Les fiches de stage et d'agent producteur **référencent** ce protocole, elles ne le redupliquent pas (source unique — SG-1 / SEC-5).

Distinct du compte-rendu structuré des **reviewers** ([`report-format.md`](report-format.md) / [`report-format.schema.json`](report-format.schema.json), **inchangé**) : un producteur ne joint **aucun fichier de rapport JSON**.

## Geste de fin de mission (obligatoire)

En toute dernière action (livré, ou bloqué), le producteur :

- ne joint **que son livrable** (le fichier produit) — **aucun fichier de rapport** ;
- réduit le corps au **strict minimum** : mention valide du Tech Lead + **une** ligne de statut (`livré` / `proposé` / `appliqué` / `bloqué : <raison en une phrase>`) ;
- **aucune prose, aucun relevé fin, aucune liste de points, aucun bloc technique** dans le thread ;
- publie **en réponse dans le thread** de la mission ; après publication, **lire
  obligatoirement `trigger_outcomes`** dans la réponse de la CLI. La tâche n'est
  **PAS terminée** tant que `trigger_outcomes` ne confirme pas un run enfilé pour le
  Tech Lead :
  - statut `blocked` / `coalesced` / `deferred`, **ou** absence de mention active du
    Tech Lead dans le corps → **corriger la mention et retenter UNE seule fois** ;
  - si la reprise échoue → **passer l'issue en `blocked`** et **escalader à l'humain**
    (ne jamais laisser le flux s'arrêter silencieusement) ;
  - un compte-rendu dont `trigger_outcomes` ne confirme aucun run de reprise est
    **réputé non rendu** — l'agent le signale explicitement plutôt que de clore.

Pour les branches **n8n / Home Assistant** : le livrable est appliqué via MCP ; ne joindre un fichier **que s'il existe** (p. ex. export de flux), sinon la ligne de statut suffit.

> Invariant conservé : sans **mention valide** du Leader, le compte-rendu est réputé **non rendu** et le flux s'arrête. Toujours au Leader, jamais à l'agent de notifications. Aucun secret ni `${SNI}`.
