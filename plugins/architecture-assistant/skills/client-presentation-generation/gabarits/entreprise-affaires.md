# Gabarit — Présentation Entreprise / Affaires (respect TOGAF)

**Public** : parties prenantes affaires et architecture d'entreprise. **Respect TOGAF** pour la version Entreprise.
**Formats** : HTML dynamique (diagrammes Archify) et/ou PowerPoint.
**Patron narratif** (quand adapté) : Contexte → Objectifs → Moyens → Méthodes → Résultats.

> **Principe (tout le gabarit) : ne rien inventer.** Chaque chapitre est produit **uniquement** à partir de la documentation d'architecture validée du projet. **Si la documentation n'est pas disponible** pour un chapitre, ce chapitre est **considéré comme exclu** (ni contenu inventé, ni section vide). Le manque peut être signalé au périmètre pour arbitrage humain.

## Chapitres

1. **Synthèse exécutive**.
   - Message clé, valeur d'affaires et décision attendue, en une page/diapositive.
   - Sources : `documentation/01-introduction.md`, `02-objectifs.md`.
2. **Contexte d'affaires**.
   - Sources : `01-introduction.md`.
3. **Cartographie des parties prenantes** (TOGAF — Phase A : Architecture Vision).
   - Identifier **qui** sont les parties prenantes, leurs **intérêts / concerns** principaux, et le **niveau d'influence et d'engagement requis** (ex. matrice pouvoir/intérêt).
   - Sources : `01-introduction.md` (parties prenantes), `001-document-architecture-solution.md` (arrimages / RACI).
4. **Compréhension des besoins d'affaires** — **ciblable** : présenter **tous** les besoins, ou **un ou plusieurs besoins spécifiques** selon la présentation désirée.
   - Sélectionner les besoins par leur **identifiant codé** (ex. `BES-001`, `UC-001`) ou par section (titre H2/H3 du `03`). Le périmètre (quels besoins) est confirmé au cadrage / gate de périmètre porté par le workflow.
   - Pour chaque besoin retenu : intitulé, contexte, valeur d'affaires, et le cas échéant sa couverture architecturale.
   - Sources : `03-besoins_affaires_exigences.md` (besoins/exigences ciblés).
5. **Registres des BAE** (Business Architecture Elements / exigences d'affaires) — **optionnel, gate légère (inclusion/exclusion) sur demande de l'humain**.
   - Décision d'inclusion/exclusion prise au **gate léger de périmètre**. Ne l'inclure **que si l'humain le demande**. S'il est généré : **concis**, **ciblé sur les thèmes en lien avec la présentation** (et les besoins retenus au point 4), présenté **sous forme de tableau** (ex. colonnes : ID BAE, intitulé, besoin/objectif lié, couverture architecturale, statut).
   - Sources : `03-besoins_affaires_exigences.md`.
6. **Indicateurs de succès (KPIs)**.
   - Comment mesure-t-on la réussite de la transformation ? **Métriques reliées aux objectifs d'affaires initiaux** (cible, valeur de référence, échéance).
   - Sources : `02-objectifs.md`, `03-besoins_affaires_exigences.md`, `13-plan-qualite.md`.
7. **Risques**.
   - Sources : `04-risques.md`.
8. **CAPEX / OPEX** — **optionnel, gate légère (inclusion/exclusion)** : à inclure **sur demande de l'humain** et **seulement si l'information est disponible dans la documentation**.
   - Si non demandé ou absent des sources, exclure le chapitre (ne rien inventer) ; le signaler au périmètre si pertinent.
   - Sources : `05-planification.md`.
9. **Juridiction** (contraintes légales / réglementaires applicables).
   - Sources : `08-contraintes.md`.
10. **Alignement architecture d'entreprise (TOGAF)** — couches Métier, Données, Application, Technologie.
    - **Diagramme Archify** : recette/type selon la [correspondance de la référence (Entreprise/Affaires)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique).
    - Sources : `06-architecture-solutions.md`, `10-cycle_vie_donnees.md`, front-matter `togaf_layer` des documents.
11. **Gestion du changement organisationnel**.
    - Impact sur les équipes, **compétences requises**, **formations nécessaires**, adhésion. Souvent sous-estimé mais critique pour l'adoption réelle.
    - Sources : `05-planification.md`, `09-deploiement.md`, `01-introduction.md` (parties prenantes).
12. **Dépendances critiques entre initiatives**.
    - Dépendances **techniques, temporelles et de ressources** entre les pièces de la feuille de route (ex. diagramme de dépendances Archify).
    - **Diagramme Archify** : recette/type selon la [correspondance de la référence (Entreprise/Affaires)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique).
    - Sources : `05-planification.md`, `06-architecture-solutions.md`, `07-choix-des-solutions.md`.
13. **Plan de transition par étapes (Transition Architectures)**.
    - Plutôt qu'une feuille de route unique, définir des **états intermédiaires mesurables**, chacun avec ses **livrables** et critères de sortie (TOGAF — Transition Architectures).
    - **Diagramme Archify** : recette/type selon la [correspondance de la référence (Entreprise/Affaires)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique).
    - Sources : `05-planification.md`, `09-deploiement.md`.
14. **Feuille de route / recommandations**.
    - Sources : `05-planification.md`, `07-choix-des-solutions.md`.

## Règles spécifiques

- Structurer selon les couches TOGAF pour la version Entreprise ; la **cartographie des parties prenantes** relève de la Phase A (Architecture Vision) et les **Transition Architectures** des états intermédiaires de la roadmap.
- Relier chaque exigence d'affaires (BAE) à sa couverture architecturale, et **chaque KPI à un objectif d'affaires initial**.
- **Registre des BAE — gate légère (inclusion/exclusion)** : décision d'inclusion prise au gate léger de périmètre, **sur demande de l'humain** ; s'il est généré, le garder **concis**, **ciblé sur les thèmes / besoins de la présentation**, et le présenter **sous forme de tableau**.
- **CAPEX / OPEX — gate légère (inclusion/exclusion)** : à inclure **sur demande de l'humain** et **seulement si disponible dans la documentation** ; sinon exclure (ne rien inventer).
- **Besoins d'affaires ciblables** : selon la présentation désirée, présenter tous les besoins ou **un/plusieurs besoins spécifiques**, sélectionnés par identifiant (`BES-001`, `UC-001`…) ou par section ; confirmer ce sous-ensemble au périmètre. Les chapitres liés (BAE, KPIs, risques, dépendances) se restreignent alors au(x) besoin(s) retenu(s) pour rester cohérents.
- Rendre visibles les **dépendances critiques** (technique / temps / ressources) et les **états de transition** (jalons mesurables + livrables).
- **Diagrammes Archify — public affaires/architecture** : déterminer la recette **avant production** selon la [correspondance de la référence (section Entreprise/Affaires)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique) ; `+trace` si l'ownership/évidence doit être démontré. Ne pas recopier la correspondance ici.
- Ne pas négliger la **conduite du changement** (compétences, formations, adhésion).
- Tableaux clairs pour parties prenantes, KPIs, risques, coûts, conformités et dépendances.
- **Ne rien inventer** : produire chaque chapitre uniquement depuis la documentation validée. **Tout chapitre sans documentation disponible est exclu** (ne pas forcer un chapitre, ne pas laisser de section vide) ; signaler le manque au périmètre pour arbitrage.
