# Protocole — format de compte-rendu A2A (Homelab)

Source unique du **compte-rendu structuré** qu'un spécialiste / reviewer remonte au Tech Lead Homelab en fin de mission. Ce protocole et le schéma [`report-format.schema.json`](report-format.schema.json) font foi : les fiches d'agent et de stage **référencent** ce format, elles ne le redupliquent pas (source unique — SG-1 / SEC-5).

> **Sérialisation : YAML.** Le fichier de rapport est écrit en **YAML** (`review-<agent>-<stack>.yaml`), pas en JSON. Le schéma [`report-format.schema.json`](report-format.schema.json) reste un **JSON Schema** (outil standard de description du contrat) et **valide le document YAML** : YAML et JSON partagent le même modèle de données, le schéma s'applique à l'identique. Seule la **sérialisation du rapport** est YAML ; le fichier de schéma, lui, demeure du JSON Schema.

Objectif : **minimiser** le retour d'information des spécialistes et le rendre **uniforme et déterministe**, pour que le Tech Lead route/arbitre sans relire de la prose. Le Tech Lead reste le **seul** à composer la communication en langage naturel vers l'humain.

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

Le contrat complet (types, enums, obligations) est porté par [`report-format.schema.json`](report-format.schema.json). Points saillants :

- `verdict` — `OK` | `RENVOI` | `BLOQUE`, lu directement par le Tech Lead pour l'aiguillage macro.
- `points[]` — **trié par gravité décroissante (`critical` en tête)**. Plafond : **3 par défaut, 5 sur `security-patch` / `new-stack`**. Tableau vide = RAS.
- `sensors[]` — **verdict de chaque sensor déclaré** dans le champ `sensors:` de la fiche de stage exécutée : c'est ce qui **rend visible dans le compte-rendu que les sensors ont bien été vérifiés**. Un élément `{ id, fire_on, verdict, note }` **par sensor déclaré** — aucune omission (SG-2 : un sensor déclaré non exécuté est `indisponible`, jamais absent ; silence = écart). `verdict` ∈ `conforme` (✅) | `ecart` (⚠️) | `indisponible` (⛔) ; `note` = une ligne factuelle (fait vérifié, écart, ou motif d'indisponibilité), **jamais de valeur de secret ni de `${SNI}`**. Ce tableau est le **miroir déterministe** des rapports de sensor postés à l'écriture ([`stage-protocol.md`](stage-protocol.md) § 4). **Advisory** : il factualise la vérification, ne vaut pas validation (SG-1..6). Tableau vide **uniquement** si le stage ne déclare aucun sensor.
- Chaque `point` porte `constat` (quoi), `cause` (pourquoi) et `correction` (comment corriger — autosuffisant pour un autre agent), plus un `id` stable (`P1`, `P2`…).
- `domaine_correction` — indice du rôle correcteur (**`null` autorisé** quand l'agent ne sait pas) ; c'est une **suggestion**, le Tech Lead tranche.
- `arbitrage_requis` — l'agent **signale** qu'un choix non purement technique existe ; il **ne décide pas** de l'escalade. **Seul le Tech Lead** détecte l'arbitrage et décide de remonter à l'humain. `arbitrage_motif` (non-`null` **uniquement** si `arbitrage_requis = true`) est rédigé pour que **le Tech Lead l'explique tel quel à l'humain** : il énonce le **choix en jeu**, les **options** (au moins deux) et le **compromis / l'impact** de chacune. Assez détaillé pour éclairer la décision, **concis** pour autant : 1 à 3 phrases, factuel, sans jargon interne ni rappel du workflow.
- `blocage` — non-`null` **uniquement** si `verdict = BLOQUE`.

## Traitement par le Tech Lead

Le Tech Lead lit le `verdict` (aiguillage immédiat), télécharge le YAML attaché, agrège les `points` des différents spécialistes, **passe en revue le tableau `sensors[]`** (chaque sensor déclaré doit y figurer avec son verdict ; un `indisponible` ou un `ecart` est tracé comme écart au Rapport de vérification, jamais lu comme conforme — SG-2), puis :

- **Renvoi direct à l'agent créateur** : sur `verdict = RENVOI` d'un QA, l'Analyste QA transmet les `points[]` par `id` directement à l'agent créateur via la **boucle courte QA ↔ spécialiste** — mécanisme décrit par [`quality-assurance.md` Step 5](../stages/production/quality-assurance.md) et [`reviewer.md`](reviewer.md). Le QA ne modifie jamais le livrable ; le Tech Lead est tenu informé (piste d'audit).
- **Escalade humaine** : sur `arbitrage_requis = true` (ou tout choix structurant), le Tech Lead décide de l'escalade et **présente l'arbitrage à l'humain en s'appuyant sur `arbitrage_motif`** — qu'il reformule au besoin, mais qui doit déjà contenir le choix, les options et le compromis pour être explicable clairement (validation humaine granulaire, invariant). Les spécialistes ne s'adressent jamais directement à l'humain.
