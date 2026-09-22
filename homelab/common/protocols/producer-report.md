# Protocole — fin de mission producteur (Homelab)

Source unique du **geste de fin de mission** d'un agent **producteur** (stages `review_class: none`) : livrable seul, corps minimal, zéro prose. Les fiches de stage et d'agent producteur **référencent** ce protocole, elles ne le redupliquent pas (source unique — SG-1 / SEC-5).

Distinct du compte-rendu structuré des **reviewers** ([`report-format.md`](report-format.md) / [`report-format.schema.json`](report-format.schema.json), **inchangé**) : un producteur ne joint **aucun fichier de rapport JSON**.

## Geste de fin de mission (obligatoire)

En toute dernière action (livré, ou bloqué), le producteur :

- ne joint **que son livrable** (le fichier produit) — **aucun fichier de rapport** ;
- réduit le corps au **strict minimum** : mention valide du Tech Lead + **une** ligne de statut (`livré` / `proposé` / `appliqué` / `bloqué : <raison en une phrase>`) ;
- **aucune prose, aucun relevé fin, aucune liste de points, aucun bloc technique** dans le thread ;
- publie **en réponse dans le thread** de la mission ; après publication, lire `trigger_outcomes` — statut `blocked` / `coalesced` / `deferred` → corriger la mention.

Pour les branches **n8n / Home Assistant** : le livrable est appliqué via MCP ; ne joindre un fichier **que s'il existe** (p. ex. export de flux), sinon la ligne de statut suffit.

> Invariant conservé : sans **mention valide** du Leader, le compte-rendu est réputé **non rendu** et le flux s'arrête. Toujours au Leader, jamais à l'agent de notifications. Aucun secret ni `${SNI}`.
