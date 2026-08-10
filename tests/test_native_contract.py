import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER_COMMIT = "2b59cb8e855894f7e7a064b15bfae409f288080b"
LOGOSCORE_COMMIT = "8720885dd821cd63eb1da00c842328cbfd1fe5fa"
LGPM_COMMIT = "202af6fa0f0f4493bc59c8a609dff9326f78a18d"
UPLOAD_ARTIFACT_COMMIT = "ea165f8d65b6e75b540449e92b4886f43607fa02"


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

    def test_metadata_is_minimal_universal_core_module(self) -> None:
        metadata = json.loads((ROOT / "metadata.json").read_text())
        self.assertEqual(metadata["name"], "sovereign_agent")
        self.assertEqual(metadata["version"], "0.1.0")
        self.assertEqual(metadata["type"], "core")
        self.assertEqual(metadata["interface"], "universal")
        self.assertEqual(metadata["main"], "sovereign_agent_plugin")
        self.assertEqual(metadata["dependencies"], [])

    def test_builder_input_is_commit_pinned(self) -> None:
        flake = (ROOT / "flake.nix").read_text()
        self.assertIn(
            f"github:logos-co/logos-module-builder/{BUILDER_COMMIT}", flake
        )
        self.assertNotIn('"github:logos-co/logos-module-builder";', flake)

    def test_public_spike_api_is_exact_and_qt_free(self) -> None:
        header = (ROOT / "src/sovereign_agent_impl.h").read_text()
        self.assertIn("class SovereignAgentImpl : public LogosModuleContext", header)
        methods = re.findall(r"std::string\s+(\w+)\s*\(\s*\)\s*;", header)
        self.assertEqual(methods, ["version", "status"])
        self.assertIn("void statusChanged(const std::string& status);", header)
        for forbidden in ("QString", "QObject", "QJson", "QVariant"):
            self.assertNotIn(forbidden, header)

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
        for required_command in (
            "nix flake lock",
            "install --file",
            "load-module sovereign_agent",
            "module-info sovereign_agent --json",
            "call sovereign_agent version --json",
            "call sovereign_agent status --json",
            "reload-module sovereign_agent",
            "status-after-stop.json",
        ):
            self.assertIn(required_command, workflow)

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
