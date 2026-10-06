---
name: create-architectural-decision-record
description: "Créer un document ADR (Architectural Decision Record) pour une documentation de décision optimisée pour l'IA."
---

# Créer un Architectural Decision Record

Créer un document ADR pour `${input:DecisionTitle}` en utilisant un format structuré optimisé pour la consommation par l'IA et la lisibilité humaine.

## Entrées

- **Contexte** : `${input:Context}`
- **Décision** : `${input:Decision}`
- **Alternatives** : `${input:Alternatives}`
- **Parties prenantes** : `${input:Stakeholders}`
- **Auteurs** : `${input:Authors}`

## Validation des entrées
Si l'une des entrées requises n'est pas fournie ou ne peut pas être déterminée à partir de l'historique de la conversation, demandez à l'utilisateur de fournir les informations manquantes avant de procéder à la génération de l'ADR.

## Exigences

- Utiliser un langage précis et sans ambiguïté
- Respecter le format ADR standardisé avec front matter
- Inclure à la fois les conséquences positives et négatives
- Documenter les alternatives avec la justification de leur rejet
- Structurer pour l'analyse automatique (machine) et la consultation humaine
- Utiliser des puces codées (codes de 3-4 lettres + numéros à 3 chiffres) pour les sections à éléments multiples
- **Jamais de référence au workflow.** L'ADR documente une décision d'architecture **produit**, pas le processus qui l'a produite. Ne jamais mentionner, dans aucune section ni le front matter, un élément du workflow qui a généré l'ADR : noms ou rôles d'agents (Architecte de solution, Reviewer de sécurité, OpenSpec Expert, coordinateur…), stages ou phases (ideation, inception, construction, cadrage, découpage…), sensors, gates, scopes, protocoles, statuts d'issue Multica (`in_progress`, `ADR Proposée`, `cancelled`…), branches git du workflow, ou tout autre artefact de pilotage. L'ADR se lit seule, par un lecteur qui ignore tout du workflow. Seul le champ `## Status` de l'ADR (valeur en anglais) décrit l'état de la décision — il ne fait pas référence au workflow.
- **Concision stricte — prose au minimum.** Les sections **Décision**, **Conséquences** et **Alternatives étudiées** doivent être **claires et immédiatement compréhensibles**, avec la prose réduite au strict minimum nécessaire à la compréhension. Préférer les puces courtes aux paragraphes ; une idée par puce ; pas de redite, pas de remplissage, pas de contexte déjà couvert ailleurs. Chaque conséquence et chaque alternative tient en une à deux phrases factuelles ; la Décision énonce le choix et sa justification sans développement superflu.
- **Langue par défaut : le français.** La documentation ADR doit être rédigée en français par défaut, sauf demande explicite contraire de l'utilisateur
- **Statuts en anglais.** Les valeurs de statut (front matter et section Status) restent en anglais (`Proposed`, `Accepted`, `Rejected`, `Superseded`, `Deprecated`) pour rester compatibles avec des outils d'architecture tels que Structurizr
- **Titre de section Status en anglais.** Le titre de la section statut doit être `Status` (en anglais) et non `Statut`, pour la compatibilité avec des outils tels que Structurizr
- **Statut unique.** La section Status ne doit pas lister toutes les valeurs possibles : ne conserver que le statut retenu
- **Date de création obligatoire.** Immédiatement **sous la section `## Status`**, l'ADR porte une section `## Date de création` renseignée avec la date de création de l'ADR au format **`YYYY-MM-DD`** (ex. `2026-10-06`). Cette date est fixée à la création du document et n'est pas modifiée ensuite (distincte de « accepté le » du front matter, qui est la date d'acceptation par le client).
- **Auteurs : toujours déduits de l'architecte de solution (humain) du projet.** L'auteur par défaut d'une ADR est le **nom réel de l'humain tenant le rôle « Architecte de solution » du projet**. Le déterminer **systématiquement dans cet ordre**, sans solliciter l'humain tant qu'une source répond :
  1. **README du projet** — section `## Équipe`, ligne « Architecte de solution : <nom> » (voir [Métadonnées du projet](../project-defaults/SKILL.md) de la skill `project-defaults`, source unique de vérité) ;
  2. **sinon** l'arrimage du document `001-document-architecture-solution.md` — matrice RACI, rôle « Architecte de solution », colonne « Nom » (voir aussi la règle « Noms de responsables » dans [`core/rules/workspace.md`](../../../../core/rules/workspace.md)).

  **Ne demander le ou les noms des auteurs à l'humain que si l'information est absente des deux sources** (README sans l'entrée « Architecte de solution » *et* arrimage `001` vide ou DAS absente). **Ne jamais mettre le nom d'un agent dans les auteurs.** Un auteur supplémentaire explicitement fourni par l'humain complète ou remplace ce défaut.
- **Pas d'issues en référence.** Ne jamais ajouter d'issues (tickets) dans la section Références
- **Liens markdown.** Toute référence à d'autres ADR ou à la documentation du projet doit utiliser le format de lien markdown `[texte](chemin)`
- **URL pour les liens externes.** Toute référence à un lien externe (internet) doit inclure l'URL complète, au format `[texte](https://...)`
- Par défaut, le nom du client et la date d'acceptation doivent restée vide. Si une instruction indique que le client a accepté l'ADR, renseigne le nom du client et la date de l'acceptation.

L'ADR doit être enregistré dans le répertoire des adrs du projet `decisions/` en respectant la convention de nommage : `NNNN-titre.md`, où NNNN est le numéro séquentiel à 4 chiffres (en partant de 0001) suivi du slug du titre (par ex. `0001-database-selection.md`).

## Structure de documentation requise

Le fichier de documentation doit suivre le modèle ci-dessous, en veillant à ce que toutes les sections soient correctement renseignées. Le front matter du markdown doit être structuré correctement comme dans l'exemple suivant :

```md
# [Titre de la décision]

---
auteurs: [Par défaut l'architecte de solution (humain) du projet — déduit du README `## Équipe` puis, à défaut, de l'arrimage RACI « Nom » du `001` ; sinon noms fournis par l'humain]  
accepté par : [Nom du client ayant accepté l'ADR]  
accepté le : [Date de l'acceptation par le client]  
supersedes: ""  
superseded_by: ""  

---

## Status

Proposed

## Date de création

YYYY-MM-DD

## Contexte

[Énoncé du problème, contraintes techniques, exigences métier et facteurs environnementaux qui motivent cette décision.]

## Décision

[Solution retenue + justification du choix, en une à trois phrases. Prose au strict minimum : énoncer le choix et pourquoi, sans développement superflu. Structuré le texte avec des éléments de styles si cela aide à la clarté du texte (exemple: Puces et numéros, paragraphe, et autre éléments de style)]

## Conséquences

<!-- Une conséquence par puce, une à deux phrases factuelles. Pas de prose de liaison. -->

### Positives

- **POS-001** : [Résultat bénéfique ou avantage]
- **POS-002** : [Gain de performance, maintenabilité ou scalabilité]
- **POS-003** : [Alignement avec les principes d'architecture]

### Négatives

- **NEG-001** : [Compromis, limitation ou inconvénient]
- **NEG-002** : [Dette technique ou complexité introduite]
- **NEG-003** : [Risque ou défi futur]

## Alternatives étudiées

<!-- Chaque alternative : description et raison du rejet en une à deux phrases chacune. -->

### ALT-001 - [Nom de l'alternative 1]

[Brève description technique]

**Raison du rejet** : [Pourquoi cette option n'a pas été retenue]

### ALT-002 - [Nom de l'alternative 2]

[Brève description technique]

**Raison du rejet** : [Pourquoi cette option n'a pas été retenue]

## Notes d'implémentation

- **IMP-001** : [Considérations clés d'implémentation]
- **IMP-002** : [Stratégie de migration ou de déploiement, le cas échéant]
- **IMP-003** : [Critères de suivi et de réussite]

## Références

- **REF-001** : [ADR associé] au format lien markdown, par ex. `[ADR-0001 - Sélection de la base de données](0001-database-selection.md)`
- **REF-002** : [Documentation externe] au format lien markdown avec l'URL complète, par ex. `[Documentation PostgreSQL](https://www.postgresql.org/docs/)`
- **REF-003** : [Norme ou cadre de référence] au format lien markdown avec l'URL complète, par ex. `[ADR Template de Michael Nygard](https://github.com/joelparkerhenderson/architecture-decision-record)`
```
