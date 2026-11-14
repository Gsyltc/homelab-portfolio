"""Tests des sensors exécutables Homelab : `python3 -m unittest discover -s homelab/scripts/tests`."""

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
from sensorlib import yamlmini  # noqa: E402
from sensorlib.common import GAP, OK, UNAVAILABLE  # noqa: E402


class Project:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def write(self, rel: str, content: str) -> str:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return str(p)

    def cleanup(self) -> None:
        self.tmp.cleanup()


def fire(root: Path, sid: str, rel_paths: list[str], scope: str | None = None) -> dict:
    argv = ["--root", str(root), "fire", sid, "--format", "json"]
    if scope:
        argv += ["--scope", scope]
    if rel_paths:
        argv += ["--path", *[str(root / p) for p in rel_paths]]
    buf = io.StringIO()
    with redirect_stdout(buf):
        sensor.main(argv)
    return json.loads(buf.getvalue())


def verdict(report: dict) -> str:
    return report["verdict"]


# --------------------------------------------------------------------------- #
# yamlmini (parser statique)
# --------------------------------------------------------------------------- #


class TestYamlMini(unittest.TestCase):
    def test_valid_mapping(self):
        node = yamlmini.parse("services:\n  web:\n    image: nginx\n")
        self.assertIn("services", node.mapping)
        self.assertIn("web", yamlmini.services(node))

    def test_duplicate_key(self):
        with self.assertRaises(yamlmini.YamlError) as cm:
            yamlmini.parse("a: 1\nb: 2\na: 3\n")
        self.assertIn("dupliquée", cm.exception.message)

    def test_tab_indent(self):
        with self.assertRaises(yamlmini.YamlError) as cm:
            yamlmini.parse("services:\n\tweb: x\n")
        self.assertIn("tabulation", cm.exception.message)

    def test_sequence(self):
        node = yamlmini.parse("items:\n  - a\n  - b\n")
        self.assertEqual(node.mapping["items"].kind, "seq")
        self.assertEqual(len(node.mapping["items"].items), 2)

    def test_multi_document(self):
        self.assertEqual(yamlmini.split_documents("a: 1\n---\nb: 2\n"), 2)
        self.assertEqual(yamlmini.split_documents("a: 1\nb: 2\n"), 1)

    def test_inline_comment_ignored(self):
        node = yamlmini.parse("image: nginx  # commentaire : non une clé\n")
        self.assertEqual(node.mapping["image"].scalar, "nginx")


# --------------------------------------------------------------------------- #
# yaml-validity
# --------------------------------------------------------------------------- #


