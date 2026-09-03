## Concepts transverses

> Cette section regroupe les **concepts transverses** de la solution : les préoccupations techniques partagées par plusieurs systèmes logiciels (communication, gestion des erreurs, transactions, cache, persistance, observabilité, configuration, accessibilité). Elle correspond au Cross-cutting Concepts (arc42 §8). Chaque concept est relié aux **patrons** du répertoire `patron-architecture/` et à la **matrice de suivi** du `02-objectifs.md`.

| ID | Concept | Description | Patron(s) associé(s) | Décisions / liens |
|----|---------|-------------|----------------------|-------------------|
| TRV-001 | Communication et intégration | Protocoles, formats d'échange, patrons d'intégration entre les systèmes de la solution | `patron-architecture/…` | ADR-xxx |
| TRV-002 | Gestion des exceptions et des erreurs | Stratégie de détection, classification, journalisation et remontée des erreurs | `patron-architecture/…` | ADR-xxx |
| TRV-003 | Gestion des transactions | Transactions locales/distribuées, cohérence éventuelle, rejeu | `patron-architecture/…` | ADR-xxx |
| TRV-004 | Cache et mise en cache | Stratégies de mise en cache, invalidations, volumétrie | `patron-architecture/…` | ADR-xxx |
| TRV-005 | Persistance | Stratégie générale de persistance (hors modèle de données détaillé du `10`) | `patron-architecture/…` | ADR-xxx |
| TRV-006 | Journalisation, observabilité et audit | Journaux, métriques, traces, conservation des journaux d'audit | `patron-architecture/…` | ADR-xxx |
| TRV-007 | Gestion de la configuration | Sources de configuration, variables d'environnement, secrets | `patron-architecture/…` | ADR-xxx |
| TRV-008 | Accessibilité et internationalisation | Règles d'accessibilité, langues, localisation | — | ADR-xxx |

**Tableau 72. Concepts transverses**

### TRV-001 — Communication et intégration

> Décrire : protocoles et formats d'échange retenus, patrons d'intégration (ex. Transactional Outbox/Inbox, publish/subscribe, queues), références aux interfaces du registre (issue ALI-40) et à la vue d'exécution du `06`.

### TRV-002 — Gestion des exceptions et des erreurs

> Décrire : classification des erreurs, stratégie de remontée aux utilisateurs et aux systèmes, journalisation, codes de retour.

### TRV-003 — Gestion des transactions

> Décrire : besoin transactionnel, transactions distribuées ou cohérence éventuelle, rejeu et idempotence, lien avec les patrons Transactional Inbox/Outbox.

### TRV-004 — Cache et mise en cache

> Décrire : données cachées, stratégies (cache-aside, write-through, TTL), invalidation, cohérence, volumétrie (lien `12-volumetries.md`).

### TRV-005 — Persistance

> Décrire : stratégie générale de persistance (base relationnelle, document, objet), approche multi-modèles le cas échéant, lien avec le modèle d'information (issue ALI-39) et le cycle de vie des données (`10`).

### TRV-006 — Journalisation, observabilité et audit

> Décrire : niveaux de journalisation, collecte des métriques et traces, journal d'audit (liens `11-securite.md`, `09-deploiement.md`).

### TRV-007 — Gestion de la configuration

> Décrire : sources de configuration, cycles de vie, gestion des secrets (sans jamais inclure de secrets dans la documentation).

### TRV-008 — Accessibilité et internationalisation

> Décrire : règles d'accessibilité applicables, langues supportées, mécanismes de localisation.
