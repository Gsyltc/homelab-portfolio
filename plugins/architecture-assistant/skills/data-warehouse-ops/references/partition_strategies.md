# Référence des stratégies de partitionnement (Partition Strategies Reference)

## Comparaison des capacités de partitionnement par plateforme

| Caractéristique | BigQuery | Snowflake | Redshift | StarRocks | ClickHouse | Databricks |
|------|----------|-----------|----------|-----------|------------|------------|
| Mode de partitionnement | Plage temps/entier/temps d'ingestion | Micro-partitions automatiques | DISTKEY + SORTKEY | RANGE/LIST | RANGE/LIST | RANGE |
| Granularité de partition | HOUR/DAY/MONTH/YEAR | Automatique | Clé composite | HOUR/DAY/MONTH/YEAR | HOUR/DAY/MONTH | YEAR/MONTH/DAY |
| Nombre maximal de partitions | 4000 | Illimité | Illimité | 1024 | Recommandé < 1000 | Recommandé < 10000 |
| Support du clustering | CLUSTER BY (4 colonnes) | CLUSTER BY (4 colonnes) | SORTKEY composite (8 colonnes) | Bucketing (BUCKETS) | ORDER BY | Z-ORDER |
| Élagage de partition | Automatique | Automatique (micro-partitions) | Manuel (SORTKEY) | Automatique | Automatique | Automatique |
| Impact sur les coûts | À l'octet scanné | Au credit | À l'heure-nœud | Gratuit (open source) | Gratuit (open source) | Au DBU |

## Stratégie de partitionnement BigQuery

### Modèle recommandé
```sql
-- Modèle standard : partition par date + clustering
CREATE TABLE dwh.fact_orders (
    order_id STRING,
    customer_id INT64,
    product_id INT64,
    order_date DATE,
    total_amount NUMERIC,
    ...
)
PARTITION BY DATE(order_date)
CLUSTER BY customer_id, product_id;
```

### Arbre de décision du choix de partition
1. Y a-t-il une colonne date/heure ? → `PARTITION BY DATE(timestamp_col)` (granularité DAY)
2. Les données sont-elles organisées par temps d'ingestion ? → `PARTITION BY _PARTITIONDATE` (partition par temps d'ingestion)
3. Uniquement un ID entier ? → `PARTITION BY RANGE_BUCKET(id, GENERATE_ARRAY(0, 1000000, 1000))`

### Choix des colonnes de clustering
- Colonnes fréquemment utilisées dans le filtre WHERE (hors colonnes de partition)
- Clés de JOIN
- Colonnes de GROUP BY / ORDER BY
- 50 k à 500 k lignes par bloc de clustering donnent le meilleur effet

### Remarques
- Configuration de l'expiration des partitions : `OPTIONS(partition_expiration_days=90)`
- Exiger un filtre de partition : `OPTIONS(require_partition_filter=TRUE)`
- Quota gratuit de 1 To de scan par jour

## Stratégie de partitionnement Snowflake

### Micro-partitions automatiques
Snowflake organise automatiquement les données en micro-partitions (50-500 Mo non compressées), sans déclaration manuelle de partition.

### Clustering (optionnel)
```sql
-- Clustering explicite pour accélérer les requêtes
CREATE TABLE dwh.fact_orders
CLUSTER BY (order_date, customer_id);
```

### Conseils de clustering
- Le clustering est efficace sur les colonnes à forte cardinalité (des millions de valeurs distinctes)
- Colonnes fréquemment utilisées dans les JOIN
- Colonnes de filtre WHERE
- Éviter le clustering sur les colonnes fréquemment mises à jour

### Surveillance
```sql
-- Consulter la profondeur de clustering (plus petit = mieux)
SELECT SYSTEM$CLUSTERING_INFORMATION('dwh.fact_orders');
-- Consulter le ratio de clustering (> 2 peut nécessiter un re-clustering)
SELECT SYSTEM$CLUSTERING_RATIO('dwh.fact_orders');
```

## Stratégie de partitionnement Redshift

### DISTKEY + SORTKEY
```sql
CREATE TABLE dwh.fact_orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date DATE,
    ...
)
DISTKEY(customer_id)          -- Répartition entre les nœuds
COMPOUND SORTKEY(order_date, customer_id);  -- Tri au sein du nœud
```

### Choix de la DISTKEY
- Choisir la colonne la plus fréquemment utilisée en JOIN
- Éviter les colonnes fortement asymétriques (une valeur représente > 25%)
- Privilégier les colonnes à forte fréquence de filtrage
- Vérifier l'asymétrie : `SELECT distkey, COUNT(*) FROM table GROUP BY distkey`

