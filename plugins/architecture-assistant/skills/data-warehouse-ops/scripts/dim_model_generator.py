#!/usr/bin/env python3
"""
Générateur de DDL de modélisation dimensionnelle — Dimension Model DDL Generator
Prend en charge le modèle en étoile (Snowflake/BigQuery/Redshift/StarRocks/ClickHouse/Databricks/Postgres)
et le paradigme de modélisation Data Vault 2.0.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ── Configuration des dialectes SQL par plateforme ──────────────────────────────────────────

PLATFORM_DIALECTS = {
    "bigquery": {
        "pk": "STRING",
        "fk": "INT64",
        "int": "INT64",
        "decimal": "NUMERIC",
        "text": "STRING",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "boolean": "BOOL",
        "json": "JSON",
        "array": "ARRAY<STRING>",
        "scd2_struct": "STRUCT<valid_from TIMESTAMP, valid_to TIMESTAMP, is_current BOOL>",
        "auto_increment": "INT64",  # BigQuery uses GENERATE_UUID() for surrogate keys
        "surrogate_key": "GENERATE_UUID()",
        "table_comment": "OPTIONS(description=\"{comment}\")",
        "partition": "PARTITION BY DATE({col})",
        "cluster": "CLUSTER BY {cols}",
        "create_syntax": "CREATE OR REPLACE TABLE",
        "merge_syntax": "MERGE",
    },
    "snowflake": {
        "pk": "VARCHAR",
        "fk": "NUMBER",
        "int": "NUMBER",
        "decimal": "NUMBER(38,2)",
        "text": "VARCHAR(16777216)",
        "date": "DATE",
        "timestamp": "TIMESTAMP_NTZ",
        "boolean": "BOOLEAN",
        "json": "VARIANT",
        "array": "ARRAY",
        "scd2_struct": "OBJECT",
        "auto_increment": "NUMBER AUTOINCREMENT",
        "surrogate_key": "SEQ4()",
        "table_comment": "COMMENT = '{comment}'",
        "partition": "",  # Auto micro-partitions
        "cluster": "CLUSTER BY ({cols})",
        "create_syntax": "CREATE OR REPLACE TABLE",
        "merge_syntax": "MERGE INTO",
    },
    "redshift": {
        "pk": "VARCHAR(256)",
        "fk": "BIGINT",
        "int": "BIGINT",
        "decimal": "DECIMAL(18,2)",
        "text": "VARCHAR(65535)",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "boolean": "BOOLEAN",
        "json": "SUPER",
        "array": "SUPER",
        "scd2_struct": "SUPER",
        "auto_increment": "BIGINT IDENTITY(1,1)",
        "surrogate_key": "IDENTITY(1,1)",
        "table_comment": "COMMENT ON TABLE {table} IS '{comment}'",
        "partition": "DISTKEY({col})",
        "cluster": "SORTKEY({cols})",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "MERGE",
    },
    "starrocks": {
        "pk": "VARCHAR",
        "fk": "BIGINT",
        "int": "BIGINT",
        "decimal": "DECIMAL(18,2)",
        "text": "STRING",
        "date": "DATE",
        "timestamp": "DATETIME",
        "boolean": "BOOLEAN",
        "json": "JSON",
        "array": "ARRAY<STRING>",
        "scd2_struct": "JSON",
        "auto_increment": "BIGINT",
        "surrogate_key": "uuid()",
        "table_comment": "COMMENT \"{comment}\"",
        "partition": "PARTITION BY RANGE({col})",
        "cluster": "",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "",  # Use INSERT OVERWRITE
    },
    "clickhouse": {
        "pk": "String",
        "fk": "Int64",
        "int": "Int64",
        "decimal": "Decimal(18,2)",
        "text": "String",
        "date": "Date",
        "timestamp": "DateTime",
        "boolean": "Bool",
        "json": "JSON",
        "array": "Array(String)",
        "scd2_struct": "Tuple(valid_from DateTime, valid_to DateTime, is_current UInt8)",
        "auto_increment": "Int64",
        "surrogate_key": "generateUUIDv4()",
        "table_comment": "COMMENT '{comment}'",
        "partition": "PARTITION BY toYYYYMM({col})",
        "cluster": "ORDER BY ({cols})",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "ALTER TABLE ... UPDATE",
    },
    "databricks": {
        "pk": "STRING",
        "fk": "BIGINT",
        "int": "BIGINT",
        "decimal": "DECIMAL(18,2)",
        "text": "STRING",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "boolean": "BOOLEAN",
        "json": "STRING",
        "array": "ARRAY<STRING>",
        "scd2_struct": "STRUCT<valid_from: TIMESTAMP, valid_to: TIMESTAMP, is_current: BOOLEAN>",
        "auto_increment": "BIGINT",
        "surrogate_key": "uuid()",
        "table_comment": "COMMENT '{comment}'",
        "partition": "PARTITIONED BY ({col})",
        "cluster": "CLUSTER BY ({cols})",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "MERGE INTO",
    },
    "postgres": {
        "pk": "VARCHAR",
        "fk": "BIGINT",
        "int": "BIGINT",
        "decimal": "NUMERIC(18,2)",
        "text": "TEXT",
        "date": "DATE",
        "timestamp": "TIMESTAMPTZ",
        "boolean": "BOOLEAN",
        "json": "JSONB",
        "array": "JSONB",
        "scd2_struct": "JSONB",
        "auto_increment": "BIGSERIAL",
        "surrogate_key": "nextval('{table}_sk_seq')",
        "table_comment": "COMMENT ON TABLE {table} IS '{comment}'",
        "partition": "PARTITION BY RANGE ({col})",
        "cluster": "",
        "create_syntax": "CREATE TABLE IF NOT EXISTS",
        "merge_syntax": "INSERT ... ON CONFLICT",
    },
}

# ── Stratégies SCD ─────────────────────────────────────────────────────

SCD_STRATEGIES = {
    1: {
        "name": "Type 1 — Écrasement (Overwrite)",
        "description": "Met à jour directement les attributs de la dimension, sans conserver l'historique",
        "extra_cols": [],
        "strategy_sql": "UPDATE {table} SET {updates} WHERE {business_key} = :bk",
    },
    2: {
        "name": "Type 2 — Ajout de ligne (Add Row)",
        "description": "Ajoute une ligne pour conserver l'historique, avec période de validité marquée par valid_from/valid_to",
        "extra_cols": [
            ("sk_id", "pk"),           # Clé de substitution
            ("valid_from", "timestamp"),
            ("valid_to", "timestamp"),
            ("is_current", "boolean"),
        ],
        "strategy_sql": "INSERT + UPDATE is_current=0, valid_to=NOW()",
    },
    3: {
        "name": "Type 3 — Ajout de colonne (Add Column)",
        "description": "Ajoute une colonne pour conserver la valeur précédente",
        "extra_cols": [
            ("previous_value", "text"),
            ("effective_date", "date"),
        ],
        "strategy_sql": "UPDATE {table} SET previous_value = {col}, {col} = :new_val",
    },
    "hybrid": {
        "name": "Hybrid (Type 1 + Type 2)",
        "description": "La plupart des attributs en Type 1 (écrasement), les attributs clés en Type 2 (historique conservé)",
        "extra_cols": [
            ("sk_id", "pk"),
            ("valid_from", "timestamp"),
            ("valid_to", "timestamp"),
            ("is_current", "boolean"),
        ],
        "strategy_sql": "Traitement mixte selon la classification des attributs",
    },
}

# ── Types de tables de faits ────────────────────────────────────────────────────

FACT_TYPES = {
    "transaction": "Table de faits transactionnelle — enregistre les événements métier, granularité = un événement",
    "periodic_snapshot": "Table de faits par instantané périodique — enregistre l'état à intervalle fixe, granularité = période + dimension",
    "accumulating_snapshot": "Table de faits par instantané cumulatif — enregistre un processus métier à cycle de vie défini",
    "factless": "Table de faits sans fait — enregistre l'occurrence d'événements/la satisfaction de conditions, sans mesure numérique",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Générateur de DDL de modélisation dimensionnelle")
    parser.add_argument("--business-domain", type=str, default="business",
                        help="Nom du domaine métier")
    parser.add_argument("--facts", type=str, required=True,
                        help="Définition des tables de faits, format 'orders:faits de commandes,order_items:détails de commandes'")
    parser.add_argument("--dimensions", type=str, required=True,
                        help="Définition des tables de dimensions, format 'dim_customer:client,dim_product:produit'")
    parser.add_argument("--schema", type=str, default="star",
                        choices=["star", "snowflake", "vault"],
                        help="Paradigme de modélisation")
    parser.add_argument("--scd-type", type=str, default="2",
                        choices=["1", "2", "3", "hybrid"],
                        help="Stratégie de dimension à variation lente")
    parser.add_argument("--platform", type=str, default="bigquery",
                        choices=list(PLATFORM_DIALECTS.keys()),
                        help="Plateforme d'entrepôt de données cible")
    parser.add_argument("--output", type=str, default="ddl/",
                        help="Répertoire de sortie")
    parser.add_argument("--schema-name", type=str, default="dwh",
                        help="Nom du schéma cible")
    parser.add_argument("--format", type=str, default="sql",
                        choices=["sql", "dbt"],
                        help="Format de sortie")
    return parser.parse_args()


def get_type(dialect: dict, typ: str) -> str:
    """Mappe un type générique vers le type spécifique à la plateforme."""
    return dialect.get(typ, typ.upper())


def build_dimension_ddl(
    dim_name: str,
    dim_desc: str,
    dialect: dict,
    scd_type: str,
    platform: str,
    schema_name: str,
    scd_extra_cols: list,
    output_format: str,
) -> str:
    """Génère la DDL d'une table de dimension."""
    table_name = dim_name if dim_name.startswith("dim_") else f"dim_{dim_name}"
    full_name = f"`{schema_name}`.`{table_name}`" if platform in ("bigquery",) else f"{schema_name}.{table_name}"

    cols = []
    # Clé de substitution
    if scd_type in ("2", "hybrid"):
        cols.append(f"    sk_{dim_name.replace('dim_', '')}_id {get_type(dialect, 'pk')} NOT NULL,")
        cols.append(f"    -- Clé de substitution (Surrogate Key)")
    # Clé métier
    cols.append(f"    {dim_name.replace('dim_', '')}_bk {get_type(dialect, 'pk')} NOT NULL,")
    cols.append(f"    -- Clé naturelle métier (Business Key)")
    # Attributs principaux
    cols.append(f"    {dim_name.replace('dim_', '')}_name {get_type(dialect, 'text')},")
    cols.append(f"    {dim_name.replace('dim_', '')}_code {get_type(dialect, 'text')},")
    cols.append(f"    description {get_type(dialect, 'text')},")
    # Colonnes de suivi SCD
    if scd_type in ("2", "hybrid"):
        cols.append(f"    valid_from {get_type(dialect, 'timestamp')} NOT NULL,")
        cols.append(f"    valid_to {get_type(dialect, 'timestamp')} DEFAULT '9999-12-31 23:59:59',")
        cols.append(f"    is_current {get_type(dialect, 'boolean')} DEFAULT TRUE,")
    elif scd_type == "3":
        cols.append(f"    effective_date {get_type(dialect, 'date')},")
    # Colonnes d'audit
    cols.append(f"    created_at {get_type(dialect, 'timestamp')} DEFAULT CURRENT_TIMESTAMP(),")
    cols.append(f"    updated_at {get_type(dialect, 'timestamp')} DEFAULT CURRENT_TIMESTAMP(),")
    cols.append(f"    source_system {get_type(dialect, 'text')}")

    pk_col = f"sk_{dim_name.replace('dim_', '')}_id" if scd_type in ("2", "hybrid") else f"{dim_name.replace('dim_', '')}_bk"
    pk_line = f"    PRIMARY KEY ({pk_col}) NOT ENFORCED" if platform == "bigquery" else f"    PRIMARY KEY ({pk_col})"

    comment = dialect.get("table_comment", "COMMENT '{comment}'")
    if "{comment}" in comment:
        comment_line = comment.format(comment=f"Table de dimension — {dim_desc} | SCD Type {scd_type}")
    else:
        comment_line = comment.format(table=full_name, comment=f"Table de dimension — {dim_desc} | SCD Type {scd_type}")

    ddl = f"""-- ============================================================
-- Table de dimension : {full_name}
-- Description : {dim_desc}
-- Stratégie SCD : {SCD_STRATEGIES[scd_type]['name']}
-- Plateforme : {platform}
-- ============================================================

{dialect['create_syntax']} {full_name} (
{chr(10).join(cols)}
{pk_line}
)
{comment_line};
"""
    return ddl


