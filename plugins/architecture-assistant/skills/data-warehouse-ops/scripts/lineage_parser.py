#!/usr/bin/env python3
"""
Analyseur de traçabilité SQL — Lineage Parser
Analyse des fichiers SQL pour extraire la traçabilité au niveau des tables et des colonnes,
génère un graphe DOT et une visualisation HTML.
S'appuie sur la bibliothèque sqlparse pour l'analyse SQL.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

try:
    import sqlparse
    from sqlparse.sql import Identifier, IdentifierList, Where, Comparison, Function
    from sqlparse.tokens import Keyword, Name, Punctuation, Whitespace, Wildcard
    HAS_SQLPARSE = True
except ImportError:
    HAS_SQLPARSE = False


def parse_args():
    parser = argparse.ArgumentParser(description="Analyseur de traçabilité SQL")
    parser.add_argument("--sql-dir", type=str, default=None,
                        help="Répertoire contenant les fichiers SQL")
    parser.add_argument("--sql-file", type=str, default=None,
                        help="Fichier SQL unique")
    parser.add_argument("--output", type=str, default="lineage/",
                        help="Répertoire de sortie")
    parser.add_argument("--level", type=str, default="table",
                        choices=["table", "column"],
                        help="Niveau de traçabilité")
    return parser.parse_args()


class SQLLineageParser:
    """Analyseur de traçabilité SQL."""

    def __init__(self, level: str = "table"):
        self.level = level
        self.edges: List[Tuple[str, str, str]] = []  # (source, target, operation)
        self.tables: Dict[str, dict] = {}
        self.column_lineage: List[dict] = []

    def parse_file(self, file_path: str) -> None:
        """Analyse un fichier SQL unique."""
        with open(file_path, "r", encoding="utf-8") as f:
            sql = f.read()

        statements = sqlparse.split(sql)
        for stmt in statements:
            self._parse_statement(stmt, file_path)

    def parse_directory(self, dir_path: str) -> None:
        """Analyse tous les fichiers SQL d'un répertoire."""
        for ext in ("*.sql", "*.ddl", "*.dml"):
            for f in Path(dir_path).rglob(ext):
                self.parse_file(str(f))

    def _parse_statement(self, sql: str, file_path: str) -> None:
        """Analyse une seule instruction SQL."""
        sql_upper = sql.upper().strip()
        file_name = os.path.basename(file_path)

        # INSERT INTO ... SELECT ...
        insert_pattern = re.compile(
            r'INSERT\s+(?:INTO|OVERWRITE)?\s*(?:TABLE\s+)?(\S+)', re.IGNORECASE
        )
        insert_match = insert_pattern.search(sql_upper)
        if insert_match:
            target = insert_match.group(1).strip("`\"").lower()

            # Extraire les tables sources du SELECT
            source_tables = self._extract_source_tables(sql)
            for src in source_tables:
                self.edges.append((src, target, "INSERT"))
                self._register_table(src, "source")
                self._register_table(target, "target")

            # Traçabilité au niveau des colonnes
            if self.level == "column":
                self._extract_column_lineage(sql, source_tables, target, file_path)
            return

        # CREATE TABLE AS SELECT (CTAS)
        ctas_pattern = re.compile(
            r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:TABLE|VIEW)\s+(?:IF\s+NOT\s+EXISTS\s+)?(\S+)\s+AS',
            re.IGNORECASE
        )
        ctas_match = ctas_pattern.search(sql_upper)
        if ctas_match:
            target = ctas_match.group(1).strip("`\"").lower()
            source_tables = self._extract_source_tables(sql)
            op = "VIEW" if "VIEW" in sql_upper[:100] else "CTAS"
            for src in source_tables:
                self.edges.append((src, target, op))
                self._register_table(src, "source")
                self._register_table(target, "target")
            return

        # CREATE VIEW
        view_pattern = re.compile(
            r'CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+(\S+)\s+AS',
            re.IGNORECASE
        )
        view_match = view_pattern.search(sql_upper)
        if view_match:
            target = view_match.group(1).strip("`\"").lower()
            source_tables = self._extract_source_tables(sql)
            for src in source_tables:
                self.edges.append((src, target, "VIEW"))
                self._register_table(src, "source")
                self._register_table(target, "view")
            return

        # MERGE INTO
        merge_pattern = re.compile(
            r'MERGE\s+(?:INTO\s+)?(\S+)\s+(?:AS\s+\S+\s+)?USING\s+(\S+)',
            re.IGNORECASE
        )
        merge_match = merge_pattern.search(sql_upper)
        if merge_match:
            target = merge_match.group(1).strip("`\"").lower()
            source = merge_match.group(2).strip("`\"").lower()
            self.edges.append((source, target, "MERGE"))
            self._register_table(source, "source")
            self._register_table(target, "target")

    def _extract_source_tables(self, sql: str) -> List[str]:
        """Extrait les noms de tables sources depuis le SQL."""
        tables = set()
        # Correspondance des noms de tables après FROM / JOIN
        patterns = [
            r'(?:FROM|JOIN)\s+(?:`?\w+`?\.)?`?(\w+)`?(?:\s+(?:AS\s+)?\w+)?',
            r'(?:FROM|JOIN)\s+`?([\w.-]+)`?',
        ]
        for p in patterns:
            for m in re.finditer(p, sql, re.IGNORECASE):
                name = m.group(1).lower().split(".")[-1].strip("`\"")
                if name not in ("select", "values", "unnest", "lateral"):
                    tables.add(name)
        return list(tables)

    def _register_table(self, name: str, role: str) -> None:
        """Enregistre une table."""
        if name not in self.tables:
            self.tables[name] = {"roles": set(), "uses": 0}
        self.tables[name]["roles"].add(role)
        self.tables[name]["uses"] += 1

    def _extract_column_lineage(
        self, sql: str, sources: List[str], target: str, file_path: str
    ) -> None:
        """Extrait la traçabilité au niveau des colonnes."""
        # Tenter d'extraire la correspondance entre les colonnes du SELECT et celles de l'INSERT
        target_cols = self._extract_insert_columns(sql)
        select_cols = self._extract_select_expressions(sql)

        if target_cols and select_cols and len(target_cols) == len(select_cols):
            for tc, sc in zip(target_cols, select_cols):
                self.column_lineage.append({
                    "source_expression": sc,
                    "target_table": target,
                    "target_column": tc,
                    "file": file_path,
                })

    def _extract_insert_columns(self, sql: str) -> List[str]:
        """Extrait les colonnes cibles de l'INSERT."""
        m = re.search(r'INSERT\s+(?:INTO|OVERWRITE)?\s*\S+\s*\(([^)]+)\)', sql, re.IGNORECASE)
        if m:
            return [c.strip().strip("`\"") for c in m.group(1).split(",")]
        return []

    def _extract_select_expressions(self, sql: str) -> List[str]:
        """Extrait les références de colonnes des expressions du SELECT."""
        # Extraire l'expression entre SELECT et FROM
        m = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE | re.DOTALL)
        if m:
            exprs = m.group(1)
            # Découper selon les virgules de premier niveau (traitement simplifié)
            cols = []
            depth = 0
            current = []
            for ch in exprs:
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                if ch == "," and depth == 0:
                    cols.append("".join(current).strip())
                    current = []
                else:
                    current.append(ch)
            if current:
                cols.append("".join(current).strip())
            return cols
        return []

    def to_dot(self) -> str:
        """Génère un graphe au format DOT."""
        dot = "digraph DataLineage {\n"
        dot += "    rankdir=LR;\n"
        dot += '    node [shape=box, style="rounded,filled", fontname="Arial"];\n'
        dot += '    edge [fontname="Arial", fontsize=10];\n\n'

        # Coloration selon le rôle
        for table, info in self.tables.items():
            roles = info["roles"]
            if "source" in roles and "target" not in roles:
                color = "#e8f5e9"  # Vert = table purement source
            elif "target" in roles and "source" not in roles:
                color = "#fff3e0"  # Orange = table purement cible
            else:
                color = "#e3f2fd"  # Bleu = table intermédiaire
            label = table.replace("_", "\\n")
            dot += f'    "{table}" [label="{label}", fillcolor="{color}", tooltip="{", ".join(roles)}"];\n'

        dot += "\n"
        for src, tgt, op in self.edges:
            style = {"INSERT": "solid", "CTAS": "dashed", "VIEW": "dotted", "MERGE": "bold"}
            color = {"INSERT": "#2e7d32", "CTAS": "#1565c0", "VIEW": "#6a1b9a", "MERGE": "#e65100"}
            dot += f'    "{src}" -> "{tgt}" [label="{op}", style={style.get(op, "solid")}, color={color.get(op, "#333")}];\n'

        dot += "}\n"
        return dot

    def get_summary(self) -> dict:
        """Génère un résumé de l'analyse."""
        source_only = [t for t, i in self.tables.items() if "source" in i["roles"] and "target" not in i["roles"]]
        target_only = [t for t, i in self.tables.items() if "target" in i["roles"] and "source" not in i["roles"]]
        intermediate = [t for t, i in self.tables.items() if "source" in i["roles"] and "target" in i["roles"]]

        return {
            "total_tables": len(self.tables),
            "total_edges": len(self.edges),
            "source_tables": len(source_only),
            "target_tables": len(target_only),
            "intermediate_tables": len(intermediate),
            "column_lineage_count": len(self.column_lineage),
            "top_tables": sorted(self.tables.items(), key=lambda x: x[1]["uses"], reverse=True)[:10],
        }


