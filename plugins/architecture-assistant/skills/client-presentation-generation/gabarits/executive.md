# Gabarit — Présentation Executive

**Public** : direction (comité de direction, comité exécutif, gestion de projet). **Niveau** : haut niveau, synthétique.
**Formats** : HTML dynamique (diagrammes Archify) et/ou PowerPoint.
**Patron narratif** (quand adapté) : Contexte → Objectifs → Moyens → Méthodes → Résultats.

> **Principe (tout le gabarit) : ne rien inventer.** Chaque chapitre est produit **uniquement** à partir de la documentation d'architecture validée du projet. **Si la documentation n'est pas disponible** pour un chapitre, ce chapitre est **considéré comme exclu** (ni contenu inventé, ni section vide). Le manque peut être signalé au périmètre pour arbitrage humain.

## Chapitres

0a. **Page de garde** *(par défaut, tous types)* — slide d'ouverture à mise en forme graphique moderne reprenant la charte `theme/` (logo inliné, dégradé primaire/secondaire, accent). **Champs normalisés** : **titre**, **sous-titre**, **public visé**, **auteur**, **année**, **date/version**, **baseline/tagline**, **confidentialité**. Ne rien inventer : titre/public/auteur issus du cadrage, charte issue de `theme/` (jamais approximée). Présente en **HTML dynamique et en PowerPoint**.
0b. **Sommaire** *(par défaut, tous types)* — juste après la page de garde : table des matières des **chapitres retenus** (thèmes de **niveau 1** uniquement), reflétant uniquement les chapitres réellement présents (un chapitre exclu faute de documentation n'y figure pas). En HTML dynamique, cohérent avec le menu latéral auto (`data-chapter`). Présent en **HTML dynamique et en PowerPoint**.
1. **Résumé exécutif** — le besoin et la valeur en quelques phrases.
   - Sources : `documentation/01-introduction.md`, `02-objectifs.md`.
2. **Contexte & enjeux**.
   - **Situation actuelle** : 2-3 faits mesurables.
   - **Problème central** : une phrase maximum.
   - **Enjeux stratégiques** : alignement avec les objectifs d'entreprise.
   - **Conséquences de l'inaction** : quantifiées si possible.
   - Sources : `01-introduction.md`, `02-objectifs.md`, `04-risques.md`.
3. **Objectifs & résultats attendus** — avec **KPIs** (tableau).
   - Chaque objectif relié à un ou plusieurs KPIs mesurables.
   - Exemple de tableau de KPIs :

     | KPI | Objectif lié | Valeur de référence | Cible | Échéance |
     | --- | --- | --- | --- | --- |
     | Délai de traitement | Efficacité opérationnelle | 8 j | 3 j | T4 2026 |
     | Taux de disponibilité | Fiabilité du service | 99,0 % | 99,9 % | T2 2026 |
     | Coût unitaire par transaction | Réduction des coûts | 1,20 $ | 0,80 $ | T4 2026 |

     *(valeurs d'exemple — à remplacer par les KPIs réels des objectifs du projet ; ne rien inventer)*
   - Sources : `02-objectifs.md`, `13-plan-qualite.md`.
4. **Vue d'ensemble de la solution** — un diagramme haut niveau (Archify), formulé en bénéfices.
   - **Principaux bénéfices métier** (liste courte, orientée valeur).
   - **Étapes de déploiement** (vue macro : jalons de mise en œuvre).
   - **Diagramme Archify** : recette/type selon la [correspondance de la référence (Executive)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique) ; procédure : [Sélection du diagramme Archify](../SKILL.md#sélection-du-diagramme-archify-avant-production).
   - Sources : `06-architecture-solutions.md`, `views/`, `09-deploiement.md`.
5. **Risques maîtrisés / points d'attention** — avec **suivi des risques** (tableau).
   - Exemple de tableau de suivi :

     | Risque | Probabilité | Impact | Atténuation |
     | --- | --- | --- | --- |
     | Dépassement de délai | Moyenne | Élevé | Découpage par jalons, walking skeleton |
     | Adoption utilisateurs | Moyenne | Élevé | Conduite du changement, formation |
     | Dépendance fournisseur | Faible | Moyen | Clause de réversibilité, standard ouvert |

     *(valeurs d'exemple — à remplacer par le registre des risques réel du projet)*
   - Sources : `04-risques.md`.
6. **Coûts & jalons**.
   - **Synthèse CAPEX / OPEX (en k$ CAD)** — **seulement si l'information est disponible** dans la documentation (sinon exclu, ne rien inventer).
   - Exemple de tableau CAPEX / OPEX :

     | Poste | Type | Année 1 (k$ CAD) | Année 2 (k$ CAD) | Année 3 (k$ CAD) | Total (k$ CAD) |
     | --- | --- | ---: | ---: | ---: | ---: |
     | Licences & logiciels | CAPEX | 120 | 20 | 20 | 160 |
     | Développement / intégration | CAPEX | 340 | 80 | 40 | 460 |
     | Infrastructure cloud | OPEX | 60 | 75 | 80 | 215 |
     | Support & exploitation | OPEX | 40 | 90 | 95 | 225 |
     | **Total CAPEX** | | **460** | **100** | **60** | **620** |
     | **Total OPEX** | | **100** | **165** | **175** | **440** |
     | **Total** | | **560** | **265** | **235** | **1 060** |

     *(valeurs d'exemple — à remplacer par les coûts réels du projet ; ne rien inventer. Si les coûts ne sont pas documentés, exclure le chapitre.)*
   - **Jalons critiques** : quels sont-ils, quand, et leurs livrables.
   - Sources : `05-planification.md`.
7. **Prochaines étapes**.
   - **Demande faite au comité** : la décision / l'arbitrage sollicité.
   - **Prochaines étapes immédiates**.
   - **Priorités et alignements** (avec les objectifs d'entreprise).
   - Sources : `05-planification.md`, `02-objectifs.md`, `07-choix-des-solutions.md`.

## Règles spécifiques

- Une idée par diapositive ; privilégier chiffres-clés, tableaux et visuels.
- **Densité et clarté rédactionnelle** : diapositives de contenu rédigées (**~180–320 mots utiles**, alternant paragraphe rédigé et liste à puces) ; diapositive à diagramme = **paragraphe de contexte au-dessus du schéma**. Densité suffisante sans jamais inventer : matière manquante **signalée**, pas comblée (cf. règles d'or 4, 13).
- **Aucune note de génération dans le rendu** (règle d'or 14) : pas de « Source : … », « rien d'inventé », process-sourcing, descripteur de rendu ni ligne de version-process **sur les diapositives** ; la discipline « ne rien inventer » reste une règle de production, non un texte de slide.
- **Diagrammes Archify — public direction** : déterminer la recette **avant production** selon la [correspondance de la référence (section Executive)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique) ; privilégier une composition `classic` **sans trace** (synthèse orientée décision). Ne pas recopier la correspondance ici.
- Traduire chaque élément technique en bénéfice métier.
- **KPIs, suivi des risques et synthèse CAPEX/OPEX présentés sous forme de tableau.**
- **CAPEX / OPEX** : uniquement **si disponible** dans la documentation, en **k$ CAD** ; sinon exclu.
- **Ne rien inventer** : produire chaque chapitre uniquement depuis la documentation validée ; **tout chapitre sans documentation disponible est exclu** (les valeurs d'exemple des tableaux sont des illustrations, à remplacer par les données réelles). Signaler le manque au périmètre.
- Ne pas exposer de détails techniques ou sensibles inutiles à la décision.
