# Logos Sovereign Agent

A native Logos Core module for a policy-bounded autonomous agent with
verifiable wallet, storage, messaging, and A2A actions.

## Current evidence state

`native-spike / cross-platform-build-proven / runtime-load-pending`

The minimal Qt-free universal module has passed semantic contract checks and
produced both development and portable `.lgx` packages on Ubuntu 24.04 and
macOS 15. The next hard gate is installing and exercising those artifacts in
the pinned Logos Core runtime. It does **not** yet claim Basecamp integration,
a testnet agent, public demo, or LP-0008 submission.

The initial build evidence is recorded in
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

## License

MIT
