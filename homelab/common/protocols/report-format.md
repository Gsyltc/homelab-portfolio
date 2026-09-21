# Protocole — format de compte-rendu A2A (Homelab)

Source unique du **compte-rendu structuré** qu'un spécialiste / reviewer remonte au Tech Lead Homelab en fin de mission. Ce protocole et le schéma [`report-format.schema.json`](report-format.schema.json) font foi : les fiches d'agent et de stage **référencent** ce format, elles ne le redupliquent pas (source unique — SG-1 / SEC-5).

Objectif : **minimiser** le retour d'information des spécialistes et le rendre **uniforme et déterministe**, pour que le Tech Lead route/arbitre sans relire de la prose. Le Tech Lead reste le **seul** à composer la communication en langage naturel vers l'humain.

## Geste de fin de mission (obligatoire)

En toute dernière action (succès, échec OU blocage), le spécialiste :

1. écrit le compte-rendu conforme au schéma dans un fichier `review-<agent>-<stack>.json` (tokens en `kebab-case`, `<agent>` = valeur de l'enum `agent`) ;
2. le dépose **en pièce jointe** du commentaire ;
3. publie ce commentaire **en réponse dans le thread** de la mission, avec la **mention valide** du Tech Lead.

```
multica issue comment add <issue-id> --parent <comment-id> \
  --attachment ./review-<agent>-<stack>.json \
  --content-file ./trigger.md
```

Le corps (`trigger.md`) est réduit au **strict minimum** : la mention valide du Tech Lead + le `verdict` en un mot + « rapport JSON en pièce jointe ». **Aucune prose, aucune liste de points dans le thread** — le détail vit exclusivement dans le JSON attaché.

> Invariant conservé : sans **mention valide** du Leader, le compte-rendu est réputé **non rendu** et le flux s'arrête (voir [`reviewer.md`](reviewer.md) § « Fin de revue »). Après publication, lire `trigger_outcomes` ; statut `blocked` / `coalesced` / `deferred` → corriger la mention. Aucun secret ni `${SNI}` dans le JSON.

## Contrat des champs

Le contrat complet (types, enums, obligations) est porté par [`report-format.schema.json`](report-format.schema.json). Points saillants :

- `verdict` — `OK` | `RENVOI` | `BLOQUE`, lu directement par le Tech Lead pour l'aiguillage macro.
- `points[]` — **trié par gravité décroissante (`critical` en tête)**. Plafond : **3 par défaut, 5 sur `security-patch` / `new-stack`**. Tableau vide = RAS.
- Chaque `point` porte `constat` (quoi), `cause` (pourquoi) et `correction` (comment corriger — autosuffisant pour un autre agent), plus un `id` stable (`P1`, `P2`…).
- `domaine_correction` — indice du rôle correcteur (**`null` autorisé** quand l'agent ne sait pas) ; c'est une **suggestion**, le Tech Lead tranche.
- `arbitrage_requis` — l'agent **signale** qu'un choix non purement technique existe ; il **ne décide pas** de l'escalade. **Seul le Tech Lead** détecte l'arbitrage et décide de remonter à l'humain. `arbitrage_motif` est non-`null` **uniquement** si `arbitrage_requis = true`.
- `blocage` — non-`null` **uniquement** si `verdict = BLOQUE`.

## Traitement par le Tech Lead

Le Tech Lead lit le `verdict` (aiguillage immédiat), télécharge le JSON attaché, agrège les `points` des différents spécialistes, puis :

- **Renvoi à un agent correcteur** : délègue le(s) point(s) par `id` ; `constat` + `cause` + `correction` + `domaine_correction` suffisent à l'agent pour comprendre et corriger sans re-analyser. L'agent correcteur renvoie ensuite un compte-rendu au même format.
- **Escalade humaine** : sur `arbitrage_requis = true` (ou tout choix structurant), le Tech Lead décide de l'escalade et présente l'arbitrage à l'humain (validation humaine granulaire, invariant). Les spécialistes ne s'adressent jamais directement à l'humain.
