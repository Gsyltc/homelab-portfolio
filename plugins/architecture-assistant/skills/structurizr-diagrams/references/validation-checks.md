# Contrôles de validation Structurizr

## 1) Aucune référence dans les libellés rendus
Interdits dans les noms/descriptions/titres/libellés de relations/titres/descriptions de vues :
- `INV-`, `CT-`, `CTR-SEC-`, `PINV-`, `RAT-`, `PLG-`, `IMP-`, `R-SEC-`
- Numéros de paragraphe `§...`

**Vérification (post-export JSON/texte) :**
```bash
grep -nE "(INV-[0-9]|CT-[0-9]|CTR-SEC-|PINV-|RAT-|PLG-|IMP-|R-SEC-|§[0-9])" export.json
```
Si trouvé → déplacer vers commentaires DSL (`// ...`), DAS ou ADR.

## 2) Un seul lien par sens entre deux éléments (vues statiques)
Pour vues conteneur/composant, consolider les interactions multiples dans le même sens en un lien unique au libellé synthétique.
**Exception** : vue dynamique (séquence) peut avoir plusieurs occurrences du même couple en étapes numérotées.

**Vérification conceptuelle :**
Extraire paires `(sourceId -> destinationId)` depuis les relations des vues statiques, trier, `uniq -d` pour repérer doublons.

## Validation CLI
```bash
# Local
structurizr.sh validate -workspace workspace.dsl

# Docker (si CLI locale indisponible/incompatible)
docker run --rm -v "$(pwd)":/usr/local/structurizr structurizr/cli:latest validate -w workspace.dsl
```
Toujours `validate` puis `export json` avant commit.
