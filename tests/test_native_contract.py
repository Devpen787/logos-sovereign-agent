import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER_COMMIT = "2b59cb8e855894f7e7a064b15bfae409f288080b"
LOGOSCORE_COMMIT = "8720885dd821cd63eb1da00c842328cbfd1fe5fa"
LGPM_COMMIT = "202af6fa0f0f4493bc59c8a609dff9326f78a18d"
UPLOAD_ARTIFACT_COMMIT = "ea165f8d65b6e75b540449e92b4886f43607fa02"
BASECAMP_COMMIT = "aa237766baf61404e12da86b7303cb41065464c9"
BASECAMP_QT_MCP_COMMIT = "1fea509485a48ab185fafae8dc21bdbcc808a07e"
CHAT_COMMIT = "dfe8ccf3eff3e95da0ba54043577270474a216ae"
DELIVERY_COMMIT = "3258cdb0132e37228aa2519e0c01c0e7429a20dd"
CHAT_BUILDER_COMMIT = "8e4ea1c1d0e523cea46850f8fd9466dd35af7cc1"
LOGOSCORE_LIBLOGOS_COMMIT = "be221c5749036343909fa0b109edecfb4d329fdd"


class NativeContractTests(unittest.TestCase):
    def test_required_native_source_files_exist(self) -> None:
        for relative in (
            "metadata.json",
            "flake.nix",
            "CMakeLists.txt",
            "src/sovereign_agent_impl.h",
            "src/sovereign_agent_impl.cpp",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_metadata_declares_the_exact_chat_dependency(self) -> None:
        metadata = json.loads((ROOT / "metadata.json").read_text())
        self.assertEqual(metadata["name"], "sovereign_agent")
        self.assertEqual(metadata["version"], "0.1.0")
        self.assertEqual(metadata["type"], "core")
        self.assertEqual(metadata["interface"], "universal")
        self.assertEqual(metadata["main"], "sovereign_agent_plugin")
        self.assertEqual(metadata["dependencies"], ["chat_module"])

    def test_builder_and_chat_inputs_are_exactly_pinned(self) -> None:
        flake = (ROOT / "flake.nix").read_text()
        self.assertIn(
            f'chat_module.url = "github:logos-co/logos-chat-module/{CHAT_COMMIT}";',
            flake,
        )
        self.assertIn(
            'logos-module-builder.follows = "chat_module/logos-module-builder";',
            flake,
        )
        self.assertNotIn(f"github:logos-co/logos-module-builder/{BUILDER_COMMIT}", flake)
        self.assertNotIn('"github:logos-co/logos-module-builder";', flake)

    def test_public_spike_api_is_exact_and_qt_free(self) -> None:
        header = (ROOT / "src/sovereign_agent_impl.h").read_text()
        self.assertIn("class SovereignAgentImpl : public LogosModuleContext", header)
        methods = re.findall(r"std::string\s+(\w+)\s*\(\s*\)\s*;", header)
        self.assertEqual(methods, ["version", "status"])
        self.assertIn("bool chatDependencyHealthy();", header)
        self.assertIn("void statusChanged(const std::string& status);", header)
        for forbidden in ("QString", "QObject", "QJson", "QVariant"):
            self.assertNotIn(forbidden, header)

    def test_chat_dependency_uses_only_the_generated_typed_sdk(self) -> None:
        implementation = (ROOT / "src/sovereign_agent_impl.cpp").read_text()
        self.assertIn('#include "logos_sdk.h"', implementation)
        self.assertIn("return modules().chat_module.health();", implementation)
        for forbidden in ("LogosAPI", "QString", "QVariant", "lp_call", "invokeRemoteMethod"):
            self.assertNotIn(forbidden, implementation)

    def test_status_contract_is_deterministic(self) -> None:
        implementation = (ROOT / "src/sovereign_agent_impl.cpp").read_text()
        self.assertIn('return "0.1.0";', implementation)
        self.assertIn('"module":"sovereign_agent"', implementation)
        self.assertIn('"state":"native_spike"', implementation)
        self.assertIn("statusChanged(result);", implementation)

    def test_native_workflow_pins_and_exercises_the_evaluator_lane(self) -> None:
        workflow = (ROOT / ".github/workflows/native-spike.yml").read_text()
        for commit in (LOGOSCORE_COMMIT, LGPM_COMMIT, UPLOAD_ARTIFACT_COMMIT):
            self.assertIn(commit, workflow)
        for commit in (CHAT_COMMIT, DELIVERY_COMMIT, LOGOSCORE_LIBLOGOS_COMMIT):
            self.assertIn(commit, workflow)
        for required_command in (
            "nix flake lock",
            "nix path-info --json ./result-lgx ./result-lgx-portable",
            'assert all(record.get("narHash") for record in records)',
            '"development": record_for("result-lgx")',
            '"portable": record_for("result-lgx-portable")',
            "install --file",
            "#cli-portable",
            "--require-signatures",
            "expect_rejection signature-required",
            "expect_rejection dev-cli-rejects-portable",
            "expect_rejection portable-cli-rejects-dev",
            "expect_rejection corrupt-archive",
            "load-module sovereign_agent",
            "module-info sovereign_agent --json",
            "call sovereign_agent version --json",
            "call sovereign_agent status --json",
            "call sovereign_agent chatDependencyHealthy --json",
            "--access-policy",
            "undeclared-caller-denied",
            "reload-module sovereign_agent",
            "status-after-daemon-restart.json",
            "status-call-after-daemon-restart.json",
            "status-after-stop.json",
            "Sanitize captured runtime logs",
            "<redacted-uuid>",
        ):
            self.assertIn(required_command, workflow)
        self.assertIn('stopped["daemon"]["status"] == "not_running"', workflow)
        self.assertNotIn("nix hash path ./result-lgx", workflow)
        self.assertIn("output-identities.json", workflow)
        self.assertNotIn("unexpectedly remained running", workflow)

    def test_lane_lock_records_runtime_security_truth(self) -> None:
        lane = json.loads((ROOT / "docs/evaluator-lane-lock.json").read_text())
        self.assertEqual(lane["nativeModules"]["chat"]["commit"], CHAT_COMMIT)
        self.assertEqual(lane["nativeModules"]["delivery"]["commit"], DELIVERY_COMMIT)
        capability = lane["capabilityEnforcement"]
        self.assertEqual(
            capability["logoscore"]["liblogosCommit"], LOGOSCORE_LIBLOGOS_COMMIT
        )
        self.assertEqual(capability["logoscore"]["status"], "enforced-in-headless-lane")
        self.assertEqual(capability["basecamp"]["status"], "explicitly-disabled")
        self.assertFalse(capability["basecamp"]["equivalentToHeadless"])

    def test_basecamp_workflow_drives_the_same_public_contract(self) -> None:
        workflow = (ROOT / ".github/workflows/basecamp-spike.yml").read_text()
        ui_test = (ROOT / "tests/basecamp_native_spike.mjs").read_text()
        for commit in (
            BASECAMP_COMMIT,
            BASECAMP_QT_MCP_COMMIT,
            LGPM_COMMIT,
            UPLOAD_ARTIFACT_COMMIT,
        ):
            self.assertIn(commit, workflow)
        for required_contract in (
            "Sovereign Agent",
            "sovereign_agent",
            "version",
            "status",
            "statusChanged",
            "native_spike",
        ):
            self.assertIn(required_contract, ui_test)
        self.assertIn("cli-portable", workflow)
        self.assertIn("bin-bundle-dir-inspector", workflow)
        self.assertIn("libopengl0", workflow)
        self.assertIn("libegl1", workflow)
        self.assertIn("ldd result-basecamp/bin/.LogosBasecamp.elf", workflow)
        self.assertIn("basecamp-evidence/linux-dynamic-libraries.txt", workflow)
        self.assertIn("basecamp_native_spike.mjs", workflow)
        self.assertIn("Sanitize captured runtime logs", workflow)
        self.assertIn("<redacted-uuid>", workflow)
        self.assertIn("waitForModuleState", ui_test)
        self.assertIn('"Not loaded"', ui_test)
        self.assertNotIn('unloaded.error !== "Module not connected"', ui_test)
        self.assertNotIn("+            ", workflow)

    def test_repository_has_no_local_path_or_secret_markers(self) -> None:
        forbidden = (
            "/Users/",
            "BEGIN PRIVATE KEY",
            "BEGIN OPENSSH PRIVATE KEY",
            "seed phrase",
            "mnemonic=",
        )
        policy_exceptions = {
            Path("AGENTS.md"),
            Path("SECURITY.md"),
            Path("tests/test_native_contract.py"),
        }
        skipped = {".git", "__pycache__", "result", "result-lgx", "result-lgx-portable"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or any(part in skipped for part in path.parts):
                continue
            if path.relative_to(ROOT) in policy_exceptions:
                continue
            try:
                content = path.read_text()
            except UnicodeDecodeError:
                continue
            for marker in forbidden:
                self.assertNotIn(marker, content, f"{marker!r} in {path.relative_to(ROOT)}")


if __name__ == "__main__":
    unittest.main()
