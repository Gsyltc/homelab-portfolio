#!/usr/bin/env python3
"""
Moteur de contrôle de la qualité des données — Data Quality Checker
Prend en charge la génération automatique de règles pour les 6 grandes dimensions de qualité,
et produit des formats Great Expectations / SQL / test dbt / Soda.
"""

import argparse
import json
import os
import sys
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any

# ── Définition des dimensions de qualité ──────────────────────────────────────────────────

QUALITY_DIMENSIONS = {
    "completeness": {
        "name": "Complétude (Completeness)",
        "description": "Vérifie si les champs obligatoires sont vides",
        "severity": "CRITICAL",
        "checks": ["not_null", "missing_rate", "row_count_check"],
        "default_threshold": {"not_null_pct": 99.0, "missing_max_pct": 1.0},
    },
    "uniqueness": {
        "name": "Unicité (Uniqueness)",
        "description": "Vérifie si la clé primaire / la clé métier est unique",
        "severity": "CRITICAL",
        "checks": ["unique", "duplicate_count", "pk_composite_unique"],
        "default_threshold": {"unique_pct": 100.0, "max_duplicates": 0},
    },
    "validity": {
        "name": "Validité (Validity)",
        "description": "Vérifie si le format/la plage des données respecte les règles métier",
        "severity": "HIGH",
        "checks": ["regex_match", "range_check", "enum_values", "date_format", "email_format"],
        "default_threshold": {"valid_pct": 95.0},
    },
    "consistency": {
        "name": "Cohérence (Consistency)",
        "description": "Vérifie si les données sont cohérentes entre tables/systèmes",
        "severity": "HIGH",
        "checks": ["referential_integrity", "cross_table_match", "aggregate_consistency"],
        "default_threshold": {"match_pct": 98.0},
    },
    "timeliness": {
        "name": "Ponctualité (Timeliness)",
        "description": "Vérifie si les données arrivent dans les délais",
        "severity": "MEDIUM",
        "checks": ["freshness_check", "max_delay", "expected_arrival"],
        "default_threshold": {"max_delay_hours": 4, "on_time_pct": 99.0},
    },
    "accuracy": {
        "name": "Exactitude (Accuracy)",
        "description": "Vérifie si les données reflètent les valeurs métier réelles",
        "severity": "HIGH",
        "checks": ["statistical_outlier", "zscore_check", "variance_from_avg", "sum_check"],
        "default_threshold": {"zscore_threshold": 3.0, "deviation_pct": 10.0},
    },
    "freshness": {
        "name": "Fraîcheur (Freshness)",
        "description": "Vérifie la date de dernière mise à jour des données",
        "severity": "MEDIUM",
        "checks": ["max_data_age", "stale_partition_check", "no_new_data_alert"],
        "default_threshold": {"max_age_hours": 24, "empty_partitions": 0},
    },
    "volume": {
        "name": "Volume (Volume)",
        "description": "Vérifie si le volume de données fluctue anormalement",
        "severity": "MEDIUM",
        "checks": ["row_count_anomaly", "volume_change_pct", "zero_row_check"],
        "default_threshold": {"anomaly_threshold_pct": 50, "min_rows": 1},
    },
    "custom": {
        "name": "Personnalisé (Custom SQL)",
        "description": "Contrôle SQL personnalisé défini par l'utilisateur",
        "severity": "HIGH",
        "checks": ["custom_sql"],
        "default_threshold": {},
    },
}

def parse_args():
    parser = argparse.ArgumentParser(description="Moteur de contrôle de la qualité des données")
    parser.add_argument("--table", type=str, required=True,
                        help="Nom de la table cible (schema.table)")
    parser.add_argument("--platform", type=str, default="bigquery",
                        choices=["bigquery", "snowflake", "redshift", "starrocks", "clickhouse", "databricks", "postgres"])
    parser.add_argument("--checks", type=str, default="completeness,uniqueness,validity",
                        help="Types de contrôle, séparés par des virgules")
    parser.add_argument("--format", type=str, default="sql",
                        choices=["great_expectations", "sql", "dbt_test", "soda"])
    parser.add_argument("--threshold-file", type=str, default=None,
                        help="Fichier de configuration des seuils (YAML)")
    parser.add_argument("--output", type=str, default="dq_checks/",
                        help="Répertoire de sortie")
    parser.add_argument("--columns", type=str, default=None,
                        help="Colonnes à contrôler, séparées par des virgules (toutes par défaut)")
    parser.add_argument("--pk-column", type=str, default="id",
                        help="Nom de la colonne de clé primaire")
    parser.add_argument("--date-column", type=str, default="created_at",
                        help="Nom de la colonne de date")
    return parser.parse_args()


