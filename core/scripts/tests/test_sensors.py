"""Tests des sensors exécutables : `python3 -m unittest discover -s core/scripts/tests`."""

from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("SENSORS_SOURCE_COMMIT", "test")

import sensor  # noqa: E402
from sensorlib import common  # noqa: E402
from sensorlib.common import GAP, OK, UNAVAILABLE  # noqa: E402

ADR = """---
auteurs: A
parties_prenantes: ""
accepte_par: ""
accepte_le: ""
supersedes: ""
superseded_by: ""
---
# ADR
## Status
Proposed
## Date de création
2026-01-02
## Contexte
Issue HOM-1, exigence FR-001.
## Décision
On fait X.
## Conséquences
### Positives
- POS-001 : a
### Négatives
- NEG-001 : b
## Alternatives étudiées
- ALT-001 : c
## Notes d'implémentation
- d
## Références
- HOM-1
"""


class Project:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def write(self, rel: str, content: str) -> None:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def fire(self, sid: str, paths: list[str] | None = None) -> list[common.Result]:
        m = sensor.load_manifests()
        return sensor.run_sensor(sid, self.root, paths, m, "test")

    def verdict(self, sid: str, paths: list[str] | None = None) -> str:
        return common.worst(self.fire(sid, paths))


class GlobTests(unittest.TestCase):
    def test_glob(self) -> None:
        g = "{documentation/*.md,decisions/[0-9][0-9][0-9][0-9]-*.md}"
        self.assertTrue(common.glob_match(g, "decisions/0001-x.md"))
        self.assertTrue(common.glob_match(g, "documentation/01.md"))
        self.assertFalse(common.glob_match(g, "documentation/a/01.md"))
        self.assertTrue(common.glob_match("documentation/**/*.md", "documentation/a/b/c.md"))
        self.assertTrue(common.glob_match("documentation/**/*.md", "documentation/c.md"))


class ManifestTests(unittest.TestCase):
    def test_all_manifests_valid_and_implemented(self) -> None:
        for sid, m in sensor.load_manifests().items():
            self.assertTrue(m.valid, f"{sid}: {m.missing}")
            self.assertIsNotNone(sensor.load_check(sid), f"{sid}: script absent/invalide")
            self.assertNotIn("non-exécutable", m.meta["command"])
            self.assertTrue(sensor.script_path(sid).is_file(), f"{sid}: {sensor.script_path(sid)} manquant")

    def test_every_stage_sensor_is_executable(self) -> None:
        import re
        stages = Path(__file__).resolve().parents[2] / "common" / "stages"
        for f in stages.rglob("*.md"):
            m = re.search(r"^sensors:\s*\[(.*?)\]", f.read_text(encoding="utf-8"), re.M)
            for sid in [x.strip() for x in (m.group(1).split(",") if m else []) if x.strip()]:
                self.assertIsNotNone(sensor.load_check(sid), f"{f.name}: sensor {sid} sans script exécutable")


class OneScriptPerSensorTests(unittest.TestCase):
    def test_bijection_manifest_script(self) -> None:
        manifests = set(sensor.load_manifests())
        scripts = {p.stem.replace("_", "-") for p in sensor.SCRIPTS_DIR.glob("*.py") if p.stem != "__init__"}
        self.assertEqual(manifests, scripts, "chaque manifeste a un script et réciproquement")
        self.assertEqual(len(scripts), 11)

    def test_each_script_exposes_run_and_id(self) -> None:
        for sid in sensor.load_manifests():
            path = sensor.script_path(sid)
            self.assertTrue(path.is_file(), f"{sid}: script manquant")
            self.assertEqual(path.read_text(encoding="utf-8").count("def run("), 1, f"{sid}: un seul run attendu")
            self.assertIsNotNone(sensor.load_check(sid), f"{sid}: run/ID invalide")

    def test_script_runs_standalone(self) -> None:
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            for sid in sensor.load_manifests():
                r = subprocess.run([sys.executable, str(sensor.script_path(sid)), "--root", d],
                                   capture_output=True, text=True, env={**os.environ, "SENSORS_SOURCE_COMMIT": "t"})
                self.assertEqual(r.returncode, 0, f"{sid}: {r.stderr}")
                self.assertIn(f"Sensor {sid}", r.stdout, f"{sid}: {r.stdout}")

    def test_missing_script_is_unavailable(self) -> None:
        self.assertIsNone(sensor.load_check("inexistant"))


class SensorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = Project()
        self.addCleanup(self.p.tmp.cleanup)

    def test_required_sections_adr(self) -> None:
        self.p.write("decisions/0001-x.md", ADR)
        self.assertEqual(self.p.verdict("required-sections-adr", ["decisions/0001-x.md"]), OK)
        self.p.write("decisions/0002-y.md", ADR.replace("- d\n", "").replace("- ALT-001 : c\n", ""))
        r = self.p.fire("required-sections-adr", ["decisions/0002-y.md"])[0]
        self.assertEqual(r.verdict, GAP)
        self.assertTrue(any("vide" in f for f in r.findings))

    def test_required_sections_adr_shape(self) -> None:
        def gaps(name: str, text: str) -> list[str]:
            self.p.write(f"decisions/{name}.md", text)
            return self.p.fire("required-sections-adr", [f"decisions/{name}.md"])[0].findings

        self.assertTrue(any("front matter absent" in f for f in gaps("0003-a", ADR.replace("---\nauteurs", "# T\n---\nauteurs", 1))))
        self.assertTrue(any("parties_prenantes" in f for f in gaps("0004-b", ADR.replace('parties_prenantes: ""\n', ""))))
        self.assertTrue(any("hors" in f for f in gaps("0005-c", ADR.replace("Proposed", "Brouillon"))))
        self.assertTrue(any("statut unique" in f for f in gaps("0006-d", ADR.replace("Proposed", "Proposed\nAccepted"))))
        self.assertEqual(gaps("0007-e", ADR.replace("Proposed", "Superseded par [ADR-0001](0001-x.md)")), [])
        self.assertTrue(any("POS-NNN" in f for f in gaps("0008-f", ADR.replace("POS-001", "x"))))
        self.assertTrue(any("ALT-NNN" in f for f in gaps("0009-g", ADR.replace("ALT-001", "x"))))
        self.assertTrue(any("introuvable" in f for f in gaps("0010-h", ADR.replace('superseded_by: ""', "superseded_by: 0099"))))

    def test_required_sections_adr_criteres_depuis_2026_11_11(self) -> None:
        self.p.write("decisions/0011-i.md", ADR.replace("2026-01-02", "2026-11-11"))
        r = self.p.fire("required-sections-adr", ["decisions/0011-i.md"])[0]
        self.assertTrue(any("Critères de décision" in f for f in r.findings))
        self.p.write("decisions/0012-j.md", ADR.replace("2026-01-02", "2026-11-11").replace("## Décision", "## Critères de décision\n- C1 : must\n## Décision"))
        self.assertEqual(self.p.verdict("required-sections-adr", ["decisions/0012-j.md"]), OK)

    def test_required_sections_out_of_scope_is_unavailable(self) -> None:
        self.p.write("README.md", "x")
        self.assertEqual(self.p.verdict("required-sections-adr", ["README.md"]), UNAVAILABLE)
        self.assertEqual(self.p.verdict("required-sections-architecture", ["README.md"]), UNAVAILABLE)
        self.assertEqual(self.p.verdict("required-sections-adr"), UNAVAILABLE)  # périmètre vide

    def test_required_sections_gate_reports_missing_das_files(self) -> None:
        self.p.write("documentation/01-introduction.md", "## Contexte\nx\n## Périmètre\ny\n## Parties prenantes\nz\n")
        rs = self.p.fire("required-sections-architecture")
        self.assertEqual(rs[0].verdict, OK)
        self.assertEqual(rs[-1].verdict, GAP)
        self.assertTrue(any("11-securite.md" in f for f in rs[-1].findings))

    def test_required_sections_architecture_covers_detailed_chapter(self) -> None:
        d = "documentation/architecture-securite/"
        self.p.write(d + "01-surfaces-et-actifs.md", "## Surfaces d'attaque\nS1\n")
        rs = self.p.fire("required-sections-architecture")
        self.assertEqual(rs[0].verdict, OK)
        self.assertEqual(rs[-1].verdict, GAP)
        self.assertTrue(any("02-menaces-stride.md" in f for f in rs[-1].findings))
        self.assertTrue(any("11-securite.md" in f for f in rs[-1].findings))  # DAS et détaillée : un seul sensor

    def test_sujets_a_jour(self) -> None:
        doc = "---\ndoc_id: x\nsujets:\n  - Alpha\n  - Beta (v2)\n---\n## Alpha\ntexte\n### Beta (v2)\ntexte\n#### Détail\n"
        self.p.write("documentation/a.md", doc)
        self.assertEqual(self.p.verdict("sujets-a-jour", ["documentation/a.md"]), OK)
        self.p.write("documentation/b.md", doc + "## Gamma\n")  # titre ajouté sans maj de sujets
        r = self.p.fire("sujets-a-jour", ["documentation/b.md"])[0]
        self.assertEqual(r.verdict, GAP)
        self.assertTrue(any("Gamma" in f for f in r.findings))
        self.p.write("documentation/c.md", doc.replace("### Beta (v2)", "### Delta"))  # titre renommé
        r = self.p.fire("sujets-a-jour", ["documentation/c.md"])[0]
        self.assertTrue(any("Beta" in f for f in r.findings) and any("Delta" in f for f in r.findings))
        self.p.write("documentation/d.md", doc.replace("sujets:\n  - Alpha\n  - Beta (v2)", "sujets: [\"Beta (v2)\", Alpha]"))
        r = self.p.fire("sujets-a-jour", ["documentation/d.md"])[0]
        self.assertTrue(any("ordre" in f for f in r.findings))
        self.p.write("documentation/e.md", "---\ndoc_id: x\n---\n## Alpha\n")  # sans `sujets` : hors périmètre
        self.assertEqual(self.p.verdict("sujets-a-jour", ["documentation/e.md"]), UNAVAILABLE)

    def test_template_only_section_is_empty(self) -> None:
        self.p.write("documentation/01-introduction.md", "## Contexte\n<!-- à remplir -->\n## Périmètre\n| a | b |\n|---|---|\n| <x> | ... |\n## Parties prenantes\nz\n")
        r = self.p.fire("required-sections-architecture", ["documentation/01-introduction.md"])[0]
        self.assertEqual(r.verdict, GAP)
        self.assertEqual(len(r.findings), 2)

    def test_upstream_coverage(self) -> None:
        self.p.write("decisions/0001-x.md", ADR)
        self.p.write("decisions/0002-y.md", ADR.replace("HOM-1", "rien"))
        rs = {r.target: r.verdict for r in self.p.fire("upstream-coverage")}
        self.assertEqual(rs["decisions/0001-x.md"], OK)
        self.assertEqual(rs["decisions/0002-y.md"], GAP)

    def test_diagram_validity(self) -> None:
        good = "```mermaid\nflowchart LR\n  A[a] --> B(b)\n  subgraph S\n   C\n  end\n```\n"
        bad = "```mermaid\nflowchrt LR\n  A[a --> B\n```\n"
        self.p.write("documentation/a.md", good + "```plantuml\n@startuml\nA -> B\n@enduml\n```\n")
        self.p.write("documentation/b.md", bad + "```plantuml\n@startuml\nA -> B\n```\n")
        self.assertEqual(self.p.verdict("diagram-validity", ["documentation/a.md"]), OK)
        r = self.p.fire("diagram-validity", ["documentation/b.md"])[0]
        self.assertEqual(r.verdict, GAP)
        self.assertGreaterEqual(len(r.findings), 3)

    def test_diagram_remote_include_flagged(self) -> None:
        self.p.write("documentation/c.puml", "@startuml\n!include https://evil.example/x.puml\n@enduml\n")
        r = self.p.fire("diagram-validity", ["documentation/c.puml"])[0]
        self.assertEqual(r.verdict, GAP)
        self.assertIn("SG-4", r.findings[0])

    def test_detailed_arch_refs(self) -> None:
        self.p.write("documentation/06.md", "# T\nVoir [x](architecture-detaillee/sys/a.md) et [ok](documentation/Sys#ancre)\n```\n[c](architecture-securite/b.md)\n```\n## Détail (SYS-001 Core)\n")
        r = self.p.fire("detailed-arch-refs", ["documentation/06.md"])[0]
        self.assertEqual(r.verdict, GAP)
        self.assertEqual(len(r.findings), 2)

    def test_data_lifecycle(self) -> None:
        self.assertEqual(self.p.verdict("data-lifecycle"), GAP)  # fichier absent
        self.p.write("documentation/10-cycle_vie_donnees.md",
                     "## Cycle de vie des données\nCollecte puis stockage chiffré.\n## Gouvernance de données\nPropriétaire : DSI\n## Classification des données\n| Donnée | Niveau |\n|---|---|\n| Emails | Confidentiel |\n")
        self.assertEqual(self.p.verdict("data-lifecycle"), OK)
        self.p.write("documentation/10-cycle_vie_donnees.md",
                     "## Cycle de vie des données\n<!-- x -->\n## Gouvernance de données\nPropriétaire\n## Classification des données\n| a | b |\n|---|---|\n| <x> | <y> |\n")
        self.assertEqual(self.p.verdict("data-lifecycle"), GAP)

    def test_checklist_progress(self) -> None:
        # Checklist absente ⇒ ⛔ indisponible (SG-2, jamais lu comme conforme).
        self.assertEqual(self.p.verdict("checklist-progress"), UNAVAILABLE)
        # Checklist renseignée ⇒ ✅ avec les quatre avancements restitués.
        self.p.write(
            "documentation/00-checklist-architecture.md",
            "# Checklist d'architecture — état d'avancement\n\n"
            "**% global :** 42 %\n\n"
            "## Cadrage — 80 %\n\n"
            "## Besoins (MoSCoW) — 35 %\n\n"
            "## Livrables — 20 %\n\n"
            "## Projets — 10 %\n",
        )
        r = self.p.fire("checklist-progress")[0]
        self.assertEqual(r.verdict, OK)
        joined = "\n".join([r.summary, *r.findings])
        self.assertIn("solution 42 %", r.summary)
        self.assertIn("avancement global de la solution : 42 %", joined)
        self.assertIn("avancement du cadrage : 80 %", joined)
        self.assertIn("avancement des besoins (MoSCoW) : 35 %", joined)
        self.assertIn("avancement des livrables : 20 %", joined)
        # Le sensor constate : il n'écrit rien, n'émet jamais ⚠️ (avancement bas = fait, pas écart).
        self.assertNotEqual(r.verdict, GAP)

    def test_claim_sources(self) -> None:
        self.p.write("decisions/0001-x.md", ADR)
        self.p.write("documentation/a.md", "Voir [ok](../decisions/0001-x.md) et [ko](nope.md), ADR-0099.\nHypothèse : volume stable.\nHypothèse : B (confirmée par l'humain le 2026-01-01)\n")
        self.assertEqual(self.p.verdict("claim-sources", ["decisions/0001-x.md"]), OK)
        r = self.p.fire("claim-sources", ["documentation/a.md"])[0]
        self.assertEqual(r.verdict, GAP)
        self.assertEqual(len(r.findings), 3)

    def test_traceability(self) -> None:
        self.assertEqual(self.p.verdict("traceability"), UNAVAILABLE)  # fail closed
        self.p.write("documentation/02.md", "| BA-1 | Must | FR-001 |\n| BA-2 | pas de priorité | FR-002 |\n| BA-3 | Should | - |\n")
        self.p.write("decisions/0001-x.md", ADR.replace("FR-001", "FR-001 BA-1"))
        r = self.p.fire("traceability")[0]
        self.assertEqual(r.verdict, GAP)
        joined = "\n".join(r.findings)
        self.assertIn("BA-2", joined)
        self.assertIn("BA-3", joined)
        self.assertIn("FR-002", joined)
        self.assertNotIn("BA-1 (", joined)

    def test_invalid_manifest_is_unavailable(self) -> None:
        m = sensor.load_manifests()
        m["traceability"].missing.append("origine")
        self.assertEqual(common.worst(sensor.run_sensor("traceability", self.p.root, None, m, "t")), UNAVAILABLE)

    def test_untraceable_commit_is_unavailable(self) -> None:
        self.p.write("decisions/0001-x.md", ADR)
        rs = sensor.run_sensor("required-sections-adr", self.p.root, ["decisions/0001-x.md"], sensor.load_manifests(), None)
        self.assertEqual(common.worst(rs), UNAVAILABLE)


class GateAndHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = Project()
        self.addCleanup(self.p.tmp.cleanup)

    def test_gate_never_green_on_abstract_artefacts(self) -> None:
        self.p.write("decisions/0001-x.md", ADR)
        verdict, report = sensor.run_gate("entree-inception", self.p.root, set(), "t")
        self.assertEqual(verdict, UNAVAILABLE)
        self.assertIn("demande_brute_consignee", report)
        verdict, _ = sensor.run_gate("entree-inception", self.p.root,
                                     {"demande_brute_consignee", "repertoire_projet_confirme", "scope_confirme"}, "t")
        self.assertEqual(verdict, OK)

    def test_gate_all_boundaries_parse(self) -> None:
        self.assertEqual(set(sensor.parse_boundaries()), {"entree-inception", "inception-construction", "construction-operation", "operation-fin"})
        b = sensor.parse_boundaries()["construction-operation"]
        self.assertIn("traceability", b["sensors"])
        self.assertIn("liaison-tracabilite", b["checks"])

    def _hook(self, payload: dict, *extra: str) -> tuple[int, str]:
        old = sys.stdin
        sys.stdin = io.StringIO(json.dumps(payload))
        out = io.StringIO()
        try:
            with redirect_stdout(out):
                rc = sensor.main(["--root", str(self.p.root), "hook", *extra])
        finally:
            sys.stdin = old
        return rc, out.getvalue()

    def test_hook_fires_write_sensors_only_and_never_blocks(self) -> None:
        self.p.write("documentation/06.md", "```mermaid\nflowchrt LR\n```\n")
        rc, out = self._hook({"tool_input": {"file_path": str(self.p.root / "documentation/06.md")}})
        self.assertEqual(rc, 0)
        self.assertIn("Sensor diagram-validity", out)
        self.assertIn("⚠️", out)
        self.assertNotIn("required-sections-architecture", out)  # fire_on: gate => pas au hook

    def test_hook_fires_required_sections_on_adr_write_only(self) -> None:
        self.p.write("decisions/0001-x.md", ADR.replace("Proposed", "Brouillon"))
        rc, out = self._hook({"tool_input": {"file_path": str(self.p.root / "decisions/0001-x.md")}})
        self.assertEqual(rc, 0)
        self.assertIn("Sensor required-sections-adr", out)  # write_matches : ADR contrôlé à l'écriture
        self.assertIn("hors", out)
        self.p.write("documentation/06.md", "## x\n")
        _, out = self._hook({"tool_input": {"file_path": str(self.p.root / "documentation/06.md")}})
        self.assertNotIn("required-sections-architecture", out)  # DAS : gate seul

    def test_hook_claude_format_and_audit_file(self) -> None:
        self.p.write("documentation/06.md", "# ok\n")
        audit = self.p.root / "audit.md"
        rc, out = self._hook({"tool_input": {"file_path": "documentation/06.md"}}, "--format", "claude", "--audit-file", str(audit))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertIn("detailed-arch-refs", audit.read_text(encoding="utf-8"))

    def test_hook_ignores_outside_and_garbage(self) -> None:
        self.assertEqual(self._hook({"tool_input": {"file_path": "/etc/passwd"}}), (0, ""))
        old = sys.stdin
        sys.stdin = io.StringIO("pas du json")
        try:
            self.assertEqual(sensor.main(["--root", str(self.p.root), "hook"]), 0)
        finally:
            sys.stdin = old

    def test_hook_respects_stage_sensor_filter(self) -> None:
        self.p.write("documentation/06.md", "```mermaid\nflowchrt LR\n```\n")
        _, out = self._hook({"tool_input": {"file_path": "documentation/06.md"}}, "--sensors", "detailed-arch-refs")
        self.assertNotIn("diagram-validity", out)


