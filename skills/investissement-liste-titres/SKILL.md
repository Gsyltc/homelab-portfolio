---
name: titre-liste
description: "Liste des titres détenus et des titres suivis (titres.md) partagée par tous les agents de l'équipe d'analyse financière (Hector, Nestor, Victor, Leo). Utiliser pour connaître les titres à analyser, leurs identifiants marché, le type de compte associé (REER, CELI, Marge) et les titres suivis pour opportunités sur le compte marge."
user-invocable: false
allowed-tools: Bash(multica *)
---

# Liste des titres détenus et suivis

Cette skill contient la liste des titres de l'investisseur, dans le fichier `titres.md`. Le fichier comporte **deux sections** :

## Section 1 — Titres détenus

Les titres actuellement en portefeuille. Un titre par ligne au format :
`TICKER | Nom de l'entreprise | Type (Action/FNB) | Compte (REER/CELI/Marge)`

Exemple :

```
ENB.TO | Enbridge Inc | Action | CELI et Compte sur marge
XIC.TO | iShares Core S&P/TSX Capped Composite Index ETF | FNB | REER
```

- `TICKER` : identifiant boursier sur le marché canadien (TSX), avec le suffixe `.TO` le cas échéant.
- `Type` : `Action` ou `FNB`.
- `Compte` : type(s) de compte dans lequel le titre est détenu — `REER`, `CELI` et/ou `Compte sur marge` (plusieurs comptes séparés par « et »).

## Section 2 — Titres suivis (liste de surveillance)

Titres non détenus mais **surveillés en vue d'une prise de position sur le compte sur marge** pour réaliser des gains. Un titre par ligne au format :
`TICKER | Nom de l'entreprise`

Exemple :

```
CM.TO | Canadian Imperial Bank of Commerce
```

Ces titres doivent être analysés comme des **candidats à l'achat pour le compte marge** : opportunité de gain court terme (trading de journée, cible ~25 $/jour), liquidité, volatilité, momentum, niveaux d'entrée/sortie et risques.

## Règles d'utilisation

- **Lire `titres.md` avant toute analyse ou collecte.** C'est la liste de référence unique.
- Analyser UNIQUEMENT les titres présents dans `titres.md`. Ne jamais en inventer ou en ajouter.
- Les **titres détenus** font l'objet d'une analyse de portefeuille adaptée au compte.
- Les **titres suivis** font l'objet d'une analyse d'opportunité pour le compte marge.
- Le fichier peut évoluer : à chaque nouvelle tâche, relire la version courante.

## Profils d'objectifs par compte (pour adapter les recommandations)

| Compte    | Objectifs de l'investisseur                       |
| --------- | ------------------------------------------------- |
| **REER**  | Bons dividendes + réduction d'impôts              |
| **CELI**  | Hauts dividendes, à l'abri de l'impôt             |
| **Marge** | Trading de journée, cible ~25 $ de gains par jour |

## Mise à jour

- La liste est mise à jour manuellement par l'humain. Les agents n'y ajoutent jamais de titre sans demande explicite.
- Si `titres.md` est vide ou absent, signaler à Hector qu'aucune liste de titres n'est encore disponible.