def load_thresholds(file_path: str | None) -> dict:
    """Charge le fichier de configuration des seuils."""
    thresholds = {}
    if file_path and os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            thresholds = yaml.safe_load(f) or {}
    return thresholds


def generate_sql_checks(
    table: str,
    checks: List[str],
    platform: str,
    pk_column: str,
    date_column: str,
    columns: List[str] | None,
    thresholds: dict,
) -> str:
    """Génère des contrôles de qualité des données au format SQL pur."""

    # Fonctions spécifiques à la plateforme
    platform_funcs = {
        "bigquery": {"current_ts": "CURRENT_TIMESTAMP()", "array_agg": "ARRAY_AGG", "safe_div": "SAFE_DIVIDE"},
        "snowflake": {"current_ts": "CURRENT_TIMESTAMP()", "array_agg": "ARRAY_AGG", "safe_div": "DIV0"},
        "redshift": {"current_ts": "GETDATE()", "array_agg": "LISTAGG", "safe_div": "NULLIF"},
        "postgres": {"current_ts": "NOW()", "array_agg": "ARRAY_AGG", "safe_div": "NULLIF"},
    }
    funcs = platform_funcs.get(platform, platform_funcs["bigquery"])
    ct = funcs["current_ts"]

    sql = f"""-- ============================================================
-- Data Quality Checks for: {table}
-- Platform: {platform}
-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- ============================================================

"""

    # 1. Contrôle de complétude
    if "completeness" in checks:
        t = thresholds.get("completeness", {})
        null_pct = t.get("not_null_pct", 99.0)
        sql += f"""
-- [COMPLETENESS] Not Null Rate Check
SELECT
    '{table}' AS table_name,
    'completeness' AS check_type,
    'not_null_rate' AS check_name,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN {pk_column} IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN {pk_column} IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct,
    CASE WHEN ROUND(100.0 * SUM(CASE WHEN {pk_column} IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) > {100 - null_pct}
         THEN 'FAIL' ELSE 'PASS' END AS status
FROM {table};
"""
        if columns:
            sql += f"""
-- [COMPLETENESS] Column-level missing rate
SELECT
"""
            col_checks = []
            for col in columns:
                col_checks.append(
                    f"    ROUND(100.0 * SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS {col}_missing_pct"
                )
            sql += ",\n".join(col_checks)
            sql += f"\nFROM {table};\n"

    # 2. Contrôle d'unicité
    if "uniqueness" in checks:
        sql += f"""
-- [UNIQUENESS] Primary Key Uniqueness
SELECT
    '{table}' AS table_name,
    'uniqueness' AS check_type,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT {pk_column}) AS distinct_pks,
    COUNT(*) - COUNT(DISTINCT {pk_column}) AS duplicate_count,
    CASE WHEN COUNT(*) = COUNT(DISTINCT {pk_column})
         THEN 'PASS' ELSE 'FAIL' END AS status
FROM {table};
"""
        sql += f"""
-- [UNIQUENESS] Duplicate Detail (Top 100)
SELECT {pk_column}, COUNT(*) AS dup_count
FROM {table}
GROUP BY {pk_column}
HAVING COUNT(*) > 1
ORDER BY dup_count DESC
LIMIT 100;
"""

    # 3. Contrôle de validité
    if "validity" in checks:
        sql += f"""
-- [VALIDITY] Range Check Example
-- Vérifier si les colonnes numériques sont dans une plage raisonnable
"""
        if columns:
            for col in columns:
                sql += f"""
-- Check: {col} IS NOT NULL AND {col} >= 0
SELECT
    '{col}' AS column_name,
    COUNT(*) AS total,
    SUM(CASE WHEN {col} < 0 OR {col} IS NULL THEN 1 ELSE 0 END) AS invalid_count,
    ROUND(100.0 * SUM(CASE WHEN {col} < 0 OR {col} IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS invalid_pct
FROM {table};
"""
        sql += f"""
-- [VALIDITY] Date Format Check
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN SAFE.PARSE_DATE('%Y-%m-%d', CAST({date_column} AS STRING)) IS NULL THEN 1 ELSE 0 END) AS invalid_date_count
FROM {table};
"""

    # 4. Contrôle de ponctualité/fraîcheur
    if "timeliness" in checks or "freshness" in checks:
        t = thresholds.get("timeliness", thresholds.get("freshness", {}))
        max_hours = t.get("max_delay_hours", t.get("max_age_hours", 24))
        sql += f"""
-- [TIMELINESS] Data Freshness Check
SELECT
    '{table}' AS table_name,
    'freshness' AS check_type,
    MAX({date_column}) AS latest_record,
    TIMESTAMP_DIFF({ct}, MAX({date_column}), HOUR) AS hours_since_latest,
    CASE WHEN TIMESTAMP_DIFF({ct}, MAX({date_column}), HOUR) <= {max_hours}
         THEN 'PASS' ELSE 'FAIL' END AS status
FROM {table};
"""

    # 5. Contrôle du volume de données
    if "volume" in checks:
        t = thresholds.get("volume", {})
        min_rows = t.get("min_rows", 1)
        sql += f"""
-- [VOLUME] Row Count Check
SELECT
    '{table}' AS table_name,
    'volume' AS check_type,
    COUNT(*) AS row_count,
    CASE WHEN COUNT(*) >= {min_rows} THEN 'PASS' ELSE 'FAIL' END AS status
FROM {table};
"""

    # 6. Contrôle d'anomalies statistiques
    if "accuracy" in checks:
        t = thresholds.get("accuracy", {})
        zscore_threshold = t.get("zscore_threshold", 3.0)
        if columns:
            for col in columns:
                sql += f"""
-- [ACCURACY] Z-Score Outlier Check for {col}
WITH stats AS (
    SELECT
        AVG({col}) AS mean_val,
        STDDEV({col}) AS std_val
    FROM {table}
    WHERE {col} IS NOT NULL
),
outliers AS (
    SELECT
        {pk_column},
        {col},
        ({col} - stats.mean_val) / NULLIF(stats.std_val, 0) AS z_score
    FROM {table}, stats
    WHERE {col} IS NOT NULL
      AND ABS(({col} - stats.mean_val) / NULLIF(stats.std_val, 0)) > {zscore_threshold}
)
SELECT
    COUNT(*) AS outlier_count,
    ROUND(100.0 * COUNT(*) / NULLIF((SELECT COUNT(*) FROM {table}), 0), 2) AS outlier_pct,
    CASE WHEN COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM {table}), 0) < 5.0
         THEN 'PASS' ELSE 'WARN' END AS status
FROM outliers;
"""

    return sql


