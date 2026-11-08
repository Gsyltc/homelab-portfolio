---
id: checklist-progress
kind: deterministic
command: "python3 core/scripts/sensors/checklist_progress.py"
default_severity: advisory
description: "Restitue l'avancement de la checklist d'architecture (% global de la solution, cadrage, besoins MoSCoW, livrables) à partir du fichier d'état, sans décider ni écrire."
category: progress
fire_on: gate
matches: "documentation/00-checklist-architecture.md"
origine: HOM-273
---

# Sensor `checklist-progress` — avancement de la checklist d'architecture *(prioritaire)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`), **avant chaque gate granulaire humaine durant la Construction**. Il **parcourt le fichier d'état** de la checklist d'architecture (`documentation/00-checklist-architecture.md`) et **restitue l'avancement** porté par ce fichier. Il est lu par l'**Architecte de solution intégrateur** (coordinateur, Architecture Solution & Intégration) : il **constate**, il **ne décide pas** — aucun % n'est calculé ni écrit par le sensor, aucun auto-accept. **Advisory** (`default_severity: advisory`) : il n'empêche ni la validation humaine granulaire, ni le contrôle sécurité.

> **Source unique de la mécanique.** Le barème **80/10/10**, le décompte des sections conformes, la revue pair, l'acceptation humaine et l'agrégation (% section / % global) ont leur **source unique** dans le protocole [`../../common/protocols/architecture-checklist.md`](../../common/protocols/architecture-checklist.md). Le sensor **lit les % déjà portés** dans le fichier d'état par le coordinateur ; il ne les recalcule pas et ne redéfinit aucun contrat de sections (`required-sections`, `data-lifecycle` restent les sources uniques des dénominateurs).

## Avancements restitués

Le sensor rapporte, tels qu'ils figurent dans le fichier d'état :

- l'**avancement global de la solution** — `**% global :** <n> %` ;
- l'**avancement du cadrage** — titre `## Cadrage — <n> %` ;
- l'**avancement des besoins (MoSCoW)** — titre `## Besoins (MoSCoW) — <n> %` ;
- l'**avancement des livrables** — titre `## Livrables — <n> %`.

## Contrat de vérification (`checks`)

```yaml
checks:
  fichier: "documentation/00-checklist-architecture.md"   # fichier d'état de la checklist (présent)
  restitue:                                                # LECTURE SEULE des % déjà portés (le sensor constate)
    avancement_global_solution: "**% global :** <n> %"     # % global de la checklist
    avancement_cadrage: "## Cadrage — <n> %"               # section Cadrage
    avancement_besoins: "## Besoins (MoSCoW) — <n> %"      # section Besoins MoSCoW
    avancement_livrables: "## Livrables — <n> %"           # section Livrables
  calcul_80_10_10: "hors périmètre du sensor"              # mécanique = protocole architecture-checklist.md (source unique)
  auto_accept: false                                       # jamais : le sensor n'écrit rien, ne valide rien
  non_lisible: "⛔ indisponible"                           # fichier absent / illisible / aucun % lisible (SG-2)
```

## Sortie (piste d'audit)

Verdicts : `✅` avancement restitué · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5). Le sensor n'émet **jamais** `⚠️` : un avancement bas n'est pas un écart de forme, c'est un fait restitué à l'humain (le gate planification / réalisation ≥ 80 % relève du protocole et de la décision humaine, pas du sensor).

```
Sensor checklist-progress — documentation/00-checklist-architecture.md   (source : core/sensors/sensors/checklist-progress.md @ <commit>)
- verdict : ✅ avancement restitué — solution <n> % | cadrage <n> % | besoins <n> % | livrables <n> % | ⛔ indisponible : <motif>
  - avancement global de la solution : <n> %
  - avancement du cadrage : <n> %
  - avancement des besoins (MoSCoW) : <n> %
  - avancement des livrables : <n> %
```

## Garde-fous

- **Advisory, aucun auto-accept.** Le sensor **ne remplace ni ne conditionne** la validation humaine granulaire ni le contrôle sécurité systématique de l'Architecte cybersécurité (SG-3). Il **constate** l'avancement ; le jugement et l'acceptation restent humains (protocole § 7). Aucun % n'est écrit par le sensor.
- **SG-1 / SG-6** — manifeste versionné, `origine` traçable (HOM-273) ; tout affaiblissement du check passe par le contrôle sécurité. Le passage de `advisory` à `blocking` resterait une **décision séparée** (ADR + contrôle sécurité), comme pour les autres sensors.
- **SG-2 — indisponible ≠ conforme** : fichier d'état absent, illisible ou sans avancement lisible ⇒ `⛔`, jamais `✅`.
- **SG-4** — parsing **statique** seul (lecture Markdown, aucun rendu, aucun réseau, aucune exécution de contenu d'artefact) ; le fichier d'état est une donnée non fiable.
- **SG-5** — chaque rapport porte `manifeste @ commit` ; provenance non traçable ⇒ `⛔`.