def build_fact_ddl(
    fact_name: str,
    fact_desc: str,
    dimensions: list,
    dialect: dict,
    platform: str,
    schema_name: str,
    output_format: str,
) -> str:
    """Génère la DDL d'une table de faits."""
    table_name = fact_name if fact_name.startswith("fact_") else f"fact_{fact_name}"
    full_name = f"`{schema_name}`.`{table_name}`" if platform in ("bigquery",) else f"{schema_name}.{table_name}"

    cols = []
    cols.append(f"    -- Clés étrangères de dimension")
    for dim in dimensions:
        dim_clean = dim.replace("dim_", "")
        cols.append(f"    fk_{dim_clean}_sk {get_type(dialect, 'fk')} NOT NULL,")

    cols.append(f"    -- Dimension de date")
    cols.append(f"    fk_date_sk {get_type(dialect, 'fk')} NOT NULL,")

    cols.append(f"    -- Mesures (Measures)")
    cols.append(f"    quantity {get_type(dialect, 'int')} DEFAULT 0,")
    cols.append(f"    unit_price {get_type(dialect, 'decimal')},")
    cols.append(f"    total_amount {get_type(dialect, 'decimal')},")
    cols.append(f"    discount_amount {get_type(dialect, 'decimal')} DEFAULT 0,")
    cols.append(f"    net_amount {get_type(dialect, 'decimal')},")

    cols.append(f"    -- Colonnes d'audit")
    cols.append(f"    created_at {get_type(dialect, 'timestamp')} DEFAULT CURRENT_TIMESTAMP(),")
    cols.append(f"    source_batch_id {get_type(dialect, 'text')},")
    cols.append(f"    etl_job_id {get_type(dialect, 'text')}")

    # Partitionnement et clustering
    partition_clause = ""
    cluster_clause = ""
    if platform == "bigquery":
        partition_clause = f"\nPARTITION BY DATE(fk_date_sk)"
        cluster_clause = f"\nCLUSTER BY fk_{dimensions[0].replace('dim_', '')}_sk" if dimensions else ""
    elif platform == "clickhouse":
        partition_clause = f"\nPARTITION BY toYYYYMM(created_at)"
        cluster_clause = f"\nORDER BY (fk_date_sk)" if dimensions else ""
    elif platform == "starrocks":
        partition_clause = f"\nPARTITION BY RANGE(fk_date_sk)"

    comment = dialect.get("table_comment", "COMMENT '{comment}'")
    if "{comment}" in comment:
        comment_line = comment.format(comment=fact_desc)
    else:
        comment_line = comment.format(table=full_name, comment=fact_desc)

    ddl = f"""-- ============================================================
-- Table de faits : {full_name}
-- Description : {fact_desc}
-- Type : Transaction Fact
-- Granularité : une ligne par transaction
-- Plateforme : {platform}
-- ============================================================

{dialect['create_syntax']} {full_name} (
{chr(10).join(cols)}
)
{partition_clause}{cluster_clause};
{comment_line}
"""
    return ddl


