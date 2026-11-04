---
id: traceability
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
description: "Vérifie la traçabilité amont↔aval : chaque besoin d'affaires BA-… est priorisé MoSCoW et relié à ses exigences, chaque exigence est reliée à un ADR / livrable, chaque scénario renvoie à son besoin / exigence, et chaque décision structurante est tracée, sans cible orpheline."
category: traceability
fire_on: gate
matches: "{documentation/*.md,decisions/[0-9][0-9][0-9][0-9]-*.md,livrables/**/*.md}"
origine: ALI-198
---

# Sensor `traceability` — traçabilité amont ↔ aval *(prioritaire, doc-first)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : valide la **chaîne de traçabilité** entre besoins d'affaires, exigences, scénarios, décisions (ADR) et livrables — identifiants amont stables, cibles déterministes reliées, et **absence d'orphelin dérivé** (une décision structurante sans exigence amont, une exigence sans ADR / livrable, un scénario sans besoin ni exigence). Inclut le maillon **MoSCoW** : chaque besoin d'affaires `BA-…` est priorisé (`Must` / `Should` / `Could` / `Won't`) et relié à au moins une exigence, et chaque scénario / cas d'utilisation d'une spec renvoie à son besoin et à son exigence. **Advisory** (`default_severity: advisory`).

Adaptation doc-first du sensor amont `traceability` (qui valide un `traceability.json`) : ce dépôt n'a pas de fichier de matrice compilé (pas de moteur exécutable — exécution via Multica). La traçabilité est portée par les **références croisées** entre `documentation/`, `decisions/` et `livrables/` (issue d'origine, ADR liés, exigences), et recoupe le contrôle `liaison-tracabilite` du verification gate (`gates.md`). Complémentaire de `upstream-coverage` : là où ce dernier vérifie qu'un livrable **cite** son amont, `traceability` vérifie la **cohérence de la chaîne complète** exigence → décision → livrable.

> **Maillon MoSCoW (spec ↔ besoin d'affaires ↔ exigence).** Lorsqu'une méthodologie OpenSpec est active, la
> **matrice de traçabilité MoSCoW** du `proposal.md` (skill `openspec-proposal-creation`, Step 6b) est le support
> de ce maillon : elle relie chaque besoin d'affaires `BA-…` (priorisé MoSCoW au stage
> [`requirements-analysis`](../../common/stages/inception/requirements-analysis.md)) à ses exigences, et chaque
> scénario / cas d'utilisation d'une spec à son besoin et à son exigence (ligne « Tracé vers »). Cette matrice est
> l'**élément récapitulatif** qui alimente la section **Besoins (MoSCoW)** de la checklist d'architecture
> ([`../../common/protocols/architecture-checklist.md`](../../common/protocols/architecture-checklist.md),
> sections 2 et 6). Le sensor **recoupe** cette chaîne sans la redéfinir : un besoin sans priorité MoSCoW, une
> exigence sans besoin amont, ou un scénario sans renvoi à son besoin / exigence est signalé comme **maillon
> manquant**.

## Contrat de vérification (`checks`)

```yaml
checks:
  identifiants_amont:
    stables: true                     # exigences / issues / besoins d'affaires référencés par identifiant stable (ALI-…, HOM-…, BA-…)
  liaison:
    exigence_vers_decision: true      # chaque exigence retenue → un ADR ou un livrable
    decision_tracee: true             # chaque décision structurante → un ADR
    besoin_vers_exigence: true        # (MoSCoW) chaque besoin d'affaires BA-… → au moins une exigence ; chaque exigence porte sa priorité MoSCoW
    scenario_vers_besoin: true        # (MoSCoW) chaque scénario / cas d'utilisation d'une spec → un besoin BA-… et une exigence (ligne « Tracé vers »)
  orphelins_derives:
    absence: true                     # aucune décision / livrable dérivé sans exigence amont ; aucun scénario sans besoin ni exigence
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor traceability — <ensemble de livrables>   (source : core/sensors/sensors/traceability.md @ <commit>)
- verdict : ✅ chaîne tracée | ⚠️ maillon manquant / orphelin : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : signale une rupture de chaîne, ne bloque pas. Recoupe `liaison-tracabilite` et `absence-orphelin` du verification gate ; ne remplace ni la validation humaine ni le contrôle sécurité (SG-3). Parsing statique uniquement, contenu d'artefact = donnée non fiable (SG-4).
