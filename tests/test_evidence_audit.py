import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDITOR_PATH = ROOT / "tools" / "audit_evidence.py"


def load_auditor():
    spec = importlib.util.spec_from_file_location("audit_evidence", AUDITOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load evidence auditor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EvidenceAuditTests(unittest.TestCase):
    def make_native_fixture(self, root: Path) -> None:
        runtime = root / "runtime-evidence"
        capability = runtime / "capability"
        negatives = runtime / "dependency-negatives"
        capability.mkdir(parents=True)
        negatives.mkdir(parents=True)

        def write_json(relative: str, value) -> None:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value) + "\n")

        (root / "flake.lock").write_text('{"version": 7}\n')
        write_json(
            "output-identities.json",
            {
                "development": {"narHash": "sha256-dev", "storePath": "/nix/dev"},
                "portable": {"narHash": "sha256-portable", "storePath": "/nix/portable"},
            },
        )
        write_json(
            "runtime-evidence/load.json",
            {
                "status": "ok",
                "module": "sovereign_agent",
                "dependencies_loaded": ["delivery_module", "chat_module"],
            },
        )
        write_json(
            "runtime-evidence/module-info.json",
            {
                "name": "sovereign_agent",
                "status": "loaded",
                "dependencies": ["chat_module"],
                "methods": [
                    {"name": "version"},
                    {"name": "status"},
                    {"name": "chatDependencyHealthy"},
                ],
            },
        )
        write_json("runtime-evidence/version-call.json", {"status": "ok", "result": "0.1.0"})
        write_json(
            "runtime-evidence/chat-health-via-declared-caller.json",
            {"status": "ok", "result": True},
        )
        write_json(
            "runtime-evidence/capability/capability-denied-token-issuance.json",
            {"status": "ok", "result": ""},
        )
        write_json(
            "runtime-evidence/capability/core-service-administrative-path.json",
            {"status": "ok", "result": True},
        )
        expected = {"module": "sovereign_agent", "state": "native_spike", "version": "0.1.0"}
        for name in (
            "status-call-before-reload.json",
            "status-call-after-reload.json",
            "status-call-after-daemon-restart.json",
        ):
            write_json(f"runtime-evidence/{name}", {"status": "ok", "result": json.dumps(expected)})
        for name in ("status-after-stop.json", "status-after-final-stop.json"):
            write_json(f"runtime-evidence/{name}", {"daemon": {"status": "not_running"}})
        (negatives / "compile-missing-declaration.txt").write_text("chat_module missing\n")
        (negatives / "runtime-missing-dependency.txt").write_text("chat_module unavailable\n")
        (runtime / "daemon.log").write_text("sanitized runtime\n")

    def test_native_evidence_auditor_accepts_complete_fixture(self) -> None:
        auditor = load_auditor()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_native_fixture(root)
            summary = auditor.audit_native(root)
        self.assertEqual(summary["classification"], "native-evidence-audited")
        self.assertEqual(summary["declaredDependencies"], ["chat_module"])

    def test_native_evidence_auditor_rejects_uuid_leak(self) -> None:
        auditor = load_auditor()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_native_fixture(root)
            (root / "runtime-evidence" / "daemon.log").write_text(
                "token 123e4567-e89b-42d3-a456-426614174000\n"
            )
            with self.assertRaisesRegex(AssertionError, "UUID-shaped"):
                auditor.audit_native(root)

    def make_basecamp_fixture(self, root: Path) -> None:
        evidence = root / "basecamp-evidence"
        evidence.mkdir(parents=True)
        expected = {"module": "sovereign_agent", "state": "native_spike", "version": "0.1.0"}
        contract = {
            "module": "sovereign_agent",
            "version": {"result": "0.1.0"},
            "status": {"result": json.dumps(expected)},
            "chatDependencyHealthy": {"result": True},
            "methods": [
                {"name": "version"},
                {"name": "status"},
                {"name": "chatDependencyHealthy"},
            ],
            "events": [{"name": "statusChanged"}],
            "unloaded": {"state": "Not loaded"},
            "reloaded": {"state": "Loaded"},
            "afterReload": {"result": json.dumps(expected)},
        }
        (root / "flake.lock").write_text('{"version": 7}\n')
        (evidence / "basecamp-contract.json").write_text(json.dumps(contract) + "\n")
        (evidence / "lgpm-info.json").write_text(
            json.dumps({"name": "sovereign_agent", "dependencies": ["chat_module"]}) + "\n"
        )
        (evidence / "artifact-sha256.txt").write_text("abc  flake.lock\n")
        (evidence / "basecamp-sovereign-agent-interface.png").write_bytes(b"png")
        (evidence / "linux-dynamic-libraries.txt").write_text("libQt6Core.so => /nix/store/lib\n")
        (evidence / "ui-test.log").write_text("sanitized Basecamp run\n")

    def test_basecamp_evidence_auditor_accepts_complete_linux_fixture(self) -> None:
        auditor = load_auditor()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_basecamp_fixture(root)
            summary = auditor.audit_basecamp(root, require_linux_ldd=True)
        self.assertEqual(summary["classification"], "basecamp-evidence-audited")
        self.assertTrue(summary["typedChatDependencyHealthy"])

    def test_basecamp_evidence_auditor_rejects_unresolved_linux_library(self) -> None:
        auditor = load_auditor()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_basecamp_fixture(root)
            (root / "basecamp-evidence" / "linux-dynamic-libraries.txt").write_text(
                "libEGL.so => not found\n"
            )
            with self.assertRaisesRegex(AssertionError, "unresolved"):
                auditor.audit_basecamp(root, require_linux_ldd=True)


if __name__ == "__main__":
    unittest.main()
