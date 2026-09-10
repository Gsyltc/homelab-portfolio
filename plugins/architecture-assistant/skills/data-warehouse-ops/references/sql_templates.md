# Bibliothèque de modèles SQL (SQL Templates for Data Warehouse)

## Modèles ETL courants

### 1. Chargement incrémentiel (Incremental Load)

```sql
-- Extraction incrémentielle basée sur l'horodatage
INSERT INTO dwh.fact_orders
SELECT *
FROM source.orders
WHERE updated_at > (
    SELECT COALESCE(MAX(updated_at), TIMESTAMP('2000-01-01'))
    FROM dwh.fact_orders
);
```

### 2. MERGE / UPSERT

```sql
-- BigQuery / Snowflake / Redshift
MERGE INTO dwh.dim_customer T
USING staging.dim_customer S
ON T.customer_bk = S.customer_bk AND T.is_current = TRUE
WHEN MATCHED AND T.name != S.name THEN
    UPDATE SET valid_to = CURRENT_TIMESTAMP(), is_current = FALSE
WHEN NOT MATCHED THEN
    INSERT (customer_sk, customer_bk, name, email, valid_from, valid_to, is_current)
    VALUES (GENERATE_UUID(), S.customer_bk, S.name, S.email, CURRENT_TIMESTAMP(), TIMESTAMP('9999-12-31'), TRUE);
```

### 3. Processus complet SCD Type 2

```sql
-- Étape 1 : Identifier les enregistrements modifiés
WITH changes AS (
    SELECT
        S.*,
        T.customer_sk AS existing_sk,
        CASE
            WHEN T.customer_sk IS NULL THEN 'NEW'
            WHEN S.name != T.name OR S.email != T.email THEN 'CHANGED'
            ELSE 'UNCHANGED'
        END AS change_type
    FROM staging.dim_customer S
    LEFT JOIN dwh.dim_customer T
        ON S.customer_bk = T.customer_bk AND T.is_current = TRUE
)
-- Étape 2 : Fermer l'ancienne version
UPDATE dwh.dim_customer T
SET valid_to = CURRENT_TIMESTAMP(), is_current = FALSE
FROM changes C
WHERE T.customer_sk = C.existing_sk AND C.change_type = 'CHANGED';

-- Étape 3 : Insérer la nouvelle version
INSERT INTO dwh.dim_customer
SELECT
    GENERATE_UUID(), customer_bk, name, email,
    CURRENT_TIMESTAMP(), TIMESTAMP('9999-12-31'), TRUE
FROM changes
WHERE change_type IN ('NEW', 'CHANGED');
```

### 4. Remplissage de la dimension de date

```sql
-- BigQuery : générer une dimension de date sur 10 ans
INSERT INTO dwh.dim_date
SELECT
    FORMAT_DATE('%Y%m%d', d) AS date_sk,
    DATE(d) AS full_date,
    EXTRACT(YEAR FROM d) AS year,
    EXTRACT(QUARTER FROM d) AS quarter,
    CONCAT('Q', EXTRACT(QUARTER FROM d)) AS quarter_name,
    EXTRACT(MONTH FROM d) AS month,
    FORMAT_DATE('%B', d) AS month_name,
    FORMAT_DATE('%b', d) AS month_abbr,
    EXTRACT(WEEK FROM d) AS week_of_year,
    EXTRACT(DAYOFWEEK FROM d) AS day_of_week,
    FORMAT_DATE('%A', d) AS day_name,
    FORMAT_DATE('%a', d) AS day_name_abbr,
    EXTRACT(DAYOFWEEK FROM d) IN (1, 7) AS is_weekend,
    FALSE AS is_holiday,
    EXTRACT(YEAR FROM DATE_ADD(d, INTERVAL 3 MONTH)) AS fiscal_year,
    EXTRACT(QUARTER FROM DATE_ADD(d, INTERVAL 3 MONTH)) AS fiscal_quarter
FROM UNNEST(GENERATE_DATE_ARRAY('2020-01-01', '2030-12-31')) AS d;
```

## Modèles courants de fonctions de fenêtrage

### Dédoublonnage en conservant le plus récent
```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) AS rn
    FROM source.orders
)
SELECT * EXCEPT(rn) FROM ranked WHERE rn = 1;
```

### Valeur cumulée (Running Total)
```sql
SELECT
    dt,
    daily_amount,
    SUM(daily_amount) OVER (ORDER BY dt ROWS UNBOUNDED PRECEDING) AS cumulative_amount,
    AVG(daily_amount) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d
FROM daily_summary;
```

### Comparaison sur un an / sur une période
```sql
SELECT
    dt,
    amount,
    LAG(amount, 1) OVER (ORDER BY dt) AS prev_day,
    LAG(amount, 7) OVER (ORDER BY dt) AS prev_week_same_day,
    LAG(amount, 30) OVER (ORDER BY dt) AS prev_month_same_day,
    ROUND(100.0 * (amount - LAG(amount, 1) OVER (ORDER BY dt)) / NULLIF(LAG(amount, 1) OVER (ORDER BY dt), 0), 2) AS dod_pct
FROM daily_metrics;
```

## SQL de qualité des données

### Détection des doublons
```sql
SELECT id, COUNT(*) AS dup_count
FROM dwh.fact_orders
GROUP BY id
HAVING COUNT(*) > 1
ORDER BY dup_count DESC
LIMIT 100;
```

### Détection des enregistrements orphelins
```sql
SELECT DISTINCT f.customer_id
FROM dwh.fact_orders f
LEFT JOIN dwh.dim_customer d ON f.customer_id = d.customer_bk
WHERE d.customer_bk IS NULL;
```

### Répartition des valeurs nulles
```sql
SELECT
    'total' AS metric, COUNT(*) AS value FROM dwh.fact_orders
UNION ALL
SELECT 'null_customer_id', COUNT(*) FROM dwh.fact_orders WHERE customer_id IS NULL
UNION ALL
SELECT 'null_amount', COUNT(*) FROM dwh.fact_orders WHERE amount IS NULL;
```

## SQL d'optimisation des performances

### Vérification de l'élagage de partition
```sql
-- BigQuery : vérifier si la requête utilise l'élagage de partition
SELECT
    query,
    total_bytes_processed,
    total_bytes_billed,
    cache_hit
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
ORDER BY total_bytes_processed DESC
LIMIT 10;
```

### Vue matérialisée
```sql
-- Vue matérialisée BigQuery
CREATE MATERIALIZED VIEW dwh.mv_daily_sales_summary AS
SELECT
    DATE(order_date) AS dt,
    product_category,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM dwh.fact_orders
GROUP BY dt, product_category;
```

## SQL d'administration et d'exploitation

### Statistiques de taille des tables
```sql
-- BigQuery
SELECT
    table_name,
    ROUND(size_bytes / POW(1024, 3), 2) AS size_gb,
    row_count
FROM `project`.dwh.__TABLES__
ORDER BY size_bytes DESC;
```

### Informations de partition
```sql
-- Statistiques de partition BigQuery
SELECT
    partition_id,
    ROUND(size_bytes / POW(1024, 3), 2) AS size_gb,
    row_count,
    TIMESTAMP_MILLIS(last_modified_time) AS last_modified
FROM `project`.dwh.INFORMATION_SCHEMA.PARTITIONS
WHERE table_name = 'fact_orders'
ORDER BY partition_id DESC
LIMIT 20;
```
