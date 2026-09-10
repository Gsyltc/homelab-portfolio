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

Check déterministe déclenché **au gate de phase** (`fire_on: gate`) : vérifie que le document **Cycle de vie des données** (`documentation/10-cycle_vie_donnees.md`) est **présent** et **correctement renseigné** — sections obligatoires présentes et non vides, et **couverture effective des données du projet** (au moins une donnée / catégorie de données du projet classifiée et rattachée à une étape de cycle de vie). **Advisory** (`default_severity: advisory`) : il factualise l'état du document, mais **ne bloque jamais** — ni le gate humain, ni la validation de Manuel.

> **Un signal advisory, lu par deux acteurs (jamais bloquant)** :
> - **Manuel (Architecte de solution), valideur du livrable données** — le signal `data-lifecycle` **assiste** la revue Manuel → Diego : il factualise la présence et le renseignement du document, mais **ne conditionne pas** la validation. Manuel reste seul juge — il peut demander une correction à Diego sur la base d'un `⚠️` / `⛔`, ou valider en connaissance de cause en actant l'écart sur l'issue. Le sensor n'oppose aucun blocage automatique (voir [`solution-architect-agent`](../../agents/solution-architect-agent.md) et [`data-architect-agent`](../../agents/data-architect-agent.md)).
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

`required-sections` porte déjà `10-cycle_vie_donnees.md` dans ses fichiers mandatory (sections « Gouvernance de données » / « Classification des données »). `data-lifecycle` est **complémentaire** : il **spécialise** le contrôle sur ce document (ajout de la section « Cycle de vie des données » et de la **couverture effective des données du projet**), et **assiste** la revue Manuel → Diego sans jamais la bloquer. Toute évolution du gabarit `gabarits/10` doit être répercutée ici **et** dans `required-sections` dans la même PR (SG-1 / SG-6).

## Sortie (piste d'audit)

Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible (SG-2, jamais lu comme conforme). Source tracée (SG-5).

```
Sensor data-lifecycle — documentation/10-cycle_vie_donnees.md   (source : core/sensors/sensors/data-lifecycle.md @ <commit>)
- verdict : ✅ présent et renseigné (données projet classifiées + rattachées au cycle) | ⚠️ fichier absent | ⚠️ sections manquantes/vides : <liste> | ⚠️ aucune donnée projet classifiée/rattachée (gabarit non renseigné) | ⛔ indisponible : <motif>
```

## Garde-fou

Advisory : n'empêche pas l'écriture d'un artefact et **ne bloque jamais** — ni le gate humain côté coordinateur (Sylvain), ni la validation de Manuel dans la revue A2A Manuel → Diego, où il ne fait qu'**assister** le jugement. Un signal au vert ne vaut pas validation ; un écart n'oppose aucun blocage automatique. Le passage du sensor à `blocking` resterait une décision structurante (ADR + contrôle sécurité, Architecte cybersécurité) — hors de ce manifeste.