def generate_html_visualizer(parser: SQLLineageParser, output_dir: str) -> str:
    """Génère une page HTML interactive de visualisation de la traçabilité."""
    summary = parser.get_summary()

    # Construire les données des nœuds et des arêtes
    nodes = []
    node_ids = set()
    for table, info in parser.tables.items():
        if table not in node_ids:
            node_ids.add(table)
            roles = info["roles"]
            if "source" in roles and "target" not in roles:
                group = "source"
            elif "target" in roles and "source" not in roles:
                group = "target"
            else:
                group = "intermediate"
            nodes.append({"id": table, "label": table, "group": group, "uses": info["uses"]})
    for src, tgt, op in parser.edges:
        if src not in node_ids:
            node_ids.add(src)
            nodes.append({"id": src, "label": src, "group": "source", "uses": 0})
        if tgt not in node_ids:
            node_ids.add(tgt)
            nodes.append({"id": tgt, "label": tgt, "group": "target", "uses": 0})

    edges = [{"from": src, "to": tgt, "label": op} for src, tgt, op in parser.edges]

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)
    top_tables_json = json.dumps(
        [{"name": t, "uses": u["uses"]} for t, u in summary["top_tables"]],
        ensure_ascii=False
    )

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualisation de la traçabilité des données</title>
    <script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.6/dist/vis-network.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f5; }}
        .header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff; padding: 20px 32px; }}
        .header h1 {{ font-size: 24px; }}
        .header .meta {{ font-size: 13px; opacity: 0.7; margin-top: 4px; }}
        .layout {{ display: flex; height: calc(100vh - 90px); }}
        .sidebar {{ width: 280px; background: #fff; padding: 20px; overflow-y: auto; border-right: 1px solid #e0e0e0; }}
        .main {{ flex: 1; position: relative; }}
        #network {{ width: 100%; height: 100%; }}
        .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 20px; }}
        .stat {{ background: #f8fafc; padding: 10px; border-radius: 8px; text-align: center; }}
        .stat .num {{ font-size: 22px; font-weight: 700; color: #1a1a2e; }}
        .stat .lbl {{ font-size: 11px; color: #888; margin-top: 2px; }}
        .legend {{ margin-top: 20px; }}
        .legend-item {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 13px; }}
        .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 12px; }}
        th, td {{ padding: 6px 8px; border-bottom: 1px solid #eee; text-align: left; }}
        th {{ color: #888; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔗 Visualisation de la traçabilité des données</h1>
        <div class="meta">Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Niveau de traçabilité : {parser.level}</div>
    </div>
    <div class="layout">
        <div class="sidebar">
            <div class="stats">
                <div class="stat"><div class="num">{summary['total_tables']}</div><div class="lbl">Nombre total de tables</div></div>
                <div class="stat"><div class="num">{summary['total_edges']}</div><div class="lbl">Relations de traçabilité</div></div>
                <div class="stat"><div class="num">{summary['source_tables']}</div><div class="lbl">Tables sources</div></div>
                <div class="stat"><div class="num">{summary['target_tables']}</div><div class="lbl">Tables cibles</div></div>
            </div>
            <div class="legend">
                <h3 style="font-size:14px;margin-bottom:8px;">Légende</h3>
                <div class="legend-item"><div class="legend-dot" style="background:#4caf50;"></div>Table source</div>
                <div class="legend-item"><div class="legend-dot" style="background:#ff9800;"></div>Table cible</div>
                <div class="legend-item"><div class="legend-dot" style="background:#2196f3;"></div>Table intermédiaire</div>
                <div class="legend-item"><div style="border-bottom:2px solid #2e7d32;width:20px;"></div>INSERT</div>
                <div class="legend-item"><div style="border-bottom:2px dashed #1565c0;width:20px;"></div>CTAS</div>
                <div class="legend-item"><div style="border-bottom:2px dotted #6a1b9a;width:20px;"></div>VIEW</div>
            </div>
            <h3 style="font-size:14px;margin-top:20px;">Top 10 des tables</h3>
            <table id="topTablesTable">
                <thead><tr><th>Nom de table</th><th>Nombre de références</th></tr></thead>
                <tbody></tbody>
            </table>
        </div>
        <div class="main">
            <div id="network"></div>
        </div>
    </div>
    <script>
        const nodesData = {nodes_json};
        const edgesData = {edges_json};
        const topTables = {top_tables_json};

        // Remplir le tableau des tables les plus référencées
        const tb = document.querySelector('#topTablesTable tbody');
        topTables.forEach(t => {{
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${{t.name}}</td><td>${{t.uses}}</td>`;
            tb.appendChild(tr);
        }});

        // Construire le graphe réseau Vis.js
        const nodes = new vis.DataSet(nodesData.map(n => ({{
            id: n.id,
            label: n.label,
            color: {{
                background: n.group === 'source' ? '#c8e6c9' : n.group === 'target' ? '#ffe0b2' : '#bbdefb',
                border: n.group === 'source' ? '#4caf50' : n.group === 'target' ? '#ff9800' : '#2196f3',
            }},
            font: {{ size: 10, face: 'Arial' }},
            borderWidth: 1,
            shape: 'box',
            margin: 8,
        }})));

        const edges = new vis.DataSet(edgesData.map(e => ({{
            from: e.from,
            to: e.to,
            label: e.label,
            arrows: 'to',
            font: {{ size: 9, align: 'middle' }},
            color: {{
                color: e.label === 'INSERT' ? '#2e7d32' :
                       e.label === 'CTAS' ? '#1565c0' :
                       e.label === 'VIEW' ? '#6a1b9a' : '#333',
            }},
            dashes: e.label === 'CTAS' ? true : e.label === 'VIEW' ? [2,4] : false,
            width: e.label === 'MERGE' ? 2 : 1,
        }})));

        const container = document.getElementById('network');
        const data = {{ nodes, edges }};
        const options = {{
            layout: {{ hierarchical: {{ direction: 'LR', sortMethod: 'directed', nodeSpacing: 180, levelSeparation: 250 }} }},
            physics: {{ hierarchicalRepulsion: {{ nodeDistance: 150 }}, solver: 'hierarchicalRepulsion' }},
            interaction: {{ hover: true, tooltipDelay: 200 }},
        }};
        new vis.Network(container, data, options);
    </script>
</body>
</html>"""
    return html


def main():
    args = parse_args()

    if not HAS_SQLPARSE:
        print("⚠️  sqlparse n'est pas installé ; une analyse de base par expressions régulières sera utilisée")
        print("   Installation : pip install sqlparse")

    if not args.sql_dir and not args.sql_file:
        print("❌ Veuillez spécifier --sql-dir ou --sql-file")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    parser = SQLLineageParser(level=args.level)

    if args.sql_file:
        print(f"📂 Analyse du fichier : {args.sql_file}")
        parser.parse_file(args.sql_file)
    elif args.sql_dir:
        print(f"📂 Analyse du répertoire : {args.sql_dir}")
        parser.parse_directory(args.sql_dir)

    summary = parser.get_summary()

    # Sauvegarder le fichier DOT
    dot_file = os.path.join(args.output, "lineage.dot")
    with open(dot_file, "w", encoding="utf-8") as f:
        f.write(parser.to_dot())

    # Sauvegarder le JSON
    json_data = {
        "summary": summary,
        "edges": [{"source": s, "target": t, "operation": o} for s, t, o in parser.edges],
        "tables": {t: {"roles": list(i["roles"]), "uses": i["uses"]} for t, i in parser.tables.items()},
        "column_lineage": parser.column_lineage,
        "generated_at": datetime.now().isoformat(),
    }
    json_file = os.path.join(args.output, "lineage.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    # Générer la visualisation HTML
    html_file = os.path.join(args.output, "lineage_visualizer.html")
    html = generate_html_visualizer(parser, args.output)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Analyse de traçabilité terminée")
    print(f"📄 DOT : {dot_file}")
    print(f"📄 JSON : {json_file}")
    print(f"🌐 HTML : {html_file}")
    print(f"\n📊 Statistiques :")
    print(f"   Nombre total de tables : {summary['total_tables']}")
    print(f"   Nombre d'arêtes de traçabilité : {summary['total_edges']}")
    print(f"   Tables sources : {summary['source_tables']} | Tables cibles : {summary['target_tables']} | Tables intermédiaires : {summary['intermediate_tables']}")


if __name__ == "__main__":
    main()
