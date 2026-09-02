# Verification gates — contrôle de traçabilité aux frontières de phases

Manifeste déclaratif des **verification gates** décrits dans « Verification gates & Sensors » de [`docs/core-workflow.md`](../../docs/core-workflow.md). **Advisory** : produit un rapport, ne bloque jamais le gate humain.

À chaque **frontière de phase**, en amont de la validation humaine, trois contrôles déterministes :

1. **`artefacts-presents`** — les artefacts requis en sortie de phase existent.
2. **`liaison-tracabilite`** — chaque exigence retenue est reliée à un ADR / livrable, et chaque décision structurante est tracée en ADR.
3. **`absence-orphelin`** — aucun ADR / livrable / diagramme n'est déconnecté (sans exigence amont ni référence).

## Frontières et artefacts requis

> Adossé à la structure Inception / Construction / Operation actuelle. La matrice suivra l'ossature à 5 phases au stage ultérieur (voir ADR-0003, IMP-003).

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
    sensors: [diagram-validity]

  - id: construction-operation
    frontiere: "Construction → Operation"
    artefacts_requis:
      - livrables_detailles
      - adr_a_jour
      - coherence_doc_adr
    checks: [artefacts-presents, liaison-tracabilite, absence-orphelin]
    sensors: [required-sections]

  - id: operation-fin
    frontiere: "Operation → Fin"
    artefacts_requis:
      - plan_ou_configuration_valide
      - rollback_si_action_destructive   # conditionnel
    checks: [artefacts-presents]
```

## En cas d'écart (advisory)

- Le coordinateur **ne bloque pas** : il **signale l'écart** dans le « Rapport de vérification » sur l'issue et **propose de revenir corriger** avant de présenter le contenu à l'humain.
- L'humain reste seul décideur : demander la correction, ou valider en connaissance de cause en actant l'écart sur l'issue.
- Le gate automatique ne remplace, n'abaisse ni ne court-circuite jamais le contrôle sécurité ni la validation humaine granulaire (invariants non négociables).

## Rapport de gate (piste d'audit)

Posté en commentaire sur l'issue, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (non exécuté / en erreur / hors périmètre — **jamais lu comme conforme**, SG-2). Le rapport porte sa **source** (manifeste + commit) pour être non répudiable (SG-5).

```
Rapport de vérification — <frontière>   (source : core/sensors/gates.md @ <commit>)
- artefacts-presents : ✅ | ⚠️ <artefact manquant> | ⛔ <indisponible>
- liaison-tracabilite : ✅ | ⚠️ <exigence sans ADR / livrable> | ⛔ <indisponible>
- absence-orphelin : ✅ | ⚠️ <ADR / livrable / diagramme orphelin> | ⛔ <indisponible>
```
