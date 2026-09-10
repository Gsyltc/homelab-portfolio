#!/usr/bin/env python3
"""
Analyseur d'optimisation des coûts — Cost Optimizer
Analyse les journaux de requêtes et les données de facturation, identifie les points chauds de coût,
génère des recommandations d'optimisation et un rapport HTML.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any

# ── Moteur de règles d'optimisation ──────────────────────────────────────────────────

OPTIMIZATION_RULES = [
    {
        "id": "R001",
        "name": "Détection de scan complet de table",
        "description": "La requête n'utilise pas de filtre de partition ni d'index, provoquant un scan complet de la table",
        "detect": lambda q: any(kw in q.get("query_text", "").upper() for kw in ["SELECT *", "SELECT COUNT(*)"])
                            and "WHERE" not in q.get("query_text", "").upper(),
        "severity": "CRITICAL",
        "fix": "Ajouter une condition de filtre de partition (WHERE dt = 'YYYY-MM-DD') ou filtrer via une clé de clustering",
        "savings_estimate": "80-99%",
    },
    {
        "id": "R002",
        "name": "Usage abusif de SELECT *",
        "description": "SELECT * lit toutes les colonnes, augmentant le volume scanné et le coût",
        "detect": lambda q: "SELECT *" in q.get("query_text", "").upper(),
        "severity": "HIGH",
        "fix": "Ne sélectionner que les colonnes nécessaires, réduisant de 50-90% le volume de données transféré",
        "savings_estimate": "50-90%",
    },
    {
        "id": "R003",
        "name": "Détection de requêtes répétées",
        "description": "La même requête est exécutée plusieurs fois ; envisager un cache par vue matérialisée",
        "detect": lambda q, patterns: q.get("query_hash") in patterns.get("repeated", set()),
        "severity": "HIGH",
        "fix": "Créer une vue matérialisée (MATERIALIZED VIEW) ou utiliser le cache d'un outil BI",
        "savings_estimate": "70-95%",
    },
    {
        "id": "R004",
        "name": "Détection de JOIN inefficace",
        "description": "La condition de JOIN manque d'index/clé de clustering, produit cartésien ou JOIN sur un gros volume",
        "detect": lambda q: ("JOIN" in q.get("query_text", "").upper()
                            and "CROSS JOIN" in q.get("query_text", "").upper()),
        "severity": "CRITICAL",
        "fix": "Éviter CROSS JOIN, s'assurer que la condition de JOIN utilise les bonnes clés, envisager une table large pré-jointe",
        "savings_estimate": "90-99%",
    },
    {
        "id": "R005",
        "name": "Sous-requête complexe",
        "description": "Des sous-requêtes imbriquées sur plusieurs niveaux peuvent être optimisées en CTE/WITH",
        "detect": lambda q: q.get("query_text", "").count("(SELECT") >= 3,
        "severity": "MEDIUM",
        "fix": "Réécrire les sous-requêtes complexes avec WITH (CTE) pour améliorer la lisibilité et l'efficacité d'exécution",
        "savings_estimate": "10-50%",
    },
    {
        "id": "R006",
        "name": "Surcharge des petites requêtes",
        "description": "Grand nombre de petites requêtes avec peu de données, part fixe de surcharge élevée",
        "detect": lambda q: q.get("bytes_processed", 0) < 10 * 1024 * 1024,  # < 10 Mo
        "severity": "LOW",
        "fix": "Regrouper les petites requêtes en requêtes par lot, ou ajuster l'unité de facturation minimale",
        "savings_estimate": "20-40%",
    },
    {
        "id": "R007",
        "name": "Détection de déséquilibre des données",
        "description": "La consommation des requêtes d'un utilisateur/d'une équipe dépasse largement la moyenne",
        "severity": "HIGH",
        "fix": "Examiner les requêtes très consommatrices, définir des quotas, optimiser le modèle de données",
        "savings_estimate": "30-70%",
    },
    {
        "id": "R008",
        "name": "Absence de LIMIT",
        "description": "La requête ne précise pas de LIMIT et peut renvoyer un grand volume de données",
        "detect": lambda q: ("SELECT" in q.get("query_text", "").upper()
                            and "LIMIT" not in q.get("query_text", "").upper()
                            and q.get("bytes_processed", 0) > 100 * 1024 * 1024 * 1024),
        "severity": "MEDIUM",
        "fix": "Ajouter une clause LIMIT, ou utiliser un échantillonnage TABLESAMPLE",
        "savings_estimate": "10-30%",
    },
]


def parse_args():
    parser = argparse.ArgumentParser(description="Analyseur d'optimisation des coûts")
    parser.add_argument("--query-log", type=str, required=True,
                        help="Fichier de journal de requêtes (JSON)")
    parser.add_argument("--platform", type=str, default="bigquery",
                        choices=["bigquery", "snowflake", "redshift", "starrocks", "clickhouse", "databricks"])
    parser.add_argument("--billing-data", type=str, default=None,
                        help="Données de facturation (CSV)")
    parser.add_argument("--output", type=str, default="optimization_report/")
    parser.add_argument("--top-n", type=int, default=20,
                        help="Analyser les N requêtes les plus coûteuses")
    return parser.parse_args()


def load_query_log(file_path: str) -> list:
    """Charge le journal de requêtes."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "queries" in data:
        return data["queries"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Format du journal de requêtes incorrect ; attendu : tableau JSON ou objet contenant la clé queries")


def load_billing(file_path: str) -> list | None:
    """Charge les données de facturation."""
    if not file_path or not os.path.exists(file_path):
        return None
    import csv
    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def analyze_queries(queries: list, platform: str, top_n: int) -> dict:
    """Analyse les requêtes et génère des recommandations d'optimisation."""
    # Trier par volume d'octets traités
    sorted_queries = sorted(
        queries,
        key=lambda q: q.get("bytes_processed", 0) or q.get("cost", 0) or 0,
        reverse=True,
    )
    top_queries = sorted_queries[:top_n]

    # Statistiques
    total_bytes = sum(q.get("bytes_processed", 0) or 0 for q in queries)
    total_queries = len(queries)
    avg_bytes = total_bytes / max(total_queries, 1)

    # Détecter les requêtes répétées
    query_hashes = defaultdict(list)
    for q in queries:
        h = hash(q.get("query_text", "")[:200])
        query_hashes[h].append(q)

    repeated = set()
    for h, qs in query_hashes.items():
        if len(qs) > 5:
            repeated.add(h)

    patterns = {"repeated": repeated}

    # Appliquer les règles d'optimisation
    findings = []
    for q in top_queries:
        for rule in OPTIMIZATION_RULES:
            if "detect" not in rule:
                continue
            try:
                if callable(rule["detect"]):
                    # Vérifier la signature
                    import inspect
                    sig = inspect.signature(rule["detect"])
                    if len(sig.parameters) > 1:
                        matched = rule["detect"](q, patterns)
                    else:
                        matched = rule["detect"](q)
                    if matched:
                        findings.append({
                            "query": q.get("query_text", "")[:200],
                            "rule_id": rule["id"],
                            "rule_name": rule["name"],
                            "severity": rule["severity"],
                            "fix": rule["fix"],
                            "savings_estimate": rule.get("savings_estimate", "N/A"),
                            "bytes_processed": q.get("bytes_processed", 0),
                            "duration_sec": q.get("duration", 0),
                        })
            except Exception:
                continue

    # Statistiques par utilisateur/équipe
    user_stats = defaultdict(lambda: {"queries": 0, "total_bytes": 0, "total_cost": 0})
    for q in queries:
        user = q.get("user", q.get("user_email", "unknown"))
        user_stats[user]["queries"] += 1
        user_stats[user]["total_bytes"] += q.get("bytes_processed", 0) or 0
        user_stats[user]["total_cost"] += q.get("cost", 0) or 0

    # Identifier le déséquilibre des données
    skew_findings = []
    avg_per_user = total_bytes / max(len(user_stats), 1)
    for user, stats in user_stats.items():
        if stats["total_bytes"] > avg_per_user * 3:
            skew_findings.append({
                "user": user,
                "total_bytes": stats["total_bytes"],
                "avg_multiple": round(stats["total_bytes"] / max(avg_per_user, 1), 1),
                "queries": stats["queries"],
            })

    # Statistiques par table
    table_stats = defaultdict(lambda: {"bytes": 0, "queries": 0, "avg_bytes": 0})
    for q in queries:
        text = q.get("query_text", "")
        tables = extract_tables(text)
        for t in tables:
            table_stats[t]["bytes"] += q.get("bytes_processed", 0) or 0
            table_stats[t]["queries"] += 1
    for t in table_stats:
        table_stats[t]["avg_bytes"] = table_stats[t]["bytes"] / max(table_stats[t]["queries"], 1)

    top_tables = sorted(table_stats.items(), key=lambda x: x[1]["bytes"], reverse=True)[:10]

    return {
        "summary": {
            "total_queries": total_queries,
            "total_bytes_processed": total_bytes,
            "total_bytes_formatted": format_bytes(total_bytes),
            "avg_bytes_per_query": format_bytes(avg_bytes),
            "platform": platform,
        },
        "top_cost_queries": [
            {
                "query": q.get("query_text", "")[:300],
                "bytes_processed": q.get("bytes_processed", 0),
                "bytes_formatted": format_bytes(q.get("bytes_processed", 0) or 0),
                "duration_sec": q.get("duration", 0),
                "user": q.get("user", q.get("user_email", "unknown")),
            }
            for q in top_queries[:10]
        ],
        "findings": findings[:30],
        "skew_findings": skew_findings,
        "top_tables": [
            {"table": t, "bytes": format_bytes(s["bytes"]), "queries": s["queries"]}
            for t, s in top_tables
        ],
        "cost_breakdown": {
            "critical": len([f for f in findings if f["severity"] == "CRITICAL"]),
            "high": len([f for f in findings if f["severity"] == "HIGH"]),
            "medium": len([f for f in findings if f["severity"] == "MEDIUM"]),
            "low": len([f for f in findings if f["severity"] == "LOW"]),
        },
    }


def extract_tables(query_text: str) -> set:
    """Extrait les noms de tables depuis le SQL."""
    import re
    tables = set()
    # Correspondance des noms de tables après FROM / JOIN
    patterns = [
        r'(?:FROM|JOIN)\s+(?:`?\w+`?\.)?`?(\w+)`?',
        r'(?:FROM|JOIN)\s+`?(\w+\.\w+)`?',
    ]
    for p in patterns:
        for m in re.finditer(p, query_text, re.IGNORECASE):
            tables.add(m.group(1))
    return tables


def format_bytes(b: float) -> str:
    """Formate un nombre d'octets en chaîne lisible."""
    if b is None or b == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while b >= 1024 and i < len(units) - 1:
        b /= 1024
        i += 1
    return f"{b:.2f} {units[i]}"


def generate_html_report(analysis: dict, output_dir: str) -> str:
    """Génère un rapport HTML interactif d'optimisation des coûts."""
    summary = analysis["summary"]
    findings = analysis["findings"]
    cost_bd = analysis["cost_breakdown"]

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'optimisation des coûts de l'entrepôt de données — {summary['platform']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f7fa; color: #1a1a2e; padding: 24px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ font-size: 28px; margin-bottom: 8px; color: #0f0f23; }}
        .subtitle {{ color: #666; margin-bottom: 24px; font-size: 14px; }}
        .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 32px; }}
        .card {{ background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
        .card .label {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }}
        .card .value {{ font-size: 28px; font-weight: 700; color: #0f0f23; }}
        .card .unit {{ font-size: 14px; font-weight: 400; color: #888; }}
        .section {{ background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
        .section h2 {{ font-size: 18px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #e8ecf1; }}
        .finding {{ border-left: 4px solid #ddd; padding: 12px 16px; margin-bottom: 12px; background: #fafbfc; border-radius: 0 8px 8px 0; }}
        .finding.CRITICAL {{ border-color: #e74c3c; background: #fef2f2; }}
        .finding.HIGH {{ border-color: #f39c12; background: #fffbeb; }}
        .finding.MEDIUM {{ border-color: #3498db; background: #eff6ff; }}
        .finding.LOW {{ border-color: #95a5a6; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-right: 8px; }}
        .badge.CRITICAL {{ background: #fef2f2; color: #e74c3c; }}
        .badge.HIGH {{ background: #fffbeb; color: #d97706; }}
        .badge.MEDIUM {{ background: #eff6ff; color: #2563eb; }}
        .badge.LOW {{ background: #f3f4f6; color: #6b7280; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #e8ecf1; font-size: 13px; }}
        th {{ background: #f8fafc; font-weight: 600; color: #475569; }}
        tr:hover td {{ background: #f8fafc; }}
        .chart-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 16px; }}
        @media (max-width: 768px) {{ .chart-row {{ grid-template-columns: 1fr; }} }}
        canvas {{ max-height: 300px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Rapport d'optimisation des coûts de l'entrepôt de données</h1>
        <p class="subtitle">Plateforme cible : {summary['platform']} | Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="cards">
            <div class="card">
                <div class="label">Nombre total de requêtes</div>
                <div class="value">{summary['total_queries']:,}<span class="unit"> fois</span></div>
            </div>
            <div class="card">
                <div class="label">Volume total de données scannées</div>
                <div class="value">{summary['total_bytes_formatted']}</div>
            </div>
            <div class="card">
                <div class="label">Moyenne par requête</div>
                <div class="value">{summary['avg_bytes_per_query']}</div>
            </div>
            <div class="card">
                <div class="label">Recommandations d'optimisation</div>
                <div class="value">{len(findings)}<span class="unit"> éléments</span></div>
            </div>
        </div>

        <div class="section">
            <h2>📈 Répartition par gravité des problèmes</h2>
            <div class="chart-row">
                <div><canvas id="severityChart"></canvas></div>
                <div>
                    <p style="font-size:14px; color:#666; margin-bottom:8px;">Regroupé par gravité :</p>
                    <p>🔴 CRITICAL : <strong>{cost_bd['critical']}</strong> éléments — à traiter immédiatement</p>
                    <p>🟠 HIGH : <strong>{cost_bd['high']}</strong> éléments — à traiter dans la semaine</p>
                    <p>🔵 MEDIUM : <strong>{cost_bd['medium']}</strong> éléments — à optimiser dans le mois</p>
                    <p>⚪ LOW : <strong>{cost_bd['low']}</strong> éléments — peut être différé</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🔍 Liste des recommandations d'optimisation</h2>
            <table>
                <thead>
                    <tr><th>Règle</th><th>Gravité</th><th>Volume de données</th><th>Recommandation de correction</th><th>Économie estimée</th></tr>
                </thead>
                <tbody>
"""
    for f in findings[:20]:
        html += f"""
                    <tr>
                        <td><strong>{f['rule_id']}</strong> {f['rule_name']}</td>
                        <td><span class="badge {f['severity']}">{f['severity']}</span></td>
                        <td>{format_bytes(f.get('bytes_processed', 0))}</td>
                        <td style="font-size:12px;">{f['fix']}</td>
                        <td>{f.get('savings_estimate', 'N/A')}</td>
                    </tr>
"""
    html += """
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>🔥 Top 10 des requêtes les plus coûteuses</h2>
            <table>
                <thead>
                    <tr><th>#</th><th>Requête</th><th>Volume scanné</th><th>Durée</th><th>Utilisateur</th></tr>
                </thead>
                <tbody>
"""
    for i, q in enumerate(analysis["top_cost_queries"], 1):
        text = q["query"][:150].replace("<", "&lt;").replace(">", "&gt;")
        html += f"""
                    <tr>
                        <td>{i}</td>
                        <td style="font-size:12px;max-width:400px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{text}...</td>
                        <td>{q['bytes_formatted']}</td>
                        <td>{q.get('duration_sec', 'N/A')}s</td>
                        <td>{q['user']}</td>
                    </tr>
"""
    html += """
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>🗄️ Top 10 des tables les plus consommatrices</h2>
            <table>
                <thead>
                    <tr><th>Nom de table</th><th>Volume scanné</th><th>Nombre de requêtes</th></tr>
                </thead>
                <tbody>
"""
    for t in analysis["top_tables"]:
        html += f"""
                    <tr><td>{t['table']}</td><td>{t['bytes']}</td><td>{t['queries']}</td></tr>
"""
    html += """
                </tbody>
            </table>
        </div>
    </div>

    <script>
        new Chart(document.getElementById('severityChart'), {
            type: 'doughnut',
            data: {
                labels: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                datasets: [{
                    data: [
"""
    html += f"                        {cost_bd['critical']}, {cost_bd['high']}, {cost_bd['medium']}, {cost_bd['low']}"
    html += """
                    ],
                    backgroundColor: ['#e74c3c', '#f39c12', '#3498db', '#95a5a6'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    </script>
</body>
</html>"""
    return html


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    if not os.path.exists(args.query_log):
        print(f"❌ Le fichier de journal de requêtes n'existe pas : {args.query_log}")
        sys.exit(1)

    print(f"📂 Chargement du journal de requêtes : {args.query_log}")
    queries = load_query_log(args.query_log)
    print(f"   {len(queries)} enregistrements de requêtes")

    print(f"🔍 Analyse en cours...")
    analysis = analyze_queries(queries, args.platform, args.top_n)

    # Sauvegarder le JSON
    json_file = os.path.join(args.output, "cost_analysis.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    # Sauvegarder le HTML
    html_file = os.path.join(args.output, "cost_optimization_report.html")
    html = generate_html_report(analysis, args.output)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    summary = analysis["summary"]
    print(f"\n✅ Rapport généré")
    print(f"📄 JSON : {json_file}")
    print(f"🌐 HTML : {html_file}")
    print(f"\n📊 Résumé :")
    print(f"   Nombre total de requêtes : {summary['total_queries']:,}")
    print(f"   Volume total scanné : {summary['total_bytes_formatted']}")
    print(f"   Recommandations d'optimisation : {len(analysis['findings'])} éléments")
    print(f"   CRITICAL : {analysis['cost_breakdown']['critical']}")
    print(f"   HIGH : {analysis['cost_breakdown']['high']}")
    print(f"   MEDIUM : {analysis['cost_breakdown']['medium']}")


if __name__ == "__main__":
    main()