def build_date_dimension_ddl(dialect: dict, platform: str, schema_name: str) -> str:
    """Génère la DDL de la table de dimension de date."""
    full_name = f"`{schema_name}`.`dim_date`" if platform in ("bigquery",) else f"{schema_name}.dim_date"

    comment = dialect.get("table_comment", "COMMENT '{comment}'")
    if "{comment}" in comment:
        comment_line = comment.format(comment="Table de dimension de date — couvre une plage de 10 ans")
    else:
        comment_line = comment.format(table=full_name, comment="Table de dimension de date — couvre une plage de 10 ans")

    ddl = f"""-- ============================================================
-- Table de dimension de date : {full_name}
-- Description : dimension de date standard, couvrant une plage de 10 ans
-- ============================================================

{dialect['create_syntax']} {full_name} (
    date_sk           {get_type(dialect, 'fk')} NOT NULL,      -- Clé de substitution de date (YYYYMMDD)
    full_date         {get_type(dialect, 'date')} NOT NULL,    -- Date complète
    year              {get_type(dialect, 'int')},              -- Année
    quarter           {get_type(dialect, 'int')},              -- Trimestre (1-4)
    quarter_name      {get_type(dialect, 'text')},             -- Q1/Q2/Q3/Q4
    month             {get_type(dialect, 'int')},              -- Mois (1-12)
    month_name        {get_type(dialect, 'text')},             -- Nom du mois
    month_abbr        {get_type(dialect, 'text')},             -- Abréviation du mois
    week_of_year      {get_type(dialect, 'int')},              -- Numéro de semaine ISO
    day_of_week       {get_type(dialect, 'int')},              -- Jour de la semaine (1-7)
    day_name          {get_type(dialect, 'text')},             -- Nom du jour
    day_name_abbr     {get_type(dialect, 'text')},             -- Abréviation du jour
    is_weekend        {get_type(dialect, 'boolean')},          -- Week-end ou non
    is_holiday        {get_type(dialect, 'boolean')},          -- Jour férié ou non
    fiscal_year       {get_type(dialect, 'int')},              -- Exercice fiscal
    fiscal_quarter    {get_type(dialect, 'int')},              -- Trimestre fiscal
    PRIMARY KEY (date_sk) NOT ENFORCED
)
{comment_line};
"""
    return ddl


