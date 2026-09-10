---
name: data-warehouse-ops
description: "Compétence d'exploitation du cycle de vie complet d'un entrepôt de données (data warehouse / big data). Couvre 9 modules : définition de la source unique de vérité (SSOT), construction de pipelines ETL/ELT, modélisation dimensionnelle (étoile / flocon / Data Vault), contrôle de la qualité des données, stratégies de partitionnement, optimisation des coûts/performances, gouvernance des données, traçabilité du lignage et supervision des SLA. Prend en charge les principaux entrepôts cloud (BigQuery / Snowflake / Redshift / Databricks / StarRocks / ClickHouse) et la chaîne d'outils open source (dbt / Airflow / Great Expectations / OpenLineage / DataHub). Déclencheurs : entrepôt de données, data warehouse, DW, ETL, ELT, modélisation dimensionnelle, schéma en étoile, qualité des données, stratégie de partitionnement, optimisation d'entrepôt, gouvernance des données, traçabilité du lignage, supervision SLA, pipeline de données."
agent_created: true
---

# Compétence — Exploitation d'entrepôt de données (Data Warehouse Operations)

Assistant d'exploitation couvrant le cycle de vie complet d'un entrepôt de données, de la conception de l'architecture à la supervision quotidienne.

## Index des modules

Cette compétence comprend 9 grands modules de travail, accompagnés de scripts / références / ressources :

| Module | Mots-clés | Script | Document de référence |
|------|--------|------|----------|
| 1. Source unique de vérité | SSOT, standards de données | — | governance_framework.md |
| 2. Pipeline ETL/ELT | pipeline, dbt, Airflow | etl_pipeline_builder.py | sql_templates.md |
| 3. Modélisation dimensionnelle | schéma en étoile, Kimball | dim_model_generator.py | dimensional_modeling.md |
| 4. Qualité des données | DQ, Great Expectations | data_quality_checker.py | data_quality_rules.md |
| 5. Stratégie de partitionnement | partition, clustering | partition_advisor.py | partition_strategies.md |
| 6. Optimisation coûts/performances | coût, performance | cost_optimizer.py | partition_strategies.md |
| 7. Gouvernance des données | gouvernance, catalogue | — | governance_framework.md |
| 8. Traçabilité du lignage | lignage, OpenLineage | lineage_parser.py | — |
| 9. Supervision des SLA | SLA, fraîcheur, disponibilité | sla_monitor.py | sla_templates.md |

## Déroulement du travail

Lorsqu'un utilisateur formule un besoin lié à l'entrepôt de données, suivre ce déroulement :

### Phase 0 : Identification du besoin et routage

