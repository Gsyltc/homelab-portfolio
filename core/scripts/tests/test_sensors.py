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

ADR = """# ADR
---
auteurs: A
accepté par: ""
accepté le: ""
supersedes: ""
superseded_by: ""
---
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
- a
### Négatives
- b
## Alternatives étudiées
- c
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
            self.assertIn(sid, sensor.CHECKS)
            self.assertNotIn("non-exécutable", m.meta["command"])

    def test_every_stage_sensor_is_executable(self) -> None:
        import re
        stages = Path(__file__).resolve().parents[2] / "common" / "stages"
        for f in stages.rglob("*.md"):
            m = re.search(r"^sensors:\s*\[(.*?)\]", f.read_text(encoding="utf-8"), re.M)
            for sid in [x.strip() for x in (m.group(1).split(",") if m else []) if x.strip()]:
                self.assertIn(sid, sensor.CHECKS, f"{f.name}: sensor {sid} non exécutable")


class SensorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = Project()
        self.addCleanup(self.p.tmp.cleanup)

    def test_required_sections_adr(self) -> None:
        self.p.write("decisions/0001-x.md", ADR)
        self.assertEqual(self.p.verdict("required-sections", ["decisions/0001-x.md"]), OK)
        self.p.write("decisions/0002-y.md", ADR.replace("- d\n", "").replace("- c\n", ""))
        r = self.p.fire("required-sections", ["decisions/0002-y.md"])[0]
        self.assertEqual(r.verdict, GAP)
        self.assertTrue(any("vide" in f for f in r.findings))

    def test_required_sections_out_of_scope_is_unavailable(self) -> None:
        self.p.write("README.md", "x")
        self.assertEqual(self.p.verdict("required-sections", ["README.md"]), UNAVAILABLE)
        self.assertEqual(self.p.verdict("required-sections"), UNAVAILABLE)  # périmètre vide

    def test_required_sections_gate_reports_missing_das_files(self) -> None:
        self.p.write("documentation/01-introduction.md", "## Contexte\nx\n## Périmètre\ny\n## Parties prenantes\nz\n")
        rs = self.p.fire("required-sections")
        self.assertEqual(rs[0].verdict, OK)
        self.assertEqual(rs[-1].verdict, GAP)
        self.assertTrue(any("11-securite.md" in f for f in rs[-1].findings))

    def test_template_only_section_is_empty(self) -> None:
        self.p.write("documentation/01-introduction.md", "## Contexte\n<!-- à remplir -->\n## Périmètre\n| a | b |\n|---|---|\n| <x> | ... |\n## Parties prenantes\nz\n")
        r = self.p.fire("required-sections", ["documentation/01-introduction.md"])[0]
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
        rs = sensor.run_sensor("required-sections", self.p.root, ["decisions/0001-x.md"], sensor.load_manifests(), None)
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
        self.assertNotIn("required-sections", out)  # fire_on: gate => pas au hook

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


if __name__ == "__main__":
    unittest.main()
