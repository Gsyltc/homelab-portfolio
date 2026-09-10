# Référentiel des règles de qualité des données (Data Quality Rules Reference)

## Les 6 grandes dimensions de la qualité

### 1. Complétude (Completeness)

| Règle | Vérification SQL | Seuil recommandé |
|------|----------|----------|
| Clé primaire non nulle | `COUNT(*) WHERE pk IS NULL` | = 0 |
| Taux de non-nullité des champs obligatoires | `SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END) / COUNT(*)` | < 1% |
| Couverture des dimensions clés | Les clés étrangères de dimension de la table de faits ont-elles toutes une ligne de dimension correspondante | = 100% |

```sql
-- Exemple de vérification de complétude
SELECT
    'completeness' AS check_type,
    COUNT(*) AS total,
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct
FROM dwh.dim_customer;
```

### 2. Unicité (Uniqueness)

| Règle | Vérification SQL | Seuil recommandé |
|------|----------|----------|
| Unicité de la clé primaire | `COUNT(*) vs COUNT(DISTINCT pk)` | Parfaitement identiques |
| Unicité de la clé métier | `SELECT bk, COUNT(*) HAVING COUNT(*) > 1` | = 0 |
| Unicité de la clé composite | `SELECT col1, col2, COUNT(*) HAVING COUNT(*) > 1` | = 0 |

### 3. Validité (Validity)

| Règle | Vérification SQL | Seuil recommandé |
|------|----------|----------|
| Type de données correct | Analyse du format de date, valeur numérique convertible | = 100% |
| Plage de valeurs | `col BETWEEN min AND max` | > 99% |
| Valeur d'énumération valide | `col IN ('A','B','C')` | = 100% |
| Correspondance regex | `REGEXP_CONTAINS(col, r'pattern')` | > 95% |
| Intégrité référentielle | `fk NOT IN (SELECT pk FROM dim_table)` | = 0 |

### 4. Cohérence (Consistency)

| Règle | Vérification SQL | Seuil recommandé |
|------|----------|----------|
| Cohérence inter-tables | Les attributs d'une même entité sont-ils cohérents entre différentes tables | > 99% |
| Cohérence des agrégats | `SUM(fact.amount) = SUM(agg.amount)` | Écart < 0,1% |
| Cohérence inter-systèmes | Comparaison du nombre d'enregistrements entre système source et entrepôt | Écart < 1% |

### 5. Ponctualité (Timeliness)

| Règle | Vérification SQL | Seuil recommandé |
|------|----------|----------|
| Fraîcheur des données | `MAX(created_at) vs NOW()` | < seuil SLA |
| Taux de ponctualité du pipeline | Proportion de pipelines terminés dans la fenêtre de temps prévue | > 99% |
| Livraison retardée | Latence des données du système source vers l'entrepôt | < 1h (cœur) |

### 6. Exactitude (Accuracy)

| Règle | Vérification SQL | Seuil recommandé |
|------|----------|----------|
| Anomalie statistique | Proportion de lignes avec Z-Score > 3 | < 1% |
| Plausibilité des montants | `amount < 0 OR amount > 1000000` | < 0,1% |
| Dérive de distribution | Divergence KL entre la distribution du jour et la moyenne des 7 jours précédents | < 0,1 |
| Vérification des valeurs nulles/négatives | `amount <= 0` | Selon le métier |

## Aide-mémoire des règles Great Expectations

```yaml
# Complétude
- expect_column_values_to_not_be_null:
    column: customer_id
    mostly: 0.99

# Unicité
- expect_column_values_to_be_unique:
    column: order_id

# Ensemble de valeurs
- expect_column_values_to_be_in_set:
    column: status
    value_set: ["active", "inactive", "pending"]

# Plage
- expect_column_values_to_be_between:
    column: age
    min_value: 0
    max_value: 150

# Regex
- expect_column_values_to_match_regex:
    column: email
    regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

# Fraîcheur
- expect_column_max_to_be_between:
    column: updated_at
    max_value: "{{ now() }}"
    min_value: "{{ now() - timedelta(days=1) }}"
```

## Modèle de tests dbt

```yaml
# schema.yml
version: 2
models:
  - name: fact_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customer')
              field: customer_sk
      - name: order_amount
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
      - name: order_status
        tests:
          - accepted_values:
              values: ['pending', 'shipped', 'delivered', 'cancelled']
```

## Règles de détection d'anomalies

### Anomalie de volume de données
```sql
-- Détecter si le volume de données du jour dévie anormalement
WITH daily_stats AS (
    SELECT
        DATE(created_at) AS dt,
        COUNT(*) AS row_count
    FROM fact_orders
    WHERE DATE(created_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY dt
),
stats AS (
    SELECT AVG(row_count) AS avg_count, STDDEV(row_count) AS std_count
    FROM daily_stats
    WHERE dt < CURRENT_DATE()
)
SELECT
    d.dt,
    d.row_count,
    s.avg_count,
    (d.row_count - s.avg_count) / NULLIF(s.std_count, 0) AS z_score,
    CASE WHEN ABS((d.row_count - s.avg_count) / NULLIF(s.std_count, 0)) > 3
         THEN 'ANOMALY' ELSE 'NORMAL' END AS status
FROM daily_stats d, stats s
WHERE d.dt = CURRENT_DATE();
```

## Seuils de qualité recommandés

| Type de données | Complétude | Unicité | Validité | Ponctualité |
|----------|--------|--------|--------|--------|
| Données transactionnelles cœur | 100% | 100% | 99,9% | 4h |
| Données de référence client | 99% | 100% | 99% | 8h |
| Journaux de comportement | 95% | — | 95% | 1h |
| Données tierces | 90% | — | 90% | 24h |
| Données archivées | 98% | 100% | 98% | — |

## Liste de contrôle

- [ ] Chaque table cœur couvre au moins les vérifications de complétude, d'unicité et de validité
- [ ] La détection d'anomalies est configurée pour les indicateurs métier clés
- [ ] Un chemin d'escalade en cas de défaillance est défini (qui / quand / comment notifier)
- [ ] Les vérifications de qualité sont intégrées au pipeline ETL
- [ ] Les rapports et tendances de qualité sont revus régulièrement (chaque semaine)
