# Bonnes pratiques de modélisation dimensionnelle (Dimensional Modeling Best Practices)

## Méthode en 4 étapes de Kimball

### Étape 1 : Choisir le processus métier
Identifier clairement le processus métier à modéliser (commande, expédition, paiement, inscription, etc.) ; une table de faits correspond à un seul processus métier.

### Étape 2 : Déclarer la granularité
Définir ce que représente chaque ligne de la table de faits. Plus la granularité est fine, mieux c'est — la granularité atomique est la plus flexible.
- Niveau ligne de commande : une ligne = un article d'une commande
- Niveau transaction : une ligne = une transaction
- Niveau événement : une ligne = un événement de comportement utilisateur

### Étape 3 : Identifier les dimensions
Les dimensions qui entourent la table de faits : qui, quoi, quand, où, pourquoi.
- Qui (Who) : client, utilisateur, fournisseur
- Quoi (What) : produit, service, SKU
- Quand (When) : date, heure
- Où (Where) : magasin, région, canal
- Pourquoi (Why) : promotion, campagne, code de motif

### Étape 4 : Identifier les faits (mesures)
Mesures métier numériques et additionnables : quantité, montant, coût, durée, etc.

## Modèle en étoile vs modèle en flocon

| Caractéristique | Modèle en étoile | Modèle en flocon |
|------|----------|----------|
| Normalisation des tables de dimensions | Dénormalisé (table large) | Normalisé (hiérarchie à plusieurs niveaux) |
| Performance des requêtes | ⭐⭐⭐⭐⭐ Peu de JOIN | ⭐⭐⭐ Beaucoup de JOIN |
| Espace de stockage | Plus important | Plus faible |
| Complexité de maintenance | Faible | Élevée |
| Cas d'usage | Rapports BI, analyse en libre-service | Contextes à fortes exigences de gouvernance des données |

**Recommandation : utiliser par défaut le modèle en étoile, et n'envisager le modèle en flocon que dans les cas suivants :**
- Les hiérarchies de dimensions sont nombreuses et fréquemment interrogées de façon indépendante
- Le coût de stockage est une contrainte majeure
- Il existe déjà un système mature de gestion des hiérarchies de dimensions

## Types de tables de faits

### 1. Table de faits transactionnelle (Transaction Fact)
- La plus courante, granularité = un événement métier unique
- Insertion d'une ligne à chaque événement
- Mesures additionnables
- Exemple : `fact_orders` (chaque ligne = une commande)

### 2. Table de faits à instantané périodique (Periodic Snapshot)
- Enregistre l'état à intervalle fixe (jour/semaine/mois)
- Mesures semi-additionnables (les soldes ne peuvent pas être additionnés dans le temps)
- Exemple : `fact_inventory_daily` (instantané quotidien des stocks)