def generate_great_expectations(
    table: str,
    checks: List[str],
    platform: str,
    pk_column: str,
    date_column: str,
    columns: List[str] | None,
    thresholds: dict,
) -> str:
    """Génère un suite Great Expectations au format YAML."""
    suite_name = table.replace(".", "_").replace("`", "")
    yml = f"""# Great Expectations Expectation Suite
# Generated for: {table} ({platform})
# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

suite_name: {suite_name}_quality_suite
data_asset_type: Table

expectations:
"""
    # Complétude
    if "completeness" in checks:
        t = thresholds.get("completeness", {})
        expect_pct = t.get("not_null_pct", 99.0) / 100.0
        yml += f"""
  # === COMPLETENESS ===
  - expectation_type: expect_column_values_to_not_be_null
    kwargs:
      column: {pk_column}
      mostly: {expect_pct}
    meta:
      dimension: completeness
      severity: critical
"""
        if columns:
            for col in columns:
                yml += f"""  - expectation_type: expect_column_values_to_not_be_null
    kwargs:
      column: {col}
      mostly: {expect_pct}
    meta:
      dimension: completeness
"""

    # Unicité
    if "uniqueness" in checks:
        yml += f"""
  # === UNIQUENESS ===
  - expectation_type: expect_column_values_to_be_unique
    kwargs:
      column: {pk_column}
    meta:
      dimension: uniqueness
      severity: critical
"""

    # Validité
    if "validity" in checks:
        yml += f"""
  # === VALIDITY ===
  - expectation_type: expect_column_values_to_be_of_type
    kwargs:
      column: {pk_column}
      type_: varchar
      or_other_types: [int, integer]
    meta:
      dimension: validity
"""

    # Fraîcheur
    if "freshness" in checks or "timeliness" in checks:
        yml += f"""
  # === FRESHNESS ===
  - expectation_type: expect_column_max_to_be_between
    kwargs:
      column: {date_column}
      min_value: "{{{{ now() - timedelta(days=1) }}}}"
      max_value: "{{{{ now() }}}}"
    meta:
      dimension: freshness
      severity: warning
"""

    # Volume de données
    if "volume" in checks:
        t = thresholds.get("volume", {})
        min_rows = t.get("min_rows", 1)
        yml += f"""
  # === VOLUME ===
  - expectation_type: expect_table_row_count_to_be_between
    kwargs:
      min_value: {min_rows}
      max_value: 1000000000
    meta:
      dimension: volume
"""

    return yml


