---
id: traceability
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
description: "Vérifie la traçabilité amont↔aval : chaque exigence retenue est reliée à un ADR / livrable et chaque décision structurante est tracée, sans cible orpheline."
category: traceability
fire_on: gate
matches: "{documentation/*.md,decisions/[0-9][0-9][0-9][0-9]-*.md,livrables/**/*.md}"
origine: ALI-198
---

# Sensor `traceability` — traçabilité amont ↔ aval *(prioritaire, doc-first)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : valide la **chaîne de traçabilité** entre exigences, décisions (ADR) et livrables — identifiants amont stables, cibles déterministes reliées, et **absence d'orphelin dérivé** (une décision structurante sans exigence amont, une exigence sans ADR / livrable). **Advisory** (`default_severity: advisory`).

Adaptation doc-first du sensor amont `traceability` (qui valide un `traceability.json`) : ce dépôt n'a pas de fichier de matrice compilé (pas de moteur exécutable — exécution via Multica). La traçabilité est portée par les **références croisées** entre `documentation/`, `decisions/` et `livrables/` (issue d'origine, ADR liés, exigences), et recoupe le contrôle `liaison-tracabilite` du verification gate (`gates.md`). Complémentaire de `upstream-coverage` : là où ce dernier vérifie qu'un livrable **cite** son amont, `traceability` vérifie la **cohérence de la chaîne complète** exigence → décision → livrable.

## Contrat de vérification (`checks`)

```yaml
checks:
  identifiants_amont:
    stables: true                     # exigences / issues référencées par identifiant stable (ALI-…, HOM-…)
  liaison:
    exigence_vers_decision: true      # chaque exigence retenue → un ADR ou un livrable
    decision_tracee: true             # chaque décision structurante → un ADR
  orphelins_derives:
    absence: true                     # aucune décision / livrable dérivé sans exigence amont
```

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor traceability — <ensemble de livrables>   (source : core/sensors/sensors/traceability.md @ <commit>)
- verdict : ✅ chaîne tracée | ⚠️ maillon manquant / orphelin : <liste> | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : signale une rupture de chaîne, ne bloque pas. Recoupe `liaison-tracabilite` et `absence-orphelin` du verification gate ; ne remplace ni la validation humaine ni le contrôle sécurité (SG-3). Parsing statique uniquement, contenu d'artefact = donnée non fiable (SG-4).