class ReportCheckTests(unittest.TestCase):
    """Durcissement 2 (ORIG-418) : contrôle de gate du compte rendu — section `## Sensors` vs `sensors:`."""

    def setUp(self) -> None:
        self.p = Project()
        self.addCleanup(self.p.tmp.cleanup)

    def _stage(self, rel: str, sensors: str | None) -> Path:
        body = "---\nslug: s\n"
        if sensors is not None:
            body += f"sensors: [{sensors}]\n"
        body += "---\n# Stage\n"
        self.p.write(rel, body)
        return self.p.root / rel

    def test_stage_sensors_parsing(self) -> None:
        self.assertEqual(sensor.stage_sensors(self._stage("s.md", "a, b, c")), ["a", "b", "c"])
        self.assertEqual(sensor.stage_sensors(self._stage("e.md", "")), [])
        self.assertEqual(sensor.stage_sensors(self._stage("n.md", None)), [])
        self.assertIsNone(sensor.stage_sensors(self.p.root / "absent.md"))

    def test_report_has_sensors_section(self) -> None:
        self.assertTrue(sensor.report_has_sensors_section("## Résumé\n- x\n## Sensors\n- `a` : ✅\n"))
        self.assertFalse(sensor.report_has_sensors_section("## Résumé\n- x\n"))
        self.assertFalse(sensor.report_has_sensors_section("## Résumé\n- x\n## Sensors\n\n## Fin\n- y\n"))

    def test_declared_sensors_but_no_section_is_gap(self) -> None:
        stage = self._stage("prod.md", "style-concision, claim-sources")
        r = sensor.check_report(stage, "## Résumé\n- fait X\n")
        self.assertEqual(r.verdict, GAP)
        self.assertEqual(len(r.findings), 2)
        self.assertTrue(any("style-concision" in f for f in r.findings))

    def test_declared_sensors_with_section_is_ok(self) -> None:
        stage = self._stage("prod.md", "style-concision")
        r = sensor.check_report(stage, "## Résumé\n- x\n## Sensors\n- `style-concision` : ✅ conforme\n")
        self.assertEqual(r.verdict, OK)

    def test_no_declared_sensors_is_ok_even_without_section(self) -> None:
        stage = self._stage("framing.md", "")
        self.assertEqual(sensor.check_report(stage, "## Résumé\n- x\n").verdict, OK)
        stage2 = self._stage("framing2.md", None)
        self.assertEqual(sensor.check_report(stage2, "## Résumé\n- x\n").verdict, OK)

    def test_missing_stage_is_unavailable(self) -> None:
        r = sensor.check_report(self.p.root / "absent.md", "## Résumé\n- x\n")
        self.assertEqual(r.verdict, UNAVAILABLE)

    def test_report_check_cli_advisory_and_strict(self) -> None:
        stage = self._stage("prod.md", "style-concision")
        report = self.p.root / "r.md"
        report.write_text("## Résumé\n- x\n", encoding="utf-8")
        old = sys.stdin
        try:
            sys.stdin = io.StringIO("")
            out = io.StringIO()
            with redirect_stdout(out):
                rc = sensor.main(["--root", str(self.p.root), "report-check", "--stage", str(stage),
                                  "--report-file", str(report)])
            self.assertEqual(rc, 0)  # advisory : code 0 même en écart
            self.assertIn("⚠️", out.getvalue())
            rc_strict = sensor.main(["--root", str(self.p.root), "--strict", "report-check",
                                     "--stage", str(stage), "--report-file", str(report)])
            self.assertEqual(rc_strict, 1)  # --strict : code 1 (CI uniquement)
        finally:
            sys.stdin = old

    def test_report_check_json(self) -> None:
        stage = self._stage("prod.md", "style-concision")
        report = self.p.root / "r.md"
        report.write_text("## Résumé\n- x\n## Sensors\n- `style-concision` : ✅\n", encoding="utf-8")
        out = io.StringIO()
        with redirect_stdout(out):
            sensor.main(["--root", str(self.p.root), "report-check", "--stage", str(stage),
                         "--report-file", str(report), "--format", "json"])
        data = json.loads(out.getvalue())
        self.assertEqual(data["verdict"], OK)
        self.assertEqual(data["result"]["sensor"], "report-sensors-section")


if __name__ == "__main__":
    unittest.main()