def generate_dbt_tests(
    table: str,
    checks: List[str],
    platform: str,
    pk_column: str,
    date_column: str,
    columns: List[str] | None,
    thresholds: dict,
) -> str:
    """Génère des tests dbt au format YAML."""
    model_name = table.split(".")[-1] if "." in table else table
    yml = f"""# dbt Tests for model: {model_name}
# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

version: 2

models:
  - name: {model_name}
    description: "Data quality tests for {table}"
    columns:
"""
    yml += f"""      - name: {pk_column}
        description: "Primary key"
        tests:
          - not_null
          - unique
"""

    if "freshness" in checks or "timeliness" in checks:
        yml += f"""      - name: {date_column}
        description: "Record timestamp"
        tests:
          - not_null
"""

    if columns:
        for col in columns:
            if col == pk_column or col == date_column:
                continue
            yml += f"""      - name: {col}
        tests:
          - not_null:
              config:
                severity: warn
"""

    if "validity" in checks:
        yml += f"""
    # Custom data tests (place in tests/generic/)
    # tests:
    #   - dbt_utils.expression_is_true:
    #       expression: "amount >= 0"
"""
    return yml


def generate_soda_checks(
    table: str,
    checks: List[str],
    platform: str,
    pk_column: str,
    date_column: str,
    columns: List[str] | None,
    thresholds: dict,
) -> str:
    """Génère des contrôles SodaCL au format YAML."""
    yml = f"""# SodaCL Checks for {table}
# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

checks for {table}:
"""
    if "completeness" in checks:
        yml += f"""
  # Completeness
  - missing_count({pk_column}) = 0:
      name: PK must not be null
      fail: when > 0
"""

    if "uniqueness" in checks:
        yml += f"""
  # Uniqueness
  - duplicate_count({pk_column}) = 0:
      name: PK must be unique
"""

    if "freshness" in checks or "timeliness" in checks:
        yml += f"""
  # Freshness
  - freshness({date_column}) < 1d:
      name: Data must be less than 1 day old
"""

    if "volume" in checks:
        t = thresholds.get("volume", {})
        min_rows = t.get("min_rows", 1)
        yml += f"""
  # Volume
  - row_count > {min_rows}:
      name: Table must have data
"""

    if "validity" in checks:
        yml += f"""
  # Validity (customize per column)
  - invalid_count({pk_column}) = 0:
      valid_format: uuid
      name: PK must be valid format
"""

    if columns:
        for col in columns:
            if col == pk_column or col == date_column:
                continue
            yml += f"""  - missing_count({col}) < 100:
      name: {col} should have minimal nulls
"""

    return yml


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    checks = [c.strip() for c in args.checks.split(",")]
    invalid = [c for c in checks if c not in QUALITY_DIMENSIONS]
    if invalid:
        print(f"⚠️  Type de contrôle inconnu : {invalid}")
        print(f"Types de contrôle disponibles : {list(QUALITY_DIMENSIONS.keys())}")
        checks = [c for c in checks if c in QUALITY_DIMENSIONS]

    thresholds = load_thresholds(args.threshold_file)
    # Fusionner les seuils par défaut
    for dim_name, dim_info in QUALITY_DIMENSIONS.items():
        if dim_name not in thresholds:
            thresholds[dim_name] = dim_info["default_threshold"]

    columns = args.columns.split(",") if args.columns else None
    cols_clean = [c.strip() for c in columns] if columns else None

    # Générer le format correspondant
    generators = {
        "sql": generate_sql_checks,
        "great_expectations": generate_great_expectations,
        "dbt_test": generate_dbt_tests,
        "soda": generate_soda_checks,
    }

    ext_map = {"sql": "sql", "great_expectations": "yml", "dbt_test": "yml", "soda": "yml"}

    generator = generators[args.format]
    content = generator(
        table=args.table,
        checks=checks,
        platform=args.platform,
        pk_column=args.pk_column,
        date_column=args.date_column,
        columns=cols_clean,
        thresholds=thresholds,
    )

    ext = ext_map[args.format]
    safe_name = args.table.replace(".", "_").replace("`", "")
    output_file = os.path.join(args.output, f"{safe_name}_dq.{ext}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Contrôles de qualité des données générés : {output_file}")
    print(f"📋 Dimensions de contrôle : {', '.join(checks)}")
    print(f"🔧 Format de sortie : {args.format}")
    print(f"☁️  Plateforme cible : {args.platform}")

    # Générer le résumé
    summary = {
        "table": args.table,
        "platform": args.platform,
        "format": args.format,
        "checks": checks,
        "generated_at": datetime.now().isoformat(),
        "output_file": output_file,
    }
    summary_file = os.path.join(args.output, f"{safe_name}_dq_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"📄 Résumé : {summary_file}")


if __name__ == "__main__":
    main()
