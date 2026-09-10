#!/usr/bin/env python3
"""
Conseiller de stratégie de partitionnement — Partition Advisor
Analyse la DDL des tables et les modèles de requêtes pour recommander automatiquement
la stratégie optimale de partitionnement et de clustering.
Prend en charge BigQuery / Snowflake / Redshift / StarRocks / ClickHouse / Databricks.
"""

import argparse
import sys
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple

# ── Matrice des capacités de partitionnement par plateforme ──────────────────────────────────────────────

PLATFORM_CAPABILITIES = {
    "bigquery": {
        "partition_types": ["time_unit", "ingestion_time", "integer_range"],
        "time_granularity": ["HOUR", "DAY", "MONTH", "YEAR"],
        "max_partitions": 4000,
        "supports_clustering": True,
        "max_cluster_cols": 4,
        "clustering_cardinality_advice": "~50k-500k lignes par groupe est optimal",
        "partition_pruning": "Élagage automatique des partitions",
        "cost_model": "Facturation à l'octet scanné ; l'élagage des partitions réduit fortement le coût",
        "partition_syntax": "PARTITION BY {strategy}",
        "cluster_syntax": "CLUSTER BY {cols}",
        "best_practices": [
            "Utiliser comme clé de partition les colonnes fréquemment filtrées par WHERE",
            "Les colonnes à forte cardinalité ne conviennent pas au partitionnement (ex. user_id)",
            "La granularité de partition = DAY est la plus courante",
            "Associer CLUSTER BY pour trier les colonnes à forte cardinalité",
        ],
    },
    "snowflake": {
        "partition_types": ["auto_micro_partition"],
        "time_granularity": ["AUTO"],
        "max_partitions": "Illimité (micro-partitions automatiques)",
        "supports_clustering": True,
        "max_cluster_cols": 4,
        "clustering_cardinality_advice": "Les colonnes à cardinalité moyenne à élevée fonctionnent bien",
        "partition_pruning": "Élagage automatique des micro-partitions",
        "cost_model": "Facturation au crédit ; le clustering réduit le nombre de micro-partitions scannées",
        "partition_syntax": "Gestion automatique, aucun partitionnement explicite requis",
        "cluster_syntax": "CLUSTER BY ({cols})",
        "best_practices": [
            "Snowflake gère automatiquement les micro-partitions, aucun partitionnement manuel requis",
            "Utiliser CLUSTER BY sur les colonnes à forte cardinalité pour accélérer le filtrage et les JOIN",
            "Clusteriser sur les clés de JOIN fréquemment utilisées",
            "Vérifier régulièrement la profondeur de clustering (SYSTEM$CLUSTERING_INFORMATION)",
        ],
    },
    "redshift": {
        "partition_types": ["distribution", "sort"],
        "time_granularity": ["DISTKEY + SORTKEY"],
        "max_partitions": "Illimité",
        "supports_clustering": True,
        "max_cluster_cols": "SORTKEY composite jusqu'à 8 colonnes",
        "clustering_cardinality_advice": "DISTKEY faible cardinalité, SORTKEY filtrage de plage courant",
        "partition_pruning": "Scan de plage via SORTKEY",
        "cost_model": "Facturation à l'heure-nœud",
        "partition_syntax": "DISTKEY({col})",
        "cluster_syntax": "SORTKEY({cols})",
        "best_practices": [
            "Choisir pour DISTKEY les colonnes fréquemment jointes, en évitant le déséquilibre des données",
            "Choisir pour SORTKEY les colonnes de filtrage de plage par WHERE (généralement la colonne de date en premier)",
            "Ordonner un SORTKEY composite selon la fréquence de filtrage",
            "Exécuter régulièrement VACUUM et ANALYZE",
        ],
    },
    "starrocks": {
        "partition_types": ["range", "list"],
        "time_granularity": ["HOUR", "DAY", "MONTH", "YEAR"],
        "max_partitions": 1024,
        "supports_clustering": False,
        "max_cluster_cols": 0,
        "clustering_cardinality_advice": "",
        "partition_pruning": "Élagage des partitions + élagage des buckets",
        "cost_model": "Open source, gratuit",
        "partition_syntax": "PARTITION BY RANGE({col})",
        "cluster_syntax": "DISTRIBUTED BY HASH({cols}) BUCKETS N",
        "best_practices": [
            "Partitionner par plage (RANGE) de date",
            "Choisir pour la clé de bucket une colonne à forte cardinalité et à distribution uniforme",
            "La granularité de partition MONTH est la plus courante",
            "Le partitionnement dynamique gère automatiquement les partitions",
        ],
    },
    "clickhouse": {
        "partition_types": ["range", "list"],
        "time_granularity": ["MONTH", "DAY", "HOUR"],
        "max_partitions": "Recommandé < 1000",
        "supports_clustering": True,
        "max_cluster_cols": "Illimité",
        "clustering_cardinality_advice": "La clé primaire est la clé de tri",
        "partition_pruning": "Élagage des partitions + index de clé primaire",
        "cost_model": "Open source, gratuit",
        "partition_syntax": "PARTITION BY {expr}",
        "cluster_syntax": "ORDER BY ({cols})",
        "best_practices": [
            "La granularité de partition MONTH est la plus courante",
            "Ordonner la clé primaire (ORDER BY) selon la fréquence des requêtes",
            "Éviter un trop grand nombre de partitions (<1000)",
            "Utiliser TTL pour purger automatiquement les anciennes données",
        ],
    },
    "databricks": {
        "partition_types": ["range"],
        "time_granularity": ["YEAR", "MONTH", "DAY"],
        "max_partitions": "Recommandé < 10000",
        "supports_clustering": True,
        "max_cluster_cols": 4,
        "clustering_cardinality_advice": "Éviter trop de colonnes à forte cardinalité",
        "partition_pruning": "Élagage des partitions + Z-Ordering",
        "cost_model": "Facturation au DBU",
        "partition_syntax": "PARTITIONED BY ({col})",
        "cluster_syntax": "CLUSTER BY ({cols})",
        "best_practices": [
            "Cardinalité de partition modérée (100-10000)",
            "Z-Ordering de Delta Lake pour accélérer le filtrage multidimensionnel",
            "La commande OPTIMIZE maintient le clustering",
            "Éviter le problème des petits fichiers",
        ],
    },
}

