# Logos Sovereign Agent

A native Logos Core module for a policy-bounded autonomous agent with
verifiable wallet, storage, messaging, and A2A actions.

## Current evidence state

`native-spike / declared-composition-and-basecamp-dual-host-proven / corrected-gates-candidate`

The minimal Qt-free universal module has passed semantic contract checks and
produced both development and portable `.lgx` packages on Ubuntu 24.04 and
macOS 15. The pinned Logos Core runtime and exact Basecamp 0.2.3 Module
Inspector have both completed the minimal lifecycle on both hosts. Exact Chat
and transitive Delivery composition through generated typed glue has also
passed the headless and Basecamp paths on both hosts. The corrected policy
negative and official-reference gates remain pending in the next candidate.
It does **not** yet claim a testnet agent, public release, prize readiness, or
an LP-0008 submission.

The build and runtime evidence is recorded in
[`docs/native-spike-build-evidence-2026-08-10.md`](docs/native-spike-build-evidence-2026-08-10.md).

## First proof target

```text
official minimal-module parity
-> build development and portable .lgx
-> install in matching hosts
-> prove process liveness and method discovery
-> call version and status
-> reload and restart
-> repeat in logoscore and Basecamp
-> prove declared dependency and capability-policy boundaries
-> pass unmodified official Chat and LEZ reference specifications
```

## Contract check

```bash
python3 -m unittest discover -s tests -v
```

## Native build

Requires Nix with flakes enabled:

```bash
nix build .#lgx
nix build .#lgx-portable
```

The build input is pinned to the exact Module Builder commit recorded in
[`docs/evaluator-lane-lock.json`](docs/evaluator-lane-lock.json).

## Evidence audit

After downloading and extracting a successful `native-spike-*` artifact, run
the independent fail-closed verifier against its root:

```bash
python3 tools/audit_evidence.py /path/to/extracted-artifact --json
python3 tools/audit_evidence.py /path/to/basecamp-artifact --kind basecamp --require-linux-ldd --json
```

It verifies the labeled NAR identities, declared dependency closure, typed Chat
call, peer capability denial, lifecycle/restart records, negative dependency
tests, Basecamp unload/reload contract, optional Linux dynamic closure, and log
sanitization.

## License

MIT
