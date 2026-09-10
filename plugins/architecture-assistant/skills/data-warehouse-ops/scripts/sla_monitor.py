#!/usr/bin/env python3
"""
Générateur de tableau de bord de surveillance SLA — SLA Monitor
Génère un tableau de bord de surveillance HTML interactif à partir de l'historique
d'exécution des pipelines et de la configuration des SLA.
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def parse_args():
    parser = argparse.ArgumentParser(description="Générateur de tableau de bord de surveillance SLA")
    parser.add_argument("--config", type=str, default=None,
                        help="Fichier de configuration des SLA (YAML)")
    parser.add_argument("--pipeline-runs", type=str, required=True,
                        help="Données d'historique d'exécution des pipelines (CSV)")
    parser.add_argument("--output", type=str, default="sla_dashboard/",
                        help="Répertoire de sortie")
    parser.add_argument("--days", type=int, default=30,
                        help="Plage de données à analyser (jours)")
    return parser.parse_args()


DEFAULT_SLA_CONFIG = {
    "sla_tiers": {
        "tier_1_critical": {
            "name": "Tier 1 — Pipelines critiques",
            "freshness_hours": 4,
            "uptime_pct": 99.9,
            "max_failure_rate_pct": 1.0,
            "notification_channels": ["pagerduty", "slack"],
            "description": "Pipelines impactant directement les indicateurs métier clés",
        },
        "tier_2_important": {
            "name": "Tier 2 — Pipelines importants",
            "freshness_hours": 8,
            "uptime_pct": 99.5,
            "max_failure_rate_pct": 3.0,
            "notification_channels": ["slack", "email"],
            "description": "Pipelines impactant les rapports et analyses internes",
        },
        "tier_3_normal": {
            "name": "Tier 3 — Pipelines courants",
            "freshness_hours": 24,
            "uptime_pct": 99.0,
            "max_failure_rate_pct": 5.0,
            "notification_channels": ["email"],
            "description": "Pipelines de données non critiques",
        },
    },
    "alert_rules": {
        "freshness_violation": "La fraîcheur des données dépasse le seuil SLA",
        "failure_rate_spike": "Le taux d'échec augmente de > 200% par rapport à la moyenne des 7 jours précédents",
        "volume_anomaly": "La variation du volume de données dépasse 50%",
        "consecutive_failures": "Plus de 3 échecs consécutifs",
    },
}


def load_config(file_path: str | None) -> dict:
    """Charge la configuration des SLA."""
    if file_path and os.path.exists(file_path):
        if not HAS_YAML:
            print("⚠️  PyYAML n'est pas installé, utilisation de la configuration par défaut")
            return DEFAULT_SLA_CONFIG
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or DEFAULT_SLA_CONFIG
    return DEFAULT_SLA_CONFIG


def load_pipeline_runs(file_path: str) -> list:
    """Charge l'historique d'exécution des pipelines."""
    runs = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            runs.append(row)
    return runs


def analyze_pipeline_runs(runs: list, config: dict, days: int) -> dict:
    """Analyse les données d'exécution des pipelines."""
    now = datetime.now()
    cutoff = now - timedelta(days=days)

    # Regrouper par pipeline
    pipeline_stats = defaultdict(lambda: {
        "runs": [],
        "total": 0,
        "success": 0,
        "failed": 0,
        "running": 0,
        "durations": [],
        "latest_run": None,
        "daily_runs": defaultdict(int),
    })

    for run in runs:
        pipeline = run.get("pipeline_name", run.get("dag_id", "unknown"))
        status = run.get("status", run.get("state", "unknown")).lower()
        start_time_str = run.get("start_time", run.get("execution_date", ""))
        duration_str = run.get("duration_sec", run.get("duration", 0))

        try:
            duration = float(duration_str)
        except (ValueError, TypeError):
            duration = 0

        stats = pipeline_stats[pipeline]
        stats["total"] += 1

        if status in ("success", "succeeded", "completed"):
            stats["success"] += 1
            stats["durations"].append(duration)
        elif status in ("failed", "error", "failure"):
            stats["failed"] += 1
        elif status in ("running", "queued"):
            stats["running"] += 1

        # Analyser la date/heure
        try:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
                try:
                    start_dt = datetime.strptime(start_time_str[:19], fmt)
                    break
                except ValueError:
                    continue
            else:
                start_dt = None
        except Exception:
            start_dt = None

        if start_dt and start_dt >= cutoff:
            stats["daily_runs"][start_dt.strftime("%Y-%m-%d")] += 1
            if stats["latest_run"] is None or start_dt > stats["latest_run"]:
                stats["latest_run"] = start_dt

    # Calculer les indicateurs SLA par pipeline
    sla_results = {}
    for pipeline, stats in pipeline_stats.items():
        if stats["total"] == 0:
            continue

        success_rate = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0
        failure_rate = (stats["failed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        avg_duration = sum(stats["durations"]) / len(stats["durations"]) if stats["durations"] else 0

        # Déterminer quel niveau de SLA est satisfait
        sla_level = "tier_3_normal"
        tiers = config.get("sla_tiers", DEFAULT_SLA_CONFIG["sla_tiers"])
        if success_rate >= tiers.get("tier_1_critical", {}).get("uptime_pct", 99.9):
            sla_level = "tier_1_critical"
        elif success_rate >= tiers.get("tier_2_important", {}).get("uptime_pct", 99.5):
            sla_level = "tier_2_important"

        # Détecter les anomalies
        alerts = detect_anomalies(pipeline, stats, config, days)

        sla_results[pipeline] = {
            "total_runs": stats["total"],
            "success": stats["success"],
            "failed": stats["failed"],
            "success_rate": round(success_rate, 2),
            "failure_rate": round(failure_rate, 2),
            "avg_duration_sec": round(avg_duration, 1),
            "latest_run": stats["latest_run"].isoformat() if stats["latest_run"] else None,
            "sla_level": sla_level,
            "sla_status": "COMPLIANT" if success_rate >= tiers.get(sla_level, {}).get("uptime_pct", 99) else "VIOLATED",
            "alerts": alerts,
        }

    # Statistiques globales
    global_stats = {
        "total_pipelines": len(sla_results),
        "compiant_pipelines": sum(1 for p in sla_results.values() if p["sla_status"] == "COMPLIANT"),
        "violated_pipelines": sum(1 for p in sla_results.values() if p["sla_status"] == "VIOLATED"),
        "total_runs": sum(p["total_runs"] for p in sla_results.values()),
        "total_failures": sum(p["failed"] for p in sla_results.values()),
        "overall_success_rate": round(
            sum(p["success"] for p in sla_results.values()) /
            max(sum(p["total_runs"] for p in sla_results.values()), 1) * 100, 2
        ),
        "total_alerts": sum(len(p["alerts"]) for p in sla_results.values()),
    }

    return {
        "global": global_stats,
        "pipelines": sla_results,
        "config": config,
        "analysis_period_days": days,
        "generated_at": datetime.now().isoformat(),
    }


def detect_anomalies(pipeline: str, stats: dict, config: dict, days: int) -> list:
    """Détecte les anomalies."""
    alerts = []

    tiers = config.get("sla_tiers", DEFAULT_SLA_CONFIG["sla_tiers"])
    tier = tiers.get("tier_2_important", {})

    # Taux d'échec trop élevé
    failure_rate = (stats["failed"] / stats["total"] * 100) if stats["total"] > 0 else 0
    if failure_rate > tier.get("max_failure_rate_pct", 3.0):
        alerts.append({
            "type": "high_failure_rate",
            "severity": "CRITICAL" if failure_rate > 10 else "HIGH",
            "message": f"Le taux d'échec {failure_rate:.1f}% dépasse le seuil {tier.get('max_failure_rate_pct', 3.0)}%",
            "metric": f"{failure_rate:.1f}%",
            "threshold": f"{tier.get('max_failure_rate_pct', 3.0)}%",
        })

    # Fraîcheur des données
    if stats["latest_run"]:
        hours_since = (datetime.now() - stats["latest_run"]).total_seconds() / 3600
        freshness_threshold = tier.get("freshness_hours", 8)
        if hours_since > freshness_threshold:
            alerts.append({
                "type": "freshness_violation",
                "severity": "HIGH" if hours_since > freshness_threshold * 2 else "MEDIUM",
                "message": f"La dernière exécution réussie remonte à {hours_since:.1f} heures, dépassant le SLA {freshness_threshold}h",
                "metric": f"{hours_since:.1f}h",
                "threshold": f"{freshness_threshold}h",
            })

    # Durée moyenne anormale
    if stats["durations"] and len(stats["durations"]) > 5:
        avg = sum(stats["durations"]) / len(stats["durations"])
        recent_avg = sum(stats["durations"][-5:]) / min(len(stats["durations"]), 5)
        if avg > 0 and recent_avg > avg * 2:
            alerts.append({
                "type": "duration_spike",
                "severity": "MEDIUM",
                "message": f"La durée d'exécution récente {recent_avg:.0f}s dépasse largement la moyenne {avg:.0f}s",
                "metric": f"{recent_avg:.0f}s",
                "threshold": f"{avg:.0f}s (avg)",
            })

    return alerts


def generate_html_dashboard(analysis: dict) -> str:
    """Génère un tableau de bord de surveillance SLA HTML interactif."""
    g = analysis["global"]
    pipelines = analysis["pipelines"]

    # Données des pipelines au format JSON
    pipe_names = list(pipelines.keys())
    pipe_json = json.dumps([
        {
            "name": name,
            "success_rate": p["success_rate"],
            "failure_rate": p["failure_rate"],
            "total_runs": p["total_runs"],
            "sla_level": p["sla_level"],
            "sla_status": p["sla_status"],
            "alerts": len(p["alerts"]),
        }
        for name, p in pipelines.items()
    ], ensure_ascii=False)

    # Classer par tier
    tier_counts = defaultdict(int)
    for p in pipelines.values():
        tier_counts[p["sla_level"]] += 1

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tableau de bord de surveillance SLA</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f5; padding: 24px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ font-size: 28px; color: #0f0f23; margin-bottom: 4px; }}
        .subtitle {{ color: #666; font-size: 13px; margin-bottom: 24px; }}
        .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 24px; }}
        .card {{ background: #fff; border-radius: 10px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
        .card .lbl {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.05em; }}
        .card .val {{ font-size: 26px; font-weight: 700; }}
        .card.green .val {{ color: #059669; }}
        .card.red .val {{ color: #dc2626; }}
        .card.amber .val {{ color: #d97706; }}
        .section {{ background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
        .section h2 {{ font-size: 18px; margin-bottom: 16px; border-bottom: 2px solid #e8ecf1; padding-bottom: 8px; }}
        .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
        @media (max-width: 768px) {{ .charts {{ grid-template-columns: 1fr; }} }}
        canvas {{ max-height: 300px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th, td {{ padding: 10px 12px; border-bottom: 1px solid #e8ecf1; text-align: left; }}
        th {{ background: #f8fafc; font-weight: 600; color: #475569; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
        .badge.pass {{ background: #ecfdf5; color: #059669; }}
        .badge.fail {{ background: #fef2f2; color: #dc2626; }}
        .badge.t1 {{ background: #ede9fe; color: #7c3aed; }}
        .badge.t2 {{ background: #dbeafe; color: #2563eb; }}
        .badge.t3 {{ background: #f3f4f6; color: #6b7280; }}
        tr:hover td {{ background: #f8fafc; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📡 Tableau de bord de surveillance SLA des pipelines de données</h1>
        <p class="subtitle">Période d'analyse : {analysis['analysis_period_days']} derniers jours | Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="cards">
            <div class="card green">
                <div class="lbl">Nombre total de pipelines</div>
                <div class="val">{g['total_pipelines']}<span style="font-size:14px;font-weight:400;color:#666;"> </span></div>
            </div>
            <div class="card green">
                <div class="lbl">Taux de réussite global</div>
                <div class="val">{g['overall_success_rate']}<span style="font-size:14px;font-weight:400;color:#666;">%</span></div>
            </div>
            <div class="card green">
                <div class="lbl">Conformité SLA</div>
                <div class="val">{g['compiant_pipelines']}<span style="font-size:14px;font-weight:400;color:#666;"> / {g['total_pipelines']}</span></div>
            </div>
            <div class="card {'red' if g['violated_pipelines'] > 0 else 'green'}">
                <div class="lbl">Violations de SLA</div>
                <div class="val">{g['violated_pipelines']}<span style="font-size:14px;font-weight:400;color:#666;"> </span></div>
            </div>
            <div class="card {'amber' if g['total_alerts'] > 0 else 'green'}">
                <div class="lbl">Alertes actives</div>
                <div class="val">{g['total_alerts']}<span style="font-size:14px;font-weight:400;color:#666;"> </span></div>
            </div>
            <div class="card">
                <div class="lbl">Nombre total d'exécutions</div>
                <div class="val">{g['total_runs']:,}</div>
            </div>
        </div>

        <div class="section">
            <h2>📊 Répartition des taux de réussite des pipelines</h2>
            <div class="charts">
                <div><canvas id="successChart"></canvas></div>
                <div><canvas id="tierChart"></canvas></div>
            </div>
        </div>

        <div class="section">
            <h2>📋 Détail SLA des pipelines</h2>
            <table id="pipelineTable">
                <thead>
                    <tr>
                        <th>Nom du pipeline</th>
                        <th>Niveau SLA</th>
                        <th>Taux de réussite</th>
                        <th>Taux d'échec</th>
                        <th>Total exécutions</th>
                        <th>Statut SLA</th>
                        <th>Alertes</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

    <script>
        const pipes = {pipe_json};

        // Remplir le tableau
        const tb = document.querySelector('#pipelineTable tbody');
        pipes.forEach(p => {{
            const statusClass = p.sla_status === 'COMPLIANT' ? 'pass' : 'fail';
            const tierClass = p.sla_level === 'tier_1_critical' ? 't1' : p.sla_level === 'tier_2_important' ? 't2' : 't3';
            const tierLabel = p.sla_level === 'tier_1_critical' ? 'T1 Critique' : p.sla_level === 'tier_2_important' ? 'T2 Important' : 'T3 Courant';
            const alertCell = p.alerts > 0 ? `<span style="color:#dc2626;font-weight:600;">${{p.alerts}}</span>` : '0';
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${{p.name}}</strong></td>
                <td><span class="badge ${{tierClass}}">${{tierLabel}}</span></td>
                <td>${{p.success_rate}}%</td>
                <td style="color:${{p.failure_rate > 5 ? '#dc2626' : '#666'}}">${{p.failure_rate}}%</td>
                <td>${{p.total_runs}}</td>
                <td><span class="badge ${{statusClass}}">${{p.sla_status === 'COMPLIANT' ? '✅ COMPLIANT' : '❌ VIOLATED'}}</span></td>
                <td>${{alertCell}}</td>
            `;
            tb.appendChild(tr);
        }});

        // Graphique des taux de réussite
        new Chart(document.getElementById('successChart'), {{
            type: 'bar',
            data: {{
                labels: pipes.map(p => p.name),
                datasets: [{{
                    label: 'Taux de réussite (%)',
                    data: pipes.map(p => p.success_rate),
                    backgroundColor: pipes.map(p => p.success_rate >= 99 ? '#059669' : p.success_rate >= 95 ? '#d97706' : '#dc2626'),
                    borderRadius: 4,
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{ y: {{ min: 80, max: 100 }} }},
                plugins: {{ legend: {{ display: false }} }}
            }}
        }});

        // Répartition par tier
        const tierCounts = {{
            tier_1_critical: {tier_counts.get('tier_1_critical', 0)},
            tier_2_important: {tier_counts.get('tier_2_important', 0)},
            tier_3_normal: {tier_counts.get('tier_3_normal', 0)},
        }};
        new Chart(document.getElementById('tierChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['T1 Critique', 'T2 Important', 'T3 Courant'],
                datasets: [{{
                    data: [tierCounts.tier_1_critical, tierCounts.tier_2_important, tierCounts.tier_3_normal],
                    backgroundColor: ['#7c3aed', '#2563eb', '#6b7280'],
                    borderWidth: 0,
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ position: 'bottom' }} }}
            }}
        }});
    </script>
</body>
</html>"""
    return html


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    if not os.path.exists(args.pipeline_runs):
        print(f"❌ Les données d'exécution des pipelines n'existent pas : {args.pipeline_runs}")
        sys.exit(1)

    config = load_config(args.config)
    runs = load_pipeline_runs(args.pipeline_runs)

    print(f"📂 Chargement de {len(runs)} enregistrements d'exécution de pipelines")
    print(f"📅 Plage d'analyse : {args.days} derniers jours")

    analysis = analyze_pipeline_runs(runs, config, args.days)

    # Sauvegarder le JSON
    json_file = os.path.join(args.output, "sla_analysis.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    # Sauvegarder le tableau de bord HTML
    html_file = os.path.join(args.output, "sla_dashboard.html")
    html = generate_html_dashboard(analysis)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    g = analysis["global"]
    print(f"\n✅ Tableau de bord de surveillance SLA généré")
    print(f"📄 JSON : {json_file}")
    print(f"🌐 HTML : {html_file}")
    print(f"\n📊 Résumé :")
    print(f"   Nombre total de pipelines : {g['total_pipelines']}")
    print(f"   Taux de réussite global : {g['overall_success_rate']}%")
    print(f"   Conformité SLA : {g['compiant_pipelines']}/{g['total_pipelines']}")
    print(f"   Violations de SLA : {g['violated_pipelines']}")
    print(f"   Alertes actives : {g['total_alerts']}")


if __name__ == "__main__":
    main()