# ── Analyse des modèles de requêtes ──────────────────────────────────────────────────

QUERY_PATTERNS = {
    "daily_report": {
        "description": "Requête de rapport quotidien : agrégation par jour",
        "filter_columns": ["date", "dt", "created_date"],
        "recommended_partition": "DAY",
        "priority": "HIGH",
    },
    "monthly_trend": {
        "description": "Tendance mensuelle : agrégation par mois",
        "filter_columns": ["month", "year_month"],
        "recommended_partition": "MONTH",
        "priority": "MEDIUM",
    },
    "user_lookup": {
        "description": "Recherche utilisateur : recherche exacte par ID utilisateur",
        "filter_columns": ["user_id", "customer_id"],
        "recommended_partition": "CLUSTER_ONLY",
        "priority": "HIGH",
    },
    "real_time": {
        "description": "Requête temps réel : nécessite les données les plus récentes",
        "filter_columns": ["created_at", "event_time", "ingestion_time"],
        "recommended_partition": "HOUR",
        "priority": "HIGH",
    },
    "range_scan": {
        "description": "Scan de plage : requêtes par lot sur une période",
        "filter_columns": ["created_at", "updated_at"],
        "recommended_partition": "MONTH",
        "priority": "MEDIUM",
    },
    "full_scan": {
        "description": "Scan complet : analyse périodique de toute la table",
        "filter_columns": [],
        "recommended_partition": "MONTH",
        "priority": "LOW",
    },
    "dimensional_join": {
        "description": "JOIN dimensionnel : jointure d'une grande table avec des tables de dimension",
        "filter_columns": ["dim_key", "category_id"],
        "recommended_partition": "CLUSTER_ONLY",
        "priority": "HIGH",
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description="Conseiller de stratégie de partitionnement")
    parser.add_argument("--ddl-file", type=str, required=True,
                        help="Chemin du fichier DDL de la table")
    parser.add_argument("--query-patterns", type=str, required=True,
                        help="Description des modèles de requêtes, séparés par des virgules : daily_report,monthly_trend,user_lookup,...")
    parser.add_argument("--platform", type=str, default="bigquery",
                        choices=list(PLATFORM_CAPABILITIES.keys()))
    parser.add_argument("--data-volume", type=str, default="1TB,100M rows",
                        help="Ordre de grandeur du volume de données : '10TB,500M rows'")
    parser.add_argument("--output", type=str, default="partition_advice/")
    return parser.parse_args()


def parse_ddl(file_path: str) -> dict:
    """Analyse un fichier DDL pour extraire les informations de la table et les colonnes."""
    with open(file_path, "r", encoding="utf-8") as f:
        ddl = f.read()

    table_name = "unknown_table"
    m = re.search(r'TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+\.\w+)`?', ddl, re.IGNORECASE)
    if m:
        table_name = m.group(1)

    # Analyser les noms et types de colonnes
    columns = []
    # Correspondance des définitions de colonnes
    col_pattern = re.findall(r'^\s*(\w+)\s+(\w+(?:\([^)]*\))?)', ddl, re.MULTILINE)
    for col_name, col_type in col_pattern:
        if col_name.upper() not in ("PRIMARY", "PARTITION", "CLUSTER", "DISTKEY", "SORTKEY",
                                      "CREATE", "TABLE", "COMMENT", "OPTIONS", "DISTRIBUTED"):
            columns.append({"name": col_name, "type": col_type.upper()})

    return {"name": table_name, "columns": columns, "ddl": ddl}


def classify_columns(columns: list) -> dict:
    """Classe les colonnes en clés de dimension, mesures, colonnes temporelles, etc."""
    classified = {
        "time_columns": [],
        "key_columns": [],
        "measure_columns": [],
        "text_columns": [],
        "other": [],
    }

    for col in columns:
        name = col["name"].lower()
        typ = col["type"].upper()

        # Colonnes temporelles
        if any(kw in name for kw in ["date", "time", "dt", "created", "updated", "timestamp",
                                       "event_time", "ingestion", "etl"]):
            classified["time_columns"].append(col)
        elif any(kw in typ for kw in ["DATE", "TIME", "TIMESTAMP", "DATETIME"]):
            classified["time_columns"].append(col)
        # Colonnes clés
        elif any(kw in name for kw in ["id", "key", "sk", "bk", "pk", "fk"]):
            classified["key_columns"].append(col)
        # Colonnes de mesure
        elif any(kw in typ for kw in ["INT", "NUMERIC", "DECIMAL", "FLOAT", "DOUBLE", "NUMBER", "BIGINT"]):
            classified["measure_columns"].append(col)
        # Colonnes de texte
        elif any(kw in typ for kw in ["STRING", "VARCHAR", "TEXT", "CHAR"]):
            classified["text_columns"].append(col)
        else:
            classified["other"].append(col)

    return classified


def recommend_strategy(
    classified: dict,
    query_patterns: list,
    platform: str,
    data_volume: str,
) -> dict:
    """Génère une stratégie recommandée de partitionnement et de clustering."""
    caps = PLATFORM_CAPABILITIES[platform]
    patterns = [p.strip() for p in query_patterns if p.strip() in QUERY_PATTERNS]
    pattern_data = [QUERY_PATTERNS[p] for p in patterns]

    # Sélectionner la colonne de partition
    partition_col = None
    partition_granularity = "MONTH"  # Valeur par défaut
    cluster_cols = []

    time_cols = classified["time_columns"]
    key_cols = classified["key_columns"]

    # Logique de recommandation de la colonne de partition
    if time_cols:
        # Privilégier les colonnes de type created_at / event_time
        priority_time = [c for c in time_cols
                         if any(kw in c["name"].lower()
                                for kw in ["created", "event_time", "dt", "date"])]
        partition_col = (priority_time or time_cols)[0]

        # Choisir la granularité selon les modèles de requêtes
        if any(p.get("recommended_partition") == "HOUR" for p in pattern_data):
            partition_granularity = "HOUR"
        elif any(p.get("recommended_partition") == "DAY" for p in pattern_data):
            partition_granularity = "DAY"
        elif any(p.get("recommended_partition") == "MONTH" for p in pattern_data):
            partition_granularity = "MONTH"
    elif platform == "snowflake":
        partition_col = None  # Snowflake gère automatiquement
    elif platform == "redshift":
        # Pour Redshift, DISTKEY choisit la colonne la plus fréquemment jointe
        partition_col = key_cols[0] if key_cols else None

    # Recommandation des colonnes de clustering
    # Les colonnes à forte cardinalité conviennent au clustering
    if key_cols:
        cluster_cols.append(key_cols[0]["name"])
    # Parmi les colonnes de texte, category/type/status, etc. conviennent au clustering
    text_cols = classified["text_columns"]
    for col in text_cols:
        if any(kw in col["name"].lower() for kw in ["category", "type", "status", "region", "country"]):
            cluster_cols.append(col["name"])
            break

    # Clustering piloté par les modèles de requêtes
    for p in pattern_data:
        if p.get("recommended_partition") == "CLUSTER_ONLY":
            for col in p.get("filter_columns", []):
                if col not in cluster_cols:
                    cluster_cols.append(col)

    # Ajustements spécifiques à la plateforme
    max_cluster = caps.get("max_cluster_cols", 4)
    if isinstance(max_cluster, int):
        cluster_cols = cluster_cols[:max_cluster]

    # Générer les recommandations DDL
    ddl_suggestions = _generate_ddl(
        platform, partition_col, partition_granularity, cluster_cols, caps
    )

    # Avertissements de risque
    risks = _identify_risks(classified, partition_col, platform, caps)

    return {
        "platform": platform,
        "table_analysis": {
            "total_columns": sum(len(v) for v in classified.values()),
            "time_columns": [c["name"] for c in time_cols],
            "key_columns": [c["name"] for c in key_cols],
        },
        "query_patterns_considered": patterns,
        "recommendation": {
            "partition_column": partition_col["name"] if partition_col else "N/A (auto-managed)",
            "partition_granularity": partition_granularity,
            "cluster_columns": cluster_cols,
            "ddl_example": ddl_suggestions,
        },
        "cost_impact": _estimate_cost_impact(classified, partition_col, platform),
        "risks": risks,
        "best_practices": caps["best_practices"],
    }


def _generate_ddl(
    platform: str,
    partition_col: dict | None,
    granularity: str,
    cluster_cols: list,
    caps: dict,
) -> str:
    """Génère un exemple de DDL de partitionnement."""
    lines = []

    if platform == "bigquery":
        if partition_col:
            col_name = partition_col["name"]
            if any(kw in partition_col["type"].upper() for kw in ["INT", "NUMERIC", "BIGINT"]):
                lines.append(f"PARTITION BY RANGE_BUCKET({col_name}, GENERATE_ARRAY(0, 1000000, 1000))")
            else:
                lines.append(f"PARTITION BY DATE({col_name})")
        if cluster_cols:
            lines.append(f"CLUSTER BY {', '.join(cluster_cols)}")

    elif platform == "snowflake":
        if cluster_cols:
            lines.append(f"CLUSTER BY ({', '.join(cluster_cols)})")
        lines.insert(0, "-- Snowflake gère automatiquement les micro-partitions ; ci-dessous les recommandations de clustering")

    elif platform == "redshift":
        if partition_col and not cluster_cols:
            lines.append(f"DISTKEY({partition_col['name']})")
        if cluster_cols:
            lines.append(f"COMPOUND SORTKEY({', '.join(cluster_cols)})")

    elif platform == "starrocks":
        if partition_col:
            col_name = partition_col["name"]
            if granularity in ("HOUR", "DAY", "MONTH", "YEAR"):
                lines.append(f"PARTITION BY RANGE({col_name}) (")
                lines.append(f"    PARTITION p_default VALUES LESS THAN MAXVALUE")
                lines.append(f")")
        if cluster_cols:
            lines.append(f"DISTRIBUTED BY HASH({cluster_cols[0]}) BUCKETS 32")

    elif platform == "clickhouse":
        if partition_col:
            col_name = partition_col["name"]
            lines.append(f"PARTITION BY toYYYYMM({col_name})")
        if cluster_cols:
            lines.append(f"ORDER BY ({', '.join(cluster_cols)})")

    elif platform == "databricks":
        if partition_col:
            col_name = partition_col["name"]
            if granularity in ("YEAR", "MONTH", "DAY"):
                fn = {"YEAR": "year", "MONTH": "month", "DAY": "date"}[granularity]
                lines.append(f"PARTITIONED BY ({fn}({col_name}))")
        if cluster_cols:
            lines.append(f"-- Utiliser OPTIMIZE ... ZORDER BY ({', '.join(cluster_cols)})")

    return "\n".join(lines) if lines else "-- La plateforme actuelle ne nécessite pas de déclaration explicite de partitionnement"


def _identify_risks(
    classified: dict,
    partition_col: dict | None,
    platform: str,
    caps: dict,
) -> list:
    """Identifie les risques de la stratégie de partitionnement."""
    risks = []

    # Aucune colonne de partition trouvée
    if not partition_col and platform not in ("snowflake",):
        risks.append({
            "level": "WARNING",
            "message": "Aucune colonne de partition appropriée trouvée ; les performances des requêtes peuvent être affectées",
            "suggestion": "Il est recommandé d'ajouter une colonne de date de type created_at ou dt",
        })

    # Colonne à forte cardinalité utilisée comme partition
    if partition_col and "id" in partition_col["name"].lower() and platform != "snowflake":
        risks.append({
            "level": "CRITICAL",
            "message": f"La colonne clé à forte cardinalité {partition_col['name']} ne devrait pas être utilisée comme clé de partition",
            "suggestion": "Utiliser le clustering (CLUSTER BY) au lieu du partitionnement, ou choisir une colonne de date",
        })

    # Recommandation de clustering pour Snowflake
    if platform == "snowflake" and not caps.get("supports_clustering"):
        risks.append({
            "level": "INFO",
            "message": "Les micro-partitions automatiques de Snowflake sont suffisantes ; le clustering est facultatif",
        })

    return risks


def _estimate_cost_impact(
    classified: dict,
    partition_col: dict | None,
    platform: str,
) -> str:
    """Estime l'impact sur les coûts de la stratégie de partitionnement."""
    if platform == "bigquery":
        return "Réduction estimée de 60-90% du volume d'octets scannés par requête (selon que les modèles de requêtes activent ou non l'élagage des partitions)"
    elif platform == "snowflake":
        return "Gestion automatique des micro-partitions ; le clustering peut réduire de 20-50% le nombre de micro-partitions scannées"
    elif platform == "redshift":
        return "DISTKEY réduit les déplacements de données entre nœuds, SORTKEY accélère les requêtes de plage"
    elif platform in ("starrocks", "clickhouse"):
        return "L'élagage des partitions permet d'ignorer les partitions non pertinentes, réduisant de 70-95% le volume scanné"
    elif platform == "databricks":
        return "Élagage des partitions + Z-Ordering ; réduction possible de 50-80% des scans de fichiers"
    return "L'optimisation des coûts dépend des modèles de requêtes spécifiques"


def generate_report(result: dict, output_dir: str) -> str:
    """Génère un rapport de recommandations de partitionnement au format Markdown."""
    rec = result["recommendation"]
    md = f"""# Rapport de recommandations de stratégie de partitionnement

**Date de génération** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Plateforme cible** : {result['platform']}
**Modèles de requêtes** : {', '.join(result['query_patterns_considered'])}

## Analyse de la table

| Indicateur | Valeur |
|------|-----|
| Nombre total de colonnes | {result['table_analysis']['total_columns']} |
| Colonnes temporelles | {', '.join(result['table_analysis']['time_columns']) or 'aucune'} |
| Colonnes clés | {', '.join(result['table_analysis']['key_columns']) or 'aucune'} |

## Stratégie recommandée

- **Colonne de partition** : `{rec['partition_column']}`
- **Granularité de partition** : `{rec['partition_granularity']}`
- **Colonnes de clustering** : `{', '.join(rec['cluster_columns']) or 'aucune'}`

### Exemple de DDL

```sql
{rec['ddl_example']}
```

## Impact sur les coûts

{result['cost_impact']}

## Avertissements de risque

"""
    for risk in result["risks"]:
        md += f"- **[{risk['level']}]** {risk['message']}\n"
        md += f"  - Suggestion : {risk['suggestion']}\n"

    md += f"""
## Bonnes pratiques ({result['platform']})

"""
    for bp in result["best_practices"]:
        md += f"- {bp}\n"

    md += """
## Actions à suivre

1. Appliquer la stratégie de partitionnement recommandée dans un environnement de test
2. Utiliser EXPLAIN pour vérifier que le plan de requête active l'élagage des partitions
3. Surveiller l'évolution des performances des requêtes
4. Itérer et optimiser la granularité de partition selon les modèles de requêtes réels
"""
    return md


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    if not os.path.exists(args.ddl_file):
        print(f"❌ Le fichier DDL n'existe pas : {args.ddl_file}")
        sys.exit(1)

    table_info = parse_ddl(args.ddl_file)
    classified = classify_columns(table_info["columns"])
    query_patterns = [p.strip() for p in args.query_patterns.split(",")]

    result = recommend_strategy(classified, query_patterns, args.platform, args.data_volume)

    # Sauvegarder le JSON
    table_safe = table_info["name"].replace(".", "_").replace("`", "")
    json_file = os.path.join(args.output, f"{table_safe}_partition_advice.json")
    result["table_name"] = table_info["name"]
    result["generated_at"] = datetime.now().isoformat()
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Sauvegarder le rapport Markdown
    md_file = os.path.join(args.output, f"{table_safe}_partition_advice.md")
    report = generate_report(result, args.output)
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Recommandations de partitionnement générées")
    print(f"📄 JSON : {json_file}")
    print(f"📝 Rapport : {md_file}")
    print(f"")
    print(f"📊 Stratégie recommandée :")
    rec = result["recommendation"]
    print(f"   Colonne de partition : {rec['partition_column']}")
    print(f"   Granularité de partition : {rec['partition_granularity']}")
    print(f"   Colonnes de clustering : {', '.join(rec['cluster_columns']) or 'aucune'}")
    print(f"   Impact sur les coûts : {result['cost_impact']}")


if __name__ == "__main__":
    main()
