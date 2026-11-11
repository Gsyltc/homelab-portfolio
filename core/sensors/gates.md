# Verification gates — contrôle de traçabilité aux frontières de phases

Manifeste déclaratif des **verification gates** décrits dans [`core/common/protocols/governance-security.md`](../common/protocols/governance-security.md) et exécutés aux frontières de phases par [`core/common/conductor.md`](../common/conductor.md). **Advisory** : produit un rapport, ne bloque jamais le gate humain.

À chaque **frontière de phase**, en amont de la validation humaine, trois contrôles déterministes :

1. **`artefacts-presents`** — les artefacts requis en sortie de phase existent.
2. **`liaison-tracabilite`** — chaque exigence retenue est reliée à un ADR / livrable, et chaque décision structurante est tracée en ADR.
3. **`absence-orphelin`** — aucun ADR / livrable / diagramme n'est déconnecté (sans exigence amont ni référence).

## Frontières et artefacts requis

> Adossé à la structure Inception / Construction / Operation actuelle. La matrice suivra l'ossature à 5 phases au stage ultérieur.

```yaml
type: verification-gates
nature: advisory
origine: ALI-188
boundaries:
  - id: entree-inception
    frontiere: "Entrée → Inception"
    artefacts_requis:
      - demande_brute_consignee
      - repertoire_projet_confirme
      - scope_confirme
    checks: [artefacts-presents]

  - id: inception-construction
    frontiere: "Inception → Construction"
    artefacts_requis:
      - besoins_traces
      - adr_conception
      - diagramme_principal
      - scope_et_axes_confirmes
    checks: [artefacts-presents, liaison-tracabilite, absence-orphelin]
    sensors: [diagram-validity, data-lifecycle, claim-sources, style-concision]   # data-lifecycle : advisory pour tous (assiste l'Architecte de solution, alerte le coordinateur — jamais bloquant) ; claim-sources : chaque affirmation de la conception porte une source résoluble

  - id: construction-operation
    frontiere: "Construction → Operation"
    artefacts_requis:
      - livrables_detailles
      - adr_a_jour
      - coherence_doc_adr
    checks: [artefacts-presents, liaison-tracabilite, absence-orphelin]
    sensors: [required-sections-adr, required-sections-architecture, claim-sources, traceability, style-concision]   # traceability : chaîne exigence → ADR → livrable cohérente, sans orphelin dérivé ; claim-sources : chaque affirmation retenue porte une source résoluble

  - id: operation-fin
    frontiere: "Operation → Fin"
    artefacts_requis:
      - plan_ou_configuration_valide
      - rollback_si_action_destructive   # conditionnel
    checks: [artefacts-presents]
```

## Exécution

Lancé **depuis le checkout `homelab-portfolio`** (le dépôt `core`), chemin ancré sur sa racine `$CORE_HOME`, `--root` pointant le projet vérifié (convention d'invocation : [`../common/protocols/stage-protocol.md`](../common/protocols/stage-protocol.md), temps 4) :

```
python3 "$CORE_HOME/core/scripts/sensor.py" --root <projet> gate <id-frontière> [--attest <artefact>,...]
```

Le script produit le « Rapport de vérification » ci-dessous.

- **`artefacts-presents`** — vérifié par fichier pour `adr_conception`, `adr_a_jour`, `livrables_detailles` et `diagramme_principal`. Les autres artefacts (ex. `demande_brute_consignee`) vivent sur l'issue : ils restent `⛔` tant que le coordinateur ne les atteste pas avec `--attest`.
- **`liaison-tracabilite`** — verdict du sensor [`traceability`](sensors/traceability.md).
- **`absence-orphelin`** — verdict du sensor [`upstream-coverage`](sensors/upstream-coverage.md).
- **`sensors`** — chaque sensor listé pour la frontière est exécuté en balayage de gate.

## En cas d'écart (advisory)

- Le coordinateur **ne bloque pas** : il **signale l'écart** dans le « Rapport de vérification » sur l'issue et **propose de revenir corriger** avant de présenter le contenu à l'humain.
- L'humain reste seul décideur : demander la correction, ou valider en connaissance de cause en actant l'écart sur l'issue.
- Le gate automatique ne remplace, n'abaisse ni ne court-circuite jamais le contrôle sécurité ni la validation humaine granulaire (invariants non négociables).

## Rapport de gate (piste d'audit)

Posté en commentaire sur l'issue, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (non exécuté / en erreur / hors périmètre — **jamais lu comme conforme**, SG-2). Le rapport porte sa **source** (manifeste + commit) pour être non répudiable (SG-5).

> **Destinataire = humain → présentation en clair (ci-dessous). Destinataire = agent → message A2A.** Le rapport de gate affiché ci-dessous est la **présentation destinée à l'humain**, avant sa validation. Lorsque les verdicts doivent être **transmis à un autre agent** (handoff A2A pur), ils voyagent dans un **message A2A `type: rapport-verification`** (champ `sensors_resultats`, verdicts `conforme | ecart | indisponible`) joint à l'issue — schéma source unique : [`../common/protocols/governance-security.md`](../common/protocols/governance-security.md), « Schéma du message A2A ». Ce fichier ne redéfinit pas le schéma.

```
Rapport de vérification — <frontière>   (source : core/sensors/gates.md @ <commit>)
- artefacts-presents : ✅ | ⚠️ <artefact manquant> | ⛔ <indisponible>
- liaison-tracabilite : ✅ | ⚠️ <exigence sans ADR / livrable> | ⛔ <indisponible>
- absence-orphelin : ✅ | ⚠️ <ADR / livrable / diagramme orphelin> | ⛔ <indisponible>
```
