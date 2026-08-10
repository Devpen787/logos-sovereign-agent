# Logos Sovereign Agent

A native Logos Core module for a policy-bounded autonomous agent with
verifiable wallet, storage, messaging, and A2A actions.

## Current evidence state

`native-spike / local-contract-only`

The repository currently contains the minimal Qt-free universal-module source
and semantic contract tests. It does **not** yet claim a successful Nix build,
`.lgx` package, Logos Core load, Basecamp integration, testnet agent, public
demo, or LP-0008 submission.

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