1. Analyser la demande de l'utilisateur et identifier le(s) module(s) concerné(s).
2. Si plusieurs modules sont concernés, les ordonner selon leurs dépendances (d'abord la modélisation → puis l'ETL → puis la qualité → puis l'optimisation → puis la supervision).
3. Confirmer la plateforme d'entrepôt cible (BigQuery / Snowflake / Redshift / StarRocks / ClickHouse / Databricks / autre).

### Phase 1 : Conception de l'architecture et modélisation (modules 1-3)

**Définition de la source unique de vérité (SSOT) :**
- Identifier les entités clés du domaine métier (client / produit / commande / fournisseur, etc.).
- Définir pour chaque entité la source de données faisant autorité et la norme de « golden record ».
- Produire la matrice SSOT : entité → système source → clé primaire → fréquence de mise à jour → responsable de la donnée (Owner).
- Charger `references/governance_framework.md` pour le modèle de conception SSOT.

**Modélisation dimensionnelle :**
- Utiliser `scripts/dim_model_generator.py` pour générer le DDL.
- Prend en charge le schéma en étoile (par défaut), le schéma en flocon, Data Vault 2.0.
- Génère automatiquement : tables de faits + tables de dimensions + clés de substitution + stratégies SCD Type 1/2/3.
- Paramètres à spécifier : `--schema star|snowflake|vault --scd-type 2 --platform bigquery`.
- Charger `references/dimensional_modeling.md` pour les bonnes pratiques de modélisation.

**Conception de pipeline ETL/ELT :**
- Utiliser `scripts/etl_pipeline_builder.py` pour générer un modèle de pipeline.
- Prend en charge trois formats de sortie : dbt / Airflow / SQL personnalisé.
- Inclut le chargement incrémental, la CDC, la gestion des erreurs et la logique de reprise.
- Charger `references/sql_templates.md` pour les patrons SQL standard.

### Phase 2 : Qualité et gouvernance des données (modules 4 et 7)

**Contrôle de la qualité des données :**
- Utiliser `scripts/data_quality_checker.py` pour générer les règles de contrôle.
- Couvre les 6 dimensions de la qualité : complétude, unicité, validité, cohérence, ponctualité, exactitude.
- Produit une suite Great Expectations (YAML) ou un script de contrôle en SQL pur.
- Charger `references/data_quality_rules.md` pour les modèles de règles prédéfinis.

**Gouvernance des données :**
- Charger `references/governance_framework.md`.
- Définir les domaines de données, les responsables (Owner) et les rôles d'intendance (data steward).
- Établir la stratégie de classification et de niveau de sensibilité des données (public / interne / confidentiel / secret).
- Définir les stratégies de rétention et d'archivage des données.

### Phase 3 : Optimisation des performances et des coûts (modules 5-6)

**Conception de la stratégie de partitionnement :**
- Utiliser `scripts/partition_advisor.py` pour analyser la structure des tables et recommander un schéma de partitionnement.
- Entrée : DDL de la table + description des modèles de requête.
- Sortie : instructions `PARTITION BY` / `CLUSTER BY` spécifiques à la plateforme.
- Charger `references/partition_strategies.md` pour les différences entre plateformes.

**Optimisation des coûts/performances :**
- Utiliser `scripts/cost_optimizer.py` pour analyser le coût des requêtes.
- Détecte : balayages de table complets, produits cartésiens, obliquité des données (data skew), jointures inefficaces.
- Sortie : recommandations d'optimisation (vues matérialisées, ajustement des clés de clustering, poussée de prédicats).
- Génère un rapport d'analyse de coûts HTML interactif (`assets/cost_report.html`).

### Phase 4 : Lignage et supervision (modules 8-9)

**Traçabilité du lignage :**
- Utiliser `scripts/lineage_parser.py` pour analyser le SQL et extraire le lignage au niveau colonne.
- Prend en charge : `INSERT...SELECT`, `CREATE TABLE AS`, `VIEW`, `MERGE`.
- Sortie : graphe au format DOT + visualisation HTML interactive (`assets/lineage_visualizer.html`).

**Supervision des SLA :**
- Utiliser `scripts/sla_monitor.py` pour générer un tableau de bord de supervision.
- Indicateurs supervisés : fraîcheur des données, durée d'exécution des pipelines, taux d'échec, variations de volume.
- Sortie : tableau de bord HTML (`assets/sla_dashboard.html`).
- Charger `references/sla_templates.md` pour les standards de définition des SLA.

## Utilisation des scripts

Tous les scripts se trouvent dans le répertoire `scripts/` et s'exécutent avec Python 3.9+.

### dim_model_generator.py — Générateur de DDL de modélisation dimensionnelle

```bash
python scripts/dim_model_generator.py \
  --business-domain "Commandes e-commerce" \
  --facts "orders:Faits de commande,order_items:Détail de commande" \
  --dimensions "customer:Client,dim_product:Produit,dim_date:Date,dim_store:Magasin" \
  --schema star \
  --scd-type 2 \
  --platform snowflake \
  --output ddl/
```

Description des paramètres :
- `--business-domain` : nom du domaine métier.
- `--facts` : définition des tables de faits, format `nom_table:description`.
- `--dimensions` : définition des tables de dimensions, format `nom_table:description`.
- `--schema` : paradigme de modélisation `star` (par défaut) | `snowflake` | `vault`.
- `--scd-type` : stratégie de dimension à évolution lente `1` | `2` | `3` | `hybrid`.
- `--platform` : plateforme cible `bigquery` | `snowflake` | `redshift` | `starrocks` | `clickhouse` | `databricks` | `postgres`.
- `--output` : répertoire de sortie.

### data_quality_checker.py — Moteur de contrôle de la qualité des données

```bash
python scripts/data_quality_checker.py \
  --table dwh.fact_orders \
  --platform bigquery \
  --checks "completeness,uniqueness,validity,freshness" \
  --format great_expectations \
  --threshold-file dq_thresholds.yaml \
  --output dq_checks/
```

Description des paramètres :
- `--table` : table cible (format `schema.table` pris en charge).
- `--platform` : plateforme cible.
- `--checks` : types de contrôle, séparés par des virgules. Pris en charge : completeness, uniqueness, validity, consistency, timeliness, accuracy, freshness, volume, custom.
- `--format` : format de sortie `great_expectations` | `sql` | `dbt_test` | `soda`.
- `--threshold-file` : fichier de configuration des seuils (facultatif).
- `--output` : répertoire de sortie.

### partition_advisor.py — Conseiller en stratégie de partitionnement

```bash
python scripts/partition_advisor.py \
  --ddl-file ddl/fact_orders.sql \
  --query-patterns "daily_report,monthly_trend,user_lookup" \
  --platform bigquery \
  --data-volume "10TB,500M rows" \
  --output recommendations/
```

Description des paramètres :
- `--ddl-file` : chemin du fichier DDL de la table.
- `--query-patterns` : description des modèles de requête.
- `--platform` : plateforme cible.
- `--data-volume` : ordre de grandeur du volume de données.
- `--output` : répertoire de sortie.

### cost_optimizer.py — Analyseur d'optimisation des coûts

```bash
python scripts/cost_optimizer.py \
  --query-log queries.json \
  --platform bigquery \
  --billing-data billing.csv \
  --output optimization_report/
```

Description des paramètres :
- `--query-log` : journal des requêtes (format JSON, avec query_text, bytes_processed, duration).
- `--platform` : plateforme cible.
- `--billing-data` : données de facturation (facultatif).
- `--output` : répertoire de sortie.

### lineage_parser.py — Analyseur de lignage SQL

```bash
python scripts/lineage_parser.py \
  --sql-dir sql/ \
  --output lineage/
```

Description des paramètres :
- `--sql-dir` : répertoire contenant les fichiers SQL.
- `--sql-file` : fichier SQL unique (alternatif à `--sql-dir`).
- `--output` : répertoire de sortie.
- `--level` : niveau de lignage `table` (par défaut) | `column`.

### sla_monitor.py — Générateur de tableau de bord de supervision SLA

```bash
python scripts/sla_monitor.py \
  --config sla_config.yaml \
  --pipeline-runs runs.csv \
  --output dashboard/
```

Description des paramètres :
- `--config` : fichier de configuration des SLA.
- `--pipeline-runs` : historique des exécutions de pipelines.
- `--output` : répertoire de sortie.

### etl_pipeline_builder.py — Générateur de modèles de pipeline ETL

```bash
python scripts/etl_pipeline_builder.py \
  --source-type mysql \
  --target-platform snowflake \
  --mode incremental \
  --cdc-method timestamp \
  --orchestrator airflow \
  --output pipelines/
```

## Index des documents de référence

Charger le fichier correspondant pour approfondir un sujet :

| Fichier | Contenu | Cas d'usage |
|------|------|----------|
| `references/dimensional_modeling.md` | Méthode Kimball en 4 étapes, stratégies SCD, types de tables de faits, patrons de conception de dimensions | Lors de la conception d'un modèle dimensionnel |
| `references/data_quality_rules.md` | Bibliothèque de règles de qualité selon 6 dimensions, modèles Great Expectations, règles de détection d'anomalies | Lors de la définition des contrôles de qualité |
| `references/sql_templates.md` | SQL de patrons ETL, fonctions de fenêtrage, MERGE/UPSERT, modèles de chargement incrémental | Lors de l'écriture de la logique ETL |
| `references/partition_strategies.md` | Comparaison du partitionnement par plateforme, stratégies de clustering, bonnes pratiques d'élagage de partitions | Lors de la conception d'un schéma de partitionnement |
| `references/governance_framework.md` | Modèle de définition SSOT, découpage en domaines de données, rôles et responsabilités, standards de classification | Lors de la définition d'une stratégie de gouvernance |
| `references/sla_templates.md` | Définition des indicateurs SLA, niveaux de fraîcheur, modèles de règles d'alerte | Lors de la mise en place d'un dispositif SLA |

## Conventions de sortie

Toutes les sorties de visualisation génèrent par défaut un rapport HTML interactif (utilisant Chart.js + mise en page responsive), avec les caractéristiques suivantes :
- Adaptation automatique au thème clair/sombre.
- Graphiques interactifs (zoom / filtrage / export).
- Étiquettes rédigées en français par défaut (langue de l'humain).
- Cartes de synthèse des indicateurs clés intégrées au rapport.

## Adaptation par plateforme

Le dialecte SQL est adapté automatiquement à la plateforme cible :

| Caractéristique | BigQuery | Snowflake | Redshift | StarRocks | ClickHouse |
|------|----------|-----------|----------|-----------|------------|
| Syntaxe de partitionnement | `PARTITION BY DATE(timestamp)` | micro-partitions automatiques | `DISTKEY`+`SORTKEY` | `PARTITION BY RANGE(dt)` | `PARTITION BY toYYYYMM(dt)` |
| Fusion incrémentale | `MERGE` | `MERGE` | `MERGE` (2023+) | `INSERT OVERWRITE` | `ALTER TABLE...UPDATE` |
| Vue matérialisée | ✅ | ✅ | ✅ (2023+) | ✅ asynchrone | ✅ |
| Semi-structuré | type `JSON` | `VARIANT` | `SUPER` | type `JSON` | type `JSON` |
| UDF | SQL/JS | SQL/JS/Python/Java | SQL/Python | UDF Java | SQL |
| Modèle de coût | par octets balayés | par crédit | par heure-nœud | open source gratuit | open source gratuit |

## Déclencheurs

**Déclencheurs (français)** : entrepôt de données, data warehouse, DW, ETL, ELT, modélisation dimensionnelle, schéma en étoile, schéma en flocon, qualité des données, stratégie de partitionnement, optimisation d'entrepôt, gouvernance des données, traçabilité du lignage, analyse de lignage, supervision SLA, exploitation d'entrepôt, pipeline de données, fraîcheur des données, vue matérialisée, dimension à évolution lente, SCD, clé de substitution, dimension conforme, catalogue de données, intendance des données, golden record, table de faits, table de dimensions, data lake, lakehouse.

**Déclencheurs (anglais)** : data warehouse, dimensional modeling, star schema, snowflake schema, data vault, ETL pipeline, ELT pipeline, data quality, DQ checks, partition strategy, data lineage, column lineage, SLA monitoring, data freshness, data governance, data catalog, surrogate key, slowly changing dimension, fact table, dimension table, data mart, data lakehouse.

Activer cette compétence lorsque le message de l'utilisateur contient l'un des mots-clés ci-dessus et concerne une opération de conception / construction / optimisation / contrôle / supervision.
