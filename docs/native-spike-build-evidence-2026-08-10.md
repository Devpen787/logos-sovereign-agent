# Native spike build evidence — 2026-08-10

## Classification

`minimal-contract-dual-host-logoscore-and-basecamp-proven / protocol-composition-pending`

The source and gate at commit
`0fc38dc02dcc91fc0c786dce006ee9511d922c7d` completed the public contract
and native-spike workflows on Ubuntu 24.04 and macOS 15. Run
[`31404402665`](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665)
then proved the same portable package through the real Basecamp 0.2.3 Module
Inspector on both hosts, including method/event discovery, calls, unload, and
reload. It does not prove protocol composition, capability-policy parity,
testnet deployment, or prize readiness.

## Public evidence

- Pull request: [#1](https://github.com/Devpen787/logos-sovereign-agent/pull/1)
- Contract workflow: [run 31395410117](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410117)
- Native runtime workflow: [run 31395410267](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267)
- Linux job: [93476957618](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/job/93476957618)
- macOS job: [93476957501](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/job/93476957501)
- Linux evidence artifact: [9065899299](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/artifacts/9065899299), retained through 2026-09-09
- macOS evidence artifact: [9065876532](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31395410267/artifacts/9065876532), retained through 2026-09-09
- Basecamp workflow: [run 31404402665](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665)
- Basecamp Linux job: [93507057966](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665/job/93507057966)
- Basecamp macOS job: [93507057950](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665/job/93507057950)
- Basecamp Linux artifact: [9069852891](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665/artifacts/9069852891), retained through 2026-09-09
- Basecamp macOS artifact: [9070004456](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402665/artifacts/9070004456), retained through 2026-09-09

## Exact output identities

The generated dependency lock has SHA-256
`5d25b56a124cb93601c8b203d703da5946137bdd8e4a857c3110f169a86db7f2`
on both hosts.

| Host | Variant | LGX SHA-256 |
|---|---|---|
| Ubuntu 24.04 | development, `linux-amd64-dev` | `fae8f8a80d4562387e12be640de8351ae8fe4a4640426da231edd8a0b542d86b` |
| Ubuntu 24.04 | portable, `linux-amd64` | `bf4fe21b9066bbfe79638985ee5c4e1d9832399e55a4a8f9e9d836461c548360` |
| macOS 15 | development, `darwin-arm64-dev` | `fd4bf28fd64c22d085e27e3b0cbe53f2dbb1bcc141334751d510d92de94b2966` |
| macOS 15 | portable, `darwin-arm64` | `431a0143007f714bf78ebbf127eadf823c8ce19a6d1964440b9df11472ecca10` |

Each output contains `logos-sovereign_agent-module-lib.lgx`.

An earlier revision mislabeled values from `nix hash path` over the result
links as the NAR identities of the two outputs. Those four claims are
withdrawn. Commit `d828039b72c9ccefd6cfd901256bd4e3cc2e0770` changes the
collector to use `nix path-info --json` and fails the job unless both output
records contain a `narHash`. No replacement NAR values are claimed here until
the collector emits an explicit development/portable mapping. Run
[`31404402750`](https://github.com/Devpen787/logos-sovereign-agent/actions/runs/31404402750)
contains two valid `narHash` records per host, but the unlabeled pair is not
being mapped by path order or inferred size.

## Runtime assertions

Both host jobs proved all of the following against exact pinned releases:

- unsigned development-package installation with `lgpm` 0.2.1 source commit
  `202af6fa0f0f4493bc59c8a609dff9326f78a18d`;
- daemon startup with the bundled capability module;
- discovery before load and `loaded` state after load;
- method and event introspection for `version`, `status`, and `statusChanged`;
- deterministic calls before and after reload;
- process statistics while loaded; and
- clean stop followed by `daemon.status == not_running`.

## Disclosed findings

The exact Basecamp run proves runtime viability on Ubuntu, but it predates the
explicit Linux `ldd` closure assertion now staged in the next candidate. Do
not relabel successful UI execution as a captured dependency-closure record.

Exact Basecamp 0.2.3 calls `logos_core_set_access_policy(nullptr)` and explains
that policy enforcement is temporarily disabled because QML callers are not
represented in the module dependency graph. The frozen Logos Core flake,
despite stale README/source comments saying policy is a no-op, resolves its
root `logos-liblogos_8` input to commit
`be221c5749036343909fa0b109edecfb4d329fdd`, which implements parsed enforce
policies and derived caller restrictions. Capability denial therefore must be
proved in the headless lane and disclosed as non-equivalent in Basecamp.

The Basecamp logs expose process-local UUID tokens while the runtime is alive.
They are invalid after process exit, but future evidence collectors redact all
UUID-shaped values from captured `.log` and `.txt` files before upload. The two
already-published minimal-contract artifacts are retained as historical
evidence and are not described as sanitized.

The macOS portable bundler reported embedded `/nix/` strings in the module and
OpenSSL binary data, then classified all references as portable. The module
has not yet been run outside Nix, so this remains an explicit portability risk
rather than a closed finding.

The macOS daemon also logged a missing `eventResponse(QString, QVariantList)`
signal while initializing Logos Core's bundled capability module. The
sovereign-agent provider loaded, forwarded its own event, reloaded, and stopped
successfully. The warning is retained as upstream host evidence.

The first runtime-gate run correctly produced all successful lifecycle records
but ended red because the verifier assumed post-stop `status` must exit
non-zero. Pinned Logos Core returned the correct `not_running` JSON with exit
code zero. Commit `0fc38dc` changed the gate to assert the returned state; the
fresh two-host run is green.

GitHub currently warns that the pinned latest `actions/upload-artifact` v7.0.1
action declares Node.js 20 while the runner forces Node.js 24. Artifact upload
completed on both hosts. This is a CI-maintenance warning, not module evidence.

## Next gate

Build the exact Chat 0.2.2 and Delivery 0.2.0 dependencies, prove the generated
typed `modules().chat_module.health()` call in both hosts, prove an explicit
undeclared-caller denial in Logos Core, repeat the Basecamp UI lifecycle with
the composed package set, capture the Linux dynamic-library closure, and
sanitize all uploaded logs. No product feature work begins from this result
alone.
