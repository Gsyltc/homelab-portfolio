# Compensating Transaction

> Patron d'architecture cloud documenté dans le [catalogue des patrons de l'Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction). Les patrons sont agnostiques à la technologie : applicables sur Azure, AWS, sur site et en hybride.

## Objectif du patron

Annuler le travail effectué par une séquence d'étapes qui forment une opération globalement cohérente (éventuellement cohérente) : en cas d'échec, exécuter des étapes de compensation pour revenir à un état acceptable.

## Quand l'envisager

- Pour les opérations distribuées qui ne peuvent pas être transactionnelles de façon atomique (ex. appels à plusieurs services).
- Lorsqu'une étape intermédiaire échoue après que d'autres ont réussi.
- Pour implémenter la cohérence finale sur des flux multi-services.

## Quand ne PAS l'envisager

- Lorsqu'une vraie transaction distribuée (2PC) est possible et appropriée.
- Si les étapes ne présentent aucun effet de bord à annuler.
- Lorsque la compensation n'est pas techniquement réalisable (effets externes irréversibles).

## Prérequis

### Logiciel

- Implémentation des étapes de compensation dans chaque service concerné et logique d'orchestration/coordination.

### Infrastructure

- Traçabilité des étapes effectuées (journal) pour savoir quoi compenser.

## Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Évite les verrous longs et le couplage transactionnel. | Logique de compensation complexe et risquée. |
| Permet des opérations longues et distribuées cohérentes. | Fenêtre d'incohérence temporaire pendant le traitement. |
| Cohérence finale explicite et contrôlable. | Compensation impossible pour certains effets irréversibles. |

## Piliers couverts et objectifs réalisés

| Pilier (Well-Architected Framework) | Objectifs réalisés du pilier |
|-------------------------------------|-------------------------------|
| Fiabilité | Maintien de la cohérence des données en cas d'échec partiel d'une opération distribuée. |

## Source

[Patron Compensating Transaction – Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction)
