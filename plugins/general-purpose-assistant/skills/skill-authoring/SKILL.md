---
name: skill-authoring
description: "Créer, modifier et valider une Agent Skill conforme à la norme agentskills.io dans ce dépôt. Utiliser à CHAQUE création ou modification d'une skill (plugins/<plugin>/skills/<skill>/SKILL.md) : définit le frontmatter autorisé, les contraintes de nom et de description, l'organisation scripts/references/assets, et impose la validation via le validateur officiel skills-ref avant livraison. Se déclenche sur : skill, SKILL.md, Agent Skill, créer une skill, modifier une skill, frontmatter, agentskills, validateur skills-ref, conformité skill."
license: MIT
metadata:
  author: Gsyltc
  specification: https://agentskills.io/specification
---

# Créer et modifier une Agent Skill conforme

Toute skill de ce dépôt **doit** respecter la norme [Agent Skills](https://agentskills.io/specification).
Une skill est toujours portée par un **Agent Plugin** (`plugins/<plugin>/skills/<skill>/`).

## Règle d'or

À chaque création **ou** modification d'une skill, valide-la avec le validateur
officiel **avant** de livrer :

```bash
scripts/validate_skills.sh plugins/<plugin>/skills/<skill>
# ou, en direct :
uvx --from skills-ref agentskills validate plugins/<plugin>/skills/<skill>
```

Un commit qui casse la conformité est bloqué par le hook `pre-commit`
(`git config core.hooksPath .githooks`) et par la CI GitHub Actions.

## Emplacement et structure

```
plugins/<plugin>/skills/<skill>/
├── SKILL.md          # requis : frontmatter YAML + instructions Markdown
├── scripts/          # optionnel : code exécutable
├── references/       # optionnel : documentation chargée à la demande
└── assets/           # optionnel : gabarits, images, données
```

- Le **répertoire de la skill** porte le nom canonique : c'est lui qui est
  référencé par les agents (`core/agents/`) et les gabarits. Le champ `name`
  du frontmatter **doit être identique** au nom du répertoire.
- Garde `SKILL.md` sous **500 lignes** ; déporte le détail dans `references/`.

## Frontmatter autorisé (et lui seul)

| Champ           | Requis | Contrainte |
|-----------------|--------|------------|
| `name`          | oui    | 1–64 caractères ; minuscules `a-z`, chiffres `0-9`, tirets ; ne commence/termine pas par `-`, pas de `--` ; **égal au nom du répertoire**. |
| `description`   | oui    | 1–1024 caractères, non vide. Dit **ce que** fait la skill **et quand** l'utiliser ; inclut des mots-clés déclencheurs. |
| `license`       | non    | Nom de licence ou référence à un fichier de licence. |
| `compatibility` | non    | 1–500 caractères ; prérequis d'environnement (produit, paquets, réseau). |
| `metadata`      | non    | Table **clé→valeur de type chaîne**. Range ici tout champ hors norme. |
| `allowed-tools` | non    | Chaîne d'outils pré-approuvés séparés par des espaces (expérimental). |

**Tout autre champ est interdit.** Un champ maison (`user-invocable`,
`keywords`, `agent_created`, …) se place **sous `metadata:`** avec une valeur
en **chaîne** (les booléens deviennent `"true"`/`"false"`, une liste devient
une chaîne séparée par des virgules) :

```yaml
metadata:
  user-invocable: "false"
  keywords: "mot un, mot deux, mot trois"
```

## Rédiger la `description`

C'est le champ qui décide si l'agent active la skill. Voir le guide
[Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions).

- Impératif : « Résume le document », pas « Résumé du document ».
- Deux faces : **ce que** fait la skill **et quand** l'utiliser.
- Ajoute des **déclencheurs** concrets (termes que l'humain emploiera).
- Reste sous 1024 caractères.

```yaml
# Bon
description: "Extrait le texte et les tableaux de fichiers PDF, remplit des formulaires et fusionne des PDF. Utiliser pour tout travail sur des documents PDF ou quand l'humain mentionne PDF, formulaire, extraction."
# Mauvais
description: "Aide avec les PDF."
```

## Corps du `SKILL.md`

Markdown libre, actionnable, une seule préoccupation par skill. Sections
recommandées : instructions pas à pas, exemples d'entrées/sorties, cas limites.
L'agent charge tout le corps à l'activation — déporte le volumineux dans
`references/` et référence-le en **chemin relatif d'un seul niveau**
(`references/REFERENCE.md`, `scripts/extract.py`).

## Checklist avant de livrer

1. `name` = nom du répertoire, format valide.
2. `description` non vide, < 1024 caractères, avec déclencheurs.
3. Aucun champ hors norme (extras sous `metadata:`, valeurs en chaînes).
4. `SKILL.md` < 500 lignes.
5. `scripts/validate_skills.sh plugins/<plugin>/skills/<skill>` passe.
6. Si la skill ajoute un comportement, mettre à jour `CHANGELOG.md`.

## Références

- Spécification : https://agentskills.io/specification
- Bonnes pratiques : https://agentskills.io/skill-creation/best-practices
- Optimiser les descriptions : https://agentskills.io/skill-creation/optimizing-descriptions
- Évaluer une skill : https://agentskills.io/skill-creation/evaluating-skills
- Scripts : https://agentskills.io/skill-creation/using-scripts
