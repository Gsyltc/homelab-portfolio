# Gabarit — Présentation Sécurité / Conformité

**Public** : responsables sécurité, conformité, risque. **Retenue** : ne pas exposer de détails exploitables.
**Formats** : HTML dynamique (diagrammes Archify) et/ou PowerPoint.
**Patron narratif** (quand adapté) : Contexte → Objectifs → Moyens → Méthodes → Résultats.

## Chapitres

> **Diagramme Archify** : déterminer la recette **avant production** selon la [correspondance de la référence (section Sécurité/Conformité)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique) ; procédure : [Sélection du diagramme Archify](../SKILL.md#sélection-du-diagramme-archify-avant-production). Pour ce public, **`+trace` recommandé** (évidence d'audit) — **sans exposer de détail exploitable**. Ne pas recopier la correspondance ici.

0a. **Page de garde** *(par défaut, tous types)* — slide d'ouverture à mise en forme graphique moderne reprenant la charte `theme/` (logo inliné, dégradé primaire/secondaire, accent). **Champs normalisés** : **titre**, **sous-titre**, **public visé**, **auteur**, **année**, **date/version**, **baseline/tagline**, **confidentialité**. Ne rien inventer : titre/public/auteur issus du cadrage, charte issue de `theme/` (jamais approximée). Présente en **HTML dynamique et en PowerPoint**.
0b. **Sommaire** *(par défaut, tous types)* — juste après la page de garde : table des matières des **chapitres retenus** (thèmes de **niveau 1** uniquement), reflétant uniquement les chapitres réellement présents. En HTML dynamique, cohérent avec le menu latéral auto (`data-chapter`). Présent en **HTML dynamique et en PowerPoint**.
1. **Normes de sécurité applicables**.
   - Sources : `documentation/11-securite.md`, `08-contraintes.md`.
2. **Conformités / réglementation**.
   - Sources : `08-contraintes.md`.
3. **Cycle de vie et taxonomie des données**.
   - **Diagramme Archify** : recette/type selon la [correspondance de la référence (Sécurité/Conformité)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique).
   - Sources : `10-cycle_vie_donnees.md`.
4. **Gouvernance sécurité**.
   - **Diagramme Archify** : recette/type selon la [correspondance de la référence (Sécurité/Conformité)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique) ; `+trace` pour l'évidence.
   - Sources : `11-securite.md`.
5. **Risques de sécurité & mesures** (synthèse STRIDE / OWASP, sans détails exploitables).
   - Sources : `11-securite.md`, `04-risques.md`.

## Règles spécifiques

- **Retenue** : synthétiser la posture sans exposer de vulnérabilités, secrets ou détails exploitables.
- **Diagrammes Archify — public sécurité/conformité** : déterminer la recette **avant production** selon la [correspondance de la référence (section Sécurité/Conformité)](../references/archify-diagram-types.md#correspondance-publicthème--recette-source-unique), avec **`+trace`** pour l'évidence d'audit. La trace montre la preuve, jamais un détail exploitable. Ne pas recopier la correspondance ici.
- Le **contrôle sécurité systématique** (Reviewer de sécurité) est porté par le workflow, en amont de la validation.
- Relier chaque norme/réglementation aux mesures de la solution.
- Tenir compte du champ `sensibilite` des documents source (ne pas présenter le `restreint` tel quel au client).
- **Densité et clarté rédactionnelle** : diapositives de contenu rédigées (**~180–320 mots utiles**, alternant paragraphe rédigé et liste à puces) ; diapositive à diagramme = **paragraphe de contexte au-dessus du schéma**. Densité suffisante sans jamais inventer : matière manquante **signalée**, pas comblée (cf. règles d'or 4, 13).
- **Aucune note de génération dans le rendu** (règle d'or 14) : pas de « Source : … », « rien d'inventé », process-sourcing, descripteur de rendu ni ligne de version-process **sur les diapositives** ; la discipline « ne rien inventer » reste une règle de production, non un texte de slide.
