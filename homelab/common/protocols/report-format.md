# Protocole — format de compte-rendu A2A (Homelab)

Source unique du **compte-rendu de revue** qu'un reviewer remonte au Tech Lead Homelab en fin de mission. Ce protocole et le schéma [`report-format.schema.yaml`](report-format.schema.yaml) font foi ; les fiches d'agent et de stage le **référencent**, sans le redupliquer (source unique — SG-1 / SEC-5).

> **Sérialisation : YAML.** Rapport et schéma sont en **YAML**. Le rapport conforme est écrit dans `review-<agent>-<stack>.yaml` et déposé en pièce jointe.

Objectif : un retour **minimal, uniforme et déterministe**, pour que le Tech Lead route sans relire de la prose. Lui seul compose la communication en langage naturel vers l'humain.

## Geste de fin de mission (obligatoire)

En toute dernière action (succès, échec OU blocage), le spécialiste :

1. écrit le compte-rendu conforme au schéma dans un fichier **YAML** `review-<agent>-<stack>.yaml` (tokens en `kebab-case`, `<agent>` = valeur de l'enum `agent`) ;
2. le dépose **en pièce jointe** du commentaire ;
3. publie ce commentaire **en réponse dans le thread** de la mission, avec la **mention valide** du Tech Lead.

```
multica issue comment add <issue-id> --parent <comment-id> \
  --attachment ./review-<agent>-<stack>.yaml \
  --content-file ./trigger.md
```

Le corps (`trigger.md`) est réduit au **strict minimum** : la mention valide du Tech Lead + le `verdict` en un mot + « rapport YAML en pièce jointe ». **Aucune prose, aucune liste de points dans le thread** — le détail vit exclusivement dans le YAML attaché.

> Invariant conservé : sans **mention valide** du Leader, le compte-rendu est réputé **non rendu** et le flux s'arrête (voir [`reviewer.md`](reviewer.md) § « Fin de revue »). Après publication, lire `trigger_outcomes` ; statut `blocked` / `coalesced` / `deferred` → corriger la mention. Aucun secret ni `${SNI}` dans le YAML.

### Exemple de rapport YAML

```yaml
report:
  agent: analyste-qa
  verdict: RENVOI
  livrable: docker-compose.yml
  points:
    - id: P1
      gravite: critical
      constat: Secret en clair dans la variable d'environnement du service.
      cause: Valeur littérale au lieu d'une convention _FILE / secret Swarm.
      correction: Déplacer la valeur vers un secret Swarm et référencer via _FILE.
      domaine_correction: docker
      arbitrage_requis: false
      arbitrage_motif: null
  sensors:
    - id: yaml-validity
      fire_on: write
      verdict: conforme
      note: Le docker-compose.yml est un YAML valide.
    - id: plaintext-secret
      fire_on: write
      verdict: ecart
      note: Secret en clair détecté (emplacement reporté en P1, valeur jamais citée).
  blocage: null
```

## Contrat des champs

Le contrat complet (types, enums, obligations) est porté par [`report-format.schema.yaml`](report-format.schema.yaml). Points saillants :

- `verdict` — `OK` | `RENVOI` | `BLOQUE`, lu directement par le Tech Lead pour l'aiguillage macro.
- `points[]` — **trié par gravité décroissante (`critical` en tête)**. Plafond : **3 par défaut, 5 sur `security-patch` / `new-stack`**. Tableau vide = RAS.
- `sensors[]` — **verdict de chaque sensor déclaré** dans le champ `sensors:` du stage : c'est ce qui **rend visible que les sensors ont bien été vérifiés**. Un élément `{ id, fire_on, verdict, note }` par sensor — aucune omission (SG-2 : non exécuté = `indisponible`, jamais absent). `verdict` ∈ `conforme` (✅) | `ecart` (⚠️) | `indisponible` (⛔). **Advisory** : miroir des rapports à l'écriture ([`stage-protocol.md`](stage-protocol.md) § 4), ne vaut pas validation. Tableau vide **uniquement** si le stage ne déclare aucun sensor.
- Chaque `point` porte `constat` (quoi), `cause` (pourquoi), `correction` (autosuffisante) et un `id` stable (`P1`, `P2`…).
- `domaine_correction` — rôle correcteur suggéré (**`null` si inconnu**) ; le Tech Lead tranche.
- `arbitrage_requis` — l'agent **signale** un choix non purement technique ; **seul le Tech Lead** décide d'escalader. `arbitrage_motif` (non-`null` **uniquement** si `arbitrage_requis = true`) énonce le choix, les options et le compromis, en 1 à 3 phrases, pour que le Tech Lead l'explique tel quel à l'humain.
- `blocage` — non-`null` **uniquement** si `verdict = BLOQUE`.

## Traitement par le Tech Lead

Le Tech Lead lit le `verdict` (aiguillage immédiat), télécharge le YAML attaché, agrège les `points` des différents spécialistes, **passe en revue le tableau `sensors[]`** (chaque sensor déclaré doit y figurer avec son verdict ; un `indisponible` ou un `ecart` est tracé comme écart au Rapport de vérification, jamais lu comme conforme — SG-2), puis :

- **Renvoi direct à l'agent créateur** : sur `verdict = RENVOI` d'un QA, l'Analyste QA transmet les `points[]` par `id` directement à l'agent créateur via la **boucle courte QA ↔ spécialiste** — mécanisme décrit par [`quality-assurance.md` Step 5](../stages/production/quality-assurance.md) et [`reviewer.md`](reviewer.md). Le QA ne modifie jamais le livrable ; le Tech Lead est tenu informé (piste d'audit).
- **Escalade humaine** : sur `arbitrage_requis = true` (ou tout choix structurant), le Tech Lead décide de l'escalade et **présente l'arbitrage à l'humain en s'appuyant sur `arbitrage_motif`** — qu'il reformule au besoin, mais qui doit déjà contenir le choix, les options et le compromis pour être explicable clairement (validation humaine granulaire, invariant). Les spécialistes ne s'adressent jamais directement à l'humain.
