---
name: create-architectural-decision-record
description: "Créer un document de décision structurante (Architectural Decision Record) pour une documentation de décision optimisée pour l'IA."
---

# Créer un Architectural Decision Record

Créer un document de décision structurante pour `${input:DecisionTitle}` en utilisant un format structuré optimisé pour la consommation par l'IA et la lisibilité humaine.

## Entrées

- **Contexte** : `${input:Context}`
- **Décision** : `${input:Decision}`
- **Alternatives** : `${input:Alternatives}`
- **Parties prenantes** : `${input:Stakeholders}`
- **Auteurs** : `${input:Authors}`

## Validation des entrées
Si l'une des entrées requises n'est pas fournie ou ne peut pas être déterminée à partir de l'historique de la conversation, demandez à l'utilisateur de fournir les informations manquantes avant de procéder à la génération de la décision structurante.

## Exigences

- Utiliser un langage précis et sans ambiguïté
- Respecter le format de décision structurante standardisé avec front matter
- Inclure à la fois les conséquences positives et négatives
- Documenter les alternatives avec la justification de leur rejet
- Structurer pour l'analyse automatique (machine) et la consultation humaine
- Utiliser des puces codées (codes de 3-4 lettres + numéros à 3 chiffres) pour les sections à éléments multiples
- **Langue par défaut : le français.** La documentation de décision structurante doit être rédigée en français par défaut, sauf demande explicite contraire de l'utilisateur
- **Statuts en anglais.** Les valeurs de statut (front matter et section Status) restent en anglais (`Proposed`, `Accepted`, `Rejected`, `Superseded`, `Deprecated`) pour rester compatibles avec des outils d'architecture tels que Structurizr
- **Titre de section Status en anglais.** Le titre de la section statut doit être `Status` (en anglais) et non `Statut`, pour la compatibilité avec des outils tels que Structurizr
- **Statut unique.** La section Status ne doit pas lister toutes les valeurs possibles : ne conserver que le statut retenu
- **Auteurs : demander à l'humain.** Ne jamais mettre le nom des agents dans les auteurs. Demander à l'humain les noms des auteurs de la décision structurante avant de générer le document
- **Pas d'issues en référence.** Ne jamais ajouter d'issues (tickets) dans la section Références
- **Liens markdown.** Toute référence à d'autres décisions structurantes ou à la documentation du projet doit utiliser le format de lien markdown `[texte](chemin)`
- **URL pour les liens externes.** Toute référence à un lien externe (internet) doit inclure l'URL complète, au format `[texte](https://...)`
- Par défaut, le nom du client et la date d'acceptation doivent restée vide. Si une instruction indique que le client a accepté la décision structurante, renseigne le nom du client et la date de l'acceptation.

La décision structurante doit être enregistrée dans le registre de décisions du projet `decisions/` en respectant la convention de nommage : `NNNN-titre.md`, où NNNN est le numéro séquentiel à 4 chiffres (en partant de 0001) suivi du slug du titre (par ex. `0001-database-selection.md`).

## Structure de documentation requise

Le fichier de documentation doit suivre le modèle ci-dessous, en veillant à ce que toutes les sections soient correctement renseignées. Le front matter du markdown doit être structuré correctement comme dans l'exemple suivant :

```md
# [Titre de la décision]

---
auteurs: [Noms des auteurs fournis par l'humain]  
accepté par : [Nom du client ayant accepté la décision structurante]  
accepté le : [Date de l'acceptation par le client]  
supersedes: ""  
superseded_by: ""  

---

## Statut

Proposed

## Contexte

[Énoncé du problème, contraintes techniques, exigences métier et facteurs environnementaux qui motivent cette décision.]

## Décision

[Solution retenue avec une justification claire du choix.]

## Conséquences

### Positives

- **POS-001** : [Résultats bénéfiques et avantages]
- **POS-002** : [Améliorations de performance, de maintenabilité et de scalabilité]
- **POS-003** : [Alignement avec les principes d'architecture]

### Négatives

- **NEG-001** : [Compromis, limitations, inconvénients]
- **NEG-002** : [Dette technique ou complexité introduite]
- **NEG-003** : [Risques et défis futurs]

## Alternatives étudiées

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

- **REF-001** : [décision structurante associée] au format lien markdown, par ex. `[Sélection de la base de données](titre-de-la-decision.md)`
- **REF-002** : [Documentation externe] au format lien markdown avec l'URL complète, par ex. `[Documentation PostgreSQL](https://www.postgresql.org/docs/)`
- **REF-003** : [Norme ou cadre de référence] au format lien markdown avec l'URL complète, par ex. `[Modèle de décision structurante de Michael Nygard](https://github.com/joelparkerhenderson/architecture-decision-record)`
```
