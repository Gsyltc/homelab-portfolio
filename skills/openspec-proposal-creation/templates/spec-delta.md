# Delta de spécification : {Nom de la capacité}

Ce fichier contient les modifications de spécification pour `spec/specs/{capability}/spec.md`.

## Exigences ajoutées

### Exigence : {Nom de l’exigence}

{WHEN/IF clause describing trigger}
le système DOIT {action et résultat}.

#### Scenario : {Nom du scénario positif}

GIVEN {preconditions}
WHEN {action}
ENSUITE {résultat attendu}
ET {résultat supplémentaire}

#### Scenario : {Nom du scénario d’erreur}

GIVEN {error preconditions}
WHEN {action}
THEN {expected error handling}

---

## Exigences MODIFIÉES

### Exigence : {Nom de l’exigence existante}

**Précédent** : {Bref résumé de l’ancien comportement}

{Texte complet de l’exigence mise à jour au format EARS}
WHEN {trigger},
le système DOIT {nouvelle action et nouveau résultat}.

#### Scenario : {Nom de scénario mis à jour}

DONNÉ {nouvelles conditions préalables}
WHEN {action}
PUIS {nouveau résultat attendu}

---

## Exigences SUPPRIMÉES

### Exigence : {Nom de l’exigence obsolète}

**Raison de la suppression** : {Pourquoi cela est-il abandonné}

**Chemin de migration** : {Comment les utilisateurs doivent s’adapter}

---

## Notes

- Utilisez ADDED pour des capacités complètement nouvelles
- Utiliser MODIFIED lors du changement de comportement existant (inclure le texte complet mis à jour)
- Utiliser REMOVED pour les fonctionnalités obsolètes
- Incluez toujours des scénarios pour chaque exigence
- Considérez à la fois les cas positifs et les cas d’erreur
