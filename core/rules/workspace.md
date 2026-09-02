# Règles — couche `workspace`

Règles valables pour **tout le workspace**, chargées au démarrage de chaque workflow. Couche de plus forte précédence. Toute règle ajoutée ici passe par un **contrôle sécurité systématique** de l'Architecte cybersécurité à l'admission (voir « Règles & boucle d'apprentissage »).

Ces règles reprennent les **invariants non négociables** déjà en vigueur (elles ne peuvent pas être affaiblies par une couche inférieure ni par un override) :

- **RULE-WS-001** — Toute modification d'architecture passe par le contrôle sécurité de l'Architecte cybersécurité avant la validation humaine.
  - _portée_ : workspace · _origine_ : core-workflow.md · _ajoutée le_ : 2026-09-02
- **RULE-WS-002** — Chaque décision structurante est tracée dans un ADR ; aucune décision acceptée sans validation humaine.
  - _portée_ : workspace · _origine_ : core-workflow.md · _ajoutée le_ : 2026-09-02
- **RULE-WS-003** — La piste d'audit vit sur l'issue Multica ; on ajoute des commentaires, on n'écrase jamais l'historique.
  - _portée_ : workspace · _origine_ : core-workflow.md · _ajoutée le_ : 2026-09-02
- **RULE-WS-004** — Chaque choix est validé / rejeté / commenté séparément (validation humaine granulaire) ; rien n'avance sur un élément non validé.
  - _portée_ : workspace · _origine_ : core-workflow.md · _ajoutée le_ : 2026-09-02
- **RULE-WS-005** — Information requise manquante → demander à l'humain et attendre ; ne jamais supposer.
  - _portée_ : workspace · _origine_ : core-workflow.md · _ajoutée le_ : 2026-09-02

> Les nouvelles règles apprises de portée `workspace` sont ajoutées ci-dessous, après confirmation humaine **et** contrôle sécurité.
