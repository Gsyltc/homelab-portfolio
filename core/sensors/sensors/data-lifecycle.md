---
id: data-lifecycle
kind: deterministic
command: "non-exécutable (advisory documentaire)"
default_severity: advisory
description: "Vérifie que le document Cycle de vie des données (10-cycle_vie_donnees.md) est présent et correctement renseigné (cycle de vie, gouvernance, classification) en fonction des données du projet."
category: document-shape
fire_on: gate
matches: "documentation/10-cycle_vie_donnees.md"
origine: ALI-231
---

# Sensor `data-lifecycle` — cycle de vie des données *(prioritaire)*

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie que le document **Cycle de vie des données** (`documentation/10-cycle_vie_donnees.md`) est **présent** et **correctement renseigné** — sections obligatoires présentes et non vides, et **couverture effective des données du projet** (au moins une donnée / catégorie de données du projet classifiée et rattachée à une étape de cycle de vie). **Advisory** (`default_severity: advisory`) au titre du manifeste.

> **Deux lectures du même signal (par conception, pas par exception)** :
> - **Manuel (Architecte de solution), valideur du livrable données** — le signal `data-lifecycle` est le **critère d'acceptation objectif** de la revue Manuel → Diego : Manuel **ne valide pas** le livrable données tant que le sensor n'est pas `✅`. Un `⚠️` ou `⛔` déclenche une **demande de correction** adressée à Diego (voir [`solution-architect-agent`](../../agents/solution-architect-agent.md) et [`data-architect-agent`](../../agents/data-architect-agent.md)). Cette exigence vaut **au sein du protocole de validation A2A Manuel → Diego** ; elle n'abaisse ni ne remplace la validation humaine granulaire ni le contrôle sécurité (invariants, SG-3).
> - **Sylvain (coordinateur) au verification gate** — le même signal est **advisory et non bloquant** : un écart est **signalé comme alerte à l'humain** dans le « Rapport de vérification », sans jamais bloquer le gate humain.

## Contrat de vérification (`checks`)

```yaml
checks:
  fichier: "documentation/10-cycle_vie_donnees.md"   # présent dans le répertoire documentation/ du projet
  sections:                                          # présentes ET non vides (contenu propre, pas de gabarit/commentaire)
    - "Cycle de vie des données"                     # étapes : collecte → stockage → utilisation → archivage → suppression
    - "Gouvernance de données"                       # rôles/responsabilités, propriété, règles de rétention
    - "Classification des données"                   # niveaux de sensibilité appliqués aux données du projet
  couverture_projet:
    # renseignement « en fonction des données du projet » : au moins une donnée / catégorie
    # du projet est classifiée ET rattachée à une étape du cycle de vie (pas un gabarit vide).
    au_moins_une_donnee_classifiee: true
    au_moins_une_donnee_rattachee_cycle: true
  non_vide: true                                     # une section présente mais vide (aucun contenu propre) = écart
```

## Cohérence avec `required-sections`

`required-sections` porte déjà `10-cycle_vie_donnees.md` dans ses fichiers mandatory (sections « Gouvernance de données » / « Classification des données »). `data-lifecycle` est **complémentaire** : il **spécialise** le contrôle sur ce document (ajout de la section « Cycle de vie des données » et de la **couverture effective des données du projet**), et sert de **critère d'acceptation objectif** de la revue Manuel → Diego. Toute évolution du gabarit `gabarits/10` doit être répercutée ici **et** dans `required-sections` dans la même PR (SG-1 / SG-6).

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor data-lifecycle — documentation/10-cycle_vie_donnees.md   (source : core/sensors/sensors/data-lifecycle.md @ <commit>)
- verdict : ✅ présent et renseigné (données projet classifiées + rattachées au cycle) | ⚠️ fichier absent | ⚠️ sections manquantes/vides : <liste> | ⚠️ aucune donnée projet classifiée/rattachée (gabarit non renseigné) | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory au niveau du manifeste : n'empêche pas l'écriture d'un artefact, et **côté coordinateur (Sylvain) il ne bloque jamais** le gate humain (simple alerte). Le **caractère bloquant** ne vaut **que** comme critère d'acceptation de la revue A2A **Manuel → Diego** (Manuel reste l'agent qui valide). Le passage du sensor à `blocking` au niveau du verification gate global resterait une décision structurante (ADR + contrôle sécurité, Architecte cybersécurité) — hors de ce manifeste.
