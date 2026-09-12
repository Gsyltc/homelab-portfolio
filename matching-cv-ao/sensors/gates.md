# Verification gates — contrôle de traçabilité aux frontières de phases

Manifeste déclaratif des **verification gates** du workflow Matching AO ↔ CV. **Advisory** : produit un rapport, ne bloque jamais le gate humain.

À chaque **frontière de phase**, en amont de la validation humaine, contrôles déterministes :

1. **`artefacts-presents`** — les artefacts requis en sortie de phase existent.
2. **`liaison-tracabilite`** — chaque exigence AO est reliée à un profil analysé.
3. **`absence-orphelin`** — aucun profil n'est déconnecté (sans exigence amont).
4. **`disponibilite-complete`** — chaque profil CV porte une disponibilité complète (date de disponibilité + taux d'utilisation en %), champs **mandatory** — voir [`disponibilite.md`](disponibilite.md).
5. **`equivalence-mifi`** — chaque profil CV porte un objet `mifi` cohérent (4 états d'`equivalence_requise` ; `niveau_equivalent_qc` non vide si `oui`/`non_requise`) ; les collaborateurs en `a_verifier` sont signalés (MIFI non tranché) — voir [`equivalence-mifi.md`](equivalence-mifi.md).

## Frontières et artefacts requis

```yaml
type: verification-gates
nature: advisory
origine: AUQU-6
boundaries:
  - id: initialisation-analyse
    frontiere: "Initialisation → Analyse"
    artefacts_requis:
      - ao-pdf-received
      - cv-available
    checks: [artefacts-presents]

  - id: analyse-matching
    frontiere: "Analyse → Matching"
    artefacts_requis:
      - ao-exigences
      - ao-profils-recherches
      - cv-profils
    checks: [artefacts-presents, liaison-tracabilite, disponibilite-complete, equivalence-mifi]

  - id: matching-validation
    frontiere: "Matching → Validation"
    artefacts_requis:
      - classement-final
    checks: [artefacts-presents, liaison-tracabilite, absence-orphelin]

  - id: validation-cloture
    frontiere: "Validation → Clôture"
    artefacts_requis:
      - resultats-valides
    checks: [artefacts-presents]
```

## En cas d'écart (advisory)

- Le coordinateur **ne bloque pas** : il **signale l'écart** dans le « Rapport de vérification » sur l'issue et **propose de revenir corriger** avant de présenter le contenu à l'humain.
- L'humain reste seul décideur : demander la correction, ou valider en connaissance de cause en actant l'écart sur l'issue.

## Rapport de gate (piste d'audit)

Posté en commentaire sur l'issue, avant la validation humaine. Verdicts : `✅` conforme · `⚠️` écart · `⛔` indisponible.

```
Rapport de vérification — <frontière>   (source : matching-cv-ao/sensors/gates.md)
- artefacts-presents : ✅ | ⚠️ <artefact manquant> | ⛔ <indisponible>
- liaison-tracabilite : ✅ | ⚠️ <exigence sans profil> | ⛔ <indisponible>
- absence-orphelin : ✅ | ⚠️ <profil orphelin> | ⛔ <indisponible>
- disponibilite-complete : ✅ | ⚠️ <profil sans disponibilité complète> | ⛔ <indisponible>   (frontière Analyse → Matching ; détail : matching-cv-ao/sensors/disponibilite.md)
- equivalence-mifi : ✅ | ⚠️ <profil sans objet mifi cohérent / en a_verifier> | ⛔ <indisponible>   (frontière Analyse → Matching ; détail : matching-cv-ao/sensors/equivalence-mifi.md)
```

À la frontière **Analyse → Matching**, le check `disponibilite-complete` est reporté (détail dans `sensors/disponibilite.md`) :

```
Rapport de vérification — Analyse → Matching   (source : matching-cv-ao/sensors/gates.md)
- artefacts-presents : ✅ | ⚠️ <artefact manquant> | ⛔ <indisponible>
- liaison-tracabilite : ✅ | ⚠️ <exigence sans profil> | ⛔ <indisponible>
- disponibilite-complete : ✅ | ⚠️ <collaborateur sans date_disponibilite / taux_utilisation> | ⛔ <indisponible>
- equivalence-mifi : ✅ | ⚠️ <collaborateur sans objet mifi cohérent / en a_verifier (MIFI non tranché)> | ⛔ <indisponible>   (détail : matching-cv-ao/sensors/equivalence-mifi.md)
```