def build_vault_ddl(
    business_domain: str,
    facts: list,
    dimensions: list,
    dialect: dict,
    platform: str,
    schema_name: str,
) -> str:
    """Génère la DDL du modèle Data Vault 2.0."""
    ddl = f"""-- ============================================================
-- Modèle Data Vault 2.0 : {business_domain}
-- Plateforme : {platform}
-- ============================================================

-- Hubs (entités métier centrales)
"""
    for dim in dimensions:
        dim_clean = dim.replace("dim_", "")
        hub_name = f"hub_{dim_clean}"
        ddl += f"""
CREATE TABLE {schema_name}.{hub_name} (
    {dim_clean}_hash_key {get_type(dialect, 'pk')} NOT NULL,
    {dim_clean}_bk {get_type(dialect, 'text')} NOT NULL,
    load_date {get_type(dialect, 'timestamp')} NOT NULL,
    record_source {get_type(dialect, 'text')} NOT NULL,
    PRIMARY KEY ({dim_clean}_hash_key)
);
"""
    # Links
    ddl += f"""
-- Links (relations)
"""
    for fact in facts:
        fact_clean = fact.replace("fact_", "")
        ddl += f"""
CREATE TABLE {schema_name}.lnk_{fact_clean} (
    {fact_clean}_hash_key {get_type(dialect, 'pk')} NOT NULL,
"""
        for dim in dimensions:
            dim_clean = dim.replace("dim_", "")
            ddl += f"    {dim_clean}_hash_key {get_type(dialect, 'fk')} NOT NULL,\n"
        ddl += f"""    load_date {get_type(dialect, 'timestamp')} NOT NULL,
    record_source {get_type(dialect, 'text')} NOT NULL,
    PRIMARY KEY ({fact_clean}_hash_key)
);
"""
    # Satellites
    ddl += f"""
-- Satellites (attributs descriptifs)
"""
    for dim in dimensions:
        dim_clean = dim.replace("dim_", "")
        ddl += f"""
CREATE TABLE {schema_name}.sat_{dim_clean} (
    {dim_clean}_hash_key {get_type(dialect, 'fk')} NOT NULL,
    load_date {get_type(dialect, 'timestamp')} NOT NULL,
    load_end_date {get_type(dialect, 'timestamp')},
    record_source {get_type(dialect, 'text')} NOT NULL,
    {dim_clean}_name {get_type(dialect, 'text')},
    hash_diff {get_type(dialect, 'text')} NOT NULL,
    PRIMARY KEY ({dim_clean}_hash_key, load_date)
);
"""
    return ddl


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    dialect = PLATFORM_DIALECTS[args.platform]
    scd_type = args.scd_type
    if scd_type.isdigit():
        scd_type = int(scd_type)

    # Analyser les entrées
    facts = []
    for f in args.facts.split(","):
        parts = f.strip().split(":")
        if len(parts) == 2:
            facts.append((parts[0].strip(), parts[1].strip()))
        else:
            facts.append((parts[0].strip(), "Table de faits"))

    dimensions = []
    for d in args.dimensions.split(","):
        parts = d.strip().split(":")
        if len(parts) == 2:
            dimensions.append((parts[0].strip(), parts[1].strip()))
        else:
            dimensions.append((parts[0].strip(), "Table de dimension"))

    dim_names = [d[0] for d in dimensions]
    scd_extra = SCD_STRATEGIES[scd_type].get("extra_cols", [])

    output_file = os.path.join(args.output, f"{args.business_domain}_ddl.sql")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"-- ============================================================\n")
        f.write(f"-- DDL du modèle dimensionnel de l'entrepôt de données\n")
        f.write(f"-- Domaine métier : {args.business_domain}\n")
        f.write(f"-- Paradigme de modélisation : {args.schema.upper()}\n")
        f.write(f"-- Stratégie SCD : {SCD_STRATEGIES[scd_type]['name']}\n")
        f.write(f"-- Plateforme cible : {args.platform}\n")
        f.write(f"-- Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- ============================================================\n\n")

        if args.schema in ("star", "snowflake"):
            # Dimension de date
            f.write(build_date_dimension_ddl(dialect, args.platform, args.schema_name))
            f.write("\n")

            # Tables de dimensions
            for dim_name, dim_desc in dimensions:
                f.write(build_dimension_ddl(
                    dim_name, dim_desc, dialect, scd_type,
                    args.platform, args.schema_name, scd_extra,
                    args.format
                ))
                f.write("\n")

            # Tables de faits
            for fact_name, fact_desc in facts:
                f.write(build_fact_ddl(
                    fact_name, fact_desc, dim_names, dialect,
                    args.platform, args.schema_name, args.format
                ))
                f.write("\n")

        elif args.schema == "vault":
            f.write(build_vault_ddl(
                args.business_domain, facts, dimensions,
                dialect, args.platform, args.schema_name
            ))

    print(f"✅ DDL générée : {output_file}")
    print(f"📋 Contient {len(dimensions)} tables de dimensions, {len(facts)} tables de faits")
    print(f"🏗️  Paradigme de modélisation : {args.schema.upper()}")
    print(f"📅 Stratégie SCD : {SCD_STRATEGIES[scd_type]['name']}")
    print(f"☁️  Plateforme cible : {args.platform}")

    # Générer les métadonnées du modèle
    meta = {
        "business_domain": args.business_domain,
        "schema": args.schema,
        "scd_type": str(scd_type),
        "platform": args.platform,
        "schema_name": args.schema_name,
        "generated_at": datetime.now().isoformat(),
        "tables": {
            "dimensions": [{"name": d[0], "description": d[1]} for d in dimensions],
            "facts": [{"name": f[0], "description": f[1]} for f in facts],
        }
    }
    meta_file = os.path.join(args.output, f"{args.business_domain}_metadata.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    print(f"📄 Métadonnées sauvegardées : {meta_file}")


if __name__ == "__main__":
    main()
