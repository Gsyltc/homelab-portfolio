---
name: sales-deck-generation
description: "Génère des supports de vente et des réponses d'appels d'offres (Word, PDF, HTML) à partir de livrables d'architecture validés (documentation d'architecture, décisions structurantes, diagrammes). Utiliser pour transformer un contenu technique d'architecture en un support orienté public commercial."
---

Skill de génération de supports commerciaux à partir des livrables d'architecture. Ne jamais réinventer le contenu technique : partir des livrables validés et les reformuler pour un public non technique.

## Étape 1 — Rassembler les sources

- Identifier sur l'issue (ou auprès du coordinateur) les livrables d'architecture validés à synthétiser : documentation d'architecture (DAS), décisions structurantes, diagrammes.
- Lire ces documents via la skill `architecture-solution-gabarits` (format standard des gabarits) ; ne pas modifier le contenu source.
- Confirmer la cible du support : type (présentation client, réponse d'appel d'offres, one-pager), public, longueur attendue, format de sortie (Word / PDF / HTML).

## Étape 2 — Choisir le format de sortie

| Format | Quand l'utiliser | Production |
| --- | --- | --- |
| **HTML** | Support web, page de présentation, rendu rapide et responsive | Fichier `.html` autoportant (CSS inline), images/diagrammes intégrés |
| **PDF** | Livrable figé à transmettre au client, réponse d'appel d'offres | Générer depuis le HTML ou le Markdown (ex. moteur d'export du poste) |
| **Word (.docx)** | Le client exige un document éditable | Depuis Markdown (ex. `pandoc`) ou gabarit `.docx` fourni |

Toujours demander le format souhaité si non précisé.

## Étape 3 — Structurer le support

Trame recommandée, adaptée au public commercial :

1. **Résumé exécutif** — le besoin métier et la valeur apportée, en quelques phrases.
2. **Contexte & enjeux** — le problème client, sans jargon.
3. **Solution proposée** — vue d'ensemble de l'architecture (reprendre un diagramme de haut niveau), formulée en bénéfices.
4. **Différenciateurs** — ce qui distingue la solution (fiabilité, sécurité, coûts maîtrisés, time-to-market).
5. **Risques maîtrisés** — mentionner les risques et comment ils sont couverts (rassure sans masquer).
6. **Prochaines étapes / offre** — planning, jalons, conditions.

## Étape 4 — Règles de rédaction

- **Traduire la technique en valeur** : chaque élément technique repris doit être relié à un bénéfice métier.
- **Rester fidèle à la source** : ne pas inventer de chiffres, de garanties ou de fonctionnalités absents des livrables validés. En cas de doute technique, remonter au coordinateur.
- **Public commercial** : éviter le jargon ; privilégier des visuels et des tableaux clairs.
- **Diagrammes** : réutiliser ceux des livrables d'architecture ; si un schéma simplifié est nécessaire, le produire en code (Mermaid/PlantUML) et valider sa syntaxe avant export.
- **Confidentialité** : ne jamais inclure de secret, d'identifiant, ni de donnée interne non destinée au client.
- **Langue** : rédiger dans la langue du destinataire (français par défaut).

## Étape 5 — Livraison

- Produire le fichier au format demandé.
- Publier le livrable sur l'issue (via `multica attachment upload`) avec un récapitulatif : type de support, public visé, sources d'architecture utilisées, format.
- Ne pas considérer la tâche terminée avant la vérification de l'assigneur.