### Choix de la SORTKEY
- 1re colonne : la colonne date la plus souvent utilisée en filtrage de plage
- Colonnes suivantes : par ordre décroissant de fréquence de requête
- Une SORTKEY composite compte au maximum 8 colonnes
- Exécuter régulièrement VACUUM et ANALYZE

### Optimisation automatique des tables (ATO)
```sql
-- Activer l'optimisation automatique Redshift
ALTER TABLE dwh.fact_orders ALTER SORTKEY AUTO;
ALTER TABLE dwh.fact_orders ALTER DISTSTYLE AUTO;
```

## Stratégie de partitionnement StarRocks

### Partition + bucketing
```sql
CREATE TABLE dwh.fact_orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date DATE,
    amount DECIMAL(18,2)
)
PARTITION BY RANGE(order_date) (
    PARTITION p202401 VALUES LESS THAN ("2024-02-01"),
    PARTITION p202402 VALUES LESS THAN ("2024-03-01"),
    PARTITION p202403 VALUES LESS THAN ("2024-04-01")
)
DISTRIBUTED BY HASH(order_id) BUCKETS 32;
```

### Partitionnement dynamique
```sql
-- Création et suppression automatiques de partitions
ALTER TABLE dwh.fact_orders
SET (
    "dynamic_partition.enable" = "true",
    "dynamic_partition.time_unit" = "MONTH",
    "dynamic_partition.start" = "-3",   -- Conserver les 3 derniers mois
    "dynamic_partition.end" = "1",      -- Créer à l'avance le mois suivant
    "dynamic_partition.prefix" = "p",
    "dynamic_partition.buckets" = "32"
);
```

### Choix de la clé de bucketing
- Colonne à forte cardinalité (beaucoup de valeurs distinctes)
- Colonne à distribution homogène
- Colonne souvent utilisée dans les JOIN d'égalité
- Recommandé : une puissance de 2

## Stratégie de partitionnement ClickHouse

### Partition + clé de tri
```sql
CREATE TABLE dwh.fact_orders (
    order_id UInt64,
    customer_id UInt64,
    order_date Date,
    amount Decimal(18,2)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(order_date)
ORDER BY (customer_id, order_date);
```

### Bonnes pratiques
- Granularité de partition : MONTH est la plus courante (ne pas être trop fin)
- ORDER BY est l'index de clé primaire → trier par fréquence de requête
- Nettoyage automatique par TTL : `TTL order_date + INTERVAL 12 MONTH DELETE`
- Ne pas dépasser 1000 partitions

## Stratégie de partitionnement Databricks (Delta Lake)

### Partition + Z-Ordering
```sql
CREATE TABLE dwh.fact_orders
USING DELTA
PARTITIONED BY (order_year, order_month)
LOCATION '/mnt/dwh/fact_orders';

-- Z-Ordering pour accélérer le filtrage multidimensionnel
OPTIMIZE dwh.fact_orders ZORDER BY (customer_id, product_id);
```

### Bonnes pratiques
- Cardinalité modérée des colonnes de partition (au moins 1 Go de données par partition)
- Éviter le problème des petits fichiers — utiliser Auto Optimize
- Choisir des colonnes de filtre à forte cardinalité pour le Z-Ordering
- Exécuter régulièrement OPTIMIZE : `OPTIMIZE dwh.fact_orders`

## Arbre de décision du choix de stratégie de partitionnement

```
Y a-t-il une dimension temporelle ?
├── Oui → partitionner par temps (DAY/MONTH)
│   ├── Les requêtes portent-elles toujours un filtre temporel ? → partition temporelle + clustering des autres colonnes
│   └── Écriture haute fréquence + requête en temps réel ? → partition à la granularité HOUR
├── Non → partitionner par clé métier
│   ├── partitionner par région/tenant (isolation multi-tenant)
│   └── ne pas partitionner, seulement clustering des colonnes à forte fréquence de requête
└── Cas particuliers
    ├── ETL incrémentiel → utiliser la partition par temps d'ingestion
    └── archivage des données → partition par année + suppression automatique par TTL
```

## Liste de contrôle des stratégies de partitionnement

- [ ] La colonne de partition est-elle souvent utilisée dans le filtre WHERE ?
- [ ] La granularité de partition est-elle adaptée (ni trop grossière, ni trop fine) ?
- [ ] Une stratégie d'expiration/nettoyage automatique des partitions est-elle configurée ?
- [ ] Les colonnes de clustering couvrent-elles les principales opérations de JOIN et de GROUP BY ?
- [ ] A-t-on évité le partitionnement sur des clés à forte cardinalité (comme user_id) ?
- [ ] Le paramètre require_partition_filter est-il configuré pour éviter un scan complet accidentel ?
- [ ] L'asymétrie des données de partition est-elle surveillée ?
