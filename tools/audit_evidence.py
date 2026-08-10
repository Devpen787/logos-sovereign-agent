#!/usr/bin/env python3
"""Independently verify a downloaded native-spike evidence artifact."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


UUID = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
)
EXPECTED_STATUS = {
    "module": "sovereign_agent",
    "state": "native_spike",
    "version": "0.1.0",
}


def read_json(root: Path, relative: str):
    path = root / relative
    assert path.is_file(), f"missing evidence file: {relative}"
    return json.loads(path.read_text())


def require_nonempty(root: Path, relative: str) -> None:
    path = root / relative
    assert path.is_file(), f"missing evidence file: {relative}"
    assert path.stat().st_size > 0, f"empty evidence file: {relative}"


def assert_sanitized(root: Path) -> None:
    leaks = []
    for captured in root.rglob("*"):
        if not captured.is_file() or captured.suffix not in {".log", ".txt"}:
            continue
        if UUID.search(captured.read_text(errors="replace")):
            leaks.append(str(captured.relative_to(root)))
    assert not leaks, f"UUID-shaped values remain in evidence: {leaks}"


def audit_native(root: Path) -> dict:
    root = root.resolve()
    require_nonempty(root, "flake.lock")

    identities = read_json(root, "output-identities.json")
    assert set(identities) == {"development", "portable"}, identities
    for variant, identity in identities.items():
        assert identity.get("narHash"), f"{variant} lacks narHash"
        assert identity.get("storePath"), f"{variant} lacks storePath"

    load = read_json(root, "runtime-evidence/load.json")
    assert load.get("status") == "ok", load
    assert load.get("module") == "sovereign_agent", load
    assert set(load.get("dependencies_loaded", [])) == {
        "chat_module",
        "delivery_module",
    }, load

    info = read_json(root, "runtime-evidence/module-info.json")
    assert info.get("name") == "sovereign_agent", info
    assert info.get("status") == "loaded", info
    assert info.get("dependencies") == ["chat_module"], info
    methods = {method.get("name") for method in info.get("methods", [])}
    assert {"version", "status", "chatDependencyHealthy"}.issubset(methods), info

    version = read_json(root, "runtime-evidence/version-call.json")
    assert version == {
        "method": "version",
        "module": "sovereign_agent",
        "result": "0.1.0",
        "status": "ok",
    } or (version.get("status") == "ok" and version.get("result") == "0.1.0"), version

    health = read_json(root, "runtime-evidence/chat-health-via-declared-caller.json")
    assert health.get("status") == "ok" and health.get("result") is True, health

    denied = read_json(
        root,
        "runtime-evidence/capability/capability-denied-token-issuance.json",
    )
    assert denied.get("status") == "ok" and denied.get("result") == "", denied

    administrative = read_json(
        root,
        "runtime-evidence/capability/core-service-administrative-path.json",
    )
    assert administrative.get("status") == "ok", administrative
    assert administrative.get("result") is True, administrative

    for name in (
        "status-call-before-reload.json",
        "status-call-after-reload.json",
        "status-call-after-daemon-restart.json",
    ):
        status = read_json(root, f"runtime-evidence/{name}")
        assert status.get("status") == "ok", status
        assert json.loads(status["result"]) == EXPECTED_STATUS, status

    for name in ("status-after-stop.json", "status-after-final-stop.json"):
        stopped = read_json(root, f"runtime-evidence/{name}")
        assert stopped["daemon"]["status"] == "not_running", stopped

    for relative in (
        "runtime-evidence/dependency-negatives/compile-missing-declaration.txt",
        "runtime-evidence/dependency-negatives/runtime-missing-dependency.txt",
    ):
        require_nonempty(root, relative)

    assert_sanitized(root / "runtime-evidence")
    return {
        "classification": "native-evidence-audited",
        "declaredDependencies": info["dependencies"],
        "loadedDependencyClosure": sorted(load["dependencies_loaded"]),
        "narHashes": {
            variant: identity["narHash"] for variant, identity in identities.items()
        },
        "peerCapabilityDenial": "empty-token",
        "coreServicePath": "administrative-call-succeeded",
    }


def audit_basecamp(root: Path, require_linux_ldd: bool = False) -> dict:
    root = root.resolve()
    evidence = root / "basecamp-evidence"
    require_nonempty(root, "flake.lock")
    require_nonempty(root, "basecamp-evidence/artifact-sha256.txt")
    require_nonempty(root, "basecamp-evidence/basecamp-sovereign-agent-interface.png")

    info = read_json(root, "basecamp-evidence/lgpm-info.json")
    assert info.get("name") == "sovereign_agent", info
    assert info.get("dependencies") == ["chat_module"], info

    contract = read_json(root, "basecamp-evidence/basecamp-contract.json")
    assert contract.get("module") == "sovereign_agent", contract
    assert contract["version"].get("result") == "0.1.0", contract["version"]
    assert contract["chatDependencyHealthy"].get("result") is True, contract

    methods = {method.get("name") for method in contract.get("methods", [])}
    events = {event.get("name") for event in contract.get("events", [])}
    assert {"version", "status", "chatDependencyHealthy"}.issubset(methods), contract
    assert "statusChanged" in events, contract
    assert json.loads(contract["status"]["result"]) == EXPECTED_STATUS, contract
    assert json.loads(contract["afterReload"]["result"]) == EXPECTED_STATUS, contract
    assert contract["unloaded"].get("state") == "Not loaded", contract
    assert contract["reloaded"].get("state") == "Loaded", contract

    if require_linux_ldd:
        relative = "basecamp-evidence/linux-dynamic-libraries.txt"
        require_nonempty(root, relative)
        dynamic_libraries = (root / relative).read_text(errors="replace")
        assert "not found" not in dynamic_libraries, "unresolved Linux dynamic library"

    assert_sanitized(evidence)
    return {
        "classification": "basecamp-evidence-audited",
        "declaredDependencies": info["dependencies"],
        "typedChatDependencyHealthy": True,
        "unloadReload": "passed",
        "linuxDynamicClosure": "passed" if require_linux_ldd else "not-applicable",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_dir", type=Path)
    parser.add_argument("--kind", choices=("native", "basecamp"), default="native")
    parser.add_argument("--require-linux-ldd", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not __debug__:
        print(
            f"{args.kind} evidence audit: FAIL: Python assertions are disabled",
            file=sys.stderr,
        )
        return 1
    try:
        if args.kind == "native":
            summary = audit_native(args.evidence_dir)
        else:
            summary = audit_basecamp(
                args.evidence_dir,
                require_linux_ldd=args.require_linux_ldd,
            )
    except (AssertionError, json.JSONDecodeError, KeyError) as error:
        print(f"{args.kind} evidence audit: FAIL: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"{args.kind} evidence audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
