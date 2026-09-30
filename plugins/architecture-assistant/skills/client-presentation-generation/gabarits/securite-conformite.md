# Gabarit — Présentation Sécurité / Conformité

**Public** : responsables sécurité, conformité, risque. **Retenue** : ne pas exposer de détails exploitables.
**Formats** : HTML dynamique (diagrammes Archify) et/ou PowerPoint.
**Patron narratif** (quand adapté) : Contexte → Objectifs → Moyens → Méthodes → Résultats.

## Chapitres

1. **Normes de sécurité applicables**.
   - Sources : `documentation/11-securite.md`, `08-contraintes.md`.
2. **Conformités / réglementation**.
   - Sources : `08-contraintes.md`.
3. **Cycle de vie et taxonomie des données**.
   - Sources : `10-cycle_vie_donnees.md`.
4. **Gouvernance sécurité**.
   - Sources : `11-securite.md`.
5. **Risques de sécurité & mesures** (synthèse STRIDE / OWASP, sans détails exploitables).
   - Sources : `11-securite.md`, `04-risques.md`.

## Règles spécifiques

- **Retenue** : synthétiser la posture sans exposer de vulnérabilités, secrets ou détails exploitables.
- Le **contrôle sécurité systématique** (Reviewer de sécurité) est porté par le workflow, en amont de la validation.
- Relier chaque norme/réglementation aux mesures de la solution.
- Tenir compte du champ `sensibilite` des documents source (ne pas présenter le `restreint` tel quel au client).