class TestYamlValidity(unittest.TestCase):
    def setUp(self):
        self.p = Project()

    def tearDown(self):
        self.p.cleanup()

    def test_valid(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    image: nginx\n")
        self.assertEqual(verdict(fire(self.p.root, "yaml-validity", ["docker-compose.yml"])), OK)

    def test_duplicate_key_is_gap(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    image: a\n    image: b\n")
        self.assertEqual(verdict(fire(self.p.root, "yaml-validity", ["docker-compose.yml"])), GAP)

    def test_multi_document_is_gap(self):
        self.p.write("docker-compose.yml", "services:\n  a:\n    image: x\n---\nservices:\n  b:\n    image: y\n")
        self.assertEqual(verdict(fire(self.p.root, "yaml-validity", ["docker-compose.yml"])), GAP)

    def test_out_of_scope_tf_is_unavailable(self):
        path = self.p.write("main.tf", "foo = 1\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            sensor.main(["--root", str(self.p.root), "fire", "yaml-validity", "--format", "json", "--path", path])
        self.assertEqual(json.loads(buf.getvalue())["verdict"], UNAVAILABLE)


# --------------------------------------------------------------------------- #
# swarm-deploy-section
# --------------------------------------------------------------------------- #


class TestSwarmDeploy(unittest.TestCase):
    def setUp(self):
        self.p = Project()

    def tearDown(self):
        self.p.cleanup()

    def test_deploy_present(self):
        self.p.write("docker-compose.yml",
                     "services:\n  web:\n    image: nginx\n    deploy:\n      placement:\n        constraints:\n          - node.role==manager\n")
        self.assertEqual(verdict(fire(self.p.root, "swarm-deploy-section", ["docker-compose.yml"])), OK)

    def test_missing_deploy_is_gap(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    image: nginx\n")
        self.assertEqual(verdict(fire(self.p.root, "swarm-deploy-section", ["docker-compose.yml"])), GAP)

    def test_non_swarm_directive_is_gap(self):
        self.p.write("docker-compose.yml",
                     "services:\n  web:\n    image: nginx\n    restart: always\n    deploy:\n      replicas: 1\n")
        rep = fire(self.p.root, "swarm-deploy-section", ["docker-compose.yml"])
        self.assertEqual(verdict(rep), GAP)
        self.assertTrue(any("restart" in f for r in rep["results"] for f in r["findings"]))

    def test_not_a_compose_is_unavailable(self):
        self.p.write("docker-compose.yml", "version: \"3.8\"\n")
        self.assertEqual(verdict(fire(self.p.root, "swarm-deploy-section", ["docker-compose.yml"])), UNAVAILABLE)


# --------------------------------------------------------------------------- #
# plaintext-secret
# --------------------------------------------------------------------------- #


class TestPlaintextSecret(unittest.TestCase):
    def setUp(self):
        self.p = Project()

    def tearDown(self):
        self.p.cleanup()

    def test_detects_password(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    environment:\n      - DB_PASSWORD=supersecret123\n")
        rep = fire(self.p.root, "plaintext-secret", ["docker-compose.yml"])
        self.assertEqual(verdict(rep), GAP)

    def test_never_leaks_value(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    environment:\n      - DB_PASSWORD=supersecret123\n")
        rep = fire(self.p.root, "plaintext-secret", ["docker-compose.yml"])
        blob = json.dumps(rep, ensure_ascii=False)
        self.assertNotIn("supersecret123", blob)  # invariant : jamais la valeur
        self.assertIn("DB_PASSWORD", blob)

    def test_file_convention_tolerated(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    environment:\n      - DB_PASSWORD_FILE=/run/secrets/db\n")
        self.assertEqual(verdict(fire(self.p.root, "plaintext-secret", ["docker-compose.yml"])), OK)

    def test_env_ref_tolerated(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    environment:\n      - API_KEY=${API_KEY}\n")
        self.assertEqual(verdict(fire(self.p.root, "plaintext-secret", ["docker-compose.yml"])), OK)

    def test_vault_ref_tolerated(self):
        self.p.write("conf.tfvars", "db_pass = \"vault:kv/stack/db\"\n")
        self.assertEqual(verdict(fire(self.p.root, "plaintext-secret", ["conf.tfvars"])), OK)

    def test_severity_blocking_on_security_scope(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    environment:\n      - DB_PASSWORD=supersecret123\n")
        rep = fire(self.p.root, "plaintext-secret", ["docker-compose.yml"], scope="security-patch")
        self.assertEqual(rep["severities"]["plaintext-secret"], "blocking")

    def test_severity_advisory_off_scope(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    environment:\n      - DB_PASSWORD=supersecret123\n")
        rep = fire(self.p.root, "plaintext-secret", ["docker-compose.yml"], scope="config-change")
        self.assertEqual(rep["severities"]["plaintext-secret"], "advisory")


# --------------------------------------------------------------------------- #
# terraform-no-sni
# --------------------------------------------------------------------------- #


class TestTerraformNoSni(unittest.TestCase):
    def setUp(self):
        self.p = Project()

    def tearDown(self):
        self.p.cleanup()

    def test_clean(self):
        self.p.write("main.tfvars", "domain = \"https://web.example.com\"\n")
        self.assertEqual(verdict(fire(self.p.root, "terraform-no-sni", ["main.tfvars"])), OK)

    def test_sni_detected(self):
        self.p.write("main.tfvars", "host = \"${SNI}\"\n")
        self.assertEqual(verdict(fire(self.p.root, "terraform-no-sni", ["main.tfvars"])), GAP)

    def test_bare_sni_detected(self):
        self.p.write("vars.tf", "x = $SNI\n")
        self.assertEqual(verdict(fire(self.p.root, "terraform-no-sni", ["vars.tf"])), GAP)

    def test_severity_blocking_on_new_stack(self):
        self.p.write("main.tfvars", "host = \"${SNI}\"\n")
        rep = fire(self.p.root, "terraform-no-sni", ["main.tfvars"], scope="new-stack")
        self.assertEqual(rep["severities"]["terraform-no-sni"], "blocking")


# --------------------------------------------------------------------------- #
# traefik-coherence
# --------------------------------------------------------------------------- #


class TestTraefikCoherence(unittest.TestCase):
    def setUp(self):
        self.p = Project()

    def tearDown(self):
        self.p.cleanup()

    def test_coherent(self):
        self.p.write("docker-compose.yml",
                     "services:\n  web:\n    networks:\n      - traefik_frontend\n    labels:\n"
                     "      - \"traefik.enable=true\"\n"
                     "      - \"traefik.http.routers.web.rule=Host(`w.ex.com`)\"\n"
                     "      - \"traefik.http.routers.web.entrypoints=websecure\"\n")
        self.assertEqual(verdict(fire(self.p.root, "traefik-coherence", ["docker-compose.yml"])), OK)

    def test_missing_rule_is_gap(self):
        self.p.write("docker-compose.yml",
                     "services:\n  web:\n    networks:\n      - traefik_frontend\n    labels:\n"
                     "      - \"traefik.enable=true\"\n")
        self.assertEqual(verdict(fire(self.p.root, "traefik-coherence", ["docker-compose.yml"])), GAP)

    def test_no_exposed_service_is_unavailable(self):
        self.p.write("docker-compose.yml", "services:\n  db:\n    image: postgres\n")
        self.assertEqual(verdict(fire(self.p.root, "traefik-coherence", ["docker-compose.yml"])), UNAVAILABLE)


# --------------------------------------------------------------------------- #
# vault-secret-exists
# --------------------------------------------------------------------------- #


class TestVaultSecretExists(unittest.TestCase):
    def setUp(self):
        self.p = Project()

    def tearDown(self):
        self.p.cleanup()

    def test_well_formed(self):
        self.p.write("conf.tfvars", "db = \"vault:kv/mystack/dbpass\"\n")
        self.assertEqual(verdict(fire(self.p.root, "vault-secret-exists", ["conf.tfvars"])), OK)

    def test_malformed_is_gap(self):
        self.p.write("conf.tfvars", "db = \"vault:oops\"\n")
        self.assertEqual(verdict(fire(self.p.root, "vault-secret-exists", ["conf.tfvars"])), GAP)

    def test_no_reference_is_unavailable(self):
        self.p.write("conf.tfvars", "db = \"plain\"\n")
        self.assertEqual(verdict(fire(self.p.root, "vault-secret-exists", ["conf.tfvars"])), UNAVAILABLE)

    def test_never_leaks_value(self):
        self.p.write("conf.tfvars", "db = \"vault:oops\"\n")
        rep = fire(self.p.root, "vault-secret-exists", ["conf.tfvars"])
        # le chemin de référence est restitué, mais aucune valeur de secret n'est lue
        self.assertIn("vault:oops", json.dumps(rep, ensure_ascii=False))


# --------------------------------------------------------------------------- #
# Dispatcher : manifestes, inconnu, gates enrichis, provenance
# --------------------------------------------------------------------------- #


class TestRequiredParameters(unittest.TestCase):
    REL = ".a-valider/HOM-1/sync-in/parametres.json"

    def setUp(self):
        self.p = Project()

    def tearDown(self):
        self.p.cleanup()

    @staticmethod
    def valid() -> dict:
        return {
            "stack_name": "sync-in",
            "cible": "swarm",
            "auth_type": "oidc",
            "fqdn": "sync.jeedom-gaston.ovh",
            "oidc": {"idp": "authentik", "client_name": "sync-in",
                     "redirect_uri": "https://sync.jeedom-gaston.ovh/api/auth/oidc/callback",
                     "scopes": ["openid", "profile", "email"]},
            "storage": {"server": "truenas", "paths": ["/mnt/datas/${ENVIRONMENT}/services/sync-in"]},
            "traefik_network": "traefik_frontend",
            "valkey_enabled": False,
            "database_service": "mariadb",
            "vault_secrets_required": True,
        }

    def run_with(self, params: dict, scope: str | None = None) -> dict:
        self.p.write(self.REL, json.dumps(params))
        return fire(self.p.root, "required-parameters", [self.REL], scope)

    def findings(self, rep: dict) -> str:
        return " ".join(f for r in rep["results"] for f in r["findings"])

    def test_valid(self):
        self.assertEqual(verdict(self.run_with(self.valid())), OK)

    def test_missing_fqdn_is_gap(self):
        params = self.valid()
        del params["fqdn"]
        rep = self.run_with(params)
        self.assertEqual(verdict(rep), GAP)
        self.assertIn("fqdn : requis", self.findings(rep))

    def test_placeholder_domain_is_gap(self):
        params = self.valid()
        params["fqdn"] = "sync.<domaine>"
        self.assertEqual(verdict(self.run_with(params)), GAP)

    def test_foreign_domain_is_gap(self):
        params = self.valid()
        params["fqdn"] = "sync.example.com"
        params["oidc"]["redirect_uri"] = "https://sync.example.com/cb"
        self.assertIn("hors du domaine", self.findings(self.run_with(params)))

    def test_oidc_other_idp_is_gap(self):
        params = self.valid()
        params["oidc"]["idp"] = "keycloak"
        self.assertIn("oidc.idp", self.findings(self.run_with(params)))

    def test_oidc_missing_when_auth_oidc(self):
        params = self.valid()
        del params["oidc"]
        self.assertIn("oidc : requis", self.findings(self.run_with(params)))

    def test_wrong_nfs_server_is_gap(self):
        params = self.valid()
        params["storage"]["server"] = "nas2"
        self.assertIn("storage.server", self.findings(self.run_with(params)))

    def test_wrong_storage_path_is_gap(self):
        params = self.valid()
        params["storage"]["paths"] = ["/data/sync-in"]
        self.assertIn("storage.paths[0]", self.findings(self.run_with(params)))

    def test_unknown_network_is_gap(self):
        params = self.valid()
        params["traefik_network"] = "public"
        self.assertIn("traefik_network", self.findings(self.run_with(params)))

    def test_proxmox_skips_swarm_params(self):
        params = self.valid()
        params["cible"] = "proxmox"
        for k in ("storage", "traefik_network", "valkey_enabled"):
            del params[k]
        self.assertEqual(verdict(self.run_with(params)), OK)

    def test_unknown_key_is_gap(self):
        params = self.valid()
        params["fdqn"] = "x"
        self.assertIn("fdqn : clé inconnue", self.findings(self.run_with(params)))

    def test_secret_key_never_leaks_value(self):
        params = self.valid()
        params["oidc"]["client_secret"] = "S3cr3tValue"
        rep = self.run_with(params)
        self.assertEqual(verdict(rep), GAP)
        self.assertNotIn("S3cr3tValue", json.dumps(rep))

    def test_invalid_json_is_unavailable(self):
        self.p.write(self.REL, "{not json")
        rep = fire(self.p.root, "required-parameters", [self.REL])
        self.assertEqual(verdict(rep), UNAVAILABLE)

    def test_no_file_is_unavailable(self):
        self.assertEqual(verdict(fire(self.p.root, "required-parameters", [])), UNAVAILABLE)

    def test_blocking_on_new_stack(self):
        m = sensor.load_manifests()["required-parameters"]
        self.assertEqual(sensor.resolve_severity(m, "new-stack"), "blocking")
        self.assertEqual(sensor.resolve_severity(m, "config-change"), "advisory")

    def test_gate_phase2_phase3_runs_sensor(self):
        self.p.write(self.REL, json.dumps(self.valid()))
        self.assertIn("required-parameters", sensor.parse_boundaries()["phase2-phase3"]["sensors"])
        buf = io.StringIO()
        with redirect_stdout(buf):
            sensor.main(["--root", str(self.p.root), "gate", "phase2-phase3", "--scope", "new-stack"])
        out = buf.getvalue()
        self.assertIn("required-parameters [BLOQUANT]", out)
        self.assertIn("parametres_requis_complets : ✅", out)


class TestDispatcher(unittest.TestCase):
    def setUp(self):
        self.p = Project()

    def tearDown(self):
        self.p.cleanup()

    def test_all_manifests_valid(self):
        manifests = sensor.load_manifests()
        self.assertEqual(len(manifests), 7)
        for sid, m in manifests.items():
            self.assertTrue(m.valid, f"{sid} invalide : {m.missing}")
            self.assertIsNotNone(sensor.load_check(sid), f"{sid} : script absent/invalide")

    def test_unknown_sensor_is_unavailable(self):
        rep = fire(self.p.root, "does-not-exist", [])
        self.assertEqual(verdict(rep), UNAVAILABLE)

    def test_severity_overrides_parsed(self):
        manifests = sensor.load_manifests()
        ov = sensor.severity_overrides(manifests["plaintext-secret"])
        self.assertTrue(any("security-patch" in scopes and sev == "blocking" for scopes, sev in ov))

    def test_resolve_severity(self):
        m = sensor.load_manifests()["terraform-no-sni"]
        self.assertEqual(sensor.resolve_severity(m, "new-stack"), "blocking")
        self.assertEqual(sensor.resolve_severity(m, "config-change"), "advisory")
        self.assertEqual(sensor.resolve_severity(m, None), "advisory")

    def test_boundaries_parsed(self):
        b = sensor.parse_boundaries()
        self.assertIn("phase3-phase4", b)
        p34 = b["phase3-phase4"]
        self.assertIn("yaml-validity", p34["sensors"])
        self.assertTrue(any(e["artifact"] == "livrable_tfvars_present" and "new-stack" in e["scopes"]
                            for e in p34["blocking_on_scope"]))
        self.assertEqual(p34["prerequis_40"], ["repertoire_travail_defini", "flux_kestra_accessible"])

    def test_gate_runs(self):
        self.p.write("docker-compose.yml", "services:\n  web:\n    image: nginx\n    deploy:\n      replicas: 1\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = sensor.main(["--root", str(self.p.root), "gate", "phase3-phase4", "--scope", "new-stack"])
        self.assertEqual(rc, 0)  # advisory : code 0
        self.assertIn("Rapport de vérification", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
