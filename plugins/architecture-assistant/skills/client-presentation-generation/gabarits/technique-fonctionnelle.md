# Gabarit — Présentation Technique / Fonctionnelle

**Public** : équipes techniques et fonctionnelles du client. **Présentation dynamique uniquement** (HTML, diagrammes Archify).
**Nomenclature client** appliquée à chaque domaine.
**Patron narratif** (quand adapté) : Contexte → Objectifs → Moyens → Méthodes → Résultats.

## Sources : DAS racine + sous-répertoires détaillés de `documentation/`

Pour une présentation technique, l'information détaillée se trouve **souvent dans les sous-répertoires de `documentation/`** (architecture détaillée par domaine), en complément des fichiers de synthèse de la DAS racine (`01`–`15`) :

| Domaine | Synthèse (DAS racine) | Détail (sous-répertoire) |
|---|---|---|
| Logiciel | `06-architecture-solutions.md`, `07-choix-des-solutions.md` | `documentation/architecture-logicielle/` |
| Infrastructure | `09-deploiement.md`, `14-preventions-et-resilience.md` | `documentation/architecture-infra/` |
| Sécurité (détail) | `11-securite.md` | `documentation/architecture-securite/` |
| Data | `10-cycle_vie_donnees.md`, `12-volumetries.md` | `documentation/architecture-donnee/` |

> Cibler d'abord la synthèse (DAS racine) pour la vue d'ensemble, puis descendre dans le **sous-répertoire de domaine** pour les aspects détaillés (via `presentation-targeting`).

## Chapitres (sélectionner selon le périmètre)

> **Diagramme Archify par chapitre** : déterminer la recette **avant production** selon la question posée. La **correspondance par chapitre (chapitre → question → recette → type → composition)** est portée **uniquement** par la référence : voir [`references/archify-diagram-types.md` → Détail par chapitre — présentation Technique / Fonctionnelle](../references/archify-diagram-types.md#détail-par-chapitre--présentation-technique--fonctionnelle). Ne pas la recopier ici. Procédure générale : [Sélection du diagramme Archify](../SKILL.md#sélection-du-diagramme-archify-avant-production).

0a. **Page de garde** *(par défaut, tous types)* — slide d'ouverture à mise en forme graphique moderne reprenant la charte `theme/` (logo inliné, dégradé primaire/secondaire, accent). Contenu : **titre**, **sous-titre**, **public visé**, **date/version**, **confidentialité**. Ne rien inventer : titre/public issus du cadrage, charte issue de `theme/` (jamais approximée). **HTML dynamique uniquement** pour ce type (contrainte de format).
0b. **Sommaire** *(par défaut, tous types)* — juste après la page de garde : table des matières des **chapitres retenus** (thèmes de **niveau 1** uniquement), reflétant uniquement les chapitres réellement présents. Cohérent avec le menu latéral auto (`data-chapter`). **HTML dynamique uniquement** pour ce type.
1. **Contexte technique & périmètre**.
   - Sources : `documentation/01-introduction.md`, `06-architecture-solutions.md`.
2. **Logiciel** — composants, intégrations, séquences.
   - Sources : `06-architecture-solutions.md`, `07-choix-des-solutions.md`, `documentation/architecture-logicielle/`.
3. **Data** — modèles, flux ; **gouvernance des données**.
   - Sources : `10-cycle_vie_donnees.md`, `12-volumetries.md`, `documentation/architecture-donnee/`.
4. **Infrastructure** — topologie ; **respect des patrons d'infrastructure client**.
   - Sources : `09-deploiement.md`, `14-preventions-et-resilience.md`, `documentation/architecture-infra/`.
5. **Sécurité (détail technique)** — contrôles, durcissement, zones de confiance.
   - Sources : `11-securite.md`, `documentation/architecture-securite/`.
6. **IA** — cas d'usage, modèles ; **gouvernance IA**.
   - Sources : `15-concepts-transverses.md`, `06-architecture-solutions.md`.
7. **Concepts transverses** — observabilité, configuration, erreurs, etc.
   - Sources : `15-concepts-transverses.md`.

## Règles spécifiques

- **HTML dynamique uniquement** ; diagrammes **Archify** interactifs.
- **Choix du diagramme avant production** : appliquer la correspondance par chapitre portée par la [référence](../references/archify-diagram-types.md#détail-par-chapitre--présentation-technique--fonctionnelle) (recette → type + composition) ; préférer `signal-flow` pour les flux/échanges et `blueprint` pour les topologies. Une recette par diagramme.
- **Descendre dans les sous-répertoires de `documentation/`** (`architecture-logicielle/`, `architecture-donnee/`, `architecture-infra/`, `architecture-securite/`, etc.) pour le détail par domaine ; la DAS racine donne la synthèse.
- Appliquer la **nomenclature client** à chaque domaine (noms de systèmes, environnements, zones).
- Respecter les **patrons d'infrastructure client** dans le chapitre Infrastructure.
- Détailler au niveau utile à l'audience technique, sans exposer de secret ; sur le détail sécurité, appliquer la retenue (pas de détails exploitables).
