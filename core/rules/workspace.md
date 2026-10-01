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

## Documentation finale

- **RULE-WS-006** — **OBLIGATOIRE.** Dans toute documentation finale livrée, aucun nom d'agent, aucune mention de skill et aucun nom de fichier ne doit apparaître. En conséquence :
  - **Liens internes** : un lien Markdown vers un autre document utilise le **titre du document** (son titre H2) comme libellé, jamais le nom de fichier. Ex. : un lien vers `11-securite.md` s'affiche `Sécurité`.
  - **Noms de responsables** : lorsqu'un nom doit être renseigné, indiquer le **nom réel du responsable du projet** tel que défini dans les Arrimages (matrice RACI, colonne « Nom »), jamais un placeholder ni un nom d'agent.
  - _portée_ : workspace · _origine_ : demande workspace multica.gaston (chat) · _ajoutée le_ : 2026-09-10

## Rédaction documentaire

- **RULE-WS-007** — **OBLIGATOIRE.** Aucun document livré ne porte d'information issue de sa génération : il ne contient que ce qui concerne le projet (architecture, décisions, exigences, etc.). Proscrire toute mention de méta-génération — p. ex. « diagramme généré avec … », « document produit par … », notes d'outil, horodatage de génération.
  - _portée_ : workspace · _origine_ : demande workspace multica.gaston (ORIG-42) · _ajoutée le_ : 2026-10-01
- **RULE-WS-008** — Les descriptions des versions documentaires (motif du changement dans l'historique du document) sont **concises** et limitées à l'essentiel : une à deux lignes factuelles, sans prose superflue.
  - _portée_ : workspace · _origine_ : demande workspace multica.gaston (ORIG-42) · _ajoutée le_ : 2026-10-01
- **RULE-WS-009** — Les diagrammes **réutilisent le thème du projet** (répertoire `theme/`, p. ex. `theme/0000-default-styles.dsl`) **lorsqu'il est disponible**, pour Structurizr, PlantUML et les autres moteurs de rendu. Ne pas réinventer ni approximer un style quand le thème existe.
  - _portée_ : workspace · _origine_ : demande workspace multica.gaston (ORIG-42) · _ajoutée le_ : 2026-10-01
- **RULE-WS-010** — Pour toute feuille de route / timeline / roadmap, **si aucune date n'est indiquée**, considérer le début à **J + 7 jours à compter de la date du jour**.
  - _portée_ : workspace · _origine_ : demande workspace multica.gaston (ORIG-42) · _ajoutée le_ : 2026-10-01
