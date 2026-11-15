# Protocole — format de compte-rendu A2A (Homelab)

Source unique du **compte-rendu de revue** remonté par un reviewer au Tech Lead Homelab en fin de mission. Ce protocole et le schéma [`report-format.schema.yaml`](report-format.schema.yaml) font foi ; fiches d'agent et de stage le **référencent** sans le redupliquer (SG-1 / SEC-5).

- **Position dans le message A2A** : le rapport reviewer est la forme détaillée du `retour` / `rapport-verification`. L'enveloppe commune est définie une seule fois dans [`governance-security.md`](governance-security.md) § « Schéma du message A2A ».
- **Champs propres au reviewer** : `verdict`, `points[]` classés (`critical/warning/info`), `sensors[]` (équivalent de `sensors_resultats`). Ils ne contredisent pas l'enveloppe.
- **Sérialisation** : YAML, fichier `review-<agent>-<stack>.yaml` joint au commentaire.
- **Objectif** : un retour minimal, uniforme et déterministe. Le Tech Lead route sans relire de prose et compose seul la communication vers l'humain.

## Geste de fin de mission (obligatoire)

Règles communes (réponse dans le thread, mention valide, `trigger_outcomes`, reprise unique) : [`governance-security.md`](governance-security.md) § « Règle A2A », « Retour A2A ». Spécifique au reviewer, en toute dernière action (succès, échec ou blocage) :

1. Écrire le rapport conforme au schéma dans `review-<agent>-<stack>.yaml` (tokens en `kebab-case`, `<agent>` = valeur de l'enum `agent`).
2. Le joindre au commentaire de réponse :

```
multica issue comment add <issue-id> --parent <comment-id> \
  --attachment ./review-<agent>-<stack>.yaml \
  --content-file ./trigger.md
```

3. Corps (`trigger.md`) : mention valide du Tech Lead + `verdict` en un mot + « rapport YAML en pièce jointe ». Le détail vit dans le YAML, jamais dans le thread.

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
- Chaque élément de `sensors[]` porte aussi, **s'il a été contrôlé sur un livrable précis**, le `sha256` de ce livrable (et `origine: execute | repris`) : c'est ce qui permet de l'enregistrer dans `versions.json` ([`governance-security.md`](governance-security.md) § « Un contrôle, un propriétaire »).
- Chaque `point` porte `constat` (quoi), `cause` (pourquoi), `correction` (autosuffisante) et un `id` stable (`P1`, `P2`…).
- `domaine_correction` — rôle correcteur suggéré (**`null` si inconnu**) ; le Tech Lead tranche.
- `arbitrage_requis` — l'agent **signale** un choix non purement technique ; **seul le Tech Lead** décide d'escalader. `arbitrage_motif` (non-`null` **uniquement** si `arbitrage_requis = true`) énonce le choix, les options et le compromis, en 1 à 3 phrases, pour que le Tech Lead l'explique tel quel à l'humain.
- `blocage` — non-`null` **uniquement** si `verdict = BLOQUE`.

## Traitement par le Tech Lead

Le Tech Lead lit le `verdict` (aiguillage immédiat), télécharge le YAML attaché, agrège les `points` des différents spécialistes, **passe en revue le tableau `sensors[]`** (chaque sensor déclaré doit y figurer avec son verdict ; un `indisponible` ou un `ecart` est tracé comme écart au Rapport de vérification, jamais lu comme conforme — SG-2), puis :

- **Renvoi via le Tech Lead** : sur `verdict = RENVOI` d'un QA ou d'une revue sécurité, le rapport va au Tech Lead. Il attend l'autre rapport, synthétise, puis transmet **un lot de correctifs** par `id` à l'agent créateur. Il n'y a pas de boucle courte directe QA ↔ spécialiste. Mécanisme : [`quality-assurance.md` Step 5](../stages/production/quality-assurance.md) et [`reviewer.md`](reviewer.md). Le QA ne modifie jamais le livrable ; le Tech Lead est tenu informé (piste d'audit).
- **Escalade humaine** : sur `arbitrage_requis = true` (ou tout choix structurant), le Tech Lead décide de l'escalade et **présente l'arbitrage à l'humain en s'appuyant sur `arbitrage_motif`**. Il peut le reformuler, mais le motif doit déjà contenir le choix, les options et le compromis (validation humaine granulaire, invariant). Les spécialistes ne s'adressent jamais directement à l'humain.