### 3. Table de faits à instantané cumulatif (Accumulating Snapshot)
- Suit un processus ayant un cycle de vie clair (par exemple une commande de sa création à sa livraison)
- Une seule ligne enregistre l'ensemble du cycle de vie
- Contient plusieurs dates de jalons
- Exemple : `fact_order_fulfillment` (processus d'exécution des commandes)

### 4. Table de faits sans fait (Factless Fact)
- Enregistre la survenance d'un événement ou la satisfaction d'une condition, sans mesure numérique
- Exemple : `fact_attendance` (relevé de présence des élèves), `fact_promotion_coverage` (couverture promotionnelle)

## Stratégies de dimensions à variation lente (SCD)

### Type 0 — Conserver la valeur d'origine
Aucune mise à jour. Convient aux attributs immuables (comme la date de naissance).

### Type 1 — Écrasement (Overwrite)
Met à jour directement l'ancienne valeur, sans conserver l'historique.
```sql
UPDATE dim_customer SET city = 'Lyon' WHERE customer_bk = 'C001';
```
- Convient : correction de données erronées, attributs dont l'historique n'a pas d'importance
- Risque : les résultats des rapports historiques changeront

### Type 2 — Ajout de ligne (Add Row) ⭐ Recommandé
Ajoute une ligne pour conserver l'historique, en marquant la période de validité par des plages temporelles.
```sql
-- Étape 1 : Fermer l'enregistrement courant
UPDATE dim_customer
SET valid_to = CURRENT_TIMESTAMP(), is_current = FALSE
WHERE customer_bk = 'C001' AND is_current = TRUE;

-- Étape 2 : Insérer la nouvelle version
INSERT INTO dim_customer (...) VALUES (..., is_current = TRUE);
```
- Avantage : suivi complet de l'historique
- Inconvénient : croissance du nombre de lignes de la table
- Clé de substitution (Surrogate Key) : une SK indépendante par version

### Type 3 — Ajout de colonne
Ajoute une colonne pour conserver la valeur précédente.
```sql
-- Ajout des colonnes previous_city, effective_date à la table dim_customer
UPDATE dim_customer SET previous_city = city, city = 'Lyon', effective_date = CURRENT_DATE();
```
- Convient : lorsqu'il suffit de savoir « quelle était la valeur avant le changement »
- Limite : ne peut stocker qu'une seule valeur historique

### Hybride (Type 1 + Type 2)
- La plupart des attributs en Type 1 (écrasement direct, comme le numéro de téléphone)
- Quelques attributs clés en Type 2 (conservation de l'historique, comme la cote de crédit)

## Modèles de conception des dimensions

### Dimension de date (Date Dimension)
**Obligatoire**. Contient de riches attributs de date :
- Clé de date (entier au format YYYYMMDD)
- Année/trimestre/mois/semaine/jour
- Week-end/jour férié ou non
- Année fiscale/trimestre fiscal

### Dimension dégénérée (Degenerate Dimension)
Clé de dimension présente dans la table de faits, sans table de dimension correspondante.
- Par exemple : `order_number`, `invoice_number`
- Il suffit de la conserver comme colonne d'attribut de dimension dans la table de faits

### Dimension fourre-tout (Junk Dimension)
Regroupe plusieurs indicateurs/statuts à faible cardinalité en une seule dimension.
- Par exemple : `payment_method` + `shipping_type` + `order_source` → `dim_order_attributes`

### Dimension à rôles multiples (Role-playing Dimension)
Une même table de dimension physique joue plusieurs rôles logiques.
- Par exemple : `dim_date` peut servir de `order_date`, `ship_date`, `delivery_date`

## Introduction à Data Vault 2.0

### Cas d'usage
- Intégration de multiples systèmes sources (10+ systèmes sources)
- Fusions/acquisitions ou changements organisationnels fréquents
- Nécessité d'une piste d'audit complète

### Structure à trois couches
- **Hub** : clé métier (comme le numéro client), ne stocke que la clé, pas les attributs
- **Link** : relations entre Hubs (comme la relation client-commande)
- **Satellite** : attributs descriptifs + horodatage

### Conseils pratiques
- Utiliser Data Vault pour la couche Raw Vault (couche d'intégration brute)
- Construire des data marts en modèle en étoile dans les couches supérieures pour la consommation métier
- Nécessite des outils de génération de code en support (le coût de maintenance manuelle est élevé)

## Liste de contrôle

- [ ] La granularité au niveau atomique est-elle définie ?
- [ ] Existe-t-il une table de dimension de date ?
- [ ] Utilise-t-on des clés de substitution plutôt que des clés naturelles ?
- [ ] La table de faits ne contient-elle que des clés étrangères et des mesures ?
- [ ] Les tables de dimensions contiennent-elles des attributs descriptifs ?
- [ ] La stratégie SCD est-elle clairement définie ?
- [ ] A-t-on pris en compte les dimensions dégénérées et fourre-tout ?
- [ ] A-t-on conçu des colonnes d'audit ETL (created_at, batch_id) ?
