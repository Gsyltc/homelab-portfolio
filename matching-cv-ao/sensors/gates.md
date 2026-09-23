# Verification gates — contrôle de traçabilité aux frontières de phases

Manifeste déclaratif des **verification gates** du workflow Matching AO ↔ CV. **Advisory** : produit un rapport, ne bloque jamais le gate humain.

À chaque **frontière de phase**, en amont de la validation humaine, contrôles déterministes :

1. **`artefacts-presents`** — les artefacts requis en sortie de phase existent.
2. **`liaison-tracabilite`** — chaque exigence AO est reliée à un profil analysé.
3. **`absence-orphelin`** — aucun profil n'est déconnecté (sans exigence amont).
4. **`disponibilite-complete`** — chaque profil CV porte une disponibilité complète (date de disponibilité + taux d'utilisation en %), champs **mandatory** — voir `disponibilite.md`.
5. **`equivalence-mifi`** — chaque profil CV porte un objet `mifi` cohérent (4 états d'`equivalence_requise` ; `niveau_equivalent_qc` non vide si `oui`/`non_requise`) ; les collaborateurs en `a_verifier` sont signalés (MIFI non tranché) — voir `equivalence-mifi.md`.
6. **`localisation-complete`** — chaque profil CV porte une ville (`localisation.ville`), champ **mandatory** ; les villes manquantes sont signalées (mention humaine attendue) — voir `localisation.md`.
7. **`expertise-firme`** — lorsque l'AO exige une expertise de firme, l'objet `expertise_firme` est présent et sa couverture est **appuyée sur le référentiel `${ROOT_DIRECTORY}/clients/*.json`** ; un `verdict` ≠ `conforme` est signalé et déclenche une **gate humaine légère** (non bloquante) — voir `expertise-firme.md`.

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
    artefacts_optionnels:
      - ao-expertise-firme
      - clients-contextes
    checks: [artefacts-presents, liaison-tracabilite, disponibilite-complete, equivalence-mifi, localisation-complete, expertise-firme]

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

- Le coordinateur **ne bloque pas** : il consigne l'écart dans le **« Rapport de vérification » joint en JSON** (voir ci-dessous) et **propose de revenir corriger** avant de présenter le contenu à l'humain.
- **Seul un écart nécessitant l'humain** est reformulé en Markdown : une **mention de l'humain + l'action** à effectuer, sans recopier le rapport. Sinon, le commentaire se limite à référencer l'artefact JSON joint.
- L'humain reste seul décideur : demander la correction, ou valider en connaissance de cause en actant l'écart sur l'issue.

## Rapport de gate (piste d'audit — artefact JSON joint)

Le « Rapport de vérification » est un **artefact JSON joint à l'issue** (type `rapport-verification` du **message A2A** — schéma défini une seule fois dans `governance-security`, **non redéfini ici**), posté avant la validation humaine. Il porte les **verdicts structurés** par check : `ok` (✅ conforme) · `ecart` (⚠️ écart) · `indisponible` (⛔). Structure des verdicts (dans le champ `resultat`/`verdicts` du message A2A) :

```json
{
  "type": "rapport-verification",
  "stage": "<frontière, ex. analyse-matching>",
  "verdicts": [
    { "check": "artefacts-presents", "statut": "ok | ecart | indisponible", "detail": "<artefact manquant si écart>" },
    { "check": "liaison-tracabilite", "statut": "ok | ecart | indisponible", "detail": "<exigence sans profil si écart>" },
    { "check": "absence-orphelin", "statut": "ok | ecart | indisponible", "detail": "<profil orphelin si écart>" },
    { "check": "disponibilite-complete", "statut": "ok | ecart | indisponible", "detail": "<collaborateur sans date_disponibilite / taux_utilisation> (frontière Analyse → Matching ; détail : matching-cv-ao/sensors/disponibilite.md)" },
    { "check": "equivalence-mifi", "statut": "ok | ecart | indisponible", "detail": "<collaborateur sans objet mifi cohérent / en a_verifier> (frontière Analyse → Matching ; détail : matching-cv-ao/sensors/equivalence-mifi.md)" },
    { "check": "localisation-complete", "statut": "ok | ecart | indisponible", "detail": "<collaborateur sans ville (localisation.ville) — mention humaine attendue> (frontière Analyse → Matching ; détail : matching-cv-ao/sensors/localisation.md)" },
    { "check": "expertise-firme", "statut": "ok | ecart | indisponible", "detail": "conforme / non exigée | minimums non atteints ou indéterminable (gate humaine légère, non bloquante) (frontière Analyse → Matching ; détail : matching-cv-ao/sensors/expertise-firme.md)" }
  ]
}
```

Seuls les checks pertinents à la frontière considérée sont inclus (voir la carte `boundaries` ci-dessus — à la frontière **Analyse → Matching**, les checks `disponibilite-complete`, `equivalence-mifi`, `localisation-complete`, `expertise-firme` s'ajoutent). La source du rapport (`matching-cv-ao/sensors/gates.md`) est rappelée dans le champ `de`/`reference_audit` du message A2A.
