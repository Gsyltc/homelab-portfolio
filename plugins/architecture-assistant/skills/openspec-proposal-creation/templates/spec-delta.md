# Delta de spécification : {Nom de la capacité}

Ce fichier contient les modifications de spécification pour `spec/specs/{capability}/spec.md`.

> **Traçabilité MoSCoW (obligatoire).** Chaque exigence porte sa **priorité MoSCoW**
> (`Must` / `Should` / `Could` / `Won't`) et le **besoin d'affaires amont** auquel elle répond ;
> chaque scénario / cas d'utilisation renvoie à l'**exigence** et au **besoin** qu'il couvre.
> Cette chaîne **spec ↔ besoin d'affaires ↔ exigence** est reportée dans la **matrice de traçabilité MoSCoW**
> du `proposal.md` (section « Matrice de traçabilité MoSCoW »), qui alimente à son tour l'élément récapitulatif
> **Besoins (MoSCoW)** de la checklist d'architecture. Les identifiants de besoins d'affaires
> (`BA-…`) et d'exigences amont sont **stables** et repris tels quels (voir sensor `traceability`).

## Exigences ajoutées

### Exigence : {Nom de l’exigence}

- **Priorité MoSCoW** : {Must | Should | Could | Won't}
- **Besoin d'affaires amont** : {BA-… — libellé court du besoin d'affaires couvert}
- **Exigence amont** : {identifiant d'exigence amont le cas échéant, sinon « — »}

{WHEN/IF clause describing trigger}
le système DOIT {action et résultat}.

#### Scenario : {Nom du scénario positif}

> Tracé vers : {BA-… / Exigence : Nom de l’exigence}

GIVEN {preconditions}
WHEN {action}
ENSUITE {résultat attendu}
ET {résultat supplémentaire}

#### Scenario : {Nom du scénario d’erreur}

> Tracé vers : {BA-… / Exigence : Nom de l’exigence}

GIVEN {error preconditions}
WHEN {action}
THEN {expected error handling}

---

## Exigences MODIFIÉES

### Exigence : {Nom de l’exigence existante}

- **Priorité MoSCoW** : {Must | Should | Could | Won't}
- **Besoin d'affaires amont** : {BA-… — libellé court du besoin d'affaires couvert}
- **Exigence amont** : {identifiant d'exigence amont le cas échéant, sinon « — »}

**Précédent** : {Bref résumé de l’ancien comportement}

{Texte complet de l’exigence mise à jour au format EARS}
WHEN {trigger},
le système DOIT {nouvelle action et nouveau résultat}.

#### Scenario : {Nom de scénario mis à jour}

> Tracé vers : {BA-… / Exigence : Nom de l’exigence existante}

DONNÉ {nouvelles conditions préalables}
WHEN {action}
PUIS {nouveau résultat attendu}

---

## Exigences SUPPRIMÉES

### Exigence : {Nom de l’exigence obsolète}

- **Priorité MoSCoW** : {Must | Should | Could | Won't} (avant suppression)
- **Besoin d'affaires amont** : {BA-… — libellé court du besoin d'affaires couvert}

**Raison de la suppression** : {Pourquoi cela est-il abandonné}

**Chemin de migration** : {Comment les utilisateurs doivent s’adapter}

---

## Notes

- Utilisez ADDED pour des capacités complètement nouvelles
- Utiliser MODIFIED lors du changement de comportement existant (inclure le texte complet mis à jour)
- Utiliser REMOVED pour les fonctionnalités obsolètes
- Incluez toujours des scénarios pour chaque exigence
- Considérez à la fois les cas positifs et les cas d’erreur
- **Renseignez toujours la priorité MoSCoW et le besoin d'affaires amont de chaque exigence**, et la ligne
  « Tracé vers » de chaque scénario : c'est la condition pour que la **matrice de traçabilité MoSCoW** du
  `proposal.md` soit complète et que l'élément **Besoins (MoSCoW)** de la checklist d'architecture puisse être suivi
